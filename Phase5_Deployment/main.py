from fastapi import FastAPI, UploadFile, File
import tempfile
import joblib
import numpy as np

from feature_extraction import extract_features

app = FastAPI(
    title="Handloom Textile Defect Detection API"
)

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

xgb_model = joblib.load(
    "saved_models/xgboost.pkl"
)

voting_model = joblib.load(
    "saved_models/voting.pkl"
)


@app.get("/")
def home():

    return {
        "message":
        "Handloom Textile Defect Detection API Running"
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    ) as temp_file:

        temp_file.write(
            await file.read()
        )

        image_path = temp_file.name

    features = extract_features(
        image_path
    )

    features_scaled = scaler.transform(
        features
    )

    rf_pred = rf_model.predict(
        features_scaled
    )[0]

    cat_pred = cat_model.predict(
        features_scaled
    )[0]

    xgb_pred = xgb_model.predict(
        features_scaled
    )[0]

    vote_pred = voting_model.predict(
        features_scaled
    )[0]

    rf_prob = float(
        np.max(
            rf_model.predict_proba(
                features_scaled
            )
        )
    )

    cat_prob = float(
        np.max(
            cat_model.predict_proba(
                features_scaled
            )
        )
    )

    xgb_prob = float(
        np.max(
            xgb_model.predict_proba(
                features_scaled
            )
        )
    )

    vote_prob = float(
        np.max(
            voting_model.predict_proba(
                features_scaled
            )
        )
    )

    return {

        "Random Forest": {

            "Prediction":
            "Defect" if rf_pred == 1 else "No Defect",

            "Confidence":
            round(
                rf_prob * 100,
                2
            )
        },

        "CatBoost": {

            "Prediction":
            "Defect" if cat_pred == 1 else "No Defect",

            "Confidence":
            round(
                cat_prob * 100,
                2
            )
        },

        "XGBoost": {

            "Prediction":
            "Defect" if xgb_pred == 1 else "No Defect",

            "Confidence":
            round(
                xgb_prob * 100,
                2
            )
        },

        "Voting": {

            "Prediction":
            "Defect" if vote_pred == 1 else "No Defect",

            "Confidence":
            round(
                vote_prob * 100,
                2
            )
        }
    }