from handlers.generic_handler import logger
from utils.db import create_collection, save_to_db, load_from_db


class QuestHandler:
    def __init__(self):
        self.state = {}

    def start_quest(self, user_id, quest_data):
        self.state[user_id] = {
            "user_id": user_id,
            "current_step": "start",
            "goal": quest_data["quest_goal"],
            "progress": {},
            "event_log": [],
            "reward": quest_data["quest_reward"],
            "description": quest_data["quest_description"]
        }

    def update_quest_state(self, user_id, action):
        state = self.state[user_id]
        # Логіка оновлення стану на основі дії гравця
        state['event_log'].append(action)
        # Збереження нового стану
        self.state[user_id] = state

    async def save_quest_state(self, user_id):
        quest_state = self.state[user_id]
        await create_collection("list_of_quests", "user_id")
        await save_to_db("list_of_quests", user_id, quest_state)
        logger.info("Quest state save successful")

    async def load_quest_state(self, user_id):
        result = await load_from_db("list_of_quests", user_id)
        if result:
            self.state[user_id] = result
            logger.info("Quest load successful")
            return True
        else:
            self.state[user_id] = {}
            return False


# quest_data = {'quest_goal': 'Retrieve a stolen gem from the bandit camp north of Eldermere.',
#               'quest_reward': 'A masterfully crafted sword and a selection of enchanted gems.',
#               'quest_description': 'Garin tells you that a precious gem, known for enhancing the strength of weapons, was stolen by a band of notorious bandits. He offers to forge you an exceptional sword if you can bring it back. Along the way, you might also discover other treasures that could aid you on your journey.'}
#
# quest = QuestHandler(quest_data, "Elderring")
# quest.start_quest(873674365)
# result = quest.save_quest_state(873674365)
# print(result)