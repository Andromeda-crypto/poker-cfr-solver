from kuhn_poker import kuhnPokerGame

def main():
    print("Welcome to Kuhn Poker!")
    game = kuhnPokerGame()

    while not game.state.is_terminal():
        print(f"\nHistory: {game.state.history}")
        print(f"Pot: {game.state.pot}")
        print(f"Your card: {game.state.cards[0]}")
        print(f"Available actions: {game.state.legal_actions()}")
        if game.state.current_player == 0:
            action = input("Enter your action: ").strip().lower()
            while action not in game.state.legal_actions():
                print("Invalid action. Try again.")
                action = input("Enter your action: ").strip().lower()
        else:
            import random
            action = random.choice(game.state.legal_actions())
            print(f"Bot (Player 1) {action}s")

        game.state = game.state.next_state(action)

    print("\nGame Over!")
    payoff = game.state.calc_payoff()
    if payoff > 0:
        print("Player 0 (You) win!")
    elif payoff < 0:
        print("Player 1 (Bot) wins!")
    else:
        print("It's a tie!")

    print(f"Final History: {game.state.history}, Cards: {game.state.cards}, Pot: {game.state.pot}")

if __name__ == "__main__":
    main()
