import gradio as gr


def create_home_page():

    with gr.Blocks() as home_page:

        gr.Markdown("""
# 🧵 Handloom Textile Defect Detection System

## AI-Powered Fabric Quality Inspection

Detect textile defects using multiple Machine Learning models.
""")

        gr.HTML("""
        <div style="display:flex; gap:20px; flex-wrap:wrap;">

            <a href="/register/"
               style="
               text-decoration:none;
               background:#2563eb;
               color:white;
               padding:15px 30px;
               border-radius:8px;
               font-size:18px;
               font-weight:bold;">

               📝 Register

            </a>


            <a href="/login/"
               style="
               text-decoration:none;
               background:#16a34a;
               color:white;
               padding:15px 30px;
               border-radius:8px;
               font-size:18px;
               font-weight:bold;">

               🔐 Login

            </a>

        </div>
        """)

    return home_page