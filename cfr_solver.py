import matplotlib.pyplot as plt
import numpy as np
from information_set import get_information_set, infoset_map
from kuhn_state import KuhnPokerState
from leduc_state import leducPokerState


class CFRSolver:
    def __init__(self, game_type="Kuhn"):
        self.game_type = game_type
        self.iterations = 0
        self.values = []

        if game_type == "Kuhn":
            self.strategy_history = {c: [] for c in ['J', 'Q', 'K']}
        else:
            self.strategy_history = {}

    def _new_game_state(self):
        if self.game_type == "Kuhn":
            return KuhnPokerState()
        else:
            return leducPokerState()

    def train(self, num_iterations):
        util = 0.0

        for i in range(num_iterations):
            state = self._new_game_state()
            util += self.cfr(state, 1.0, 1.0)
            self.iterations += 1

            # Tracking every 100 iterations
            if (i + 1) % 100 == 0:
                avg_value = util / (i + 1)
                self.values.append(avg_value)

                # If Kuhn, track per-card betting tendencies
                if self.game_type == "Kuhn":
                    for card in ['J', 'Q', 'K']:
                        if card in infoset_map:
                            avg = infoset_map[card].get_average_strategy()
                            self.strategy_history[card].append(avg[1])
                        else:
                            self.strategy_history[card].append(0)

            if (i + 1) % 5000 == 0:
                print(f"[{self.game_type}] CFR Iteration {i+1}/{num_iterations}")

        return util / num_iterations

    def cfr(self, state, reach_prob_0, reach_prob_1):
        if state.is_terminal():
            return state.calc_payoff()

        player = state.current_player

        info_key = state.get_information()
        infoset = get_information_set(info_key, state.history)

        strategy = infoset.get_strategy(reach_prob_0 if player == 0 else reach_prob_1)

        actions = state.legal_actions()
        num_actions = len(actions)

        # Handle any game’s action count
        action_utils = np.zeros(num_actions)

        for i, action in enumerate(actions):
            next_state = state.next_state(action)

            if player == 0:
                action_utils[i] = -self.cfr(next_state, reach_prob_0 * strategy[i], reach_prob_1)
            else:
                action_utils[i] = -self.cfr(next_state, reach_prob_0, reach_prob_1 * strategy[i])

        util = np.dot(strategy, action_utils)
        regrets = action_utils - util

        # Regret update
        if player == 0:
            infoset.regret_sum += reach_prob_1 * regrets
        else:
            infoset.regret_sum += reach_prob_0 * regrets

        return util

    def plot_results(self):
        # Convergence
        plt.figure(figsize=(10, 5))
        plt.plot(range(100, len(self.values) * 100 + 1, 100), self.values)
        plt.title(f"{self.game_type} CFR Convergence")
        plt.xlabel("Iterations")
        plt.ylabel("Expected Value")
        plt.grid(True)
        plt.show()

        # Kuhn only — Leduc won't have fixed card sets
        if self.game_type == "Kuhn":
            plt.figure(figsize=(10, 5))
            for card, probs in self.strategy_history.items():
                plt.plot(range(100, len(probs) * 100 + 1, 100), probs, label=f"{card} - Bet Prob")
            plt.title("Kuhn Strategy Evolution")
            plt.xlabel("Iterations")
            plt.ylabel("Probability of Betting")
            plt.legend()
            plt.grid(True)
            plt.show()


if __name__ == "__main__":
    solver = CFRSolver(game_type="Kuhn")
    solver.train(20000)

    print("\n=== Average Strategies ===")
    for key, infoset in sorted(infoset_map.items()):
        avg_strategy = infoset.get_average_strategy()
        print(f"{key}: {avg_strategy}")
