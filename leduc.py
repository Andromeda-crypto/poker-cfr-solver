# leduc poker 

import random
from leduc_state import leducPokerState

class leducPokerGame:
    def __init__(self):
        self.state= leducPokerState()
    
    def deal_cards(self):
        deck = ['J', 'J', 'K','K', 'Q', 'Q']
        random.shuffle(deck)
        return (deck.pop(),deck.pop())
    
    def play_turn(self,action=None):
        """Apply one action (from human or bot)."""
        if self.state.is_terminal():
            return
        current_player = self.state.current_player
        legal_actions = self.state.legal_actions()

        if action is None:
            action = random.choice(legal_actions)
            print(f"Bot (Player {current_player}) {action}s")
        else:
            if action not in legal_actions:
                raise ValueError(f"Invalid action '{action}'. Valid: {legal_actions}")

        self.state = self.state.next_state(action)
        return self.state
    
    def game_over(self):
        return self.state.is_terminal()
    
    def result(self):
        payoff = self.state.calc_payoff()
        if payoff > 0:
            return "Player 0 wins!"
        elif payoff < 0:
            return "Player 1 wins!"
        else:
            return "It's a tie!" # highly unlikely
        
        
    
