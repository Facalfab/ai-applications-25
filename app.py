import gradio as gr
import joblib
import numpy as np

# Load the trained model
model = joblib.load("pro_player_model.pkl")

# Define prediction function
def predict_pro_status(minutes_played, passes_total, passes_success, pass_accuracy,
                       shots_on_target, duels_total, duels_won,
                       recoveries, ball_losses, activity_score):

    # Format input for the model
    X = np.array([[minutes_played, passes_total, passes_success, pass_accuracy,
                   shots_on_target, duels_total, duels_won,
                   recoveries, ball_losses, activity_score]])

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]  # Probability of "pro"

    result = "🔵 Pro Player" if prediction == 1 else "🔴 Non-Pro Player"
    return f"Prediction: {result}\nProbability of being a Pro: {probability:.2%}"

# Define Gradio interface
inputs = [
    gr.Slider(0, 10000, label="Minutes Played (total)"),
    gr.Slider(0, 200, label="Total Passes (per 90')"),
    gr.Slider(0, 200, label="Successful Passes (per 90')"),
    gr.Slider(0, 1, step=0.01, label="Pass Accuracy (0-1)"),
    gr.Slider(0, 10, label="Shots on Target (per 90')"),
    gr.Slider(0, 100, label="Total Duels (per 90')"),
    gr.Slider(0, 100, label="Duels Won (per 90')"),
    gr.Slider(0, 100, label="Recoveries (per 90')"),
    gr.Slider(0, 100, label="Ball Losses (per 90')"),
    gr.Slider(0, 300, label="Overall Effectiveness (Score)")
]

iface = gr.Interface(
    fn=predict_pro_status,
    inputs=inputs,
    outputs="text",
    title="Pro Player Prediction",
    description="This app predicts whether a football player is likely to be a professional based on performance metrics."
)

iface.launch()
