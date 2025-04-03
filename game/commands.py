from .characters import Character
from .world import GameObject

def examine(noun):
    if noun in GameObject.objects:
        return GameObject.objects[noun].get_desc()
    return "There is nothing special here."

def attack(player, noun):
    if noun in GameObject.objects and isinstance(GameObject.objects[noun], Character):
        return player.attack(GameObject.objects[noun])
    return "You cannot attack that!"