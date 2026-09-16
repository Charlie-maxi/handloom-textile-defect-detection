import gradio as gr


MODEL_INFORMATION = {
    "Random Forest": """
# 🌲 Random Forest

## What is it?
Random Forest is an ensemble machine learning algorithm that combines multiple Decision Trees.

## How does it work?
1. Creates multiple decision trees.
2. Each tree makes a prediction.
3. The final result is selected using majority voting.

## Why is it used in this project?
It learns relationships between textile image features and defect labels.

## Advantages
- High accuracy
- Reduces overfitting
- Handles complex data

## Limitations
- Requires more memory
- Can be slower with many trees

## Project Role
Predicts whether the textile image contains a **DEFECT** or **NO DEFECT**.
""",

    "Bagging": """
# 👜 Bagging Classifier

## What is it?
Bagging means Bootstrap Aggregating.

It trains multiple models using different random samples of the dataset and combines their predictions.

## How does it work?
1. Creates random samples from the training data.
2. Trains multiple models.
3. Each model makes a prediction.
4. Predictions are combined.

## Advantages
- Reduces variance
- Improves prediction stability
- Helps reduce overfitting

## Limitations
- Uses more computational resources
- Requires multiple models

## Project Role
Provides an additional ensemble prediction for textile defect detection.
""",

    "Gradient Boosting": """
# 📈 Gradient Boosting

## What is it?
Gradient Boosting is an ensemble machine learning algorithm where models are trained sequentially.

Each new model tries to correct the errors made by previous models.

## How does it work?
Model 1 makes predictions.

Then the errors are calculated.

Model 2 tries to correct those errors.

This process continues for multiple models.

## Advantages
- High predictive performance
- Learns complex relationships

## Limitations
- Can be slower to train
- Requires parameter tuning
- Can overfit

## Project Role
Predicts whether extracted textile features represent a defect or no defect.
""",

    "LightGBM": """
# 💡 LightGBM

## Full Form
Light Gradient Boosting Machine.

## What is it?
LightGBM is a fast and efficient gradient boosting framework.

## Why is it used?
It provides efficient learning and good performance for structured numerical features.

## Advantages
- Fast
- Memory efficient
- High performance

## Limitations
- Can overfit small datasets
- Requires parameter tuning

## Project Role
Analyzes extracted textile image features and predicts DEFECT or NO DEFECT.
""",

    "XGBoost": """
# ⚡ XGBoost

## Full Form
Extreme Gradient Boosting.

## What is it?
XGBoost is an optimized implementation of gradient boosting.

## How does it work?
Decision trees are trained sequentially.

Each new tree attempts to correct the errors of previous trees.

## Advantages
- High accuracy
- Regularization helps reduce overfitting
- Efficient algorithm

## Limitations
- Requires parameter tuning
- Can use more computation

## Project Role
Predicts textile defects using extracted image features.
""",

    "CatBoost": """
# 🎯 CatBoost

## Full Form
Categorical Boosting.

## What is it?
CatBoost is a gradient boosting algorithm based on decision trees.

## How does it work?
Multiple trees are built sequentially.

Each new tree attempts to improve the prediction made by previous trees.

## Advantages
- Strong predictive performance
- Helps reduce overfitting
- Requires less preprocessing

## Limitations
- Training can take time
- Configuration can be complex

## Project Role
Independently predicts DEFECT or NO DEFECT.
""",

    "Voting Classifier": """
# 🗳️ Voting Classifier

## What is it?
A Voting Classifier combines predictions from multiple machine learning models.

## Models Used
- Random Forest
- Bagging
- Gradient Boosting
- LightGBM
- XGBoost
- CatBoost

## How does it work?
Each model makes a prediction.

The Voting Classifier combines these predictions and produces the final result.

## Advantages
- Combines strengths of multiple models
- More reliable prediction
- Less dependent on a single model

## Limitations
- Requires multiple trained models
- Uses more computational resources

## Project Role
Produces the final **DEFECT** or **NO DEFECT** result.
"""
}


def show_model(model_name):

    return MODEL_INFORMATION.get(
        model_name,
        "Please select a model."
    )


def create_models_page():

    with gr.Blocks(
        title="Machine Learning Models"
    ) as models_page:

        gr.Markdown(
            """
# 🤖 Machine Learning Model Details

Select a model to view its detailed explanation.

This is useful for explaining each machine learning model during project demonstration or viva.
"""
        )

        model_selector = gr.Radio(
            choices=[
                "Random Forest",
                "Bagging",
                "Gradient Boosting",
                "LightGBM",
                "XGBoost",
                "CatBoost",
                "Voting Classifier"
            ],
            value="Random Forest",
            label="Select a Machine Learning Model"
        )

        model_details = gr.Markdown(
            value=MODEL_INFORMATION["Random Forest"]
        )

        model_selector.change(
            fn=show_model,
            inputs=model_selector,
            outputs=model_details
        )
        gr.HTML("""
<hr>

<h3>Navigation</h3>

<div style="display:flex; gap:10px; flex-wrap:wrap;">

<a href="/dashboard/" style="padding:10px; background:#2563eb; color:white; text-decoration:none; border-radius:6px;">
🏠 Dashboard
</a>

<a href="/detection/" style="padding:10px; background:#16a34a; color:white; text-decoration:none; border-radius:6px;">
📤 Detection
</a>

<a href="/webcam/" style="padding:10px; background:#9333ea; color:white; text-decoration:none; border-radius:6px;">
🎥 Webcam
</a>

<a href="/image-url/" style="padding:10px; background:#ea580c; color:white; text-decoration:none; border-radius:6px;">
🌐 Image URL
</a>

<a href="/models/" style="padding:10px; background:#0891b2; color:white; text-decoration:none; border-radius:6px;">
🤖 Models
</a>

<a href="/history/" style="padding:10px; background:#ca8a04; color:white; text-decoration:none; border-radius:6px;">
📜 History
</a>

<a href="/feedback/" style="padding:10px; background:#db2777; color:white; text-decoration:none; border-radius:6px;">
⭐ Feedback
</a>

</div>
""")

 

    return models_page