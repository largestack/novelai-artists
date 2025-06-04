import random
import json
from collections import OrderedDict

# Placeholder for tags_data that would be loaded from tags.json
# In a real implementation, you would do:
# with open('tags.json', 'r', encoding='utf-8') as f:
#     tags_data = json.load(f)
# For this example, I'll define a few representative lists.
# The actual tags.json would contain ALL lists (eH, eV, ..., tf)
# with the new 6-element structure: [tag_str, weight, scene_req, char_adds, char_req, char_excl]

tags_data = {
    "eH": [
        ["dutch angle", 5, [], [], [], []], 
        ["from above", 5, [], [], [], []], 
        ["from below", 5, [], [], [], []], 
        ["from side", 5, [], [], [], []], 
        ["straight-on", 5, [], [], [], []],
        ["looking at viewer", 5, [], [], [], []],
        ["profile", 5, [], [], [], []],
        ["pov", 4, [], [], [], []],
        ["dynamic angle", 4, [], [], [], []],
        ["selfie", 3, [], [], [], []],
        ["worm's eye view", 3, [], [], [], []],
        ["facing viewer", 5, [], [], [], []]
    ],
    
    "eV": [
        ["solo focus", 5, [], [], [], []], 
        ["ass focus", 5, ["portrait"], [], [], ["front"]], 
        ["foot focus", 5, ["portrait", "cowboy shot", "upper body"], [], ["feet"], []], 
        ["hip focus", 5, ["portrait"], [], [], []], 
        ["back focus", 5, [], [], [], ["front"]], 
        ["breast focus", 5, [], [], ["female"], []], 
        ["armpit focus", 3, [], [], [], []], 
        ["eye focus", 5, [], [], [], []],
        ["face focus", 5, [], [], [], []],
        ["navel focus", 4, [], [], [], []],
        ["leg focus", 4, [], [], [], []],
        ["thigh focus", 4, [], [], [], []],
        ["collarbone focus", 3, [], [], [], []],
        ["lip focus", 3, [], [], [], []],
        ["hand focus", 3, [], [], [], []],
        ["ear focus", 2, [], [], [], []],
        ["neck focus", 2, [], [], [], []],
        ["midriff focus", 4, [], [], [], []]
    ],
    
    "eZ": [
        ["landscape", 5, [], [], [], []], 
        ["nature", 5, [], [], [], []], 
        ["scenery", 5, [], [], [], []], 
        ["still life", 5, [], [], [], []], 
        ["cityscape", 5, [], [], [], []],
        ["forest", 4, [], [], [], []],
        ["beach", 4, [], [], [], []],
        ["mountain", 4, [], [], [], []],
        ["ocean", 4, [], [], [], []],
        ["sky", 4, [], [], [], []],
        ["night sky", 3, [], [], [], []],
        ["sunset", 4, [], [], [], []],
        ["indoor", 4, [], [], [], []],
        ["bedroom", 3, [], [], [], []],
        ["garden", 3, [], [], [], []],
        ["waterfall", 3, [], [], [], []],
        ["ruins", 3, [], [], [], []],
        ["lake", 3, [], [], [], []],
        ["alley", 7, [], [], [], []],
        ["basement", 7, [], [], [], []],
        ["appartment, window, couch", 7, [], [], [], []],
    ],
    
    "eU": [
        ["simple background", 10, [], [], [], []], 
        ["scenery", 100, [], [], [], []],
        ["detailed background", 10, [], [], [], []],
    ],
    
    "eJ": [
        ["portrait", 4, [], ["portrait_framing"], [], []], 
        ["upper body", 5, [], ["upper_body_framing"], [], []], 
        ["cowboy shot", 3, [], ["cowboy_shot_framing"], [], []], 
        ["full body", 4, [], ["full_body_framing","legs","feet"], [], []], 
        ["close-up", 1, [], ["close_up_framing"], [], []], 
        ["headshot", 3, [], [], [], []],
        ["waist up", 4, [], [], [], []],
        ["three-quarter view", 3, [], [], [], []],
        ["dynamic pose", 4, [], [], [], []],
        ["action shot", 3, [], [], [], []]
    ],
    
    "eG": [
        ["", 4, [], [], [], []]
    ],
    
    "e_dollar": [
        ["bat ears, bat wings", 5, [], ["ears", "wings"], [], []], 
        ["cat ears, cat tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["mermaid, scales", 5, [], ["nolegs", "nofeet", "scales", "tail", "mermaid_race"], ["female"], []], 
        ["centaur", 5, [], ["nolegs", "nofeet", "centaur_race"], [], []],
        ["lamia", 5, [], ["nolegs", "nofeet", "lamia_race"], [], []],
        ["orc", 5, [], ["orc_race"], [], []],
        ["elf, pointy ears", 5, [], ["ears", "pointy_ears", "elf_race"], [], []],
        ["fox ears, fox tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["wolf ears, wolf tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["dog ears, dog tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["rabbit ears, rabbit tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["horse ears, horse tail", 5, [], ["ears", "tail", "animal_ears", "animal_tail"], [], []],
        ["cow ears, cow tail, cow horns", 5, [], ["ears", "tail", "horns", "animal_ears", "animal_tail"], [], []],
        ["goat horns", 5, [], ["horns"], [], []],
        ["dragon wings, dragon tail", 5, [], ["wings", "tail", "dragon_race"], [], []],
        ["angel wings, halo", 5, [], ["wings", "halo", "angel_race"], [], []],
        ["demon horns, demon tail, demon wings", 5, [], ["horns", "tail", "wings", "demon_race"], [], []],
        ["harpy wings", 5, [], ["wings", "harpy_race"], [], []],
        ["lizard tail, scales", 5, [], ["tail", "scales", "lizard_race"], [], []],
        ["slime girl", 4, [], ["slime_race"], ["female"], []]
    ],
    
    "eq": [
        ["dark skin", 100, [], [], [], []], 
        ["pale skin", 200, [], [], [], []], 
        ["tan", 50, [], [], [], []],
        ["olive skin", 50, [], [], [], []],
        ["light skin", 150, [], [], [], []],
        ["medium skin", 100, [], [], [], []],
        ["very dark skin", 50, [], [], [], []],
        ["deep skin", 50, [], [], [], []],
        ["fair skin", 100, [], [], [], []],
        ["tanned lines", 30, [], [], [], []],
        ["flushed skin", 40, [], [], [], []],
        ["ruddy skin", 20, [], [], [], []],
        ["colored skin", 30, [], [], [], []],
        ["blue skin", 20, [], [], [], []],
        ["green skin", 20, [], [], [], []],
        ["purple skin", 20, [], [], [], []],
        ["red skin", 20, [], [], [], []],
        ["dirty skin", 20, [], [], [], []],
        ["bruised skin", 20, [], [], [], []],
        ["black skin", 50, [], [], [], []],
    ],
    
    "tm": [
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
        ["aqua eyes", 5, [], ["eyes"], [], []],
        ["amber eyes", 5, [], ["eyes"], [], []],
        ["violet eyes", 5, [], ["eyes"], [], []],
        ["hazel eyes", 5, [], ["eyes"], [], []],
        ["white eyes", 4, [], ["eyes"], [], []],
        ["multicolored eyes", 4, [], ["eyes"], [], []]
    ],
    
    "eY": [
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
    
    "eQ": [
        ["jitome", 5, [], [], ["eyes"], []], 
        ["tsurime", 5, [], [], ["eyes"], []],
        ["tareme", 5, [], [], ["eyes"], []],
        ["sanpaku", 5, [], [], ["eyes"], []],
        ["bedroom eyes", 5, [], [], ["eyes"], []],
        ["heavy-lidded eyes", 4, [], [], ["eyes"], []],
        ["bright eyes", 4, [], [], ["eyes"], []],
        ["droopy eyes", 4, [], [], ["eyes"], []],
        ["almond eyes", 4, [], [], ["eyes"], []],
        ["round eyes", 4, [], [], ["eyes"], []],
        ["lazy eyes", 3, [], [], ["eyes"], []],
        ["upturned eyes", 3, [], [], ["eyes"], []],
        ["downturned eyes", 3, [], [], ["eyes"], []],
        ["monolid", 3, [], [], ["eyes"], []],
        ["hooded eyes", 3, [], [], ["eyes"], []],
        ["empty eyes", 5, [], [], ["eyes"], []],
        ["sad eyes", 5, [], [], ["eyes"], []],
        ["confused eyes", 5, [], [], ["eyes"], []],
        ["deep-set eyes", 3, [], [], ["eyes"], []]
    ],
    
    "eY": [
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
        ["hair up", 4, [], ["hair"], [], []]
    ],
    
    "eK": [
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

    
    "tp": [
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

    "tu": [
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
    
    "e0": [
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

    
    "e1": [
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
    
    "e2": [
        ["flat chest", 10, [], ["breasts"], ["female"], []], 
        ["tiny breasts", 10, [], ["breasts"], ["female"], []], 
        ["small breasts", 10, [], ["breasts"], ["female"], []], 
        ["medium breasts", 10, [], ["breasts"], ["female"], []],
        ["large breasts", 5, [], ["breasts"], ["female"], []],
        ["huge breasts", 3, [], ["breasts"], ["female"], []],
        ["gigantic breasts", 2, [], ["breasts"], ["female"], []],
    ],
    
    "e5": [
        ["muscular", 2, [], ["muscled_physique"], [], []], 
        ["abs", 2, [], [], ["muscled_physique"], []], 
        ["mature female", 5, [], [], ["female"], []],
        ["mature male", 5, [], [], ["male"], []],
        ["tomboy", 10, [], [], ["female"], []],
        ["manly", 5, [], [], ["male"], []], 
        ["petite", 15, [], [], [], []],
        ["slim", 15, [], [], [], []],
        ["athletic", 3, [], [], [], []],
        ["skinny", 15, [], [], [], []],
        ["slender", 5, [], [], [], []],
        ["ribs", 3, [], [], [], []],
        ["lean build", 4, [], [], [], []],
        ["willowy", 3, [], [], [], []],
        ["defined hip bones", 2, [], [], [], []],
        ["dancer's build", 3, [], [], [], []],
        ["swimmer's build", 3, [], [], [], []],
        ["runner's build", 3, [], [], [], []],
        ["elegant posture", 3, [], [], [], []],
        ["good posture", 3, [], [], [], []],
        ["subtle muscle tone", 3, [], [], [], []],
    ],
    
    "e6": [
        ["baseball cap", 5, [], ["headwear"], [], []], 
        ["crown", 5, [], ["headwear"], [], []],
        ["hat", 5, [], ["headwear"], [], []],
        ["beret", 5, [], ["headwear"], [], []],
        ["witch hat", 5, [], ["headwear"], [], []],
        ["wide-brimmed hat", 4, [], ["headwear"], [], []],
        ["sun hat", 4, [], ["headwear"], [], []],
        ["cowboy hat", 4, [], ["headwear"], [], []],
        ["straw hat", 4, [], ["headwear"], [], []],
        ["peaked cap", 4, [], ["headwear"], [], []],
        ["garrison cap", 3, [], ["headwear"], [], []],
        ["sailor hat", 4, [], ["headwear"], [], []],
        ["beanie", 4, [], ["headwear"], [], []],
        ["helmet", 4, [], ["headwear"], [], []],
        ["mini hat", 3, [], ["headwear"], [], []],
        ["top hat", 3, [], ["headwear"], [], []],
        ["fur hat", 3, [], ["headwear"], [], []],
        ["santa hat", 3, [], ["headwear"], [], []],
        ["tiara", 4, [], ["headwear"], [], []],
        ["fedora", 3, [], ["headwear"], [], []],
        ["flat cap", 3, [], ["headwear"], [], []],
        ["headpiece", 4, [], ["headwear"], [], []],
        ["hood", 4, [], ["headwear"], [], []],
        ["visor cap", 3, [], ["headwear"], [], []],
        ["bowler hat", 3, [], ["headwear"], [], []],
        ["pillbox hat", 3, [], ["headwear"], [], []],
        ["cabbie hat", 3, [], ["headwear"], [], []],
        ["bucket hat", 4, [], ["headwear"], [], []],
        ["deerstalker", 2, [], ["headwear"], [], []],
        ["newsboy cap", 3, [], ["headwear"], [], []],
        ["pork pie hat", 2, [], ["headwear"], [], []],
        ["trilby", 3, [], ["headwear"], [], []],
        ["boater hat", 3, [], ["headwear"], [], []],
        ["panama hat", 3, [], ["headwear"], [], []],
        ["sombrero", 3, [], ["headwear"], [], []],
        ["winter hat", 4, [], ["headwear"], [], []],
        ["ushanka", 3, [], ["headwear"], [], []],
        ["trapper hat", 3, [], ["headwear"], [], []],
        ["cloche hat", 3, [], ["headwear"], [], []],
        ["fascinator", 3, [], ["headwear"], [], []],
        ["headscarf", 4, [], ["headwear"], [], []],
        ["bandana", 4, [], ["headwear"], [], []],
        ["turban", 3, [], ["headwear"], [], []],
        ["hijab", 3, [], ["headwear"], [], []],
        ["keffiyeh", 2, [], ["headwear"], [], []],
        ["military cap", 3, [], ["headwear"], [], []],
        ["officer's cap", 3, [], ["headwear"], [], []],
        ["police hat", 3, [], ["headwear"], [], []],
        ["chef hat", 3, [], ["headwear"], [], []],
        ["nurse cap", 3, [], ["headwear"], [], []],
        ["graduate cap", 3, [], ["headwear"], [], []],
        ["mortarboard", 3, [], ["headwear"], [], []],
        ["flower crown", 4, [], ["headwear"], [], []],
        ["laurel crown", 3, [], ["headwear"], [], []],
        ["circlet", 3, [], ["headwear"], [], []],
        ["diadem", 3, [], ["headwear"], [], []],
        ["combat helmet", 3, [], ["headwear"], [], []],
        ["medieval helmet", 3, [], ["headwear"], [], []],
        ["knight helmet", 3, [], ["headwear"], [], []],
        ["horned helmet", 3, [], ["headwear"], [], []],
        ["football helmet", 2, [], ["headwear"], [], []],
        ["bicycle helmet", 2, [], ["headwear"], [], []],
        ["motorcycle helmet", 2, [], ["headwear"], [], []],
        ["space helmet", 2, [], ["headwear"], [], []],
        ["jester hat", 3, [], ["headwear"], [], []],
        ["party hat", 3, [], ["headwear"], [], []],
        ["birthday hat", 3, [], ["headwear"], [], []],
        ["propeller cap", 2, [], ["headwear"], [], []],
        ["cat ear headband", 4, [], ["headwear"], [], []],
        ["bunny ear headband", 4, [], ["headwear"], [], []],
        ["fox ear headband", 3, [], ["headwear"], [], []],
        ["animal ear headband", 3, [], ["headwear"], [], []],
        ["headset", 4, [], ["headwear"], [], []],
        ["headphones", 4, [], ["headwear"], [], []],
        ["crown of thorns", 2, [], ["headwear"], [], []],
        ["bridal veil", 3, [], ["headwear"], [], []],
        ["wedding veil", 3, [], ["headwear"], [], []],
        ["face veil", 3, [], ["headwear"], [], []],
        ["bonnet", 3, [], ["headwear"], [], []],
        ["hennin", 2, [], ["headwear"], [], []],
        ["bishop's mitre", 2, [], ["headwear"], [], []],
        ["papal tiara", 2, [], ["headwear"], [], []],
        ["fez", 2, [], ["headwear"], [], []],
        ["balaclava", 2, [], ["headwear"], [], []],
        ["headwrap", 3, [], ["headwear"], [], []],
        ["earmuffs", 3, [], ["headwear"], [], []],
        ["ear covers", 3, [], ["headwear"], [], []],
        ["goggles on head", 3, [], ["headwear"], [], []],
        ["sunglasses on head", 3, [], ["headwear"], [], []],
        ["crown of flowers", 3, [], ["headwear"], [], []],
        ["head wreath", 3, [], ["headwear"], [], []]
    ],

    "e3": [
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

    "e4": [
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
    
    "e7": [
        ["cocktail dress", 5, [], [], ["female"], []], 
        ["kimono", 5, [], [], [], []],
        ["sundress", 5, [], [], ["female"], []],
        ["evening gown", 5, [], [], ["female"], []],
        ["yukata", 5, [], [], [], []],
        ["qipao", 5, [], [], ["female"], []],
        ["china dress", 5, [], [], ["female"], []],
        ["wedding dress", 4, [], [], ["female"], []],
        ["ball gown", 4, [], [], ["female"], []],
        ["summer dress", 5, [], [], ["female"], []],
        ["gothic lolita dress", 4, [], [], ["female"], []],
        ["sailor dress", 4, [], [], ["female"], []],
        ["sweater dress", 4, [], [], ["female"], []],
        ["pencil dress", 4, [], [], ["female"], []],
        ["pinafore dress", 4, [], [], ["female"], []],
        ["halter dress", 4, [], [], ["female"], []],
        ["strapless dress", 4, [], [], ["female"], []],
        ["frilled dress", 4, [], [], ["female"], []],
        ["pleated dress", 4, [], [], ["female"], []],
        ["layered dress", 4, [], [], ["female"], []],
        ["a-line dress", 5, [], [], ["female"], []],
        ["shift dress", 5, [], [], ["female"], []],
        ["wrap dress", 5, [], [], ["female"], []],
        ["bodycon dress", 5, [], [], ["female"], []],
        ["maxi dress", 5, [], [], ["female"], []],
        ["mini dress", 5, [], [], ["female"], []],
        ["midi dress", 5, [], [], ["female"], []],
        ["slip dress", 4, [], [], ["female"], []],
        ["empire dress", 4, [], [], ["female"], []],
        ["tea dress", 4, [], [], ["female"], []],
        ["shirt dress", 5, [], [], ["female"], []],
        ["peplum dress", 4, [], [], ["female"], []],
        ["off-shoulder dress", 5, [], [], ["female"], []],
        ["one-shoulder dress", 4, [], [], ["female"], []],
        ["backless dress", 4, [], [], ["female"], []],
        ["high-low dress", 4, [], [], ["female"], []],
        ["tulle dress", 4, [], [], ["female"], []],
        ["sheath dress", 4, [], [], ["female"], []],
        ["chiffon dress", 4, [], [], ["female"], []],
        ["satin dress", 4, [], [], ["female"], []],
        ["lace dress", 5, [], [], ["female"], []],
        ["velvet dress", 4, [], [], ["female"], []],
        ["leather dress", 3, [], [], ["female"], []],
        ["denim dress", 4, [], [], ["female"], []],
        ["knit dress", 4, [], [], ["female"], []],
        ["floral dress", 5, [], [], ["female"], []],
        ["polka dot dress", 4, [], [], ["female"], []],
        ["striped dress", 4, [], [], ["female"], []],
        ["plaid dress", 4, [], [], ["female"], []],
        ["checkered dress", 4, [], [], ["female"], []],
        ["sequin dress", 3, [], [], ["female"], []],
        ["embroidered dress", 4, [], [], ["female"], []],
        ["beaded dress", 3, [], [], ["female"], []],
        ["ruffled dress", 4, [], [], ["female"], []],
        ["tiered dress", 4, [], [], ["female"], []],
        ["drop waist dress", 3, [], [], ["female"], []],
        ["princess line dress", 4, [], [], ["female"], []],
        ["swing dress", 4, [], [], ["female"], []],
        ["dirndl", 3, [], [], ["female"], []],
        ["hanbok", 3, [], [], ["female"], []],
        ["ao dai", 3, [], [], ["female"], []],
        ["salwar kameez", 3, [], [], ["female"], []],
        ["saree", 3, [], [], ["female"], []],
        ["lehenga", 3, [], [], ["female"], []],
        ["kilt", 3, [], [], [], []],
        ["caftan", 3, [], [], ["female"], []],
        ["dashiki", 3, [], [], [], []],
        ["furisode", 4, [], [], ["female"], []],
        ["mermaid dress", 4, [], [], ["female"], []],
        ["trumpet dress", 3, [], [], ["female"], []],
        ["tent dress", 3, [], [], ["female"], []],
        ["babydoll dress", 4, [], [], ["female"], []],
        ["skater dress", 4, [], [], ["female"], []],
        ["prairie dress", 3, [], [], ["female"], []],
        ["smock dress", 3, [], [], ["female"], []],
        ["blazer dress", 4, [], [], ["female"], []],
        ["jumper dress", 4, [], [], ["female"], []],
        ["cape dress", 3, [], [], ["female"], []],
        ["coat dress", 4, [], [], ["female"], []],
        ["corset dress", 4, [], [], ["female"], []],
        ["halterneck dress", 4, [], [], ["female"], []],
        ["cowl neck dress", 3, [], [], ["female"], []],
        ["v-neck dress", 4, [], [], ["female"], []],
        ["square neck dress", 3, [], [], ["female"], []],
        ["boat neck dress", 3, [], [], ["female"], []],
        ["collared dress", 4, [], [], ["female"], []],
        ["turtleneck dress", 4, [], [], ["female"], []],
        ["mock neck dress", 3, [], [], ["female"], []],
        ["sleeveless dress", 4, [], [], ["female"], []],
        ["cap sleeve dress", 3, [], [], ["female"], []],
        ["short sleeve dress", 4, [], [], ["female"], []],
        ["three-quarter sleeve dress", 4, [], [], ["female"], []],
        ["long sleeve dress", 4, [], [], ["female"], []],
        ["bell sleeve dress", 3, [], [], ["female"], []],
        ["puff sleeve dress", 4, [], [], ["female"], []],
        ["dolman sleeve dress", 3, [], [], ["female"], []],
        ["raglan sleeve dress", 3, [], [], ["female"], []],
        ["flutter sleeve dress", 3, [], [], ["female"], []],
        ["kimono sleeve dress", 3, [], [], ["female"], []],
        ["cold shoulder dress", 4, [], [], ["female"], []],
        ["cutout dress", 4, [], [], ["female"], []],
        ["handkerchief dress", 3, [], [], ["female"], []],
        ["bubble dress", 3, [], [], ["female"], []],
        ["blouson dress", 3, [], [], ["female"], []],
        ["trapeze dress", 3, [], [], ["female"], []],
        ["t-shirt dress", 4, [], [], ["female"], []],
        ["polo dress", 3, [], [], ["female"], []],
        ["hoodie dress", 4, [], [], ["female"], []],
        ["pajama dress", 3, [], [], ["female"], []],
        ["beach dress", 4, [], [], ["female"], []],
        ["kaftan", 3, [], [], ["female"], []],
        ["tunic dress", 4, [], [], ["female"], []],
        ["housedress", 3, [], [], ["female"], []],
        ["nightgown", 4, [], [], ["female"], []],
        ["negligee", 3, [], [], ["female"], []],
        ["victorian dress", 3, [], [], ["female"], []],
        ["edwardian dress", 3, [], [], ["female"], []],
        ["regency dress", 3, [], [], ["female"], []],
        ["1920s flapper dress", 3, [], [], ["female"], []],
        ["1950s dress", 4, [], [], ["female"], []],
        ["1960s mod dress", 3, [], [], ["female"], []],
        ["1970s maxi dress", 3, [], [], ["female"], []],
        ["1980s power dress", 3, [], [], ["female"], []],
        ["punk dress", 3, [], [], ["female"], []],
        ["grunge dress", 3, [], [], ["female"], []],
        ["hippie dress", 3, [], [], ["female"], []],
        ["steampunk dress", 3, [], [], ["female"], []],
        ["cyberpunk dress", 3, [], [], ["female"], []],
        ["cottagecore dress", 4, [], [], ["female"], []],
        ["casual dress", 5, [], [], ["female"], []],
        ["formal dress", 5, [], [], ["female"], []],
        ["office dress", 4, [], [], ["female"], []],
        ["party dress", 5, [], [], ["female"], []],
        ["prom dress", 4, [], [], ["female"], []],
        ["graduation dress", 3, [], [], ["female"], []],
        ["bridesmaids dress", 3, [], [], ["female"], []],
        ["funeral dress", 2, [], [], ["female"], []],
    ],

    "eX": [
        ["heterochromia", 5, [], [], ["eyes"], []], 
        ["glowing eyes", 5, [], [], ["eyes"], []],
        ["pupil-less", 4, [], [], ["eyes"], []],
        ["slit pupils", 4, [], [], ["eyes"], []],
        ["star-shaped pupils", 4, [], [], ["eyes"], []],
        ["heart-shaped pupils", 4, [], [], ["eyes"], []],
        ["symbol-shaped pupils", 4, [], [], ["eyes"], []],
        ["closed eyes", 4, [], [], ["eyes"], []],
        ["half-closed eyes", 4, [], [], ["eyes"], []],
        ["narrowed eyes", 4, [], [], ["eyes"], []],
        ["wide eyes", 4, [], [], ["eyes"], []],
        ["empty eyes", 3, [], [], ["eyes"], []],
        ["sparkling eyes", 4, [], [], ["eyes"], []],
        ["constricted pupils", 3, [], [], ["eyes"], []],
        ["ringed eyes", 3, [], [], ["eyes"], []],
        ["multicolored pupils", 3, [], [], ["eyes"], []]
    ],

    "e8": [
        ["socks", 5, [], ["legwear"], ["feet"], []], 
        ["thighhighs", 5, [], ["legwear"], ["female","legs"], []],
        ["pantyhose", 5, [], ["legwear"], ["female"], []],
        ["kneehighs", 5, [], ["legwear"], ["female"], []],
        ["stockings", 5, [], ["legwear"], ["female"], []],
        ["tabi", 3, [], ["legwear"], [], []],
        ["fishnets", 4, [], ["legwear"], ["female"], []],
        ["loose socks", 3, [], ["legwear"], ["female"], []],
        ["bobby socks", 3, [], ["legwear"], ["female"], []],
        ["ankle socks", 4, [], ["legwear"], [], []],
        ["crew socks", 4, [], ["legwear"], [], []],
        ["knee socks", 4, [], ["legwear"], [], []],
        ["over-kneehighs", 4, [], ["legwear"], ["female"], []],
        ["fishnet thighhighs", 3, [], ["legwear"], ["female"], []],
        ["ribbed legwear", 3, [], ["legwear"], [], []],
        ["single thighhigh", 3, [], ["legwear"], ["female"], []],
        ["toeless legwear", 3, [], ["legwear"], [], []],
        ["striped legwear", 4, [], ["legwear"], [], []]
    ],
    
    "e9": [
        ["fishnet legwear", 5, [], [], ["legwear"], []], 
        ["bow legwear", 5, [], [], ["legwear", "female"], []],
        ["frilled legwear", 5, [], [], ["legwear"], []],
        ["lace-trimmed legwear", 5, [], [], ["legwear"], []],
        ["polka-dot legwear", 4, [], [], ["legwear"], []],
        ["striped legwear", 4, [], [], ["legwear"], []],
        ["heart print legwear", 3, [], [], ["legwear"], []],
        ["star print legwear", 3, [], [], ["legwear"], []],
        ["animal print legwear", 3, [], [], ["legwear"], []],
        ["patterned legwear", 4, [], [], ["legwear"], []],
        ["ripped legwear", 3, [], [], ["legwear"], []],
        ["floral print legwear", 3, [], [], ["legwear"], []],
        ["ribbed legwear", 3, [], [], ["legwear"], []],
        ["argyle legwear", 3, [], [], ["legwear"], []],
        ["checkered legwear", 3, [], [], ["legwear"], []],
        ["seamed legwear", 3, [], [], ["legwear"], []]
    ],
    
    "te": [
        ["blouse", 5, [], [], [], []], 
        ["hoodie", 5, [], [], [], []], 
        ["virgin killer sweater", 5, [], [], ["female"],[]],
        ["t-shirt", 5, [], [], [], []],
        ["tank top", 5, [], [], [], []],
        ["turtleneck", 5, [], [], [], []],
        ["crop top", 5, [], [], ["female"], []],
        ["cardigan", 5, [], [], [], []],
        ["sweater", 5, [], [], [], []],
        ["vest", 5, [], [], [], []],
        ["dress shirt", 5, [], [], [], []],
        ["jacket", 5, [], [], [], []],
        ["tube top", 4, [], [], ["female"], []],
        ["halter top", 4, [], [], ["female"], []],
        ["off-shoulder top", 4, [], [], ["female"], []],
        ["camisole", 4, [], [], ["female"], []],
        ["ribbed sweater", 4, [], [], [], []],
        ["turtleneck sweater", 4, [], [], [], []],
        ["button-up shirt", 4, [], [], [], []],
        ["polo shirt", 4, [], [], [], []],
        ["collared shirt", 5, [], [], [], []],
        ["sleeveless shirt", 5, [], [], [], []],
        ["sweatshirt", 5, [], [], [], []],
        ["pullover", 5, [], [], [], []],
        ["v-neck shirt", 5, [], [], [], []],
        ["henley shirt", 4, [], [], [], []],
        ["raglan shirt", 4, [], [], [], []],
        ["jersey", 4, [], [], [], []],
        ["tunic", 4, [], [], [], []],
        ["muscle shirt", 4, [], [], ["male"], []],
        ["blazer", 4, [], [], [], []],
        ["suit jacket", 4, [], [], [], []],
        ["bomber jacket", 4, [], [], [], []],
        ["windbreaker", 4, [], [], [], []],
        ["leather jacket", 4, [], [], [], []],
        ["denim jacket", 4, [], [], [], []],
        ["puffer jacket", 4, [], [], [], []],
        ["track jacket", 4, [], [], [], []],
        ["varsity jacket", 4, [], [], [], []],
        ["bolero jacket", 3, [], [], ["female"], []],
        ["cropped jacket", 3, [], [], [], []],
        ["tailcoat", 3, [], [], [], []],
        ["peacoat", 3, [], [], [], []],
        ["trenchcoat", 3, [], [], [], []],
        ["parka", 3, [], [], [], []],
        ["anorak", 3, [], [], [], []],
        ["cape", 3, [], [], [], []],
        ["waistcoat", 3, [], [], [], []],
        ["bustier", 3, [], [], ["female"], []],
        ["corset", 3, [], [], ["female"], []],
        ["bandeau top", 3, [], [], ["female"], []],
        ["bralette", 3, [], [], ["female"], []],
        ["bodysuit top", 3, [], [], ["female"], []],
        ["strapless top", 3, [], [], ["female"], []],
        ["peplum top", 3, [], [], ["female"], []],
        ["wrap top", 3, [], [], ["female"], []],
        ["cold shoulder top", 3, [], [], ["female"], []],
        ["bardot top", 3, [], [], ["female"], []],
        ["kimono top", 3, [], [], [], []],
        ["tie-front top", 3, [], [], ["female"], []],
        ["smock top", 3, [], [], [], []],
        ["mandarin collar shirt", 3, [], [], [], []],
        ["tuxedo shirt", 3, [], [], [], []],
        ["hawaiian shirt", 3, [], [], [], []],
        ["flannel shirt", 4, [], [], [], []],
        ["peasant blouse", 3, [], [], ["female"], []],
        ["silk blouse", 3, [], [], ["female"], []],
        ["chiffon blouse", 3, [], [], ["female"], []],
        ["poet blouse", 2, [], [], ["female"], []],
        ["sailor top", 3, [], [], [], []],
        ["mock neck top", 3, [], [], [], []],
        ["cowl neck top", 3, [], [], [], []],
        ["boat neck top", 3, [], [], [], []],
        ["scoop neck top", 3, [], [], [], []],
        ["crew neck shirt", 3, [], [], [], []],
        ["long sleeve shirt", 4, [], [], [], []],
        ["short sleeve shirt", 4, [], [], [], []],
        ["three-quarter sleeve shirt", 3, [], [], [], []],
        ["sleeveless turtleneck", 3, [], [], [], []],
        ["aran sweater", 3, [], [], [], []],
        ["cable knit sweater", 3, [], [], [], []],
        ["cashmere sweater", 3, [], [], [], []],
        ["oversized sweater", 4, [], [], [], []],
        ["sweater vest", 3, [], [], [], []],
        ["cropped sweater", 3, [], [], ["female"], []],
        ["graphic tee", 4, [], [], [], []],
        ["striped shirt", 4, [], [], [], []],
        ["printed shirt", 4, [], [], [], []],
        ["band shirt", 3, [], [], [], []],
        ["uniform shirt", 3, [], [], [], []],
        ["chef's jacket", 2, [], [], [], []],
        ["lab coat", 3, [], [], [], []],
        ["utility vest", 3, [], [], [], []],
        ["down vest", 3, [], [], [], []],
        ["fur vest", 2, [], [], [], []],
        ["quilted vest", 2, [], [], [], []],
        ["shrug", 2, [], [], ["female"], []],
        ["poncho", 2, [], [], [], []]
    ],

    "tt": [
        ["pants", 5, [], [], [], []], 
        ["shorts", 5, [], [], [], []], 
        ["short shorts", 8, [], [], ["female"], []],
        ["miniskirt", 5, [], [], ["female"], []],
        ["pleated skirt", 5, [], [], ["female"], []],
        ["jeans", 5, [], [], [], []],
        ["leggings", 5, [], [], [], []],
        ["trousers", 5, [], [], [], []],
        ["capri pants", 4, [], [], [], []],
        ["bike shorts", 4, [], [], [], []],
        ["denim shorts", 4, [], [], [], []],
        ["cargo pants", 4, [], [], [], []],
        ["sweatpants", 4, [], [], [], []],
        ["pencil skirt", 4, [], [], ["female"], []],
        ["microskirt", 3, [], [], ["female"], []],
        ["long skirt", 4, [], [], ["female"], []],
        ["a-line skirt", 4, [], [], ["female"], []],
        ["circle skirt", 4, [], [], ["female"], []],
        ["midi skirt", 4, [], [], ["female"], []],
        ["skirt set", 4, [], [], ["female"], []],
        ["tennis skirt", 3, [], [], ["female"], []],
        ["skinny jeans", 4, [], [], [], []],
        ["bootcut jeans", 4, [], [], [], []],
        ["wide-leg jeans", 4, [], [], [], []],
        ["boyfriend jeans", 4, [], [], ["female"], []],
        ["mom jeans", 4, [], [], ["female"], []],
        ["high-waisted jeans", 4, [], [], [], []],
        ["low-rise jeans", 4, [], [], [], []],
        ["distressed jeans", 4, [], [], [], []],
        ["ripped jeans", 4, [], [], [], []],
        ["straight-leg pants", 4, [], [], [], []],
        ["baggy pants", 4, [], [], [], []],
        ["fitted pants", 4, [], [], [], []],
        ["wide-leg pants", 4, [], [], [], []],
        ["culottes", 3, [], [], ["female"], []],
        ["palazzo pants", 3, [], [], ["female"], []],
        ["harem pants", 3, [], [], [], []],
        ["joggers", 4, [], [], [], []],
        ["track pants", 4, [], [], [], []],
        ["slacks", 4, [], [], [], []],
        ["dress pants", 4, [], [], [], []],
        ["chinos", 4, [], [], [], []],
        ["khakis", 4, [], [], [], []],
        ["corduroys", 3, [], [], [], []],
        ["leather pants", 3, [], [], [], []],
        ["jeggings", 3, [], [], ["female"], []],
        ["yoga pants", 3, [], [], ["female"], []],
        ["cigarette pants", 3, [], [], [], []],
        ["bell bottoms", 3, [], [], [], []],
        ["flared pants", 3, [], [], [], []],
        ["paper bag pants", 3, [], [], ["female"], []],
        ["bermuda shorts", 3, [], [], [], []],
        ["cargo shorts", 3, [], [], [], []],
        ["board shorts", 3, [], [], [], []],
        ["running shorts", 3, [], [], [], []],
        ["cutoffs", 3, [], [], [], []],
        ["jean shorts", 3, [], [], [], []],
        ["chino shorts", 3, [], [], [], []],
        ["high-waisted shorts", 3, [], [], ["female"], []],
        ["dolphin shorts", 3, [], [], ["female"], []],
        ["skorts", 3, [], [], ["female"], []],
        ["culotte shorts", 2, [], [], ["female"], []],
        ["bubble shorts", 2, [], [], [], []],
        ["bloomers", 3, [], [], ["female"], []],
        ["buruma", 3, [], [], ["female"], []],
        ["high-waisted skirt", 3, [], [], ["female"], []],
        ["pencil skirt", 3, [], [], ["female"], []],
        ["bubble skirt", 3, [], [], ["female"], []],
        ["wrap skirt", 3, [], [], ["female"], []],
        ["asymmetrical skirt", 3, [], [], ["female"], []],
        ["tiered skirt", 3, [], [], ["female"], []],
        ["layered skirt", 3, [], [], ["female"], []],
        ["flared skirt", 3, [], [], ["female"], []],
        ["tulip skirt", 3, [], [], ["female"], []],
        ["peplum skirt", 3, [], [], ["female"], []],
        ["fishtail skirt", 2, [], [], ["female"], []],
        ["high-low skirt", 2, [], [], ["female"], []],
        ["maxi skirt", 2, [], [], ["female"], []],
        ["denim skirt", 3, [], [], ["female"], []],
        ["leather skirt", 3, [], [], ["female"], []],
        ["tulle skirt", 3, [], [], ["female"], []],
        ["tartan skirt", 3, [], [], ["female"], []],
        ["plaid skirt", 3, [], [], ["female"], []],
        ["pleather pants", 2, [], [], [], []],
        ["side-split skirt", 3, [], [], ["female"], []],
        ["pinafore skirt", 3, [], [], ["female"], []],
        ["suspender skirt", 3, [], [], ["female"], []],
        ["kilt", 2, [], [], [], []],
        ["sarong", 2, [], [], ["female"], []],
        ["overskirt", 2, [], [], ["female"], []],
        ["pelvic curtain", 2, [], [], ["female"], []],
        ["hakama", 3, [], [], [], []],
        ["culottes", 2, [], [], ["female"], []]
    ],
    
    "ta": [
        ["boots", 5, [], ["footwear"], ["feet"], []], 
        ["high heels", 5, [], ["footwear"], ["female","feet"], []],
        ["sneakers", 5, [], ["footwear"], ["feet"], []],
        ["sandals", 5, [], ["footwear"], ["feet"], []],
        ["loafers", 5, [], ["footwear"], ["feet"], []],
        ["mary janes", 5, [], ["footwear"], ["female","feet"], []],
        ["pumps", 4, [], ["footwear"], ["female","feet"], []],
        ["ankle boots", 4, [], ["footwear"], ["feet"], []],
        ["knee boots", 4, [], ["footwear"], ["feet"], []],
        ["thigh boots", 4, [], ["footwear"], ["feet"], []],
        ["platform shoes", 3, [], ["footwear"], ["feet"], []],
        ["geta", 3, [], ["footwear"], ["feet"], []],
        ["flip-flops", 3, [], ["footwear"], ["feet"], []],
        ["ballet flats", 3, [], ["footwear"], ["female","feet"], []],
        ["slippers", 4, [], ["footwear"], ["feet"], []],
        ["barefoot", 4, [], [], ["feet"], []],
        ["stilettos", 3, [], ["footwear"], ["female","feet"], []],
        ["combat boots", 3, [], ["footwear"], ["feet"], []],
        ["leather boots", 3, [], ["footwear"], ["feet"], []],
        ["oxford shoes", 3, [], ["footwear"], ["feet"], []]
    ],
    
    "ti": [
        ["school uniform", 10, [], [], [], []], 
        ["maid", 5, [], [], ["female"], []],
        ["nurse", 4, [], [], ["female"], []],
        ["police uniform", 4, [], [], [], []],
        ["military uniform", 4, [], [], [], []],
        ["sailor uniform", 4, [], [], [], []],
        ["serafuku", 5, [], [], ["female"], []],
        ["gym uniform", 4, [], [], [], []],
        ["cheerleader", 4, [], [], ["female"], []],
        ["butler", 4, [], [], ["male"], []],
        ["waitress", 4, [], [], ["female"], []],
        ["office lady", 4, [], [], ["female"], []],
        ["idol", 4, [], [], [], []],
        ["witch", 4, [], [], ["female"], []],
        ["nun", 3, [], [], ["female"], []],
        ["priest", 3, [], [], ["male"], []],
        ["doctor", 4, [], [], [], []],
        ["chef", 3, [], [], [], []],
        ["firefighter", 3, [], [], [], []],
        ["pilot", 3, [], [], [], []],
        ["flight attendant", 4, [], [], [], []],
        ["shrine maiden", 4, [], [], ["female"], []],
        ["miko", 4, [], [], ["female"], []],
        ["samurai", 4, [], [], [], []],
        ["ninja", 4, [], [], [], []],
        ["knight", 4, [], [], [], []],
        ["wizard", 4, [], [], [], []],
        ["astronaut", 3, [], [], [], []],
        ["pirate", 4, [], [], [], []],
        ["cowboy", 3, [], [], ["male"], []],
        ["cowgirl", 3, [], [], ["female"], []],
        ["waiter", 3, [], [], ["male"], []],
        ["bartender", 3, [], [], [], []],
        ["scientist", 3, [], [], [], []],
        ["lab coat", 4, [], [], [], []],
        ["martial artist", 3, [], [], [], []],
        ["gi", 3, [], [], [], []],
        ["karategi", 3, [], [], [], []],
        ["judogi", 3, [], [], [], []],
        ["hakama", 4, [], [], [], []],
        ["kimono uniform", 4, [], [], [], []],
        ["race queen", 3, [], [], ["female"], []],
        ["race car driver", 3, [], [], [], []],
        ["mechanic", 3, [], [], [], []],
        ["construction worker", 2, [], [], [], []],
        ["gardener", 2, [], [], [], []],
        ["farmhand", 2, [], [], [], []],
        ["conductor", 3, [], [], [], []],
        ["magician", 3, [], [], [], []],
        ["magical girl", 4, [], [], ["female"], []],
        ["superhero", 4, [], [], [], []],
        ["police officer", 4, [], [], [], []],
        ["detective", 3, [], [], [], []],
        ["security guard", 3, [], [], [], []],
        ["postal worker", 2, [], [], [], []],
        ["delivery person", 2, [], [], [], []],
        ["professor", 3, [], [], [], []],
        ["teacher", 4, [], [], [], []],
        ["student", 5, [], [], [], []],
        ["high school student", 5, [], [], [], []],
        ["middle school student", 5, [], [], [], []],
        ["elementary school student", 4, [], [], [], []],
        ["college student", 4, [], [], [], []],
        ["graduate student", 3, [], [], [], []],
        ["librarian", 3, [], [], [], []],
        ["archaeologist", 2, [], [], [], []],
        ["explorer", 3, [], [], [], []],
        ["adventurer", 3, [], [], [], []],
        ["businessman", 3, [], [], ["male"], []],
        ["businesswoman", 3, [], [], ["female"], []],
        ["office worker", 4, [], [], [], []],
        ["executive", 3, [], [], [], []],
        ["secretary", 3, [], [], [], []],
        ["receptionist", 3, [], [], [], []],
        ["banker", 2, [], [], [], []],
        ["accountant", 2, [], [], [], []],
        ["lawyer", 3, [], [], [], []],
        ["judge", 3, [], [], [], []],
        ["reporter", 3, [], [], [], []],
        ["photographer", 3, [], [], [], []],
        ["journalist", 3, [], [], [], []],
        ["artist", 3, [], [], [], []],
        ["painter", 3, [], [], [], []],
        ["sculptor", 2, [], [], [], []],
        ["musician", 3, [], [], [], []],
        ["rockstar", 3, [], [], [], []],
        ["popstar", 3, [], [], [], []],
        ["dancer", 3, [], [], [], []],
        ["ballet dancer", 3, [], [], [], []],
        ["figure skater", 3, [], [], [], []],
        ["gymnast", 3, [], [], [], []],
        ["swimmer", 3, [], [], [], []],
        ["diver", 2, [], [], [], []],
        ["surfer", 2, [], [], [], []],
        ["skier", 2, [], [], [], []],
        ["snowboarder", 2, [], [], [], []],
        ["athlete", 3, [], [], [], []],
        ["tennis player", 3, [], [], [], []],
        ["baseball player", 3, [], [], [], []],
        ["basketball player", 3, [], [], [], []],
        ["soccer player", 3, [], [], [], []],
        ["football player", 3, [], [], [], []],
        ["hockey player", 2, [], [], [], []],
        ["volleyball player", 3, [], [], [], []],
        ["track and field athlete", 2, [], [], [], []],
        ["hiker", 2, [], [], [], []],
        ["mountain climber", 2, [], [], [], []],
        ["fisher", 2, [], [], [], []],
        ["hunter", 2, [], [], [], []],
        ["ranger", 3, [], [], [], []],
        ["lifeguard", 3, [], [], [], []],
        ["coast guard", 2, [], [], [], []],
        ["sailor", 3, [], [], [], []],
        ["captain", 3, [], [], [], []],
        ["first mate", 2, [], [], [], []],
        ["navigator", 2, [], [], [], []],
        ["engineer", 3, [], [], [], []],
        ["architect", 2, [], [], [], []],
        ["designer", 3, [], [], [], []],
        ["fashion designer", 3, [], [], [], []],
        ["model", 3, [], [], [], []],
        ["fashion model", 3, [], [], [], []],
        ["hairdresser", 2, [], [], [], []],
        ["stylist", 2, [], [], [], []],
        ["makeup artist", 2, [], [], [], []],
        ["barber", 2, [], [], ["male"], []],
        ["server", 3, [], [], [], []],
        ["host", 3, [], [], ["male"], []],
        ["hostess", 3, [], [], ["female"], []],
        ["barista", 3, [], [], [], []],
        ["baker", 2, [], [], [], []],
        ["pastry chef", 2, [], [], [], []],
        ["butcher", 2, [], [], [], []],
        ["sushi chef", 2, [], [], [], []],
        ["head chef", 2, [], [], [], []],
        ["sous chef", 2, [], [], [], []],
        ["line cook", 2, [], [], [], []],
        ["fast food worker", 2, [], [], [], []],
        ["paramedic", 3, [], [], [], []],
        ["EMT", 3, [], [], [], []],
        ["surgeon", 3, [], [], [], []],
        ["pharmacist", 2, [], [], [], []],
        ["dentist", 2, [], [], [], []],
        ["veterinarian", 2, [], [], [], []],
        ["zookeeper", 2, [], [], [], []],
        ["pet groomer", 2, [], [], [], []],
        ["dog walker", 2, [], [], [], []],
        ["fortune teller", 3, [], [], [], []],
        ["clown", 2, [], [], [], []],
        ["jester", 2, [], [], [], []],
        ["ringmaster", 2, [], [], [], []],
        ["acrobat", 2, [], [], [], []],
        ["mime", 2, [], [], [], []],
        ["tour guide", 2, [], [], [], []],
        ["hotel staff", 2, [], [], [], []],
        ["bellhop", 2, [], [], [], []],
        ["concierge", 2, [], [], [], []],
        ["housekeeping", 2, [], [], [], []],
        ["janitor", 2, [], [], [], []],
        ["cleaner", 2, [], [], [], []],
        ["mechanic", 3, [], [], [], []],
        ["technician", 2, [], [], [], []],
        ["electrician", 2, [], [], [], []],
        ["plumber", 2, [], [], [], []],
        ["carpenter", 2, [], [], [], []],
        ["painter (worker)", 2, [], [], [], []],
        ["factory worker", 2, [], [], [], []],
        ["miner", 2, [], [], [], []],
        ["lumberjack", 2, [], [], [], []],
        ["fisherman", 2, [], [], [], []],
        ["farmer", 2, [], [], [], []],
        ["rancher", 2, [], [], [], []],
        ["shepherd", 2, [], [], [], []],
        ["beekeeper", 2, [], [], [], []],
        ["florist", 2, [], [], [], []],
        ["historian", 2, [], [], [], []],
        ["curator", 2, [], [], [], []],
        ["museum guide", 2, [], [], [], []],
        ["ambassador", 2, [], [], [], []],
        ["diplomat", 2, [], [], [], []],
        ["politician", 2, [], [], [], []],
        ["mayor", 2, [], [], [], []],
        ["governor", 2, [], [], [], []],
        ["president", 2, [], [], [], []],
        ["prime minister", 2, [], [], [], []],
        ["king", 2, [], [], ["male"], []],
        ["queen", 2, [], [], ["female"], []],
        ["prince", 2, [], [], ["male"], []],
        ["princess", 2, [], [], ["female"], []],
        ["royal guard", 2, [], [], [], []],
        ["palace guard", 2, [], [], [], []],
        ["royal advisor", 2, [], [], [], []],
        ["emperor", 2, [], [], ["male"], []],
        ["empress", 2, [], [], ["female"], []],
        ["gladiator", 2, [], [], [], []],
        ["monk", 2, [], [], ["male"], []],
        ["priest", 2, [], [], ["male"], []],
        ["bishop", 2, [], [], ["male"], []],
        ["cardinal", 2, [], [], ["male"], []],
        ["pope", 2, [], [], ["male"], []],
        ["priestess", 2, [], [], ["female"], []],
        ["high priestess", 2, [], [], ["female"], []],
        ["oracle", 2, [], [], [], []],
        ["shaman", 2, [], [], [], []],
        ["druid", 2, [], [], [], []],
        ["healer", 2, [], [], [], []],
        ["alchemist", 2, [], [], [], []],
    ],
    
    "ts": [
        ["bodysuit", 5, [], [], [], []], 
        ["leotard", 5, [], [], ["female"], []],
        ["plugsuit", 4, [], [], [], []],
        ["zentai", 3, [], [], [], []],
        ["wetsuit", 4, [], [], [], []],
        ["spacesuit", 3, [], [], [], []],
        ["latex bodysuit", 3, [], [], [], []],
        ["catsuit", 3, [], [], [], []],
        ["racing suit", 3, [], [], [], []],
        ["superhero costume", 3, [], [], [], []],
        ["high-leg leotard", 3, [], [], ["female"], []],
        ["high-leg bodysuit", 3, [], [], [], []],
        ["tights", 4, [], [], [], []],
        ["jumpsuit", 4, [], [], [], []],
        ["romper", 3, [], [], ["female"], []],
        ["overalls", 4, [], [], [], []],
        ["hazmat suit", 2, [], [], [], []],
        ["armor bodysuit", 3, [], [], [], []]
    ],

    "underwear": [
        ["underwear, plain white bra and panties", 5, [], [], ["female"], []],
        ["underwear, lingerie set", 5, [], [], ["female"], []],
        ["underwear, lace-trimmed underwear", 5, [], [], ["female"], []],
        ["underwear, sports bra", 5, [], [], ["female"], []],
        ["underwear, boxer briefs", 5, [], [], ["male"], []],
        ["underwear, boxer shorts", 5, [], [], ["male"], []],
        ["underwear, boxer briefs and bra", 5, [], [], ["female"], []],
        ["underwear, boxer shorts and bra", 5, [], [], ["female"], []],
        ["underwear, briefs", 5, [], [], ["male"], []],
        ["underwear, boyshorts", 4, [], [], ["female"], []],
        ["underwear, high-waisted panties and bra", 4, [], [], ["female"], []],
        ["underwear, cotton underwear and bra", 4, [], [], ["female"], []],
        ["underwear, matching bra and panties", 4, [], [], ["female"], []],
        ["underwear, floral print underwear", 3, [], [], ["female"], []],
        ["underwear, triangle bra and underwear", 3, [], [], ["female"], []],
        ["underwear, wireless bra and underwear", 3, [], [], ["female"], []],
    ],
    
    "tr": [
        ["swimsuit", 5, [], [], [], []], 
        ["bikini", 5, [], [], ["female"], []],
        ["one-piece swimsuit", 5, [], [], ["female"], []],
        ["school swimsuit", 4, [], [], ["female"], []],
        ["competition swimsuit", 4, [], [], [], []],
        ["sports swimsuit", 4, [], [], [], []],
        ["side-tie bikini", 4, [], [], ["female"], []],
        ["string bikini", 4, [], [], ["female"], []],
        ["micro bikini", 3, [], [], ["female"], []],
        ["front-tie bikini", 3, [], [], ["female"], []],
        ["frilled bikini", 3, [], [], ["female"], []],
        ["sling bikini", 3, [], [], ["female"], []],
        ["highleg swimsuit", 3, [], [], ["female"], []],
        ["v-shaped swimsuit", 3, [], [], ["female"], []],
        ["tankini", 3, [], [], ["female"], []],
        ["swim trunks", 4, [], [], ["male"], []],
        ["swim briefs", 3, [], [], ["male"], []],
        ["wetsuit", 3, [], [], [], []]
    ],
    
    "tn": [
        ["necklace", 5, [], [], [], []], 
        ["glasses", 5, [], [], [], []], 
        ["earrings", 5, [], [], ["female"], []],
        ["bracelet", 5, [], [], [], []],
        ["watch", 5, [], [], [], []],
        ["ring", 5, [], [], [], []],
        ["choker", 5, [], [], [], []],
        ["pendant", 4, [], [], [], []],
        ["anklet", 4, [], [], [], []],
        ["sunglasses", 4, [], [], [], []],
        ["belt", 4, [], [], [], []],
        ["armband", 4, [], [], [], []],
        ["bandana", 4, [], [], [], []],
        ["wristband", 4, [], [], [], []],
        ["ribbon choker", 4, [], [], [], []],
        ["bell collar", 3, [], [], [], []],
        ["spiked collar", 3, [], [], [], []],
        ["tiara", 3, [], [], [], []],
        ["crown", 3, [], [], [], []],
        ["bangle", 3, [], [], [], []],
        ["hair ties", 4, [], [], [], []],
        ["brooch", 4, [], [], [], []],
        ["medal", 3, [], [], [], []],
        ["eye mask", 3, [], [], [], []],
        ["tied up", 10, [], [], [], []],
        ["bondage", 10, [], [], [], []],
        ["chained up", 10, [], [], [], []],
        ["hands tied", 10, [], [], [], []],
        ["rope around neck", 5, [], [], [], []],
        ["pearl necklace", 4, [], [], [], []],
        ["diamond necklace", 4, [], [], [], []],
        ["gold necklace", 4, [], [], [], []],
        ["silver necklace", 4, [], [], [], []],
        ["locket", 4, [], [], [], []],
        ["heart pendant", 4, [], [], [], []],
        ["cross pendant", 4, [], [], [], []],
        ["star pendant", 4, [], [], [], []],
        ["charm bracelet", 4, [], [], [], []],
        ["tennis bracelet", 3, [], [], [], []],
        ["cuff bracelet", 3, [], [], [], []],
        ["friendship bracelet", 3, [], [], [], []],
        ["beaded bracelet", 4, [], [], [], []],
        ["leather bracelet", 4, [], [], [], []],
        ["analog watch", 4, [], [], [], []],
        ["digital watch", 4, [], [], [], []],
        ["smart watch", 4, [], [], [], []],
        ["pocket watch", 3, [], [], [], []],
        ["wedding ring", 4, [], [], [], []],
        ["engagement ring", 4, [], [], [], []],
        ["signet ring", 3, [], [], [], []],
        ["cocktail ring", 3, [], [], ["female"], []],
        ["promise ring", 3, [], [], [], []],
        ["mood ring", 2, [], [], [], []],
        ["thumb ring", 3, [], [], [], []],
        ["multiple rings", 3, [], [], [], []],
        ["gem ring", 3, [], [], [], []],
        ["band ring", 3, [], [], [], []],
        ["velvet choker", 3, [], [], [], []],
        ["leather choker", 3, [], [], [], []],
        ["lace choker", 3, [], [], ["female"], []],
        ["neck bell", 3, [], [], [], []],
        ["heart choker", 3, [], [], [], []],
        ["crystal pendant", 3, [], [], [], []],
        ["gemstone pendant", 3, [], [], [], []],
        ["photo pendant", 3, [], [], [], []],
        ["amulet", 3, [], [], [], []],
        ["talisman", 3, [], [], [], []],
        ["chandelier earrings", 3, [], [], ["female"], []],
        ["stud earrings", 4, [], [], [], []],
        ["hoop earrings", 4, [], [], ["female"], []],
        ["drop earrings", 3, [], [], ["female"], []],
        ["dangle earrings", 3, [], [], ["female"], []],
        ["clip-on earrings", 3, [], [], ["female"], []],
        ["pearl earrings", 3, [], [], ["female"], []],
        ["diamond earrings", 3, [], [], ["female"], []],
        ["ear cuff", 3, [], [], [], []],
        ["industrial piercing", 2, [], [], [], []],
        ["tragus piercing", 2, [], [], [], []],
        ["helix piercing", 2, [], [], [], []],
        ["multiple ear piercings", 3, [], [], [], []],
        ["reading glasses", 4, [], [], [], []],
        ["round glasses", 4, [], [], [], []],
        ["square glasses", 4, [], [], [], []],
        ["cat-eye glasses", 3, [], [], ["female"], []],
        ["oversized glasses", 3, [], [], [], []],
        ["half-rim glasses", 3, [], [], [], []],
        ["rimless glasses", 3, [], [], [], []],
        ["aviator glasses", 3, [], [], [], []],
        ["wayfarer glasses", 3, [], [], [], []],
        ["wire-frame glasses", 3, [], [], [], []],
        ["thick-framed glasses", 3, [], [], [], []],
        ["monocle", 2, [], [], [], []],
        ["pince-nez", 2, [], [], [], []],
        ["opera glasses", 2, [], [], [], []],
        ["safety glasses", 2, [], [], [], []],
        ["sports sunglasses", 3, [], [], [], []],
        ["aviator sunglasses", 3, [], [], [], []],
        ["round sunglasses", 3, [], [], [], []],
        ["heart-shaped sunglasses", 3, [], [], [], []],
        ["mirrored sunglasses", 3, [], [], [], []],
        ["tinted sunglasses", 3, [], [], [], []],
        ["retro sunglasses", 3, [], [], [], []],
        ["waist belt", 4, [], [], [], []],
        ["chain belt", 3, [], [], [], []],
        ["leather belt", 4, [], [], [], []],
        ["studded belt", 3, [], [], [], []],
        ["utility belt", 3, [], [], [], []],
        ["obi", 3, [], [], [], []],
        ["waist cincher", 8, [], [], ["female"], []],
        ["decorative belt", 3, [], [], [], []],
        ["ceremonial belt", 2, [], [], [], []],
        ["fitness tracker", 3, [], [], [], []],
        ["cuffs", 5, [], [], [], []],
        ["shackles", 10, [], [], [], []],
        ["handcuffs", 5, [], [], [], []],
        ["flower crown", 3, [], [], [], []],
        ["laurel crown", 3, [], [], [], []],
        ["headphones", 4, [], [], [], []],
        ["cat headphones", 3, [], [], [], []],
        ["wireless earbuds", 3, [], [], [], []],
        ["nameplate necklace", 3, [], [], [], []],
        ["body chain", 3, [], [], ["female"], []],
        ["belly chain", 3, [], [], ["female"], []],
        ["naval piercing", 3, [], [], ["female"], []],
        ["lip piercing", 2, [], [], [], []],
        ["nose ring", 3, [], [], [], []],
        ["nose stud", 3, [], [], [], []],
        ["eyebrow piercing", 2, [], [], [], []],
        ["tongue piercing", 2, [], [], [], []],
        ["multiple piercings", 3, [], [], [], []],
        ["spiked wristband", 3, [], [], [], []],
        ["athletic wristband", 3, [], [], [], []],
        ["sweatband", 3, [], [], [], []],
        ["bandaged wrist", 3, [], [], [], []],
        ["sweat towel", 3, [], [], [], []],
        ["arm garter", 3, [], [], [], []],
        ["thigh garter", 3, [], [], ["female"], []],
        ["bridal garter", 3, [], [], ["female"], []],
        ["leg band", 3, [], [], [], []],
        ["lanyard", 3, [], [], [], []],
        ["ID card", 3, [], [], [], []],
        ["badge", 3, [], [], [], []],
        ["name tag", 3, [], [], [], []],
        ["ribbons", 3, [], [], [], []],
        ["arm ribbon", 3, [], [], [], []],
        ["wrist ribbon", 3, [], [], [], []],
        ["neck ribbon", 3, [], [], [], []],
        ["toe ring", 2, [], [], [], []],
        ["ankle chain", 3, [], [], [], []],
        ["ankle monitor", 2, [], [], [], []],
        ["smart band", 3, [], [], [], []],
        ["medical bracelet", 2, [], [], [], []],
        ["charm necklace", 3, [], [], [], []],
        ["rosary beads", 3, [], [], [], []],
        ["prayer beads", 3, [], [], [], []],
        ["mala beads", 2, [], [], [], []],
        ["bead necklace", 3, [], [], [], []]
    ],

    
    "to": [
        ["smile", 5, [], [], [], []], 
        ["blush", 5, [], [], [], []], 
        ["ahegao", 1, [], [], [], []],
        ["frown", 5, [], [], [], []],
        ["pout", 5, [], [], [], []],
        ["grin", 5, [], [], [], []],
        ["smirk", 5, [], [], [], []],
        ["angry", 6, [], [], [], []],
        ["crying", 3, [], [], [], []],
        ["embarrassed", 4, [], [], [], []],
        ["surprised", 4, [], [], [], []],
        ["scared", 7, [], [], [], []],
        ["depressed", 7, [], [], [], []],
        ["terrified", 5, [], [], [], []],
        ["sad", 6, [], [], [], []],
        ["laughing", 4, [], [], [], []],
        ["screaming", 3, [], [], [], []],
        ["grimace", 3, [], [], [], []],
        ["winking", 4, [], [], [], []],
        ["drooling", 3, [], [], [], []],
        ["expressionless", 4, [], [], [], []],
        ["happy", 5, [], [], [], []],
        ["serious", 4, [], [], [], []],
        ["tongue out", 4, [], [], [], []],
        ["open mouth", 4, [], [], [], []],
        ["closed mouth", 4, [], [], [], []],
        ["parted lips", 4, [], [], [], []],
        ["funny face", 4, [], [], [], []],
        ["confused", 4, [], [], [], []],
        ["anxious", 5, [], [], [], []],
        ["nervous", 5, [], [], [], []],
        ["relieved", 4, [], [], [], []],
        ["excited", 5, [], [], [], []],
        ["annoyed", 5, [], [], [], []],
        ["disgusted", 4, [], [], [], []],
        ["bored", 4, [], [], [], []],
        ["proud", 4, [], [], [], []],
        ["confident", 5, [], [], [], []],
        ["shy", 5, [], [], [], []],
        ["frustrated", 4, [], [], [], []],
        ["shocked", 4, [], [], [], []],
        ["curious", 4, [], [], [], []],
        ["sleepy", 4, [], [], [], []],
        ["yawning", 3, [], [], [], []],
        ["laughing tears", 4, [], [], [], []],
        ["mischievous", 4, [], [], [], []],
        ["thoughtful", 4, [], [], [], []],
        ["content", 4, [], [], [], []],
        ["hopeful", 4, [], [], [], []],
        ["determined", 5, [], [], [], []],
        ["smug", 5, [], [], [], []],
        ["skeptical", 4, [], [], [], []],
        ["suspicious", 4, [], [], [], []],
        ["neutral expression", 4, [], [], [], []],
        ["puppy eyes", 4, [], [], [], []],
        ["pleading look", 4, [], [], [], []],
        ["cheeky", 4, [], [], [], []],
        ["teasing", 4, [], [], [], []],
        ["tearful", 3, [], [], [], []],
        ["bitter smile", 3, [], [], [], []],
        ["forced smile", 3, [], [], [], []],
        ["evil smile", 3, [], [], [], []],
        ["panicked", 4, [], [], [], []],
        ["joyful", 5, [], [], [], []],
        ["disappointed", 4, [], [], [], []],
        ["distant look", 3, [], [], [], []],
        ["longing", 3, [], [], [], []],
        ["nostalgic", 3, [], [], [], []],
        ["guilty", 3, [], [], [], []],
        ["remorseful", 3, [], [], [], []],
        ["hopeless", 3, [], [], [], []],
        ["overwhelmed", 3, [], [], [], []],
        ["worried", 4, [], [], [], []],
        ["irritated", 4, [], [], [], []],
        ["contemplative", 3, [], [], [], []],
        ["impressed", 3, [], [], [], []],
        ["exasperated", 3, [], [], [], []],
        ["bewildered", 3, [], [], [], []],
        ["dazed", 3, [], [], [], []],
        ["startled", 3, [], [], [], []],
        ["sheepish", 3, [], [], [], []],
        ["awed", 3, [], [], [], []],
        ["horrified", 3, [], [], [], []],
        ["ecstatic", 4, [], [], [], []],
        ["satisfied", 4, [], [], [], []],
        ["serene", 4, [], [], [], []],
        ["blank stare", 3, [], [], [], []],
        ["unimpressed", 3, [], [], [], []],
        ["judgmental", 3, [], [], [], []],
        ["doubtful", 3, [], [], [], []],
        ["lovestruck", 3, [], [], [], []],
        ["bittersweet", 3, [], [], [], []],
        ["intrigued", 4, [], [], [], []],
        ["amused", 4, [], [], [], []],
        ["suspicious glare", 3, [], [], [], []],
        ["compassionate", 3, [], [], [], []],
        ["gentle smile", 4, [], [], [], []],
        ["resigned", 3, [], [], [], []],
        ["indifferent", 3, [], [], [], []],
        ["fascinated", 3, [], [], [], []],
        ["zealous", 3, [], [], [], []],
        ["grumpy", 4, [], [], [], []],
        ["cheerful", 5, [], [], [], []],
        ["coy", 3, [], [], [], []],
        ["yearning", 3, [], [], [], []],
        ["apologetic", 3, [], [], [], []],
        ["stern", 4, [], [], [], []],
        ["fierce", 4, [], [], [], []],
        ["glaring", 4, [], [], [], []],
        ["melancholic", 3, [], [], [], []],
        ["awestruck", 3, [], [], [], []],
    ],

    
    "tl": [
        ["year 2023", 5, [], [], [], []], 
        ["year 2024", 5, [], [], [], []],
        ["year 2025", 5, [], [], [], []],
        ["spring", 5, [], [], [], []],
        ["summer", 5, [], [], [], []],
        ["autumn", 5, [], [], [], []],
        ["winter", 5, [], [], [], []],
        ["morning", 5, [], [], [], []],
        ["afternoon", 5, [], [], [], []],
        ["evening", 5, [], [], [], []],
        ["night", 5, [], [], [], []],
        ["dawn", 4, [], [], [], []],
        ["dusk", 4, [], [], [], []],
        ["midnight", 4, [], [], [], []],
        ["rainy season", 3, [], [], [], []],
        ["snowy season", 3, [], [], [], []],
        ["cherry blossom season", 4, [], [], [], []],
        ["autumn leaves", 4, [], [], [], []],
        ["christmas", 4, [], [], [], []],
        ["halloween", 4, [], [], [], []],
        ["valentine", 4, [], [], [], []],
        ["new year", 4, [], [], [], []]
    ],
    
    "td": [
        ["forest", 5, [], [], [], []], 
        ["cityscape", 5, [], [], [], []],
        ["beach", 5, [], [], [], []],
        ["mountains", 5, [], [], [], []],
        ["river", 5, [], [], [], []],
        ["lake", 5, [], [], [], []],
        ["desert", 4, [], [], [], []],
        ["ocean", 5, [], [], [], []],
        ["sky", 5, [], [], [], []],
        ["clouds", 5, [], [], [], []],
        ["stars", 4, [], [], [], []],
        ["cherry blossoms", 4, [], [], [], []],
        ["autumn leaves", 4, [], [], [], []],
        ["snow", 4, [], [], [], []],
        ["rain", 4, [], [], [], []],
        ["waterfall", 4, [], [], [], []],
        ["path", 4, [], [], [], []],
        ["road", 4, [], [], [], []],
        ["street", 4, [], [], [], []],
        ["garden", 4, [], [], [], []],
        ["field", 4, [], [], [], []],
        ["house", 4, [], [], [], []],
        ["castle", 3, [], [], [], []],
        ["ruins", 3, [], [], [], []]
    ],
    
    "tc": [
        ["cat", 5, [], [], [], []], 
        ["sword", 5, [], [], [], []],
        ["dog", 5, [], [], [], []],
        ["book", 5, [], [], [], []],
        ["gun", 4, [], [], [], []],
        ["staff", 4, [], [], [], []],
        ["spear", 4, [], [], [], []],
        ["bow", 4, [], [], [], []],
        ["shield", 4, [], [], [], []],
        ["axe", 4, [], [], [], []],
        ["hammer", 4, [], [], [], []],
        ["knife", 4, [], [], [], []],
        ["bird", 4, [], [], [], []],
        ["flower", 5, [], [], [], []],
        ["umbrella", 4, [], [], [], []],
        ["fan", 4, [], [], [], []],
        ["cup", 4, [], [], [], []],
        ["food", 4, [], [], [], []],
        ["chair", 4, [], [], [], []],
        ["table", 4, [], [], [], []],
        ["teddy bear", 3, [], [], [], []],
        ["butterfly", 3, [], [], [], []],
        ["fish", 3, [], [], [], []],
        ["phone", 4, [], [], [], []]
    ],
    
    "tg": [
        ["sparkles", 5, [], [], [], []], 
        ["depth of field", 5, [], [], [], []],
        ["lens flare", 4, [], [], [], []],
        ["bokeh", 4, [], [], [], []],
        ["light rays", 4, [], [], [], []],
        ["bloom", 4, [], [], [], []],
        ["backlighting", 4, [], [], [], []],
        ["silhouette", 4, [], [], [], []],
        ["glow", 4, [], [], [], []],
        ["chromatic aberration", 3, [], [], [], []],
        ["light particles", 4, [], [], [], []],
        ["afterimage", 3, [], [], [], []],
        ["diffraction spikes", 3, [], [], [], []],
        ["film grain", 3, [], [], [], []],
        ["steam", 3, [], [], [], []],
        ["smoke", 3, [], [], [], []],
        ["water drop", 3, [], [], [], []],
        ["sunbeam", 4, [], [], [], []],
        ["dappled sunlight", 4, [], [], [], []],
        ["rimlight", 4, [], [], [], []],
        ["light trail", 3, [], [], [], []],
        ["volumetric lighting", 4, [], [], [], []],
        ["godrays", 4, [], [], [], []],
        ["glint", 4, [], [], [], []],
        ["aura", 4, [], [], [], []],
        ["motion blur", 4, [], [], [], []],
        ["motion lines", 4, [], [], [], []],
        ["speed lines", 4, [], [], [], []],
        ["focus pull", 3, [], [], [], []],
        ["rack focus", 3, [], [], [], []],
        ["tilt-shift", 3, [], [], [], []],
        ["vignette", 3, [], [], [], []],
        ["halftone", 3, [], [], [], []],
        ["scanlines", 3, [], [], [], []],
    ],
    
    "tf": [
        ["blue", 5, [], [], [], []], 
        ["red", 5, [], [], [], []], 
        ["black", 5, [], [], [], []],
        ["white", 5, [], [], [], []],
        ["pink", 5, [], [], [], []],
        ["purple", 5, [], [], [], []],
        ["green", 5, [], [], [], []],
        ["yellow", 5, [], [], [], []],
        ["orange", 5, [], [], [], []],
        ["brown", 5, [], [], [], []],
        ["grey", 5, [], [], [], []],
        ["teal", 4, [], [], [], []],
        ["navy", 4, [], [], [], []],
        ["gold", 4, [], [], [], []],
        ["silver", 4, [], [], [], []],
        ["multicolored", 4, [], [], [], []],
        ["pastel colors", 4, [], [], [], []],
        ["neon colors", 3, [], [], [], []],
        ["primary colors", 3, [], [], [], []],
        ["complementary colors", 3, [], [], [], []],
        ["warm colors", 4, [], [], [], []],
        ["cool colors", 4, [], [], [], []],
        ["earth tones", 4, [], [], [], []],
        ["vibrant colors", 4, [], [], [], []]
    ]
}

# Load NSFW tags
ty = {
    "p": [
        [
            "uncensored, pussy",
            5
        ],
        [
            "uncensored, pussy, fat mons",
            2
        ]
    ],
    "mp": [
        [
            "uncensored, penis",
            5
        ],
        [
            "uncensored, huge penis",
            5
        ],
        [
            "uncensored, large penis",
            5
        ],
        [
            "uncensored, small penis",
            5
        ]
    ],
    "n": [
        [
            "clothing aside",
            5
        ],
        [
            "clothes down",
            5
        ],
        [
            "open clothes",
            5
        ],
        [
            "see-through",
            5
        ],
        [
            "unbuttoned",
            5
        ],
        [
            "untied",
            5
        ],
        [
            "unzipped",
            5
        ],
        [
            "breasts out",
            5
        ],
        [
            "areola slip",
            5
        ],
        [
            "nipple slip",
            5
        ],
        [
            "barefoot",
            5
        ],
        [
            "panties around one leg",
            5
        ],
        [
            "downblouse",
            5
        ],
        [
            "downpants",
            5
        ],
        [
            "pantyshot",
            5
        ],
        [
            "upskirt",
            5
        ]
    ],
    "u": [
        [
            "bandaid on pussy",
            5
        ],
        [
            "lingerie",
            5
        ],
        [
            "bra",
            5
        ],
        [
            "fishnets",
            5
        ],
        [
            "garter belt",
            5
        ],
        [
            "panties",
            5
        ],
        [
            "boyshort panties",
            5
        ],
        [
            "micro panties",
            5
        ],
        [
            "lowleg panties",
            5
        ],
        [
            "highleg panties",
            5
        ],
        [
            "thong",
            5
        ],
        [
            "g-string",
            5
        ],
        [
            "pearl thong",
            5
        ],
        [
            "boxers",
            5
        ],
        [
            "briefs",
            5
        ],
        [
            "boxer briefs",
            5
        ],
        [
            "crotchless panties",
            5
        ],
        [
            "reverse bunnysuit",
            5
        ],
        [
            "pasties",
            5
        ],
        [
            "nipple rings",
            5
        ]
    ],
    "nk": [
        [
            "naked apron",
            5
        ],
        [
            "naked bandage",
            5
        ],
        [
            "naked cape",
            5
        ],
        [
            "naked capelet",
            5
        ],
        [
            "naked chocolate",
            5
        ],
        [
            "naked cloak",
            5
        ],
        [
            "naked coat",
            5
        ],
        [
            "naked hoodie",
            5
        ],
        [
            "naked jacket",
            5
        ],
        [
            "naked overalls",
            5
        ],
        [
            "naked ribbon",
            5
        ],
        [
            "naked robe",
            5
        ],
        [
            "naked scarf",
            5
        ],
        [
            "naked sheet",
            5
        ],
        [
            "naked shirt",
            5
        ],
        [
            "naked suspenders",
            5
        ],
        [
            "naked tabard",
            5
        ],
        [
            "naked towel",
            5
        ],
        [
            "nude",
            25
        ]
    ],
    "bd": [
        [
            "blindfold",
            5
        ],
        [
            "gimp suit",
            5
        ],
        [
            "bondage outfit",
            5
        ],
        [
            "latex",
            5
        ],
        [
            "monoglove",
            5
        ]
    ],
    "nEx": [
        [
            "pubic hair",
            25
        ],
        [
            "pussy juice",
            25
        ],
        [
            "clitoris piercing",
            25
        ],
        [
            "clitoris ring",
            25
        ],
        [
            "armpits",
            25
        ],
        [
            "lactation",
            25
        ],
        [
            "pregnant",
            25
        ],
        [
            "exhibitionism",
            25
        ],
        [
            "cameltoe",
            25
        ],
        [
            "covered nipples",
            25
        ],
        [
            "puffy nipples",
            25
        ],
        [
            "inverted nipples",
            25
        ],
        [
            "nipple piercing",
            25
        ],
        [
            "dark nipples",
            25
        ]
    ],
    "nSM": [
        [
            "adjusting panties",
            15
        ],
        [
            "hand in panties",
            15
        ],
        [
            "panty pull",
            15
        ],
        [
            "panties aside",
            15
        ],
        [
            "panty lift",
            15
        ],
        [
            "cumdrip into panties",
            15
        ],
        [
            "vibrator under panties",
            15
        ],
        [
            "undressing",
            15
        ],
        [
            "untying",
            15
        ],
        [
            "unzipping",
            15
        ],
        [
            "shirt lift",
            15
        ],
        [
            "dress lift",
            15
        ],
        [
            "covering privates",
            15
        ],
        [
            "nude modeling",
            15
        ],
        [
            "ass grab",
            15
        ],
        [
            "groping",
            15
        ],
        [
            "crotch grab",
            15
        ],
        [
            "grabbing own breast",
            15
        ],
        [
            "cum inflation",
            15
        ],
        [
            "big belly",
            15
        ],
        [
            "after sex",
            15
        ],
        [
            "after anal",
            15
        ],
        [
            "after fellatio",
            15
        ],
        [
            "after masturbation",
            15
        ],
        [
            "after paizuri",
            15,
            [
                "flat chest"
            ]
        ],
        [
            "after rape",
            15
        ],
        [
            "bondage",
            15
        ],
        [
            "humiliation",
            15
        ],
        [
            "spanked",
            15
        ],
        [
            "bukkake",
            15
        ],
        [
            "cumdump",
            15
        ],
        [
            "cumdrip",
            15
        ],
        [
            "cum in mouth",
            15
        ],
        [
            "cum in pussy",
            15
        ],
        [
            "cum in ass",
            15
        ],
        [
            "cum on body",
            15
        ],
        [
            "cum on armpits",
            15
        ],
        [
            "cum on ass",
            15
        ],
        [
            "cum on breasts",
            15
        ],
        [
            "cum on feet",
            15
        ],
        [
            "cum on fingers",
            15
        ],
        [
            "cum on hair",
            15
        ],
        [
            "cum on stomach",
            15
        ],
        [
            "cum on clothes",
            15
        ],
        [
            "cum on eyewear",
            15
        ],
        [
            "ejaculation",
            15
        ],
        [
            "facial",
            15
        ],
        [
            "public indecency",
            15
        ],
        [
            "female ejaculation",
            15
        ],
        [
            "peeing",
            15
        ],
        [
            "sex machine",
            15
        ],
        [
            "milking",
            15
        ],
        [
            "breast pump",
            15
        ],
        [
            "milking machine",
            15
        ],
        [
            "spread legs",
            15
        ],
        [
            "presenting",
            15
        ],
        [
            "presenting armpit",
            15
        ],
        [
            "on stomach",
            15
        ],
        [
            "on back",
            15
        ],
        [
            "rear view",
            15
        ],
        [
            "orgasm",
            15
        ]
    ],
    "nSA": [
        [
            "anal fingering",
            15
        ],
        [
            "fingering",
            15
        ],
        [
            "ass grab",
            15
        ],
        [
            "ass smack",
            15
        ],
        [
            "covering ass",
            15
        ],
        [
            "spread ass",
            15
        ],
        [
            "spread anus",
            15
        ],
        [
            "cum in ass",
            15
        ],
        [
            "cum on ass",
            15
        ]
    ],
    "nSP": [
        [
            "spread pussy",
            15
        ],
        [
            "masturbation",
            15
        ],
        [
            "cum in pussy",
            15
        ],
        [
            "cum on pussy",
            15
        ]
    ],
    "nPM": [
        [
            "footjob",
            5
        ],
        [
            "licking foot",
            5
        ],
        [
            "foot worship",
            5
        ],
        [
            "smelling feet",
            5
        ],
        [
            "paizuri",
            5,
            [
                "flat chest"
            ]
        ],
        [
            "paizuri, on back",
            5,
            [
                "flat chest"
            ]
        ],
        [
            "grabbing another's breast",
            5
        ],
        [
            "handjob",
            5
        ],
        [
            "torso grab",
            5
        ],
        [
            "nursing handjob",
            5
        ],
        [
            "breast sucking",
            5
        ],
        [
            "fellatio",
            5
        ],
        [
            "molestation",
            5
        ],
        [
            "kiss",
            5
        ],
        [
            "hugging",
            5
        ]
    ],
    "nPA": [
        [
            "anal",
            4
        ],
        [
            "anal, doggystyle",
            4
        ],
        [
            "anal, doggystyle, bent over",
            4
        ],
        [
            "anal, doggystyle, top-down bottom-up",
            4
        ],
        [
            "anal, spooning, on-side",
            4
        ],
        [
            "anal, cowgirl position",
            4
        ],
        [
            "anal, reverse cowgirl position",
            4
        ],
        [
            "anal, reverse upright straddle, straddling",
            4
        ],
        [
            "anal, upright straddle, straddling",
            4
        ],
        [
            "anal, on back, folded",
            4
        ],
        [
            "anal, missionary",
            4
        ],
        [
            "anal, suspended congress",
            4
        ]
    ],
    "nPP": [
        [
            "sex",
            5
        ],
        [
            "sex, doggystyle",
            5
        ],
        [
            "sex, doggystyle, bent over",
            5
        ],
        [
            "sex, doggystyle, top-down bottom-up",
            5
        ],
        [
            "sex, spooning, on-side",
            5
        ],
        [
            "sex, cowgirl position",
            5
        ],
        [
            "sex, reverse cowgirl position",
            5
        ],
        [
            "sex, reverse upright straddle, straddling",
            5
        ],
        [
            "sex, upright straddle, straddling",
            5
        ],
        [
            "sex, on back, folded",
            5
        ],
        [
            "sex, missionary",
            5
        ],
        [
            "sex, suspended congress",
            5
        ],
        [
            "sex, defloration",
            5
        ],
        [
            "sex, gangbang",
            5
        ],
        [
            "sex, stomach bulge",
            5
        ]
    ],
    "sMod": [
        [
            "clothed sex",
            5
        ],
        [
            "happy sex",
            5
        ],
        [
            "implied sex",
            5
        ],
        [
            "tentacle sex",
            5
        ],
        [
            "ahegao",
            5
        ],
        [
            "fucked silly",
            5
        ],
        [
            "rape",
            5
        ],
        [
            "femdom rape",
            5
        ]
    ],
    "sActMod": [
        [
            "bondage",
            5
        ],
        [
            "femdom",
            5
        ],
        [
            "assertive female",
            5
        ],
        [
            "humiliation",
            5
        ],
        [
            "body writing",
            5
        ],
        [
            "public use",
            5
        ],
        [
            "body writing",
            5
        ],
        [
            "slave",
            5
        ],
        [
            "cum",
            5
        ],
        [
            "prostitution",
            5
        ],
        [
            "netorare",
            5
        ],
        [
            "voyeurism",
            5
        ],
        [
            "naughty face",
            5
        ],
        [
            "condom",
            5
        ],
        [
            "sound effects",
            5
        ],
        [
            "lactation",
            5
        ]
    ],
    "sT": [
        [
            "dildo",
            5
        ],
        [
            "vibrator",
            5
        ],
        [
            "anal beads",
            5
        ],
        [
            "leash",
            5
        ],
        [
            "pillory",
            5
        ],
        [
            "rope",
            5
        ],
        [
            "whip",
            5
        ],
        [
            "gag",
            5
        ]
    ],
    "h": "hetero",
    "yu": "yuri",
    "ya": "yaoi",
    "fu": "futanari",
    "fwm": "futa with male",
    "fwf": "futa with female",
    "nw": "nsfw"
}

def get_weighted_choice(choices_with_weights, current_scene_tags_set, character_flags_set=None):
    if character_flags_set is None:
        character_flags_set = set()

    filtered_choices = []
    for choice_item_orig in choices_with_weights:
        # Ensure choice_item has the full 6-element structure for processing
        choice_item = list(choice_item_orig) # Make a mutable copy
        if len(choice_item) < 2: continue # Invalid item

        tag_to_return = choice_item[0]
        weight = choice_item[1]
        
        scene_requires = choice_item[2] if len(choice_item) > 2 and choice_item[2] else []
        char_adds = choice_item[3] if len(choice_item) > 3 and choice_item[3] else []
        char_requires = choice_item[4] if len(choice_item) > 4 and choice_item[4] else []
        char_excludes = choice_item[5] if len(choice_item) > 5 and choice_item[5] else []
        
        # Standardize the choice_item to the full structure for return
        full_choice_item = [tag_to_return, weight, scene_requires, char_adds, char_requires, char_excludes]

        is_choice_valid = True
        # Check scene_requires
        if scene_requires:
            if not all(cond in current_scene_tags_set for cond in scene_requires):
                is_choice_valid = False
        
        # Check char_requires (only if character_flags_set is provided for this choice type)
        if is_choice_valid and char_requires:
            if not all(cond in character_flags_set for cond in char_requires):
                is_choice_valid = False
        
        # Check char_excludes (only if character_flags_set is provided for this choice type)
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

    rand_val = random.randint(1, total_weight)
    cumulative_weight = 0
    for item in filtered_choices:
        cumulative_weight += item[1]
        if rand_val <= cumulative_weight:
            return item # Return the full chosen item
    
    return None


def generate_character_tags(char_actual_type, current_scene_tags_set, is_nsfw, total_chars_in_scene, framing_tag_str):
    char_tags_strings = [] # List to hold final tag strings for this character
    character_flags = set()

    if char_actual_type == "f":
        character_flags.add("female")
    elif char_actual_type == "m":
        character_flags.add("male")
    # Add other initial flags if necessary, e.g. based on framing_tag_str
    if framing_tag_str == "full body":
        character_flags.add("legs")
        character_flags.add("feet")
    elif framing_tag_str == "cowboy_shot":
        character_flags.add("legs")


    def_scene_tags_for_choice = current_scene_tags_set.union(set(char_tags_strings))


    # Helper to process a choice
    def apply_choice(category_key, probability, is_multi_part_tag=False, second_category_key=None):
        nonlocal def_scene_tags_for_choice
        if random.random() < probability:
            chosen_item = get_weighted_choice(tags_data[category_key], def_scene_tags_for_choice, character_flags)
            if chosen_item:
                char_tags_strings.append(chosen_item[0])
                for flag in chosen_item[3]: # char_adds_list
                    character_flags.add(flag)
                def_scene_tags_for_choice.add(chosen_item[0]) # Add main tag to set for subsequent choices
                if chosen_item[0] == "long hair": character_flags.add("longhair") # specific common flag

                if is_multi_part_tag and second_category_key:
                    chosen_item2 = get_weighted_choice(tags_data[second_category_key], def_scene_tags_for_choice, character_flags)
                    if chosen_item2:
                        char_tags_strings.append(chosen_item2[0])
                        for flag in chosen_item2[3]: character_flags.add(flag)
                        def_scene_tags_for_choice.add(chosen_item2[0])


    apply_choice("e_dollar", 0.0) # Species/Race
    apply_choice("eq", 0.4)      # Skin color
    
    if "noeyes" not in character_flags : # From JS logic for tR (eX)
        apply_choice("tm", 0.8)      # Eye color
        apply_choice("eX", 0.1)      # Eye details
        apply_choice("eQ", 0.2)      # Eye shape

    apply_choice("eY", 0.8)      # Hair length
    apply_choice("eK", 0.7)      # Hair style (main)
    apply_choice("tp", 0.7)      # Hair color
    apply_choice("tu", 0.1, is_multi_part_tag=True, second_category_key="tp") # Multicolor hair + base
    apply_choice("e0", 0.3)      # Hair properties (messy, pointy)
    apply_choice("e1", 0.3)      # Bangs, sidelocks

    if "female" in character_flags: # breast size
        apply_choice("e2", 1.0)

    # Body features (e5)
    num_body_features_choices_weights = []
    if total_chars_in_scene == 1:
        num_body_features_choices_weights = [[0, 30], [1, 10], [2, 5]]
    elif total_chars_in_scene == 2:
        num_body_features_choices_weights = [[0, 20], [1, 40], [2, 10]]
    else:
        num_body_features_choices_weights = [[0, 30], [1, 30]]
    
    # This weighted choice is for count, not a tag directly.
    # For simplicity, I'll use random.choices if available or simulate.
    # Python's get_weighted_choice returns the item itself.
    # Here we need the number.
    # Simplified: pick a number of e5 tags to add
    counts = [item[0] for item in num_body_features_choices_weights]
    weights = [item[1] for item in num_body_features_choices_weights]
    if counts and weights and sum(weights) > 0:
      num_e5_tags_to_add = random.choices(counts, weights=weights, k=1)[0]
      for _ in range(num_e5_tags_to_add):
          apply_choice("e5", 1.0) # Probability 1.0 because we've already decided to add one

    # Headwear
    if random.random() < 0.2:
        apply_choice("e6", 1.0) # Hat
        apply_choice("e4", 0.2) # Hat ornament
    elif random.random() < 0.3:
        apply_choice("e3", 1.0) # Hair accessory

    clothing_category_item = get_weighted_choice([
        ["uniform", 10, [], [], [], []], 
        ["swimsuit", 5, [], [], [], []], 
        ["bodysuit", 5, [], [], [], []], 
        ["normal clothes", 40, [], [], [], []],
        ["underwear", 20, [], [], [], []]
    ], def_scene_tags_for_choice, character_flags)
    clothing_category = clothing_category_item[0] if clothing_category_item else None

    if is_nsfw: # NSFW clothing modifications
        nsfw_clothing_mod_choice_item = get_weighted_choice([["n", 15], ["u", 10], ["nk", 5]], def_scene_tags_for_choice, character_flags) # Assuming simple structure for this specific choice
        if nsfw_clothing_mod_choice_item:
            nsfw_clothing_mod_choice = nsfw_clothing_mod_choice_item[0]
            if nsfw_clothing_mod_choice == "n" and 'n' in ty:
                chosen_nsfw_item = get_weighted_choice(ty['n'], def_scene_tags_for_choice, character_flags)
                if chosen_nsfw_item: char_tags_strings.append(chosen_nsfw_item[0]) # Simpler handling for ty items
            elif nsfw_clothing_mod_choice == "u" and 'u' in ty:
                chosen_nsfw_item = get_weighted_choice(ty['u'], def_scene_tags_for_choice, character_flags)
                if chosen_nsfw_item: char_tags_strings.append(chosen_nsfw_item[0])
                if random.random() < 0.5: clothing_category = None
            elif nsfw_clothing_mod_choice == "nk" and 'nk' in ty:
                chosen_nsfw_item = get_weighted_choice(ty['nk'], def_scene_tags_for_choice, character_flags)
                if chosen_nsfw_item: char_tags_strings.append(chosen_nsfw_item[0])
                clothing_category = None
        
        if framing_tag_str not in ["portrait", "upper body"]:
            if "female" in character_flags and random.random() < 0.8 and 'p' in ty:
                chosen_nsfw_item = get_weighted_choice(ty['p'], def_scene_tags_for_choice, character_flags)
                if chosen_nsfw_item: char_tags_strings.append(chosen_nsfw_item[0])
            elif "male" in character_flags and random.random() < 0.8 and 'mp' in ty:
                chosen_nsfw_item = get_weighted_choice(ty['mp'], def_scene_tags_for_choice, character_flags)
                if chosen_nsfw_item: char_tags_strings.append(chosen_nsfw_item[0])


    if clothing_category == "uniform": apply_choice("ti", 1.0)
    elif clothing_category == "swimsuit": apply_choice("tr", 1.0)
    elif clothing_category == "bodysuit": apply_choice("ts", 1.0)
    elif clothing_category == "underwear": apply_choice("underwear", 1.0)
    elif clothing_category == "normal clothes":
        if "female" in character_flags and random.random() < 0.5: # Legwear for females
            apply_choice("e8", 1.0) # Legwear
            apply_choice("e9", 0.2) # Legwear detail
        
        is_dress = False
        if "female" in character_flags and random.random() < 0.2: # Dress for females
            use_color = random.random() < 0.5
            color_item = get_weighted_choice(tags_data["tf"], def_scene_tags_for_choice, character_flags) if use_color else None
            color = color_item[0] if color_item else ""
            
            dress_item_choice = get_weighted_choice(tags_data["e7"], def_scene_tags_for_choice, character_flags)
            if dress_item_choice:
                is_dress = True
                final_dress_tag = f"{color} {dress_item_choice[0]}".strip() if use_color and color else dress_item_choice[0]
                char_tags_strings.append(final_dress_tag)
                for flag in dress_item_choice[3]: character_flags.add(flag)
                def_scene_tags_for_choice.add(final_dress_tag)

        if not is_dress: # Tops/bottoms/footwear
            if random.random() < 0.85: # Top wear
                use_color = random.random() < 0.5
                color_item = get_weighted_choice(tags_data["tf"], def_scene_tags_for_choice, character_flags) if use_color else None
                color = color_item[0] if color_item else ""
                top_item_choice = get_weighted_choice(tags_data["te"], def_scene_tags_for_choice, character_flags)
                if top_item_choice:
                    final_top_tag = f"{color} {top_item_choice[0]}".strip() if use_color and color else top_item_choice[0]
                    char_tags_strings.append(final_top_tag)
                    for flag in top_item_choice[3]: character_flags.add(flag)
                    def_scene_tags_for_choice.add(final_top_tag)
            
            if "nolegs" not in character_flags:
                if random.random() < 0.85 and "portrait_framing" not in character_flags : # Bottom wear - portrait check by flag
                    use_color = random.random() < 0.5
                    color_item = get_weighted_choice(tags_data["tf"], def_scene_tags_for_choice, character_flags) if use_color else None
                    color = color_item[0] if color_item else ""
                    bottom_item_choice = get_weighted_choice(tags_data["tt"], def_scene_tags_for_choice, character_flags)
                    if bottom_item_choice:
                        final_bottom_tag = f"{color} {bottom_item_choice[0]}".strip() if use_color and color else bottom_item_choice[0]
                        char_tags_strings.append(final_bottom_tag)
                        for flag in bottom_item_choice[3]: character_flags.add(flag)
                        def_scene_tags_for_choice.add(final_bottom_tag)
                
                if "nofeet" not in character_flags:
                    if random.random() < 0.6 and ("full_body_framing" in character_flags or framing_tag_str is None) : # Footwear
                        use_color = random.random() < 0.5
                        color_item = get_weighted_choice(tags_data["tf"], def_scene_tags_for_choice, character_flags) if use_color else None
                        color = color_item[0] if color_item else ""
                        footwear_item_choice = get_weighted_choice(tags_data["ta"], def_scene_tags_for_choice, character_flags)
                        if footwear_item_choice:
                            final_footwear_tag = f"{color} {footwear_item_choice[0]}".strip() if use_color and color else footwear_item_choice[0]
                            char_tags_strings.append(final_footwear_tag)
                            for flag in footwear_item_choice[3]: character_flags.add(flag)
                            def_scene_tags_for_choice.add(final_footwear_tag)

    apply_choice("to", 0.6) # Expression

    pose_chance = 0.4
    if is_nsfw and total_chars_in_scene == 1: pose_chance = 1.0
    
    if random.random() < pose_chance: # Pose
        pose_choices_data = list(tags_data.get("th", [])) # Use .get for safety
        if is_nsfw:
            # Assuming ty items might not have full 6-element structure,
            # get_weighted_choice handles this.
            if 'nSM' in ty: pose_choices_data.extend(ty['nSM'])
            if 'nSA' in ty: pose_choices_data.extend(ty['nSA'])
            if 'nSP' in ty: pose_choices_data.extend(ty['nSP'])
        
        chosen_pose_item = get_weighted_choice(pose_choices_data, def_scene_tags_for_choice, character_flags)
        if chosen_pose_item:
            char_tags_strings.append(chosen_pose_item[0])
            for flag in chosen_pose_item[3]: character_flags.add(flag)
            def_scene_tags_for_choice.add(chosen_pose_item[0])


    # Filter eye color if eyes are closed/sleeping
    has_closed_eyes_tag = any(
        "closed eyes" in tag_group.lower() or \
        "sleeping" in tag_group.lower() or \
        "zzz" in tag_group.lower()
        for tag_group in char_tags_strings
    ) or "noeyes" in character_flags # Also if noeyes flag is set

    if has_closed_eyes_tag:
        # Get base eye color tags (item[0]) from the eye color category (tm)
        eye_color_tag_names_to_remove = {item[0] for item in tags_data.get("tm", [])}
        # Filter out char_tags_strings
        char_tags_strings = [tag_str for tag_str in char_tags_strings if tag_str not in eye_color_tag_names_to_remove]


    # Accessories/Details (tn)
    num_accessories_choices_weights = []
    if total_chars_in_scene == 1: num_accessories_choices_weights = [[0, 10], [1, 30], [2, 15], [3, 5]]
    elif total_chars_in_scene == 2: num_accessories_choices_weights = [[0, 20], [1, 40], [2, 10]]
    else: num_accessories_choices_weights = [[0, 30], [1, 30]]

    acc_counts = [item[0] for item in num_accessories_choices_weights]
    acc_weights = [item[1] for item in num_accessories_choices_weights]

    if acc_counts and acc_weights and sum(acc_weights) > 0:
        num_tn_tags_to_add = random.choices(acc_counts, weights=acc_weights, k=1)[0]
        
        accessory_choices_data = list(tags_data.get("tn", []))
        if is_nsfw and 'nEx' in ty:
            accessory_choices_data.extend(ty['nEx'])
            
        for _ in range(num_tn_tags_to_add):
            chosen_accessory_item = get_weighted_choice(accessory_choices_data, def_scene_tags_for_choice, character_flags)
            if chosen_accessory_item:
                char_tags_strings.append(chosen_accessory_item[0])
                for flag in chosen_accessory_item[3]: character_flags.add(flag)
                def_scene_tags_for_choice.add(chosen_accessory_item[0])
            
    if "nolegs" in character_flags or "nofeet" in character_flags : # Remove legwear if character has no legs/feet
        legwear_tags_to_check = set()
        if tags_data.get("e8"): legwear_tags_to_check.update(item[0] for item in tags_data["e8"]) # legwear
        if tags_data.get("e9"): legwear_tags_to_check.update(item[0] for item in tags_data["e9"]) # legwear details
        
        char_tags_strings_no_legwear = []
        for tag_str in char_tags_strings:
            # More precise check: remove if the tag IS a legwear tag, not just contains "legwear"
            is_legwear = False
            for legwear_base in legwear_tags_to_check:
                if legwear_base in tag_str: # If a known legwear tag is part of this generated tag string
                    is_legwear = True
                    break
            if not is_legwear:
                 char_tags_strings_no_legwear.append(tag_str)
        char_tags_strings = char_tags_strings_no_legwear
        
    return char_tags_strings


def generate_scene_prompts_v2(num_prompts_per_category):
    categories = {
        "prompts_1boy": {"num_girls": 0, "num_boys": 1, "is_nsfw": False, "target_list_key": "man", "prepend": "1boy, adult, man, "},
        "prompts_1boy_nsfw": {"num_girls": 0, "num_boys": 1, "is_nsfw": True, "target_list_key": "man_nsfw", "prepend": "1boy, adult, man, "},
        "prompts_1girl": {"num_girls": 1, "num_boys": 0, "is_nsfw": False, "target_list_key": "woman", "prepend": "1girl, adult, woman, "},
        "prompts_1girl_nsfw": {"num_girls": 1, "num_boys": 0, "is_nsfw": True, "target_list_key": "woman_nsfw", "prepend": "1girl, adult, woman, "},
        # Add other categories as needed
    }

    all_prompts = {key_info["target_list_key"]: [] for key_info in categories.values()}

    for category_filename_base, params in categories.items():
        num_girls = params["num_girls"]
        num_boys = params["num_boys"]
        is_nsfw_category = params["is_nsfw"]
        current_category_key = params["target_list_key"]

        print(f"Generating for category: {current_category_key}")
        generated_prompts_for_category = 0

        while generated_prompts_for_category < num_prompts_per_category:
            general_tags_for_scene_list = []
            
            num_total_chars_in_scene = num_girls + num_boys

            if num_girls == 1: general_tags_for_scene_list.append("1girl")
            elif num_girls > 1: general_tags_for_scene_list.append(f"{num_girls}girls")
            if num_boys == 1: general_tags_for_scene_list.append("1boy")
            elif num_boys > 1: general_tags_for_scene_list.append(f"{num_boys}boys")
            
            # Convert general_tags_for_scene_list to a set for efficient lookup in get_weighted_choice
            current_scene_tags_set = set(tag_item.strip() for tag_group_str in general_tags_for_scene_list for tag_item in tag_group_str.split(','))

            framing_tag_for_scene_str = None # This will be the string like "portrait"
            
            # --- General Scene Tags ---
            # Style
            if random.random() < 0.3:
                chosen_item = get_weighted_choice(tags_data["eG"], current_scene_tags_set)
                if chosen_item: general_tags_for_scene_list.append(chosen_item[0]); current_scene_tags_set.add(chosen_item[0])
            # Background
            if random.random() < 0.8:
                bg_item = get_weighted_choice(tags_data["eU"], current_scene_tags_set)
                if bg_item:
                    general_tags_for_scene_list.append(bg_item[0]); current_scene_tags_set.add(bg_item[0])
                    if bg_item[0] == "scenery" and random.random() < 0.5:
                        num_scenery_details = random.randint(1, 2)
                        for _ in range(num_scenery_details):
                            detail_item = get_weighted_choice(tags_data["td"], current_scene_tags_set)
                            if detail_item: general_tags_for_scene_list.append(detail_item[0]); current_scene_tags_set.add(detail_item[0])
            # Camera Angle
            if random.random() < 0.3:
                angle_item = get_weighted_choice(tags_data["eH"], current_scene_tags_set)
                if angle_item: general_tags_for_scene_list.append(angle_item[0]); current_scene_tags_set.add(angle_item[0])
            # Framing
            if random.random() < 0.7:
                framing_item = get_weighted_choice(tags_data["eJ"], current_scene_tags_set)
                if framing_item:
                    framing_tag_for_scene_str = framing_item[0]
                    general_tags_for_scene_list.append(framing_tag_for_scene_str)
                    current_scene_tags_set.add(framing_tag_for_scene_str)
                    # Add flags from framing_item if they exist (char_adds_list is index 3)
                    # These flags are more conceptual for the scene setup
                    # For now, framing_tag_for_scene_str is passed to char gen.
                    # The flags like "legs", "feet" are added within generate_character_tags based on this string.


            if is_nsfw_category:
                if ty.get('nw'): # This 'nw' is often a single string, not a list of choices
                    if isinstance(ty['nw'], str): general_tags_for_scene_list.append(ty['nw']); current_scene_tags_set.add(ty['nw'])
                    elif isinstance(ty['nw'], list): # if it's a list of choices
                        nw_item = get_weighted_choice(ty['nw'], current_scene_tags_set)
                        if nw_item: general_tags_for_scene_list.append(nw_item[0]); current_scene_tags_set.add(nw_item[0])

                if random.random() < 0.4 and ty.get('sActMod'):
                    sact_item = get_weighted_choice(ty['sActMod'], current_scene_tags_set)
                    if sact_item: general_tags_for_scene_list.append(sact_item[0]); current_scene_tags_set.add(sact_item[0])
                # ... other nsfw general tags ...
                if num_girls == 1 and num_boys == 0 and random.random() < 0.2 and ty.get('fu'):
                     if isinstance(ty['fu'], str): general_tags_for_scene_list.append(ty['fu']); current_scene_tags_set.add(ty['fu'])
                     # futa logic might need to set a character_flag for the girl too

            # --- Generate Character Specific Tags ---
            all_character_specific_tags_list = []
            
            # The `current_scene_tags_set` passed to `generate_character_tags` should contain
            # all general scene tags determined so far, as some character choices might depend on them.
            # (e.g. if a character tag had a `scene_requires` for "outdoors")
            
            for _ in range(num_girls):
                character_tags = generate_character_tags("f", current_scene_tags_set, is_nsfw_category, num_total_chars_in_scene, framing_tag_for_scene_str)
                all_character_specific_tags_list.extend(character_tags)

            for _ in range(num_boys):
                character_tags = generate_character_tags("m", current_scene_tags_set, is_nsfw_category, num_total_chars_in_scene, framing_tag_for_scene_str)
                all_character_specific_tags_list.extend(character_tags)
            
            # Update current_scene_tags_set with character tags for subsequent general choices
            for tag_group_str in all_character_specific_tags_list:
                 for tag_item in tag_group_str.split(','): current_scene_tags_set.add(tag_item.strip())


            # --- More General Tags (Objects, Effects, etc. Post-Character) ---
            if random.random() < 0.2: # Objects
                num_objects = random.randint(0, (2 if num_total_chars_in_scene == 0 else 3))
                for _ in range(num_objects):
                    obj_item = get_weighted_choice(tags_data["tc"], current_scene_tags_set)
                    if obj_item: general_tags_for_scene_list.append(obj_item[0]); current_scene_tags_set.add(obj_item[0])
            
            if random.random() < 0.25: # Effects
                num_effects = random.randint(1, 2)
                for _ in range(num_effects):
                    effect_item = get_weighted_choice(tags_data["tg"], current_scene_tags_set)
                    if effect_item: general_tags_for_scene_list.append(effect_item[0]); current_scene_tags_set.add(effect_item[0])
            
            if random.random() < 0.2: # Year
                year_item = get_weighted_choice(tags_data["tl"], current_scene_tags_set)
                if year_item: general_tags_for_scene_list.append(year_item[0]); current_scene_tags_set.add(year_item[0])

            if num_total_chars_in_scene > 0 and random.random() < 0.1 : # Focus (eV)
                focus_item = get_weighted_choice(tags_data["eV"], current_scene_tags_set) # Pass character flags if eV choices depend on them
                if focus_item: general_tags_for_scene_list.append(focus_item[0]); current_scene_tags_set.add(focus_item[0])
            elif num_total_chars_in_scene == 0 and random.random() < 0.2: # Focus on scenery (eZ)
                 scenery_focus_item = get_weighted_choice(tags_data["eZ"], current_scene_tags_set)
                 if scenery_focus_item: general_tags_for_scene_list.append(scenery_focus_item[0]); current_scene_tags_set.add(scenery_focus_item[0])
            
            # --- Finalize Prompt String ---
            all_tags_for_scene_combined_raw = []
            for tag_group_str in general_tags_for_scene_list + all_character_specific_tags_list:
                for tag_item in tag_group_str.split(","):
                    cleaned_tag = tag_item.strip().replace("_", " ")
                    if cleaned_tag: all_tags_for_scene_combined_raw.append(cleaned_tag)
            
            ordered_unique_tags = list(OrderedDict.fromkeys(all_tags_for_scene_combined_raw))
            ordered_unique_tags = [tag for tag in ordered_unique_tags if tag]

            if not ordered_unique_tags: continue

            # Remove 1girl and 1 boy if they are present
            ordered_unique_tags = [tag for tag in ordered_unique_tags if tag not in ["1girl", "1boy"]]

            # Add the prepend string to the beginning of the prompt
            prepend_str = params["prepend"]
            prepend_terms = prepend_str.split(",")
            prepend_terms = [term.strip() for term in prepend_terms if term.strip()]
            prepend_terms = [term for term in prepend_terms if term not in ordered_unique_tags] # Avoid duplicates
            ordered_unique_tags = prepend_terms + ordered_unique_tags

            processed_tags_for_final_string = []
            for tag in ordered_unique_tags:
                if random.random() < 0.02: processed_tags_for_final_string.append(f"{{{tag}}}")
                else: processed_tags_for_final_string.append(tag)
            
            final_prompt_str = ", ".join(processed_tags_for_final_string)
            all_prompts[current_category_key].append(final_prompt_str)
            generated_prompts_for_category += 1 
        
        if generated_prompts_for_category < num_prompts_per_category:
             print(f"Warning: Only generated {generated_prompts_for_category}/{num_prompts_per_category} prompts for {current_category_key}.")
    return all_prompts

if __name__ == "__main__":
    num_prompts_per_category = 40000  # Reduced for quicker testing
    print(f"Starting generation of {num_prompts_per_category} prompts per category...")
    all_final_prompts = generate_scene_prompts_v2(num_prompts_per_category)

    for category, prompts in all_final_prompts.items():
        filename = f"{category}.txt"
        with open(filename, "w", encoding="utf-8") as f_out:
            for prompt in prompts:
                f_out.write(prompt + "\n")
        print(f"Written {len(prompts)} prompts to {filename}")
    print("Generation complete.")

