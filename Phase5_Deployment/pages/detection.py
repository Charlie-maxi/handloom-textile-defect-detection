import gradio as gr
from prediction import predict_fabric


# ==========================================
# CREATE DETECTION PAGE
# ==========================================

def create_detection_page():

    with gr.Blocks(
        title="Textile Image Detection"
    ) as detection_page:

        gr.Markdown("""
# 📤 Textile Defect Detection

Upload a textile or fabric image and the system will analyze it using multiple Machine Learning models.

The following models are used:

- Random Forest
- Gradient Boosting
- Bagging
- LightGBM
- XGBoost
- CatBoost
- Voting Classifier
""")

        gr.Markdown("---")

        with gr.Row():

            # ==================================
            # IMAGE INPUT
            # ==================================

            upload_image = gr.Image(
                label="Upload Fabric Image",
                type="numpy",
                sources=["upload"]
            )

            # ==================================
            # PREDICTION OUTPUT
            # ==================================

            prediction_result = gr.Textbox(
                label="Prediction Results",
                lines=25
            )


        # ==================================
        # BUTTONS
        # ==================================

        with gr.Row():

            predict_button = gr.Button(
                "🔍 Predict Defect",
                variant="primary"
            )

            clear_button = gr.Button(
                "🗑️ Clear"
            )


        # ==================================
        # PREDICTION EVENT
        # ==================================

        predict_button.click(
            fn=predict_fabric,
            inputs=upload_image,
            outputs=prediction_result
        )


        # ==================================
        # CLEAR EVENT
        # ==================================

        clear_button.click(
            fn=lambda: (None, ""),
            inputs=[],
            outputs=[
                upload_image,
                prediction_result
            ]
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


    return detection_page