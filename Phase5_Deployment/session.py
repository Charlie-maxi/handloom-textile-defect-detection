# =====================================
# CURRENT USER SESSION
# =====================================

current_user = None


def set_current_user(user):

    global current_user

    current_user = user


def get_current_user():

    return current_user


def get_current_user_id():

    if current_user is None:
        return None

    return current_user["id"]