import random
import json
import datetime

# --- Advanced Component Dictionaries and Lists ---

# Breast sizes with specified distribution
BREAST_SIZES = ["flat chest", "small breasts", "medium breasts", "large breasts", "huge breasts"]
BREAST_WEIGHTS = [0.20, 0.50, 0.10, 0.10, 0.10]

# --- Core Scenarios ---
# Scenarios provide a narrative backbone, linking location, props, and character roles.

SCENARIOS = {
    "dubcon": [
        {
            "name": "Dungeon Captivity",
            "location": "dungeon",
            "props": ["stone walls", "torchlight", "hay on floor", "shackles on wall"],
            "dominant_role": {"name": "Captor", "action": "forcing themself on the captive"},
            "submissive_role": {"name": "Captive", "action": "being pinned down"},
            "theme_tags": ["bondage", "captivity", "struggle"]
        },
        {
            "name": "Office Blackmail",
            "location": "corporate office",
            "props": ["mahogany desk", "large window overlooking city", "incriminating photos on desk", "spilled coffee"],
            "dominant_role": {"name": "Boss", "action": "asserting dominance from behind"},
            "submissive_role": {"name": "Subordinate", "action": "bent over desk"},
            "theme_tags": ["blackmail", "power imbalance", "humiliation"]
        },
        {
            "name": "Alleyway Ambush",
            "location": "dark alley",
            "props": ["brick walls", "graffiti", "overflowing dumpster", "single dim light"],
            "dominant_role": {"name": "Attacker", "action": "pinning them against the wall"},
            "submissive_role": {"name": "Victim", "action": "being cornered and assaulted"},
            "theme_tags": ["ambush", "noncon", "fear"]
        },
        {
            "name": "Hypnotic Control",
            "location": "sterile lab",
            "props": ["glowing screens", "examination table", "hypnotic spiral on monitor", "wires"],
            "dominant_role": {"name": "Controller", "action": "manipulating their body"},
            "submissive_role": {"name": "Subject", "action": "passively receiving, under influence"},
            "theme_tags": ["mind control", "hypnosis", "unaware"]
        },
        {
            "name": "Somnophilia",
            "location": "bedroom",
            "props": ["moonlight through window", "messy sheets", "clothes on floor"],
            "dominant_role": {"name": "Watcher", "action": "having sex with sleeping person"},
            "submissive_role": {"name": "Sleeper", "action": "unconscious, being taken advantage of"},
            "theme_tags": ["somnophilia", "sleeping", "noncon"]
        }
    ],
    "consensual": [
        {
            "name": "Passionate Bedroom Encounter",
            "location": "cozy bedroom",
            "props": ["soft bedsheets", "candlelight", "romantic music playing softly"],
            "dominant_role": {"name": "Lover", "action": "passionately making love"},
            "submissive_role": {"name": "Lover", "action": "eagerly receiving"},
            "theme_tags": ["romance", "passion", "intimacy"]
        },
        {
            "name": "Spontaneous Living Room Fun",
            "location": "living room",
            "props": ["plush couch", "rug", "movie paused on TV"],
            "dominant_role": {"name": "Partner", "action": "playfully on top"},
            "submissive_role": {"name": "Partner", "action": "laughing, legs wrapped around partner"},
            "theme_tags": ["playful", "spontaneous", "loving"]
        },
        {
            "name": "Exhibitionist Beach Sex",
            "location": "secluded beach at night",
            "props": ["moonlit waves", "sand", "empty shoreline"],
            "dominant_role": {"name": "Exhibitionist", "action": "thrusting with abandon"},
            "submissive_role": {"name": "Exhibitionist", "action": "moaning loudly under the stars"},
            "theme_tags": ["exhibitionism", "public", "adventurous"]
        }
    ]
}

# --- Detailed Descriptor Lists ---

# General Appearance
HAIR_STYLES = ["long messy hair", "short pixie cut", "braided hair", "tight bun", "shaved head", "military buzz cut"]
HAIR_COLORS = ["jet black", "platinum blonde", "fiery red", "brunette", "unnatural blue", "hot pink"]
SKIN_TONES = ["pale ivory skin", "dark chocolate skin", "sun-kissed tan skin", "olive skin"]
BODY_TYPES = ["lithe and athletic", "soft and chubby", "heavily muscular", "tall and slender", "short and curvy"]
BODY_DETAILS = ["tribal tattoos on arm", "a large scar across back", "freckles across nose", "small birthmark on thigh", "body covered in sweat"]

# Clothing States (for dubcon scenarios)
CLOTHING_STATES = ["business suit in disarray", "torn t-shirt", "dress hiked up", "partially undressed", "uniform ripped open"]

# POV Character Fragments
POV_MAN_PARTS = ["muscular arms holding them down", "penis, thrusting", "looking down at their face"]
POV_WOMAN_PARTS = ["looking down at their chest", "hands gripping their partner's back", "seeing partner's face between their legs"]

# Role-Specific Expressions and Physicality
EXPRESSIONS = {
    "dubcon_dominant": ["predatory smirk", "cold and emotionless gaze", "angry and forceful expression", "look of intense concentration", "possessive stare"],
    "dubcon_submissive": ["face streaked with tears", "eyes wide with fear", "grimacing in pain", "blank and dissociated stare", "pleading eyes", "defiant glare"],
    "consensual": ["eyes closed in ecstasy", "biting lower lip in pleasure", "mouth open, moaning", "lovingly looking into partner's eyes", "playful smile"]
}

