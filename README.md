# poker-cfr-solver

# Project Overview

This project demonstrates the application of Counterfactual Regret Minimization (CFR) to solve Kuhn Poker, a simplified zero-sum poker game. The CFR solver trains a bot to play optimally, and the project includes an interactive web demo where a human player can play against the trained bot.

The project highlights:

Advanced understanding of game theory and imperfect information games.

Practical implementation of AI training algorithms.

Interactive visualizations of strategy evolution and regret.

Real-time human vs bot gameplay with a live demo.

|Technology                                                                                                          | Purpose                                                                     |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)             | Core language for game logic, CFR solver, and training scripts              |
| ![NumPy](https://img.shields.io/badge/NumPy-F0DB4F?style=for-the-badge\&logo=NumPy\&logoColor=white)                | Efficient numerical operations for strategy computation and regret tracking |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge\&logo=Matplotlib\&logoColor=white) | Visualization of strategy evolution and cumulative regrets                  |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)    | Web-based frontend for interactive human vs bot gameplay                    |
| Git                                                                                                                 | Version control and project tracking                                        |

# Features

CFR Solver with strategy and regret tracking

Human vs Trained Bot Gameplay via Streamlit

Visualizations: strategy evolution and cumulative regrets per card

Live Demo showcasing decision-making of the bot


# Future Enhancements
Extend to full-scale poker variants (Texas Hold’em, Omaha)

Integrate real-time interactive visualizations in the web app

Implement vectorized CFR solver and multi-threaded optimization

Add opponent modeling for more advanced bot behavior
