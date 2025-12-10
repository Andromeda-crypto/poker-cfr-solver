import random

class KuhnPokerState:
    def __init__(self, history="", cards=None, current_player=0, pot=2):
        self.history = history                    # public betting history
        self.cards = cards or random.sample(['J', 'Q', 'K'], 2)
        self.current_player = current_player      # 0 or 1
        self.pot = pot

    def get_information(self):
        private_card = self.cards[self.current_player]
        return f"P{self.current_player}-{private_card}-{self.history}"

    def legal_actions(self):
        h = self.history
        if h.endswith("B"):
            return ["call", "fold"]
        if h == "C":
            return ["check", "bet"]
        return ["check", "bet"]
    
    def is_terminal(self):
        h = self.history
        if h.endswith("F"):
            return True
        if h == "CC":
            return True
        if h == "BC":
            return True

        return False
    
    def calc_payoff(self):
        h = self.history

        if not self.is_terminal():
            return 0

        if h.endswith("F"):
            folded_player = 1 - self.current_player  # current_player already flipped
            if folded_player == 0:
                return -1
            else:
                return 1

        p0, p1 = self.cards
        rank = {'J': 1, 'Q': 2, 'K': 3}

        if rank[p0] > rank[p1]:
            return 1
        elif rank[p0] < rank[p1]:
            return -1
        return 0

    def next_state(self, action):
        h_new = self.history + action[0].upper()
        pot_new = self.pot

        if action == "bet":
            pot_new += 1
        elif action == "call":
            pot_new += 1

        return KuhnPokerState(
            history=h_new,
            cards=self.cards.copy(),
            current_player=1 - self.current_player,
            pot=pot_new
        )
    def __repr__(self):
        return (
            f"KuhnPokerState(history='{self.history}', "
            f"cards={self.cards}, current_player={self.current_player}, pot={self.pot})"
        )

if __name__ == "__main__":
    print("Testing terminal states & actions")
    tests = ["", "C", "B", "BC", "BF", "CC", "CB"]
    for h in tests:
        s = KuhnPokerState(history=h)
        print(f"{h:3}  → actions={s.legal_actions()}  terminal={s.is_terminal()}")


               
