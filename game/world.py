import random as rd
from .game_object import GameObject
from .characters import Orc, Elf, Human
from .items import HealingPotion, DamagePotion, Weapon, Armor


class Enemy(GameObject):
    """Base class for all enemies in the game."""

    def __init__(self, name, description, character_class):
        super().__init__(name, description)
        self.character = character_class(name)
        # give enemies some random items they might drop
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
        self.enemies = []  # clear existing enemies

        available_types = enemy_types.copy()

        for _ in range(5):  # generate 5 random enemies
            if not available_types:
                # if we've used all the types, refill
                available_types = enemy_types.copy()
            
            if available_types:
                # select a random enemy type and remove it from available_types
                type_index = rd.randint(0, len(available_types) - 1)
                character_class, description = available_types.pop(type_index)

                # generate a unique name with race and number
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
        """Randomly selects an enemy from the current region."""
        if self.enemies:
            return rd.choice(self.enemies)
        else:
            return None
        
    def handle_victory(self, enemy):
        """Handle the aftermath of defeating an enemy."""
        print(f"You have defeated {enemy.name}!")

        # award loot if the enemy has any
        if hasattr(enemy.character, 'inventory') and enemy.character.inventory:
            print("You found some items!")
            for item in enemy.character.inventory:
                print(f"  - {item.name}: {item.description}")
                self.player.add_item(item)
    
    def give_reward(self, player):
        """Give rewards after combat and return message."""
        enemy = self.get_last_defeated_enemy()
        if not enemy:
            return None
        
        reward_message = []
        reward_message.append(f"You have defeated {enemy.name}!")
        
        # award loot if the enemy has any
        if hasattr(enemy.character, 'inventory') and enemy.character.inventory:
            reward_message.append("You found some items!")
            for item in enemy.character.inventory:
                reward_message.append(f"  - {item.name}: {item.description}")
                player.add_item(item)
        
        # remove the enemy from the world
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        
        return "\n".join(reward_message)

    def get_last_defeated_enemy(self):
        """Get the last defeated enemy (for reward purposes)."""
        for enemy in self.enemies:
            if hasattr(enemy, 'character') and enemy.character.health <= 0:
                return enemy
        return None