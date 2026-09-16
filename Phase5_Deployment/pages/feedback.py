import gradio as gr
from database import save_feedback


# ==========================================
# SUBMIT FEEDBACK
# ==========================================

def submit_feedback(rating, comment):

    try:

        # Temporary user ID
        # Later we connect the actual logged-in user
        user_id = 1

        if rating is None:
            return "❌ Please select a rating."

        if not comment or comment.strip() == "":
            return "❌ Please enter your feedback."

        save_feedback(
            user_id,
            int(rating),
            comment
        )

        return "✅ Thank you! Your feedback has been submitted successfully."

    except Exception as e:

        return f"❌ Error: {str(e)}"


# ==========================================
# CREATE FEEDBACK PAGE
# ==========================================

def create_feedback_page():

    with gr.Blocks(
        title="Feedback"
    ) as feedback_page:

        gr.Markdown("""
# ⭐ Feedback

Your feedback helps us improve the Handloom Textile Defect Detection System.

Please rate your experience and share your comments.
""")

        gr.Markdown("---")

        rating = gr.Radio(
            choices=[
                ("⭐ 1 - Very Poor", 1),
                ("⭐⭐ 2 - Poor", 2),
                ("⭐⭐⭐ 3 - Average", 3),
                ("⭐⭐⭐⭐ 4 - Good", 4),
                ("⭐⭐⭐⭐⭐ 5 - Excellent", 5)
            ],
            label="Rate Your Experience"
        )

        comment = gr.Textbox(
            label="Your Feedback",
            placeholder="Write your feedback here...",
            lines=6
        )

        submit_button = gr.Button(
            "⭐ Submit Feedback",
            variant="primary"
        )

        status = gr.Textbox(
            label="Status",
            interactive=False
        )

        submit_button.click(
            fn=submit_feedback,
            inputs=[
                rating,
                comment
            ],
            outputs=status
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

    return feedback_page