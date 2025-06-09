#!/usr/bin/env python3
import os
import json
import base64
import random
import shutil
import requests
from PIL import Image
import io
import argparse
import time
import zipfile
from dotenv import load_dotenv
import hashlib
import glob

# Configuration
OUTPUT_SITE_DIR = "./output_site"
OUTPUT_IMAGES_DIR = "./output_images" # Base for _data.json files and SFW images
NSFW_IMAGES_DIR_BASE = f"{OUTPUT_IMAGES_DIR}/nsfw_gallery" # Dedicated base for NSFW images
ARTISTS_FILE = "artists.txt"
NSFW_PROMPTS_FILE = "nsfw.txt" # For NSFW prompts
TEMPLATE_FILE = "template.prompt"
API_URL = "https://image.novelai.net"

# Define all possible gallery sections in one place
ALL_SECTIONS_CONFIG = {
    "women": {
        "id": "women", "name": "Women", "file": "1girl.txt", "max_images": 45000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/full", "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/thumb", "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/raw",
        "is_nsfw": False, "type": "standard"
    },
    "men": {
        "id": "men", "name": "Men", "file": "1boy.txt", "max_images": 5000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/full", "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/thumb", "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/raw",
        "is_nsfw": False, "type": "standard"
    },
    "nsfw": {
        "id": "nsfw", "name": "NSFW Zone", "file": NSFW_PROMPTS_FILE, "max_images": 24000,
        "images_dir_full": f"{NSFW_IMAGES_DIR_BASE}/full", "images_dir_thumb": f"{NSFW_IMAGES_DIR_BASE}/thumb", "images_dir_raw": f"{NSFW_IMAGES_DIR_BASE}/raw",
        "is_nsfw": True, "type": "standard"
    },
    "noncon": {
        "id": "noncon", "name": "Non-Con Gallery", "file": "prompts_gemini.json", "max_images": 24000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/noncon/full", "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/noncon/thumb", "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/noncon/raw",
        "is_nsfw": True, "type": "v4_structured", "unlinked": True
    }
}

# CONFIG VARIABLES
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Define models to use
MODELS = [
    {"id": "nai-diffusion-4-full", "name": "NAI Diffusion 4 Full"},
    {"id": "nai-diffusion-4-curated-preview", "name": "NAI Diffusion 4 Curated"},
    {"id": "nai-diffusion-4-5-curated", "name": "NAI Diffusion 4.5 Curated"},
    {"id": "nai-diffusion-4-5-full", "name": "NAI Diffusion 4.5 Full"},
]

def setup_directories():
    os.makedirs(OUTPUT_SITE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)
    for section_cfg in ALL_SECTIONS_CONFIG.values():
        os.makedirs(section_cfg["images_dir_full"], exist_ok=True)
        os.makedirs(section_cfg["images_dir_thumb"], exist_ok=True)
        os.makedirs(section_cfg["images_dir_raw"], exist_ok=True)
    for folder in ["css", "js"]:
        src, dest = f"./{folder}", f"{OUTPUT_SITE_DIR}/{folder}"
        if os.path.exists(src):
            if os.path.exists(dest): shutil.rmtree(dest)
            shutil.copytree(src, dest)

