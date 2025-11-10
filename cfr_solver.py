import matplotlib.pyplot as plt
import numpy as np
from information_set import get_information_set, infoset_map
from kuhn_state import kuhnPokerState


class CFRSolver:
    def __init__(self):
        self.iterations = 0
        self.values = []
        self.strategy_history = {'J': [], 'Q': [], 'K': []}

    def train(self, num_iterations):
        util = 0.0

        for i in range(num_iterations):
            state = kuhnPokerState()
            util += self.cfr(state, 1.0, 1.0)
            self.iterations += 1

            if (i + 1) % 100 == 0:
                avg_value = util / (i + 1)
                self.values.append(avg_value)


                for card in ['J', 'Q', 'K']:
                    infoset_key = f"{card}"
                    if infoset_key in infoset_map:
                        avg_strategy = infoset_map[infoset_key].get_average_strategy()
                        self.strategy_history[card].append(avg_strategy[1])  
                    else:
                        self.strategy_history[card].append(0.0)

            if (i + 1) % 1000 == 0:
                print(f"Iteration {i + 1}/{num_iterations}")
        avg_game_value = util/num_iterations
        print(f"\nAverage game value: {avg_game_value:.4f}")
        return avg_game_value

    def cfr(self, state, reach_prob_0, reach_prob_1):
        if state.is_terminal():
            return state.calc_payoff()

        player = state.current_player
        card = state.cards[player]
        infoset = get_information_set(card, state.history)

        strategy = infoset.get_strategy(reach_prob_0 if player == 0 else reach_prob_1)
        actions = state.legal_actions()
        action_utils = np.zeros(len(actions))

        for i, action in enumerate(actions):
            next_state = state.next_state(action)
            if player == 0:
                action_utils[i] = -self.cfr(next_state, reach_prob_0 * strategy[i], reach_prob_1)
            else:
                action_utils[i] = -self.cfr(next_state, reach_prob_0, reach_prob_1 * strategy[i])

        util = np.dot(strategy, action_utils)
        regrets = action_utils - util

        if player == 0:
            infoset.regret_sum += reach_prob_1 * regrets
        else:
            infoset.regret_sum += reach_prob_0 * regrets

        return util

    def plot_results(self):
        # Convergence curve
        plt.figure(figsize=(10, 5))
        plt.plot(range(100, len(self.values) * 100 + 1, 100), self.values)
        plt.title("CFR Convergence (Average Game Value)")
        plt.xlabel("Iterations")
        plt.ylabel("Expected Value")
        plt.grid(True)
        plt.show()


        plt.figure(figsize=(10, 5))
        for card, probs in self.strategy_history.items():
            plt.plot(range(100, len(probs) * 100 + 1, 100), probs, label=f"{card} - Bet Prob")
        plt.title("Strategy Evolution per Card")
        plt.xlabel("Iterations")
        plt.ylabel("Probability of Betting")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    solver = CFRSolver()
    solver.train(10000)

    print("\n=== Average Strategies ===")
    for key, infoset in sorted(infoset_map.items()):
        avg_strategy = infoset.get_average_strategy()
        print(f"{key}: Check/Call={avg_strategy[0]:.3f}, Bet/Fold={avg_strategy[1]:.3f}")

    # Manual visualization trigger
    solver.plot_results()
