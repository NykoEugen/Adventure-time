from random import randint

from utils.load_json import load_json

game_context = load_json("text-templates/game-context.json")
num_actions = randint(0, 5)
text = load_json("text-templates/prompt_test.json")
prompt = text["base_prompt"].format(game_context=game_context ,action="Fight", num_action=num_actions)

print(prompt)