def read_artists():
    if not os.path.exists(ARTISTS_FILE):
        print(f"Warning: {ARTISTS_FILE} not found."); return []
    with open(ARTISTS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def read_template():
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Error: {TEMPLATE_FILE} not found.")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def login(api_key=None):
    credentials_file, env_var_names = ".nai_credentials.json", ["NAI_PERSISTENT_TOKEN", "NAI_PERSISTENT_API_KEY"]
    load_dotenv()
    if api_key: return {"Authorization": f"Bearer {api_key}"}
    for var in env_var_names:
        if token := os.getenv(var): return {"Authorization": f"Bearer {token}"}
    if os.path.exists(credentials_file):
        try:
            with open(credentials_file, "r") as f: return {"Authorization": f"Bearer {json.load(f)['accessToken']}"}
        except Exception: pass
    email = input("Enter NovelAI email (or API Key): ")
    auth_url, auth_headers, auth_payload = f"{API_URL}/user", {}, {}
    if "@" not in email and len(email) > 60:
        auth_url += "/create-persistent-token"; auth_headers = {"Authorization": f"Bearer {email}"}
    else:
        auth_url += "/login"; auth_payload = {"email": email, "password": input("Enter NovelAI password: ")}
    try:
        response = requests.post(auth_url, json=auth_payload, headers=auth_headers)
        response.raise_for_status(); data = response.json()
        with open(credentials_file, "w") as f: json.dump({"accessToken": data['accessToken']}, f)
        print("Login/Auth successful. Token cached.")
        return {"Authorization": f"Bearer {data['accessToken']}"}
    except Exception as e:
        raise Exception(f"Authentication failed: {e}")

def _save_image_files(img_bytes, filename_stem, dirs):
    img = Image.open(io.BytesIO(img_bytes))
    with open(os.path.join(dirs['raw'], f"{filename_stem}.png"), "wb") as f: f.write(img_bytes)
    full_size, thumb_size = (int(img.width*0.7), int(img.height*0.7)), (int(img.width*0.35), int(img.height*0.35))
    for path, size in [(os.path.join(dirs['full'], f"{filename_stem}.jpg"), full_size), (os.path.join(dirs['thumb'], f"{filename_stem}.jpg"), thumb_size)]:
        thumb = img.copy(); thumb.thumbnail(size, Image.Resampling.LANCZOS)
        thumb.convert("RGB").save(path, "JPEG", quality=80)
    return True

def _api_request(payload, headers, filename_base, dirs):
    try:
        response = requests.post(f"{API_URL}/ai/generate-image", headers=headers, json=payload)
        response.raise_for_status()
        zip_bytes = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_bytes, 'r') as zf:
            if not zf.namelist(): raise Exception("Empty zip from API")
            img_name = next((n for n in zf.namelist() if n.startswith('image_')), zf.namelist()[0])
            _save_image_files(zf.read(img_name), f"{filename_base}_{payload['parameters']['seed']}", dirs)
        return True
    except Exception as e:
        print(f"API request error for {filename_base}: {e}")
        if hasattr(e, 'response'): print(f"Response: {e.response.text}")
        return False

def generate_image_v3(prompt, headers, filename_base, model_id, dirs, is_nsfw=False):
    seed = random.randint(1, 2147483647)
    base_prompt = f"{prompt}, no text, best quality, masterpiece, very aesthetic, absurdres"
    neg = "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page"
    if is_nsfw: neg += ", shota, child"
    else: neg = "nsfw, " + neg
    payload = {"input": base_prompt, "model": model_id, "action": "generate", "parameters": { "params_version": 3, "width": 832, "height": 1216, "scale": 6, "sampler": "k_dpmpp_2m_sde", "steps": 28, "n_samples": 1, "ucPreset": 0, "qualityToggle": True, "seed": seed, "negative_prompt": neg}}
    print(f"Generating V3 image for: {filename_base} (seed: {seed})")
    if _api_request(payload, headers, filename_base, dirs):
        return {"filename_stem": f"{filename_base}_{seed}", "seed": seed}
    return None

def generate_image_v4(prompt_obj, artist, headers, filename_base, model_id, dirs):
    seed = random.randint(1, 2147483647)
    base_prompt = f"by {artist}, very aesthetic, masterpiece, absurdres, no text, {prompt_obj['prompt']}"
    neg = "lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page"
    payload = {
        "input": base_prompt, "model": model_id, "action": "generate",
        "parameters": {
            "params_version": 3, "width": 832, "height": 1216, "scale": 5, "sampler": "k_euler_ancestral", "steps": 23, "n_samples": 1, "ucPreset": 0, "qualityToggle": True, "seed": seed,
            "v4_prompt": {"caption": {"base_caption": base_prompt, "char_captions": [{"char_caption": prompt_obj['character1'], "centers": [{"x": 0.5, "y": 0.5}]}, {"char_caption": prompt_obj['character2'], "centers": [{"x": 0.5, "y": 0.5}]}]}, "use_coords": False, "use_order": True},
            "v4_negative_prompt": {"caption": {"base_caption": neg, "char_captions": [{"char_caption": ""}, {"char_caption": ""}]}},
            "characterPrompts": [{"prompt": prompt_obj['character1'], "uc": ""}, {"prompt": prompt_obj['character2'], "uc": ""}],
            "negative_prompt": neg
        }}
    print(f"Generating V4 image for: {filename_base} (seed: {seed})")
    if _api_request(payload, headers, filename_base, dirs):
        return {"filename_stem": f"{filename_base}_{seed}", "seed": seed}
    return None

