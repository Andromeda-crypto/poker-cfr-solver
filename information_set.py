import numpy as np

class InformationSet:
    def __init__(self, key):
        self.key = key
        self.num_actions = 2
        self.regret_sum = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.strategy = np.zeros(self.num_actions)

    def get_strategy(self, reach_probability):
        normalizing_sum = 0
        for action in range(self.num_actions):
            self.strategy[action] = max(0, self.regret_sum[action])
            normalizing_sum += self.strategy[action]
        
        if normalizing_sum > 0:
            self.strategy /= normalizing_sum
        else:
            self.strategy = np.ones(self.num_actions) / self.num_actions
        self.strategy_sum += reach_probability * self.strategy
        
        return self.strategy
    
    def get_average_strategy(self):
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            return self.strategy_sum / normalizing_sum
        else:
            return np.ones(self.num_actions) / self.num_actions


infoset_map = {}

def get_information_set(card, history):
    key = f"{card}{history}"
    if key not in infoset_map:
        infoset_map[key] = InformationSet(key)
    return infoset_map[key]