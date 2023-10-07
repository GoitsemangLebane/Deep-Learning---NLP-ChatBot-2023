from customtkinter import *
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
import customtkinter
import subprocess
import time
import threading

popup = None
application_opened = False  # Flag to track if the application has been opened
frame2 = None

def open_main_application(username):
    global popup, application_opened
    popup = customtkinter.CTkFrame(app, bg_color='#2e2e2e', fg_color='#2e2e2e', width=300, height=80)
    popup.place(x=75, y=130)

    # Create a label for the message
    message_label = customtkinter.CTkLabel(popup, font=font3, text='Application Opening...', text_color='#fff', bg_color='#2e2e2e')
    message_label.place(x=20, y=10)

    app.update_idletasks()  # Update the GUI
    time.sleep(10)  # Simulate loading delay (you can adjust this time)

    # Open your main application here (replace with your code)
    start_chatbot(username)
    application_opened = True  # Set the flag to indicate the application has been opened
    popup.destroy()  # Close the pop-up when loading is complete

def start_chatbot(username):
    try:
        subprocess.Popen(['python', 'app.py', '--username', username])  # Replace 'app.py' with the correct path to your chatbot application file

    except Exception as e:
        messagebox.showerror('Error', f'Error starting the chatbot: {str(e)}')

#create a window
app = CTk()
app.title('Login')
app.geometry("450x360+480+200")
app.config(bg="#001220")

font1 = ('Helvetica',25,'bold')
font2 = ('Arial',17,'bold')
font3 = ('Arial',13,'bold')
font4 = ('Arial',13,'bold', 'underline')

# Database Initialization and Connection
conn = sqlite3.connect('authentication.db')
# cursor object to interact with the database
cursor = conn.cursor()
# SQL commands
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username !='' and password !='':
            cursor.execute('SELECT username FROM users WHERE username=?', [username])
            if cursor.fetchone() is not None:
                messagebox.showerror('Error', 'Username already exists!')
            else:
                encoded_password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                cursor.execute('INSERT INTO users VALUES (?,?)', [username, hashed_password])
                conn.commit()
                messagebox.showinfo('Success', 'Account Created!')
    else:
        messagebox.showerror('Error', 'Enter All Fields')

def login_account():
    global frame2
    username = username_entry2.get()
    password = password_entry2.get()
    if username !='' and password !='':
        cursor.execute('SELECT password FROM users WHERE username=?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', 'Login successful!')
                # Call the function to start the chatbot application
                #frame2.destroy()
                open_main_application(username) # open loading progress bar
            else:
                messagebox.showerror('Error', 'Invalid Credentials, Try again!')
        else:
            messagebox.showerror('Error', 'Invalid Credentials, Try again!')
    else:
        messagebox.showerror('Error', 'Enter All Data!')
'''
# Function to open the main application after login
def open_main_application():
    global popup
    popup = tk.Toplevel(app)
    popup.title("Opening Application")
    popup.geometry("300x100")

    # Create a label for the message
    message_label = tk.Label(popup, text="Application Opening...", padx=20, pady=10)
    message_label.pack()

    # Create a progress bar
    progress = ttk.Progressbar(popup, length=200, mode="indeterminate")
    progress.pack()

    # Function to simulate loading
    def simulate_loading():
        for i in range(0, 101, 10):
            progress["value"] = i
            app.update_idletasks()  # Update the GUI
            time.sleep(1)  # Simulate loading delay
        popup.destroy()  # Close the pop-up when loading is complete
        # Open your main application here (replace with your code)
        open_main_app()

    # Use a separate thread to simulate loading
    loading_thread = threading.Thread(target=simulate_loading)
    loading_thread.start()

# Function to start the chatbot application
def start_chatbot():
    try:
        subprocess.Popen(['python', 'app.py'])  # Replace 'app.py' with the correct path to your chatbot application file

    except Exception as e:
        messagebox.showerror('Error', f'Error starting the chatbot: {str(e)}')
'''

def login():
    global frame2
    frame1.destroy()
    frame2 = customtkinter.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=470, height=360)
    frame2.place(x=0, y=0)

    image2_label = Label(frame2, image=resized_image, bg='#001220')
    image2_label.place(x=0, y=85)
    

    login_label2 = customtkinter.CTkLabel(frame2, font=font1, text='Log In', text_color='#fff', bg_color='#001220')
    login_label2.place(x=280, y=20)

    global username_entry2
    global password_entry2

    username_entry2 = customtkinter.CTkEntry(frame2, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121110', border_color='#004780', border_width=1, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
    username_entry2.place(x=230, y=80)
    password_entry2 = customtkinter.CTkEntry(frame2, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121110', border_color='#004780', border_width=1, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
    password_entry2.place(x=230, y=150)

    login_button2 = customtkinter.CTkButton(frame2, command=login_account, font=font2, text_color='#fff', text='Login', fg_color='#00965d', bg_color='#121111', hover_color='#006e44', cursor='hand2', width=40)
    login_button2.place(x=230, y=220)

frame1 = customtkinter.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=470, height=360)
frame1.place(x=0, y=0)


# IMAGE RESIZING START //////////////////////////////////////////////////////////////////////////////////////////////////////
# Calculate the available width and height for the image
available_width = 150  # Adjust this value as needed based on your layout
available_height =350
# Load the original image
original_image = PhotoImage(file="HelpR_logo.png")
# Get the original image's dimensions
original_width = original_image.width()
original_height = original_image.height()
# Calculate the aspect ratio of the original image
aspect_ratio = original_width / original_height
# Calculate the new width and height for the resized image
if original_width > available_width:
    new_width = available_width
    new_height = int(new_width / aspect_ratio)
else:
    new_width = original_width
    new_height = original_height
# Resize the image to fit within the available space
resized_image = original_image.subsample(int(original_width / new_width), int(original_height / new_height))
# Create a Label for the resized image
image1_label = Label(frame1, image=resized_image, bg='#001220')
image1_label.place(x=0, y=85)
# IMAGE RESIZING END //////////////////////////////////////////////////////////////////////////////////////////////////////////

signup_label = customtkinter.CTkLabel(frame1, font=font1, text='Sign Up', text_color='#fff', bg_color='#001220')
signup_label.place(x=280, y=20)

username_entry = customtkinter.CTkEntry(frame1, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121110', border_color='#004780', border_width=1, placeholder_text='Username', placeholder_text_color='#a3a3a3', width=200, height=50)
username_entry.place(x=230, y=80)

password_entry = customtkinter.CTkEntry(frame1, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121110', border_color='#004780', border_width=1, placeholder_text='Password', placeholder_text_color='#a3a3a3', width=200, height=50)
password_entry.place(x=230, y=150)

signup_button = customtkinter.CTkButton(frame1, command=signup, font=font2, text='Sign Up', fg_color='#00965d', hover_color='#006e44', bg_color='#121110', cursor='hand2', corner_radius=5, width=200)
signup_button.place(x=230, y=220)

login_label = customtkinter.CTkLabel(frame1, font=font3, text='Already have an Account?', text_color='#fff', bg_color='#001220')
login_label.place(x=230, y=250)

login_button = customtkinter.CTkButton(frame1, command=login, font=font4, text_color='#00bf77', text='Login', fg_color='#001220', hover_color='#001220', cursor='hand2', width=40)
login_button.place(x=395, y=250)

app.mainloop()