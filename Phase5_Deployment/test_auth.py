from database import initialize_database
from auth import register_user, login_user


initialize_database()


# Test registration

success, message = register_user(
    "abhishek_test",
    "abhishek_test@gmail.com",
    "123456"
)

print("Registration:")
print(message)


print("\nLogin:")

success, message, user = login_user(
    "abhishek_test",
    "123456"
)

print(message)
print(user)