import gradio as gr
from prediction import predict_fabric


# ==========================================
# CREATE WEBCAM PAGE
# ==========================================

def create_webcam_page():

    with gr.Blocks(
        title="Live Webcam Detection"
    ) as webcam_page:

        gr.Markdown("""
# 🎥 Live Webcam Textile Defect Detection

Turn on your webcam and show the textile or fabric to the camera.

The system will analyze the webcam image using:

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
            # WEBCAM INPUT
            # ==================================

            webcam_image = gr.Image(
                label="📷 Live Webcam",
                sources=["webcam"],
                type="numpy",
                streaming=True
            )


            # ==================================
            # LIVE RESULT
            # ==================================

            webcam_result = gr.Textbox(
                label="🔍 Live Prediction Results",
                lines=25
            )


        gr.Markdown("""
### 📌 Instructions

1. Click the **Webcam** button.
2. Allow camera permission in your browser.
3. Turn on the camera.
4. Show the textile fabric clearly.
5. The system will automatically analyze the image.
""")


        # ==================================
        # LIVE STREAM PREDICTION
        # ==================================

        webcam_image.stream(
            fn=predict_fabric,
            inputs=webcam_image,
            outputs=webcam_result
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



    return webcam_page