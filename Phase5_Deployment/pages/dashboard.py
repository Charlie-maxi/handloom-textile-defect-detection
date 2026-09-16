import gradio as gr
from database import get_admin_dashboard_stats


def create_dashboard_page():

    # For now we display overall system statistics.
    # Later we will connect the logged-in user's session.

    def load_dashboard():

        stats = get_admin_dashboard_stats()

        return (
            f"""
# 📊 Dashboard

## 🧵 Handloom Textile Defect Detection System

Welcome to the Textile Defect Detection Dashboard.
""",

            f"👥 Total Users\n\n# {stats['total_users']}",

            f"🔍 Total Predictions\n\n# {stats['total_predictions']}",

            f"⚠️ Defects Detected\n\n# {stats['defect_count']}",

            f"⭐ Average Rating\n\n# {stats['average_rating']} / 5"
        )


    with gr.Blocks(
        title="Dashboard"
    ) as dashboard_page:

        title = gr.Markdown()

        with gr.Row():

            total_users = gr.Markdown()

            total_predictions = gr.Markdown()

            defect_count = gr.Markdown()

            average_rating = gr.Markdown()


        gr.Markdown("---")


        gr.Markdown("""
# 🚀 System Features

Select a feature below.
""")


        with gr.Row():

            gr.Markdown("""
### 📤 Upload Detection

Upload a textile image and detect defects.

➡️ Go to `/detection`
""")


            gr.Markdown("""
### 🎥 Live Webcam Detection

Use your webcam for live textile defect detection.

➡️ Go to `/webcam`
""")


            gr.Markdown("""
### 🌐 Image URL Detection

Paste an online textile image URL.

➡️ Go to `/image-url`
""")


        with gr.Row():

            gr.Markdown("""
### 🤖 Machine Learning Models

View detailed information about every model.

➡️ Go to `/models`
""")


            gr.Markdown("""
### 📜 Prediction History

View previously generated predictions.

➡️ Go to `/history`
""")


            gr.Markdown("""
### ⭐ Feedback

Rate and provide feedback about the system.

➡️ Go to `/feedback`
""")


        refresh_button = gr.Button(
            "🔄 Refresh Dashboard",
            variant="primary"
        )


        refresh_button.click(

            fn=load_dashboard,

            inputs=[],

            outputs=[
                title,
                total_users,
                total_predictions,
                defect_count,
                average_rating
            ]
        )


        dashboard_page.load(

            fn=load_dashboard,

            inputs=[],

            outputs=[
                title,
                total_users,
                total_predictions,
                defect_count,
                average_rating
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


    return dashboard_page