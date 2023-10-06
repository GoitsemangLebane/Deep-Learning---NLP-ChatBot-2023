from tkinter import *
import tkinter as tk
from Chat import get_response, bot_name, speak
from user_authentication import register_user, login_user
from user_authentication import register_user_wrapper, login_user_wrapper
from tkinter import Entry, Button, Toplevel, Label
import time

entry_email = None
entry_password = None
entry_first_name = None
entry_last_name = None

# Create a function to open the login dialog
def open_login_dialog():
    login_dialog = Toplevel(root)
    login_dialog.title("Login")
    global entry_email, entry_password, entry_first_name, entry_last_name

    label_email = Label(login_dialog, text="Email:")
    label_email.pack()

    entry_email = Entry(login_dialog)
    entry_email.pack()

    label_password = Label(login_dialog, text="Password:")
    label_password.pack()

    entry_password = Entry(login_dialog, show="*")
    entry_password.pack()

    login_button = Button(login_dialog, text="Login", command=lambda: _on_login_pressed(entry_email, entry_password))
    login_button.pack()

    register_button = Button(login_dialog, text="Register", command=open_registration_dialog)
    register_button.pack()


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202a"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 12"
FONT_BOLD = "Helvetica 12 bold"

root = tk.Tk()
root.title("HelpR")
root.geometry("470x550+320+100")
root.resizable(width=False, height=False)
root.configure(width=470, height=550, bg="#F8EDE3")
root.iconbitmap(r'icon.ico')

button1 = PhotoImage(file="send_button.png")

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# HEAD LABEL
def open_calendar(event):
    #  actual link to the external calendar
    calendar_link = 'https://www.officeholidays.com/calendars/planners/botswana/2023'
    webbrowser.open(calendar_link)

head_label = Label(root, bg='#967E76', fg='white', text='Dumela!', font="Helvetica 12 bold", pady=10)
head_label.place(relwidth=1)

# Load a calendar icon image and create a label with the image
calendar_icon = PhotoImage(file='calendar_icon.png')  # Replace with the actual path to your icon image
calendar_label = tk.Label(root, image=calendar_icon, cursor="hand2")
calendar_label.place(relx=0.9, relwidth=0.1)  # Adjust position and size as needed

# Make the label clickable by binding it to the open_calendar function
calendar_label.bind("<Button-1>", open_calendar)

# Create a Tooltip instance for the calendar label
tooltip_text = "Click to View Khoi San community Events..."
tooltip = Tooltip(calendar_label, tooltip_text)

# tiny divider
line = Label(root, width=450, bg='#B9FFF8')
line.place(relwidth=1, rely=0.07, relheight=0.020)

#uhuh/////////////////////////////////////////////////////////////////////
# Function to handle user login
def _on_login_pressed(email_entry, password_entry):
    # Get user input from entry fields
    email = email_entry.get()
    password = password_entry.get()

    # Call the login function from user_authentication.py
    user = login_user_wrapper(email, password)

    if user:
        # Login successful
        print("Login successful!")
        login_dialog.destroy()  # Close the login dialog
        # You can add code here to enable the main chatbot interface

    else:
        # Login failed
        print("Login failed!")

# Function to open the registration dialog
def open_registration_dialog():
    registration_dialog = Toplevel(root)
    registration_dialog.title("Register")
    global entry_email, entry_password, entry_first_name, entry_last_name


    label_email = Label(registration_dialog, text="Email:")
    label_email.pack()

    entry_email = Entry(registration_dialog)
    entry_email.pack()

    label_password = Label(registration_dialog, text="Password:")
    label_password.pack()

    entry_password = Entry(registration_dialog, show="*")
    entry_password.pack()

    label_first_name = Label(registration_dialog, text="First Name:")
    label_first_name.pack()

    entry_first_name = Entry(registration_dialog)
    entry_first_name.pack()

    label_last_name = Label(registration_dialog, text="Last Name:")
    label_last_name.pack()

    entry_last_name = Entry(registration_dialog)
    entry_last_name.pack()

    register_button = Button(registration_dialog, text="Register", command=lambda: _on_register_pressed(entry_email, entry_password, entry_first_name, entry_last_name))
    register_button.pack()

    back_button = Button(registration_dialog, text="Back to Login", command=registration_dialog.destroy)
    back_button.pack()

