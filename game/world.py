import random as rd
from .game_object import GameObject
from .characters import Orc, Elf, Human
from .items import HealingPotion, DamagePotion, Weapon, Armor


class Enemy(GameObject):
    """Base class for all enemies in the game."""

    def __init__(self, name, description, character_class):
        super().__init__(name, description)
        self.character = character_class(name)
        # Give enemies some random items they might drop
        self.setup_loot()

    def get_desc(self):
        return f"{self.description}"

    def setup_loot(self):
        """Set up potential loot drops for this enemy."""
        # 50% chance to have an item
        if rd.random() < 0.5:
            loot_options = [
                HealingPotion(healing_amount=rd.randint(5, 15)),
                DamagePotion(damage_amount=rd.randint(5, 12)),
                Weapon(f"{self.character.race} Blade", f"A weapon taken from a defeated {self.character.race}.",
                       rd.randint(1, 3)),
                Armor(f"{self.character.race} Armor", f"Armor scavenged from a fallen {self.character.race}.",
                      rd.randint(1, 2))
            ]
            self.character.inventory = [rd.choice(loot_options)]


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
        self.current_region = "forest"  # default starting region
        self.populate_world()

    def populate_world(self):
        """Populates the world with random enemies."""
        enemy_types = self.regions.get(self.current_region, [])
        self.enemies = []  # Clear existing enemies

        for _ in range(5):  # Generate 5 random enemies for now
            if enemy_types:
                character_class, description = rd.choice(enemy_types)
                name = f"{character_class.__name__}_{rd.randint(1, 100)}"
                self.enemies.append(Enemy(name, description, character_class))

    def change_region(self, new_region):
        """Change the player's region and re-populate the world with enemies."""
        if new_region.lower() in self.regions:
            self.current_region = new_region.lower()
            print(f"You have entered the {new_region}!")
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

            # Start combat with the enemy
            from .combat import Combat
            combat = Combat(self.player, enemy.character)

            print(f"You have encountered {enemy.name}!")
            print(enemy.get_desc())

            combat.start_combat()

            # If the player won, give them any loot and remove the enemy
            if self.player.is_alive() and not enemy.character.is_alive():
                self.handle_victory(enemy)
                self.enemies.remove(enemy)

            return enemy
        else:
            return None

    def handle_victory(self, enemy):
        """Handle the aftermath of defeating an enemy."""
        print(f"You have defeated {enemy.name}!")

        # Award loot if the enemy has any
        if hasattr(enemy.character, 'inventory') and enemy.character.inventory:
            print("You found some items!")
            for item in enemy.character.inventory:
                print(f"  - {item.name}: {item.description}")
                self.player.add_item(item)