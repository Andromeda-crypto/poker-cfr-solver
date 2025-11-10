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
        if self.history.endswith("F"):
            return True
        if self.history.endswith("CC"):
           return True
        if self.history.endswith("BC") or self.history.endswith("CB"):
            return True
    
        return False


    def calc_payoff(self):
        if not self.is_terminal():
            return 0

        if self.history.endswith("F"):
        # The player who folded loses
            return -1 if self.history[-2] == "B" else 1

        p0_card, p1_card = self.cards
        card_rank = {'J': 1, 'Q': 2, 'K': 3}
        if card_rank[p0_card] > card_rank[p1_card]:
            return 1
        elif card_rank[p0_card] < card_rank[p1_card]:
            return -1
        else:
            return 0 


        
    def next_state(self, action):
        new_history = self.history + action[0].upper()
        new_pot = self.pot
        new_cards = self.cards.copy()

        if action == "bet":
            new_pot += 1
            next_player = 1 - self.current_player
        elif action == "call":
            new_pot += 1
            next_player = 1 - self.current_player
        elif action == "fold":
            next_player = 1 - self.current_player
        elif action == "check":
            next_player = 1 - self.current_player
        else:
            raise ValueError(f"Invalid action: {action}")

        next_state = kuhnPokerState(
            history=new_history,
            cards=new_cards,
            current_player=next_player,
            pot=new_pot
        )

        return next_state


    

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

               
