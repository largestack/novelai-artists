#!/usr/bin/env python3
"""
NovelAI Gallery Site Generator
Refactored for cleanliness, maintainability, and production-grade quality.
"""

import os
import json
import base64
import random
import shutil
import requests
import argparse
import time
import zipfile
import hashlib
from PIL import Image
import io
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional, Tuple

# --- Constants and Configuration ---

# Core Paths
OUTPUT_SITE_DIR = "./output_site"
OUTPUT_DATA_DIR = "./output_images"  # Centralized directory for JSON data files
STATIC_ASSETS_DIR = "./static_assets"  # Source for CSS/JS

# Input Files
ARTISTS_FILE = "artists.txt"
PROMPT_TEMPLATE_FILE = "template.prompt"

# API & Generation
API_URL = "https://image.novelai.net"
NAI_CREDENTIALS_CACHE = ".nai_credentials.json"
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Site Structure Configuration
# Defines all gallery sections, their properties, and generation types.
# 'base_image_path_segment' is used to construct paths, ensuring backward compatibility.
# 'type' determines which payload (v3 for single prompt, v4 for multi-character) is used.
SITE_CONFIG = {
    "women": {
        "name": "Women",
        "prompt_file": "1girl.txt",
        "max_images": 45000,
        "base_image_path_segment": "images",
        "is_nsfw": False,
        "type": "v3"
    },
    "men": {
        "name": "Men",
        "prompt_file": "1boy.txt",
        "max_images": 5000,
        "base_image_path_segment": "images",
        "is_nsfw": False,
        "type": "v3"
    },
    "nsfw": {
        "name": "NSFW Zone",
        "prompt_file": "nsfw.txt",
        "max_images": 24000,
        "base_image_path_segment": "images/nsfw_gallery",
        "is_nsfw": True,
        "type": "v3"
    },
    "noncon": {
        "name": "Non-Con Gallery",
        "prompt_file": "prompts_gemini.json",
        "max_images": 24000,
        "base_image_path_segment": "images/noncon",
        "is_nsfw": True,
        "type": "v4",
        "hidden": True # This section will not appear in the navigation
    }
}

# Models available for generation
MODELS = [
    {"id": "nai-diffusion-4-full", "name": "NAI Diffusion 4 Full"},
    {"id": "nai-diffusion-4-curated-preview", "name": "NAI Diffusion 4 Curated"},
    {"id": "nai-diffusion-4-5-curated", "name": "NAI Diffusion 4.5 Curated"},
    {"id": "nai-diffusion-4-5-full", "name": "NAI Diffusion 4.5 Full"},
]
# The model used for all new image generations
NEW_GENERATION_MODEL_ID = "nai-diffusion-4-5-full"


class ConfigManager:
    """Handles loading and processing of all site configuration."""

    def __init__(self, site_config: Dict[str, Any]):
        self.config = site_config
        self._build_dynamic_paths()

    def _build_dynamic_paths(self):
        """Builds full, thumb, and raw image paths for each section."""
        for section_id, conf in self.config.items():
            # MODIFICATION: Point to the image source directory based on section ID.
            # This matches the user's structure: ./output_images/noncon/thumb/...
            image_source_path = os.path.join(OUTPUT_DATA_DIR, section_id)
            
            # This 'paths' key is now for the SOURCE files for reading/writing.
            conf["paths"] = {
                "full": os.path.join(image_source_path, "full"),
                "thumb": os.path.join(image_source_path, "thumb"),
                "raw": os.path.join(image_source_path, "raw"),
            }
            conf["data_file"] = os.path.join(OUTPUT_DATA_DIR, f"{section_id}_data.json")


    def get_section_config(self, section_id: str) -> Dict[str, Any]:
        return self.config[section_id]

    def get_all_sections(self) -> Dict[str, Any]:
        return self.config


