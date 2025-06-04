import random
import json
from collections import OrderedDict

# Original tags_data with modifications for NSFW content
tags_data = {
    "eH": [ # Camera Angles - Increased POV, added POV man
        ["dutch angle", 3, [], [], [], []],
        ["from above", 5, [], [], [], []],
        ["from below", 5, [], [], [], []],
        ["from side", 5, [], [], [], []],
        ["straight-on", 4, [], [], [], []],
        ["looking at viewer", 3, [], [], [], []],
        ["profile", 3, [], [], [], []],
        ["pov", 7, [], [], [], []], # Increased weight
        ["pov man", 15, [], [], ["male"], []], # Added for specific request
        ["pov woman", 4, [], [], ["female"], []],  # Lower weight for woman POV
        ["dynamic angle", 4, [], [], [], []],
        ["selfie", 1, [], [], [], []], # Rare for these scenes
        ["worm's eye view", 2, [], [], [], []],
        ["facing viewer", 3, [], [], [], []],
        ["close-up on genitals", 6, [], [], [], []],
        ["crotch level shot", 6, [], [], [], []],
        ["ass view", 6, [], [], [], []],
        ["pussy view", 6, [], [], ["female"], []],
        ["penis view", 6, [], [], ["male"], []],
    ],
    "eV": [ # Focus - Emphasize body parts relevant to NSFW
        ["solo focus", 2, [], [], [], []],
        ["ass focus", 8, ["portrait"], [], [], ["front"]],
        ["pussy focus", 8, ["portrait"], [], ["female"], []],
        ["penis focus", 8, ["portrait"], [], ["male"], []],
        ["ball focus", 5, ["portrait"], [], ["male"], []],
        ["foot focus", 2, ["portrait", "cowboy shot", "upper body"], [], ["feet"], []], # Rare
        ["hip focus", 5, ["portrait"], [], [], []],
        ["back focus", 4, [], [], [], ["front"]],
        ["breast focus", 7, [], [], ["female"], []],
        ["nipple focus", 6, [], [], ["female"], []],
        ["armpit focus", 1, [], [], [], []], # Rare
        ["eye focus", 2, [], [], [], []],
        ["face focus", 4, [], [], [], []], # For expressions
        ["navel focus", 2, [], [], [], []],
        ["leg focus", 3, [], [], [], []],
        ["thigh focus", 4, [], [], [], []],
        ["hand focus", 2, [], [], [], []], # e.g. hand on penis/pussy
        ["mouth focus", 4, [], [], [], []], # For oral, expressions
        ["stomach focus", 3, [], [], [], []],
    ],
        "eZ": [ # Environment - Greatly expanded with more variety and non-con themes
        # --- Generic / Utility ---
        ["simple background", 7, [], [], [], []], # Increased weight slightly
        ["dark room", 6, [], [], [], []],         # Good for atmosphere, versatile
        ["indoors", 5, [], [], [], []],            # Generic indoor
        ["outdoors", 5, [], [], [], []],           # Generic outdoor
        ["on the floor", 6, [], [], [], []],       # Positional
        ["against a wall", 5, [], [], [], []],    # Positional

        # --- Common Indoor / Domestic ---
        ["bedroom", 15, [], [], [], []],          # Very common
        ["bed", 15, [], [], [], []],              # Very common
        ["living room", 8, [], [], [], []],
        ["couch", 9, [], [], [], []],
        ["kitchen", 5, [], [], [], []],
        ["kitchen counter", 4, [], [], [], []],
        ["dining room", 3, [], [], [], []],
        ["bathroom", 6, [], [], [], []],
        ["shower", 7, [], [], [], []],            # Higher weight for common scene
        ["bathtub", 4, [], [], [], []],
        ["study", 3, [], [], [], []],
        ["home office", 3, [], [], [], []],
        ["library (home)", 2, [], [], [], []],
        ["walk-in closet", 2, [], [], [], []],
        ["laundry room", 1, [], [], [], []],
        ["basement", 3, [], [], [], []],          # Can have non-con undertones
        ["attic", 2, [], [], [], []],             # Can have non-con undertones
        ["garage", 3, [], [], [], []],
        ["hallway", 3, [], [], [], []],
        ["stairs", 3, [], [], [], []],

        # --- Luxury / Specific Indoor ---
        ["hotel room", 7, [], [], [], []],
        ["luxury hotel suite", 4, [], [], [], []],
        ["motel room", 4, [], [], [], []],        # Can be grim/non-con
        ["dingy apartment", 3, [], [], [], []],   # Grim setting
        ["luxury apartment", 4, [], [], [], []],
        ["penthouse apartment", 3, [], [], [], []],
        ["mansion", 4, [], [], [], []],
        ["cabin (cozy)", 4, [], [], [], []],
        ["cabin (isolated/woods)", 3, [], [], [], []], # Non-con potential
        ["private pool (indoor)", 2, [], [], [], []],
        ["hot tub (private)", 4, [], [], [], []],
        ["private sauna", 3, [], [], [], []],
        ["home gym", 2, [], [], [], []],
        ["wine cellar", 1, [], [], [], []],
        ["panic room", 0.5, [], [], [], []],      # Non-con

        # --- Outdoor (Natural) ---
        ["forest", 5, [], [], [], []],             # General forest
        ["deep forest", 3, [], [], [], []],        # More isolated
        ["woods", 5, [], [], [], []],
        ["beach", 5, [], [], [], []],              # General beach
        ["secluded beach", 3, [], [], [], []],
        ["park (day)", 3, [], [], [], []],
        ["park (night)", 4, [], [], [], []],       # Riskier
        ["garden", 4, [], [], [], []],
        ["meadow", 3, [], [], [], []],
        ["field (rural)", 3, [], [], [], []],
        ["lakefront", 3, [], [], [], []],
        ["riverbank", 3, [], [], [], []],
        ["cave", 2, [], [], [], []],               # Non-con potential
        ["waterfall", 3, [], [], [], []],
        ["mountainside", 2, [], [], [], []],
        ["hiking trail (secluded)", 3, [], [], [], []],
        ["desert", 1, [], [], [], []],
        ["desert oasis", 1, [], [], [], []],
        ["swamp", 1, [], [], [], []],               # Can be grim
        ["jungle", 2, [], [], [], []],
        ["island (deserted)", 1, [], [], [], []],
        ["cliffside", 2, [], [], [], []],
        ["hot spring (natural)", 3, [], [], [], []],

        # --- Outdoor (Urban / Man-made) ---
        ["rooftop", 4, [], [], [], []],
        ["balcony", 4, [], [], [], []],
        ["patio", 4, [], [], [], []],
        ["alleyway", 5, [], [], [], []],           # Classic risky/non-con
        ["dark alleyway", 4, [], [], [], []],      # More specific non-con
        ["back alley", 5, [], [], [], []],
        ["construction site (night)", 3, [], [], [], []], # Non-con potential
        ["abandoned lot", 2, [], [], [], []],
        ["junkyard", 2, [], [], [], []],           # Grim, non-con
        ["playground (night)", 2, [], [], [], []], # Risky, taboo
        ["under a bridge", 3, [], [], [], []],     # Non-con potential
        ["ruins (ancient)", 1, [], [], [], []],
        ["ruins (modern/urban decay)", 2, [], [], [], []], # Non-con potential
        ["quarry", 1, [], [], [], []],
        ["gazebo", 2, [], [], [], []],
        ["cemetery", 2, [], [], [], []],           # Taboo, risky
        ["courtyard", 3, [], [], [], []],

        # --- Public / Semi-Public (General & Establishments) ---
        ["public bath", 3, [], [], [], []],        # Existing, riskier
        ["locker room", 3, [], [], [], []],
        ["showers (public/gym)", 3, [], [], [], []],
        ["changing room (store)", 3, [], [], [], []],
        ["fitting room", 4, [], [], [], []],
        ["public restroom", 3, [], [], [], []],
        ["toilet stall", 2, [], [], [], []],
        ["office (workplace, after hours)", 4, [], [], [], []],
        ["boss's office", 2, [], [], [], []],      # Power dynamic
        ["cubicle farm (empty)", 1, [], [], [], []],
        ["conference room (empty)", 2, [], [], [], []],
        ["classroom (empty)", 3, [], [], [], []],
        ["lecture hall (empty)", 2, [], [], [], []],
        ["university library (secluded stacks)", 3, [], [], [], []],
        ["school hallway (empty)", 2, [], [], [], []],
        ["dorm room", 5, [], [], [], []],
        ["frat house", 3, [], [], [], []],          # Party, non-con potential
        ["sorority house", 3, [], [], [], []],
        ["movie theater (back row/empty)", 3, [], [], [], []],
        ["nightclub", 4, [], [], [], []],
        ["nightclub bathroom", 3, [], [], [], []],
        ["nightclub VIP room", 2, [], [], [], []],
        ["bar", 4, [], [], [], []],
        ["bar bathroom", 3, [], [], [], []],
        ["bar backroom", 2, [], [], [], []],        # Non-con potential
        ["restaurant kitchen (closed)", 1, [], [], [], []],
        ["restaurant (empty)", 2, [], [], [], []],
        ["store (after hours)", 2, [], [], [], []],
        ["stockroom", 3, [], [], [], []],           # Non-con potential
        ["stairwell (public building)", 4, [], [], [], []],
        ["elevator (stuck or empty)", 3, [], [], [], []], # Non-con potential
        ["parking garage (secluded spot)", 4, [], [], [], []], # Non-con potential
        ["under bleachers", 3, [], [], [], []],     # Non-con potential
        ["stadium (empty)", 1, [], [], [], []],
        ["amusement park (hidden area/after hours)", 1, [], [], [], []],
        ["museum (empty exhibit/after hours)", 1, [], [], [], []],
        ["art gallery (private room/after hours)", 1, [], [], [], []],
        ["backstage (theater/concert)", 2, [], [], [], []],
        ["church (empty/confessional)", 1, [], [], [], []], # Taboo
        ["hospital room (unoccupied)", 1, [], [], [], []], # Risky (avoiding patient context directly for non-con for now unless explicitly for that theme)
        ["hospital utility closet", 1, [], [], [], []],
        ["gym (public, empty)", 3, [], [], [], []],
        ["dance studio (empty)", 2, [], [], [], []],
        ["recording studio (soundproof)", 1, [], [], [], []],
        ["warehouse", 3, [], [], [], []],           # Can be non-con

        # --- Vehicles ---
        ["car interior", 5, [], [], [], []],
        ["back seat of car", 4, [], [], [], []],
        ["front seat of car", 3, [], [], [], []],
        ["van interior", 3, [], [], [], []],        # Classic non-con
        ["truck cabin", 2, [], [], [], []],
        ["bus (empty/back)", 2, [], [], [], []],
        ["train compartment (private/empty)", 2, [], [], [], []],
        ["airplane lavatory", 1, [], [], [], []],   # Mile high
        ["boat cabin", 3, [], [], [], []],
        ["yacht deck", 2, [], [], [], []],
        ["cruise ship cabin", 3, [], [], [], []],
        ["limousine interior", 2, [], [], [], []],
        ["RV interior", 3, [], [], [], []],
        ["ambulance (unconventional)", 0.5, [], [], [], []], # Dark theme

        # --- Explicitly Non-Con / Captivity / Grim ---
        ["abandoned building", 4, [], [], [], []],
        ["abandoned house", 4, [], [], [], []],
        ["abandoned warehouse", 4, [], [], [], []],
        ["abandoned factory", 3, [], [], [], []],
        ["abandoned school", 2, [], [], [], []],
        ["abandoned hospital", 2, [], [], [], []], # Grim, non-con
        ["derelict shack", 3, [], [], [], []],
        ["dungeon", 3, [], [], [], []],            # Classic non-con
        ["cellar (locked)", 3, [], [], [], []],    # Non-con
        ["prison cell", 2, [], [], [], []],        # Non-con, power dynamic
        ["interrogation room", 1, [], [], [], []], # Power dynamic, non-con
        ["soundproof room", 2, [], [], [], []],    # Non-con
        ["torture chamber", 0.5, [], [], [], []],  # Extreme non-con
        ["brothel room", 3, [], [], [], []],       # Transactional, power
        ["slave auction block", 0.5, [], [], [], []], # Extreme non-con, historical
        ["human cage", 1, [], [], [], []],         # Captivity
        ["slum alley", 3, [], [], [], []],
        ["crack house", 1, [], [], [], []],        # Grim, desperation
        ["shipping container (locked)", 1, [], [], [], []], # Confinement
        ["underground bunker", 2, [], [], [], []], # Confinement
        ["secret laboratory", 1, [], [], [], []],  # Non-con, experimental
        ["asylum cell (padded room)", 1, [], [], [], []], # Non-con, vulnerability
        ["ritual site", 1, [], [], [], []],        # Non-con, dark cults
        ["sacrificial altar", 0.5, [], [], [], []], # Non-con
        ["crime scene (aftermath)", 0.5, [], [], [], []], # Very dark

        # --- Unique / Specific / Taboo ---
        ["on a stage (empty theater)", 2, [], [], [], []],
        ["in a display window (shop, after hours)", 0.5, [], [], [], []], # Exhibitionism
        ["glass room (observation)", 1, [], [], [], []], # Voyeurism, non-con
        ["operating room (unconventional)", 0.5, [], [], [], []], # Dark, medical fetish/non-con
        ["morgue", 0.5, [], [], [], []],           # Extreme taboo
        ["green screen room", 0.5, [], [], [], []], # Meta, filming
        ["server room (cold)", 0.5, [], [], [], []],
        ["rooftop pool (night)", 3, [], [], [], []],
        ["shipwreck (on beach/island)", 1, [], [], [], []],
        ["treehouse", 2, [], [], [], []],
        ["crypt", 1, [], [], [], []],              # Taboo
        ["haunted house (attraction, empty)", 1, [], [], [], []],
        ["sauna (public, empty)", 2, [], [], [], []], # Risky
        ["steam room (public, empty)", 2, [], [], [], []], # Risky
        ["control room (empty)", 1, [], [], [], []],
        ["observatory (night, empty)", 1, [], [], [], []],

        # --- Original Action-Environments (kept for compatibility, could be phased out for pure location + action tags) ---
        ["outdoor sex", 2, [], [], [], []],        # Original, now lower weight due to specifics
        ["forest sex", 2, [], [], [], []],         # Original
        ["beach sex", 2, [], [], [], []],          # Original
    ],

    "eU": [ # Background detail
        ["simple background", 10, [], [], [], []],
        ["indoors, detailed background", 5, [], [], [], []],
        ["outdoors, detailed background", 3, [], [], [], []], # Less common for these scenes
    ],
    "eJ": [ # Framing - Full body, close-ups more relevant
        ["portrait", 2, [], ["portrait_framing"], [], []], # Less focus on just face
        ["upper body", 3, [], ["upper_body_framing"], [], []],
        ["cowboy shot", 3, [], ["cowboy_shot_framing", "legs"], [], []],
        ["full body", 8, [], ["full_body_framing","legs","feet"], [], []],
        ["close-up", 7, [], ["close_up_framing"], [], []], # Good for genitals/action
        ["extreme close-up", 4, [], [], [], []],
        ["waist up", 4, [], [], [], []],
    ],
    "eG": [["", 4, [], [], [], []]], # Style - can be kept default
    "e_dollar": [ # Species - mostly human, but some variety can be kept if desired, low probability
        ["human", 50, [], [], [], []], # Explicitly add human as high weight
        ["cat ears, cat tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["elf, pointy ears", 5, [], ["ears", "pointy_ears", "elf_race"], [], []],
        ["demon horns, demon tail", 2, [], ["horns", "tail", "demon_race"], [], []],
    ],
    "eq": [ # Skin Color
        ["dark skin", 100, [], [], [], []],
        ["pale skin", 200, [], [], [], []],
        ["tan", 50, [], [], [], []],
        ["olive skin", 50, [], [], [], []],
        ["light skin", 150, [], [], [], []],
        ["medium skin", 100, [], [], [], []],
        ["very dark skin", 50, [], [], [], []],
        ["fair skin", 100, [], [], [], []],
        ["black skin", 50, [], [], [], []],
    ],
    "tm": [ # Eye Color
        ["blue eyes", 5, [], ["eyes"], [], []], 
        ["red eyes", 5, [], ["eyes"], [], []],
        ["green eyes", 5, [], ["eyes"], [], []],
        ["brown eyes", 5, [], ["eyes"], [], []],
        ["purple eyes", 5, [], ["eyes"], [], []],
        ["yellow eyes", 5, [], ["eyes"], [], []],
        ["pink eyes", 5, [], ["eyes"], [], []],
        ["grey eyes", 5, [], ["eyes"], [], []],
        ["black eyes", 5, [], ["eyes"], [], []],
        ["orange eyes", 5, [], ["eyes"], [], []],
    ],
    "eY": [ # Hair Length
        ["short hair", 5, [], ["hair"], [], []], 
        ["long hair", 5, [], ["hair", "longhair"], [], []],
        ["medium hair", 5, [], ["hair"], [], []],
        ["very long hair", 4, [], ["hair", "longhair"], [], []],
        ["shoulder-length hair", 4, [], ["hair"], [], []],
        ["bob cut", 4, [], ["hair"], [], []],
        ["pixie cut", 3, [], ["hair"], [], []],
        ["buzz cut", 3, [], ["hair"], [], []],
        ["hime cut", 3, [], ["hair"], [], []],
        ["undercut", 3, [], ["hair"], [], []],
        ["mohawk", 2, [], ["hair"], [], []],
        ["asymmetrical hair", 3, [], ["hair"], [], []],
        ["flipped hair", 3, [], ["hair"], [], []],
        ["floating hair", 3, [], ["hair"], [], []],
        ["hair down", 4, [], ["hair"], [], []],
        ["hair up", 4, [], ["hair"], [], []],
        ["chin-length hair", 4, [], ["hair"], [], []],
        ["jaw-length hair", 4, [], ["hair"], [], []],
        ["neck-length hair", 4, [], ["hair"], [], []],
        ["collarbone-length hair", 4, [], ["hair"], [], []],
        ["mid-back length hair", 4, [], ["hair", "longhair"], [], []],
        ["waist-length hair", 4, [], ["hair", "longhair"], [], []],
        ["hip-length hair", 4, [], ["hair", "longhair"], [], []],
        ["knee-length hair", 3, [], ["hair", "longhair"], [], []],
        ["floor-length hair", 3, [], ["hair", "longhair"], [], []],
        ["ankle-length hair", 3, [], ["hair", "longhair"], [], []],
        ["absurdly long hair", 3, [], ["hair", "longhair"], [], []],
        ["a-line bob", 3, [], ["hair"], [], []],
        ["graduated bob", 3, [], ["hair"], [], []],
        ["inverted bob", 3, [], ["hair"], [], []],
        ["asymmetric bob", 3, [], ["hair"], [], []],
        ["blunt bob", 3, [], ["hair"], [], []],
        ["layered bob", 3, [], ["hair"], [], []],
        ["angled bob", 3, [], ["hair"], [], []],
        ["pageboy cut", 3, [], ["hair"], [], []],
        ["bowl cut", 3, [], ["hair"], [], []],
        ["mushroom cut", 3, [], ["hair"], [], []],
        ["french crop", 3, [], ["hair"], [], []],
        ["crew cut", 3, [], ["hair"], [], []],
        ["fade haircut", 3, [], ["hair"], [], []],
        ["high and tight", 3, [], ["hair"], [], []],
        ["flattop", 2, [], ["hair"], [], []],
        ["ivy league cut", 2, [], ["hair"], [], []],
        ["butch cut", 2, [], ["hair"], [], []],
        ["taper cut", 3, [], ["hair"], [], []],
        ["disconnected undercut", 3, [], ["hair"], [], []],
        ["side-swept undercut", 3, [], ["hair"], [], []],
        ["pompadour", 3, [], ["hair"], [], []],
        ["quiff", 3, [], ["hair"], [], []],
        ["ducktail", 2, [], ["hair"], [], []],
        ["mullet", 2, [], ["hair"], [], []],
        ["shag cut", 3, [], ["hair"], [], []],
        ["wolf cut", 3, [], ["hair"], [], []],
        ["feathered hair", 3, [], ["hair"], [], []],
        ["layered hair", 4, [], ["hair"], [], []],
        ["wispy hair", 3, [], ["hair"], [], []],
        ["razor cut", 3, [], ["hair"], [], []],
        ["textured crop", 3, [], ["hair"], [], []],
        ["bixie cut", 3, [], ["hair"], [], []],
        ["lob haircut", 3, [], ["hair"], [], []],
        ["curtained hair", 3, [], ["hair"], [], []],
        ["mop top", 3, [], ["hair"], [], []],
        ["side part", 3, [], ["hair"], [], []],
        ["middle part", 3, [], ["hair"], [], []],
        ["deep side part", 3, [], ["hair"], [], []],
        ["zigzag part", 2, [], ["hair"], [], []],
        ["no part", 3, [], ["hair"], [], []],
        ["shaved sides", 3, [], ["hair"], [], []],
        ["shaved nape", 3, [], ["hair"], [], []],
        ["shaved head", 3, [], ["hair"], [], []],
        ["half-shaved head", 3, [], ["hair"], [], []],
        ["side-shaved", 3, [], ["hair"], [], []],
        ["partially shaved", 3, [], ["hair"], [], []],
        ["rat tail", 2, [], ["hair"], [], []],
        ["uneven cut", 3, [], ["hair"], [], []],
        ["choppy cut", 3, [], ["hair"], [], []],
        ["wedge cut", 2, [], ["hair"], [], []],
        ["hi-lo cut", 3, [], ["hair"], [], []],
        ["wolf cut", 3, [], ["hair"], [], []],
        ["princess cut", 3, [], ["hair"], [], []],
        ["octopus cut", 2, [], ["hair"], [], []],
        ["butterfly cut", 3, [], ["hair"], [], []],
        ["V-cut hair", 3, [], ["hair"], [], []],
        ["U-cut hair", 3, [], ["hair"], [], []],
        ["straight-across cut", 3, [], ["hair"], [], []],
        ["face-framing layers", 3, [], ["hair"], [], []],
        ["long layers", 3, [], ["hair"], [], []],
        ["short layers", 3, [], ["hair"], [], []],
        ["cascade cut", 3, [], ["hair"], [], []],
        ["stacked haircut", 3, [], ["hair"], [], []],
        ["jellyfish haircut", 2, [], ["hair"], [], []],
        ["micro bangs", 3, [], ["hair"], [], []],
        ["hair tucked behind ear", 3, [], ["hair"], [], []],
        ["hair not covering ears", 3, [], ["hair"], [], []],
        ["hair covering ears", 3, [], ["hair"], [], []],
        ["hair over shoulders", 3, [], ["hair"], [], []],
        ["hair behind shoulders", 3, [], ["hair"], [], []],
        ["even hair length", 3, [], ["hair"], [], []],
        ["uneven hair length", 3, [], ["hair"], [], []],
        ["longer front", 3, [], ["hair"], [], []],
        ["longer back", 3, [], ["hair"], [], []],
        ["chin-level bob", 3, [], ["hair"], [], []],
        ["jagged-cut ends", 2, [], ["hair"], [], []],
    ],
    "eK": [ # Hair Style
        ["braid", 5, [], [], ["hair"], []], 
        ["ponytail", 5, [], [], ["hair"], []],
        ["twintails", 5, [], [], ["hair"], []],
        ["bun", 5, [], [], ["hair"], []],
        ["side ponytail", 5, [], [], ["hair"], []],
        ["high ponytail", 5, [], [], ["hair"], []],
        ["low ponytail", 5, [], [], ["hair"], []],
        ["twin braids", 5, [], [], ["hair"], []],
        ["single braid", 5, [], [], ["hair"], []],
        ["french braid", 4, [], [], ["hair"], []],
        ["crown braid", 4, [], [], ["hair"], []],
        ["braided ponytail", 4, [], [], ["hair"], []],
        ["half updo", 4, [], [], ["hair"], []],
        ["drill hair", 4, [], [], ["hair"], []],
        ["drill twintails", 4, [], [], ["hair"], []],
        ["side bun", 4, [], [], ["hair"], []],
        ["double bun", 4, [], [], ["hair"], []],
        ["cone hair bun", 3, [], [], ["hair"], []],
        ["folded ponytail", 3, [], [], ["hair"], []],
        ["hair buns", 4, [], [], ["hair"], []],
        ["low twintails", 4, [], [], ["hair"], []],
        ["twin drills", 4, [], [], ["hair"], []],
        ["one side up", 4, [], [], ["hair"], []],
        ["two side up", 4, [], [], ["hair"], []],
        ["sidecut", 3, [], [], ["hair"], []],
        ["complex braids", 3, [], [], ["hair"], []],
        ["fishtail braid", 3, [], [], ["hair"], []],
        ["box braids", 3, [], [], ["hair"], []],
        ["topknot", 3, [], [], ["hair"], []],
        ["chignon", 3, [], [], ["hair"], []],
        ["space buns", 3, [], [], ["hair"], []],
        ["odango", 4, [], [], ["hair"], []],
        ["half-up braid", 3, [], [], ["hair"], []],
        ["messy bun", 3, [], [], ["hair"], []],
        ["folded-fan ponytail", 3, [], [], ["hair"], []],
        ["braided crown", 3, [], [], ["hair"], []],
        ["multi-tied hair", 3, [], [], ["hair"], []],
        ["low tied long hair", 3, [], [], ["hair"], []],
        ["tri-tails", 3, [], [], ["hair"], []],
        ["quad tails", 2, [], [], ["hair"], []],
        ["braided hair rings", 3, [], [], ["hair"], []],
        ["dutch braid", 3, [], [], ["hair"], []],
        ["boxer braids", 3, [], [], ["hair"], []],
        ["milkmaid braids", 2, [], [], ["hair"], []],
        ["cornrows", 2, [], [], ["hair"], []],
        ["waterfall braid", 2, [], [], ["hair"], []],
        ["side swept", 3, [], [], ["hair"], []],
        ["half-up twin tails", 3, [], [], ["hair"], []],
        ["half-up bun", 3, [], [], ["hair"], []],
        ["braided bun", 3, [], [], ["hair"], []],
        ["hime-cut", 4, [], [], ["hair"], []],
        ["front braids", 3, [], [], ["hair"], []],
        ["bubble ponytail", 3, [], [], ["hair"], []],
        ["multi-section braid", 2, [], [], ["hair"], []],
        ["victory rolls", 2, [], [], ["hair"], []],
        ["pompadour", 2, [], [], ["hair"], []],
        ["french twist", 2, [], [], ["hair"], []],
        ["bouffant", 2, [], [], ["hair"], []],
        ["triple bun", 2, [], [], ["hair"], []],
        ["braided pigtails", 3, [], [], ["hair"], []],
        ["princess leia buns", 2, [], [], ["hair"], []],
        ["ringlet pigtails", 3, [], [], ["hair"], []],
        ["vertical drill hair", 3, [], [], ["hair"], []],
        ["horizontal drill hair", 3, [], [], ["hair"], []],
        ["hair intakes", 3, [], [], ["hair"], []],
        ["side-swept bangs with ponytail", 3, [], [], ["hair"], []],
        ["side-swept bangs with bun", 3, [], [], ["hair"], []],
        ["asymmetrical ponytail", 3, [], [], ["hair"], []],
        ["wrapped ponytail", 3, [], [], ["hair"], []],
        ["ribbon-tied ponytail", 3, [], [], ["hair"], []],
        ["scrunchie ponytail", 3, [], [], ["hair"], []],
        ["sleek ponytail", 3, [], [], ["hair"], []],
        ["tousled ponytail", 3, [], [], ["hair"], []],
        ["wrapped bun", 3, [], [], ["hair"], []],
        ["high bun", 3, [], [], ["hair"], []],
        ["low bun", 3, [], [], ["hair"], []],
        ["sock bun", 2, [], [], ["hair"], []],
        ["donut bun", 2, [], [], ["hair"], []],
        ["braided top knot", 2, [], [], ["hair"], []],
        ["half-crown braid", 3, [], [], ["hair"], []],
        ["lace braid", 2, [], [], ["hair"], []],
        ["rope braid", 2, [], [], ["hair"], []],
        ["herringbone braid", 2, [], [], ["hair"], []],
        ["dutch fishtail braid", 2, [], [], ["hair"], []],
        ["four strand braid", 2, [], [], ["hair"], []],
        ["five strand braid", 2, [], [], ["hair"], []],
        ["infinity braid", 2, [], [], ["hair"], []],
        ["pull-through braid", 2, [], [], ["hair"], []],
        ["stacked braids", 2, [], [], ["hair"], []],
        ["ladder braid", 2, [], [], ["hair"], []],
        ["snake braid", 2, [], [], ["hair"], []],
        ["zigzag braid", 2, [], [], ["hair"], []],
        ["twisted braid", 3, [], [], ["hair"], []],
        ["loop braid", 2, [], [], ["hair"], []],
        ["halo braid", 2, [], [], ["hair"], []],
        ["grecian braid", 2, [], [], ["hair"], []],
        ["goddess braids", 2, [], [], ["hair"], []],
        ["fulani braids", 2, [], [], ["hair"], []],
        ["twisted updo", 3, [], [], ["hair"], []],
        ["braided updo", 3, [], [], ["hair"], []],
        ["half-braided updo", 3, [], [], ["hair"], []],
        ["gibson tuck", 2, [], [], ["hair"], []],
        ["twisted bun", 3, [], [], ["hair"], []],
        ["braided crown updo", 2, [], [], ["hair"], []],
        ["twisted crown", 2, [], [], ["hair"], []],
        ["ribbon braid", 3, [], [], ["hair"], []],
        ["yarn braid", 2, [], [], ["hair"], []],
        ["chopstick bun", 2, [], [], ["hair"], []],
        ["stacked bun", 2, [], [], ["hair"], []],
        ["fan bun", 2, [], [], ["hair"], []],
        ["ballet bun", 2, [], [], ["hair"], []],
        ["nautilus bun", 2, [], [], ["hair"], []],
        ["butterfly bun", 2, [], [], ["hair"], []],
        ["heart bun", 2, [], [], ["hair"], []],
        ["pigtail buns", 3, [], [], ["hair"], []],
        ["triple mini buns", 2, [], [], ["hair"], []],
        ["quadruple mini buns", 2, [], [], ["hair"], []],
        ["half twist ponytail", 3, [], [], ["hair"], []],
        ["looped ponytail", 3, [], [], ["hair"], []],
        ["stacked ponytail", 3, [], [], ["hair"], []],
        ["knotted ponytail", 2, [], [], ["hair"], []],
        ["criss-cross ponytail", 2, [], [], ["hair"], []],
        ["bubble pigtails", 3, [], [], ["hair"], []],
        ["segmented ponytail", 3, [], [], ["hair"], []],
        ["heart-shaped bun", 2, [], [], ["hair"], []],
        ["star-shaped bun", 2, [], [], ["hair"], []],
        ["flower-shaped bun", 2, [], [], ["hair"], []],
        ["braided pigtail buns", 2, [], [], ["hair"], []],
        ["sculpted updo", 2, [], [], ["hair"], []],
        ["vintage updo", 2, [], [], ["hair"], []],
        ["retro updo", 2, [], [], ["hair"], []],
        ["asymmetrical updo", 2, [], [], ["hair"], []],
        ["avant-garde updo", 2, [], [], ["hair"], []],
        ["futuristic updo", 2, [], [], ["hair"], []],
        ["spiral updo", 2, [], [], ["hair"], []],
        ["structured updo", 2, [], [], ["hair"], []],
        ["cascading updo", 2, [], [], ["hair"], []],
        ["twisted side ponytail", 3, [], [], ["hair"], []],
        ["threaded ponytail", 2, [], [], ["hair"], []],
        ["woven ponytail", 2, [], [], ["hair"], []],
        ["peek-a-boo braids", 2, [], [], ["hair"], []],
        ["hidden braids", 2, [], [], ["hair"], []],
        ["lattice braids", 2, [], [], ["hair"], []],
        ["basketweave braids", 2, [], [], ["hair"], []],
        ["cascading braids", 3, [], [], ["hair"], []],
        ["waterfall twists", 2, [], [], ["hair"], []],
        ["mermaid braids", 2, [], [], ["hair"], []],
        ["unicorn braid", 2, [], [], ["hair"], []],
        ["dragon tail braid", 2, [], [], ["hair"], []],
        ["mohawk braid", 2, [], [], ["hair"], []],
        ["faux hawk braid", 2, [], [], ["hair"], []],
        ["undercut with braids", 2, [], [], ["hair"], []],
        ["sidecut with braids", 2, [], [], ["hair"], []],
        ["sectioned ponytail", 3, [], [], ["hair"], []],
        ["manga-style flared ponytail", 3, [], [], ["hair"], []],
        ["anime-style gravity-defying ponytail", 3, [], [], ["hair"], []],
        ["curled twintails", 3, [], [], ["hair"], []],
        ["braided twintails", 3, [], [], ["hair"], []],
        ["looped twintails", 3, [], [], ["hair"], []],
        ["twintails with ribbons", 3, [], [], ["hair"], []],
        ["twintails with bows", 3, [], [], ["hair"], []],
        ["segmented twintails", 3, [], [], ["hair"], []],
        ["curled drill ponytail", 3, [], [], ["hair"], []],
        ["single drill curl", 3, [], [], ["hair"], []],
        ["triple drill curls", 2, [], [], ["hair"], []],
        ["quadruple drill curls", 2, [], [], ["hair"], []],
        ["geometric updo", 2, [], [], ["hair"], []],
        ["asymmetrical twin tails", 3, [], [], ["hair"], []],
        ["braided mohawk", 2, [], [], ["hair"], []],
        ["nape knot", 3, [], [], ["hair"], []],
        ["octopus bun", 2, [], [], ["hair"], []],
        ["crown twist", 3, [], [], ["hair"], []],
        ["bow-shaped bun", 2, [], [], ["hair"], []],
        ["figure-8 bun", 2, [], [], ["hair"], []],
        ["criss-cross updo", 2, [], [], ["hair"], []],
        ["looped updo", 2, [], [], ["hair"], []],
        ["knotted updo", 2, [], [], ["hair"], []],
        ["curved ponytail", 3, [], [], ["hair"], []],
        ["s-curve ponytail", 3, [], [], ["hair"], []],
        ["zigzag ponytail", 3, [], [], ["hair"], []],
        ["architectural updo", 2, [], [], ["hair"], []],
        ["layered updo", 2, [], [], ["hair"], []],
        ["feathered updo", 2, [], [], ["hair"], []],
        ["wrapped crown braid", 2, [], [], ["hair"], []],
        ["hidden crown braid", 2, [], [], ["hair"], []],
        ["stacked crown braid", 2, [], [], ["hair"], []],
        ["voluminous updo", 2, [], [], ["hair"], []],
        ["beehive updo", 2, [], [], ["hair"], []],
        ["anime princess updo", 3, [], [], ["hair"], []],
        ["manga queen updo", 3, [], [], ["hair"], []],
        ["fantasy braided updo", 2, [], [], ["hair"], []],
        ["samurai-inspired updo", 2, [], [], ["hair"], []],
        ["ninja ponytail", 2, [], [], ["hair"], []],
        ["warrior braids", 2, [], [], ["hair"], []]
    ],
    "tp": [ # Hair Color
        ["black hair", 5, [], [], ["hair"], []], 
        ["blonde hair", 5, [], [], ["hair"], []],
        ["brown hair", 5, [], [], ["hair"], []],
        ["red hair", 5, [], [], ["hair"], []],
        ["pink hair", 5, [], [], ["hair"], []],
        ["blue hair", 5, [], [], ["hair"], []],
        ["purple hair", 5, [], [], ["hair"], []],
        ["white hair", 5, [], [], ["hair"], []],
        ["silver hair", 5, [], [], ["hair"], []],
        ["green hair", 5, [], [], ["hair"], []],
        ["grey hair", 5, [], [], ["hair"], []],
        ["orange hair", 5, [], [], ["hair"], []],
        ["aqua hair", 4, [], [], ["hair"], []],
        ["teal hair", 4, [], [], ["hair"], []],
        ["auburn hair", 4, [], [], ["hair"], []],
        ["strawberry blonde hair", 4, [], [], ["hair"], []],
        ["platinum blonde hair", 4, [], [], ["hair"], []],
        ["ash blonde hair", 4, [], [], ["hair"], []],
        ["honey blonde hair", 4, [], [], ["hair"], []],
        ["golden blonde hair", 4, [], [], ["hair"], []],
        ["dirty blonde hair", 4, [], [], ["hair"], []],
        ["light brown hair", 4, [], [], ["hair"], []],
        ["dark brown hair", 4, [], [], ["hair"], []],
        ["chestnut hair", 4, [], [], ["hair"], []],
        ["chocolate brown hair", 4, [], [], ["hair"], []],
        ["caramel hair", 4, [], [], ["hair"], []],
        ["copper hair", 4, [], [], ["hair"], []],
        ["ginger hair", 4, [], [], ["hair"], []],
        ["scarlet hair", 4, [], [], ["hair"], []],
        ["crimson hair", 4, [], [], ["hair"], []],
        ["burgundy hair", 4, [], [], ["hair"], []],
        ["maroon hair", 3, [], [], ["hair"], []],
        ["hot pink hair", 4, [], [], ["hair"], []],
        ["magenta hair", 4, [], [], ["hair"], []],
        ["rose pink hair", 4, [], [], ["hair"], []],
        ["pastel pink hair", 4, [], [], ["hair"], []],
        ["salmon pink hair", 3, [], [], ["hair"], []],
        ["coral hair", 3, [], [], ["hair"], []],
        ["peach hair", 3, [], [], ["hair"], []],
        ["navy blue hair", 4, [], [], ["hair"], []],
        ["royal blue hair", 4, [], [], ["hair"], []],
        ["sky blue hair", 4, [], [], ["hair"], []],
        ["baby blue hair", 4, [], [], ["hair"], []],
        ["sapphire hair", 3, [], [], ["hair"], []],
        ["cobalt blue hair", 3, [], [], ["hair"], []],
        ["indigo hair", 4, [], [], ["hair"], []],
        ["lavender hair", 4, [], [], ["hair"], []],
        ["violet hair", 4, [], [], ["hair"], []],
        ["plum hair", 3, [], [], ["hair"], []],
        ["lilac hair", 4, [], [], ["hair"], []],
        ["amethyst hair", 3, [], [], ["hair"], []],
        ["mauve hair", 3, [], [], ["hair"], []],
        ["periwinkle hair", 3, [], [], ["hair"], []],
        ["ivory hair", 3, [], [], ["hair"], []],
        ["cream hair", 3, [], [], ["hair"], []],
        ["snow white hair", 4, [], [], ["hair"], []],
        ["pearl white hair", 3, [], [], ["hair"], []],
        ["metallic silver hair", 3, [], [], ["hair"], []],
        ["chrome hair", 3, [], [], ["hair"], []],
        ["gunmetal hair", 3, [], [], ["hair"], []],
        ["mint green hair", 4, [], [], ["hair"], []],
        ["emerald green hair", 4, [], [], ["hair"], []],
        ["olive green hair", 3, [], [], ["hair"], []],
        ["lime green hair", 3, [], [], ["hair"], []],
        ["forest green hair", 3, [], [], ["hair"], []],
        ["sage green hair", 3, [], [], ["hair"], []],
        ["charcoal grey hair", 3, [], [], ["hair"], []],
        ["slate grey hair", 3, [], [], ["hair"], []],
        ["steel grey hair", 3, [], [], ["hair"], []],
        ["ash grey hair", 3, [], [], ["hair"], []],
        ["tangerine hair", 3, [], [], ["hair"], []],
        ["amber hair", 3, [], [], ["hair"], []],
        ["apricot hair", 3, [], [], ["hair"], []],
        ["rust hair", 3, [], [], ["hair"], []],
        ["vermilion hair", 3, [], [], ["hair"], []],
        ["cyan hair", 4, [], [], ["hair"], []],
        ["turquoise hair", 4, [], [], ["hair"], []],
        ["seafoam hair", 3, [], [], ["hair"], []],
        ["cerulean hair", 3, [], [], ["hair"], []],
        ["mahogany hair", 3, [], [], ["hair"], []],
        ["sandy blonde hair", 3, [], [], ["hair"], []],
        ["hazel hair", 3, [], [], ["hair"], []],
        ["raven black hair", 4, [], [], ["hair"], []],
        ["jet black hair", 4, [], [], ["hair"], []],
        ["ebony hair", 3, [], [], ["hair"], []],
        ["midnight black hair", 3, [], [], ["hair"], []],
        ["iridescent hair", 3, [], [], ["hair"], []],
        ["neon blue hair", 3, [], [], ["hair"], []],
        ["neon green hair", 3, [], [], ["hair"], []],
        ["neon pink hair", 3, [], [], ["hair"], []],
        ["neon purple hair", 3, [], [], ["hair"], []],
        ["neon orange hair", 3, [], [], ["hair"], []],
        ["pastel blue hair", 3, [], [], ["hair"], []],
        ["pastel green hair", 3, [], [], ["hair"], []],
        ["pastel purple hair", 3, [], [], ["hair"], []],
        ["pastel orange hair", 3, [], [], ["hair"], []],
        ["pastel yellow hair", 3, [], [], ["hair"], []],
        ["mustard yellow hair", 2, [], [], ["hair"], []],
        ["golden yellow hair", 3, [], [], ["hair"], []],
        ["lemon yellow hair", 3, [], [], ["hair"], []],
        ["wheat blonde hair", 3, [], [], ["hair"], []],
        ["flaxen hair", 3, [], [], ["hair"], []]
    ],
    "tu": [ # Multicolor Hair - low probability
        ["multicolored hair", 5, [], [], ["hair"], []], 
        ["gradient hair", 5, [], [], ["hair"], []],
        ["streaked hair", 5, [], [], ["hair"], []],
        ["two-tone hair", 5, [], [], ["hair"], []],
        ["highlighted hair", 4, [], [], ["hair"], []],
        ["ombre hair", 4, [], [], ["hair"], []],
        ["colored inner hair", 4, [], [], ["hair"], []],
        ["colored tips", 4, [], [], ["hair"], []],
        ["frosted tips", 3, [], [], ["hair"], []],
        ["dip dye", 3, [], [], ["hair"], []],
        ["rainbow hair", 3, [], [], ["hair"], []],
        ["tri-colored hair", 3, [], [], ["hair"], []],
        ["natural black to colored", 3, [], [], ["hair"], []],
        ["blue streaks", 3, [], [], ["hair"], []],
        ["pink streaks", 3, [], [], ["hair"], []],
        ["red streaks", 3, [], [], ["hair"], []]
    ],
    "e0": [ # Hair Properties
        ["messy hair", 5, [], [], ["hair"], []], 
        ["wavy hair", 5, [], [], ["hair"], []],
        ["curly hair", 5, [], [], ["hair"], []],
        ["straight hair", 5, [], [], ["hair"], []],
        ["spiky hair", 4, [], [], ["hair"], []],
        ["wet hair", 4, [], [], ["hair"], []],
        ["disheveled hair", 4, [], [], ["hair"], []],
        ["slicked back hair", 4, [], [], ["hair"], []],
        ["windswept hair", 4, [], [], ["hair"], []],
        ["wild hair", 3, [], [], ["hair"], []],
        ["shiny hair", 3, [], [], ["hair"], []],
        ["fluffy hair", 3, [], [], ["hair"], []],
        ["tousled hair", 3, [], [], ["hair"], []],
        ["crimped hair", 2, [], [], ["hair"], []],
        ["afro", 2, [], [], ["hair"], []],
        ["beehive hairstyle", 2, [], [], ["hair"], []],
        ["ringlets", 3, [], [], ["hair"], []],
        ["corkscrew curls", 3, [], [], ["hair"], []],
        ["waves", 3, [], [], ["hair"], []],
        ["bedhead", 3, [], [], ["hair"], []],
        ["permed hair", 2, [], [], ["hair"], []],
        ["straightened hair", 2, [], [], ["hair"], []],
        ["layered hair", 3, [], [], ["hair"], []],
        ["feathered hair", 3, [], [], ["hair"], []],
        ["voluminous hair", 3, [], [], ["hair"], []],
        ["frizzy hair", 2, [], [], ["hair"], []],
        ["textured hair", 3, [], [], ["hair"], []],
        ["silky hair", 3, [], [], ["hair"], []],
        ["glossy hair", 3, [], [], ["hair"], []],
        ["matte hair", 2, [], [], ["hair"], []],
        ["coiled hair", 2, [], [], ["hair"], []],
        ["kinky hair", 2, [], [], ["hair"], []],
        ["relaxed hair", 2, [], [], ["hair"], []],
        ["natural hair", 3, [], [], ["hair"], []],
        ["beach waves", 3, [], [], ["hair"], []],
        ["finger waves", 2, [], [], ["hair"], []],
        ["defined curls", 3, [], [], ["hair"], []],
        ["loose curls", 3, [], [], ["hair"], []],
        ["tight curls", 2, [], [], ["hair"], []],
        ["spiral curls", 2, [], [], ["hair"], []],
        ["s-waves", 2, [], [], ["hair"], []],
        ["teased hair", 2, [], [], ["hair"], []],
        ["brushed out curls", 2, [], [], ["hair"], []],
        ["piecey hair", 2, [], [], ["hair"], []],
        ["ruffled hair", 3, [], [], ["hair"], []],
        ["razored hair", 2, [], [], ["hair"], []],
        ["blunt cut", 3, [], [], ["hair"], []],
        ["choppy hair", 3, [], [], ["hair"], []],
        ["hair flowing over shoulders", 3, [], [], ["hair"], []],
        ["floating hair", 3, [], [], ["hair"], []],
        ["wind-blown hair", 3, [], [], ["hair"], []],
        ["hair spread out", 3, [], [], ["hair"], []],
        ["sculpted hair", 2, [], [], ["hair"], []],
        ["asymmetric hair texture", 2, [], [], ["hair"], []],
        ["big hair", 2, [], [], ["hair"], []],
        ["defined hair", 3, [], [], ["hair"], []],
        ["bouncy hair", 3, [], [], ["hair"], []],
        ["undone hair", 3, [], [], ["hair"], []],
        ["polished hair", 3, [], [], ["hair"], []],
        ["mussed hair", 3, [], [], ["hair"], []],
        ["tangle-free hair", 2, [], [], ["hair"], []],
        ["casual hair", 3, [], [], ["hair"], []],
        ["formal hair", 3, [], [], ["hair"], []],
        ["airy hair", 2, [], [], ["hair"], []],
        ["weightless hair", 2, [], [], ["hair"], []],
        ["volumized hair", 3, [], [], ["hair"], []],
        ["thin hair", 3, [], [], ["hair"], []],
        ["thick hair", 3, [], [], ["hair"], []],
        ["dense hair", 3, [], [], ["hair"], []],
        ["fine hair", 3, [], [], ["hair"], []],
        ["coarse hair", 2, [], [], ["hair"], []],
        ["soft hair", 3, [], [], ["hair"], []],
        ["stiff hair", 2, [], [], ["hair"], []],
        ["pin-straight hair", 3, [], [], ["hair"], []],
        ["sleek hair", 3, [], [], ["hair"], []],
        ["smooth hair", 3, [], [], ["hair"], []],
        ["rough hair", 2, [], [], ["hair"], []],
        ["damaged hair", 1, [], [], ["hair"], []],
        ["healthy hair", 3, [], [], ["hair"], []],
        ["virgin hair", 2, [], [], ["hair"], []],
        ["processed hair", 2, [], [], ["hair"], []],
        ["dyed hair", 3, [], [], ["hair"], []],
        ["highlighted hair", 3, [], [], ["hair"], []],
        ["lowlighted hair", 2, [], [], ["hair"], []],
        ["bleached hair", 2, [], [], ["hair"], []],
        ["balayage hair", 2, [], [], ["hair"], []],
        ["ombré hair", 3, [], [], ["hair"], []],
        ["sombré hair", 2, [], [], ["hair"], []],
        ["rooted hair", 2, [], [], ["hair"], []],
        ["dip-dyed hair", 3, [], [], ["hair"], []],
        ["money piece hair", 2, [], [], ["hair"], []],
        ["foiled hair", 2, [], [], ["hair"], []],
        ["dimensional hair", 2, [], [], ["hair"], []],
        ["glassy hair", 2, [], [], ["hair"], []],
        ["reflective hair", 2, [], [], ["hair"], []],
        ["matte-finish hair", 2, [], [], ["hair"], []],
        ["satin-finish hair", 2, [], [], ["hair"], []],
        ["semi-gloss hair", 2, [], [], ["hair"], []],
        ["high-gloss hair", 2, [], [], ["hair"], []],
        ["touchable hair", 2, [], [], ["hair"], []],
        ["movement in hair", 3, [], [], ["hair"], []],
        ["flowing hair", 3, [], [], ["hair"], []],
        ["static hair", 2, [], [], ["hair"], []],
        ["gravity-defying hair", 2, [], [], ["hair"], []],
        ["cloud-like hair", 2, [], [], ["hair"], []],
        ["cotton candy hair", 2, [], [], ["hair"], []],
        ["feathery hair", 3, [], [], ["hair"], []],
        ["wispy hair", 3, [], [], ["hair"], []],
        ["chunky hair", 2, [], [], ["hair"], []],
        ["piece-y hair", 2, [], [], ["hair"], []],
        ["defined pieces", 2, [], [], ["hair"], []],
        ["textured pieces", 2, [], [], ["hair"], []],
        ["face-framing hair", 3, [], [], ["hair"], []],
        ["hair tucked behind ear", 3, [], [], ["hair"], []],
        ["hair over face", 3, [], [], ["hair"], []],
        ["hair curtaining face", 3, [], [], ["hair"], []],
        ["beach hair", 3, [], [], ["hair"], []],
        ["tousled beach waves", 3, [], [], ["hair"], []],
        ["bed head", 3, [], [], ["hair"], []],
        ["just-woke-up hair", 3, [], [], ["hair"], []],
        ["just-showered hair", 3, [], [], ["hair"], []],
        ["damp hair", 3, [], [], ["hair"], []],
        ["soaking wet hair", 2, [], [], ["hair"], []],
        ["dripping hair", 2, [], [], ["hair"], []],
        ["slick hair", 3, [], [], ["hair"], []],
        ["oily hair", 1, [], [], ["hair"], []],
        ["greasy hair", 1, [], [], ["hair"], []],
        ["clean hair", 3, [], [], ["hair"], []],
        ["freshly-washed hair", 3, [], [], ["hair"], []],
        ["second-day hair", 2, [], [], ["hair"], []],
        ["third-day hair", 2, [], [], ["hair"], []],
        ["lived-in hair", 2, [], [], ["hair"], []],
        ["undone texture", 3, [], [], ["hair"], []],
        ["natural texture", 3, [], [], ["hair"], []],
        ["enhanced texture", 2, [], [], ["hair"], []],
        ["defined texture", 3, [], [], ["hair"], []],
        ["brushed-out texture", 2, [], [], ["hair"], []],
        ["air-dried hair", 2, [], [], ["hair"], []],
        ["diffused hair", 2, [], [], ["hair"], []],
        ["blow-dried hair", 2, [], [], ["hair"], []],
        ["heat-styled hair", 2, [], [], ["hair"], []],
        ["flat-ironed hair", 2, [], [], ["hair"], []],
        ["curled hair", 3, [], [], ["hair"], []],
        ["waved hair", 3, [], [], ["hair"], []],
        ["teased hair", 2, [], [], ["hair"], []],
        ["ratted hair", 1, [], [], ["hair"], []],
        ["backcombed hair", 2, [], [], ["hair"], []],
        ["voluminous roots", 2, [], [], ["hair"], []],
        ["flat roots", 2, [], [], ["hair"], []],
        ["root lift", 2, [], [], ["hair"], []],
        ["root volume", 2, [], [], ["hair"], []],
        ["bouncy ends", 2, [], [], ["hair"], []],
        ["flipped ends", 2, [], [], ["hair"], []],
        ["curled ends", 2, [], [], ["hair"], []],
        ["straight ends", 2, [], [], ["hair"], []],
        ["blunt ends", 2, [], [], ["hair"], []],
        ["textured ends", 2, [], [], ["hair"], []],
        ["feathered ends", 2, [], [], ["hair"], []],
        ["tapered ends", 2, [], [], ["hair"], []],
        ["point-cut ends", 2, [], [], ["hair"], []],
        ["razored ends", 2, [], [], ["hair"], []],
        ["split ends", 1, [], [], ["hair"], []],
        ["sealed ends", 2, [], [], ["hair"], []],
        ["frayed ends", 1, [], [], ["hair"], []],
    ],
    "e1": [ # Bangs/Sidelocks - less emphasis
        ["blunt bangs", 5, [], [], ["hair"], []], 
        ["sidelocks", 5, [], [], ["hair"], []],
        ["parted bangs", 5, [], [], ["hair"], []],
        ["swept bangs", 4, [], [], ["hair"], []],
        ["hair between eyes", 4, [], [], ["hair"], []],
        ["parted hair", 4, [], [], ["hair"], []],
        ["split bangs", 4, [], [], ["hair"], []],
        ["crossed bangs", 4, [], [], ["hair"], []],
        ["asymmetrical bangs", 3, [], [], ["hair"], []],
        ["diagonal bangs", 3, [], [], ["hair"], []],
        ["curtained hair", 3, [], [], ["hair"], []],
        ["hair over one eye", 4, [], [], ["hair"], []],
        ["hair over eyes", 3, [], [], ["hair"], []],
        ["hair over shoulder", 4, [], [], ["hair"], []],
        ["hair intakes", 3, [], [], ["hair"], []],
        ["hair pulled back", 4, [], [], ["hair"], []],
        ["side-swept bangs", 4, [], [], ["hair"], []],
        ["wispy bangs", 3, [], [], ["hair"], []],
        ["baby bangs", 3, [], [], ["hair"], []],
        ["micro bangs", 3, [], [], ["hair"], []],
        ["feathered bangs", 3, [], [], ["hair"], []],
        ["choppy bangs", 3, [], [], ["hair"], []],
        ["curved bangs", 3, [], [], ["hair"], []],
        ["arched bangs", 3, [], [], ["hair"], []],
        ["u-shaped bangs", 3, [], [], ["hair"], []],
        ["v-shaped bangs", 3, [], [], ["hair"], []],
        ["straight-across bangs", 4, [], [], ["hair"], []],
        ["see-through bangs", 3, [], [], ["hair"], []],
        ["asymmetric bangs", 3, [], [], ["hair"], []],
        ["middle-parted bangs", 4, [], [], ["hair"], []],
        ["bangs pinned back", 3, [], [], ["hair"], []],
        ["bangs pinned aside", 3, [], [], ["hair"], []],
        ["bangs tucked behind ear", 3, [], [], ["hair"], []],
        ["curtain bangs", 3, [], [], ["hair"], []],
        ["face-framing layers", 3, [], [], ["hair"], []],
        ["long sidelocks", 4, [], [], ["hair"], []],
        ["short sidelocks", 3, [], [], ["hair"], []],
        ["twin sidelocks", 3, [], [], ["hair"], []],
        ["ear-length sidelocks", 3, [], [], ["hair"], []],
        ["single sidelock", 3, [], [], ["hair"], []],
        ["hair flaps", 3, [], [], ["hair"], []],
        ["hair over both shoulders", 4, [], [], ["hair"], []],
        ["hair tucked behind ear", 4, [], [], ["hair"], []],
        ["hair behind ear", 4, [], [], ["hair"], []],
        ["center part", 4, [], [], ["hair"], []],
        ["side part", 4, [], [], ["hair"], []],
        ["zigzag part", 3, [], [], ["hair"], []],
        ["deep side part", 3, [], [], ["hair"], []],
        ["no bangs", 3, [], [], ["hair"], []],
        ["grown-out bangs", 3, [], [], ["hair"], []],
        ["fringe", 4, [], [], ["hair"], []],
        ["cropped bangs", 3, [], [], ["hair"], []],
        ["long bangs", 4, [], [], ["hair"], []],
        ["hair swept to side", 3, [], [], ["hair"], []],
        ["messy bangs", 3, [], [], ["hair"], []],
        ["jagged bangs", 3, [], [], ["hair"], []],
        ["rounded bangs", 3, [], [], ["hair"], []],
        ["hair covering ears", 3, [], [], ["hair"], []],
        ["hair tucked", 3, [], [], ["hair"], []],
        ["half-braided bangs", 2, [], [], ["hair"], []],
        ["braided sidelocks", 3, [], [], ["hair"], []],
        ["hair pulled to side", 3, [], [], ["hair"], []],
        ["face-framing pieces", 3, [], [], ["hair"], []],
        ["hair covering one eye", 3, [], [], ["hair"], []],
        ["hair covering forehead", 3, [], [], ["hair"], []],
        ["hime cut bangs", 3, [], [], ["hair"], []],
        ["wolf cut bangs", 2, [], [], ["hair"], []],
        ["shaggy bangs", 3, [], [], ["hair"], []],
        ["whispy sidelocks", 3, [], [], ["hair"], []],
        ["curled sidelocks", 3, [], [], ["hair"], []],
        ["drill sidelocks", 3, [], [], ["hair"], []],
        ["multiple sidelocks", 3, [], [], ["hair"], []],
        ["long bangs swept to side", 3, [], [], ["hair"], []],
        ["center-parted hair", 3, [], [], ["hair"], []],
        ["side-parted hair", 3, [], [], ["hair"], []],
        ["triple-parted bangs", 2, [], [], ["hair"], []],
        ["hair framing face", 4, [], [], ["hair"], []],
        ["hanging hair", 3, [], [], ["hair"], []],
        ["layered bangs", 3, [], [], ["hair"], []],
        ["hair tossed over shoulder", 3, [], [], ["hair"], []],
        ["hair cascading over shoulder", 3, [], [], ["hair"], []],
        ["tendrils of hair", 3, [], [], ["hair"], []],
        ["hair wisps", 3, [], [], ["hair"], []],
        ["hair swept up", 3, [], [], ["hair"], []],
        ["face-framing tendrils", 3, [], [], ["hair"], []],
        ["loose strands of hair", 3, [], [], ["hair"], []],
        ["piece-y bangs", 2, [], [], ["hair"], []],
        ["textured bangs", 3, [], [], ["hair"], []],
        ["eyebrow-length bangs", 3, [], [], ["hair"], []],
        ["eyelash-length bangs", 3, [], [], ["hair"], []],
        ["cheek-length sidelocks", 3, [], [], ["hair"], []],
        ["chin-length sidelocks", 3, [], [], ["hair"], []],
        ["chest-length sidelocks", 3, [], [], ["hair"], []],
        ["hair swept behind", 3, [], [], ["hair"], []],
        ["flyaway hair", 2, [], [], ["hair"], []],
        ["hair strand between eyes", 3, [], [], ["hair"], []]
    ],
    "e2": [ # Breast Size - important for female characters
        ["flat chest", 8, [], ["breasts"], ["female"], []],
        ["tiny breasts", 12, [], ["breasts"], ["female"], []],
        ["small breasts", 15, [], ["breasts"], ["female"], []],
        ["medium breasts", 10, [], ["breasts"], ["female"], []],
        ["large breasts", 8, [], ["breasts"], ["female"], []],
        ["huge breasts", 6, [], ["breasts"], ["female"], []],
        ["gigantic breasts", 3, [], ["breasts"], ["female"], []],
    ],
    "e5": [ # Body Features
        ["muscular female", 3, [], ["muscled_physique"], ["female"], []],
        ["muscular male", 5, [], ["muscled_physique"], ["male"], []],
        ["abs", 4, [], [], ["muscled_physique"], []],
        ["petite", 9, [], [], ["female"], []],
        ["slim body", 10, [], [], [], []],
        ["curvy body", 6, [], [], ["female"], []],
        ["athletic", 4, [], [], [], []],
        ["skinny", 10, [], [], [], []],
        ["slender", 5, [], [], [], []],
        ["ribs", 3, [], [], [], []],
        ["lean build", 8, [], [], [], []],
        ["willowy", 6, [], [], [], []],
        ["defined hip bones", 2, [], [], [], []],
        ["dancer's build", 3, [], [], [], []],
        ["swimmer's build", 3, [], [], [], []],
        ["runner's build", 3, [], [], [], []],
        ["elegant posture", 3, [], [], [], []],
        ["good posture", 3, [], [], [], []],
        ["subtle muscle tone", 3, [], [], [], []],
    ],
    "e6": [ # Headwear - RARELY, only if "naked with hat" is chosen
        ["baseball cap", 1, [], ["headwear"], [], []],
        ["witch hat", 1, [], ["headwear"], [], []],
        ["wide-brimmed hat", 1, [], ["headwear"], [], []],
        ["sun hat", 1, [], ["headwear"], [], []],
        ["hood", 4, [], ["headwear"], [], []],
    ],
    "e3": [ # Hair Accessory - RARELY
        ["hair ribbon", 5, [], ["hair_accessory"], ["female"], []], 
        ["hairband", 5, [], ["hair_accessory"], [], []],
        ["hair bow", 5, [], ["hair_accessory"], [], []],
        ["hair flower", 5, [], ["hair_accessory"], [], []],
        ["hair ornament", 5, [], ["hair_accessory"], [], []],
        ["hairpin", 5, [], ["hair_accessory"], [], []],
        ["hair clip", 5, [], ["hair_accessory"], [], []],
        ["hair tubes", 4, [], ["hair_accessory"], [], []],
        ["hair bobbles", 4, [], ["hair_accessory"], [], []],
        ["hair rings", 4, [], ["hair_accessory"], [], []],
        ["hair scrunchie", 4, [], ["hair_accessory"], [], []],
        ["hair stick", 4, [], ["hair_accessory"], [], []],
        ["hair intakes", 3, [], ["hair_accessory"], [], []],
        ["hair bell", 3, [], ["hair_accessory"], [], []],
        ["hair tie", 4, [], ["hair_accessory"], [], []],
        ["head wings", 3, [], ["hair_accessory"], [], []],
        ["x hair ornament", 3, [], ["hair_accessory"], [], []],
        ["star hair ornament", 3, [], ["hair_accessory"], [], []],
        ["heart hair ornament", 3, [], ["hair_accessory"], [], []],
        ["butterfly hair ornament", 3, [], ["hair_accessory"], [], []],
        ["leaf hair ornament", 3, [], ["hair_accessory"], [], []],
        ["flower hair ornament", 4, [], ["hair_accessory"], [], []],
        ["cherry blossom hair ornament", 3, [], ["hair_accessory"], [], []],
        ["rose hair ornament", 3, [], ["hair_accessory"], [], []],
        ["sunflower hair ornament", 3, [], ["hair_accessory"], [], []],
        ["daisy hair ornament", 3, [], ["hair_accessory"], [], []],
        ["hibiscus hair ornament", 3, [], ["hair_accessory"], [], []],
        ["lily hair ornament", 3, [], ["hair_accessory"], [], []],
        ["sakura hair ornament", 3, [], ["hair_accessory"], [], []],
        ["plum blossom hair ornament", 3, [], ["hair_accessory"], [], []],
        ["lotus hair ornament", 3, [], ["hair_accessory"], [], []],
        ["pearl hair ornament", 3, [], ["hair_accessory"], [], []],
        ["jeweled hair ornament", 3, [], ["hair_accessory"], [], []],
        ["crystal hair ornament", 3, [], ["hair_accessory"], [], []],
        ["diamond hair ornament", 3, [], ["hair_accessory"], [], []],
        ["ruby hair ornament", 3, [], ["hair_accessory"], [], []],
        ["sapphire hair ornament", 3, [], ["hair_accessory"], [], []],
        ["emerald hair ornament", 3, [], ["hair_accessory"], [], []],
        ["amethyst hair ornament", 3, [], ["hair_accessory"], [], []],
        ["topaz hair ornament", 3, [], ["hair_accessory"], [], []],
        ["jade hair ornament", 3, [], ["hair_accessory"], [], []],
        ["gold hair ornament", 3, [], ["hair_accessory"], [], []],
        ["silver hair ornament", 3, [], ["hair_accessory"], [], []],
        ["bronze hair ornament", 3, [], ["hair_accessory"], [], []],
        ["copper hair ornament", 3, [], ["hair_accessory"], [], []],
        ["moon hair ornament", 3, [], ["hair_accessory"], [], []],
        ["sun hair ornament", 3, [], ["hair_accessory"], [], []],
        ["snowflake hair ornament", 3, [], ["hair_accessory"], [], []],
        ["lightning bolt hair ornament", 3, [], ["hair_accessory"], [], []],
        ["skull hair ornament", 3, [], ["hair_accessory"], [], []],
        ["cross hair ornament", 3, [], ["hair_accessory"], [], []],
        ["crown hair ornament", 3, [], ["hair_accessory"], [], []],
        ["tiara hair ornament", 3, [], ["hair_accessory"], [], []],
        ["feather hair ornament", 3, [], ["hair_accessory"], [], []],
        ["bird hair ornament", 3, [], ["hair_accessory"], [], []],
        ["dragon hair ornament", 3, [], ["hair_accessory"], [], []],
        ["butterfly clip", 3, [], ["hair_accessory"], [], []],
        ["dragonfly hair ornament", 3, [], ["hair_accessory"], [], []],
        ["ladybug hair ornament", 3, [], ["hair_accessory"], [], []],
        ["bee hair ornament", 3, [], ["hair_accessory"], [], []],
        ["lace headband", 3, [], ["hair_accessory"], [], []],
        ["beaded headband", 3, [], ["hair_accessory"], [], []],
        ["metal headband", 3, [], ["hair_accessory"], [], []],
        ["plastic headband", 3, [], ["hair_accessory"], [], []],
        ["fabric headband", 3, [], ["hair_accessory"], [], []],
        ["braided headband", 3, [], ["hair_accessory"], [], []],
        ["velvet headband", 3, [], ["hair_accessory"], [], []],
        ["sport headband", 3, [], ["hair_accessory"], [], []],
        ["zigzag headband", 3, [], ["hair_accessory"], [], []],
        ["wide headband", 3, [], ["hair_accessory"], [], []],
        ["thin headband", 3, [], ["hair_accessory"], [], []],
        ["polka dot hair accessory", 3, [], ["hair_accessory"], [], []],
        ["striped hair accessory", 3, [], ["hair_accessory"], [], []],
        ["checkered hair accessory", 3, [], ["hair_accessory"], [], []],
        ["plaid hair accessory", 3, [], ["hair_accessory"], [], []],
        ["animal print hair accessory", 3, [], ["hair_accessory"], [], []],
        ["leopard print hair accessory", 3, [], ["hair_accessory"], [], []],
        ["zebra print hair accessory", 3, [], ["hair_accessory"], [], []],
        ["heart-shaped clip", 3, [], ["hair_accessory"], [], []],
        ["star-shaped clip", 3, [], ["hair_accessory"], [], []],
        ["cloud-shaped clip", 3, [], ["hair_accessory"], [], []]
    ],
    "e4": [ # Hat Accessory - RARELY
        ["hat bow", 5, [], [], ["headwear"], []], 
        ["hat flower", 5, [], [], ["headwear"], []],
        ["hat ribbon", 5, [], [], ["headwear"], []],
        ["hat feather", 4, [], [], ["headwear"], []],
        ["hat ornament", 4, [], [], ["headwear"], []],
        ["hat pin", 3, [], [], ["headwear"], []],
        ["hat brooch", 3, [], [], ["headwear"], []],
        ["hat decoration", 4, [], [], ["headwear"], []],
        ["hat gem", 3, [], [], ["headwear"], []],
        ["hat charm", 3, [], [], ["headwear"], []],
        ["hat band", 4, [], [], ["headwear"], []],
        ["hat emblem", 3, [], [], ["headwear"], []],
        ["hat logo", 3, [], [], ["headwear"], []],
        ["hat cockade", 2, [], [], ["headwear"], []],
        ["hat tassel", 3, [], [], ["headwear"], []],
        ["hat buckle", 3, [], [], ["headwear"], []],
        ["hat veil", 3, [], [], ["headwear"], []],
        ["hat patch", 3, [], [], ["headwear"], []],
        ["hat buttons", 3, [], [], ["headwear"], []],
        ["hat strings", 3, [], [], ["headwear"], []],
        ["hat pompom", 3, [], [], ["headwear"], []],
        ["hat bell", 3, [], [], ["headwear"], []],
        ["hat chain", 3, [], [], ["headwear"], []],
        ["hat medal", 3, [], [], ["headwear"], []],
        ["hat badge", 3, [], [], ["headwear"], []],
        ["hat insignia", 3, [], [], ["headwear"], []],
        ["hat rank", 3, [], [], ["headwear"], []],
        ["hat beads", 3, [], [], ["headwear"], []],
        ["hat sequins", 3, [], [], ["headwear"], []],
        ["hat crystals", 3, [], [], ["headwear"], []],
        ["hat diamonds", 3, [], [], ["headwear"], []],
        ["hat pearls", 3, [], [], ["headwear"], []],
        ["hat jewels", 3, [], [], ["headwear"], []],
        ["hat lace", 3, [], [], ["headwear"], []],
        ["hat trim", 3, [], [], ["headwear"], []],
        ["hat cord", 3, [], [], ["headwear"], []],
        ["hat braid", 3, [], [], ["headwear"], []],
        ["hat piping", 3, [], [], ["headwear"], []],
        ["hat fringe", 3, [], [], ["headwear"], []],
        ["hat frills", 3, [], [], ["headwear"], []],
    ],
    # Clothing categories - used very specifically for "naked with <item>"
    "e7": [["cocktail dress", 1, [], [], ["female"], []]],
    "e8": [["thighhighs", 1, [], ["legwear"], ["female","legs"], []]],
    "e9": [["fishnet legwear", 1, [], [], ["legwear"], []]],
    "te": [["t-shirt", 1, [], [], [], []], ["open shirt", 1, [], [], [],[]]],
    "tt": [["miniskirt", 1, [], [], ["female"], []]],
    "ta": [["boots", 1, [], ["footwear"], ["feet"], []]],
    "ti": [["school uniform", 1, [], [], [], []]],
    "ts": [["bodysuit", 1, [], [], [], []]],
    "underwear": [["lingerie set", 1, [], [], ["female"], []], ["panties", 1, [], [], ["female"],[]], ["bra", 1, [], [], ["female"],[]]],
    "tr": [["bikini", 1, [], [], ["female"], []], ["swimsuit", 1, [], [], ["female"],[]]],

    "eX": [ # Eye Details
        ["heterochromia", 2, [], [], ["eyes"], []],
        ["glowing eyes", 1, [], [], ["eyes"], []], 
        ["pupil-less", 1, [], [], ["eyes"], []],
        ["slit pupils", 1, [], [], ["eyes"], []],
        ["heart-shaped pupils", 3, [], [], ["eyes"], []], # Lust
        ["spiral pupils", 2, [], [], ["eyes"], []], # Dazed/hypno
        ["dilated pupils", 4, [], [], ["eyes"],[]],
        ["closed eyes", 3, [], [], ["eyes"], []], # Mid-orgasm, pain
        ["half-closed eyes", 5, [], [], ["eyes"], []], # Pleasure, pain
        ["narrowed eyes", 4, [], [], ["eyes"], []], # Anger, suspicion
        ["wide eyes", 3, [], [], ["eyes"], []], # Surprise, fear
        ["rolled back eyes", 6, [], [], ["eyes"], []], # Orgasm
    ],
    "tn": [ # Accessories - mostly disabled or for specific "naked with X"
        ["necklace", 1, [], [], [], []],
        ["glasses", 1, [], [], [], []],
        ["choker", 2, [], [], [], []], 
        ["gag", 1, [], [], [], []], 
        ["blindfold", 1, [], [], [], []], 
        ["rope", 1, [], [], [], []], 
    ],
    "to": [ # NSFW Expressions 
        ["ecstasy", 10, [], [], [], []], 
        ["pleasure", 10, [], [], [], []], 
        ["intense pleasure", 9, [], [], [], []],
        ["orgasm", 12, [], [], [], []], 
        ["pre-orgasm", 7, [], [], [], []], 
        ["post-orgasm", 6, [], [], [], []],
        ["pain", 9, [], [], [], []], 
        ["sexual pain", 8, [], [], [], []],
        ["upset", 7, [], [], [], []], 
        ["crying during sex", 6, [], [], [], []], 
        ["tears of pain", 5, [], [], [], []], 
        ["tears of pleasure", 5, [], [], [], []],
        ["angry sex face", 8, [], [], [], []], 
        ["furious", 6, [], [], [], []], 
        ["frustrated", 5, [], [], [], []],
        ["ahegao", 7, [], [], [], []], 
        ["lustful", 9, [], [], [], []], 
        ["yearning", 6, [], [], [], []],
        ["suffering (sexual)", 5, [], [], [], []], 
        ["forced smile", 2, [], [], [], []],
        ["screaming (pleasure)", 6, [], [], [], []], 
        ["screaming (pain)", 5, [], [], [], []], 
        ["moaning", 10, [], [], [], []],
        ["blush", 8, [], [], [], []], 
        ["heavy blush", 6, [], [], [], []], 
        ["sweating", 7, [], [], [], []],
        ["eyes rolled back", 8, [], [], ["eyes"], []], 
        ["trembling", 6, [], [], [], []],
        ["open mouth", 9, [], [], [], []], 
        ["parted lips", 8, [], [], [], []], 
        ["tongue out", 4, [], [], [], []], 
        ["biting lip", 5, [], [], [], []],
        ["embarrassed", 3, [], [], [], []], 
        ["shy", 2, [], [], [], []], 
        ["scared", 6, [], [], [], []], 
        ["terrified", 5, [], [], [], []], 
        ["anxious", 4, [], [], [], []],
        ["smirk", 3, [], [], [], []], 
        ["smug", 2, [], [], [], []], 
        ["determined", 3, [], [], [], []], 
        ["expressionless (during sex)", 2, [], [], [], []], 
        ["panting", 7, [], [], [], []],
        ["drooling", 3, [], [], [], []],
    ],
        "tl": [ # Time/Season - Expanded
        # Times of Day
        ["night", 12, [], [], [], []],
        ["midnight", 4, [], [], [], []],
        ["witching hour", 1, [], [], [], []], # Atmospheric, rare
        ["late night", 5, [], [], [], []],
        ["evening", 7, [], [], [], []],
        ["dusk", 4, [], [], [], []],
        ["twilight", 4, [], [], [], []], # Can overlap dusk/dawn, distinct tag
        ["day", 10, [], [], [], []],     # Generic daytime
        ["afternoon", 6, [], [], [], []],
        ["midday", 3, [], [], [], []],
        ["morning", 6, [], [], [], []],
        ["early morning", 4, [], [], [], []],
        ["dawn", 4, [], [], [], []],
        ["sunrise", 3, [], [], [], []], # Event
        ["sunset", 5, [], [], [], []],  # Event
        ["golden hour", 3, [], [], [], []], # Specific lighting condition
        ["blue hour", 2, [], [], [], []],   # Specific lighting condition

        # Seasons
        ["spring", 3, [], [], [], []],
        ["summer", 5, [], [], [], []],
        ["autumn", 3, [], [], [], []], # or "fall"
        ["winter", 4, [], [], [], []],

        # Weather Conditions
        ["clear sky", 6, [], [], [], []],
        ["sunny day", 7, ["day"], [], [], []],
        ["partly cloudy", 4, [], [], [], []],
        ["cloudy day", 5, ["day"], [], [], []],
        ["overcast sky", 4, [], [], [], []],
        ["rainy day", 4, [], [], [], []],
        ["raining", 5, [], [], [], []], # The action
        ["light rain", 3, [], [], [], []],
        ["heavy rain", 3, [], [], [], []],
        ["downpour", 2, [], [], [], []],
        ["stormy weather", 3, [], [], [], []],
        ["thunderstorm", 2, [], [], [], []], # Includes thunder, lightning
        ["lightning", 1, ["stormy weather", "night"], [], [], []],
        ["snowy day", 3, ["winter"], [], [], []],
        ["snowing", 4, ["winter"], [], [], []], # The action
        ["light snow", 2, ["winter"], [], [], []],
        ["heavy snow", 1, ["winter"], [], [], []],
        ["blizzard", 1, ["winter"], [], [], []],
        ["foggy", 3, [], [], [], []],
        ["misty", 2, [], [], [], []],
        ["windy", 3, [], [], [], []],
        ["strong winds", 1, [], [], [], []],
        ["hot day", 4, ["summer", "day"], [], [], []],
        ["humid weather", 2, [], [], [], []],
        ["cold day", 3, ["winter", "autumn"], [], [], []],
        ["freezing weather", 1, ["winter"], [], [], []],
        ["hail", 0.5, [], [], [], []],
    ],
    "td": [ # Scenery details - Expanded (details within an environment)
        # Original (rephrased as background elements)
        ["forest background", 3, ["outdoors"], [], [], []],
        ["beach background", 3, ["outdoors"], [], [], []],

        # Natural Environment Details
        ["trees", 5, ["outdoors"], [], [], []],
        ["dense foliage", 3, ["forest background", "jungle"], [], [], []],
        ["undergrowth", 2, ["forest background", "woods"], [], [], []],
        ["bushes", 4, ["outdoors", "garden"], [], [], []],
        ["flowers", 4, ["outdoors", "garden"], [], [], []],
        ["wildflowers", 3, ["outdoors", "meadow", "field"], [], [], []],
        ["rose bushes", 2, ["garden"], [], [], []],
        ["rocks", 4, ["outdoors"], [], [], []],
        ["boulders", 2, ["outdoors", "mountainside"], [], [], []],
        ["cliffs", 2, ["outdoors", "mountainside", "coastline"], [], [], []],
        ["sand dunes", 2, ["beach background", "desert"], [], [], []],
        ["ocean waves", 3, ["beach background"], [], [], []],
        ["calm water", 3, ["lake", "pond", "calm sea"], [], [], []],
        ["ripples on water", 2, [], [], [], []],
        ["river view", 3, ["outdoors"], [], [], []],
        ["lake view", 3, ["outdoors"], [], [], []],
        ["pond", 2, ["outdoors"], [], [], []],
        ["stream", 2, ["outdoors", "forest background"], [], [], []],
        ["waterfall in background", 2, ["outdoors"], [], [], []],
        ["mountain range in background", 3, ["outdoors"], [], [], []],
        ["rolling hills", 3, ["outdoors"], [], [], []],
        ["grassy field", 4, ["outdoors"], [], [], []],
        ["path", 3, ["outdoors"], [], [], []],
        ["dirt road", 2, ["outdoors"], [], [], []],
        ["vines", 2, ["outdoors", "jungle", "ruins"], [], [], []],
        ["ivy covered wall", 2, [], [], [], []],
        ["fallen leaves", 2, ["autumn", "forest background"], [], [], []],
        ["mossy rocks", 2, ["forest background", "ruins"], [], [], []],
        ["cave mouth", 1, ["outdoors"], [], [], []],
        ["stalactites", 1, ["cave"], [], [], []],
        ["stalagmites", 1, ["cave"], [], [], []],
        ["glowing mushrooms", 0.5, ["cave", "forest background", "night"], [], [], []], # Fantasy/magical

        # Atmospheric/Sky Details
        ["starry sky", 4, ["night"], [], [], []],
        ["full moon", 3, ["night"], [], [], []],
        ["crescent moon", 2, ["night"], [], [], []],
        ["no moon", 1, ["night"], [], [], []],
        ["milky way visible", 1, ["night", "clear sky"], [], [], []],
        ["clouds", 4, [], [], [], []],
        ["puffy clouds", 3, ["day"], [], [], []],
        ["storm clouds", 2, ["stormy weather"], [], [], []],
        ["sun visible", 4, ["day"], [], [], []],
        ["bright sunlight", 5, ["day", "sunny day"], [], [], []],
        ["dappled sunlight", 3, ["day", "forest background"], [], [], []],
        ["moonlight", 5, ["night"], [], [], []],
        ["shaft of moonlight", 3, ["night", "indoors", "window"], [], [], []],
        ["sun rays", 3, [], [], [], []],
        ["god rays", 2, [], [], [], []], # (crepuscular rays)
        ["rain streaks", 2, ["raining"], [], [], []],
        ["snowflakes falling", 2, ["snowing"], [], [], []],
        ["fog bank", 2, ["foggy"], [], [], []],
        ["ground mist", 3, ["morning", "night", "swamp"], [], [], []],
        ["aurora borealis", 0.5, ["night", "winter", "clear sky"], [], [], []], # Rare
        ["rainbow", 0.5, ["day", "rainy day"], [], [], []], # Rare

        # Urban/Man-Made Environment Details
        ["cityscape background", 4, ["urban"], [], [], []],
        ["distant city lights", 3, ["night", "urban"], [], [], []],
        ["streetlights", 4, ["night", "urban"], [], [], []],
        ["flickering streetlight", 1, ["night", "urban", "dark alleyway"], [], [], []],
        ["neon signs", 3, ["night", "urban"], [], [], []],
        ["buildings", 4, ["urban"], [], [], []],
        ["skyscrapers", 3, ["urban", "cityscape background"], [], [], []],
        ["windows (exterior)", 3, ["urban", "building"], [], [], []],
        ["lit windows (seen from outside)", 2, ["night", "urban"], [], [], []],
        ["darkened windows", 2, ["night", "urban", "abandoned building"], [], [], []],
        ["graffiti on wall", 3, ["urban", "alleyway"], [], [], []],
        ["brick wall texture", 3, [], [], [], []],
        ["concrete wall texture", 3, [], [], [], []],
        ["cobblestone street", 2, ["urban"], [], [], []],
        ["asphalt road", 2, ["urban"], [], [], []],
        ["wet pavement", 4, ["raining", "urban"], [], [], []],
        ["puddles", 3, ["raining", "urban"], [], [], []],
        ["reflection in puddle", 2, ["puddles", "night"], [], [], []],
        ["manhole cover", 1, ["urban"], [], [], []],
        ["steam from manhole", 0.5, ["urban", "night"], [], [], []],
        ["trash cans", 2, ["urban", "alleyway"], [], [], []],
        ["overflowing trash can", 1, ["urban", "alleyway", "slum alley"], [], [], []],
        ["dumpster", 2, ["urban", "alleyway"], [], [], []],
        ["parked cars (background)", 3, ["urban"], [], [], []],
        ["fence", 3, [], [], [], []],
        ["chain-link fence", 2, ["urban", "industrial"], [], [], []],
        ["broken fence", 1, ["abandoned building", "rural"], [], [], []],
        ["wooden fence", 2, ["garden", "rural"], [], [], []],
        ["power lines", 1, ["urban", "rural"], [], [], []],
        ["fire escape", 2, ["urban", "building"], [], [], []],
        ["billboards", 1, ["urban"], [], [], []],
        ["ruined wall", 2, ["ruins", "abandoned building"], [], [], []],
        ["broken glass on ground", 2, ["abandoned building", "alleyway", "crime scene"], [], [], []],
        ["debris on ground", 2, ["abandoned building", "construction site", "ruins"], [], [], []],
        ["barbed wire", 1, ["prison cell", "abandoned factory", "military"], [], [], []],

        # Indoor Details (complementary to eZ location)
        ["window (view from inside)", 5, ["indoors"], [], [], []],
        ["curtains", 4, ["indoors", "window"], [], [], []],
        ["sheer curtains", 2, ["indoors", "window"], [], [], []],
        ["blinds (venetian/roller)", 3, ["indoors", "window"], [], [], []],
        ["door (interior)", 4, ["indoors"], [], [], []],
        ["open doorway", 3, ["indoors"], [], [], []],
        ["closed door", 3, ["indoors"], [], [], []],
        ["door ajar", 2, ["indoors"], [], [], []],
        ["fireplace (lit/unlit)", 3, ["indoors"], [], [], []],
        ["burning fireplace", 2, ["indoors", "fireplace"], [], [], []],
        ["rug", 4, ["indoors"], [], [], []],
        ["ornate rug", 2, ["indoors", "luxury hotel suite", "mansion"], [], [], []],
        ["shag rug", 1, ["indoors"], [], [], []],
        ["carpeted floor", 4, ["indoors"], [], [], []],
        ["hardwood floor", 3, ["indoors"], [], [], []],
        ["tiled floor", 3, ["indoors", "bathroom", "kitchen"], [], [], []],
        ["bookshelf", 3, ["indoors", "study", "library"], [], [], []],
        ["scattered books", 2, ["indoors", "study", "library"], [], [], []],
        ["desk lamp", 3, ["indoors", "desk", "office"], [], [], []],
        ["floor lamp", 2, ["indoors"], [], [], []],
        ["chandelier", 1, ["indoors", "mansion", "luxury hotel suite"], [], [], []],
        ["candles (decorative)", 3, ["indoors"], [], [], []],
        ["lit candles (atmosphere)", 3, ["indoors"], [], [], []],
        ["mirror (wall-mounted)", 4, ["indoors", "bathroom", "bedroom"], [], [], []],
        ["artwork on wall", 3, ["indoors"], [], [], []],
        ["framed photos", 2, ["indoors"], [], [], []],
        ["potted plants (indoor)", 3, ["indoors"], [], [], []],
        ["wallpaper", 3, ["indoors"], [], [], []],
        ["peeling wallpaper", 1, ["indoors", "abandoned house", "dingy apartment"], [], [], []],
        ["exposed pipes", 1, ["indoors", "basement", "abandoned factory"], [], [], []],
        ["steam (from shower/bath)", 3, ["bathroom", "shower", "bathtub"], [], [], []],
        ["water droplets on surfaces", 3, ["bathroom", "shower", "raining"], [], [], []],
        ["condensation on window", 2, ["indoors", "cold day", "rainy day"], [], [], []],
    ],
    "tc": [ # Objects - Greatly Expanded
        # Common Furniture/Room Objects (some overlap with eZ if the object IS the scene focus)
        ["bed", 12, [], [], [], []], # Primary object
        ["pillows", 10, ["bed", "couch"], [], [], []],
        ["bolster pillow", 2, ["bed"], [], [], []],
        ["blanket", 7, ["bed", "couch"], [], [], []],
        ["duvet", 6, ["bed"], [], [], []],
        ["comforter", 6, ["bed"], [], [], []],
        ["sheets", 10, ["bed"], [], [], []], # e.g., "tangled sheets", "silk sheets"
        ["satin sheets", 2, ["bed"], [], [], []],
        ["messy bed", 5, ["bed"], [], [], []],
        ["unmade bed", 4, ["bed"], [], [], []],
        ["couch", 8, [], [], [], []],
        ["sofa", 7, [], [], [], []],
        ["loveseat", 3, [], [], [], []],
        ["armchair", 4, [], [], [], []],
        ["recliner", 2, [], [], [], []],
        ["chair", 5, [], [], [], []], # Generic
        ["wooden chair", 3, [], [], [], []],
        ["folding chair", 1, [], [], [], []], # Can imply makeshift/non-con
        ["stool", 2, [], [], [], []],
        ["ottoman", 2, ["couch", "armchair"], [], [], []],
        ["table", 5, [], [], [], []], # Generic
        ["coffee table", 4, ["couch", "living room"], [], [], []],
        ["dining table", 3, ["dining room", "kitchen"], [], [], []],
        ["bedside table", 4, ["bed", "bedroom"], [], [], []],
        ["nightstand", 4, ["bed", "bedroom"], [], [], []],
        ["desk", 3, ["study", "office", "bedroom"], [], [], []],
        ["dressing table (vanity)", 2, ["bedroom"], [], [], []],
        ["lamp", 4, [], [], [], []], # Generic
        ["bedside lamp", 3, ["nightstand", "bedside table"], [], [], []],
        ["mirror (handheld)", 3, [], [], [], []],
        ["mirror (full-length)", 3, ["bedroom", "dressing room"], [], [], []],
        ["towel", 5, ["bathroom", "beach", "pool"], [], [], []],
        ["bathrobe", 3, ["bathroom", "bedroom"], [], [], []],
        ["bathtub (filled with water)", 3, ["bathroom"], [], [], []],
        ["shower head (running water)", 2, ["bathroom", "shower"], [], [], []],
        ["sink", 2, ["bathroom", "kitchen"], [], [], []],
        ["rug", 4, [], [], [], []],
        ["throw rug", 3, [], [], [], []],

        # Sex Toys
        ["vibrator", 3, [], ["toy"], [], []], # Generic
        ["wand vibrator", 2.5, [], ["toy"], [], []], # e.g. Hitachi
        ["bullet vibrator", 1.5, [], ["toy"], [], []],
        ["rabbit vibrator", 1.5, [], ["toy", "female"], ["female"], []],
        ["g-spot vibrator", 1, [], ["toy", "female"], ["female"], []],
        ["clitoral vibrator", 1, [], ["toy", "female"], ["female"], []],
        ["dildo", 3.5, [], ["toy"], [], []], # Generic
        ["double-ended dildo", 1, [], ["toy"], [], []],
        ["realistic dildo", 2, [], ["toy"], [], []],
        ["veiny dildo", 1.5, [], ["toy"], [], []],
        ["glass dildo", 0.5, [], ["toy"], [], []],
        ["silicone dildo", 1.5, [], ["toy"], [], []],
        ["metal dildo", 0.3, [], ["toy"], [], []],
        ["inflatable dildo", 0.2, [], ["toy"], [], []],
        ["suction cup dildo", 1, [], ["toy"], [], []],
        ["strapon dildo", 2, [], ["toy"], [], []],
        ["harness", 1.5, ["strapon dildo"], ["toy"], [], []],
        ["anal beads", 1.5, [], ["toy", "anal_play"], [], []],
        ["butt plug", 2.5, [], ["toy", "anal_play"], [], []],
        ["jeweled butt plug", 1, [], ["toy", "anal_play"], [], []],
        ["vibrating butt plug", 1, [], ["toy", "anal_play"], [], []],
        ["cock ring", 1.5, [], ["toy", "male"], ["male"], []],
        ["vibrating cock ring", 1, [], ["toy", "male"], ["male"], []],
        ["ball stretcher", 0.5, [], ["toy", "male", "bdsm_item"], ["male"], []],
        ["nipple clamps", 1.5, [], ["toy", "bdsm_item"], [], []],
        ["nipple suckers", 0.5, [], ["toy", "bdsm_item"], [], []],
        ["ben wa balls", 0.5, [], ["toy", "female"], ["female"], []],
        ["kegel balls", 0.3, [], ["toy", "female"], ["female"], []],
        ["Fleshlight", 1, [], ["toy", "male"], ["male"], []], # Or similar male masturbator
        ["masturbation sleeve", 1, [], ["toy", "male"], ["male"], []],
        ["prostate massager", 0.7, [], ["toy", "male", "anal_play"], ["male"], []],
        ["sex doll", 0.3, [], ["toy"], [], []], # Can be specific (male/female doll)
        ["love doll", 0.3, [], ["toy"], [], []],
        ["egg vibrator", 1, [], ["toy"], [], []],
        ["remote controlled vibrator", 1, [], ["toy"], [], []],

        # BDSM Gear / Restraints
        ["rope", 4, [], ["bdsm_item", "restraint_item"], [], []], # For bondage or decoration
        ["shibari rope", 1, [], ["bdsm_item", "restraint_item"], [], []],
        ["chains", 2.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["rusty chains", 1, ["dungeon", "abandoned building"], ["bdsm_item", "restraint_item"], [], []],
        ["handcuffs", 3, [], ["bdsm_item", "restraint_item"], [], []],
        ["metal handcuffs", 2.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["fuzzy handcuffs", 1, [], ["bdsm_item", "restraint_item"], [], []],
        ["leather cuffs", 1.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["leg cuffs", 1.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["ankle cuffs", 1.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["thigh cuffs", 1, [], ["bdsm_item", "restraint_item"], [], []],
        ["shackles", 2, [], ["bdsm_item", "restraint_item"], [], []],
        ["manacles", 1.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["collar (BDSM)", 2.5, [], ["bdsm_item", "accessory"], [], []],
        ["studded collar", 1, [], ["bdsm_item", "accessory"], [], []],
        ["leash", 1.5, ["collar"], ["bdsm_item"], [], []],
        ["ball gag", 2, [], ["bdsm_item", "gag_item"], [], []],
        ["ring gag", 1, [], ["bdsm_item", "gag_item"], [], []],
        ["tape gag", 1.5, [], ["bdsm_item", "gag_item"], [], []], # Duct tape, medical tape
        ["cloth gag", 1, [], ["bdsm_item", "gag_item"], [], []],
        ["blindfold", 2.5, [], ["bdsm_item", "sensory_item"], [], []],
        ["silk blindfold", 1, [], ["bdsm_item", "sensory_item"], [], []],
        ["whip", 1.5, [], ["bdsm_item", "impact_item"], [], []],
        ["bullwhip", 0.5, [], ["bdsm_item", "impact_item"], [], []],
        ["flogger", 1.5, [], ["bdsm_item", "impact_item"], [], []],
        ["riding crop", 1.5, [], ["bdsm_item", "impact_item"], [], []],
        ["paddle", 1.5, [], ["bdsm_item", "impact_item"], [], []],
        ["cane (impact play)", 1, [], ["bdsm_item", "impact_item"], [], []],
        ["bondage tape", 1, [], ["bdsm_item", "restraint_item"], [], []],
        ["spreader bar", 1, [], ["bdsm_item", "restraint_item"], [], []],
        ["sex swing", 0.7, [], ["bdsm_item", "furniture"], [], []],
        ["bondage chair", 0.5, [], ["bdsm_item", "furniture"], [], []],
        ["stocks (pillory)", 0.3, [], ["bdsm_item", "furniture"], [], []],
        ["St. Andrew's cross", 0.3, [], ["bdsm_item", "furniture"], [], []],
        ["muzzle gag", 0.5, [], ["bdsm_item", "gag_item"], [], []],
        ["spider gag", 0.3, [], ["bdsm_item", "gag_item"], [], []],
        ["suspension ropes", 0.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["hogtie restraints", 0.7, [], ["bdsm_item", "restraint_item"], [], []], # Itemizing the result
        ["straightjacket", 0.2, ["asylum cell"], ["bdsm_item", "restraint_item"], [], []], # Very specific
        ["thumbcuffs", 0.5, [], ["bdsm_item", "restraint_item"], [], []],
        ["wartenberg wheel", 0.2, [], ["bdsm_item", "sensation_item"], [], []],
        ["violet wand (device)", 0.2, [], ["bdsm_item", "sensation_item", "electro_play"], [], []],
        ["flesh hooks", 0.05, [], ["bdsm_item", "extreme_play"], [], []], # Very extreme
        ["safety scissors (for rope)", 0.5, ["rope", "bdsm_item"], [], [], []], # Utility

        # Food/Drink as Props
        ["wine glass", 2, [], [], [], []],
        ["champagne flute", 1, [], [], [], []],
        ["bottle of wine", 1.5, [], [], [], []],
        ["bottle of champagne", 1, [], [], [], []],
        ["beer bottle", 1, [], [], [], []],
        ["whiskey glass", 1, [], [], [], []],
        ["strawberries", 1, [], ["food_item"], [], []],
        ["cherries", 0.5, [], ["food_item"], [], []],
        ["whipped cream can", 1, [], ["food_item"], [], []],
        ["chocolate syrup bottle", 0.5, [], ["food_item"], [], []],
        ["ice cubes", 1, [], ["sensation_item"], [], []],
        ["honey jar", 0.5, [], ["food_item"], [], []],
        ["sushi platter", 0.2, [], ["food_item"], [], []], # Nyotaimori context

        # Clothing as Props (discarded on floor, etc.)
        ["discarded clothes", 4, [], [], [], []],
        ["pile of clothes", 3, [], [], [], []],
        ["bra on floor", 2, [], [], ["female"], []],
        ["panties on floor", 2, [], [], ["female"], []],
        ["thong on floor", 1.5, [], [], ["female"], []],
        ["stockings (discarded)", 1.5, [], [], ["female"], []],
        ["heels (discarded)", 1.5, [], [], ["female"], []],
        ["shirt (open/on floor)", 2, [], [], [], []],
        ["trousers (on floor)", 1.5, [], [], [], []],
        ["boxers (on floor)", 1, [], [], ["male"], []],
        ["briefs (on floor)", 1, [], [], ["male"], []],
        ["dress (on floor)", 1.5, [], [], ["female"], []],

        # Tech/Recording/Voyeurism
        ["camera (still/video)", 1.5, [], ["recording_device"], [], []],
        ["tripod with camera", 1, ["camera"], ["recording_device"], [], []],
        ["smartphone (recording/photo)", 1.5, [], ["recording_device"], [], []],
        ["webcam", 0.7, [], ["recording_device"], [], []],
        ["hidden camera", 0.3, [], ["recording_device", "voyeur_theme"], [], []], # Non-con implication
        ["laptop (open)", 2, [], [], [], []],
        ["tablet device", 1, [], [], [], []],
        ["headphones", 1, [], [], [], []],
        ["microphone (studio/handheld)", 0.5, [], [], [], []],
        ["remote control (for toys/camera)", 1, [], [], [], []],
        ["security monitor", 0.3, ["control room"], ["voyeur_theme"], [], []],

        # Miscellaneous / Scene Setting / Darker Themes
        ["candles (lit for atmosphere)", 4, [], [], [], []],
        ["candelabra", 1, [], [], [], []],
        ["incense burning", 1, [], [], [], []],
        ["rose petals (scattered)", 2, [], [], [], []],
        ["condom wrapper", 2, [], [], [], []],
        ["condom (unused)", 1.5, [], [], [], []],
        ["used condom", 2.5, [], [], [], []],
        ["lube bottle", 3.5, [], ["sex_aid"], [], []],
        ["pool of lubricant", 1, [], ["sex_aid"], [], []],
        ["tissues (box/scattered)", 2, [], [], [], []],
        ["cigarettes", 1, [], [], [], []],
        ["lit cigarette", 0.5, ["cigarettes"], [], [], []],
        ["ashtray", 0.5, ["cigarettes"], [], [], []],
        ["book (open/closed)", 1, [], [], [], []],
        ["diary", 0.5, [], [], [], []],
        ["musical instrument", 0.5, [], [], [], []], # e.g., guitar, piano
        ["syringe (medical/drugs)", 0.2, [], ["medical_item", "drug_item", "non_con_tool"], [], []], # Caution
        ["scalpel", 0.1, [], ["medical_item", "weapon_item", "extreme_gore"], [], []], # Extreme caution
        ["plastic sheeting", 0.3, ["basement", "abandoned building"], ["non_con_tool", "gore_prep"], [], []], # Dark
        ["bucket", 0.5, [], [], [], []],
        ["cleaning supplies", 0.3, [], [], [], []], # Aftermath implication
        ["evidence bag", 0.1, ["crime scene"], [], [], []], # Very dark
        ["knife", 0.5, [], ["weapon_item", "non_con_tool"], [], []],
        ["gun", 0.3, [], ["weapon_item", "non_con_tool"], [], []],
        ["baseball bat", 0.2, [], ["weapon_item"], [], []],
        ["money (scattered/pile)", 1, [], [], [], []], # Prostitution/transaction
        ["drugs (powder/pills)", 0.2, [], ["drug_item", "non_con_tool"], [], []], # Caution
        ["alcohol bottle (generic)", 1.5, [], [], [], []],
        ["empty alcohol bottles", 1, [], [], [], []],
        ["broken bottle", 0.5, [], ["weapon_item"], [], []],
        ["bloodstains", 0.1, [], ["gore_element", "violence_aftermath"], [], []], # Caution, for very specific themes
        ["examination table", 0.2, ["medical_theme", "non_con_setting"], [], [], []],
        ["IV drip stand", 0.1, ["medical_theme", "non_con_setting"], [], [], []],
        ["first aid kit", 0.5, [], [], [], []],
    ],
    "tg": [ # Effects
        ["motion", 8, [], [], [], []],
        ["motion lines", 8, [], [], [], []],
        ["depth of field", 8, [], [], [], []],
        ["bokeh", 5, [], [], [], []],
        ["motion blur", 4, [], [], [], []], 
        ["lens flare", 2, [], [], [], []],
        ["sweat drops", 5, [], [], [], []],
        ["glowing skin", 4, [], [], [], []],
        ["rim lighting", 5, [], [], [], []],
    ],
    "tf": [ # Colors - for the rare clothing item, hair, eyes
        ["blue", 5, [], [], [], []], 
        ["red", 5, [], [], [], []],
        ["black", 5, [], [], [], []],
        ["white", 5, [], [], [], []],
        ["pink", 5, [], [], [], []],
        ["purple", 3, [], [], [], []],
    ]
}

# NSFW specific tags for the sexual content
nsfw_specific_tags = {
    "p": [ # Pussy details
        ["uncensored pussy", 10], 
        ["detailed pussy", 8], 
        ["pussy lips visible", 7],
        ["shaved pussy", 6], 
        ["natural pubic hair", 5], 
        ["trimmed pubic hair", 4],
        ["wet pussy", 8], 
        ["gaping pussy", 5], 
        ["puffy pussy lips", 4],
        ["close-up of pussy", 6]
    ],
    "mp": [ # Penis details
        ["uncensored penis", 10], 
        ["detailed penis", 8], 
        ["veiny penis", 6],
        ["large penis", 7], 
        ["huge penis", 5], 
        ["average penis", 6], 
        ["erect penis", 10], 
        ["testicles visible", 8], 
        ["balls", 8], 
        ["pre-cum dripping", 6], 
        ["close-up of penis", 6],
    ],
    "naked_with_item": [ # All scenes are naked, EXCEPT for these rare items
        ["naked except for a t-shirt", 5, ["t-shirt"]],
        ["naked except for an open shirt", 4, ["open shirt"]],
        ["naked except for panties", 5, ["panties"]],
        ["naked except for a bra", 5, ["bra"]],
        ["naked except for a lingerie set", 3, ["lingerie set"]],
        ["naked except for a garter belt and stockings", 2, ["garter belt", "stockings"]],
        ["naked except for a swimsuit", 4, ["swimsuit"]],
        ["naked except for a one piece swimsuit", 4, ["swimsuit"]],
        ["naked except for a micro bikini", 3, ["micro bikini"]],
        ["naked except for socks", 2, ["socks"]],
        ["naked except for thighhighs", 3, ["thighhighs"]],
        ["naked except for a collar", 2, ["choker"]],
        ["naked except for glasses", 1, ["glasses"]],
    ],
    "ejaculation_events": [
        ["ejaculation", 10], 
        ["cumming", 10], 
        ["male ejaculation", 9], 
        ["shooting cum", 8],
        ["fertilization", 8],
        ["creampie", 8, [], [], ["female", "intercourse_vaginal"], []], 
        ["deep creampie", 6, [], [], ["female", "intercourse_vaginal"], []],
        ["cum dripping from pussy", 7, [], [], ["female", "intercourse_vaginal"], []],
        ["anal creampie", 8, [], [], ["female", "intercourse_anal"], []],
        ["cum dripping from ass", 7, [], [], ["female", "intercourse_anal"], []],
        ["facial", 7], 
        ["cum on face", 7], 
        ["cum covering face", 5],
        ["cum on breasts", 6, [], [], ["female"], []], 
        ["cum on tits", 6, [], [], ["female"], []],
        ["cum on stomach", 5], 
        ["cum on abs", 4],
        ["cum on ass", 5, [], [], ["female"], []],
        ["cum in mouth", 4], 
        ["mouthful of cum", 3],
        ["cum on body", 6], 
        ["covered in cum", 4],
        ["female ejaculation", 3, [], [], ["female"], []], 
        ["squirting", 3, [], [], ["female"], []],
        ["semen visible", 7], 
        ["thick semen", 6], 
        ["gooey semen", 5],
        ["pussy juice and semen mixed", 6, [], [], ["female"], []],
        ["internal cumshot", 4],
        ["pull out and cum", 3],
    ],
    "core_acts_intercourse": [
        # --- Consensual - Common & Foundational ---
        ["sex, missionary position, man on top, eye contact, gentle thrusts", 10],
        ["sex, missionary position, man on top, passionate kissing, deep thrusts", 9],
        ["sex, missionary position, woman's legs wrapped around his waist", 8],
        ["sex, missionary position, woman's legs on his shoulders, deep penetration", 7],
        ["sex, doggy style, from behind, ass focus, rhythmic pounding", 10],
        ["sex, doggy style, from behind, deep thrusts, hands on her hips", 9],
        ["sex, doggy style, face down ass up, looking back seductively", 7, [], [], ["female"], []],
        ["sex, doggy style, kneeling, arching back", 8],
        ["sex, woman on top, cowgirl position, riding penis, hip grinding passionately", 9],
        ["sex, woman on top, cowgirl position, slow and sensual ride, teasing", 7],
        ["sex, woman on top, reverse cowgirl position, pussy grinding hard against him", 8],
        ["sex, woman on top, reverse cowgirl position, looking over shoulder, ass focus", 7],
        ["sex, standing, holding her up against wall, legs wrapped around his waist, intense", 7],
        ["sex, standing, her back to wall, his hand on her throat (consensual rough play)", 6],
        ["sex, standing, one leg hiked up on furniture for deeper access", 5],
        ["sex, legs wrapped around waist, deep penetration, pulling her closer", 8],
        ["sex, legs on shoulders, intense fucking, her hips lifted", 8],
        ["sex, spooning position, intimate and gentle, morning light", 6],
        ["sex, spooning position, deep thrusts from behind, sleepy sex", 7],
        ["sex, prone bone, face down ass up, rhythmic fucking, hands gripping sheets", 7, [], [], ["female"], []],
        ["sex, prone bone, man pressing her down, deep grinding", 6, [], [], ["female"], []],
        ["sex, passionate, deep kissing, bodies pressed together, breathless", 7],
        ["sex, rough, hair pulling, biting neck, marking skin (consensual)", 7],
        ["pussy fucking, close-up on penetration, wet sounds", 9],
        ["slow sex, sensual grinding, whispers, building tension", 6],
        ["fast sex, pounding, breathless, frantic pace", 7],
        ["deepthroating penis with vagina, extreme vaginal depth, stretching sensation", 4], # Anatomically unlikely but common tag
        ["lotus position sex, intimate connection, eye gazing, spiritual", 4],
        ["X-marks-the-spot position sex (pretzel dip), deep angle, flexible", 3],
        ["piledriver sex position, her upside down, legs locked around his neck", 4],
        ["sex on a chair, her facing him, straddling his lap, intense eye contact", 6],
        ["sex on a chair, her facing away, bent over his lap", 5],
        ["sex on a table, her on back, legs spread wide, vulnerable", 6],
        ["sex on kitchen counter, one leg propped up, urgent", 5],
        ["sex, outdoor, leaning against tree, rustling leaves", 5],
        ["sex, shower, bodies wet and slick, steam rising", 6],
        ["sex, bed, tangled sheets, lazy afternoon fucking", 8],
        ["urgent sex, clothes partially on, desperate fumbling, against a door", 7],
        ["loving sex, tender caresses, soft moans, slow build-up", 6],
        ["teasing sex, shallow thrusts, denial and pleasure", 4],
        ["exploratory sex, trying new angles, playful", 5],
        ["sex, bent over furniture (bed edge, sofa arm), from behind", 7],
        ["sex, her on her side, one leg raised, deep access", 6],
        ["synchronized breathing during sex, connected, rhythmic", 3],
        ["orgasmic sex, building to climax, convulsions, screaming pleasure", 7],
        ["sex, hands bound playfully, vulnerable (consensual)", 4],
        ["sex, blindfolded (consensual), heightened senses", 4],
        ["sex with dirty talk, encouraging moans, explicit words", 6],
        ["sex, grinding against his thigh before penetration, teasing", 4],
        ["sex, making out intensely during, tongues tangling", 7],
        ["sex, him sitting, her straddling facing him, energetic riding", 6],
        ["sex, him sitting on edge of bed, her standing and leaning down onto him", 5],
        ["sex, sixty-nine (69) position, mutual oral while fucking (if possible)", 3], # tricky for AI
        ["sex, woman initiating, taking control, dominant female", 5],
        ["sex, man dominating, assertive, taking lead", 5],
        ["sex, athletic, acrobatic positions, flexible couple", 3],
        ["sex in a car, cramped space, steamed up windows", 5],
        ["sex on the floor, carpet burns, raw passion", 6],
        ["sex, using pillows to prop hips for better angle", 5],
        ["sex, woman guiding his penis in, taking charge of entry", 6],
        ["sex, hand pressed against her mouth to muffle moans (playful)", 4],
        ["sex, mirrored, watching themselves in a mirror", 3],
        ["sex, celebratory, after good news, joyful", 4],
        ["sex, reconciliation, making up after a fight, emotional", 4],
        ["sex, sleepy, half-awake fumbling, comforting", 5],
        ["sex, drunk, uninhibited, clumsy but fun", 4],
        ["sex, high energy, almost fighting, aggressive play", 5],
        ["sex, shared orgasm, climaxing together", 6],
        ["sex, him gently spreading her lips before entry", 7],
        ["sex, deep vaginal fucking, cervix stimulation (implied)", 6],
        ["sex, rhythmic slapping of skin, wet sounds", 7],
        ["sex, man lifting woman easily, showing strength", 5],

        # --- Non-Consensual Themes - Intercourse ---
        ["forced sex, missionary position, pinned down hard, struggling violently", 7],
        ["forced sex, missionary position, wrists held above head, terror in eyes", 6],
        ["rape, doggy style, victim crying silently, held firmly by hips, face hidden", 7],
        ["rape, doggy style, hair pulled back hard, neck exposed, whimpering", 6],
        ["vaginal rape, woman actively resisting, overpowered by brute strength", 6],
        ["vaginal rape, clothes torn, body bruised, defiant glare amidst tears", 5],
        ["nonconsensual intercourse, standing, slammed against wall, dazed victim", 6],
        ["nonconsensual intercourse, standing, one leg forced up, shock and pain", 5],
        ["forced prone bone, face pressed into mattress, muffled screams, body trembling", 6, [], [], ["female"], []],
        ["forced prone bone, hands tied behind back, helpless arching", 5, [], [], ["female"], []],
        ["struggling during intercourse, trying to push away, kicking legs", 7],
        ["pinned down and fucked, tears streaming down face, begging to stop", 7],
        ["rape, legs forced open wide, humiliated and exposed, vacant stare", 6],
        ["rape, assailant smirking, enjoying her suffering", 5],
        ["abducted and raped, dirty room, fear scent, constant threat", 5],
        ["abducted and raped, gagged with cloth, blindfolded, disoriented", 4],
        ["blackmail sex, unwilling participant, humiliated expression, forced compliance", 4],
        ["blackmail sex, forced to perform, shame and anger hidden", 3],
        ["drugged and raped, limp body, vacant eyes, drooling", 3], # Sensitive
        ["intercourse with unconscious person, nonconsensual, lifeless victim", 3], # Sensitive
        ["sleep rape, waking up to violent penetration, confusion and terror", 3], # Sensitive
        ["forced impregnation, breeding rape, despair and violation, trapped", 4],
        ["gang rape, multiple assailants, overwhelmed victim, brutalized", 2], # Very extreme
        ["gang rape, passed around, broken spirit, dark alley", 2], # Very extreme
        ["public rape, onlookers, victim's intense shame and terror, exposed", 2], # Very extreme
        ["bound and raped, rope bondage cutting into skin, struggling futilely", 6],
        ["bound and raped, spread eagle on bed, total helplessness", 5],
        ["gagged and raped, silenced victim, fear in wide eyes, tears leaking", 6],
        ["gagged and raped, ball gag, muffled whimpers of pain", 5],
        ["surprise sex from behind, nonconsensual, slammed forward, sharp pain", 5],
        ["breaking and entering, home invasion rape, night terror, caught unaware", 5],
        ["captured and used, sex slave, despair in eyes, collar and chain", 4],
        ["captured and used, daily rape, broken will, submissive fear", 3],
        ["forced to spread legs for intercourse, trembling from fear", 6],
        ["rough handling, forced entry, painful tearing sensation, crying out", 6],
        ["rape by surprise, attacker hiding, sudden assault", 5],
        ["interrogation rape, power play, breaking the victim, cold room", 3],
        ["revenge rape, hateful expression from assailant, cruel words", 3],
        ["rape, victim trying to cover self, clothes ripped away", 6],
        ["forced to endure, dissociation, staring blankly during rape", 5],
        ["threatened with weapon during rape, knife to throat, terrified compliance", 4],
        ["ambush rape, dragged into bushes, struggling on rough ground", 5],
        ["rape in a car, trapped, unable to escape, banging on windows", 4],
        ["coerced sex, subtle threats, fear of repercussions, no choice", 4],
        ["rape, assailant much larger, complete physical overpowering", 6],
        ["rape, leaving bruises and marks, evidence of assault", 5],
        ["rape, victim goes limp, giving up fight, empty eyes", 4],
        ["rape, using her body like an object, dehumanizing", 5],
        ["forced orgasm during rape, involuntary convulsions, shame and disgust", 3], # Complex, sensitive
        ["rape, then abandoned, left crying and broken", 4],
        ["nonconsensual, first time, terrified virgin, painful defloration", 4], # Specific
        ["hatefuck, brutal intercourse driven by anger, painful", 5],
        ["rape, victim's hands clawing at assailant's back, desperate defense", 6],
        ["forced vaginal creampie, nonconsensual internal ejaculation, disgust", 5],
        ["mind break during rape, incoherent sobbing, complete submission to terror", 2], # Extreme psychological
        ["rape, victim pleading for mercy, ignored by assailant", 6],
        ["slapping face during rape, humiliation and pain", 5],
        ["choking during rape, gasping for air, adding to terror", 4],
        ["rape, victim's perspective, focusing on her fear and violation", 5, [], [], ["female"], []], # POV hint
        ["rape, assailant's perspective, focusing on power and dominance", 5, [], [], ["male"], []], # POV hint
        ["war rape, victim of conflict, trauma, soldier assailant", 2], # Very specific, sensitive
        ["human trafficking victim, forced prostitution, dead eyes", 3] # Scenario context
    ],
    "core_acts_anal": [
        # --- Consensual - Common & Foundational ---
        ["anal sex, missionary position, man on top, careful entry, lots of lube", 8],
        ["anal sex, missionary position, legs high, deep anal penetration", 7],
        ["anal sex, doggy style, from behind, ass focus, deep powerful anal thrusts", 10],
        ["anal sex, doggy style, rhythmic pounding, hands gripping her waist", 9],
        ["anal sex, doggy style, her arching back, offering ass", 8],
        ["anal sex, woman on top, reverse cowgirl anal, controlled riding, grinding on penis", 7],
        ["anal sex, woman on top, reverse cowgirl anal, looking back, ass cheeks spread", 6],
        ["anal sex, spooning position, on side, intimate anal, gentle stretching", 6],
        ["anal sex, spooning position, deep, slow anal thrusts from behind", 7],
        ["anal sex, standing, bent over table, ass up, vulnerable offering", 8],
        ["anal sex, standing, leaning against wall, one leg lifted for access", 7],
        ["anal sex, legs on shoulders, deep anal penetration, stretching asshole wide", 9],
        ["anal sex, legs held straight up, complete anal exposure", 7],
        ["anal sex, prone bone, face down ass up, rhythmic anal fucking, ass quivering", 8, [], [], ["female"], []],
        ["anal sex, prone bone, hips tilted up with pillow, deeper access", 7, [], [], ["female"], []],
        ["ass fucking, close-up on anal penetration, lubrication visible, asshole gaping", 10],
        ["slow anal sex, careful stretching, gentle moans, building to intensity", 6],
        ["hard anal sex, pounding ass, crying out (pleasure/pain mix), red ass", 7],
        ["first time anal sex, nervous, careful, lots of lube, slow entry", 5],
        ["anal sex, woman on back, legs held high and wide by her hands", 7],
        ["anal sex, spanking during, red ass, building to anal entry", 6],
        ["wide open ass, rosebud, ready for anal penetration, glistening with lube", 7],
        ["anal stretching, fingers then penis, gradual preparation", 5],
        ["deep anal fucking, hitting deep spots, intense sensations", 8],
        ["anal sex, him sitting, her straddling him facing away, reverse cowgirl anal on lap", 6],
        ["anal sex, bent over his knees, spanked then fucked", 6],
        ["passionate anal sex, kissing, eye contact, intense connection", 7],
        ["anal sex with vibrator on clit, dual stimulation", 5],
        ["experimental anal positions, exploring angles", 4],
        ["anal sex, feeling of fullness, stretching pleasure", 7],
        ["quick and rough anal sex, urgent, against a wall", 6],
        ["anal orgasm, intense full body convulsions from anal pleasure", 6],
        ["anal sex, teasing entry, pulling out and pushing back in slowly", 5],
        ["using butt plug before anal sex to prepare", 4],
        ["anal sex in shower, water as lube, slippery", 5],
        ["anal sex, woman guiding his penis to her ass", 6],
        ["anal sex, man lifting her hips for deeper thrusts", 7],
        ["anal sex, dirty talk about her tight ass", 6],
        ["anal sex, grinding, circular motions for varied stimulation", 5],
        ["ass worship before anal sex, licking, kissing asshole", 4],

        # --- Non-Consensual Themes - Anal ---
        ["forced anal sex, missionary, pinned down, painful stretching, screams", 7],
        ["forced anal sex, missionary, legs forced apart, tears of pain", 6],
        ["anal rape, doggy style, victim struggling violently, crying out, held by hair", 8],
        ["anal rape, doggy style, face pushed into ground, brutal thrusts", 7],
        ["nonconsensual anal sex, bent over furniture, held down firmly, sobbing", 7],
        ["nonconsensual anal sex, no lubrication, agonizing friction, bleeding", 6],
        ["forced anal entry, screaming in pain, resisting futilely, body shaking", 7],
        ["anal rape, legs forced over shoulders, helpless exposure, intense pain", 7],
        ["surprise anal sex, from behind, nonconsensual, shock and tearing pain", 6],
        ["pinned face down, forced anal, muffled cries into pillow, body rigid", 6, [], [], ["female"], []],
        ["struggling against anal rape, trying to clench sphincter, overpowered", 6],
        ["anal violation, overpowered, humiliated, feeling defiled", 6],
        ["bound and anally raped, helpless victim, ropes cutting in, despair", 6],
        ["bound spread eagle for anal rape, total vulnerability", 5],
        ["gagged during anal rape, silent tears, eyes wide with terror", 6],
        ["ball gag during anal rape, muffled screams of agony", 5],
        ["drugged for anal rape, unresponsive victim, body used like a doll", 3], # Sensitive
        ["unconscious anal rape, limp body, no resistance", 3], # Sensitive
        ["forced ass to mouth (after anal), degrading humiliation, disgust", 2], # Extreme, related
        ["double anal penetration, nonconsensual, tearing, overwhelmed", 2], # Extreme, implies multiple attackers or large toys
        ["public anal humiliation, forced act in front of others, shame", 2], # Extreme
        ["brutal anal fucking, nonconsensual, bleeding profusely, lasting injury", 4], # Graphic
        ["forced to take large object anally, nonconsensual, extreme stretching, pain", 3],
        ["anal rape, victim arching back in pain, trying to escape penetration", 7],
        ["anal rape, assailant taunting, cruel words during assault", 5],
        ["breaking and entering, home invasion, surprised and anally raped", 5],
        ["captured and used for anal sex, slave-like conditions, hopelessness", 4],
        ["forced anal creampie, nonconsensual internal ejaculation in ass, revulsion", 6],
        ["anal rape, victim trying to crawl away, dragged back", 6],
        ["hate-filled anal rape, intent to injure and degrade", 5],
        ["first time anal, nonconsensual, extreme pain, terror", 5],
        ["revenge anal rape, targeted violation, assailant's cold fury", 4],
        ["anal rape, victim shitting self from fear or force, extreme humiliation", 1], # Very graphic, extreme
        ["using object to force open asshole before rape", 4],
        ["spitting on ass as lube for rape, degrading", 5],
        ["gang anal rape, multiple assailants, torn and bleeding, psychological trauma", 2], # Very extreme
        ["anal rape, assailant filming the act, further violation", 3],
        ["mind break during anal rape, victim becoming catatonic", 2] # Extreme psychological
    ],

    "nsfw_details_misc": [ 
        ["pubic hair", 7], 
        ["bush", 5], 
        ["shaved", 8], 
        ["xray", 10],
        ["trimmed pubic hair", 6],
        ["pussy juice", 7, [], [], ["female"], []], 
        ["wetness", 7],
        ["clitoris visible", 5, [], [], ["female"], []],
        ["areolae visible", 8], 
        ["puffy nipples", 7], 
        ["dark nipples", 5], 
        ["erect nipples", 8],
        ["nipple piercing", 2, [], [], ["female"],[]], 
        ["armpits visible", 3], 
        ["shaved armpits", 2],
        ["lactation", 1, [], [], ["female"], []], 
        ["pregnant sex", 0.5, [], [], ["female"], []], 
        ["exhibitionism", 2], 
        ["cameltoe", 1, [], [], ["female"], []], 
        ["stomach bulge from deep penetration", 3, [], [], ["female"],[]],
        ["asshole visible", 7], 
        ["anus visible", 7], 
        ["puckered asshole", 5], 
        ["gaping asshole", 4],
        ["egg fertilization", 0.5, [], [], ["female", "internal_cumshot_vaginal"], []], 
        ["womb view, fertilization happening", 0.3, [], [], ["female", "internal_cumshot_vaginal"], []], 
        ["sperm visible inside pussy", 3, [], [], ["female", "internal_cumshot_vaginal"],[]],
        ["sperm visible inside ass", 3, [], [], ["female", "internal_cumshot_anal"],[]],
        ["sweat on body", 7], 
        ["glistening with sweat", 6],
        ["veins popping", 4]
    ],
    "toys_rare": [ # Very low chance of being picked
        ["using dildo", 1], 
        ["using vibrator", 1], 
        ["anal beads insertion", 0.5],
        ["butt plug visible", 0.5]
    ],
    "bd": [ # Bondage items - RARE
        ["blindfold", 1], 
        ["rope bondage", 0.5], 
        ["handcuffs", 0.5], 
        ["ball gag", 0.3],
    ],
    "positions": [
        # --- On Back (Supine) ---
        ["on back, legs spread", 30],
        ["on back, legs wide apart", 20],
        ["on back, legs raised", 15],
        ["on back, knees to chest", 10], # Good for deep penetration, impregnation
        ["on back, ankles on shoulders", 8], # Deep penetration, impregnation
        ["on back, ankles behind head", 5], # Flexible, very deep
        ["on back, hips raised (e.g. pillow under hips)", 15], # Impregnation focus
        ["missionary position", 10], # Classic
        ["starfish position (on back, limbs spread wide)", 15], # Vulnerable
        ["pinned on back, arms above head", 15], # Non-con
        ["pinned on back, legs forced open", 15], # Non-con
        ["spread eagle on back", 15], # Vulnerable, BDSM, Non-con
        ["spread eagle restrained", 15], # Vulnerable, BDSM, Non-con
        ["butterfly position (on back, soles of feet together, knees open)", 10],

        # --- On Stomach (Prone) ---
        ["on stomach, legs slightly apart", 7],
        ["face down, ass up", 10], # Versatile, doggy, non-con if forced
        ["prone bone (general term for sex while prone)", 8],
        ["prone, legs spread wide", 6],
        ["prone, hips slightly raised", 7], # For better access
        ["pinned on stomach, arms behind back", 5], # Non-con
        ["spread eagle (on stomach, restrained or willing)", 5], # Vulnerable, BDSM, Non-con
        ["face pressed into mattress/pillow/surface", 4], # Can imply non-con, suffocation play

        # --- On Hands and Knees / All Fours / Kneeling ---
        ["on hands and knees", 10], # Classic for doggy style
        ["doggy style", 10], # General term, very common
        ["presenting (on hands and knees, invitingly or forced)", 7],
        ["all fours", 9], # Similar to on hands and knees
        ["kneeling", 6],
        ["kneeling, leaning forward", 6],
        ["kneeling, back arched", 5],
        ["forced to kneel (submissive / non-con)", 4],

        # --- Sitting / Rider Positions ---
        ["sitting on penis (general)", 7], # Original, kept for compatibility
        ["cowgirl position (woman on top, facing forward)", 9],
        ["reverse cowgirl position (woman on top, facing away)", 8],
        ["empress position (variation of cowgirl, leaning back)", 5],
        ["lap dance position (sexual, leading to intercourse)", 5],
        ["sitting on lap, facing partner", 6],
        ["sitting on lap, facing away from partner", 5],
        ["sitting, legs spread open (e.g. on edge of bed/chair)", 7],

        # --- Standing Positions ---
        ["standing sex", 7],
        ["standing, bent over at waist (partner behind)", 8], # Doggy variant, non-con potential
        ["standing, one leg raised/hooked around partner", 6],
        ["standing, lifted/carried during sex", 6],
        ["against wall (standing, general)", 8],
        ["pinned against wall (forcefully)", 6], # Non-con

        # --- Bent Over (various contexts) ---
        ["bent over (at waist, general)", 9], # Versatile, e.g., over a surface
        ["bent over furniture (table, chair, bed edge)", 8], # Can be non-con if forced
        ["bent over, hands on knees", 7],
        ["bent over, hands on ankles/floor", 6], # Deeper bend
        ["sharply bent over, ass presented high", 7],

        # --- Spooning / On Side ---
        ["on side (spooning position, entry from behind)", 7],
        ["on side, facing each other (intimate, leg intertwined)", 5],
        ["on side, top leg raised high (for deeper access)", 6],

        # --- Modifiers / General Postures / Limb Placements ---
        ["arched back", 8], # Common modifier for many positions
        ["deeply arched back", 6],
        ["hips thrusting", 7], # Action, but implies a sustained part of a position
        ["grinding hips", 7], # Action, implies contact and motion
        ["straddling partner (on top or seated across)", 8], # Versatile
        ["legs wrapped around waist", 9], # Common, intimate, deep
        ["legs wrapped around neck", 4], # Flexible, very deep
        ["legs locked (around partner's back/waist securely)", 6],
        ["legs straight up in the air", 7], # Can aid impregnation
        ["legs held wide open (willingly or forced)", 7],
        ["presenting ass", 8], # Doggy, non-con, inviting
        ["presenting pussy", 8], # Inviting, vulnerable

        # --- More Specific / Named / Advanced Positions ---
        ["lotus position (seated, facing, legs intertwined)", 3],
        ["standing wheelbarrow position", 4], # Deep, impregnation potential
        ["kneeling wheelbarrow position", 3], # Variation
        ["pile driver position (forceful, often implies roughness)", 4], # Can be rough/non-con
        ["bridge position (hips raised high off ground, supported or not)", 4],
        ["pretzel dip position", 3], # Specific, acrobatic
        ["lotus trap position", 3], # Advanced

        # --- Explicit Non-Con / Restraint / Dominance Focused ---
        ["held down firmly", 6], # General non-con
        ["arms pinned above head", 6], # Non-con, BDSM
        ["arms pinned behind back", 5], # Non-con, BDSM
        ["legs pinned together (resisting)", 4], # Implies struggle
        ["legs held apart by captor(s)", 5], # Clear non-con
        ["manhandled into position", 5], # Non-con
        ["struggling against position/restraints", 4], # Active non-con
        ["over the knee (domineering, for spanking or sex)", 5], # Can be con or non-con
        ["forced submission position", 4], # General non-con
        ["human furniture (objectification)", 2], # Extreme, non-con
        ["suspended (e.g. in slings, ropes - BDSM/non-con)", 2], # Requires more setup
    ]
}

def get_weighted_choice(choices_with_weights, current_scene_tags_set, character_flags_set=None):
    if character_flags_set is None:
        character_flags_set = set()

    filtered_choices = []
    for choice_item_orig in choices_with_weights:
        choice_item = list(choice_item_orig) # Make a mutable copy
        if len(choice_item) < 2: continue

        tag_to_return = choice_item[0]
        weight = choice_item[1]
        
        # Pad with defaults if shorter than 6 elements
        scene_requires = choice_item[2] if len(choice_item) > 2 and choice_item[2] else []
        char_adds = choice_item[3] if len(choice_item) > 3 and choice_item[3] else []
        char_requires = choice_item[4] if len(choice_item) > 4 and choice_item[4] else []
        char_excludes = choice_item[5] if len(choice_item) > 5 and choice_item[5] else []
        
        full_choice_item = [tag_to_return, weight, scene_requires, char_adds, char_requires, char_excludes]

        is_choice_valid = True
        if scene_requires:
            if not all(cond in current_scene_tags_set for cond in scene_requires):
                is_choice_valid = False
        
        if is_choice_valid and char_requires:
            if not all(cond in character_flags_set for cond in char_requires):
                is_choice_valid = False
        
        if is_choice_valid and char_excludes:
            if any(cond in character_flags_set for cond in char_excludes):
                is_choice_valid = False
        
        if is_choice_valid:
            filtered_choices.append(full_choice_item)

    if not filtered_choices:
        return None

    total_weight = sum(item[1] for item in filtered_choices)
    if total_weight <= 0:
        return None

    rand_val = random.uniform(0, total_weight)
    cumulative_weight = 0
    for item in filtered_choices:
        cumulative_weight += item[1]
        if rand_val <= cumulative_weight:
            return item 
    
    return None 

def generate_character_tags(char_actual_type, current_scene_tags_set, is_pov_man, framing_tag_str, scene_act_type):
    char_tags_strings = []
    character_flags = set()

    if char_actual_type == "f":
        character_flags.add("female")
    elif char_actual_type == "m":
        character_flags.add("male")

    # MODIFICATION: Check if framing_tag_str is a valid string before using it
    if framing_tag_str:  # This handles None or empty string
        if framing_tag_str == "full body": 
            character_flags.update(["legs", "feet"])
        elif framing_tag_str == "cowboy_shot": 
            character_flags.add("legs")
        
        # The problematic line, now guarded:
        if "close-up" in framing_tag_str or "extreme close-up" in framing_tag_str:
            character_flags.add("is_closeup")
    # END MODIFICATION

    def_scene_tags_for_choice = current_scene_tags_set.union(set(char_tags_strings))

    # Simplified character generation for men in POV scenes
    simplified_man = char_actual_type == "m" and is_pov_man

    def apply_choice(category_key, probability, dataSource=tags_data, is_multi_part_tag=False, second_category_key=None):
        nonlocal def_scene_tags_for_choice
        if random.random() < probability:
            if category_key not in dataSource: 
                return
            
            choices = dataSource[category_key]
            chosen_item = get_weighted_choice(choices, def_scene_tags_for_choice, character_flags)
            if chosen_item:
                char_tags_strings.append(chosen_item[0])
                for flag in chosen_item[3]: 
                    character_flags.add(flag)
                def_scene_tags_for_choice.add(chosen_item[0])
                if chosen_item[0] == "long hair": 
                    character_flags.add("longhair")

                if is_multi_part_tag and second_category_key and second_category_key in dataSource:
                    chosen_item2 = get_weighted_choice(dataSource[second_category_key], def_scene_tags_for_choice, character_flags)
                    if chosen_item2:
                        char_tags_strings.append(chosen_item2[0])
                        for flag in chosen_item2[3]: 
                            character_flags.add(flag)
                        def_scene_tags_for_choice.add(chosen_item2[0])
    
    # --- Character Appearance ---
    # If man in POV, minimal details
    if simplified_man:
        # Very minimal description for POV man
        if random.random() < 0.2:  # Only sometimes add detail at all
            if random.random() < 0.3:
                apply_choice("e5", 1.0)  # Maybe muscular/abs
    else:
        # For women or non-POV men, full details
        apply_choice("e_dollar", 0.05)  # Species/Race (mostly human)
        apply_choice("eq", 0.8)      # Skin color
        
        if "noeyes" not in character_flags and not character_flags.intersection({"is_closeup", "genital_focus"}):
            apply_choice("tm", 0.8)      # Eye color
            apply_choice("eX", 0.4)      # Eye details
            apply_choice("eQ", 0.1)      # Eye shape

        apply_choice("eY", 0.7)      # Hair length
        apply_choice("eK", 0.6)      # Hair style
        apply_choice("tp", 0.8)      # Hair color
        apply_choice("tu", 0.05, is_multi_part_tag=True, second_category_key="tp")  # Multicolor hair rare
        apply_choice("e0", 0.5)      # Hair properties (messy, wet common)
        apply_choice("e1", 0.2)      # Bangs, sidelocks

        if "female" in character_flags: 
            apply_choice("e2", 1.0)  # Breast size

        # Body features
        num_e5_tags_to_add = random.choices([0, 1, 2], weights=[20, 60, 20], k=1)[0]
        for _ in range(num_e5_tags_to_add):
            apply_choice("e5", 1.0)

    # --- Nudity and Clothing Exceptions ---
    is_fully_nude = True
    character_flags.add("nude_by_default")  # Mark that default is nude

    if random.random() < 0.10 and not simplified_man:  # Only women or visible men get clothing items
        chosen_naked_item_spec = get_weighted_choice(nsfw_specific_tags.get("naked_with_item", []), def_scene_tags_for_choice, character_flags)
        if chosen_naked_item_spec:
            is_fully_nude = False
            character_flags.discard("nude_by_default")
            char_tags_strings.append(chosen_naked_item_spec[0])  # e.g., "naked except for a t-shirt"
            def_scene_tags_for_choice.add(chosen_naked_item_spec[0])
            
            # Add specific item if defined
            if len(chosen_naked_item_spec) > 2 and chosen_naked_item_spec[2]:
                for item_to_add_str in chosen_naked_item_spec[2]:
                    # Add color sometimes
                    item_tag = None
                    color_prefix = ""
                    if random.random() < 0.5:
                        color_item = get_weighted_choice(tags_data.get("tf", []), def_scene_tags_for_choice, character_flags)
                        if color_item: 
                            color_prefix = color_item[0]
                    
                    # Simple item lookup
                    item_tag = item_to_add_str

                    if item_tag:
                        final_item_tag = f"{color_prefix} {item_tag}".strip()
                        char_tags_strings.append(final_item_tag)
                        def_scene_tags_for_choice.add(final_item_tag)

    if is_fully_nude:
        char_tags_strings.append("nude")
        character_flags.add("fully_nude")
        def_scene_tags_for_choice.add("nude")

    # --- NSFW Character Details ---
    is_genitals_visible = "is_closeup" not in character_flags or \
                          ("portrait_framing" not in character_flags and \
                           "upper_body_framing" not in character_flags)

    # Add genital details for non-simplified characters
    if is_genitals_visible and not simplified_man:
        if "female" in character_flags:
            apply_choice("p", 0.9, nsfw_specific_tags)  # Pussy details
        if "male" in character_flags:
            apply_choice("mp", 0.9, nsfw_specific_tags)  # Penis details

    # Other NSFW details for non-simplified characters
    if not simplified_man:
        apply_choice("nsfw_details_misc", 0.7, nsfw_specific_tags)  # Other details
    
    # --- Expression --- (even for simplified man if face is visible)
    if not simplified_man or (simplified_man and random.random() < 0.3):
        apply_choice("to", 0.95)  # Expressions - occasionally add for POV man

    # --- Positions ---
    if not simplified_man:
        if random.random() < 0.7:  # High chance for position
            apply_choice("positions", 1.0, nsfw_specific_tags)

    # Filter eye color if eyes are closed/rolled back
    has_closed_eyes_tag = any(
        "closed eyes" in tag.lower() or "eyes rolled back" in tag.lower() 
        for tag in char_tags_strings
    ) or "noeyes" in character_flags

    if has_closed_eyes_tag:
        eye_color_tag_names_to_remove = {item[0] for item in tags_data.get("tm", [])}
        char_tags_strings = [tag_str for tag_str in char_tags_strings if tag_str not in eye_color_tag_names_to_remove]
            
    return char_tags_strings


def generate_prompts_nsfw(num_prompts_per_category):
    categories = {
        "prompts_man_woman_intercourse": {
            "is_nsfw": True,
            "target_list_key": "man_woman_intercourse",
            "scene_keywords": ["intercourse"],
            "act_type": "intercourse",
            "pov_man": False,
            "fixed_char_prefix_female": ["1girl", "adult woman"],
            "fixed_char_prefix_male": ["1boy", "adult man"]
        },
        "prompts_man_woman_anal": {
            "is_nsfw": True,
            "target_list_key": "man_woman_anal",
            "scene_keywords": ["anal sex"],
            "act_type": "anal",
            "pov_man": False,
            "fixed_char_prefix_female": ["1girl", "adult woman"],
            "fixed_char_prefix_male": ["1boy", "adult man"]
        },
        "prompts_pov_man_intercourse": {
            "is_nsfw": True,
            "target_list_key": "pov_man_intercourse",
            "scene_keywords": ["pov man", "intercourse"],
            "act_type": "intercourse",
            "pov_man": True,
            "fixed_char_prefix_female": ["1girl", "adult woman"],
            "fixed_char_prefix_male": ["1boy", "adult man"]
        },
        "prompts_pov_man_anal": {
            "is_nsfw": True,
            "target_list_key": "pov_man_anal",
            "scene_keywords": ["pov man", "anal sex"],
            "act_type": "anal",
            "pov_man": True,
            "fixed_char_prefix_female": ["1girl", "adult woman"],
            "fixed_char_prefix_male": ["1boy", "adult man"]
        },
    }

    all_prompts = {key_info["target_list_key"]: [] for key_info in categories.values()}

    for category_filename_base, params in categories.items():
        # is_nsfw_category = params["is_nsfw"] # This is always true for current categories
        current_category_key = params["target_list_key"]
        scene_act_type = params["act_type"]
        is_pov_man = params.get("pov_man", False)
        
        scene_keywords_from_params = params.get("scene_keywords", [])
        fixed_female_prefixes = params.get("fixed_char_prefix_female", ["1girl", "adult woman"])
        fixed_male_prefixes = params.get("fixed_char_prefix_male", ["1boy", "adult man"])


        print(f"Generating for category: {current_category_key}")
        generated_prompts_for_category = 0

        while generated_prompts_for_category < num_prompts_per_category:
            general_tags_for_scene_list = [] # Holds dynamically generated scene tags
            current_scene_tags_set = set()  # Initialize fresh for each prompt

            # Add scene_keywords_from_params to the set for requirements checking
            current_scene_tags_set.update(scene_keywords_from_params)

            # Add the scene act type flag
            if scene_act_type == "intercourse":
                current_scene_tags_set.add("intercourse_vaginal")
            elif scene_act_type == "anal":
                current_scene_tags_set.add("intercourse_anal")

            framing_tag_for_scene_str = None
            
            # --- Core Sexual Act Tag ---
            core_act_list_source_key = f"core_acts_{scene_act_type}"
            core_act_list = nsfw_specific_tags.get(core_act_list_source_key, [])

            if core_act_list:
                main_action_item = get_weighted_choice(core_act_list, current_scene_tags_set)
                if main_action_item:
                    general_tags_for_scene_list.append(main_action_item[0])
                    current_scene_tags_set.add(main_action_item[0]) # Add main action to set for context

            # --- General Scene Setup ---
            def apply_scene_choice(key, probability, dataSource=tags_data):
                # nonlocal current_scene_tags_set # Not needed as it's modified directly
                if random.random() < probability:
                    item = get_weighted_choice(dataSource.get(key, []), current_scene_tags_set)
                    if item:
                        general_tags_for_scene_list.append(item[0])
                        current_scene_tags_set.add(item[0])
                        # Add flags from chosen item to current_scene_tags_set if any (item[3] are char_adds, item[2] scene_requires)
                        # For scene choices, we mostly care about the tag itself for context.
                        # The get_weighted_choice already handles scene_requires.
                        return item[0]
                return None

            apply_scene_choice("eU", 0.6)  # Background detail
            apply_scene_choice("eZ", 0.7)  # Environment

            if not is_pov_man:
                if random.random() < 0.8:
                    apply_scene_choice("eH", 1.0) # Camera Angle (if not POV)
            # POV is handled by scene_keywords_from_params if applicable

            if random.random() < 0.9: # Framing
                framing_tag_item = get_weighted_choice(tags_data.get("eJ",[]), current_scene_tags_set)
                if framing_tag_item:
                    framing_tag_for_scene_str = framing_tag_item[0]
                    general_tags_for_scene_list.append(framing_tag_for_scene_str)
                    current_scene_tags_set.add(framing_tag_for_scene_str)
            
            apply_scene_choice("eV", 0.15) # Focus on specific part

            # --- Generate Character Specific Tags ---
            # Female character
            woman_tags_raw = generate_character_tags("f", current_scene_tags_set, is_pov_man, framing_tag_for_scene_str, scene_act_type)
            # Update scene_tags_set with woman tags for man's generation context
            for tag_str_char in woman_tags_raw:
                for tag_item_char in tag_str_char.split(','): # Tags from generate_character_tags can be comma-separated
                    current_scene_tags_set.add(tag_item_char.strip().replace("_", " "))
            
            # Male character
            man_tags_raw = generate_character_tags("m", current_scene_tags_set, is_pov_man, framing_tag_for_scene_str, scene_act_type)
            # Update scene_tags_set with man tags (though less critical after both are generated)
            for tag_str_char in man_tags_raw:
                for tag_item_char in tag_str_char.split(','):
                    current_scene_tags_set.add(tag_item_char.strip().replace("_", " "))

            # --- Ejaculation & Fertilization ---
            if random.random() < 0.75:
                ejac_item = get_weighted_choice(nsfw_specific_tags.get("ejaculation_events", []), current_scene_tags_set)
                if ejac_item:
                    ejac_tag = ejac_item[0]
                    valid_ejac = True
                    if "intercourse_vaginal" in current_scene_tags_set and "anal creampie" in ejac_tag:
                        valid_ejac = False
                    if "intercourse_anal" in current_scene_tags_set and ("creampie" in ejac_tag and "anal" not in ejac_tag): # e.g. "creampie" without "anal"
                        valid_ejac = False
                    
                    if valid_ejac:
                        general_tags_for_scene_list.append(ejac_tag)
                        current_scene_tags_set.add(ejac_tag)
                        if "creampie" in ejac_tag or "internal cumshot" in ejac_tag:
                            if "intercourse_vaginal" in current_scene_tags_set: current_scene_tags_set.add("internal_cumshot_vaginal")
                            if "intercourse_anal" in current_scene_tags_set: current_scene_tags_set.add("internal_cumshot_anal")

            if "internal_cumshot_vaginal" in current_scene_tags_set and random.random() < 0.05:
                fert_choices = [item for item in nsfw_specific_tags.get("nsfw_details_misc", []) if "fertilization" in item[0] or "womb" in item[0]]
                if fert_choices:
                    fert_item = get_weighted_choice(fert_choices, current_scene_tags_set)
                    if fert_item: general_tags_for_scene_list.append(fert_item[0]) # Not adding to current_scene_tags_set as it's a late detail

            # --- Other Scene Details ---
            apply_scene_choice("tg", 0.3)  # Effects
            if random.random() < 0.03: apply_scene_choice("toys_rare", 1.0, nsfw_specific_tags)
            if random.random() < 0.02: apply_scene_choice("bd", 1.0, nsfw_specific_tags)

            # --- Assemble Final Prompt String in New Order ---

            # 1. Clean General Scene Details
            # (scene_keywords_from_params are from category def, general_tags_for_scene_list are dynamic)
            _raw_general_tags = scene_keywords_from_params + general_tags_for_scene_list
            _cleaned_general_parts = []
            for tag_phrase in _raw_general_tags:
                for part in tag_phrase.split(','):
                    cleaned = part.strip().replace("_", " ")
                    if cleaned: _cleaned_general_parts.append(cleaned)
            cleaned_general_scene_tags = list(OrderedDict.fromkeys(_cleaned_general_parts))

            # 2. Clean Woman Details
            _raw_woman_details = []
            adult_woman_desc = next((p for p in fixed_female_prefixes if p == "adult woman"), None)
            if adult_woman_desc: _raw_woman_details.append(adult_woman_desc)
            _raw_woman_details.extend(woman_tags_raw)
            _cleaned_woman_parts = []
            for tag_phrase in _raw_woman_details:
                for part in tag_phrase.split(','):
                    cleaned = part.strip().replace("_", " ")
                    if cleaned: _cleaned_woman_parts.append(cleaned)
            cleaned_woman_tags = list(OrderedDict.fromkeys(_cleaned_woman_parts))

            # 3. Clean Man Details
            _raw_man_details = []
            adult_man_desc = next((p for p in fixed_male_prefixes if p == "adult man"), None)
            if adult_man_desc: _raw_man_details.append(adult_man_desc)
            _raw_man_details.extend(man_tags_raw)
            _cleaned_man_parts = []
            for tag_phrase in _raw_man_details:
                for part in tag_phrase.split(','):
                    cleaned = part.strip().replace("_", " ")
                    if cleaned: _cleaned_man_parts.append(cleaned)
            cleaned_man_tags = list(OrderedDict.fromkeys(_cleaned_man_parts))

            # 4. Construct ordered list for final prompt
            final_ordered_tags = []
            final_ordered_tags.extend(cleaned_general_scene_tags)
            
            girl_prefix_structural = next((p for p in fixed_female_prefixes if "girl" in p), "1girl")
            final_ordered_tags.append(girl_prefix_structural)
            final_ordered_tags.extend(cleaned_woman_tags)
            
            boy_prefix_structural = next((p for p in fixed_male_prefixes if "boy" in p), "1boy")
            final_ordered_tags.append(boy_prefix_structural)
            final_ordered_tags.extend(cleaned_man_tags)

            # Global deduplication, keeping first occurrences (important for structural tags)
            final_unique_ordered_tags = list(OrderedDict.fromkeys(tag for tag in final_ordered_tags if tag))
            
            if not final_unique_ordered_tags: continue

            # Apply emphasis
            processed_tags_for_final_string = []
            for tag in final_unique_ordered_tags:
                if random.random() < 0.01: processed_tags_for_final_string.append(f"{{{tag}}}")
                elif random.random() < 0.005: processed_tags_for_final_string.append(f"[[{tag}]]")
                else: processed_tags_for_final_string.append(tag)
            
            final_prompt_str = ", ".join(processed_tags_for_final_string)
            all_prompts[current_category_key].append(final_prompt_str)
            generated_prompts_for_category += 1
            
            if generated_prompts_for_category % 500 == 0:
                print(f"  Generated {generated_prompts_for_category}/{num_prompts_per_category} for {current_category_key}...")
        
        print(f"Completed {generated_prompts_for_category}/{num_prompts_per_category} prompts for {current_category_key}.")
    
    return all_prompts


if __name__ == "__main__":
    num_prompts_per_category = 40000  # 10k per category = 40k total
    print(f"Starting NSFW prompt generation: {num_prompts_per_category} prompts per category...")
    
    all_final_prompts = generate_prompts_nsfw(num_prompts_per_category)

    for category, prompts in all_final_prompts.items():
        filename = f"{category}_nsfw.txt"
        with open(filename, "w", encoding="utf-8") as f_out:
            for prompt in prompts:
                f_out.write(prompt + "\n")
        print(f"Written {len(prompts)} prompts to {filename}")
    
    print("NSFW prompt generation complete.")
