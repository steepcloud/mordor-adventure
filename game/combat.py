import random as rd


class Combat:
    """Handles combat between the player and enemies."""

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_order = self.determine_turn_order()

    def determine_turn_order(self):
        """Determine who attacks first using a random coin flip."""
        return "player" if rd.choice(["heads", "tails"]) == "heads" else "enemy"

    def attack(self, attacker, target, attack_type="normal"):
        """Handle an attack from the attacker to the target."""
        # Critical hit chance (20% chance for critical hit)
        is_critical = rd.random() < 0.2
        damage = rd.randint(1, attacker.attack_power)

        # Apply critical hit bonus
        if is_critical:
            damage *= 2
            print(f"Critical hit! {attacker.name} deals double damage!")

        # Special attack logic
        if attack_type == "special":
            damage += rd.randint(1, 3)  # Special attacks do more damage
            print(f"{attacker.name} uses a special attack!")

        # Apply the damage to the target
        target.health -= damage

        # Message about the attack
        print(f"{attacker.name} attacks {target.name} for {damage} damage!")
        print(f"{target.name} now has {target.health} HP.")

    def check_for_death(self):
        """Check if either the player or the enemy is dead."""
        if self.player.health <= 0:
            print(f"{self.player.name} has been defeated!")
            return True
        elif self.enemy.health <= 0:
            print(f"{self.enemy.name} has been defeated!")
            return True
        return False

    def start_combat(self):
        """Initiate the combat loop with random turn order."""
        print(f"The battle begins! {self.turn_order.capitalize()} attacks first.\n")

        while True:
            if self.turn_order == "player":
                self.player_turn()
                if self.check_for_death():
                    break
                self.turn_order = "enemy"  # Switch turns
            else:
                self.enemy_turn()
                if self.check_for_death():
                    break
                self.turn_order = "player"  # Switch turns

    def player_turn(self):
        """Handle the player's turn."""
        print("\nIt's your turn!")
        print("Available actions: 'attack', 'special', 'use item', 'flee'")
        action = input("What will you do? ").strip().lower()

        if action == "attack":
            self.attack(self.player, self.enemy, "normal")
        elif action == "special":
            self.attack(self.player, self.enemy, "special")
        elif action == "use item":
            if hasattr(self.player, 'inventory') and self.player.inventory:
                self.use_item()
            else:
                print("You don't have any items to use.")
                self.player_turn()  # Try again
        elif action == "flee":
            if self.attempt_flee():
                print(f"{self.player.name} successfully flees from {self.enemy.name}!")
                return  # Exit combat
            else:
                print(f"{self.player.name} tries to flee but is blocked by {self.enemy.name}!")
                self.attack(self.enemy, self.player)
        else:
            print("Invalid action. Try again.")
            self.player_turn()  # Try again

    def use_item(self):
        """Handle using an item from the player's inventory."""
        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            print("You don't have any items to use.")
            return

        print("\nYour inventory:")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.name}: {item.description}")

        choice = input("Enter the number of the item to use (or 'cancel'): ").strip().lower()
        if choice == 'cancel':
            self.player_turn()  # Go back to action selection
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(self.player.inventory):
                item = self.player.inventory[index]
                result = item.use(self.player, self.enemy)
                print(result)
                # Remove consumable items after use
                if item.consumable:
                    self.player.inventory.pop(index)
            else:
                print("Invalid item number.")
                self.use_item()  # Try again
        except ValueError:
            print("Please enter a valid number or 'cancel'.")
            self.use_item()  # Try again

    def enemy_turn(self):
        """Handle the enemy's turn."""
        print("\nIt's the enemy's turn!")
        attack_type = "special" if rd.random() < 0.3 else "normal"  # 30% chance for a special attack
        self.attack(self.enemy, self.player, attack_type)

    def attempt_flee(self):
        """
        Determines if the player can flee from the enemy.
        A higher chance of success if the player is stronger or if the enemy is weak.
        :return: True if the flee chance is 50% or higher, False otherwise.
        """
        flee_chance = rd.random()
        player_strength = self.player.health  # Using player health as strength for now
        enemy_strength = self.enemy.health  # Same for the enemy

        if player_strength > enemy_strength:
            flee_chance += 0.2

        if player_strength < enemy_strength:
            flee_chance -= 0.2

        flee_chance = max(0.0, min(flee_chance, 1.0))

        return flee_chance >= 0.5