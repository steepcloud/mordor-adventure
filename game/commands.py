from .characters import Character
from .world import GameObject
from .items import Item


def process_command(command, game_engine):
    """Process a user command and return the result."""
    if not command:
        return "Please enter a command."
    
    words = command.strip().lower().split()
    verb = words[0]
    noun = ' '.join(words[1:]) if len(words) > 1 else None
    
    if verb == "help":
        return help_command()
    
    elif verb == "look":
        return look_around(game_engine.world)
    
    elif verb == "regions":
        return show_regions(game_engine.world)
    
    elif verb == "travel" and noun:
        return travel(game_engine.world, noun)
    elif verb == "travel":
        return "Travel where? Type 'regions' to see available destinations."
    
    elif verb == "enemies":
        return show_enemies(game_engine.world)
    
    elif verb == "examine" and noun:
        return examine(noun)
    elif verb == "examine":
        return "Examine what?"
    
    elif verb == "attack" and noun:
        enemy = game_engine.world.get_enemy_by_name(noun)
        if enemy:
            from .combat import Combat
            print(f"{game_engine.player.name} initiates combat with {enemy.name}!")
            combat = Combat(game_engine.player, enemy)
            combat.start_combat()
            return "" 
        else:
            return f"No enemy named '{noun}' found."
    elif verb == "attack":
        return "Attack what? Specify an enemy name."
    
    elif verb == "encounter":
        enemy = game_engine.world.encounter_enemy()
        if enemy:
            from .combat import Combat
            print(f"{game_engine.player.name} encounters {enemy.name}!")
            combat = Combat(game_engine.player, enemy)
            combat.start_combat()
            return "" 
        else:
            return "No enemies to encounter."
    
    elif verb == "stats":
        return show_stats(game_engine.player)
    
    elif verb == "inventory":
        return show_inventory(game_engine.player)
    
    elif verb == "use" and noun:
        return use_item(game_engine.player, noun)
    elif verb == "use":
        return "Use what? Specify an item number or name."
    
    else:
        return "Unknown command. Type 'help' for a list of commands."


def examine(noun):
    """Returns the description of an object or character in the game."""
    noun = noun.lower()
    if noun in GameObject.objects:
        return GameObject.objects[noun].get_desc()
    return "There is nothing special here."


def attack(player, noun):
    """Handles attacking an NPC or character in the game."""
    noun = noun.lower()
    if noun in GameObject.objects and isinstance(GameObject.objects[noun], Character):
        return player.attack(GameObject.objects[noun])
    return "You cannot attack that!"


def show_stats(player):
    """Display character statistics."""
    return player.show_stats()


def show_inventory(player):
    """Display the player's inventory."""
    if not player.inventory:
        return "Your inventory is empty."

    inventory_text = "Your inventory:\n"
    for i, item in enumerate(player.inventory, 1):
        equipped = ""
        if hasattr(item, 'equipped') and item.equipped:
            equipped = " (equipped)"
        inventory_text += f"  {i}. {item.name}{equipped}: {item.description}\n"

    return inventory_text.strip()


def use_item(player, item_name_or_num):
    """Use an item from inventory."""
    if not player.inventory:
        return "Your inventory is empty."

    try:
        # check if the parameter is a number
        item_index = int(item_name_or_num) - 1
        if 0 <= item_index < len(player.inventory):
            item = player.inventory[item_index]
            result = item.use(player)
            if item.consumable:
                player.inventory.pop(item_index)
            return result
        else:
            return f"Invalid item number. You have {len(player.inventory)} items."
    except ValueError:
        # if not a number, search by name
        for item in player.inventory:
            if item.name.lower() == item_name_or_num.lower():
                result = item.use(player)
                if item.consumable:
                    player.inventory.remove(item)
                return result
        return f"No item named '{item_name_or_num}' found in your inventory."


def show_regions(world):
    """Display all available regions."""
    regions_text = "Available regions:\n"
    for region in world.regions.keys():
        if region == world.current_region:
            regions_text += f"  {region} (current)\n"
        else:
            regions_text += f"  {region}\n"
    return regions_text.strip()


def show_enemies(world):
    """Display all enemies in the current region."""
    if not world.enemies:
        return "There are no enemies in this region."

    enemies_text = f"Enemies in the {world.current_region}:\n"
    for i, enemy in enumerate(world.enemies, 1):
        enemies_text += f"  {i}. {enemy.name}: {enemy.get_desc()}\n"

    return enemies_text.strip()


def look_around(world):
    """Look around the current region."""
    look_text = f"You are currently in the {world.current_region}.\n"
    look_text += f"There are {len(world.enemies)} enemies in this area."
    return look_text


def travel(world, destination):
    """Travel to a new region."""
    if destination.lower() in world.regions:
        world.change_region(destination.lower())
        return f"You have traveled to the {destination}."
    else:
        return f"Invalid region: {destination}. Staying in {world.current_region}."


def help_command():
    """Display available commands."""
    commands_text = "Available commands:\n"
    commands_text += "  help - Display this help message.\n"
    commands_text += "  look - Look around your current location.\n"
    commands_text += "  regions - Show available regions to travel to.\n"
    commands_text += "  travel [region] - Travel to a different region.\n"
    commands_text += "  enemies - Show enemies in your current region.\n"
    commands_text += "  examine [object] - Examine an object or character more closely.\n"
    commands_text += "  attack [enemy] - Attack a specific enemy to start combat.\n"
    commands_text += "  encounter - Find a random enemy to battle.\n"
    commands_text += "  stats - Display your character's statistics.\n"
    commands_text += "  inventory - Display your inventory.\n"
    commands_text += "  use [item/number] - Use an item from your inventory.\n"
    commands_text += "  quit - Exit the game."
    return commands_text