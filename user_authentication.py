# Import the necessary sqlite_con functions from Firebase_auth.py
from sqlite_con import register_user, login_user

# Function to handle user registration
def register_user_wrapper(email, password, first_name, last_name):
    # Call the registration function from sqlite_con.py
    return register_user(email, password, first_name, last_name)

# Function to handle user login
def login_user_wrapper(email, password):
    # Call the login function from sqlite_con.py
    return login_user(email, password)
