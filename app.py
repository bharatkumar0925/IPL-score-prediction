# app.py

import streamlit as st
import pickle
import pandas as pd

df = pd.read_csv('final_data.csv', usecols=range(1, 8))
# Load the model
with open('score_prediction.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def calculate_crr(current_score, overs):
    return round((current_score * 6)/ overs, 2)

def main():
    st.title("Cricket Score Prediction")

    # Create input widgets
    st.sidebar.header("User Input")
    toss_won = st.sidebar.selectbox("Toss Won By", df['toss_won'].unique())
    decision = st.sidebar.selectbox("Decision", ['BOWL FIRST', 'BAT FIRST'])
    venue_options = df['venue_name'].unique()
    venue_name = st.sidebar.selectbox("Venue_name", venue_options)
    season = st.sidebar.slider("Season", 2008, 2023, 2023)
    home_team = st.sidebar.selectbox("Home Team", df['home_team'].unique())
    away_team = st.sidebar.selectbox("Away Team", df['away_team'].unique())
    current_innings = st.sidebar.selectbox("Current Innings", df['current_innings'].unique())
    innings_id = st.sidebar.slider("Innings ID", 1, 2, 1)
    balls = st.sidebar.number_input("Balls", min_value=1, max_value=120)
    current_score = st.number_input("Enter the current score", min_value=0, max_value=300)
    wickets = st.sidebar.slider("Wickets", 0, 10, 4)

    wickets_left = 10 - wickets
    crr = calculate_crr(current_score, balls)

    # Create a DataFrame with user input
    user_input = pd.DataFrame({
        'id': [2498015],  # The value doesn't matter, it's just a placeholder
        'toss_won': [toss_won],
        'decision': [decision],
        'venue_name': [venue_name],
        'season': [season],
        'home_team': [home_team],
        'away_team': [away_team],
        'current_innings': [current_innings],
        'innings_id': [innings_id],
        'current_score': [current_score],
        'wickets': [wickets],
        'wickets_left': [wickets_left],
        'crr': [crr],
    })

    # Display user input
    st.subheader("User Input:")
#    st.write(user_input)

    # Predict button
    if st.button("Predict"):
        # Make predictions
        prediction = model.predict(user_input).round(0).astype(int)
        st.sidebar.header("Model Prediction")
        st.sidebar.write("Predicted Score:", prediction[0])

if __name__ == "__main__":
    main()