class NovelAI_API:
    """A client to handle all communication with the NovelAI API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_url = API_URL
        self.headers = self._login(api_key)

    def _login(self, api_key: Optional[str]) -> Dict[str, str]:
        """Authenticates with NovelAI, prioritizing sources: CLI arg -> .env -> cache -> interactive."""
        load_dotenv()
        # 1. Prioritize API key from command line
        if api_key:
            print("Using API key from command-line argument.")
            return {"Authorization": f"Bearer {api_key}"}

        # 2. Check for persistent token in .env file
        env_token = os.getenv("NAI_PERSISTENT_TOKEN")
        if env_token:
            print("Using persistent token from .env file.")
            return {"Authorization": f"Bearer {env_token}"}

        # 3. Try to use cached credentials
        if os.path.exists(NAI_CREDENTIALS_CACHE):
            try:
                with open(NAI_CREDENTIALS_CACHE, "r") as f:
                    cached = json.load(f)
                print("Using cached access token.")
                return {"Authorization": f"Bearer {cached['accessToken']}"}
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Cached credentials file is invalid ({e}), deleting and re-authenticating.")
                os.remove(NAI_CREDENTIALS_CACHE)

        # 4. Fallback to interactive login
        print("\nNo valid credentials found. Please provide login details.")
        email = input("Enter NovelAI email (or paste an API Key): ")
        auth_url = f"{self.api_url}/user"
        auth_payload, auth_headers = {}, {}

        if "@" not in email and len(email) > 60:
            print("Input appears to be an API Key. Attempting to create a persistent token...")
            auth_url += "/create-persistent-token"
            auth_headers = {"Authorization": f"Bearer {email}"}
        else:
            password = input("Enter NovelAI password: ")
            auth_url += "/login"
            auth_payload = {"email": email, "password": password}

        try:
            response = requests.post(auth_url, json=auth_payload, headers=auth_headers)
            response.raise_for_status()
            data = response.json()
            access_token = data['accessToken']

            with open(NAI_CREDENTIALS_CACHE, "w") as f:
                json.dump({"accessToken": access_token}, f)

            print("\nAuthentication successful. Token has been cached.")
            return {"Authorization": f"Bearer {access_token}"}
        except requests.exceptions.HTTPError as e:
            msg = f"Authentication failed: {e.response.status_code} - {e.response.text}"
            print(msg)
            raise ConnectionError(msg) from e
        except Exception as e:
            msg = f"An unexpected error occurred during authentication: {e}"
            print(msg)
            raise ConnectionError(msg) from e

    def generate(self, payload: Dict[str, Any]) -> Optional[bytes]:
        """Sends a generation request to the API and extracts the image from the response."""
        try:
            response = requests.post(f"{self.api_url}/ai/generate-image", headers=self.headers, json=payload)
            response.raise_for_status()
            zip_bytes = io.BytesIO(response.content)
            with zipfile.ZipFile(zip_bytes, 'r') as zip_ref:
                image_filename = next((n for n in zip_ref.namelist() if n.endswith('.png')), None)
                if not image_filename:
                    raise IOError("No PNG image found in API response zip.")
                return zip_ref.read(image_filename)
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            if e.response:
                print(f"Response content: {e.response.text}")
            return None
        except Exception as e:
            print(f"Error processing API response: {e}")
            return None


class SiteGenerator:
    """Manages the creation of the static site, from image generation to HTML rendering."""

    def __init__(self, config_manager: ConfigManager, api_client: Optional[NovelAI_API]):
        self.config_manager = config_manager
        self.api = api_client
        self.artists = self._read_file_lines(ARTISTS_FILE)
        try:
            with open(PROMPT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
                self.prompt_template = f.read()
        except FileNotFoundError:
            print(f"Warning: {PROMPT_TEMPLATE_FILE} not found. V3 generation will fail.")
            self.prompt_template = "{{prompt}}" # Fallback

    @staticmethod
    def _read_file_lines(filepath: str) -> List[str]:
        """Reads non-empty lines from a text file."""
        if not os.path.exists(filepath):
            print(f"Warning: File not found: {filepath}")
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
            
    def _read_section_prompts(self, prompt_file: str) -> List[Any]:
        """Loads prompts from either a .txt or .json file."""
        if not os.path.exists(prompt_file):
            print(f"Warning: Prompt file not found: {prompt_file}")
            return []
        if prompt_file.endswith(".json"):
            with open(prompt_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else: # Assumes .txt
            return self._read_file_lines(prompt_file)

    @staticmethod
    def _save_image_files(img_bytes: bytes, filename_stem: str, paths: Dict[str, str]) -> Dict[str, str]:
        """Saves raw, full, and thumbnail versions of an image."""
        img = Image.open(io.BytesIO(img_bytes))
        
        # Save raw PNG
        raw_path = os.path.join(paths["raw"], f"{filename_stem}.png")
        with open(raw_path, "wb") as f: f.write(img_bytes)

        # Save full-size JPEG for display
        full_path = os.path.join(paths["full"], f"{filename_stem}.jpg")
        full_img = img.copy()
        full_img.thumbnail((int(img.width * 0.7), int(img.height * 0.7)), Image.Resampling.LANCZOS)
        full_img.convert("RGB").save(full_path, "JPEG", quality=80)
        
        # Save thumbnail JPEG
        thumb_path = os.path.join(paths["thumb"], f"{filename_stem}.jpg")
        thumb_img = img.copy()
        thumb_img.thumbnail((int(img.width * 0.35), int(img.height * 0.35)), Image.Resampling.LANCZOS)
        thumb_img.convert("RGB").save(thumb_path, "JPEG", quality=80)

        return {"full": full_path, "thumb": thumb_path, "raw": raw_path}

    def _create_v3_payload(self, prompt: str, artist: str, seed: int, is_nsfw: bool) -> Dict[str, Any]:
        """Creates the API payload for standard single-prompt (V3-style) generation."""
        full_prompt = self.prompt_template.replace("{{prompt}}", prompt).replace("{{artist}}", artist)
        if is_nsfw:
            full_prompt += ", nsfw, uncensored"
        
        base_prompt = f"{full_prompt}, no text, best quality, masterpiece, very aesthetic, absurdres"
        negative_prompt = "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page"
        if is_nsfw:
             negative_prompt += ", shota, child"
        else:
             negative_prompt += ", nsfw"

        return {
            "input": base_prompt, "model": NEW_GENERATION_MODEL_ID, "action": "generate",
            "parameters": { "params_version": 3, "width": 832, "height": 1216, "scale": 6, "sampler": "k_dpmpp_2m_sde", "steps": 28, "n_samples": 1, "ucPreset": 0, "qualityToggle": True, "seed": seed, "negative_prompt": negative_prompt }
        }

    def _create_v4_payload(self, prompt_obj: Dict[str, str], artist: str, seed: int) -> Dict[str, Any]:
        """Creates the API payload for multi-character (V4-style) generation."""
        artist = "{artist:" + artist + "}" 
        base_prompt = f"{artist}, very aesthetic, masterpiece, absurdres, no text, {prompt_obj['prompt']}"
        if "character1" not in prompt_obj or "character2" not in prompt_obj:
            print("Warning: Missing character prompts in V4 payload. Skipping generation.")
            return {}
        char1_prompt = prompt_obj['character1']
        char2_prompt = prompt_obj['character2']
        negative_prompt = "lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page"

        return {
            "input": base_prompt, "model": NEW_GENERATION_MODEL_ID, "action": "generate",
            "parameters": {
                # --- Restored parameters from the old, working script ---
                "params_version": 3, "width": 832, "height": 1216, "scale": 5, "sampler": "k_euler_ancestral",
                "steps": 23, "n_samples": 1, "ucPreset": 0, "qualityToggle": True, "add_original_image": True,
                "cfg_rescale": 0, "noise_schedule": "karras", "seed": seed,
                
                # --- Corrected v4_prompt and v4_negative_prompt structure ---
                "v4_prompt": {
                    "caption": {
                        "base_caption": base_prompt, 
                        "char_captions": [
                            {"char_caption": char1_prompt, "centers": [{"x": 0.5, "y": 0.5}]}, 
                            {"char_caption": char2_prompt, "centers": [{"x": 0.5, "y": 0.5}]}
                        ]
                    }, 
                    "use_coords": False, 
                    "use_order": True
                },
                "v4_negative_prompt": {
                    "caption": {
                        "base_caption": negative_prompt, 
                        "char_captions": [
                            {"char_caption": "", "centers": [{"x": 0.5, "y": 0.5}]}, 
                            {"char_caption": "", "centers": [{"x": 0.5, "y": 0.5}]}
                        ]
                    }
                },

                # --- Added the CRITICAL missing characterPrompts key ---
                "characterPrompts": [
                    {"prompt": char1_prompt, "uc": "", "center": {"x": 0.5, "y": 0.5}, "enabled": True},
                    {"prompt": char2_prompt, "uc": "", "center": {"x": 0.5, "y": 0.5}, "enabled": True}
                ],
                
                "negative_prompt": negative_prompt
            }
        }


    def _load_existing_data(self, section_id: str, config: Dict[str, Any]) -> Tuple[List[Dict], set]:
        """Loads and validates existing image data from the section's JSON file."""
        data_file = config["data_file"]
        if not os.path.exists(data_file):
            return [], set()

        print(f"Loading existing data from {data_file} for section '{section_id}'")
        with open(data_file, "r", encoding="utf-8") as f:
            try:
                loaded_data = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Corrupt JSON file at {data_file}. Starting fresh.")
                return [], set()
        
        valid_results, processed_ids = [], set()
        paths = config["paths"]
        
        for item in loaded_data:
            item_id = item.get("id")
            if not item_id:
                continue
            
            # Check if all required image files exist
            if all(os.path.exists(os.path.join(p, f"{item_id}.{ext}")) for p, ext in [(paths["full"], "jpg"), (paths["thumb"], "jpg"), (paths["raw"], "png")]):
                valid_results.append(item)
                # Add a unique identifier for this generation to avoid duplicates
                if config["type"] == "v4":
                    processed_ids.add(item.get("prompt_hash"))
                else: # v3
                    processed_ids.add(item.get("filename_base"))
            else:
                 print(f"  Skipping stale/invalid item: {item_id} (missing files).")
        
        if len(loaded_data) != len(valid_results):
            print(f"Filtered data: {len(valid_results)} of {len(loaded_data)} records were valid.")
        
        return valid_results, processed_ids

    def process_section_images(self, section_id: str):
        """The main orchestrator for generating images for a single section."""
        if not self.api:
            print("API client not available. Skipping image generation.")
            return

        config = self.config_manager.get_section_config(section_id)
        print(f"\nProcessing section: {config['name']} ({config['type']} type)")

        final_results, processed_ids = self._load_existing_data(section_id, config)
        
        num_to_generate = config["max_images"] - len(final_results)
        if num_to_generate <= 0:
            print(f"Section '{section_id}' is full ({len(final_results)}/{config['max_images']}). No new generation needed.")
            return

        prompts = self._read_section_prompts(config["prompt_file"])
        if not prompts or not self.artists:
            print("Cannot generate images: Missing prompts or artists.")
            return

        print(f"Attempting to generate {num_to_generate} new images...")
        model_id_str = NEW_GENERATION_MODEL_ID.replace("nai-diffusion-", "").replace("-", "_")
        
        newly_added_count = 0
        random.shuffle(prompts)

        for prompt_data in prompts:
            if newly_added_count >= num_to_generate: break

            artist = random.choice(self.artists) # Simple random selection; can be balanced if needed
            seed = random.randint(1, 2**31 - 1)
            
            if config["type"] == "v4":
                prompt_hash = hashlib.md5(json.dumps(prompt_data, sort_keys=True).encode()).hexdigest()[:10]
                if prompt_hash in processed_ids: continue
                filename_base = f"{section_id}_{prompt_hash}_{model_id_str}"
                payload = self._create_v4_payload(prompt_data, artist, seed)
            else: # v3
                prompt_plus_model = prompt_data + NEW_GENERATION_MODEL_ID
                prompt_hash = hashlib.md5(prompt_plus_model.encode()).hexdigest()[:10]
                filename_base = f"{section_id}_{prompt_hash}_{model_id_str}"
                if filename_base in processed_ids: continue
                payload = self._create_v3_payload(prompt_data, artist, seed, config["is_nsfw"])
            
            print(f"  Generating image for: {filename_base} (seed: {seed})")
            image_bytes = self.api.generate(payload)

            if not image_bytes:
                print("  -> Generation failed. Skipping.")
                time.sleep(1)
                continue

            filename_stem = f"{filename_base}_{seed}"
            self._save_image_files(image_bytes, filename_stem, config["paths"])

            model_name = next((m["name"] for m in MODELS if m["id"] == NEW_GENERATION_MODEL_ID), NEW_GENERATION_MODEL_ID)
            
            image_record = {
                "id": filename_stem, "filename_base": filename_base, "artist": artist, 
                "model": NEW_GENERATION_MODEL_ID, "modelName": model_name, "seed": seed,
            }
            if config["type"] == "v4":
                image_record.update({
                    "prompt": prompt_data.get('prompt', ''),
                    "character1": prompt_data.get('character1', ''),
                    "character2": prompt_data.get('character2', ''),
                    "prompt_hash": prompt_hash
                })
            else: # v3
                image_record["prompt"] = payload["input"]

            final_results.append(image_record)
            processed_ids.add(prompt_hash if config["type"] == "v4" else filename_base)
            newly_added_count += 1

            # Save progress incrementally
            with open(config["data_file"], "w", encoding="utf-8") as f:
                json.dump(final_results, f, indent=2)
            time.sleep(0.2)
        
        print(f"Section '{section_id}' generation complete. Added {newly_added_count} new images.")

    def generate_all_html(self):
        """Generates all HTML files for the website."""
        print("\n--- Generating HTML Pages ---")
        all_sections = self.config_manager.get_all_sections()

        for section_id, config in all_sections.items():
            self.generate_section_html(section_id, config, all_sections)
            if config["is_nsfw"]:
                self.generate_nsfw_landing_page(section_id, config)

        self.generate_index_redirect(all_sections)
        print("\n--- Finalizing Site ---")
        print(f"Website generation complete. Files are in: {os.path.abspath(OUTPUT_SITE_DIR)}")

    def generate_section_html(self, section_id: str, config: Dict[str, Any], all_sections_for_nav: Dict[str, Any]):
        """Generates the main gallery page for a single section."""
        if not os.path.exists(config["data_file"]):
            print(f"No data file for '{section_id}'. Skipping HTML generation.")
            return

        with open(config["data_file"], "r", encoding="utf-8") as f:
            images_data = json.load(f)

        if not images_data:
            print(f"Data file for '{section_id}' is empty. Skipping HTML.")
            return

        title = f"NovelAI Gallery | {config['name']}"
        html_filename = os.path.join(OUTPUT_SITE_DIR, f"{section_id}.html")
        template_text = self.prompt_template if config["type"] == "v3" else "Prompts for this section are generated via LLM from a structured specification."

        # Prepare image data for JavaScript, including the bug fix for noncon
        images_data_for_js = []
        for img in images_data:
            js_img = {
                "id": img.get("id"),
                "artist": img.get("artist"),
                "model": img.get("model"),
                "modelName": img.get("modelName"),
                "prompt": img.get("prompt"),
                "seed": img.get("seed"),
            }
            # BUG FIX: Ensure character prompts are included for V4 sections
            if 'character1' in img: js_img['character1'] = img['character1']
            if 'character2' in img: js_img['character2'] = img['character2']
            images_data_for_js.append(js_img)
        
        # Navigation links
        nav_links_html = ""
        for s_id, s_conf in all_sections_for_nav.items():
            # MODIFICATION: Skip hidden sections in the navigation
            if s_conf.get("hidden"):
                continue
            is_active = 'class="active"' if s_id == section_id else ''
            # MODIFICATION: Use s_id instead of s_conf["id"]
            link_href = f'{s_id}_landing.html' if s_conf.get("is_nsfw") else f'{s_id}.html'
            nav_links_html += f'\n<li {is_active}><a href="{link_href}">{s_conf["name"]}</a></li>'

        js_data_assignment = f"""const galleryData = {{
            "sectionImages": {json.dumps(images_data_for_js, indent=2)},
            "template": {json.dumps(template_text)},
            "section": "{section_id}",
            "isNsfwSection": {json.dumps(config["is_nsfw"])},
            "imagePaths": {{
                "full": "{config['base_image_path_segment']}/full/",
                "thumb": "{config['base_image_path_segment']}/thumb/"
            }}
        }};"""

        html_content = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><link rel="stylesheet" href="css/style.css"></head>
