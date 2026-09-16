import gradio as gr
import joblib
import numpy as np
import time
import requests
from PIL import Image
from io import BytesIO

from feature_extraction import extract_features

# Load Models

scaler = joblib.load(
    "saved_models/scaler.pkl"
)

rf_model = joblib.load(
    "saved_models/random_forest.pkl"
)

cat_model = joblib.load(
    "saved_models/catboost.pkl"
)
bag_model = joblib.load(
    "saved_models/bagging.pkl"
)

lgbm_model = joblib.load(
    "saved_models/lightgbm.pkl"
)

gb_model = joblib.load(
    "saved_models/gradient_boosting.pkl"
)

xgb_model = joblib.load(
    "saved_models/xgboost.pkl"
)

voting_model = joblib.load(
    "saved_models/voting.pkl"
)
bag_model = joblib.load(
    "saved_models/bagging.pkl"
)

lgbm_model = joblib.load(
    "saved_models/lightgbm.pkl"
)

gb_model = joblib.load(
    "saved_models/gradient_boosting.pkl"
)


def predict_fabric(image):

    try:

        if image is None:
            return "Waiting for webcam image..."

        image = np.array(image)

        print("Image received:", image.shape)

        # Handle grayscale image
        if len(image.shape) == 2:
            image = np.stack([image] * 3, axis=-1)

        # Handle RGBA image
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = image[:, :, :3]

        image = image.astype(np.uint8)

        # Extract features
        features = extract_features(image)

        features = np.array(features)

        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Scale
        features_scaled = scaler.transform(features)

        # Predictions
        rf_pred = rf_model.predict(features_scaled)[0]
        cat_pred = cat_model.predict(features_scaled)[0]
        xgb_pred = xgb_model.predict(features_scaled)[0]
        bag_pred = bag_model.predict(features_scaled)[0]
        lgbm_pred = lgbm_model.predict(features_scaled)[0]
        gb_pred = gb_model.predict(features_scaled)[0]
        vote_pred = voting_model.predict(features_scaled)[0]

        # Confidence
        rf_conf = np.max(
            rf_model.predict_proba(features_scaled)
        ) * 100

        gb_conf = np.max(
            gb_model.predict_proba(features_scaled)
        ) * 100

        bag_conf = np.max(
            bag_model.predict_proba(features_scaled)
        ) * 100

        lgbm_conf = np.max(
            lgbm_model.predict_proba(features_scaled)
        ) * 100

        xgb_conf = np.max(
            xgb_model.predict_proba(features_scaled)
        ) * 100

        cat_conf = np.max(
            cat_model.predict_proba(features_scaled)
        ) * 100

        vote_conf = np.max(
            voting_model.predict_proba(features_scaled)
        ) * 100

        result = f"""
Random Forest:
{'Defect' if rf_pred == 1 else 'No Defect'}
Confidence: {rf_conf:.2f}%

Gradient Boosting:
{'Defect' if gb_pred == 1 else 'No Defect'}
Confidence: {gb_conf:.2f}%

Bagging:
{'Defect' if bag_pred == 1 else 'No Defect'}
Confidence: {bag_conf:.2f}%

LightGBM:
{'Defect' if lgbm_pred == 1 else 'No Defect'}
Confidence: {lgbm_conf:.2f}%

XGBoost:
{'Defect' if xgb_pred == 1 else 'No Defect'}
Confidence: {xgb_conf:.2f}%

CatBoost:
{'Defect' if cat_pred == 1 else 'No Defect'}
Confidence: {cat_conf:.2f}%

Voting Classifier:
{'Defect' if vote_pred == 1 else 'No Defect'}
Confidence: {vote_conf:.2f}%

-----------------------------------

FINAL RESULT:
{'DEFECT' if vote_pred == 1 else 'NO DEFECT'}

-----------------------------------
"""

        return result

    except Exception as e:

        import traceback

        print(traceback.format_exc())

        return f"Prediction Error:\n{str(e)}"

def predict_from_url(url):
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))

        response.raise_for_status()

        if not response.headers.get("Content-Type", "").startswith("image/"):
            return f"This URL is not an image.\nContent-Type: {response.headers.get('Content-Type')}"

        image = Image.open(BytesIO(response.content)).convert("RGB")
        image = np.array(image)

        return predict_fabric(image)

    except Exception as e:
        return str(e)

with gr.Blocks() as upload_demo:

    gr.Markdown(
        "# Handloom Textile Defect Detection System"
    )

    gr.Markdown(
        """
        Upload a fabric image or capture an image using your webcam.

        **Models Used:**
        Random Forest | CatBoost | Bagging | LightGBM |
        Gradient Boosting | XGBoost | Voting Ensemble
        """
    )

    with gr.Row():

        image_input = gr.Image(
            label="Upload or Capture Fabric Image",
            type="numpy",
            sources=["upload", "webcam"]
        )

        prediction_output = gr.Textbox(
            label="Prediction Results",
            lines=25
        )

    with gr.Row():

        clear_button = gr.Button("Clear")

        submit_button = gr.Button(
            "Submit",
            variant="primary"
        )

    # Submit prediction
    submit_button.click(
        fn=predict_fabric,
        inputs=image_input,
        outputs=prediction_output
    )

    # Clear image and result
    clear_button.click(
        fn=lambda: (None, ""),
        inputs=[],
        outputs=[
            image_input,
            prediction_output
        ]
    )

# ==========================================
# LIVE WEBCAM DETECTION
# ==========================================

with gr.Blocks() as webcam_demo:

    gr.Markdown("# 🎥 Live Webcam Textile Defect Detection")

    gr.Markdown(
        "Turn on the webcam and show the fabric to the camera."
    )

    with gr.Row():

        webcam_input = gr.Image(
            label="Live Webcam",
            sources=["webcam"],
            type="numpy",
            streaming=True
        )

        webcam_output = gr.Textbox(
            label="Live Prediction Results",
            lines=25
        )

    webcam_input.stream(
        fn=predict_fabric,
        inputs=webcam_input,
        outputs=webcam_output
    )
url_demo = gr.Interface(

    fn=predict_from_url,

    inputs=gr.Textbox(
        label="Paste Image URL"
    ),

    outputs=gr.Textbox(
        label="Prediction Results"
    ),

    title="Handloom Textile Defect Detection System",

    description="""
Paste the direct URL of a fabric image for defect detection.
"""
)

demo = gr.TabbedInterface(

    [
        upload_demo,
        webcam_demo,
        url_demo
    ],

    [
        "Upload Image",
        "🎥 Live Webcam",
        "Image URL"
    ]
)

demo.launch(share=True)