PHYSICAL_DETAILS = {
    "dubcon_dominant": ["firmly gripping their hair", "handprint visible on their skin", "pinning their wrists above their head", "{visible semen on body}"],
    "dubcon_submissive": ["bruises forming on thighs", "scratch marks on partner's back", "body trembling uncontrollably", "trying to push them away weakly", "gagged with cloth", "wrists bound by rope"],
    "consensual": ["hickeys on neck", "clutching the bedsheets", "body glistening with sweat", "arching back"]
}

POSITIONS = {
    "dominant": ["on top, pinning them down", "standing over them", "holding them from behind", "pushing their face into the mattress"],
    "submissive": ["on back, legs forced apart", "bent over a desk", "on their knees", "pressed against a wall"],
    "consensual": ["missionary", "cowgirl", "doggy style", "spooning", "standing and holding on to each other"]
}


# --- Generation Logic ---

def generate_character(gender, role_type, scenario, action):
    """Generates a description string for a character based on their role in a scenario."""
    desc_parts = [gender, "adult"]
    desc_parts.append(random.choice(SKIN_TONES))
    desc_parts.append(random.choice(HAIR_STYLES) + ", " + random.choice(HAIR_COLORS))
    desc_parts.append(random.choice(BODY_TYPES))
    if random.random() < 0.3: # 30% chance of a special body detail
        desc_parts.append(random.choice(BODY_DETAILS))

    if gender == "woman":
        desc_parts.append(random.choices(BREAST_SIZES, weights=BREAST_WEIGHTS)[0])
        desc_parts.append("{pussy lips visible}")

    # Clothing state for dubcon scenarios
    if "dubcon" in scenario['theme_tags'] and random.random() < 0.5:
        desc_parts.append(random.choice(CLOTHING_STATES))
    else:
        desc_parts.append("nude")

    # Role-based action, position, expression, and physical details
    desc_parts.append(action) # Main action from scenario

    if role_type == "dominant":
        desc_parts.append(random.choice(POSITIONS["dominant"]))
        desc_parts.append(random.choice(EXPRESSIONS["dubcon_dominant"]))
        desc_parts.append(random.choice(PHYSICAL_DETAILS["dubcon_dominant"]))
    elif role_type == "submissive":
        desc_parts.append(random.choice(POSITIONS["submissive"]))
        desc_parts.append(random.choice(EXPRESSIONS["dubcon_submissive"]))
        desc_parts.append(random.choice(PHYSICAL_DETAILS["dubcon_submissive"]))
    else: # Consensual
        desc_parts.append(random.choice(POSITIONS["consensual"]))
        desc_parts.append(random.choice(EXPRESSIONS["consensual"]))
        desc_parts.append(random.choice(PHYSICAL_DETAILS["consensual"]))

    return ", ".join(desc_parts)


def generate_entry():
    """Generates a single, coherent JSON entry based on a randomly selected scenario."""
    entry = {}
    is_dubcon = random.random() < 0.5

    if is_dubcon:
        scenario = random.choice(SCENARIOS["dubcon"])
        roles = ["dominant", "submissive"]
    else:
        scenario = random.choice(SCENARIOS["consensual"])
        roles = ["consensual", "consensual"] # Both are equal partners

    random.shuffle(roles)
    role1, role2 = roles

    # Assign genders
    genders = ["man", "woman"]
    random.shuffle(genders)
    gender1, gender2 = genders
    
    # Handle POV
    is_pov = random.random() < 0.25
    pov_character_gender = None
    camera_angle = random.choice(["close-up", "medium shot", "low angle", "high angle", "pov"])
    if is_pov and camera_angle == "pov":
        pov_character_gender = random.choice(genders)
        camera_angle = f"pov {pov_character_gender}"

    # Generate Character Descriptions
    action1 = scenario['dominant_role']['action'] if role1 == "dominant" else scenario['submissive_role']['action'] if role1 == "submissive" else scenario['dominant_role']['action']
    action2 = scenario['dominant_role']['action'] if role2 == "dominant" else scenario['submissive_role']['action'] if role2 == "submissive" else scenario['submissive_role']['action']
    
    char1_desc = generate_character(gender1, role1, scenario, action1)
    char2_desc = generate_character(gender2, role2, scenario, action2)
    
    # Simplify POV character's description
    if pov_character_gender:
        if pov_character_gender == gender1:
            pov_parts = random.choice(POV_MAN_PARTS) if gender1 == "man" else random.choice(POV_WOMAN_PARTS)
            char1_desc = f"{gender1}, adult, pov, {pov_parts}"
        else:
            pov_parts = random.choice(POV_MAN_PARTS) if gender2 == "man" else random.choice(POV_WOMAN_PARTS)
            char2_desc = f"{gender2}, adult, pov, {pov_parts}"

    entry['character1'] = char1_desc
    entry['character2'] = char2_desc

    # Generate Prompt
    prompt_list = ["nsfw", scenario['name']]
    prompt_list.extend(scenario['props'])
    prompt_list.append(camera_angle)
    prompt_list.extend(scenario['theme_tags'])
    prompt_list.append("detailed background")
    
    entry['prompt'] = ", ".join(prompt_list)

    return entry

# --- Main Execution ---

if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    num_entries_to_generate = 50
    generated_data = [generate_entry() for _ in range(num_entries_to_generate)]
    
    output_filename = f"advanced_nsfw_training_data_{timestamp}.json"
    
    with open(output_filename, 'w') as f:
        json.dump(generated_data, f, indent=2)

    print(f"Successfully generated {num_entries_to_generate} advanced entries.")
    print(f"Data saved to '{output_filename}'")
    
    print("\n--- Example Advanced Entry ---")
    print(json.dumps(generated_data[0], indent=2))
