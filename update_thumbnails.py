import json
import os
from PIL import Image

# --- Hardcoded Configuration ---
JSON_FILE_PATH = 'women_data.json'
OUTPUT_JSON_FILE_PATH = 'women_data_updated.json' # Save to a new file initially, or same as input

BASE_IMAGE_OUTPUT_DIR = 'women_images'
THUMB_SUBDIR = 'thumb'
FULL_SUBDIR = 'full'

RAW_SIZE = (832, 1216) # Size of the raw images (width, height)
THUMB_RATE = 0.35
THUMB_SIZE = (int(RAW_SIZE[0] * THUMB_RATE), int(RAW_SIZE[1] * THUMB_RATE)) # Thumbnail size (width, height)
FULL_RATE = 0.7
FULL_MAX_SIZE = (int(RAW_SIZE[0] * FULL_RATE), int(RAW_SIZE[1] * FULL_RATE)) # Full size (width, height)
JPEG_QUALITY = 80
DELETE_OLD_FILES = True # Set to False if you don't want to delete old thumb/full

# --- Helper Functions ---
def ensure_dir(directory_path):
    """Creates a directory if it doesn't exist."""
    os.makedirs(directory_path, exist_ok=True)

def create_and_save_image(raw_image_path, output_path, target_size, is_thumbnail=True, quality=85):
    """
    Opens an image, resizes it, and saves it.
    For thumbnails, it uses Image.thumbnail to maintain aspect ratio and fit within target_size.
    For "full" images, it resizes to fit within target_size while maintaining aspect ratio.
    """
    try:
        img = Image.open(raw_image_path)
        img = img.convert("RGB") # Ensure it's RGB to save as JPG

        if is_thumbnail:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
        else:
            # Resize while maintaining aspect ratio to fit within FULL_MAX_SIZE
            img.thumbnail(target_size, Image.Resampling.LANCZOS) # thumbnail also works for this

        img.save(output_path, "JPEG", quality=quality)
        print(f"Successfully saved: {output_path}")
        return True
    except FileNotFoundError:
        print(f"Error: Raw image not found at {raw_image_path}")
    except Exception as e:
        print(f"Error processing {raw_image_path} for {output_path}: {e}")
    return False

def try_delete_file(file_path):
    """Tries to delete a file if it exists."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted old file: {file_path}")
        except Exception as e:
            print(f"Could not delete old file {file_path}: {e}")
    # else:
    #     print(f"Old file not found, no need to delete: {file_path}")


# --- Main Script ---
def main():
    # Create output directories
    thumb_output_dir = os.path.join(BASE_IMAGE_OUTPUT_DIR, THUMB_SUBDIR)
    full_output_dir = os.path.join(BASE_IMAGE_OUTPUT_DIR, FULL_SUBDIR)
    ensure_dir(thumb_output_dir)
    ensure_dir(full_output_dir)

    try:
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {JSON_FILE_PATH}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE_PATH}")
        return

    updated_data = [] # Use a new list to store modified items

    for index, item in enumerate(data):
        print(f"\nProcessing item {index + 1}/{len(data)}: {item.get('id', 'N/A')}")

        raw_image_path = item.get('raw_image')
        if raw_image_path is None:
            raw_image_path = item.get('raw')
        if raw_image_path is None:
            raw_image_path = os.path.join("women_images_raw", item.get('id', '') + ".png")
            if not os.path.exists(raw_image_path):
                raw_image_path = None # If still None, it will be handled below
            else:
                item['raw_image'] = raw_image_path # Update item with the fallback path
                print(f"Using fallback raw image path: {raw_image_path}")

        if not raw_image_path:
            print(f"Skipping item due to missing 'raw_image' path.")
            updated_data.append(item) # Keep item as is if no raw image
            continue

        if not os.path.exists(raw_image_path):
            print(f"Skipping item: Raw image '{raw_image_path}' not found.")
            updated_data.append(item) # Keep item as is
            continue

        # Store old paths for deletion if needed
        old_thumb_path = item.get('thumb')
        old_full_path = item.get('full')

        # Generate new filename (e.g., women_7edb4bdbcd_4_full_1626844536.jpg)
        # Using filename_base and seed if available, otherwise id
        base_name_part = item.get('filename_base')
        seed_part = item.get('seed')

        if base_name_part and seed_part is not None: # seed can be 0
            new_filename = f"{base_name_part}_{seed_part}.jpg"
        elif item.get('id'):
            # Sanitize ID for use as filename if necessary, though example implies base+seed
            sanitized_id = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in item['id'])
            new_filename = f"{sanitized_id}.jpg"
        else:
            print(f"Skipping item: Cannot determine a unique filename (missing 'filename_base'/'seed' or 'id').")
            updated_data.append(item)
            continue

        new_thumb_path_relative = os.path.join(BASE_IMAGE_OUTPUT_DIR, THUMB_SUBDIR, new_filename)
        new_full_path_relative = os.path.join(BASE_IMAGE_OUTPUT_DIR, FULL_SUBDIR, new_filename)

        # Create thumbnail
        if create_and_save_image(raw_image_path, new_thumb_path_relative, THUMB_SIZE, is_thumbnail=True, quality=JPEG_QUALITY):
            item['thumb'] = new_thumb_path_relative
        else:
            print(f"Failed to create thumbnail for {raw_image_path}. 'thumb' field not updated.")


        # Create "full" resized image
        if create_and_save_image(raw_image_path, new_full_path_relative, FULL_MAX_SIZE, is_thumbnail=False, quality=JPEG_QUALITY):
            item['full'] = new_full_path_relative
        else:
            print(f"Failed to create full image for {raw_image_path}. 'full' field not updated.")


        # Try to delete old files AFTER new ones are potentially created and paths updated
        if DELETE_OLD_FILES:
            # Important: Only delete if the old path is different from any new path
            # This handles cases where old thumb/full might have been the same, or one might be same as new
            if old_thumb_path and old_thumb_path != new_thumb_path_relative and old_thumb_path != new_full_path_relative:
                try_delete_file(old_thumb_path)
            if old_full_path and old_full_path != new_full_path_relative and old_full_path != new_thumb_path_relative:
                try_delete_file(old_full_path)
            # Special case: if old thumb and full were the same, and one of them is now a new path,
            # the above logic correctly avoids deleting it if it's still needed by the other new path.
            # However, if they were the same and NEITHER matches a new path, one delete is enough.
            # The `os.path.exists` check in `try_delete_file` handles this gracefully.

        updated_data.append(item)

        # Save JSON progressively after each item (or group of items)
        # This is safer for long processes but can be I/O intensive.
        # For very large files, you might save every N items or only at the end.
        if (index + 1) % 1000 == 0:  # Save every 1000 items
            try:
                with open(OUTPUT_JSON_FILE_PATH, 'w') as f_out:
                    json.dump(updated_data, f_out, indent=2)
                # print(f"Progressively saved {len(updated_data)} items to {OUTPUT_JSON_FILE_PATH}")
            except Exception as e:
                print(f"Error saving JSON progressively: {e}")
                # Decide if you want to stop or continue

    # Final save after processing all items
    try:
        with open(OUTPUT_JSON_FILE_PATH, 'w') as f_out:
            json.dump(updated_data, f_out, indent=2)
        print(f"Final save completed. {len(updated_data)} items saved to {OUTPUT_JSON_FILE_PATH}")
    except Exception as e:
        print(f"Error saving final JSON: {e}")
    print(f"\nProcessing complete. Updated data saved to {OUTPUT_JSON_FILE_PATH}")

if __name__ == '__main__':
    main()
