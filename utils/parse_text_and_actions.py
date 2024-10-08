import re


def parse_text_and_actions(text):
    if "**Possible actions:**" in text:
        main_text, actions_text = text.split("**Possible actions:**", 1)
        main_text = main_text.strip()

        if ',' in actions_text:
            actions = [action.strip() for action in actions_text.split(',')]
        else:
            actions_text = re.sub(r'[\d\.\-]+', '', actions_text)
            actions = [action.strip() for action in actions_text.splitlines() if action.strip()]

        actions_dict = {index + 1: action for index, action in enumerate(actions)}
    else:
        main_text = text.strip()
        actions_dict = {1: "Continue"}

    return main_text, actions_dict


# main_text, actions_dict = parse_text_and_actions("As Casper pushed open the heavy wooden door of the forge, the heat enveloped him like a warm embrace, a stark contrast to the crispness outside. The blacksmith, a burly man with arms like oak branches, looked up from his anvil, wiping sweat from his brow with a leather apron. \"Welcome, young traveler! Come to see the finest blades and armor in Eldenbrook? I've just finished a sword that could slice through armor like butter!\" The sound of hammer striking steel reverberated around the room, as molten metal glowed fiercely in the hearth, sending sparks dancing into the air.\n\n**Possible actions:** Approach creature, Retreat further")
#
# print(main_text)
# print(actions_dict)