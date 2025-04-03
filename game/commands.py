from .characters import Character
from .world import GameObject
from .items import Item


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
        # Check if the parameter is a number
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
        # If not a number, search by name
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
    """Returns a list of available commands and their descriptions."""
    return (
        "Available commands:\n"
        "  help - Show this help menu.\n"
        "  look - Look around your current region.\n"
        "  regions - Display available regions to travel to.\n"
        "  travel [region] - Travel to a new region.\n"
        "  enemies - Show all enemies in the current region.\n"
        "  examine [object/enemy] - Inspect an object or enemy.\n"
        "  attack [enemy] - Attack a specific enemy.\n"
        "  encounter - Randomly encounter an enemy in the region.\n"
        "  stats - Display your character stats.\n"
        "  inventory - Show your inventory.\n"
        "  use [item number/name] - Use an item from your inventory.\n"
        "  quit - Exit the game."
    )