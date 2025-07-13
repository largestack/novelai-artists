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
    #(0.5, "x-ai/grok-3-mini"),
    (0.5, "x-ai/grok-3"),
    #(0.5, "thedrummer/anubis-70b-v1.1"),
]
# Overrides for default params
MODEL_PARAMS = {
    "thedrummer/anubis-70b-v1.1": {
        "temperature": 0.36
    },
}

# Base scenarios selection (weight, # of scenarios)
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
    (0.75, "lesbian grossed by men"),
    (0.25, "a change room"),
    (0.25, "a bathroom"),
    (0.25, "a public restroom"),
]

INSPIRATION_OUTPUT = "inspiration_v1.txt"
TARGET_PROMPT_COUNT = 5000 # The total number of prompts you want in the file
PROMPTS_PER_GENERATION = 50 # How many prompts to ask for in each API call

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
    """Loads existing prompts from a text file. Returns an empty list if not found."""
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found. Starting with an empty list.")
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read lines and strip whitespace
            return [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"Error reading '{filepath}': {e}. Starting with an empty list.")
        return []

def save_prompts(filepath, data):
    """Saves the list of prompts to a text file, one prompt per line."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for prompt in data:
                f.write(prompt + '\n')
    except IOError as e:
        print(f"Error saving to '{filepath}': {e}")

def clean_and_parse_text_response(text_response):
    """
    Cleans and parses a text response containing a list of scenarios.
    """
    # Split the response by newlines and filter out any empty lines
    prompts = [line.strip() for line in text_response.split('\n') if line.strip()]
    
    # Optional: Further cleaning if the model adds numbering or bullet points
    cleaned_prompts = []
    for p in prompts:
        # Remove common list markers like "1. ", "- ", "* "
        cleaned_p = re.sub(r'^\s*\d+\.\s*|\s*-\s*|\s*\*\s*', '', p)
        if cleaned_p:
            cleaned_prompts.append(cleaned_p)
            
    return cleaned_prompts

def main():
    """Main function to generate and save prompts."""
    client = configure_client()

    # --- CHAT HISTORY SETUP ---
    system = """Follow the user's instructions carefully, and output a list of scenarios, with each scenario on a new line."""
    
    chat_history = [
        {
            "role": "user",
            "parts": [
                """
Output a large list of scenarios plus short descriptions of the scenario that leads to nonconsensual sex. They must be simple to depict the scenario in a single image or two and just a couple quotes, so only include simple ones that clearly immediately lead into sex in a noncon or reluctance. The woman is always the victim. Don't name characters.

Output as:
<2 sentence framing the characters>. <2 sentence story introduction, often with a speech quote or two included that clearly set the scene for the noncon sex>

Generate stories that fit into one of the below scenarios. Spread them out equally between these categories:
* {RULES_PLACEHOLDER}

Output {PROMPT_COUNT} scenarios, with each scenario on a new line.

Use a large variety in the scenarios, and be creative with the scenarios like a professional short story writer authoring unique and engaging scenarios that can be told very quickly. They must be creative and varied.

NOW OUTPUT THE RESULT. ONLY OUTPUT THE RESULT ONE PER LINE. DO NOT OUTPUT ANYTHING ELSE.
"""
            ]
        },
    ]
    

    # --- GENERATION LOOP ---
    all_prompts = load_prompts(INSPIRATION_OUTPUT)
    

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
                newly_generated_prompts = clean_and_parse_text_response(response_text)

                # Log the raw response for debugging
                print(f"Raw response from model: {response_text}")

                if newly_generated_prompts:
                    all_prompts.extend(newly_generated_prompts)
                    save_prompts(INSPIRATION_OUTPUT, all_prompts)
                    print(f"Success! Added {len(newly_generated_prompts)} prompts. Total is now {len(all_prompts)}.")
                    print(f"Data saved to '{INSPIRATION_OUTPUT}'.")
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
    print(f"All data saved in '{INSPIRATION_OUTPUT}'.")

if __name__ == "__main__":
    main()
