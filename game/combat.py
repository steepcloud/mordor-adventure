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

        # Special attack logic (TODO: implement)
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
        action = input("Do you want to 'attack' or 'flee'? ").strip().lower()

        if action == "attack":
            attack_type = self.choose_attack_type()
            self.attack(self.player, self.enemy, attack_type)
        elif action == "flee":
            if self.attempt_flee():
                print(f"{self.player.name} successfully flees from {self.enemy.name}!")
            else:
                print(f"{self.player.name} tries to flee but is blocked by {self.enemy.name}!")
                self.attack(self.enemy, self.player)
        else:
            print("Invalid action. Choose 'attack' or 'flee'.")

    def enemy_turn(self):
        """Handle the enemy's turn."""
        print("\nIt's the enemy's turn!")
        attack_type = "special" if rd.random() < 0.3 else "normal"  # 30% chance for a special attack
        self.attack(self.enemy, self.player, attack_type)

    def choose_attack_type(self):
        """Choose an attack type for the player."""
        attack_choice = rd.choice(["normal", "special"])
        if attack_choice == "normal":
            print("You choose a normal attack.")
        else:
            print("You choose a special attack!")
        return attack_choice

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
