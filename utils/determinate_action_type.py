event_keywords = {
    "battle": ["fight", "attack", "defend", "battle", "strike", "draw"],
    "quest": ["quest", "search", "find", "retrieve", "seek", "request"],
    "dialogue": ["talk", "speak", "ask", "discuss", "question", "inquire further"],
    "exploration": ["explore", "look", "discover", "investigate", "examine", "search", "observe"],
    "trade": ["buy", "sell", "trade", "purchase"],
    "rest": ["rest", "sleep", "wait", "recover"],
    "generic": ["venture into", "listen for", "turn", "approach", "retreat", "visit"]
}

# function for determinate action type by known dict
def determine_action_types(actions_dict) -> dict:
    result_dict = {}
    counter = {}  # counter for even actions
    for key, action in actions_dict.items():
        action_lower = action.lower()
        action_type = "generic"  # default type

        # Explore action type by checking dict
        for event_type, keywords in event_keywords.items():
            if any(keyword in action_lower for keyword in keywords):
                action_type = event_type
                break

        # Find out similar type
        if action_type in result_dict:
            # if yes add index
            if action_type not in counter:
                counter[action_type] = 1
            counter[action_type] += 1
            indexed_action_type = f"{action_type}_{counter[action_type]}"
        else:
            # if not only action type
            indexed_action_type = action_type
            counter[action_type] = 1  # initialize counter for type

        # add action to result
        result_dict[indexed_action_type] = action

    return result_dict
