import random as rd


class Combat:
    """Handles combat between the player and enemies."""

    def __init__(self, player, enemy):
        self.player = player
        # handle both direct character objects and enemy containers
        if hasattr(enemy, 'character'):
            self.enemy = enemy.character
        else:
            self.enemy = enemy
        self.turn_order = self.determine_turn_order()
        self.combat_log = []  # store messages instead of printing directly
        self.combat_active = True

    def determine_turn_order(self):
        """Determine who attacks first using a random coin flip."""
        return "player" if rd.choice(["heads", "tails"]) == "heads" else "enemy"

    def log(self, message):
        """Add a message to the combat log."""
        self.combat_log.append(message)

    def attack(self, attacker, target, attack_type="normal"):
        """Handle an attack from the attacker to the target."""
        # critical hits provide excitement and variability in combat
        is_critical = rd.random() < 0.2  # 20% chance for critical hit
        damage = rd.randint(1, attacker.attack_power)

        # apply critical hit bonus
        if is_critical:
            damage *= 2
            self.log(f"Critical hit! {attacker.name} deals double damage!")

        # special attacks are more powerful but limited resource
        if attack_type == "special":
            damage += rd.randint(1, 3)  # bonus damage for special attacks
            self.log(f"{attacker.name} uses a special attack!")

        # apply damage and ensure health never goes below zero
        target.health = max(0, target.health - damage)

        self.log(f"{attacker.name} attacks {target.name} for {damage} damage!")
        self.log(f"{target.name} now has {target.health} HP.")

    def check_for_death(self):
        """Check if either the player or the enemy is dead."""
        if self.player.health <= 0:
            self.player.health = 0
            self.log(f"{self.player.name} has been defeated!")
            self.combat_active = False
            return True
        elif self.enemy.health <= 0:
            self.enemy.health = 0
            self.log(f"{self.enemy.name} has been defeated!")
            self.combat_active = False
            return True
        return False

    def start_combat(self):
        """Initiate the combat loop with random turn order."""
        self.combat_log = []

        self.log(f"You face {self.enemy.name}!")

        if hasattr(self.enemy, 'description'):
            self.log(f"{self.enemy.description}")
        self.log(f"The battle begins! {self.turn_order.capitalize()} attacks first.\n")

        if self.turn_order == "enemy":
            self.enemy_turn()
            if not self.check_for_death():
                self.turn_order = "player"
                self.log("\nIt's your turn!")
                self.log("Available actions: 'attack', 'special', 'use item', 'flee'")
        else:
            self.log("\nIt's your turn!")
            self.log("Available actions: 'attack', 'special', 'use item', 'flee'")

        return self.get_combat_state()

    def get_combat_state(self):
        """Return the current combat state as a dictionary"""
        return {
            "player": {
                "name": self.player.name,
                "health": self.player.health,
                "max_health": self.player.max_health
            },
            "enemy": {
                "name": self.enemy.name,
                "health": self.enemy.health,
                "max_health": getattr(self.enemy, 'max_health', self.enemy.health)
            },
            "active": self.combat_active,
            "turn": self.turn_order,
            "log": self.combat_log,
            "victory": self.enemy.health <= 0 and self.player.health > 0 if not self.combat_active else None
        }

    def process_action(self, action, item_index=None, item_name=None):
        """Process a single combat action and return the updated state."""
        self.combat_log = []  # clear previous messages for this turn

        # enforce turn order - only process player actions during player turn
        if self.turn_order != "player":
            self.log("It's not your turn yet!")
            return self.get_combat_state()

        # handle the various action types
        if action == "attack":
            self.attack(self.player, self.enemy, "normal")
        elif action == "special":
            self.attack(self.player, self.enemy, "special")
        elif action == "use_item":
            # support both index and name-based item usage
            if item_index is not None:
                self.use_item_by_index(item_index)
            elif item_name is not None:
                self.use_item_by_name(item_name)
            else:
                self.log("No item specified.")
                return self.get_combat_state()
        elif action == "flee":
            # fleeing is not guaranteed - adds strategic decisions
            if self.attempt_flee():
                self.log(f"{self.player.name} successfully flees from {self.enemy.name}!")
                self.combat_active = False
                return self.get_combat_state()
            else:
                self.log(f"{self.player.name} tries to flee but is blocked by {self.enemy.name}!")
        else:
            # provide helpful feedback for invalid actions
            self.log(f"Invalid combat action: '{action}'")
            self.log("Available actions: 'attack', 'special', 'use_item', 'flee'")
            self.log(f"\nYou are fighting {self.enemy.name} ({self.enemy.health}/{self.enemy.max_health} HP)")

            return self.get_combat_state()

        # check if combat is over after player's action
        if self.check_for_death():
            return self.get_combat_state()

        # if combat continues, proceed with enemy turn
        self.turn_order = "enemy"
        self.enemy_turn()

        # check again if combat is over after enemy's action
        if self.check_for_death():
            return self.get_combat_state()

        # prepare for next player turn
        self.turn_order = "player"
        self.log("\nIt's your turn!")
        self.log("Available actions: 'attack', 'special', 'use item', 'flee'")

        return self.get_combat_state()

    def use_item_by_index(self, index):
        """Use an item by its inventory index."""
        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            self.log("You don't have any items to use.")
            return False

        try:
            if 0 <= index < len(self.player.inventory):
                item = self.player.inventory[index]

                if hasattr(item, 'damage_amount'):
                    result = item.use(self.player, self.enemy)
                else:
                    result = item.use(self.player)

                self.log(result)

                # remove consumable items after use
                if item.consumable:
                    self.player.inventory.pop(index)
                return True
            else:
                self.log("Invalid item index.")
                return False
        except (ValueError, IndexError):
            self.log("Error using item.")
            return False

    def use_item_by_name(self, name):
        """Use an item by its name."""
        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            self.log("You don't have any items to use.")
            return False

        for i, item in enumerate(self.player.inventory):
            if item.name.lower() == name.lower():
                return self.use_item_by_index(i)

        self.log(f"You don't have an item called '{name}'.")
        return False

    def player_turn(self):
        """Handle the player's turn."""
        print("\nIt's your turn!")
        print("Available actions: 'attack', 'special', 'use item', 'flee'")
        action = input("What will you do? ").strip().lower()

        if action == "attack":
            return self.process_action("attack")
        elif action == "special":
            return self.process_action("special")
        elif action == "use item":
            if hasattr(self.player, 'inventory') and self.player.inventory:
                print("Your inventory:")
                for i, item in enumerate(self.player.inventory):
                    print(f"{i + 1}. {item.name}")

                try:
                    item_idx = int(input("Enter item number to use: ")) - 1
                    return self.process_action("use_item", item_index=item_idx)
                except (ValueError, IndexError):
                    print("Invalid selection.")
                    return self.player_turn()  # try again
            else:
                print("You don't have any items to use.")
                return self.player_turn()
        elif action == "flee":
            return self.process_action("flee")
        else:
            print("Invalid action. Try again.")
            self.player_turn()  # try again

    def enemy_turn(self):
        """Handle the enemy's turn."""
        self.log("\nIt's the enemy's turn!")
        # enemies occasionally use special attacks for variety
        attack_type = "special" if rd.random() < 0.2 else "normal"  # 30% chance for a special attack
        self.attack(self.enemy, self.player, attack_type)

    def attempt_flee(self):
        """
        Determines if the player can flee from the enemy.
        A higher chance of success if the player is stronger or if the enemy is weak.
        :return: True if the flee chance is 50% or higher, False otherwise.
        """
        # flee chance is affected by relative strength of combatants
        flee_chance = rd.random()
        player_strength = self.player.health  # using player health as strength for now
        enemy_strength = self.enemy.health  # same for the enemy

        # easier to flee from weakened enemies
        if player_strength > enemy_strength:
            flee_chance += 0.2

        # harder to flee when you're weaker
        if player_strength < enemy_strength:
            flee_chance -= 0.2

        flee_chance = max(0.0, min(flee_chance, 1.0))

        # 50% threshold for successful fleeing
        return flee_chance >= 0.5