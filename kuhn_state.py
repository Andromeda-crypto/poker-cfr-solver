import random
class kuhnPokerState:
    def __init__(self, history="", cards=None, current_player = 0, pot=2):
        self.history = history # represents the sequence of actions taken
        self.cards = cards or random.sample(['J', 'Q', 'K'],2)
        self.current_player = current_player
        self.pot = pot

    def get_information(self,card,history):
        return f"{card}{history}"

    def legal_actions(self):
        if self.history.endswith('B'):
            return ['call', 'fold']
        
        return ['check', 'bet']
    
    def is_terminal(self):
        return self.history in ['CC', 'BC', 'BF','CBF']

    def calc_payoff(self):
        rank = {'J': 1, 'Q': 2, 'K': 3}
        card0, card1 = self.cards

        if self.history in ['BF', 'CBF']:
            return self.pot / 2 if self.current_player == 0 else -self.pot / 2
        if rank[card0] > rank[card1]:
            return self.pot / 2
        elif rank[card0] < rank[card1]:
            return -self.pot / 2
        else:
            return 0


        
    def next_state(self,action):
        if action in ["bet", "call"]:
            next_pot = self.pot + 1
        else:
            next_pot = self.pot
        next_history = self.history + action[0].upper()
        return kuhnPokerState(
            history= next_history,
            cards = self.cards,
            current_player = 1 - self.current_player,
            pot = next_pot
        )
    

game = kuhnPokerState()
print(f"initial State :\nHistory :{game.history}\nCards : {game.cards}\nCurrent Player :{game.current_player}\n Pot: {game.pot}")
next_game = game.next_state('bet')
print("\nAfter Player 0 makes a bet")
print(f"Next State :\nHistory :{next_game.history}\nCards : {next_game.cards}\n Current Player : {next_game.current_player}\n Pot: {next_game.pot}")


terminal_state = kuhnPokerState(history="BC", cards=['J','K'], current_player=0, pot =4)
print(f"\nTerminal State:\nHistory :{terminal_state.history}\nCards : {terminal_state.cards}\n Current Player :{terminal_state.current_player}\n Pot: {terminal_state.pot}")


for h in ["", "B", "BC", "BF", "C", "CB", "CBF", "CC"]:
    s = kuhnPokerState(history=h)
    print(f"{h:3} → {s.legal_actions()} | Terminal: {s.is_terminal()}")

               
