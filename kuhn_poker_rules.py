# Rules of kuhn poker implemented via python 
import random

class Player:
    def __init__(self):
        self.player1 = None
        self.player2 = None
    
    def action(self):
        return random.choice(['check', 'fold', 'bet', 'call'])
    
    def hand(self):
        return random.choice(['J', 'Q', 'K'])
    
class KuhnPoker:
    def __init__(self):
        self.deck = ['J','K', 'Q']
        self.pot = 0
        self.player1 = Player()
        self.player2 = Player()
        self.player1_hand = None
        self.player2_hand = None
        self.current_turn = 1 
        

    def deal_hands(self):
        random.shuffle(self.deck)
        print(f"Deck : {self.deck}" )
        self.player1_hand = self.deck.pop()
        self.player2_hand = self.deck.pop()

    def play_round(self):
        self.deal_hands()
        print(f"Player 1 has {self.player1_hand}\nPlayer 2 has {self.player2_hand}")

        action1 = self.player1.action()
        print(f"Player 1 action: {action1}")
        action2 = self.player2.action()
        print(f"Player 2 action: {action2}")

        # Kuhn poker rules and logic 

        if action1 == 'bet':
            self.pot += 1
            if action2 == 'call':
                self.pot += 1
                self.determine_winner()
            elif action2 == 'fold':
                print("Player 2 folds. Player 1 wins the pot. ")
                self.pot = 0
        elif action1 == 'check':
            if action2 == 'bet':
                self.pot += 1
                action1_response = self.player1.action()
                if action1_response == 'call':
                    self.pot += 1
                    self.determine_winner()
                elif action1_response == 'fold':
                    print("Player 1 folds. Player 2 wins the pot.")
                    self.pot = 0
            elif action2 == 'check':
                self.determine_winner()
        
    def determine_winner(self):
        rank = {'J': 1, 'Q': 2, 'K' : 3}
        if rank[self.player1_hand] > rank[self.player2_hand]:
            print(f"Player 1 wins the pot of {self.pot}")
        else:
            print(f"Player 2 wins pot of {self.pot}")
        self.pot = 0
        # return winner
        return "Player 1" if rank[self.player1_hand] > rank[self.player2_hand] else "Player 2"
        


if __name__ == "__main__":
    game = KuhnPoker()
    game.play_round()
    print(f"Game Over\nWinner is {game.determine_winner()}")




           




