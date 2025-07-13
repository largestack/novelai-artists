from openai import OpenAI
import json
import os
import time
import re
import random

# --- CONFIGURATION ---
# NOTE: "Gemini 2.5 Flash" is not an official model name as of June 2025.
# The latest available flash model is used instead.
#MODEL_NAME = "gemini-1.5-flash-001" 
#MODEL_NAME = "gemini-2.5-flash-preview-05-20"  # Use the latest flash model available
#MODEL_NAME = "gemini-2.5-pro-preview-06-05"  # Use the latest flash model available
MODELS = [
    (0.5, "x-ai/grok-3-mini"),
    #(0.5, "x-ai/grok-3"),
    #(0.5, "thedrummer/anubis-70b-v1.1"),
]+*
# Overrides for default params
MODEL_PARAMS = {
    "thedrummer/anubis-70b-v1.1": {
        "temperature": 0.36
    },
}

# Base scenarios selection (weight, # of scenarios)
BASE_NUM_SCENARIOS = [
  (0.25, 1),  # 1 scenarios with weight 0.25
  (0.25, 2),  # 2 scenarios with weight 0.25
  (0.25, 3),  # 3 scenarios with weight 0.25
  (0.25, 4),  # 4 scenarios with weight 0.25
  (0.25, 5),  # 5 scenarios with weight 0.25
]
BASE_NUM_SCENARIOS = [
  (0.25, 5),  # 10 scenarios with weight 0.25
]

