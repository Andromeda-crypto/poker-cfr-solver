# Rules, game state and action flow together in this file

import random
from kuhn_state import kuhnPokerState

class kuhnPokerGame:
    def __init__(self):
        self.state = kuhnPokerState()
    
    def play_round(self):
        while not self.state.is_terminal():
            current_player = self.state.current_player
            legal_actions = self.state.legal_actions()
            action = random.choice(legal_actions)
            print(f"Player {current_player} {action}s")
            self.state = self.state.next_state(action)
        payoff = self.state.calc_payoff()
        if payoff > 0:
            print(f"Player 0 wins the pot of {self.state.pot}")
        elif payoff < 0:
            print(f"player 1 wins the pot of {self.state.pot}")
        else:
            print("Tie")
        print(f"Final History: {self.state.history}, Cards: {self.state.cards}, Pot: {self.state.pot}")




game = kuhnPokerGame()
game.play_round()
