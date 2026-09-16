import gradio as gr
from auth import register_user


def register_account(username, email, password):

    success, message = register_user(
        username,
        email,
        password
    )

    if success:

        return f"""
        ✅ {message}

        Registration completed successfully!

        Please click the **Go to Login** button below.
        """

    return f"❌ {message}"


def create_register_page():

    with gr.Blocks() as register_page:

        gr.Markdown("""
# 🧵 Create Your Account

## Handloom Textile Defect Detection System

Create an account to access textile defect detection.
""")

        username = gr.Textbox(
            label="Username",
            placeholder="Enter your username"
        )

        email = gr.Textbox(
            label="Email",
            placeholder="Enter your email"
        )

        password = gr.Textbox(
            label="Password",
            type="password",
            placeholder="Enter your password"
        )

        register_button = gr.Button(
            "📝 Create Account",
            variant="primary"
        )

        output = gr.Textbox(
            label="Registration Status",
            lines=3
        )

        register_button.click(
            fn=register_account,
            inputs=[
                username,
                email,
                password
            ],
            outputs=output
        )


        # LOGIN LINK
        gr.HTML("""
        <hr>

        <h3>Already have an account?</h3>

        <a href="/login/"
           style="
           display:inline-block;
           text-decoration:none;
           background:#16a34a;
           color:white;
           padding:12px 25px;
           border-radius:8px;
           font-size:16px;
           font-weight:bold;">

           🔐 Go to Login

        </a>
        """)

    return register_page