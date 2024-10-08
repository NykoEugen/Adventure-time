from handlers.generic_handler import logger


class QuestHandler:
    def __init__(self, quest_data, location):
        self.quest_data = quest_data
        self.location = location
        self.state = {}

    def start_quest(self, user_id):
        self.state[user_id] = {
            "current_step": "start",
            "goal": self.quest_data["quest_goal"],
            "progress": {},
            "location": self.location,
            "event_log": [],
            "reward": self.quest_data["quest_reward"],
            "description": self.quest_data["quest_description"]
        }

    def update_quest_state(self, user_id, action):
        state = self.state[user_id]
        # Логіка оновлення стану на основі дії гравця
        state['event_log'].append(action)
        # Збереження нового стану
        self.state[user_id] = state

    def generate_quest_prompt(self, user_id, action, num_actions=3):
        state = self.state[user_id]
        return (
            f"Location: {state['location']}\n"
            f"Quest: {state['goal']}\n"
            f"Player action: {action}\n"
            f"Please describe what happens next, list {num_actions} possible actions."
        )
