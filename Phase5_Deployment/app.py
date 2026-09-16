import gradio as gr
from fastapi import FastAPI

from database import initialize_database
from database import create_default_admin

from pages.home import create_home_page
from pages.login import create_login_page
from pages.register import create_register_page
from pages.dashboard import create_dashboard_page
from pages.detection import create_detection_page
from pages.webcam import create_webcam_page
from pages.image_url import create_image_url_page
from pages.models import create_models_page
from pages.history import create_history_page
from pages.feedback import create_feedback_page
from pages.admin import create_admin_page


# =====================================
# DATABASE INITIALIZATION
# =====================================

initialize_database()

create_default_admin()


# =====================================
# FASTAPI APP
# =====================================

app = FastAPI()


# =====================================
# CREATE PAGES
# =====================================

home_page = create_home_page()

register_page = create_register_page()

login_page = create_login_page()

dashboard_page = create_dashboard_page()

detection_page = create_detection_page()

webcam_page = create_webcam_page()

image_url_page = create_image_url_page()

models_page = create_models_page()

history_page = create_history_page()

feedback_page = create_feedback_page()

admin_page = create_admin_page()


# =====================================
# MOUNT REGISTER
# =====================================

app = gr.mount_gradio_app(
    app,
    register_page,
    path="/register"
)


# =====================================
# MOUNT LOGIN
# =====================================

app = gr.mount_gradio_app(
    app,
    login_page,
    path="/login"
)


# =====================================
# MOUNT DASHBOARD
# =====================================

app = gr.mount_gradio_app(
    app,
    dashboard_page,
    path="/dashboard"
)


# =====================================
# MOUNT DETECTION
# =====================================

app = gr.mount_gradio_app(
    app,
    detection_page,
    path="/detection"
)


# =====================================
# MOUNT WEBCAM
# =====================================

app = gr.mount_gradio_app(
    app,
    webcam_page,
    path="/webcam"
)


# =====================================
# MOUNT IMAGE URL
# =====================================

app = gr.mount_gradio_app(
    app,
    image_url_page,
    path="/image-url"
)


# =====================================
# MOUNT MODELS
# =====================================

app = gr.mount_gradio_app(
    app,
    models_page,
    path="/models"
)


# =====================================
# MOUNT HISTORY
# =====================================

app = gr.mount_gradio_app(
    app,
    history_page,
    path="/history"
)


# =====================================
# MOUNT FEEDBACK
# =====================================

app = gr.mount_gradio_app(
    app,
    feedback_page,
    path="/feedback"
)


# =====================================
# MOUNT ADMIN
# =====================================

app = gr.mount_gradio_app(
    app,
    admin_page,
    path="/admin"
)


# =====================================
# IMPORTANT!
# HOME PAGE MUST BE LAST
# =====================================

app = gr.mount_gradio_app(
    app,
    home_page,
    path="/"
)


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":

    import uvicorn
    import os

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
