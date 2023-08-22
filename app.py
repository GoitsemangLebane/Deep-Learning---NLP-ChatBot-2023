from tkinter import *
import tkinter as tk
from Chat import get_response, bot_name, speak
import webbrowser

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
    calendar_link = 'your_calendar_link_here'
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

# text widget
text_widget = Text(root, width=20, height=2, bg='#EEEEEE', fg='black', font=FONT, padx=15, pady=10)
text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
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

def _insert_message(message, sender):
    if not message:
        return

    # Insert the user's message on the left side with a light grey background
    message1 = f"{sender}: {message}\n\n"
    text_widget.configure(state=NORMAL)
    text_widget.tag_configure("left", background="#EAECEE")
    text_widget.insert(END, message1, "left")
    text_widget.configure(state=DISABLED)

    # Get and store the bot's response
    response = get_response(message)

    # Insert the bot's response on the right side with a grey background
    message2 = f"{bot_name}: {response}\n\n"
    text_widget.tag_configure("right", background="#ABB2B9")
    text_widget.configure(state=NORMAL)
    text_widget.insert(END, message2, "right")
    text_widget.configure(state=DISABLED)

    text_widget.see(END)

    # Speak the bot's response using the pyttsx3 engine
    #speak(response)


# message entry
message_entry = Entry(bottom_label, bg="#B9FFF8", fg='#472D2D', font=FONT)
message_entry.place(relwidth=0.724, relheight=0.04, rely=0.008, relx=0.011)
message_entry.focus()
message_entry.bind("<Return>", _on_enter_pressed)

root.mainloop()
