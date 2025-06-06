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
OUTPUT_IMAGES_DIR = "./output_images"
ARTISTS_FILE = "artists.txt"
TEMPLATE_FILE = "template.prompt"
API_URL = "https://image.novelai.net"

# Configuration for different gallery sections
GALLERY_SECTIONS = [
    {
        "id": "women",
        "name": "Women",
        "file": "1girl.txt",
        "max_images": 45000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/full", # Main display images
        "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/thumb", # Main display images
        "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/raw" # Raw images (PNGs from API, or copied old fulls)
    },
    {
        "id": "men",
        "name": "Men",
        "file": "1boy.txt",
        "max_images": 5000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/full", # Main display images
        "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/thumb", # Main display images
        "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/raw" # Raw images (PNGs from API, or copied old fulls)
    }
]#!/usr/bin/env python3
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

# Configuration for different gallery sections
GALLERY_SECTIONS = [
    {
        "id": "women",
        "name": "Women",
        "file": "1girl.txt",
        "max_images": 45000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/full", # Original path for SFW
        "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/thumb", # Original path for SFW
        "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/raw", # Original path for SFW
        "is_nsfw": False
    },
    {
        "id": "men",
        "name": "Men",
        "file": "1boy.txt",
        "max_images": 5000,
        "images_dir_full": f"{OUTPUT_IMAGES_DIR}/full", # Original path for SFW
        "images_dir_thumb": f"{OUTPUT_IMAGES_DIR}/thumb", # Original path for SFW
        "images_dir_raw": f"{OUTPUT_IMAGES_DIR}/raw", # Original path for SFW
        "is_nsfw": False
    },
    {
        "id": "nsfw",
        "name": "NSFW Zone", # Clearly named
        "file": NSFW_PROMPTS_FILE, # Use the new constant
        "max_images": 20000, # Example, adjust as needed
        "images_dir_full": f"{NSFW_IMAGES_DIR_BASE}/full", # Dedicated path
        "images_dir_thumb": f"{NSFW_IMAGES_DIR_BASE}/thumb", # Dedicated path
        "images_dir_raw": f"{NSFW_IMAGES_DIR_BASE}/raw", # Dedicated path
        "is_nsfw": True # Flag for special handling
    }
]

# CONFIG VARIABLES
RANDOM_SEED = 42  # Fixed seed for deterministic image generation

# Setup fixed random seed for deterministic generation
random.seed(RANDOM_SEED)

# Define models to use
MODELS = [
    {"id": "nai-diffusion-4-full", "name": "NAI Diffusion 4 Full"},
    {"id": "nai-diffusion-4-curated-preview", "name": "NAI Diffusion 4 Curated"},
    {"id": "nai-diffusion-4-5-curated", "name": "NAI Diffusion 4.5 Curated"},
    {"id": "nai-diffusion-4-5-full", "name": "NAI Diffusion 4.5 Full"},
]



def setup_directories():
    """Setup the output directory structure"""
    os.makedirs(OUTPUT_SITE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True) # For _data.json files and SFW image folders
    # NSFW_IMAGES_DIR_BASE will be created implicitly by makedirs for section["images_dir_full"] etc. if needed

    for section in GALLERY_SECTIONS:
        os.makedirs(section["images_dir_full"], exist_ok=True)
        os.makedirs(section["images_dir_thumb"], exist_ok=True)
        os.makedirs(section["images_dir_raw"], exist_ok=True)

    for folder in ["css", "js"]:
        src_folder = f"./{folder}"
        dest_folder = f"{OUTPUT_SITE_DIR}/{folder}"
        if os.path.exists(src_folder):
            if os.path.exists(dest_folder):
                shutil.rmtree(dest_folder)
            shutil.copytree(src_folder, dest_folder)

