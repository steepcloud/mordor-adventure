import random as rd
from .combat import Combat

class GameObject:
    """Base class for all objects in the game."""
    objects = {}

    def __init__(self, name, description):
        self.name = name
        self.description = description
        GameObject.objects[self.name.lower()] = self

    def get_desc(self):
        return self.description

    @staticmethod
    def get_article(word):
        return "An" if word.lower()[0] in "aeiou" else "A"


class Enemy(GameObject):
    """Base class for all enemies in the game."""

    def __init__(self, name, description, character_class):
        super().__init__(name, description)
        self.character = character_class(name)

    def get_desc(self):
        return f"{self.character.get_desc()} {self.description}"


class World:
    """Represents the game world, with NPCs and enemies."""

    def __init__(self, player):
        self.enemies = []
        self.player = player

    def populate_world(self):
        """Populates the world with random enemies."""
        from .characters import Orc, Elf, Human

        enemy_types = [(Orc, "A menacing Orc warrior."),
                       (Elf, "A graceful Elf with sharp eyes."),
                       (Human, "A brave Human warrior.")]

        for _ in range(5):  # Generate 5 random enemies for now
            character_class, description = rd.choice(enemy_types)
            name = f"{character_class.__name__}_Enemy_{rd.randint(1, 100)}"
            self.enemies.append(Enemy(name, description, character_class))

    def encounter_enemy(self):
        """Randomly encounters an enemy."""
        if self.enemies:
            enemy = rd.choice(self.enemies)
            print(f"You have encountered {enemy.get_desc()}")
            combat = Combat(self.player, enemy.character)
            combat.start_combat()
        else:
            print("There are no enemies left to encounter.")
            return None
