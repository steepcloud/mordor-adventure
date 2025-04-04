from .commands import examine, help_command, show_regions, show_enemies, show_inventory, use_item
from .combat import Combat


def process_command(command_str, game_engine):
    """Process a command string and execute the corresponding action."""
    if not command_str:
        return "Please enter a command."

    words = command_str.strip().lower().split()
    verb = words[0]
    noun = ' '.join(words[1:]) if len(words) > 1 else None

    # command handling uses a dictionary for easy extensibility
    command_handlers = {
        "help": lambda: help_command(),
        "regions": lambda: _show_regions(game_engine),
        "travel": lambda: _handle_travel(game_engine, noun),
        "look": lambda: _handle_look(game_engine),
        "enemies": lambda: _show_enemies(game_engine),
        "examine": lambda: _handle_examine(noun),
        "stats": lambda: _show_stats(game_engine),
        "inventory": lambda: _show_inventory(game_engine),
        "use": lambda: _handle_use_item(game_engine, noun),
        "attack": lambda: _handle_attack(game_engine, noun),
        "encounter": lambda: _handle_encounter(game_engine),
    }

    # execute the command if it exists
    if verb in command_handlers:
        return command_handlers[verb]()
    else:
        return "Unknown command. Type 'help' for a list of commands."


# functions with empty string returns are printing directly
# this pattern allows flexible output handling

def _show_regions(game_engine):
    regions_text = show_regions(game_engine.world)
    print(regions_text)
    return ""  # Return empty string since we printed directly


def _handle_travel(game_engine, region_name):
    if not region_name:
        return "Travel where? Type 'regions' to see available regions."

    # region changes are handled by the world object
    result = game_engine.world.change_region(region_name)
    return result


def _handle_look(game_engine):
    # quick environment summary without entering detailed examination
    return f"You are currently in the {game_engine.world.current_region}.\n" \
           f"There are {len(game_engine.world.enemies)} enemies in this area."


def _show_enemies(game_engine):
    enemies_text = show_enemies(game_engine.world)
    print(enemies_text)
    return ""


def _handle_examine(noun):
    if not noun:
        return "Examine what?"
    return examine(noun)


def _show_stats(game_engine):
    return game_engine.player.show_stats()


def _show_inventory(game_engine):
    inventory_text = show_inventory(game_engine.player)
    print(inventory_text)
    return ""


def _handle_use_item(game_engine, item_identifier):
    if not item_identifier:
        return "Use what? Specify an item number or name."

    # player can use items by name or inventory position
    result = use_item(game_engine.player, item_identifier)
    return result


def _handle_attack(game_engine, target_name):
    if not target_name:
        return "Attack what? Specify an enemy name."

    # find enemy by name before initiating combat
    enemy = game_engine.world.get_enemy_by_name(target_name)
    if not enemy:
        return f"No enemy named '{target_name}' found."

    # terminal mode
    print(f"{game_engine.player.name} initiates combat with {enemy.name}!")
    combat = Combat(game_engine.player, enemy)
    combat.start_combat()

    return ""  # combat system handles its own output


def _handle_encounter(game_engine):
    # random enemy encounters add unpredictability to gameplay
    enemy = game_engine.world.encounter_enemy()
    if not enemy:
        return "No enemies to encounter."

    # terminal mode
    print(f"{game_engine.player.name} encounters {enemy.name}!")
    combat = Combat(game_engine.player, enemy)
    combat.start_combat()

    return ""  # combat system handles its own output