<body>
    <div id="age-disclaimer-overlay" style="display: none;"><div id="age-disclaimer-modal"><h2>Age Verification</h2><p>You must be 18 years or older to view this content.</p><p>Please confirm your age to continue.</p><button id="age-confirm-button">I am 18 or older</button><button id="age-exit-button">Exit</button></div></div>
    <header><div class="logo-container"><h1>{title}</h1></div><div class="site-navigation"><nav><ul>{nav_links_html}</ul></nav></div><div class="controls"><input type="search" id="search-box" placeholder="Search..."><button id="favorites-toggle" class="action-button">Show Favorites</button><button id="theme-toggle" class="theme-button" title="Toggle Dark/Light Mode"></button></div></header>
    <div class="template-info"><h2>Base Prompt Template</h2><pre id="template-text"></pre></div>
    <div id="model-selector" class="model-selector"></div><div id="gallery" class="image-grid"></div>
    <div id="lightbox" class="lightbox"><span class="close">&times;</span><div class="lightbox-content"><img id="lightbox-img" src="" alt="Enlarged image"><div class="lightbox-info"><div class="artist-container"><span>Artist: </span><span id="lightbox-artist" title="Click to copy artist"></span></div><div id="favorite-container" class="favorite-container"><button id="favorite-button" class="favorite-button"><span id="favorite-icon" class="favorite-icon-gfx"></span><span id="favorite-text">Add to Favorites</span></button></div><div id="lightbox-related-images" class="related-images"></div><div id="lightbox-prompt-area" class="prompt-area"></div><div class="model-container"><span>Model: </span><span id="lightbox-model"></span></div><div class="seed-container"><span>Seed: </span><span id="lightbox-seed"></span></div></div></div></div>
    <div id="fullscreen-overlay" class="fullscreen-overlay"><img id="fullscreen-img" src="" alt="Fullscreen image"></div><div id="loading" class="loading">Loading more images...</div>
    <script>{js_data_assignment}</script><script src="js/character_gallery.js"></script>
