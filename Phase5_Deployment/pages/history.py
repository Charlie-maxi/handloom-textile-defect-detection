import gradio as gr
import sqlite3


DB_NAME = "textile_defect.db"


def get_prediction_history():

    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                user_id,
                input_type,
                result,
                confidence,
                prediction_time
            FROM predictions
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            return [
                ["No predictions available", "", "", "", "", ""]
            ]

        return rows

    except Exception as e:

        return [
            [f"Error: {str(e)}", "", "", "", "", ""]
        ]


def create_history_page():

    with gr.Blocks(
        title="Prediction History"
    ) as history_page:

        gr.Markdown("""
# 📜 Prediction History

View all textile defect predictions performed using the system.

The following information will be displayed:

- Prediction ID
- User ID
- Input Type
- Result
- Confidence
- Prediction Time
""")

        history_table = gr.Dataframe(
            headers=[
                "ID",
                "User ID",
                "Input Type",
                "Result",
                "Confidence",
                "Prediction Time"
            ],
            datatype=[
                "number",
                "number",
                "str",
                "str",
                "number",
                "str"
            ],
            interactive=False,
            label="Prediction History"
        )

        refresh_button = gr.Button(
            "🔄 Refresh History",
            variant="primary"
        )

        refresh_button.click(
            fn=get_prediction_history,
            inputs=[],
            outputs=history_table
        )

        history_page.load(
            fn=get_prediction_history,
            inputs=[],
            outputs=history_table
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


    return history_page