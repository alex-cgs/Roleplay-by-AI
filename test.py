import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh
from openai import ChatCompletion

# Initialize session state for tracking players and game state
if "players" not in st.session_state:
    st.session_state.players = []
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "player_stats" not in st.session_state:
    st.session_state.player_stats = {}
if "problematic" not in st.session_state:
    st.session_state.problematic = ""
if "solutions" not in st.session_state:
    st.session_state.solutions = {}
if "dice_rolls" not in st.session_state:
    st.session_state.dice_rolls = {}

# Function to roll a dice
def roll_dice():
    return random.randint(1, 20)

# Function to update player stats
def update_stats(player, dice_roll):
    stats = st.session_state.player_stats[player]
    hp, mp, gold = stats["HP"], stats["MP"], stats["Gold"]

    if dice_roll < 5:  # Bad outcome
        hp -= 1
        mp -= 10
        st.write(f"{player} failed badly! HP -1, MP -10")
    elif dice_roll < 15:  # Neutral outcome
        mp -= 5
        st.write(f"{player} did okay. MP -5")
    else:  # Great outcome
        gold += 10
        st.write(f"{player} succeeded! Gold +10")

    # Ensure stats are within bounds
    hp = max(0, min(10, hp))
    mp = max(0, min(100, mp))
    gold = max(0, min(200, gold))

    st.session_state.player_stats[player] = {"HP": hp, "MP": mp, "Gold": gold}

# Function to generate LLM story (placeholder for actual LLM integration)
def generate_story(problematic, solutions, dice_rolls, player_stats):
    story = """Here's the round summary:
Problematic: {problematic}\n
""".format(problematic=problematic)
    for player, solution in solutions.items():
        dice_roll = dice_rolls[player]
        stats = player_stats[player]
        story += f"{player}: {solution} (Dice Roll: {dice_roll}) -> HP: {stats['HP']}, MP: {stats['MP']}, Gold: {stats['Gold']}\n"
    story += "\nPlayers move to the next round!"
    return story

# Streamlit UI
st.title("Roleplay by AI")
st.sidebar.header("Game Settings")

# Add players
player_name = st.sidebar.text_input("Enter Player Name")
if st.sidebar.button("Add Player"):
    if player_name:
        st.session_state.players.append(player_name)
        st.session_state.player_stats[player_name] = {"HP": 10, "MP": 100, "Gold": 100}

# Display player stats
st.sidebar.subheader("Player Stats")
for player, stats in st.session_state.player_stats.items():
    st.sidebar.write(f"{player}: HP: {stats['HP']}, MP: {stats['MP']}, Gold: {stats['Gold']}")

# Game logic
if len(st.session_state.players) >= 2:
    current_player = st.session_state.players[st.session_state.current_round % len(st.session_state.players)]
    st.write(f"It's {current_player}'s turn to create a problematic!")

    if st.session_state.problematic == "":
        problematic_input = st.text_area("Enter the problematic for this round:")
        if st.button("Submit Problematic"):
            st.session_state.problematic = problematic_input
    else:
        st.write(f"Problematic: {st.session_state.problematic}")

        for player in st.session_state.players:
            if player not in st.session_state.solutions:
                solution = st.text_input(f"{player}, input your solution:")
                if st.button(f"Submit Solution for {player}"):
                    st.session_state.solutions[player] = solution

        if len(st.session_state.solutions) == len(st.session_state.players):
            for player in st.session_state.players:
                dice_roll = roll_dice()
                st.session_state.dice_rolls[player] = dice_roll
                update_stats(player, dice_roll)

            story = generate_story(
                st.session_state.problematic,
                st.session_state.solutions,
                st.session_state.dice_rolls,
                st.session_state.player_stats,
            )

            st.write(story)

            # Reset for next round
            st.session_state.problematic = ""
            st.session_state.solutions = {}
            st.session_state.dice_rolls = {}
            st.session_state.current_round += 1
else:
    st.write("Add at least two players to start the game!")