# Base scenarios (weight, description)
BASE_SCENARIOS = [
    (3.0, "a brat and incest"),
    (0.5, "a bathing suit"),
    (0.5, "a sport"),
    (0.5, "incest"),
    (0.5, "unconciousness"),
    (0.5, "asleep and not waking up"),
    (0.5, "breeding against their will"),
    (0.25, "royalty"),
    (0.25, "war or pillaging"),
    (0.25, "doctors such as therapists, doctors, etc."),
    (0.25, "an alley, backstreet, warehouse, or similar location"),
    (0.25, "homelessness, poverty, or similar themes"),
    (0.25, "public use"),
    (0.25, "public places"),
    (0.25, "conquest"),
    (0.25, "mind control"),
    (0.25, "blackmail"),
    (0.25, "naivity"),
    (0.25, "a home invasion or break-in"),
    (0.25, "caught doing something bad"),
    (0.25, "not listening to a warning or instruction"),
    (1.0, "a one-piece swimsuit"),
    (0.25, "spiked drinks or food"),
    (0.25, "drugs and addiction"),
    (0.25, "teachers"),
    (0.25, "incest, uncle or cousin"),
    (0.25, "visible disability or visible physical impairment"),
    (0.25, "amputee"),
    (0.25, "disciplinary authority & enforced obedience"),
    (0.25, "forced re-education"),
    (0.25, "withholding something key from the victim"),
    (0.25, "distopian or post-apocalyptic settings"),
    (2.00, "a step dad or brother and bratty girl"),
    (0.25, "a babysitter"),
    (0.25, "a nanny"),
    (0.25, "a public pool"),
    (0.25, "a dungeon"),
    (0.25, "a princess"),
    (0.25, "being poverty stricken and selling family"),
    (0.25, "forced breeding programs"),
    (0.25, "conquest of a virgin queen or princess"),
    (0.25, "a college or university"),
    (0.25, "a locker room or changing room"),
    (0.25, "a hotel or motel"),
    (2.00, "forced prostitution"),
    (0.25, "a teacher"),
    (0.25, "a coach or sports trainer"),
    (0.25, "a best friend or close acquaintance"),
    (0.25, "a house party or social gathering"),
    (0.25, "a futuristic or sci-fi setting"),
    (0.25, "intoxication (alcohol, drugs)"),
    (0.25, "a wedding or marriage ceremony."),
    (0.25, "a specific power dynamic"),
    (0.25, "a specific legal scenario"),
    (0.25, "a specific emotional state"),
    (0.25, "a specific physical action (choking, restraint)"),
    (0.25, "a specific technology (phone, computer, etc.)"),
    (0.25, "a specific entertainment venue (theater, cinema)"),
    (0.25, "a specific transportation method (car, bus, train)"),
    (0.25, "a family vacation or trip"),
    (0.25, "a neighbor or close family friend"),
    (0.25, "a historical or medieval setting"),
    (0.25, "a fantasy or magical realm"),
    (0.25, "a farm or rural environment"),
    (0.25, "a beach or seaside location"),
    (0.25, "a gang or organized crime group"),
    (0.25, "a haunted or abandoned building"),
    (0.25, "a stranger in a foreign country"),
    (0.25, "a betrayal by a trusted partner"),
    (0.25, "a power imbalance in a relationship"),
    (0.25, "a kidnapping or abduction"),
    (0.25, "a stalker or obsessive individual"),
    (0.25, "a forced marriage or arrangement"),
    (0.25, "a survival scenario or disaster"),
    (0.25, "a road trip or long journey"),
    (0.25, "a supernatural or paranormal entity"),
    (0.25, "a mental institution or asylum"),
    (0.25, "a theater or performance setting"),
    (0.25, "a festival or crowded event"),
    (0.25, "a library or quiet study area"),
    (0.25, "a desert or arid environment"),
    (0.25, "a construction site or industrial area"),
    (0.25, "a therapist or counselor session"),
    (0.25, "a student-teacher dynamic"),
    (0.25, "a blackmail over personal secrets"),
    (0.25, "a family feud or rivalry"),
    (0.25, "a gang initiation or rite"),
    (0.25, "a forced experiment or trial"),
    (0.25, "a backalley"),
    (0.25, "a zombie apocalypse or similar scenario"),
    (0.25, "a social media or online exposure"),
    (0.25, "a post-disaster chaos setting"),
    (0.25, "a toxic or abusive relationship"),
    (0.25, "a forced partnership or alliance"),
    (0.25, "a forbidden area or trespassing"),
    (0.25, "a corrupt official or leader"),
    (0.25, "a public rape"),
    (0.25, "criminals"),
    (0.25, "brigands or bandits"),
    (0.25, "age gap"),
    (0.25, "restraints"),
    (0.25, "torture or extreme pain"),
    (0.25, "strangling or choking"),
    (0.25, "a catgirl"),
    (0.25, "a magical girl"),
    (0.50, "a family"),
    (0.25, "a superhero and supervillain"),
    (0.25, "being stuck in a small space"),
    (0.25, "being stuck in a wall or similar"),
    (0.5, "slavery"),
    (0.25, "a forced marriage or arranged marriage"),
    (0.25, "a forced sexual relationship"),
    (0.25, "starwars"),
    (0.25, "star trek"),
    (0.25, "pokemon"),
    (0.25, "harry potter"),
    (2.0, "punishment or discipline"),
    (0.5, "a rich person"),
    (0.5, "pretending to wear a condom"),
    (0.5, "pretending that you will ejaculate outside"),
    (0.25, "pretending to be sterile"),
    (0.25, "pretending to be someone else"),
    (0.25, "pretending to be dying"),
    (0.25, "drunk"),
    (0.25, "drugged"),
    (0.25, "addicted to drugs"),
    (0.25, "confused"),
    (0.25, "hypnotized"),
    (0.25, "time-stop"),
    (0.25, "bondage"),
]

# Length suggestions (weight, description
BASE_LENGTH_SUGGESTIONS = [
    (0.5, "Characters and scenes should have around 20 tags each."),
]

JSON_FILE_PATH = "prompts_gemini_v6.json"
TARGET_PROMPT_COUNT = 5000 # The total number of prompts you want in the file
PROMPTS_PER_GENERATION = 20 # How many prompts to ask for in each API call