# Add a button in your main tkinter window to open the login dialog
login_button = Button(root, text="Login", command=open_login_dialog)
login_button.place(relx=0.85, rely=0.012)
# LOGIN PART END /////////////////////////////////////////////////////////////////////////////////////////////////

# text widget for chatbot reply
text_widget = Text(root, width=20, height=2, bg='#EEEEEE', fg='black', font=FONT, padx=15, pady=10)
text_widget.place(relheight=0.745, relwidth=1, rely=0.08) #rely to move the chat downward(height)
text_widget.configure(cursor="arrow", state=DISABLED)

# scrollbar
scrollbar = Scrollbar(text_widget)
scrollbar.place(relheight=1, relx=0.974)
scrollbar.configure(command=text_widget.yview)
text_widget.configure(yscrollcommand=scrollbar.set)

# bottom label
bottom_label = Label(root, bg=BG_GRAY, height=80)
bottom_label.place(relwidth=1, rely=0.825)

# send button
send_button = Button(bottom_label, image=button1, bg=BG_GRAY, command=lambda: _on_enter_pressed(None), relief=FLAT)
send_button.place(relx=0.76, rely=0.012)


def _on_enter_pressed(event):
    message = message_entry.get()
    _insert_message(message, "You")
    message_entry.delete(0, END)  # Clear the message entry field

def _type_message(message, sender, background_color, text_color, font_style, font_size, font_family, delay_between_chars=0.05):
    # Insert the message with the specified background color and text color
    formatted_message = f"{sender}: {message}\n\n"
    text_widget.configure(state=NORMAL)
    text_widget.tag_configure("custom", background=background_color, foreground=text_color, font=(font_family, font_size, font_style))

    for char in formatted_message:
        text_widget.insert(END, char, "custom")
        text_widget.see(END)
        text_widget.update_idletasks()  # Force update of the widget
        time.sleep(delay_between_chars)

    text_widget.configure(state=DISABLED)

def _insert_message(message, sender):
    if not message:
        return

    # Insert the user's message on the left side with a light grey background
    message1 = f"{sender}: {message}\n\n"
    text_widget.configure(state=NORMAL)
    text_widget.tag_configure("left", background="#EAECEE")
    text_widget.insert(END, message1, "left")
    text_widget.configure(state=DISABLED)
    #_type_message(message, sender)

    # Get and store the bot's response
    response = get_response(message)

    # Insert the bot's response on the right side with a grey background
    _type_message(response, bot_name, background_color="#2e2e2e", text_color="white", font_style="italic", font_size=11, font_family="Arial")

    # Speak the bot's response using the pyttsx3 engine
    #speak(response)

# message entry for text input
message_entry = Entry(bottom_label, bg="#B9FFF8", fg='#472D2D', font=FONT)
message_entry.place(relwidth=0.724, relheight=0.04, rely=0.008, relx=0.011)
message_entry.focus()
message_entry.bind("<Return>", _on_enter_pressed)

# Function to handle user registration
# Function to handle user registration
# Function to handle user registration
def _on_register_pressed(email_entry, password_entry, first_name_entry, last_name_entry):
    # Get user input from entry fields
    email = email_entry.get()
    password = password_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    # Call the registration function from user_authentication.py
    result = register_user_wrapper(email, password, first_name, last_name)

    if result:
        # Registration successful
        print("Registration successful!")
        registration_dialog.destroy()  # Close the registration dialog
        # You can add code here to enable the main chatbot interface
    else:
        # Registration failed
        print("Registration failed! Check your database configuration or try a different email address.")

root.mainloop()