</body></html>"""

        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generated section page: {html_filename}")

    def generate_nsfw_landing_page(self, section_id: str, config: Dict[str, Any]):
        """Generates a warning/landing page for an NSFW section."""
        landing_page_filename = os.path.join(OUTPUT_SITE_DIR, f"{section_id}_landing.html")
        html_content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Warning: {config['name']} Content</title><link rel="stylesheet" href="css/style.css"><style>body{{display:flex;justify-content:center;align-items:center;min-height:100vh;text-align:center;padding:1rem}}.disclaimer-box{{background-color:var(--card-background);color:var(--text-color);padding:2rem 3rem;border-radius:10px;box-shadow:var(--card-shadow);max-width:650px;border:1px solid #4a4a70}}.disclaimer-box h1{{color:#ff4757;margin-bottom:1.5rem}}.disclaimer-box p{{margin-bottom:1.5rem;line-height:1.7}}.actions a{{display:inline-block;background-color:#2ecc71;color:white;padding:.9rem 1.8rem;text-decoration:none;border-radius:5px;margin:.5rem;transition:background-color .2s ease-in-out,transform .2s ease;font-weight:700}}.actions a:hover{{background-color:#27ae60}}.actions a.exit{{background-color:#7f8c8d}}.actions a.exit:hover{{background-color:#6c7a7b}}</style></head><body><div class="disclaimer-box"><h1>🔞 Adult Content Warning</h1><p>The section "<strong>{config['name']}</strong>" contains material that may be sexually explicit. You must be <strong>18 years of age or older</strong> to proceed.</p><div class="actions"><a href="{section_id}.html">Enter (I am 18+)</a><a href="index.html" class="exit">Exit</a></div></div></body></html>"""
        with open(landing_page_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generated NSFW landing page: {landing_page_filename}")

    def generate_index_redirect(self, all_sections: Dict[str, Any]):
        """Generates an index.html that redirects to the first available gallery page."""
        # MODIFICATION: Find the first non-hidden section to redirect to.
        first_sfw = next((s_id for s_id, s_conf in all_sections.items() if not s_conf.get("is_nsfw") and not s_conf.get("hidden")), None)
        first_nsfw = next((s_id for s_id, s_conf in all_sections.items() if s_conf.get("is_nsfw") and not s_conf.get("hidden")), None)
        
        target_url = None
        if first_sfw:
            target_url = f"{first_sfw}.html"
        elif first_nsfw:
            target_url = f"{first_nsfw}_landing.html"
            
        if target_url:
            html_content = f'<!DOCTYPE html><html><head><title>Redirecting...</title><meta http-equiv="refresh" content="0;url={target_url}"></head><body><p>Redirecting to <a href="{target_url}">{target_url}</a>...</p></body></html>'
            with open(os.path.join(OUTPUT_SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Generated index.html redirect to {target_url}")


def setup_directories(config_manager: ConfigManager):
    """Creates the necessary directory structure for the site and assets."""
    print("--- Setting up directories ---")
    os.makedirs(OUTPUT_SITE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)
    
    for section_conf in config_manager.get_all_sections().values():
        for path in section_conf["paths"].values():
            os.makedirs(path, exist_ok=True)

    # Copy static assets (CSS, JS)
    for asset_type in ["css", "js"]:
        src_dir = os.path.join(STATIC_ASSETS_DIR, asset_type)
        dest_dir = os.path.join(OUTPUT_SITE_DIR, asset_type)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
            print(f"Copied {src_dir} to {dest_dir}")

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate a static gallery website with NovelAI images.")
    parser.add_argument("--api-key", help="NovelAI API key (overrides .env or cached tokens).")
    parser.add_argument("--no-generate", action="store_true", help="Skip image generation, only build HTML from existing data.")
    parser.add_argument("--sections", nargs='+', help="Specify which sections to process (e.g., --sections women nsfw). Overrides other filters.")
    parser.add_argument("--generate-nsfw", action="store_true", help="Only process sections marked as NSFW.")
    parser.add_argument("--generate-noncon", action="store_true", help="Shortcut to only process the 'noncon' section.")
    parser.add_argument("--create-env-template", action="store_true", help="Create a template .env file and exit.")
    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_arguments()

    if args.create_env_template:
        if not os.path.exists(".env"):
            with open(".env", "w") as f: f.write("NAI_PERSISTENT_TOKEN=your_token_here\n")
            print("Created .env template file.")
        else:
            print(".env file already exists.")
        return

    try:
        config_manager = ConfigManager(SITE_CONFIG)
        setup_directories(config_manager)

        api_client = None
        if not args.no_generate:
            try:
                api_client = NovelAI_API(args.api_key)
            except ConnectionError:
                print("Could not log in to NovelAI. Forcing --no-generate mode.")
                args.no_generate = True

        generator = SiteGenerator(config_manager, api_client)

        # Determine which sections to process based on CLI flags
        all_sections = config_manager.get_all_sections()
        sections_to_process = list(all_sections.keys())

        if args.sections:
            sections_to_process = [s for s in args.sections if s in all_sections]
            print(f"Processing specified sections: {sections_to_process}")
        elif args.generate_noncon:
            sections_to_process = ["noncon"]
            print("Processing only the 'noncon' section.")
        elif args.generate_nsfw:
            sections_to_process = [s_id for s_id, s_conf in all_sections.items() if s_conf["is_nsfw"]]
            print("Processing only NSFW sections.")

        if not args.no_generate:
            for section_id in sections_to_process:
                generator.process_section_images(section_id)
        
        generator.generate_all_html()

    except Exception as e:
        import traceback
        print(f"\nFATAL ERROR: An unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