def weighted_choice(choices):
    """
    Selects an item from a list of (weight, item) tuples.
    """
    total_weight = sum(w for w, _ in choices)
    r = random.uniform(0, total_weight)
    upto = 0
    for w, c in choices:
        if upto + w >= r:
            return c
        upto += w
    return choices[-1][1] # Should not happen

def configure_client():
    """Checks for and configures the OpenRouter API key and returns a client."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set. Please set it to your API key.")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    print("OpenRouter client configured successfully.")
    return client

def load_prompts(filepath):
    """Loads existing prompts from a JSON file. Returns an empty list if not found."""
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found. Starting with an empty list.")
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure the data is a list
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading '{filepath}': {e}. Starting with an empty list.")
        return []

def save_prompts(filepath, data):
    """Saves the list of prompts to a JSON file with pretty printing."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving to '{filepath}': {e}")

def clean_and_parse_json(text_response):
    """
    A highly robust function to clean and parse JSON from a model's text response.
    It uses a multi-stage fallback process.
    """
    # --- Strategy 1: Find and parse a clean JSON block (markdown or raw) ---
    print("Parser: Trying Strategy 1 (Primary Extraction)...")
    match = re.search(r'```json\s*([\s\S]*?)\s*```|(\[[\s\S]*\])', text_response)
    if match:
        json_str = match.group(1) if match.group(1) else match.group(2)
        try:
            parsed_json = json.loads(json_str)
            print("Parser: Strategy 1 Succeeded.")
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"Parser: Strategy 1 failed primary parse: {e}. Moving to Strategy 2.")
            
            # --- Strategy 2: Attempt to fix common errors like trailing commas ---
            print("Parser: Trying Strategy 2 (Fix Trailing Commas)...")
            # Remove trailing commas before a closing bracket or brace
            cleaned_str = re.sub(r',\s*([\]}])', r'\1', json_str)
            try:
                parsed_json = json.loads(cleaned_str)
                print("Parser: Strategy 2 Succeeded.")
                return parsed_json
            except json.JSONDecodeError as e2:
                print(f"Parser: Strategy 2 failed: {e2}. Moving to Strategy 3.")
    else:
        print("Parser: Could not find a recognizable JSON block. Moving to Strategy 3.")

    # --- Strategy 3: Manually extract all valid top-level objects as a last resort ---
    print("Parser: Trying Strategy 3 (Individual Object Extraction)...")
    found_objects = []
    brace_level = 0
    start_index = -1

    for i, char in enumerate(text_response):
        if char == '{':
            if brace_level == 0:
                start_index = i
            brace_level += 1
        elif char == '}':
            if start_index != -1: # Ensure we are inside an object
                brace_level -= 1
                if brace_level == 0:
                    potential_obj_str = text_response[start_index:i+1]
                    try:
                        # Try to parse this individual object
                        parsed_obj = json.loads(potential_obj_str)
                        found_objects.append(parsed_obj)
                    except json.JSONDecodeError:
                        # This substring wasn't a valid object, just ignore it
                        pass
                    start_index = -1 # Reset to find the next object
    
    if found_objects:
        print(f"Parser: Strategy 3 Succeeded, extracted {len(found_objects)} individual objects.")
        return found_objects
    
    print("Parser: All strategies failed. Could not extract any valid JSON.")
    return [] # Return empty list if all parsing fails

