import gradio as gr
import sqlite3


DB_NAME = "textile_defect.db"


# ==========================================
# GET ADMIN DATA
# ==========================================

def get_admin_data():

    try:

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Total users
        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )
        total_users = cursor.fetchone()[0]

        # Total predictions
        cursor.execute(
            "SELECT COUNT(*) FROM predictions"
        )
        total_predictions = cursor.fetchone()[0]

        # Defect predictions
        cursor.execute("""
            SELECT COUNT(*)
            FROM predictions
            WHERE result = 'DEFECT'
        """)
        defect_count = cursor.fetchone()[0]

        # Average rating
        cursor.execute(
            "SELECT AVG(rating) FROM feedback"
        )
        average_rating = cursor.fetchone()[0]

        if average_rating is None:
            average_rating = 0

        # Users table
        cursor.execute("""
            SELECT
                id,
                username,
                email,
                role,
                created_at
            FROM users
            ORDER BY id DESC
        """)

        users = cursor.fetchall()

        # Feedback table
        cursor.execute("""
            SELECT
                feedback.id,
                users.username,
                feedback.rating,
                feedback.comment,
                feedback.submitted_at

            FROM feedback

            LEFT JOIN users
            ON feedback.user_id = users.id

            ORDER BY feedback.id DESC
        """)

        feedback = cursor.fetchall()

        conn.close()

        return (
            f"## 👥 Total Users: {total_users}",
            f"## 🔍 Total Predictions: {total_predictions}",
            f"## ⚠️ Defects Detected: {defect_count}",
            f"## ⭐ Average Rating: {average_rating:.2f}/5",
            users,
            feedback
        )

    except Exception as e:

        error_message = f"Error: {str(e)}"

        return (
            error_message,
            error_message,
            error_message,
            error_message,
            [],
            []
        )


# ==========================================
# CREATE ADMIN PAGE
# ==========================================

def create_admin_page():

    with gr.Blocks(
        title="Admin Dashboard"
    ) as admin_page:

        gr.Markdown("""
# 🔐 Admin Dashboard

Manage and monitor the Handloom Textile Defect Detection System.
""")

        with gr.Row():

            total_users = gr.Markdown()

            total_predictions = gr.Markdown()

            defect_count = gr.Markdown()

            average_rating = gr.Markdown()


        gr.Markdown("---")


        # ======================================
        # USERS
        # ======================================

        gr.Markdown("# 👥 Registered Users")

        users_table = gr.Dataframe(

            headers=[
                "ID",
                "Username",
                "Email",
                "Role",
                "Created At"
            ],

            datatype=[
                "number",
                "str",
                "str",
                "str",
                "str"
            ],

            interactive=False
        )


        # ======================================
        # FEEDBACK
        # ======================================

        gr.Markdown("# ⭐ User Feedback")

        feedback_table = gr.Dataframe(

            headers=[
                "ID",
                "Username",
                "Rating",
                "Comment",
                "Submitted At"
            ],

            datatype=[
                "number",
                "str",
                "number",
                "str",
                "str"
            ],

            interactive=False
        )


        # ======================================
        # REFRESH
        # ======================================

        refresh_button = gr.Button(
            "🔄 Refresh Admin Dashboard",
            variant="primary"
        )


        refresh_button.click(

            fn=get_admin_data,

            inputs=[],

            outputs=[
                total_users,
                total_predictions,
                defect_count,
                average_rating,
                users_table,
                feedback_table
            ]
        )


        admin_page.load(

            fn=get_admin_data,

            inputs=[],

            outputs=[
                total_users,
                total_predictions,
                defect_count,
                average_rating,
                users_table,
                feedback_table
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


    return admin_page