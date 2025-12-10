# streamlit_app.py

import streamlit as st
import numpy as np
from cfr_solver import CFRSolver
from kuhn_state import KuhnPokerState
from leduc_state import leducPokerState
from information_set import get_information_set, infoset_map

st.set_page_config(page_title="Poker CFR", layout="wide")
st.title("CFR Poker: Human vs Trained Bot (Kuhn & Leduc)")

# Choose game variant
game_type = st.sidebar.selectbox("Game Variant", ["Kuhn", "Leduc"])

# CFR Training (separate for each variant)
solver = CFRSolver(game_type=game_type)
avg_game_value = solver.train(20000)
st.sidebar.write(f"Average {game_type} Game Value: {avg_game_value:.4f}")

# Initialize state
if 'state' not in st.session_state or st.session_state.get('active_game') != game_type:
    st.session_state.active_game = game_type
    st.session_state.state = KuhnPokerState() if game_type == "Kuhn" else leducPokerState()
    st.session_state.history_log = []

state = st.session_state.state

def bot_action(state):
    player = state.current_player
    card_info = state.get_information()  # Works for both variants
    infoset = get_information_set(card_info, state.history)
    strategy = infoset.get_average_strategy()
    legal_actions = state.legal_actions()

    prob = np.array(strategy[:len(legal_actions)])
    prob = prob / prob.sum()

    return np.random.choice(legal_actions, p=prob)


def render_game():
    state = st.session_state.state

    st.subheader(f"History: {state.history}")
    st.write(f"Pot: {state.pot}")

    # Cards
    if game_type == "Kuhn":
        st.write(f"Your card: {state.cards[0]}")
    else:
        st.write(f"Your private card: {state.private_cards[0]}")
        if state.public_card is not None:
            st.write(f"Public card: {state.public_card}")

    if state.is_terminal():
        payoff = state.calc_payoff()
        st.success("You win!" if payoff > 0 else "Bot wins!")

        if st.button("Restart Game"):
            st.session_state.state = KuhnPokerState() if game_type == "Kuhn" else leducPokerState()
            st.session_state.history_log = []
        return

    legal_actions = state.legal_actions()
    human_action = st.radio("Choose your action:", legal_actions)

    if st.button("Play Turn"):
        new_state = state.next_state(human_action)
        st.session_state.history_log.append(f"You: {human_action}")

        if not new_state.is_terminal():
            bot_a = bot_action(new_state)
            new_state = new_state.next_state(bot_a)
            st.session_state.history_log.append(f"Bot: {bot_a}")

        st.session_state.state = new_state
        render_game()

render_game()

# Strategy Visualization
st.subheader("Strategy Probabilities (Average CFR)")
for key, infoset in infoset_map.items():
    st.write(f"Infoset {key}: {infoset.get_average_strategy()}")


# Regret Visualization
st.subheader("Regret Evolution")
for key, infoset in infoset_map.items():
    st.write(f"Infoset {key}: Regret Sum = {infoset.regret_sum}")
