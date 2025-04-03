import random as rd
from .combat import Combat
from .characters import Orc, Elf, Human

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
        self.regions = {
            "forest": [
                (Orc, "A wild Orc warrior with great strength, lurking in the shadows."),
                (Orc, "An Orc with a scarred face and a fiery temper."),
                (Orc, "A cunning Orc archer, ready to strike from a distance."),
                (Elf, "A mysterious Elf with glowing eyes and swift feet."),
                (Elf, "An Elf with a silver bow, capable of incredible precision."),
                (Elf, "A graceful Elf with sharp eyes and an unyielding will."),
            ],
            "plains": [
                (Human, "A wandering Human warrior, bearing the marks of many battles."),
                (Human, "A young Human knight, eager to prove their worth."),
                (Human, "An old, weathered Human with a hardened look."),
                (Orc, "A lone Orc patrol, stomping through the grasslands."),
                (Orc, "A brutish Orc carrying a massive club, ready to crush anything in its path."),
            ],
            "mountains": [
                (Orc, "A tough Orc warrior with a battle axe, his skin hardened by the cold."),
                (Orc, "A large Orc with fur-lined armor, built for mountain warfare."),
                (Orc, "An Orc berserker, bloodthirsty and relentless."),
                (Elf, "An agile Elf adept at mountain climbing, blending with the rocky terrain."),
                (Elf, "A stoic Elf with a longbow, perched on a mountain peak."),
                (Human, "A hardened Human explorer, wrapped in furs and equipped with climbing gear."),
            ],
        }
        self.current_region = "forest" # default starting region
        self.populate_world()

    def populate_world(self):
        """Populates the world with random enemies."""
        #from .characters import Orc, Elf, Human
        enemy_types = self.regions.get(self.current_region, [])

        for _ in range(5):  # Generate 5 random enemies for now
            if enemy_types:
                character_class, description = rd.choice(enemy_types)
                name = f"{character_class.__name__}_Enemy_{rd.randint(1, 100)}"
                self.enemies.append(Enemy(name, description, character_class))

    def change_region(self, new_region):
        """Change the player's region and re-populate the world with enemies."""
        if new_region in self.regions:
            self.current_region = new_region
            print(f"You have entered the {new_region}!")
            self.enemies.clear()
            self.populate_world()
        else:
            print(f"Invalid region: {new_region}. Staying in {self.current_region}.")

    def get_enemy_by_name(self, name):
        """Returns an enemy object by name."""
        for enemy in self.enemies:
            if enemy.name.lower() == name.lower():
                return enemy
        return None

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
