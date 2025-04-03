class GameObject:
    """Base class for all objects in the game."""
    objects = {}

    def __init__(self, name, description):
        self.name = name
        self.description = description
        GameObject.objects[self.name.lower()] = self

    def get_desc(self):
        return self.description

    @staticmethod
    def get_article(word):
        return "An" if word.lower()[0] in "aeiou" else "A"