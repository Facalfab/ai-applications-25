import gradio as gr
import joblib
import numpy as np

# Load the trained model
model = joblib.load("pro_player_model.pkl")

# Define prediction function
def predict_pro_status(minutes_played, passes_total, passes_success,
                       shots_on_target, duels_total, duels_won,
                       recoveries, ball_losses, goals, assists):

    # Cap inputs to ensure logical consistency
    passes_success = min(passes_success, passes_total)
    duels_won = min(duels_won, duels_total)

    # Derived features
    activity_score = passes_success + duels_won + recoveries
    activity_percent = (activity_score / 300) * 100  # simple normalization for display

    # Format input for the model
    X = np.array([[minutes_played, passes_total, passes_success, passes_success / passes_total if passes_total > 0 else 0,
                   shots_on_target, duels_total, duels_won,
                   recoveries, ball_losses, activity_score, goals, assists]])

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]  # Probability of "pro"

    result = "Pro Player" if prediction == 1 else "Amateur"
    summary = f"### Prediction: {result}\n"
    summary += f"**Probability of being a Pro:** {probability:.2%}\n\n"
    summary += f"**Overall Effectiveness (calculated):** {activity_percent:.2f}%\n"
    summary += "This value is based on successful passes, duels won, and recoveries, relative to a maximum reference of 300."
    return summary

# Build UI with gr.Blocks
with gr.Blocks() as demo:
    gr.Markdown("# ⚽ Pro Player Prediction")
    gr.Markdown("Enter the player's performance metrics to predict if they are likely to be a professional footballer.")

    with gr.Row():
        minutes_played = gr.Slider(0, 10000, label="Minutes Played (per season)")
        shots_on_target = gr.Slider(0, 10, label="Shots on Target (per 90')")

    with gr.Row():
        passes_total = gr.Slider(0, 200, label="Total Passes (per 90')")
        passes_success = gr.Slider(0, 200, label="Successful Passes (per 90')")

    with gr.Row():
        duels_total = gr.Slider(0, 100, label="Total Duels (per 90')")
        duels_won = gr.Slider(0, 100, label="Duels Won (per 90')")

    with gr.Row():
        recoveries = gr.Slider(0, 100, label="Recoveries (per 90')")
        ball_losses = gr.Slider(0, 100, label="Ball Losses (per 90')")

    with gr.Row():
        goals = gr.Slider(0, 10, label="Goals (per 90')")
        assists = gr.Slider(0, 10, label="Assists (per 90')")

    predict_btn = gr.Button("Predict")
    output = gr.Markdown()

    predict_btn.click(
        predict_pro_status,
        inputs=[minutes_played, passes_total, passes_success,
                shots_on_target, duels_total, duels_won,
                recoveries, ball_losses, goals, assists],
        outputs=output
    )

demo.launch()
