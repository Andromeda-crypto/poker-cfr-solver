import numpy as np
from information_set import get_information_set
from kuhn_poker import kuhnPokerGame

class CFRSolver:
    """
    Counterfactual Regret Minimization solver for Kuhn Poker.
    """
    
    def __init__(self):
        self.game = kuhnPokerGame()
        self.iterations = 0
        
    def train(self, num_iterations):
        util = 0
        for i in range(num_iterations):
            cards = self.game.deal_cards()
            util += self.cfr(cards, "", 1.0, 1.0)
            
            self.iterations += 1
            if (i + 1) % 1000 == 0:
                print(f"Iteration {i + 1}/{num_iterations}")
        
        print(f"\nAverage game value: {util / num_iterations}")
        
    def cfr(self, cards, history, reach_prob_0, reach_prob_1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player
        if self.is_terminal(history):
            return self.get_payoff(cards, history, player)
        
        card = cards[player]
        infoset = get_information_set(card, history)
        
        if player == 0:
            strategy = infoset.get_strategy(reach_prob_0)
        else:
            strategy = infoset.get_strategy(reach_prob_1)
        
        actions = ["p", "b"]
        action_utils = np.zeros(len(actions))
        
        for i, action in enumerate(actions):
            next_history = history + action
            
            if player == 0:
                action_utils[i] = -self.cfr(
                    cards, 
                    next_history, 
                    reach_prob_0 * strategy[i],
                    reach_prob_1
                )
            else:
                action_utils[i] = -self.cfr(
                    cards,
                    next_history,
                    reach_prob_0,
                    reach_prob_1 * strategy[i]
                )

        util = sum(strategy * action_utils)
        regrets = action_utils - util
    
        if player == 0:
            infoset.regret_sum += reach_prob_1 * regrets
        else:
            infoset.regret_sum += reach_prob_0 * regrets
        
        return util
    
    def is_terminal(self, history):
       
        return history in ["pp", "pbc", "pbf", "bp", "bc", "bbp", "bbc"]
    
    def get_payoff(self, cards, history, player):
       

        if "f" in history:
            return 1 
        else:
            if cards[0] > cards[1]:
                winner = 0
            else:
                winner = 1
        
            if history in ["pp"]:
                pot = 1  
            else:  
                pot = 2 
            if len(history) % 2 == player:
                if winner == player:
                    return pot
                else:
                    return -pot
            else:
                if winner == player:
                    return -pot
                else:
                    return pot


# Run training
if __name__ == "__main__":
    solver = CFRSolver()
    solver.train(10000)
    

    print("\n=== Average Strategies ===")
    from information_set import infoset_map
    for key, infoset in sorted(infoset_map.items()):
        avg_strategy = infoset.get_average_strategy()
        print(f"{key}: Pass={avg_strategy[0]:.3f}, Bet={avg_strategy[1]:.3f}")


