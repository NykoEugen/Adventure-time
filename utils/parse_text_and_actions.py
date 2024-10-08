import json
import re


def parse_text_and_actions(text):
    # Перевіряємо наявність "Possible actions:" з або без зірочок
    if "**Possible actions:**" in text or "Possible actions:" in text:
        # Розділяємо текст за "Possible actions:" зі зірочками або без них
        if "**Possible actions:**" in text:
            main_text, actions_text = text.split("**Possible actions:**", 1)
        else:
            main_text, actions_text = text.split("Possible actions:", 1)

        main_text = main_text.strip()

        # Перевіряємо, чи є коми для розділення дій
        if ',' in actions_text:
            actions = [action.strip() for action in actions_text.split(',')]
        else:
            # Видаляємо нумерацію та зайві символи перед варіантами дій
            actions_text = re.sub(r'[\d\.\-]+', '', actions_text)
            # Розділяємо варіанти дій за новими рядками
            actions = [action.strip() for action in actions_text.splitlines() if action.strip()]

        # Видаляємо зірочки на початку і в кінці кожної дії
        actions = [re.sub(r'^\*+|\*+$', '', action).strip() for action in actions]

        actions_dict = {index + 1: action for index, action in enumerate(actions)}
    else:
        main_text = text.strip()
        actions_dict = {1: "Continue"}

    return main_text, actions_dict


def parse_quest_text(text):
    quest_data = {}
    # Витягти словник з описом квесту

    pattern = re.search(r"\{.*\}", text)
    if pattern:
        quest_dict_str = pattern.group(0)
        try:
            quest_data = json.loads(quest_dict_str.replace("'", "\""))  # Заміняємо одинарні лапки на подвійні
        except json.JSONDecodeError:
            raise ValueError("Неможливо перетворити рядок на словник")

    # Витягти можливі дії
    if "Possible actions:" in text:
        description, actions_text = text.split("Possible actions:", 1)
    else:
        description = text.strip()
        actions_text = ""

    # Обрізаємо зайві пробіли
    description = description.strip()

    # Якщо є можливі дії, форматуємо їх в словник
    actions_dict = {}
    if actions_text.strip():
        actions_list = [action.strip() for action in actions_text.split(',') if action.strip()]
        actions_dict = {index + 1: action for index, action in enumerate(actions_list)}

    return quest_data, actions_dict

# main_text, actions_dict = parse_text_and_actions("As Casper pushed open the heavy wooden door of the forge, the heat enveloped him like a warm embrace, a stark contrast to the crispness outside. The blacksmith, a burly man with arms like oak branches, looked up from his anvil, wiping sweat from his brow with a leather apron. \"Welcome, young traveler! Come to see the finest blades and armor in Eldenbrook? I've just finished a sword that could slice through armor like butter!\" The sound of hammer striking steel reverberated around the room, as molten metal glowed fiercely in the hearth, sending sparks dancing into the air.\n\nPossible actions: **Approach creature**, Retreat further")
# main_text, actions_dict = parse_text_and_actions("{'quest_goal': 'Retrieve a stolen gem from the bandit camp north of Eldermere.', 'quest_reward': 'A masterfully crafted sword and a selection of enchanted gems.', 'quest_description': 'Garin tells you that a precious gem, known for enhancing the strength of weapons, was stolen by a band of notorious bandits. He offers to forge you an exceptional sword if you can bring it back. Along the way, you might also discover other treasures that could aid you on your journey.'} Possible actions: Gather supplies, Ask for details")
# print(main_text)
# print(actions_dict)