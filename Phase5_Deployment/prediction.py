import joblib
import numpy as np
import time
import requests

from PIL import Image
from io import BytesIO

from feature_extraction import extract_features
from database import save_prediction
from session import get_current_user_id


# ==========================================
# LOAD MODELS
# ==========================================

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


# ==========================================
# PREDICT FABRIC
# ==========================================

# ==========================================
# PREDICT FABRIC
# ==========================================

def predict_fabric(image, input_type="upload"):

    try:

        if image is None:
            return "Please upload an image."

        image = np.array(image)

        # Handle grayscale image
        if len(image.shape) == 2:

            image = np.stack(
                [image] * 3,
                axis=-1
            )

        # Handle RGBA image
        if len(image.shape) == 3 and image.shape[2] == 4:

            image = image[:, :, :3]

        image = image.astype(np.uint8)


        # ==================================
        # FEATURE EXTRACTION
        # ==================================

        features = extract_features(image)

        features = np.array(features)

        if features.ndim == 1:

            features = features.reshape(1, -1)


        # ==================================
        # FEATURE SCALING
        # ==================================

        features_scaled = scaler.transform(
            features
        )


        # ==================================
        # MODEL PREDICTIONS
        # ==================================

        rf_pred = rf_model.predict(
            features_scaled
        )[0]

        cat_pred = cat_model.predict(
            features_scaled
        )[0]

        xgb_pred = xgb_model.predict(
            features_scaled
        )[0]

        bag_pred = bag_model.predict(
            features_scaled
        )[0]

        lgbm_pred = lgbm_model.predict(
            features_scaled
        )[0]

        gb_pred = gb_model.predict(
            features_scaled
        )[0]

        vote_pred = voting_model.predict(
            features_scaled
        )[0]


        # ==================================
        # CONFIDENCE
        # ==================================

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


        # ==================================
        # FINAL RESULT
        # ==================================

        final_result = (
            "DEFECT"
            if vote_pred == 1
            else "NO DEFECT"
        )


        # ==================================
        # SAVE PREDICTION TO DATABASE
        # ==================================

        user_id = get_current_user_id()

        if user_id is not None:

            save_prediction(
                user_id=user_id,
                input_type=input_type,
                result=final_result,
                confidence=float(vote_conf)
            )

            print(
                f"Prediction saved for User ID: {user_id}"
            )

        else:

            print(
                "Prediction not saved: No user logged in."
            )


        # ==================================
        # DISPLAY RESULT
        # ==================================

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
{final_result}

Final Confidence:
{vote_conf:.2f}%

-----------------------------------

Prediction saved successfully.
"""

        return result


    except Exception as e:

        import traceback

        print(traceback.format_exc())

        return f"Prediction Error:\n{str(e)}"


# ==========================================
# PREDICT FROM IMAGE URL
# ==========================================

def predict_from_url(url):

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if not content_type.startswith("image/"):

            return (
                "This URL is not an image.\n"
                f"Content-Type: {content_type}"
            )

        image = Image.open(
            BytesIO(response.content)
        ).convert("RGB")

        image = np.array(image)

        return predict_fabric(
    image,
    input_type="image_url"
)

    except Exception as e:

        return f"URL Prediction Error: {str(e)}"