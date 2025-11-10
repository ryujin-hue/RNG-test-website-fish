import json

class Player:
    def __init__(self):
        """
        Initializes the player by loading attributes from game_rules.json.
        """
        with open('game_rules.json', 'r') as f:
            rules = json.load(f)

        self.attributes = rules['player_attributes']['initial_values'].copy()
        self.max_values = rules['player_attributes']['max_values'].copy()

    def apply_effects(self, effects):
        """
        Applies the effects of an event to the player's attributes.
        """
        for attr, value in effects.items():
            if attr in self.attributes:
                self.attributes[attr] += value

                # Enforce max values if they exist
                if attr in self.max_values:
                    if self.attributes[attr] > self.max_values[attr]:
                        self.attributes[attr] = self.max_values[attr]

                # Ensure attributes don't drop below zero (optional rule)
                if self.attributes[attr] < 0 and attr != 'wealth':
                     self.attributes[attr] = 0

    def get_status(self):
        """
        Returns the current state of the player's attributes.
        """
        return self.attributes

    def is_game_over(self):
        """
        Checks if the game-over conditions are met.
        For now, let's say game is over if health is 0.
        """
        return self.attributes['health'] <= 0
