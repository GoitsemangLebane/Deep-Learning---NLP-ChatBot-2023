import tkinter as tk
#from user_authentication import register_user_wrapper, login_user_wrapper
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import the required modules from Pillow
import sqlite3
from tkinter import messagebox

# Connect to a SQLite database (it will create the file if it doesn't exist)
print("Debug: Before connecting to the database")
conn = sqlite3.connect('aichatbot.db')
print("Debug: After connecting to the database")

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute SQL commands
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT,
        password TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')

class PageManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("HelpR")
        self.geometry("470x550+320+100")
        self.resizable(width=False, height=False)
        self.configure(width=470, height=550, bg="#F8EDE3")
        self.iconbitmap(r'icon.ico')

        # Load the customized button images
        self.loginButton = ImageTk.PhotoImage(file="login.png")
        self.registerButton = ImageTk.PhotoImage(file="register.png")
        self.backButton = ImageTk.PhotoImage(file="back.png")


        # Create a container frame to hold the pages
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")  # Use grid for the container

        # Create and add pages to the pages dictionary
        self.pages = {}
        self.add_page(LoginPage, "login")
        self.add_page(RegistrationPage, "registration")
        self.add_page(MainApplicationPage, "main")

        # Show the initial login page
        self.show_page("login")

    def add_page(self, page_class, page_name):
        page = page_class(self.container, self)
        self.pages[page_name] = page
        page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F8EDE3")  # Set the background color for the frame
        self.controller = controller  # Store the reference to the controller

        # Create a frame to center-align the login elements vertically
        center_frame = tk.Frame(self, bg="#F8EDE3")
        center_frame.pack(expand=True, fill="both", pady=200, padx=100)  # Adjust the pady value as needed

        # Add widgets for the login page here
        label_email = tk.Label(center_frame, text="Email:", bg="#F8EDE3")
        label_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        entry_email = tk.Entry(center_frame)
        entry_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        label_password = tk.Label(center_frame, text="Password:", bg="#F8EDE3")
        label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        entry_password = tk.Entry(center_frame, show="*")
        entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        login_button = tk.Button(center_frame, image=controller.loginButton, command=self._on_login_pressed, bg="#B9FFF8", relief=tk.FLAT)
        login_button.grid(row=2, column=1, pady=10)

        register_button = tk.Button(center_frame, image=controller.registerButton, command=lambda: self.controller.show_page("registration"), relief=tk.FLAT)
        register_button.grid(row=3, column=1)

        # Center-align the login elements horizontally within center_frame
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)

    def _on_login_pressed(self):
        # Get user input from widgets
        email = entry_email.get()
        password = entry_password.get()

        user = login_user_wrapper(email, password)

        if user:
            # Login successful, you can add code to handle the successful login
            print("Login successful!")
        else:
            # Login failed, you can display an error message or take appropriate action
            print("Login failed!")

class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create instance variables to hold the entry widgets
        self.entry_email = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_first_name = tk.Entry(self)
        self.entry_last_name = tk.Entry(self)

        # Create a frame to center-align the registration elements vertically
        center_frame = tk.Frame(self, bg="#F8EDE3")
        center_frame.pack(expand=True, fill="both", pady=200, padx=100)  # Adjust the pady value as needed

        # Add widgets for the registration page here
        label_email = tk.Label(center_frame, text="Email:", bg="#F8EDE3")
        label_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        entry_email = tk.Entry(center_frame)
        entry_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        label_password = tk.Label(center_frame, text="Password:", bg="#F8EDE3")
        label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        entry_password = tk.Entry(center_frame, show="*")
        entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        label_first_name = tk.Label(center_frame, text="First Name:", bg="#F8EDE3")
        label_first_name.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        entry_first_name = tk.Entry(center_frame)
        entry_first_name.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        label_last_name = tk.Label(center_frame, text="Last Name:", bg="#F8EDE3")
        label_last_name.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        entry_last_name = tk.Entry(center_frame)
        entry_last_name.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        register_button = tk.Button(center_frame, image=controller.registerButton, command=self._on_register_pressed, bg="#B9FFF8", relief=tk.FLAT)
        register_button.grid(row=4, columnspan=2, pady=10)

        back_button = tk.Button(center_frame, image=controller.backButton, command=self.back_to_login, bg="#B9FFF8", relief=tk.FLAT)
        back_button.grid(row=5, columnspan=2)

        # Center-align the registration elements horizontally within center_frame
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_rowconfigure(3, weight=1)
        center_frame.grid_rowconfigure(4, weight=1)
        center_frame.grid_rowconfigure(5, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)


    def _on_register_pressed(self):
        # Get user input from widgets
        self.email = self.entry_email.get()
        password = self.entry_password.get()
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()

        # Print the values for debugging
        print("email:", self.email)
        print("password:", password)
        print("first_name:", first_name)
        print("last_name:", last_name)

        conn = sqlite3.connect('aichatbot.db')
        cursor = conn.cursor()
        # Insert user data into the users table
        try:
            cursor.execute('''
                INSERT INTO users (email, password, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (self.email, password, first_name, last_name))
            conn.commit()
            messagebox.showinfo("Information", "User Registered Successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error registering user: " + str(e))
        finally:
            conn.close()

    def back_to_login(self):
        # Switch back to the login page
        self.controller.show_page("login")

class MainApplicationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Add widgets for the main application page here

if __name__ == "__main__":
    app = PageManager()
    app.mainloop()