def process_section_generation(section_config, headers, artists, template_text):
    section_id = section_config["id"]
    max_images = section_config["max_images"]
    data_file = f"{OUTPUT_IMAGES_DIR}/{section_id}_data.json"
    dirs = {"full": section_config["images_dir_full"], "thumb": section_config["images_dir_thumb"], "raw": section_config["images_dir_raw"]}
    
    final_results, processed_hashes = [], set()
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            final_results = json.load(f)
        processed_hashes.update(item.get('prompt_hash') for item in final_results)
        print(f"Loaded {len(final_results)} existing records for '{section_id}'.")
    
    num_to_generate = max_images - len(final_results)
    if num_to_generate <= 0:
        print(f"Section '{section_id}' is full. No new generation needed.")
        return final_results
    
    prompt_file = section_config['file']
    if not os.path.exists(prompt_file):
        print(f"Warning: Prompt file '{prompt_file}' not found for section '{section_id}'. Skipping generation.")
        return final_results
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompts = json.load(f) if prompt_file.endswith('.json') else [line.strip() for line in f if line.strip()]
    
    available_prompts = [p for p in prompts if (hashlib.md5(json.dumps(p, sort_keys=True).encode() if isinstance(p, dict) else p.encode()).hexdigest()[:10]) not in processed_hashes]
    random.shuffle(available_prompts)
    print(f"Attempting to generate {num_to_generate} new images for '{section_id}' from {len(available_prompts)} available prompts.")

    newly_added_count = 0
    MODEL_ID = "nai-diffusion-4-5-full"
    model_id_str = MODEL_ID.replace("nai-diffusion-", "").replace("-", "_")

    for p_item in available_prompts:
        if newly_added_count >= num_to_generate: break
        
        artist = random.choice(artists)
        is_structured = isinstance(p_item, dict)
        prompt_hash = hashlib.md5(json.dumps(p_item, sort_keys=True).encode() if is_structured else p_item.encode()).hexdigest()[:10]
        filename_base = f"{section_id}_{prompt_hash}_{model_id_str}"
        
        if is_structured: # V4 Path
            image_details = generate_image_v4(p_item, artist, headers, filename_base, MODEL_ID, dirs)
            prompt_text = f"by {artist}, very aesthetic, masterpiece, absurdres, no text, {p_item['prompt']}"
        else: # V3 Path
            prompt_text = f"{template_text.replace('{{prompt}}', p_item).replace('{{artist}}', artist)}, nsfw, uncensored" if section_config['is_nsfw'] else template_text.replace('{{prompt}}', p_item).replace('{{artist}}', artist)
            image_details = generate_image_v3(prompt_text, headers, filename_base, MODEL_ID, dirs, section_config['is_nsfw'])

        if image_details:
            image_data = {
                "id": image_details["filename_stem"], "filename_base": filename_base, "artist": artist,
                "prompt": prompt_text, "model": MODEL_ID, "modelName": next(m["name"] for m in MODELS if m["id"] == MODEL_ID),
                "seed": image_details["seed"], "prompt_hash": prompt_hash
            }
            if is_structured:
                image_data["prompt_structured"] = p_item
            
            final_results.append(image_data)
            processed_hashes.add(prompt_hash)
            newly_added_count += 1
            with open(data_file, "w", encoding="utf-8") as f: json.dump(final_results, f, indent=2)
            time.sleep(0.5)

    print(f"Finished '{section_id}' generation. Added {newly_added_count} new images. Total: {len(final_results)}.")
    return final_results