def read_artists():
    if not os.path.exists(ARTISTS_FILE):
        print(f"Warning: {ARTISTS_FILE} not found. No artists will be used.")
        return []
    with open(ARTISTS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def read_section_descriptions(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    print(f"Warning: Description file {file_path} not found.")
    return []

def read_template():
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError(f"Error: {TEMPLATE_FILE} not found. This file is required.")
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def login(api_key=None):
    credentials_file = ".nai_credentials.json"
    load_dotenv()

    if api_key:
        print("Using API key from command line arguments")
        return {"Authorization": f"Bearer {api_key}"}

    env_token = os.getenv("NAI_PERSISTENT_TOKEN") or os.getenv("NAI_PERSISTENT_API_KEY")
    if env_token:
        print("Using persistent token from .env file")
        return {"Authorization": f"Bearer {env_token}"}

    if os.path.exists(credentials_file):
        try:
            with open(credentials_file, "r") as f:
                cached = json.load(f)
                print("Using cached credentials")
                return {"Authorization": f"Bearer {cached['accessToken']}"}
        except Exception as e:
            print(f"Error loading cached credentials: {e}. Will prompt for login.")
            if os.path.exists(credentials_file): os.remove(credentials_file)

    print("No API key, persistent token, or valid cached credentials found. Please provide login credentials.")
    email = input("Enter NovelAI email (or API Key if you prefer to paste it here): ")

    auth_url = f"{API_URL}/user"
    auth_headers = {}
    auth_payload = {}

    if "@" not in email and len(email) > 60:
        print("Attempting to use input as an API Key for persistent token...")
        auth_url += "/create-persistent-token"
        auth_headers = {"Authorization": f"Bearer {email}"}
    else:
        password = input("Enter NovelAI password: ")
        auth_url += "/login"
        auth_payload = {"email": email, "password": password}

    try:
        if auth_payload:
             response = requests.post(auth_url, json=auth_payload)
        else:
             response = requests.post(auth_url, headers=auth_headers)
        response.raise_for_status()
        data = response.json()

        with open(credentials_file, "w") as f:
            json.dump({"accessToken": data['accessToken']}, f)

        if "@" not in email and len(email) > 60:
            print("\nSuccessfully authenticated using the provided API Key.")
            print("A persistent session token has been cached for future use.")
            print("You can also add this token to your .env file as NAI_PERSISTENT_TOKEN if desired.")
            print(f"NAI_PERSISTENT_TOKEN={data['accessToken']}")
        else:
            print("\nLogin successful. Session token cached.")
            print("TIP: For long-term automated use, consider creating a persistent token via NovelAI's settings")
            print("and storing it in a .env file as NAI_PERSISTENT_TOKEN=your_token")

        return {"Authorization": f"Bearer {data['accessToken']}"}
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_text = e.response.text
        if status_code == 401:
            print(f"Authentication failed: Invalid credentials or API key. ({status_code})")
        else:
            print(f"Authentication error: {status_code} - {error_text}")
        raise Exception("Authentication failed.")
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        raise Exception("Authentication failed.")

def generate_image(prompt, headers, filename_base, model_id,
                   images_dir_full, images_dir_thumb, images_dir_raw, is_nsfw_section=False): # Added is_nsfw_section
    seed = random.randint(1, 2147483647)
    base_prompt = f"{prompt}, no text, best quality, masterpiece, very aesthetic, absurdres"
    
    if is_nsfw_section:
        # For NSFW, remove "nsfw" from negative, and add other common undesired tags for adult content
        negative_prompt = "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page, shota, child"
    else:
        # Standard SFW negative prompt
        negative_prompt = "nsfw, blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page"

    payload = {
        "input": base_prompt, "model": model_id, "action": "generate",
        "parameters": {
            "params_version": 3, "width": 832, "height": 1216, "scale": 6,
            "sampler": "k_dpmpp_2m_sde", "steps": 28, "n_samples": 1, "ucPreset": 0,
            "qualityToggle": True, "autoSmea": False, "dynamic_thresholding": False,
            "controlnet_strength": 1, "legacy": False, "add_original_image": True,
            "cfg_rescale": 0, "noise_schedule": "karras", "legacy_v3_extend": False,
            "skip_cfg_above_sigma": None, "use_coords": False, "legacy_uc": False,
            "normalize_reference_strength_multiple": True,
            "v4_prompt": {"caption": {"base_caption": base_prompt, "char_captions": []}, "use_coords": False, "use_order": True},
            "v4_negative_prompt": {"caption": {"base_caption": negative_prompt, "char_captions": []}, "legacy_uc": False},
            "seed": seed, "characterPrompts": [], "reference_image_multiple": [],
            "reference_strength_multiple": [], "negative_prompt": negative_prompt
        }
    }

    print(f"Generating image for: {filename_base}_ (seed: {seed}) with model {model_id}")

    try:
        response = requests.post(f"{API_URL}/ai/generate-image", headers=headers, json=payload)
        response.raise_for_status()

        zip_bytes = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_bytes, 'r') as zip_ref:
            if not zip_ref.namelist():
                raise Exception("No files found in the zip archive from API.")
            image_file_name_in_zip = next((name for name in zip_ref.namelist() if name.startswith('image_') and name.endswith('.png')), None)
            if not image_file_name_in_zip: image_file_name_in_zip = zip_ref.namelist()[0]

            image_bytes = zip_ref.read(image_file_name_in_zip)
            img = Image.open(io.BytesIO(image_bytes))

        filename_stem = f"{filename_base}_{seed}"

        # Save raw PNG image
        raw_png_filename = f"{filename_stem}.png"
        actual_save_raw_path = os.path.join(images_dir_raw, raw_png_filename)
        os.makedirs(images_dir_raw, exist_ok=True) # Ensure raw directory exists
        with open(actual_save_raw_path, "wb") as f:
            f.write(image_bytes)

        # Save full-size display JPEG
        jpeg_filename = f"{filename_stem}.jpg"
        actual_save_full_path = os.path.join(images_dir_full, jpeg_filename)
        os.makedirs(images_dir_full, exist_ok=True) # Ensure full directory exists
        full_size = (int(img.width * 0.7), int(img.height * 0.7))
        img_full = img.copy()
        img_full.thumbnail(full_size, Image.Resampling.LANCZOS)
        img_full.convert("RGB").save(actual_save_full_path, "JPEG", quality=80)

        # Save thumbnail JPEG
        actual_save_thumb_path = os.path.join(images_dir_thumb, jpeg_filename)
        os.makedirs(images_dir_thumb, exist_ok=True) # Ensure thumb directory exists
        thumb_size = (int(img.width * 0.35), int(img.height * 0.35))
        img_thumb = img.copy()
        img_thumb.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        img_thumb.convert("RGB").save(actual_save_thumb_path, "JPEG", quality=80)

        return {
            "filename_base": filename_base,
            "filename_stem": filename_stem,
            "full_path_for_html": os.path.relpath(actual_save_full_path, OUTPUT_SITE_DIR).replace(os.sep, '/'),
            "thumb_path_for_html": os.path.relpath(actual_save_thumb_path, OUTPUT_SITE_DIR).replace(os.sep, '/'),
            "raw_path_for_html": os.path.relpath(actual_save_raw_path, OUTPUT_SITE_DIR).replace(os.sep, '/'),
            "seed": seed,
            "model_id": model_id,
            "modelName": next((m["name"] for m in MODELS if m["id"] == model_id), model_id)
        }
    except requests.exceptions.RequestException as e:
        print(f"API request error for {filename_base}: {e}")
        if hasattr(e, 'response') and e.response is not None: print(f"Response content: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error processing image for {filename_base}: {e}")
        return None

def generate_character_prompt(character_desc, artist_name, template):
    filled_prompt = template.replace("{{prompt}}", character_desc)
    filled_prompt = filled_prompt.replace("{{artist}}", artist_name )
    return filled_prompt

def generate_section_images(section_config, character_descriptions, artists, template, headers):
    section_id = section_config["id"]
    images_dir_full = section_config["images_dir_full"]
    images_dir_thumb = section_config["images_dir_thumb"]
    images_dir_raw = section_config["images_dir_raw"]
    is_nsfw = section_config.get("is_nsfw", False) # Get NSFW flag

    max_images = section_config["max_images"]
    section_data_file = f"{OUTPUT_IMAGES_DIR}/{section_id}_data.json"

    final_results_for_section = []
    processed_filename_bases = set()
    
    items_in_json_file = 0
    loaded_data_from_json = []

    NEW_GENERATION_MODEL_ID = "nai-diffusion-4-5-full" 

    if os.path.exists(section_data_file):
        print(f"Loading existing data from {section_data_file} for section '{section_id}'")
        with open(section_data_file, "r", encoding="utf-8") as f:
            loaded_data_from_json = json.load(f)
        items_in_json_file = len(loaded_data_from_json)

        for item in loaded_data_from_json:
            if 'filename_base' not in item or not item['filename_base']:
                id_val = item.get('id', '')
                full_val = item.get('full', '') 
                potential_stem_from_id = id_val if '.' not in id_val and '_' in id_val else None
                base_name_with_seed = potential_stem_from_id or (os.path.splitext(os.path.basename(full_val))[0] if full_val else "")
                if base_name_with_seed:
                    parts = base_name_with_seed.split('_')
                    if len(parts) > 1 and parts[-1].isdigit(): 
                        item['filename_base'] = '_'.join(parts[:-1])
                    else: 
                        item['filename_base'] = base_name_with_seed 
            
            filename_stem = item.get('id')
            if not filename_stem:
                print(f"  Skipping stale/invalid item due to missing 'id': {item}")
                continue

            if 'model' not in item: item['model'] = "unknown_model"

            full_path_str = os.path.join(images_dir_full, f"{filename_stem}.jpg")
            thumb_path_str = os.path.join(images_dir_thumb, f"{filename_stem}.jpg")
            raw_path_str = os.path.join(images_dir_raw, f"{filename_stem}.png")
            if not os.path.exists(raw_path_str): 
                raw_path_str_jpg = os.path.join(images_dir_raw, f"{filename_stem}.jpg")
                if os.path.exists(raw_path_str_jpg):
                    raw_path_str = raw_path_str_jpg # Fallback to JPG if PNG not found for raw
                # If neither .png nor .jpg exists for raw, the condition below will fail it.


            if os.path.exists(full_path_str) and \
               os.path.exists(thumb_path_str) and \
               os.path.exists(raw_path_str) and \
               item.get('filename_base'): 
                if len(final_results_for_section) < max_images:
                    final_results_for_section.append(item)
                    processed_filename_bases.add(item['filename_base'])
                else:
                    break
            else:
                print(f"  Skipping stale/invalid item: {filename_stem}.")
                if not item.get('filename_base'): print("    Reason: Missing filename_base.")
                if not os.path.exists(full_path_str): print(f"    Missing: {full_path_str}")
                if not os.path.exists(thumb_path_str): print(f"    Missing: {thumb_path_str}")
                if not os.path.exists(raw_path_str): print(f"    Missing raw file for {filename_stem} (checked .png and .jpg at {os.path.join(images_dir_raw, filename_stem)})")
        
        if items_in_json_file > 0 and len(final_results_for_section) < items_in_json_file:
             print(f"Note: From {items_in_json_file} items in JSON, {len(final_results_for_section)} were valid and loaded. Others were stale/invalid or exceeded max_images.")
        print(f"Loaded {len(final_results_for_section)} valid existing images from JSON for section '{section_id}'.")

        if len(final_results_for_section) >= max_images:
             print(f"Max images ({max_images}) for section '{section_id}' reached from JSON data. No new generation needed.")

    data_changed_during_load_filter = items_in_json_file != len(final_results_for_section)

    model_artist_counts = {
        (model["id"], artist): 0 for model in MODELS for artist in artists
    }

    for item in final_results_for_section:
        model_id = item.get("model") 
        artist = item.get("artist")
        if any(m["id"] == model_id for m in MODELS) and artist in artists:
            if (model_id, artist) in model_artist_counts:
                 model_artist_counts[(model_id, artist)] += 1
        elif model_id and artist : 
            print(f"  Note: Existing item for model '{model_id}' and artist '{artist}' found, but this combination is not in current active generation sets. It will be kept.")

    if not artists:
        print(f"Skipping further image processing for section '{section_id}': No artists from {ARTISTS_FILE}.")
        if data_changed_during_load_filter:
            with open(section_data_file, "w", encoding="utf-8") as f:
                json.dump(final_results_for_section, f, indent=2)
            print(f"Saved updated data (due to filtering) to {section_data_file} for section '{section_id}'.")
        return final_results_for_section
        
    if not character_descriptions:
        print(f"Skipping further image processing for section '{section_id}': No descriptions from {section_config['file']}.")
        if data_changed_during_load_filter:
            with open(section_data_file, "w", encoding="utf-8") as f:
                json.dump(final_results_for_section, f, indent=2)
            print(f"Saved updated data (due to filtering) to {section_data_file} for section '{section_id}'.")
        return final_results_for_section

    num_slots_to_fill = max_images - len(final_results_for_section)
    if num_slots_to_fill <= 0:
        print(f"Section '{section_id}' is already full ({len(final_results_for_section)}/{max_images} images). No new images will be generated.")
        if data_changed_during_load_filter:
            with open(section_data_file, "w", encoding="utf-8") as f:
                json.dump(final_results_for_section, f, indent=2)
            print(f"Saved updated data (due to filtering) to {section_data_file} for section '{section_id}'.")
        return final_results_for_section

    available_descriptions = character_descriptions.copy()
    random.shuffle(available_descriptions)
    newly_added_images_count = 0

    print(f"Attempting to generate up to {num_slots_to_fill} new {section_id} images, using model '{NEW_GENERATION_MODEL_ID}' and balancing artists.")

    for char_desc in available_descriptions:
        if newly_added_images_count >= num_slots_to_fill:
            print(f"Reached target of {num_slots_to_fill} new images for section '{section_id}'. Stopping further generation.")
            break

        counts_for_new_gen_model_artist = {}
        for artist_name in artists: 
            counts_for_new_gen_model_artist[artist_name] = model_artist_counts.get((NEW_GENERATION_MODEL_ID, artist_name), 0)
        
        min_artist_count = min(counts_for_new_gen_model_artist.values())
        eligible_artists = [
            artist_name for artist_name, count in counts_for_new_gen_model_artist.items()
            if count == min_artist_count
        ]
        selected_artist = random.choice(eligible_artists)
        
        actual_model_for_generation = NEW_GENERATION_MODEL_ID

        prompt_text = generate_character_prompt(char_desc, selected_artist, template)
        prompt_text = prompt_text.strip()  # Clean up whitespace
        if is_nsfw:
            prompt_text = f"{prompt_text}, nsfw, uncensored"  # Add nsfw tag for NSFW sections
        prompt_plus_model_str = prompt_text + actual_model_for_generation 
        prompt_hash = hashlib.md5(prompt_plus_model_str.encode("utf-8")).hexdigest()[:10]

        model_identifier_for_filename = actual_model_for_generation.replace("nai-diffusion-", "").replace("-", "_")
        filename_base = f"{section_id}_{prompt_hash}_{model_identifier_for_filename}"

        if filename_base in processed_filename_bases:
            continue

        potential_existing_raw_glob = os.path.join(images_dir_raw, f"{filename_base}_*.png")
        potential_existing_thumb_glob = os.path.join(images_dir_thumb, f"{filename_base}_*.jpg")

        if glob.glob(potential_existing_raw_glob) or glob.glob(potential_existing_thumb_glob):
            print(f"  Skipping generation for filename_base '{filename_base}': Files already exist on disk.")
            processed_filename_bases.add(filename_base)
            continue
        
        if headers is None: 
            print("  Skipping API call because headers are not available (e.g. --no-generate or login failed).")
            continue

        print(f"  Generating image for: {char_desc[:60]}... (Artist: {selected_artist}, Model: {actual_model_for_generation}, NSFW: {is_nsfw})")
        image_details = generate_image(
            prompt_text,
            headers,
            filename_base, 
            actual_model_for_generation, 
            images_dir_full=images_dir_full,
            images_dir_thumb=images_dir_thumb,
            images_dir_raw=images_dir_raw,
            is_nsfw_section=is_nsfw # Pass the flag here
        )

        if not image_details:
            time.sleep(1) 
            continue

        image_data_to_store = {
            "id": image_details["filename_stem"], 
            "filename_base": image_details["filename_base"], 
            "artist": selected_artist,
            "prompt": prompt_text, 
            "model": image_details["model_id"], 
            "seed": image_details["seed"],
            "modelName": image_details["modelName"] # Ensure modelName is included
        }
        final_results_for_section.append(image_data_to_store)
        processed_filename_bases.add(filename_base) 

        model_artist_counts[(actual_model_for_generation, selected_artist)] = model_artist_counts.get((actual_model_for_generation, selected_artist), 0) + 1
        newly_added_images_count += 1

        with open(section_data_file, "w", encoding="utf-8") as f:
            json.dump(final_results_for_section, f, indent=2)
        
        time.sleep(0.1) 

    with open(section_data_file, "w", encoding="utf-8") as f:
        json.dump(final_results_for_section, f, indent=2)
    print(f"Section '{section_id}': Added {newly_added_images_count} new images. Total: {len(final_results_for_section)}.")
    return final_results_for_section


def generate_redirect_html(output_path, target_url):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0;url={target_url}">
    <link rel="canonical" href="{target_url}" />
    <script type="text/javascript">window.location.href = "{target_url}";</script>
</head>
<body><p>If you are not redirected, <a href="{target_url}">click here</a>.</p></body></html>"""
    with open(output_path, "w", encoding="utf-8") as f: f.write(html_content)
    print(f"Generated redirect page: {output_path} -> {target_url}")

def generate_section_html(section_config, images_data, template_text, all_gallery_sections_for_nav):
    section_id = section_config["id"]
    section_name = section_config["name"]
    is_nsfw_page = section_config.get("is_nsfw", False)
    title = f"NovelAI Gallery | {section_name}"
    html_filename = f"{OUTPUT_SITE_DIR}/{section_id}.html"

    safe_template_for_js = json.dumps(template_text)
    
    images_data_for_js = []
    for img in images_data:
        # Ensure modelName is present, falling back to model ID if necessary
        model_name = img.get("modelName", img.get("model", "unknown_model"))
        if not model_name and "model" in img: # if modelName was empty but model exists
             model_name = next((m["name"] for m in MODELS if m["id"] == img["model"]), img["model"])

        images_data_for_js.append({
            "id": img["id"],
            "artist": img.get("artist", "N/A"),
            "model": img.get("model", "unknown_model"),
            "modelName": model_name, # Use resolved model_name
            "prompt": img.get("prompt", ""),
            "seed": img.get("seed", ""),
        })
    serialized_images_data = json.dumps(images_data_for_js)

    nav_links_html = ""
    # Use all_gallery_sections_for_nav to ensure all configured sections appear in nav,
    # respecting the original GALLERY_SECTIONS order and definitions.
    for s_nav in all_gallery_sections_for_nav:
        is_active = 'class="active"' if s_nav["id"] == section_id else ''
        link_href = f'{s_nav["id"]}.html'
        if s_nav.get("is_nsfw", False): # If the section itself is NSFW
            link_href = f'{s_nav["id"]}_landing.html' # Link to its landing page
        nav_links_html += f'\n                    <li {is_active}><a href="{link_href}">{s_nav["name"]}</a></li>'

    # The age disclaimer is always included but hidden by default. JS will control its visibility.
    age_disclaimer_display_style = "display: none;"

    js_data_assignment = f"""const galleryData = {{
            "sectionImages": {serialized_images_data},
            "template": {safe_template_for_js},
            "section": "{section_id}",
            "isNsfwSection": {json.dumps(is_nsfw_page)}
        }};"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div id="age-disclaimer-overlay" style="{age_disclaimer_display_style}">
        <div id="age-disclaimer-modal">
            <h2>Age Verification</h2>
            <p>You must be 18 years or older to view this content. {'The images in this section may be explicit and are intended for mature audiences only.' if is_nsfw_page else 'The images are intended to be SFW, but occasional errors sometimes result in nudity.'}</p>
            <p>Please confirm your age to continue.</p>
            <button id="age-confirm-button">I am 18 or older</button>
            <button id="age-exit-button">Exit</button>
        </div>
    </div>

    <header>
        <div class="logo-container">
            <svg class="logo" viewBox="0 0 100 100" width="40" height="40"><circle cx="50" cy="50" r="40" fill="#6c5ce7" /><path d="M30,30 L70,70 M30,70 L70,30" stroke="white" stroke-width="8" stroke-linecap="round" /></svg>
            <h1>{title}</h1>
        </div>
        <div class="site-navigation"><nav><ul>{nav_links_html}</ul></nav></div>
        <div class="controls">
            <input type="search" id="search-box" placeholder="Search tags or artists...">
            <button id="favorites-toggle" class="action-button">Show Favorites</button>
            <button id="theme-toggle" class="theme-button" title="Toggle Dark/Light Mode"></button>
        </div>
    </header>
    <div class="template-info"><h2>Base Prompt Template</h2><pre id="template-text"></pre></div>
    <div id="model-selector" class="model-selector"></div>
    <div id="gallery" class="image-grid"></div>
    <div id="lightbox" class="lightbox">
        <span class="close">&times;</span>
        <div class="lightbox-content">
            <img id="lightbox-img" src="" alt="Enlarged image">
            <div class="lightbox-info">
                <div class="artist-container"><span>Artist: </span><span id="lightbox-artist" title="Click to copy artist" style="cursor:pointer;"></span></div>
                <div id="favorite-container" class="favorite-container"><button id="favorite-button" class="favorite-button"><span id="favorite-icon" class="favorite-icon-gfx"></span><span id="favorite-text">Add to Favorites</span></button></div>
                <div id="lightbox-related-images" class="related-images"></div>
                <div id="lightbox-tags-container" class="tags-container-modal"></div>
                <div class="prompt-container"><h4>Prompt:</h4><pre id="lightbox-prompt"></pre><button id="copy-prompt" class="copy-button">Copy Prompt</button></div>
                <div class="model-container"><span>Model: </span><span id="lightbox-model"></span></div>
                <div class="seed-container"><span>Seed: </span><span id="lightbox-seed"></span></div>                
            </div>
        </div>
    </div>
    <div id="fullscreen-overlay" class="fullscreen-overlay"><img id="fullscreen-img" src="" alt="Fullscreen image"></div>
    <div id="loading" class="loading">Loading more images...</div>
    <script>{js_data_assignment}</script>
    <script src="js/character_gallery.js"></script>
</body>
</html>"""

    with open(html_filename, "w", encoding="utf-8") as f: f.write(html_content)
    print(f"Generated section page: {html_filename}")



# New function to generate NSFW landing page
def generate_nsfw_landing_page(output_site_dir, nsfw_section_id, nsfw_section_name):
    nsfw_gallery_url = f"{nsfw_section_id}.html" # Actual gallery page
    landing_page_filename = f"{output_site_dir}/{nsfw_section_id}_landing.html"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warning: {nsfw_section_name} Content</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        body {{ display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 100vh; text-align: center; background-color: #1a1a2e; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 1rem;}}
        .disclaimer-box {{ background-color: #24243e; padding: 2rem 3rem; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); max-width: 650px; border: 1px solid #4a4a70; }}
        .disclaimer-box h1 {{ color: #ff4757; margin-bottom: 1.5rem; font-size: 2rem; text-transform: uppercase; letter-spacing: 1px;}}
        .disclaimer-box p {{ margin-bottom: 1.5rem; line-height: 1.7; font-size: 1.05rem; }}
        .disclaimer-box strong {{ color: #ffa502; }}
        .disclaimer-box .actions a {{ display: inline-block; background-color: #2ecc71; color: white; padding: 0.9rem 1.8rem; text-decoration: none; border-radius: 5px; margin: 0.5rem; transition: background-color 0.2s ease-in-out, transform 0.2s ease; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }}
        .disclaimer-box .actions a:hover {{ background-color: #27ae60; transform: translateY(-2px); }}
        .disclaimer-box .actions a.exit {{ background-color: #7f8c8d; }}
        .disclaimer-box .actions a.exit:hover {{ background-color: #6c7a7b; }}
        .warning-icon {{ font-size: 2.5rem; margin-bottom: 1rem; color: #ff4757; }}
    </style>
</head>
<body>
    <div class="disclaimer-box">
        <div class="warning-icon"><span role="img" aria-label="warning">🔞</span></div>
        <h1>Adult Content Warning</h1>
        <p>The section "<strong>{nsfw_section_name}</strong>" you are about to enter contains material that is sexually explicit and intended for adult audiences only. This content may be considered Not Safe For Work (NSFW).</p>
        <p>You must be <strong>18 years of age or older</strong> (or the legal age of majority in your jurisdiction) to access this content. If you are not of legal age, or if such material offends you or is illegal to view in your location, please do not proceed.</p>
        <p>By clicking "<strong>Enter Site (I Confirm I Am 18+)</strong>", you affirm that you meet these age requirements, that you understand the nature of the content, and that you are choosing to view it voluntarily.</p>
        <div class="actions">
            <a href="{nsfw_gallery_url}">Enter Site (I Confirm I Am 18+)</a>
            <a href="index.html" class="exit">Exit to Main Page</a>
        </div>
    </div>
</body>
</html>"""
    with open(landing_page_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated NSFW landing page: {landing_page_filename} for section '{nsfw_section_name}'")


def main():
    parser = argparse.ArgumentParser(description="Generate a static gallery website with NovelAI images")
    parser.add_argument("--api-key", help="NovelAI API key (overrides .env or cached tokens)")
    parser.add_argument("--no-generate", action="store_true", help="Skip image generation, only build website from existing data.")
    parser.add_argument("--create-env-template", action="store_true", help="Create a template .env file and exit.")
    parser.add_argument("--generate-nsfw", action="store_true", help="Only generate images and content for NSFW sections.")
    args = parser.parse_args()

    if args.create_env_template:
        env_file_path = ".env"
        if not os.path.exists(env_file_path):
            with open(env_file_path, "w") as f:
                f.write("# NovelAI Persistent Token (recommended for automated use)\n")
                f.write("# Obtain from NovelAI website/API settings if you have an account.\n")
                f.write("# NAI_PERSISTENT_TOKEN=your_long_alphanumeric_token_here\n\n")
                f.write("# Alternatively, NAI_PERSISTENT_API_KEY is also checked (older variable name).\n")
                f.write("# NAI_PERSISTENT_API_KEY=your_long_alphanumeric_token_here\n")
            print(f"Created {env_file_path}. Add your NovelAI persistent token.")
        else:
            print(f"{env_file_path} already exists. Not overwriting.")
        return

    setup_directories()

    try:
        template_text = read_template()
        artists = read_artists()

        sections_to_process = GALLERY_SECTIONS
        if args.generate_nsfw:
            sections_to_process = [s for s in GALLERY_SECTIONS if s.get("is_nsfw", False)]
            if not sections_to_process:
                print("NSFW generation requested (--generate-nsfw), but no NSFW sections are configured in GALLERY_SECTIONS. Exiting.")
                return
            print("Processing NSFW sections only due to --generate-nsfw flag.")

        section_descriptions = {}
        for section_config in sections_to_process: # Only load descriptions for sections we process
            desc = read_section_descriptions(section_config["file"])
            section_descriptions[section_config["id"]] = desc
            print(f"Found {len(desc)} descriptions in {section_config['file']} for section '{section_config['id']}'.")
            if not desc:
                 print(f"Warning: No descriptions loaded for '{section_config['id']}' from {section_config['file']}. Section might be empty if no existing data.")


        headers = None
        if not args.no_generate:
            if not artists: print("Warning: No artists found. Image generation requiring artists will be limited.")
            try:
                headers = login(args.api_key)
            except Exception as e:
                print(f"Login failed: {e}. Cannot generate images. Try with --no-generate or fix login.")
                args.no_generate = True # Force no-generate mode if login fails

        print("\n--- Processing Gallery Sections ---")
        all_sections_data = {}

        for section_config in sections_to_process:
            section_id = section_config["id"]
            print(f"\nProcessing section: {section_config['name']}")

            current_section_data = generate_section_images(
                section_config,
                section_descriptions.get(section_id, []),
                artists if headers and not args.no_generate else [], # Pass empty list if no headers/no_generate
                template_text,
                headers if not args.no_generate else None
            )
            all_sections_data[section_id] = current_section_data

        print("\n--- Generating HTML Pages ---")
        loaded_any_data_for_html = False
        for section_config in sections_to_process: # Only generate HTML for processed sections
            section_id = section_config["id"]
            images_data_for_html = all_sections_data.get(section_id, [])
            
            # If --no-generate, we might not have data if JSON was missing. Load it if not already loaded.
            if args.no_generate and not images_data_for_html:
                section_data_file = f"{OUTPUT_IMAGES_DIR}/{section_id}_data.json"
                if os.path.exists(section_data_file):
                    try:
                        with open(section_data_file, "r", encoding="utf-8") as f:
                            images_data_for_html = json.load(f)
                        all_sections_data[section_id] = images_data_for_html # Store it
                        print(f"Loaded data for section '{section_id}' from JSON for HTML generation (as --no-generate was used).")
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode JSON from {section_data_file} for HTML generation.")
                else:
                    print(f"Warning: No data file ({section_data_file}) found for section '{section_id}' and --no-generate was used. HTML page may be empty or skip generation.")

            if images_data_for_html or not args.no_generate : # Generate HTML if data exists, or if we are in generation mode (might create empty page)
                loaded_any_data_for_html = True if images_data_for_html else loaded_any_data_for_html
                generate_section_html(section_config, images_data_for_html, template_text, GALLERY_SECTIONS) # Pass ALL sections for nav
            else:
                print(f"Skipping HTML generation for section '{section_id}' as no data was loaded/generated.")


        # Generate NSFW landing pages for *all* configured NSFW sections, regardless of --generate-nsfw filter for processing.
        # This ensures landing pages exist if the sections are defined.
        for section_config in GALLERY_SECTIONS:
            if section_config.get("is_nsfw", False):
                generate_nsfw_landing_page(OUTPUT_SITE_DIR, section_config["id"], section_config["name"])


        if args.no_generate and not loaded_any_data_for_html and not sections_to_process:
             print("Warning: --no-generate was used, and no sections were processed (e.g. --generate-nsfw with no NSFW sections). Site may be incomplete.")
        elif args.no_generate and not loaded_any_data_for_html and sections_to_process:
             print(f"Warning: --no-generate was used, and no existing valid data files (*_data.json) were found or processed for the active sections. Site may be empty for: {[s['id'] for s in sections_to_process]}.")


        # Determine redirect for index.html based on original GALLERY_SECTIONS
        if GALLERY_SECTIONS:
            first_sfw_section = next((s for s in GALLERY_SECTIONS if not s.get("is_nsfw", False)), None)
            first_nsfw_section = next((s for s in GALLERY_SECTIONS if s.get("is_nsfw", False)), None)
            
            redirect_target_url = None
            if first_sfw_section:
                redirect_target_url = f"{first_sfw_section['id']}.html"
            elif first_nsfw_section: # If no SFW sections, redirect to first NSFW landing page
                redirect_target_url = f"{first_nsfw_section['id']}_landing.html"
            
            if redirect_target_url:
                generate_redirect_html(f"{OUTPUT_SITE_DIR}/index.html", redirect_target_url)
            elif sections_to_process: # Fallback if only specific (e.g. nsfw) sections were processed and no general rule matched
                first_processed_section = sections_to_process[0]
                target_url = f"{first_processed_section['id']}.html"
                if first_processed_section.get("is_nsfw"):
                    target_url = f"{first_processed_section['id']}_landing.html"
                generate_redirect_html(f"{OUTPUT_SITE_DIR}/index.html", target_url)
            else: # No sections at all
                placeholder_index_content = "<!DOCTYPE html><html><head><title>Gallery</title></head><body><p>No gallery sections configured or processed.</p></body></html>"
                with open(f"{OUTPUT_SITE_DIR}/index.html", "w", encoding="utf-8") as f: f.write(placeholder_index_content)
                print("No gallery sections defined or processed. Created a placeholder index.html.")
        else:
            placeholder_index_content = "<!DOCTYPE html><html><head><title>Gallery</title></head><body><p>No gallery sections configured.</p></body></html>"
            with open(f"{OUTPUT_SITE_DIR}/index.html", "w", encoding="utf-8") as f: f.write(placeholder_index_content)
            print("No gallery sections defined. Created a placeholder index.html.")

        print(f"\nWebsite generation complete. Files are in: {os.path.abspath(OUTPUT_SITE_DIR)}")
        print(f"Open {os.path.join(os.path.abspath(OUTPUT_SITE_DIR), 'index.html')} in your browser.")

    except FileNotFoundError as e:
        print(f"Error: A required file was not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
