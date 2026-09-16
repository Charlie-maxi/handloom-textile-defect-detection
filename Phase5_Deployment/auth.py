from database import create_user, get_user, save_login


# =====================================
# REGISTER USER
# =====================================

def register_user(username, email, password):

    if not username or not email or not password:
        return False, "All fields are required."

    return create_user(
        username,
        email,
        password
    )


# =====================================
# LOGIN USER
# =====================================

def login_user(username, password):

    if not username or not password:
        return False, "Username and password are required.", None

    user = get_user(username)

    if user is None:
        return False, "User not found.", None

    # user structure:
    # 0 = id
    # 1 = username
    # 2 = email
    # 3 = password
    # 4 = role
    # 5 = created_at

    if user[3] != password:
        return False, "Incorrect password.", None

    save_login(user[0])

    user_data = {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "role": user[4]
    }

    return True, "Login successful!", user_data