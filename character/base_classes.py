from handlers.db import save_hero_changes, db


class Character:
    def __init__(self, character_id, name, character_type, strength, dexterity, intelligence, endurance, charisma):
        self.character_id = character_id
        self.name = name
        self.character_type = character_type
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.endurance = endurance
        self.charisma = charisma
        self.health = self.endurance * 10
        self.mana = self.intelligence * 10
        self.abilities = []
        self.equipment = {
            "cloak": None,
            "boots": None,
            "gloves": None,
            "weapon": None,
            "helmet": None
        }
        self.inventory = []

    #Base actions
    def attack(self, target):
        # Атака базується на силі персонажа
        damage = self.strength
        target.health -= damage
        return f"{self.name} атакує {target.name} і завдає {damage} шкоди!"

    def defend(self):
        # Захист може зменшити отриману шкоду
        defense_boost = self.endurance * 0.3  # Бонус захисту
        return f"{self.name} захищається, зменшуючи наступний удар на {defense_boost}!"

    #Abilities actions
    def use_ability(self, ability, target):
        if ability in self.abilities:
            if self.mana >= ability.mana_cost:
                self.mana -= ability.mana_cost
                return ability.use(self, target)
            else:
                return f"{self.name} не вистачає мани для {ability.name}."
        else:
            return f"У {self.name} немає такої здібності."

    #Inventory methods
    def add_item(self, item) -> str:
        if len(self.inventory) < 3:
            self.inventory.append(item)
            message = "Предмет додано"
            return message
        else:
            message = "Інвентар заповнений!"
            return message

    def use_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            # Наприклад, якщо предмет відновлює здоров'я
            if item == "Healing Potion":
                self.health += 20
                return f"{self.name} використовує {item} і відновлює 20 здоров'я!"
        else:
            return f"У {self.name} немає {item} в інвентарі."

    def remove_item(self, item) -> str:
        if item in self.inventory:
            self.inventory.remove(item)
            message = "Предмет видалено"
            return message
        else:
            message = "Предмет не знайдено в інвентарі."
            return message

    async def save_character_state(self):
        all_param = {
                        "character_id": self.character_id,
                        "name": self.name,
                        "character_type": self.character_type,
                        "strength": self.strength,
                        "dexterity": self.dexterity,
                        "intelligence": self.intelligence,
                        "endurance": self.endurance,
                        "charisma": self.charisma,
                        "health": self.health,
                        "mana": self.mana,
                        "abilities": self.abilities,
                        "equipment": self.equipment,
                    }
        await save_hero_changes(self.character_id, all_param)


class Warrior(Character):
    def __init__(self, character_id, name):
        super().__init__(character_id, name, "Warrior", strength=15, dexterity=10, intelligence=5, endurance=12, charisma=6)
        self.abilities = ["Shield Bash", "Battle Cry"]  # Здібності воїна


class Mage(Character):
    def __init__(self, character_id, name):
        super().__init__(character_id, name, "Mage", strength=5, dexterity=8, intelligence=15, endurance=6, charisma=9)
        self.abilities = ["Fireball", "Teleport"]  # Здібності мага


class Archer(Character):
    def __init__(self,character_id, name):
        super().__init__(character_id, name, "Archer", strength=8, dexterity=15, intelligence=6, endurance=10, charisma=9)
        self.abilities = ["Quick Shot", "Stealth"]  # Здібності лучника
