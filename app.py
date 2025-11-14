# streamlit_app.py

import streamlit as st
import numpy as np
from cfr_solver import CFRSolver
from kuhn_state import kuhnPokerState
from information_set import get_information_set, infoset_map

st.set_page_config(page_title="Kuhn Poker CFR", layout="wide")
st.title("Kuhn Poker: Human vs Trained Bot")


solver = CFRSolver()
avg_game_value = solver.train(10000)  

st.sidebar.write(f"Average Game Value: {avg_game_value:.4f}")

if 'state' not in st.session_state:
    st.session_state.state = kuhnPokerState()
    st.session_state.history_log = []

def bot_action(state):
    player = state.current_player
    card = state.cards[player]
    infoset = get_information_set(card, state.history)
    strategy = infoset.get_average_strategy()
    legal_actions = state.legal_actions()


    if 'check' in legal_actions and 'bet' in legal_actions:
        prob = strategy  # [check, bet]
    else:
        prob = [strategy[0], strategy[1]]  # [call, fold]

    action = np.random.choice(legal_actions, p=prob/np.sum(prob))
    return action

def render_game():
    state = st.session_state.state
    st.subheader(f"History: {state.history}")
    st.write(f"Pot: {state.pot}")
    st.write(f"Your card: {state.cards[0]}")  # Player 0 is human

    if state.is_terminal():
        payoff = state.calc_payoff()
        if payoff > 0:
            st.success("You win!")
        else:
            st.error("Bot wins!")
        if st.button("Restart Game"):
            st.session_state.state = kuhnPokerState()
            st.session_state.history_log = []
        return

    # Human action
    legal_actions = state.legal_actions()
    human_action = st.radio("Choose your action:", legal_actions)
    if st.button("Play Turn"):
        # Human plays
        state = state.next_state(human_action)
        st.session_state.history_log.append(f"You: {human_action}")

        # Bot plays
        if not state.is_terminal():
            bot_a = bot_action(state)
            state = state.next_state(bot_a)
            st.session_state.history_log.append(f"Bot: {bot_a}")

        st.session_state.state = state
        render_game()

render_game()


st.subheader("Strategy Probabilities (Average CFR)")
cards = ['J','Q','K']
for card in cards:
    probs = []
    for key, infoset in infoset_map.items():
        if key.startswith(card):
            avg = infoset.get_average_strategy()
            probs.append(avg[1])  
    st.line_chart(np.array(probs))


st.subheader("Regret Evolution")
for card in cards:
    regrets = []
    for key, infoset in infoset_map.items():
        if key.startswith(card):
            regrets.append(np.sum(infoset.regret_sum))
    st.bar_chart(np.array(regrets))