def generate_nsfw_landing_page(output_site_dir, section_id, section_name):
    landing_file = f"{output_site_dir}/{section_id}_landing.html"
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Warning: {section_name} Content</title><link rel="stylesheet" href="css/style.css"><style>body{{display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;text-align:center;background-color:#1a1a2e;color:#e0e0e0;font-family:'Segoe UI',sans-serif;padding:1rem}}.disclaimer-box{{background-color:#24243e;padding:2rem 3rem;border-radius:10px;box-shadow:0 10px 25px rgba(0,0,0,0.5);max-width:650px;border:1px solid #4a4a70}}h1{{color:#ff4757;margin-bottom:1.5rem;font-size:2rem;text-transform:uppercase}}p{{margin-bottom:1.5rem;line-height:1.7;font-size:1.05rem}}strong{{color:#ffa502}}.actions a{{display:inline-block;background-color:#2ecc71;color:white;padding:.9rem 1.8rem;text-decoration:none;border-radius:5px;margin:.5rem;transition:all .2s ease;font-weight:700;text-transform:uppercase}}.actions a:hover{{background-color:#27ae60;transform:translateY(-2px)}}.actions a.exit{{background-color:#7f8c8d}}.actions a.exit:hover{{background-color:#6c7a7b}}</style></head><body><div class="disclaimer-box"><span style="font-size: 2.5rem; color: #ff4757;">🔞</span><h1>Adult Content Warning</h1><p>The section "<strong>{section_name}</strong>" contains sexually explicit material intended for adults only. This content may be NSFW.</p><p>You must be <strong>18 years of age or older</strong> to proceed. If you are not of legal age, or if such material is illegal in your location, please exit now.</p><p>By clicking "Enter", you affirm you meet these requirements.</p><div class="actions"><a href="{section_id}.html">Enter (I Confirm I Am 18+)</a><a href="index.html" class="exit">Exit</a></div></div></body></html>"""
    with open(landing_file, "w", encoding="utf-8") as f: f.write(html)
    print(f"Generated NSFW landing page: {landing_file}")

def generate_section_html(section_config, images_data, template_text):
    section_id, section_name, is_nsfw = section_config["id"], section_config["name"], section_config["is_nsfw"]
    title = f"NovelAI Gallery | {section_name}"
    html_filename = f"{OUTPUT_SITE_DIR}/{section_id}.html"

    images_data_for_js = []
    for img in images_data:
        model_name = img.get("modelName", next((m['name'] for m in MODELS if m['id'] == img.get('model')), "Unknown"))
        img_js = {"id": img["id"], "artist": img.get("artist", "N/A"), "model": img.get("model"), "modelName": model_name, "prompt": img.get("prompt"), "seed": img.get("seed")}
        if 'prompt_structured' in img:
            img_js['prompt_structured'] = img['prompt_structured']
        images_data_for_js.append(img_js)

    nav_links_html = ""
    for s_nav in [s for s in ALL_SECTIONS_CONFIG.values() if not s.get("unlinked")]:
        is_active = 'class="active"' if s_nav["id"] == section_id else ''
        link_href = f'{s_nav["id"]}_landing.html' if s_nav["is_nsfw"] else f'{s_nav["id"]}.html'
        nav_links_html += f'<li {is_active}><a href="{link_href}">{s_nav["name"]}</a></li>'
    if not nav_links_html: nav_links_html = f'<li><a href="index.html">Back</a></li>'
    
    js_data = f"""const galleryData = {{ "sectionImages": {json.dumps(images_data_for_js)}, "template": {json.dumps(template_text)}, "section": "{section_id}", "isNsfwSection": {json.dumps(is_nsfw)} }};"""

    html_content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><link rel="stylesheet" href="css/style.css"></head><body>
    <div id="age-disclaimer-overlay" style="display: none;"><div id="age-disclaimer-modal"><h2>Age Verification</h2><p>You must be 18 years or older to view this content.</p><button id="age-confirm-button">I am 18 or older</button><button id="age-exit-button">Exit</button></div></div>
    <header><div class="logo-container"><h1>{title}</h1></div><div class="site-navigation"><nav><ul>{nav_links_html}</ul></nav></div><div class="controls"><input type="search" id="search-box" placeholder="Search..."><button id="favorites-toggle">Show Favorites</button><button id="theme-toggle" title="Toggle Theme"></button></div></header>
    <div class="template-info"><h2>Base Prompt Template</h2><pre id="template-text"></pre></div>
    <div id="model-selector" class="model-selector"></div><div id="gallery" class="image-grid"></div>
    <div id="lightbox"><span class="close">&times;</span><div class="lightbox-content"><img id="lightbox-img" alt="Enlarged image"><div class="lightbox-info"><div class="artist-container"><span>Artist: </span><span id="lightbox-artist"></span></div><div id="favorite-container"><button id="favorite-button"><span id="favorite-icon-gfx"></span><span id="favorite-text"></span></button></div><div id="lightbox-related-images"></div><div class="prompt-container"></div><div class="model-container"><span>Model: </span><span id="lightbox-model"></span></div><div class="seed-container"><span>Seed: </span><span id="lightbox-seed"></span></div></div></div></div>
    <div id="fullscreen-overlay"><img id="fullscreen-img" alt="Fullscreen image"></div><div id="loading">Loading...</div>
    <script>{js_data}</script><script src="js/character_gallery.js"></script></body></html>"""
    with open(html_filename, "w", encoding="utf-8") as f: f.write(html_content)
    print(f"Generated section page: {html_filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate a static gallery website")
    parser.add_argument("--api-key", help="NovelAI API key")
    parser.add_argument("--no-generate", action="store_true", help="Skip image generation, only build from existing data")
    parser.add_argument("--generate-nsfw", action="store_true", help="Only generate images for NSFW sections (includes noncon)")
    parser.add_argument("--generate-noncon", action="store_true", help="Only generate images for the noncon section")
    args = parser.parse_args()

    setup_directories()
    
    headers = None
    if not args.no_generate:
        try:
            headers = login(args.api_key)
        except Exception as e:
            print(f"Login failed: {e}. Switching to --no-generate mode.")
            args.no_generate = True

    artists = read_artists()
    template_text = read_template()
    if not artists and not args.no_generate:
        print("Warning: artists.txt is empty. Generation will be skipped.")
        args.no_generate = True
    
    sections_to_generate = []
    if not args.no_generate:
        if args.generate_noncon:
            sections_to_generate.append("noncon")
        elif args.generate_nsfw:
            sections_to_generate.extend([sid for sid, scfg in ALL_SECTIONS_CONFIG.items() if scfg['is_nsfw']])
        else:
            sections_to_generate.extend(ALL_SECTIONS_CONFIG.keys())
        
        print(f"\n--- Generating images for sections: {', '.join(sections_to_generate)} ---")
        for section_id in sections_to_generate:
            process_section_generation(ALL_SECTIONS_CONFIG[section_id], headers, artists, template_text)

    print("\n--- Building Website from All Available Data ---")
    for section_id, section_config in ALL_SECTIONS_CONFIG.items():
        data_file = f"{OUTPUT_IMAGES_DIR}/{section_id}_data.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                try:
                    images_data = json.load(f)
                    if images_data:
                        base_template_text = "Structured prompts via LLM" if section_config['type'] == 'v4_structured' else template_text
                        generate_section_html(section_config, images_data, base_template_text)
                    else: print(f"Data file for '{section_id}' is empty. Skipping HTML.")
                except json.JSONDecodeError:
                    print(f"Error decoding {data_file}. Skipping HTML for '{section_id}'.")
        else:
            print(f"No data file found for '{section_id}'. Skipping HTML generation.")
        
        if section_config['is_nsfw']:
            generate_nsfw_landing_page(OUTPUT_SITE_DIR, section_id, section_config['name'])
    
    linked_sections = [s for s in ALL_SECTIONS_CONFIG.values() if not s.get("unlinked")]
    if linked_sections:
        first_sfw = next((s for s in linked_sections if not s['is_nsfw']), None)
        first_nsfw = next((s for s in linked_sections if s['is_nsfw']), None)
        target = f"{first_sfw['id']}.html" if first_sfw else (f"{first_nsfw['id']}_landing.html" if first_nsfw else "women.html")
        with open(f"{OUTPUT_SITE_DIR}/index.html", "w") as f: f.write(f'<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url={target}"></head></html>')
        print(f"Generated index.html redirecting to {target}")

    print(f"\nWebsite generation complete. Files are in: {os.path.abspath(OUTPUT_SITE_DIR)}")

if __name__ == "__main__":
    main()
