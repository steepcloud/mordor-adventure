from .characters import Character
from .world import GameObject

def examine(noun):
    """Returns the description of an object or character in the game."""
    if noun in GameObject.objects:
        return GameObject.objects[noun].get_desc()
    return "There is nothing special here."

def attack(player, noun):
    """Handles attacking an NPC or character in the game."""
    if noun in GameObject.objects and isinstance(GameObject.objects[noun], Character):
        return player.attack(GameObject.objects[noun])
    return "You cannot attack that!"

def help_command():
    """Returns a list of available commands and their descriptions."""
    return (
        "Available commands:\n"
        "  examine [object] - Inspect an object or character.\n"
        "  attack [enemy] - Attack an enemy if they are present.\n"
        "  quit - Exit the game.\n"
        "  help - Show this help menu."
    )
