import sqlite3
from datetime import datetime


DB_NAME = "textile_defect.db"


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():

    conn = sqlite3.connect(DB_NAME)

    return conn


# =====================================
# INITIALIZE DATABASE
# =====================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TEXT
    )
    """)

    # LOGIN HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        login_time TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # PREDICTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        input_type TEXT,
        result TEXT,
        confidence REAL,
        prediction_time TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # FEEDBACK TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        rating INTEGER,
        comment TEXT,
        submitted_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# =====================================
# CREATE USER
# =====================================

def create_user(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users
        (username, email, password, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            email,
            password,
            "user",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:

        return False, "Username or Email already exists."

    finally:

        conn.close()


# =====================================
# GET USER
# =====================================

def get_user(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user


# =====================================
# LOGIN USER
# =====================================

def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, email, password, role
    FROM users
    WHERE username = ?
    AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:

        save_login(user[0])

        return True, user

    return False, None


# =====================================
# SAVE LOGIN HISTORY
# =====================================

def save_login(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO login_history
    (user_id, login_time)
    VALUES (?, ?)
    """, (
        user_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =====================================
# SAVE PREDICTION
# =====================================

def save_prediction(user_id, input_type, result, confidence):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (user_id, input_type, result, confidence, prediction_time)
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        input_type,
        result,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =====================================
# GET USER PREDICTIONS
# =====================================

def get_user_predictions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        input_type,
        result,
        confidence,
        prediction_time
    FROM predictions
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    predictions = cursor.fetchall()

    conn.close()

    return predictions


# =====================================
# SAVE FEEDBACK
# =====================================

def save_feedback(user_id, rating, comment):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO feedback
    (user_id, rating, comment, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        rating,
        comment,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return True


# =====================================
# USER DASHBOARD STATISTICS
# =====================================

def get_user_dashboard_stats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE user_id = ?
    """, (user_id,))

    total_predictions = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE user_id = ?
    AND result = 'DEFECT'
    """, (user_id,))

    defect_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE user_id = ?
    AND result = 'NO DEFECT'
    """, (user_id,))

    no_defect_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT AVG(rating)
    FROM feedback
    WHERE user_id = ?
    """, (user_id,))

    average_rating = cursor.fetchone()[0]

    conn.close()

    if average_rating is None:
        average_rating = 0

    return {
        "total_predictions": total_predictions,
        "defect_count": defect_count,
        "no_defect_count": no_defect_count,
        "average_rating": round(average_rating, 2)
    }


# =====================================
# ADMIN DASHBOARD STATISTICS
# =====================================

def get_admin_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM login_history")
    total_logins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE result = 'DEFECT'
    """)
    defect_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE result = 'NO DEFECT'
    """)
    no_defect_count = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(rating) FROM feedback")
    average_rating = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = cursor.fetchone()[0]

    conn.close()

    if average_rating is None:
        average_rating = 0

    return {
        "total_users": total_users,
        "total_logins": total_logins,
        "total_predictions": total_predictions,
        "defect_count": defect_count,
        "no_defect_count": no_defect_count,
        "average_rating": round(average_rating, 2),
        "total_feedback": total_feedback
    }


# =====================================
# GET ALL FEEDBACK
# =====================================

def get_all_feedback():

    conn = get_connection()
    cursor = conn.cursor()

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

    feedback_data = cursor.fetchall()

    conn.close()

    return feedback_data


# =====================================
# CREATE DEFAULT ADMIN
# =====================================

def create_default_admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM users
    WHERE username = ?
    """, ("admin",))

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
        INSERT INTO users
        (username, email, password, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            "admin",
            "admin@textile.com",
            "admin123",
            "admin",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        print("Default admin created.")

    conn.close()


# =====================================
# INITIALIZE DATABASE
# =====================================

if __name__ == "__main__":

    initialize_database()
    create_default_admin()

    print("Database initialized successfully!")