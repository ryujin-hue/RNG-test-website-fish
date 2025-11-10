import json
import random

class TrngEngine:
    def __init__(self):
        """
        Initializes the TRNG engine by loading events from game_rules.json.
        """
        with open('game_rules.json', 'r') as f:
            rules = json.load(f)
        self.events = rules['random_events']
        self.total_weight = sum(event['probability_weight'] for event in self.events)

    def get_random_event(self):
        """
        Selects a random event based on its probability weight.
        """
        rand_num = random.uniform(0, self.total_weight)
        cumulative_weight = 0

        for event in self.events:
            cumulative_weight += event['probability_weight']
            if rand_num <= cumulative_weight:
                return event

        # Fallback, should not happen with correct logic
        return random.choice(self.events)
