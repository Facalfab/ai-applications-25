# Pro Player Prediction

## Project Description
This application predicts whether a football player is likely to become a professional based on selected performance metrics (per 90 minutes).  
The model was trained on data from professional and youth players, using manually engineered features and a classification approach.

## App
| Platform        | Link |
|----------------|------|
| Hugging Face Space | [Pro Player Prediction App](https://huggingface.co/spaces/YOUR_USERNAME/pro-player-prediction) |
| Code         | [GitHub Repository](https://github.com/Facalfab/ai-applications-25/) |

## Data Sources and Features

| Source          | Description                          |
|-----------------|--------------------------------------|
| Kaggle Dataset  | Player stats from professional leagues |
| Wyscout Data    | Swiss players from Super League and youth levels (U17, U19, U21) |

### Features

| Feature            | Description                                         |
|--------------------|-----------------------------------------------------|
| minutes_played     | Total minutes played (season)                      |
| passes_total       | Passes attempted per 90 minutes                    |
| passes_success     | Passes completed per 90 minutes                    |
| pass_accuracy      | passes_success / passes_total                      |
| shots_on_target    | Accurate shots per 90 minutes                      |
| duels_total        | Total duels per 90 minutes                         |
| duels_won          | Duels won per 90 minutes                           |
| recoveries         | Ball recoveries per 90 minutes                     |
| ball_losses        | Ball losses per 90 minutes                         |
| activity_score     | passes_success + duels_won + recoveries            |

Additionally:
- `activity_percent = (activity_score / 300) * 100` was shown in the output as "Overall Effectiveness".

---

## Feature Engineering

| Feature            | Description |
|--------------------|-------------|
| pass_accuracy      | `passes_success / passes_total` |
| activity_score     | `passes_success + duels_won + recoveries` |
| activity_percent   | `activity_score / 300 * 100` – shown in output as Overall Effectiveness % |

---

## Model Training

### Data Size
- Approx. 5000 players total

### Class Definition
- `is_pro = 1` → professional player  
- `is_pro = 0` → non-professional or youth player

### Training / Test Split
- 80/20 random split  
- Train Accuracy: 1.0000  
- Test Accuracy: 0.9904  
High generalization, no sign of overfitting

## Performance

| It. Nr | Model              | Performance | Features | Description |
|--------|--------------------|-------------|----------|-------------|
| 1      | Logistic Regression| Train: 0.99, Test: 0.98 | 10 engineered features | Slight underfitting, interpretable baseline |
| 2      | Random Forest      | Train: 1.00, Test: 0.99 | Same as above | High generalization, final model selected |

---

### Probability Threshold:
To increase precision, the classification threshold was manually set to 80%:
```python
prediction = 1 if probability > 0.8 else 0
```

---

## Decision Threshold

By default, most classifiers use a probability threshold of **50%** to classify.  
To ensure higher certainty, we manually set the threshold to:

```python
prediction = 1 if probability > 0.8 else 0
```
---
### References
![image](https://github.com/user-attachments/assets/4b19fbd6-ec1e-4743-81f4-a6e0efe0414f)
![image](https://github.com/user-attachments/assets/8664158b-cde8-4b88-906f-53f26119000a)


## Limitations
- Some labels were synthetically assigned due to lack of real youth performance data.
- The 300-point scale for activity score is a heuristic.
- All predictions are based solely on performance metrics and do not consider external factors (e.g., injuries, market value).

