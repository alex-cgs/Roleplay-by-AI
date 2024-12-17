import streamlit as st
import random
import time
from mistralai import Mistral
from google_engine import process_prompt

model = "mistral-small-latest"

client = Mistral(api_key="djjALP5Hi379dudy3IjDwPAPaPxsRpKt")

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
if "story_generated" not in st.session_state:
    st.session_state.story_generated = False
if "next_round_triggered" not in st.session_state:
    st.session_state.next_round_triggered = False

def roll_dice():
    return random.randint(1, 20)

def get_dice_color(roll):
    if roll >= 15:
        return "#4CAF50"
    elif roll >= 5:
        return "#FFC107"
    else:
        return "#F44336"

def display_dice_rolls(rolls):
    st.write("### Dice Rolls")
    for player, roll in rolls.items():
        color = get_dice_color(roll)
        st.markdown(
            f"<div style='display: inline-block; text-align: center; margin: 10px;'>"
            f"<div style='border: 2px solid #666; border-radius: 50%; width: 80px; height: 80px; display: flex; justify-content: center; align-items: center; background-color: {color}; color: white;'>"
            f"<p style='margin: 0;'>{roll}</p></div>"
            f"<p>{player}</p></div>",
            unsafe_allow_html=True
        )

def render_player_stats():
    st.write("### Player Statistics")
    for player, stats in st.session_state.player_stats.items():
        st.write(f"#### {player}")
        st.progress(stats["HP"] / 10, f"HP: {stats['HP']} / 10")
        st.progress(stats["MP"] / 100, f"MP: {stats['MP']} / 100")
        st.progress(stats["Gold"] / 200, f"Gold: {stats['Gold']} / 200")

def update_stats(player, dice_roll):
    stats = st.session_state.player_stats[player]
    hp, mp, gold = stats["HP"], stats["MP"], stats["Gold"]

    if dice_roll < 5:
        hp -= 1
        mp -= 10
        st.error(f"{player} failed badly! HP -1, MP -10")
    elif dice_roll < 15:
        mp -= 5
        st.warning(f"{player} did okay. MP -5")
    else:
        gold += 10
        st.success(f"{player} succeeded! Gold +10")

    stats["HP"] = max(0, min(10, hp))
    stats["MP"] = max(0, min(100, mp))
    stats["Gold"] = max(0, min(200, gold))
    st.session_state.player_stats[player] = stats

def generate_story(problematic, solutions, dice_rolls, player_stats):
    story_prompt = f"Here's the round summary:\nProblematic: {problematic}\n\n"
    for player, solution in solutions.items():
        dice_roll = dice_rolls[player]
        stats = player_stats[player]
        story_prompt += f"{player}: {solution} (Dice Roll: {dice_roll}) -> HP: {stats['HP']}, MP: {stats['MP']}, Gold: {stats['Gold']}\n"

    try:
        proc_prompt = process_prompt(st.session_state.problematic)
        with st.spinner("Loading/Saving..."):
            time.sleep(1)
            response = client.chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a storytelling game master that provides cohesive story summaries under 150 words."},
                    {"role": "user", "content": story_prompt + "\n" + proc_prompt},
                ]
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating story: {e}")
        return "An error occurred while generating the story."

st.title("Roleplay by AI")
st.sidebar.header("Game Settings")

player_name = st.sidebar.text_input("Enter Player Name")
if st.sidebar.button("Add Player"):
    if player_name and player_name not in st.session_state.players:
        st.session_state.players.append(player_name)
        st.session_state.player_stats[player_name] = {"HP": 10, "MP": 100, "Gold": 100}

render_player_stats()

if len(st.session_state.players) >= 2:
    current_player = st.session_state.players[st.session_state.current_round % len(st.session_state.players)]
    st.write(f"### It's {current_player}'s turn to create a problematic!")

    if st.session_state.problematic == "":
        problematic_input = st.text_area("Enter the problematic for this round:")
        if st.button("Submit Problematic"):
            st.session_state.problematic = problematic_input
    else:
        st.write(f"### Problematic: {st.session_state.problematic}")

        # Collect all solutions first
        if not st.session_state.story_generated:
            solutions_ready = True
            for player in st.session_state.players:
                if player not in st.session_state.solutions:
                    solution = st.text_input(f"{player}, input your solution:", key=f"solution_{player}")
                    if solution == "":
                        solutions_ready = False
                    else:
                        st.session_state.solutions[player] = solution
            if solutions_ready and st.button("Submit All Propositions"):
                st.session_state.story_generated = True
                st.session_state.next_round_triggered = False

        if st.session_state.story_generated:
            if not st.session_state.next_round_triggered:
                for player in st.session_state.players:
                    dice_roll = roll_dice()
                    st.session_state.dice_rolls[player] = dice_roll
                    update_stats(player, dice_roll)
                st.session_state.next_round_triggered = True

            display_dice_rolls(st.session_state.dice_rolls)
            story = generate_story(
                st.session_state.problematic,
                st.session_state.solutions,
                st.session_state.dice_rolls,
                st.session_state.player_stats,
            )

            st.write("### Story Summary")
            st.markdown(f"<div style='padding: 10px; border-radius: 5px;'>{story}</div>", unsafe_allow_html=True)

            if st.button("Go Next Round"):
                st.session_state.problematic = ""
                st.session_state.solutions = {}
                st.session_state.dice_rolls = {}
                st.session_state.story_generated = False
                st.session_state.current_round += 1
                st.session_state.next_round_triggered = False
else:
    st.write("Add at least two players to start the game!")
