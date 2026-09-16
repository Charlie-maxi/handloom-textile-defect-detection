import gradio as gr

from auth import login_user
from session import set_current_user


# =====================================
# LOGIN ACCOUNT
# =====================================

def login_account(username, password):

    success, message, user = login_user(
        username,
        password
    )

    if success:

        # Save logged-in user
        set_current_user(user)

        # Admin
        if user["role"] == "admin":

            return (
                f"✅ Welcome Admin {user['username']}!\n\n"
                "Login successful. Redirecting to Admin Dashboard...",
                "/admin/"
            )

        # Normal User
        return (
            f"✅ Welcome {user['username']}!\n\n"
            "Login successful. Redirecting to Dashboard...",
            "/dashboard/"
        )

    # Login failed
    return (
        f"❌ {message}",
        ""
    )


# =====================================
# CREATE LOGIN PAGE
# =====================================

def create_login_page():

    with gr.Blocks() as login_page:

        gr.Markdown("""
# 🔐 Login

## Handloom Textile Defect Detection System
""")

        # =====================================
        # INPUTS
        # =====================================

        username = gr.Textbox(
            label="Username",
            placeholder="Enter your username"
        )

        password = gr.Textbox(
            label="Password",
            type="password",
            placeholder="Enter your password"
        )

        # =====================================
        # LOGIN BUTTON
        # =====================================

        login_button = gr.Button(
            "Login",
            variant="primary"
        )

        # =====================================
        # STATUS OUTPUT
        # =====================================

        output = gr.Textbox(
            label="Login Status",
            lines=4
        )

        # Hidden textbox stores redirect URL
        redirect_url = gr.Textbox(
            visible=False
        )

        # =====================================
        # LOGIN EVENT
        # =====================================

        login_event = login_button.click(

            fn=login_account,

            inputs=[
                username,
                password
            ],

            outputs=[
                output,
                redirect_url
            ]
        )

        # =====================================
        # REDIRECT AFTER SUCCESSFUL LOGIN
        # =====================================

        login_event.then(

            fn=None,

            inputs=redirect_url,

            outputs=None,

            js="""
            (url) => {

                if (url) {

                    window.location.href = url;

                }

            }
            """
        )


        # =====================================
        # REGISTER LINK
        # =====================================

        gr.HTML("""
<hr>

<h3>Don't have an account?</h3>

<a href="/register/"
   style="
   display:inline-block;
   text-decoration:none;
   background:#2563eb;
   color:white;
   padding:12px 25px;
   border-radius:8px;
   font-size:16px;
   font-weight:bold;">

📝 Create Account

</a>
""")

    return login_page