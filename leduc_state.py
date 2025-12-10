import random

class leducPokerState:
    def __init__(self, history="", private_cards=None, public_card=None,
                 current_player=0, pot=2):
        """
        Leduc Poker:
          - 6-card deck: JJ QQ KK
          - Each player gets 1 private card
          - After betting round 1: reveal 1 public card
          - Then second betting round
        """

        self.history = history
        self.current_player = current_player
        self.pot = pot

        # Deal private cards if not given
        if private_cards is None:
            deck = ['J','J','Q','Q','K','K']
            random.shuffle(deck)
            self.private_cards = (deck.pop(), deck.pop())
            self.remaining_deck = deck
        else:
            self.private_cards = private_cards
            # You must supply the deck if you use custom cards
            self.remaining_deck = ['J','J','Q','Q','K','K']

        # Public card
        self.public_card = public_card

 
    def get_information(self):
        """Information set: private card + public card + betting history"""
        priv = self.private_cards[self.current_player]
        pub = self.public_card if self.public_card is not None else "_"
        return f"{priv}|{pub}|{self.history}"


    def legal_actions(self):
        h = self.history

        # After a bet: only call or fold
        if h.endswith("B"):
            return ["call", "fold"]
        return ["check", "bet"]

    def is_terminal(self):
        h = self.history
        if h.endswith("F"):
            return True
        if h.endswith("CC") or h.endswith("BC") or h.endswith("CB"):
            if h.count("C") == 2 and self.public_card is None:
                return False  # go to round 2
            return True

        return False
    def calc_payoff(self):
        if self.history.endswith("F"):
            # The folder loses 1 pot unit
            last = self.history[-2]
            if last == "B":      # Player who bet wins
                return 1 if self.current_player == 1 else -1
            else:
                return 1 if self.current_player == 0 else -1

        # Showdown
        p0 = self.private_cards[0]
        p1 = self.private_cards[1]
        ranks = {'J': 1, 'Q': 2, 'K': 3}

        # Pair with public card wins
        if p0 == self.public_card and p1 != self.public_card:
            return 1
        if p1 == self.public_card and p0 != self.public_card:
            return -1
        if ranks[p0] > ranks[p1]:
            return 1
        if ranks[p1] > ranks[p0]:
            return -1
        return 0

    def next_state(self, action):
        a = action[0].upper()
        h2 = self.history + a
        pot2 = self.pot

        # Betting adds to pot
        if action == "bet" or action == "call":
            pot2 += 1

        # Player alternates
        next_player = 1 - self.current_player

        # ON FIRST CC → REVEAL PUBLIC CARD
        if h2.endswith("CC") and self.public_card is None:
            # Reveal a public card from remaining deck
            pub = random.choice(self.remaining_deck)
            return leducPokerState(
                history=h2,
                private_cards=self.private_cards,
                public_card=pub,
                current_player=next_player,
                pot=pot2
            )

        # Otherwise continue game
        return leducPokerState(
            history=h2,
            private_cards=self.private_cards,
            public_card=self.public_card,
            current_player=next_player,
            pot=pot2
        )

