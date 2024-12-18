# Roleplay-by-AI

Made by Alexandre Tinouert, Kevin Moreira Da Silva and David Pereira as part of our NLP's final project (winter semester 2024).

# Requirements

The project needs some libraries, thus to install them do: ```pip install -r requirements.txt``` in your shell.

# Description

To launch the project, do: ```python -m streamlit run rpbyai.py``` in your shell.

We use Mistral for generating stories (as it was free :p), and Google for simple searches, as it is simple for using it in a RAG in that case.

For the files:
- ```rpbyai.py``` contains the bulk of the game, with the game rules, and the general structure of the app.
- ```google_engine.py``` contains the simple RAG model we made for extracting some features from the problematics.

PLEASE! Do not use our api keys too much or we will be limited.