def main():
    """Main function to generate and save prompts."""
    client = configure_client()

    # --- CHAT HISTORY SETUP ---
    # This history primes the model with our successful interaction to guide its output.
    n_examples = PROMPTS_PER_GENERATION
    
    system = """Follow the user's instructions carefully, and output a JSON array with the specified structure."""
    
    chat_history = [
        {
            "role": "user",
            "parts": [
                """
{
  "task": "Generate a JSON array with entries containing 'prompt', 'character1', and 'character2' following strict content guidelines.",
  "requirements": {
    "structure": {
      "format": "JSON array with entries containing three string keys: 'prompt', 'character1', 'character2'",
      "prompt": {
        "components": [
          "Must include 'nsfw, ' tag",
          "Short note on what the scene is about",
          "Scene location descriptors (indoor/outdoor, specific setting)",
          "Camera angles (overhead, POV, side-view, etc)",
          "Visible environmental objects, this can include background elements too",
          "Speech and thinking bubble text. It MUST be at the very end of this prompt section (format: one of 'speech bubble', 'speech bubbles', 'thought bubble', 'thought bubbles', or similar, and then ending with: ', Text:<speech or thought bubble 1 text>(<new line><new line><speech or thought bubble 2 text>)', where () denote optional and <> are placeholders that should be replaced and should not include quotes.)"
        ],
        "rules": [
          {RULES_PLACEHOLDER},
          "sexual intercourse",
          "Scenes must depict non-consensual or dubious consent sexual acts",
          "No markdown formatting in text",
          "Prioritize visual elements over auditory/sensory details",
          "Scenes have at least one speech or thinking bubble. The speech should be helping set the scene usually.",
          "Do not add anime tags",
        ]
      },
      "characters": {
        "gender": "Strictly male-female pairs. People in background is ok.",
        "descriptors": {
          "required": [
            "Demographic prefix ('man, adult,' or 'woman, adult,')",
            "Hairstyle (style, color, length), be detailed",
            "Body features",
            "If woman: breast size. 10% flat, 80% small, 10% medium/large",
            "Clothing state (eg. nude/specific garment details)",
            "Sexual act specifics (positions, penetration type)",
            "Facial expression (eg. crying, screaming, angry, gaze direction, eyes expression)",
            "Body position (eg. standing, lying, etc)",
            "Physical interactions (gripping, restraint marks, ...)",
            "Actions (e.g., 'giving blowjob', 'receiving sex', 'trying to get away', 'being held down', 'hands on hips', ...)"
          ],
          "conditionals": [
            "Include bruising/red marks for non-con scenes if appropriate",
            "BDSM gear descriptions where contextually relevant"
          ]
        }
      }
    },
    "content_distribution": {
      "anatomy": {
        "breasts": "10% flat, 80% small, 10% medium/large",
        "acts": {
          "primary": "90% vaginal intercourse",
          "secondary": "10% other acts (oral, etc)"
        }
      }
    },
    "style_constraints": {
      "artist_notes": "Reserve style tags for later injection",
      "prohibited": [
        "Underage descriptors",
        "Auditory/smell references"
      ]
    }
  },
  "output_instructions": {
    "quantity": "{PROMPT_COUNT} unique and diverse entries",
    "diversity": "Maximize scenario variation across entries",
    "specificity": "Atomic detail level for tags (e.g., 'plain red sweater with white collar' not 'shirt')",
    "formatting": "Escape special characters in speech text"
  }
}

{OUTPUT_PLACEHOLDER}

NOW OUTPUT THE ARRAY OF JSON RESULT. EACH ENTRY MUST HAVE KEYS `prompt`, `character1`, `character2`. IT MUST START WITH EXACTLY THIS:
```json
"""
            ]
        },
    ]
    

    # --- GENERATION LOOP ---
    all_prompts = load_prompts(JSON_FILE_PATH)
    

    while len(all_prompts) < TARGET_PROMPT_COUNT:
        # Deep copy the chat history to avoid modifying the original
        from copy import deepcopy
        history = deepcopy(chat_history)  # Use deepcopy to ensure we don't modify the original chat history

        history[0]["parts"][0] = history[0]["parts"][0].replace("{{PROMPTS_PER_GENERATION}}", str(PROMPTS_PER_GENERATION))
        history[0]["parts"][0] = history[0]["parts"][0].replace("{{PROMPTS_PER_GENERATION-1}}", str(PROMPTS_PER_GENERATION - 1))

        # Select a model and its parameters
        model_name = weighted_choice(MODELS)
        model_params = MODEL_PARAMS.get(model_name, {})
        print(f"Selected model: {model_name} with params: {model_params}")

        # Select number of scenarios
        num_scenarios = weighted_choice(BASE_NUM_SCENARIOS)
        
        # Select scenarios
        selected_rules = []
        # Create a copy of the list to avoid modifying the original
        scenarios_copy = BASE_SCENARIOS.copy()
        for i in range(num_scenarios):
            if not scenarios_copy:
                break
            rule = weighted_choice(scenarios_copy)
            selected_rules.append(rule)

            # Remove the selected rule to avoid duplicates
            scenarios_copy = [(w, r) for w, r in scenarios_copy if r != rule]
        # Format the selected rules into a single string
        rules_str = " OR ".join(selected_rules)
        rules_str = f'"Scenes must involve {rules_str}"'
        history[0]["parts"][0] = history[0]["parts"][0].replace("{RULES_PLACEHOLDER}", rules_str)

        # Select length suggestion
        length_suggestion = weighted_choice(BASE_LENGTH_SUGGESTIONS)
        history[0]["parts"][0] = history[0]["parts"][0].replace("{OUTPUT_PLACEHOLDER}", length_suggestion)
        history[0]["parts"][0] = history[0]["parts"][0].replace("{PROMPT_COUNT}", str(PROMPTS_PER_GENERATION))

        # print the current chat history for debugging
        print("\nCurrent chat history:")
        for entry in history:
            print(f"{entry['role']}: {entry['parts'][0]}")

        current_count = len(all_prompts)
        print(f"\nCurrently have {current_count} prompts. Target is {TARGET_PROMPT_COUNT}.")
        print(f"Requesting {PROMPTS_PER_GENERATION} more prompts from the model...")

        retry_count = 20
        while retry_count > 0 and len(all_prompts) < TARGET_PROMPT_COUNT:
            try:
                # The new request to the model
                messages = [
                    {"role": "system", "content": system}
                ]
                for entry in history:
                    messages.append({"role": entry["role"], "content": entry["parts"][0]})

                completion_params = {
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": 8192,
                }
                # Add model-specific parameters
                completion_params.update(model_params)

                response = client.chat.completions.create(**completion_params)
                
                response_text = response.choices[0].message.content
                newly_generated_prompts = clean_and_parse_json(response_text)

                # Log the raw response for debugging
                print(f"Raw response from model: {response_text}")

                if newly_generated_prompts and isinstance(newly_generated_prompts, list) and len(newly_generated_prompts) > 0 and all(isinstance(entry, dict) for entry in newly_generated_prompts):
                    # Validate first entry
                    first_entry = newly_generated_prompts[0]
                    if not all(key in first_entry for key in ['prompt', 'character1', 'character2']):
                        print("Invalid format in generated prompts. Missing required keys.")
                        raise ValueError("Generated prompts do not match expected format.")

                    all_prompts.extend(newly_generated_prompts)
                    save_prompts(JSON_FILE_PATH, all_prompts)
                    print(f"Success! Added {len(newly_generated_prompts)} prompts. Total is now {len(all_prompts)}.")
                    print(f"Data saved to '{JSON_FILE_PATH}'.")
                    break
                else:
                    print("Could not get a valid list of prompts from the model on this attempt. Trying again.")

            except Exception as e:
                print(f"Retry {20 - retry_count} failed with error: {e}")
                print("Waiting for 2 seconds before retrying...")
                time.sleep(2) # Wait a bit longer if there's a serious API error

                retry_count -= 1

        # A short delay to avoid hitting rate limits
        time.sleep(2)

    print(f"\nTarget of {TARGET_PROMPT_COUNT} prompts reached. Final count is {len(all_prompts)}.")
    print(f"All data saved in '{JSON_FILE_PATH}'.")

if __name__ == "__main__":
    main()
