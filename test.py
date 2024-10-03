from utils.load_json import load_texts

text = load_texts("text-templates/game-promts.json")
intro = text["intro"].format(character_name="Astro", character_type="Warrior")
print(intro)