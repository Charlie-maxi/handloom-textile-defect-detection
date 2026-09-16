import gradio as gr
from prediction import predict_from_url


# ==========================================
# CREATE IMAGE URL DETECTION PAGE
# ==========================================

def create_image_url_page():

    with gr.Blocks(
        title="Image URL Detection"
    ) as image_url_page:

        gr.Markdown("""
# 🌐 Textile Defect Detection Using Image URL

Paste the **direct URL of a textile or fabric image**.

The system will download the image and analyze it using multiple Machine Learning models.

### Supported Models

- 🌲 Random Forest
- 📈 Gradient Boosting
- 👜 Bagging
- 💡 LightGBM
- ⚡ XGBoost
- 🎯 CatBoost
- 🗳️ Voting Classifier
""")

        gr.Markdown("---")

        # ==================================
        # URL INPUT
        # ==================================

        image_url = gr.Textbox(
            label="Image URL",
            placeholder="Paste direct image URL here..."
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
        # RESULT OUTPUT
        # ==================================

        prediction_result = gr.Textbox(
            label="Prediction Results",
            lines=25
        )


        # ==================================
        # PREDICTION EVENT
        # ==================================

        predict_button.click(
            fn=predict_from_url,
            inputs=image_url,
            outputs=prediction_result
        )


        # ==================================
        # CLEAR EVENT
        # ==================================

        clear_button.click(
            fn=lambda: ("", ""),
            inputs=[],
            outputs=[
                image_url,
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




    return image_url_page