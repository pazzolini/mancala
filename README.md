# Mancala

## Overview

This repository contains the first practical assignment for **Elements of Artificial Intelligence and Data Science 2022/23**. It contains Python scripts for playing and analyzing the game of Mancala. The scripts allow different modes of play, including human vs. human, human vs. AI, and AI vs. AI, as well as statistical analysis of AI performance.

## Human vs. Human Mode

- 📌 File: mancala_human_human.py
- 🎮 Description: Allows two human players to compete against each other.

## Human vs. AI Mode

- 📌 File: mancala_human_ai.py
- 🎮 Description: Allows a human player (Player 1) to compete against an AI agent. There are three difficulty levels to choose from.
- 📁 Dependencies: Imports AI agents from ai_agents.py.

## AI vs. AI Mode

- 📌 File: mancala_ai_ai.py
- 🎮 Description: Allows two AI agents to play against each other.
- 📁 Dependencies: Imports AI agents from ai_agents2.py.

## AI Performance Statistics

- 📌 File: statistics.py
- 📊 Description: Runs a user-defined number of games between different AI agents and collects performance statistics.

## Customization

If you want to modify the AI’s evaluation functions or adjust the search depth of the minimax algorithm, you can edit the ai_agents2.py file and then run statistics.py to analyze the changes.

@ Vítor Ferreira | LIACD
