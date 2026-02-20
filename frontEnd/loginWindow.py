import sys
import os
# Add project root to sys.path to allow importing bindings
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bindings  # type: ignore
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from frontEnd.mainWindow import mainWindow

backgroundColor = "#2c0a0a"
buttonColor = "#570202"

def loginWindow():
       
        root = tk.Tk()

        root.tk.call('tk', 'scaling', 1.5) # Set the scaling factor to 1.5 for better visibility on high-DPI displays
        root.title("Password Manager - Login") # Set the window title to "Password Manager - Login"
        root.geometry("400x250") # Set the window size to 1200x900 pixels
        root.configure(bg=backgroundColor) # Set the background color to a dark shade of red
        root.resizable(False, False) # Disable window resizing

        frame = tk.Frame(root, bg=backgroundColor) # Create a frame to hold the login widgets, with the same background color
        frame.pack(expand=True) # Pack the frame to fill the available space and center it

        passwordLabel = tk.Label(frame, text="Enter password", bg=backgroundColor, fg="white", font=("Arial", 18)) # Create a label for the password entry field
        passwordLabel.pack(pady=10) # Add some vertical padding around the label

        def capEntry(newValue):
                if len(newValue) > 10: # Check if the new value exceeds the maximum length of 20 characters
                        return False # If it does, reject the input by returning False
                return True # Otherwise, accept the input by returning True
        validateCommand = root.register(capEntry)

        passwordEntry = tk.Entry(frame, show="*", font=("Arial", 18), validate="key", validatecommand=(validateCommand, "%P"),bg="#1a0b0b", fg="white", insertbackground="white") # Create an entry widget for the password input, with the characters hidden and validation enabled
        passwordEntry.pack(pady=10) # Add some vertical padding around the entry widget

        def submitPassword(password, root):
                if bindings.validatePin(password): # Check if the entered password matches the expected value
                        root.destroy()
                        mainWindow()
                else:
                        messagebox.showerror("Login Failed", "Incorrect password. Please try again.") # If it doesn't, show an error message

        # Run the submitPassword function when the user presses the Enter key while the password entry field is focused
        def on_enter_key(event):
                submitPassword(passwordEntry.get(), root)

        passwordEntry.bind('<Return>', on_enter_key)

        # Making the button modern by removing the border and changing the background color
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
        style.configure("Custom.TButton",
                font=("Arial", 18, "bold"),
                foreground="#fff",
                background=buttonColor,
                borderwidth=0,
                focusthickness=3,
                focuscolor='none',
                padding=10)
        style.map("Custom.TButton",
                background=[('active', "#7e480b")])

        enterButton = ttk.Button(frame, text="Enter", style="Custom.TButton", command= lambda: submitPassword(passwordEntry.get(), root)) # Create a button to submit the password, which calls the submitPassword function when clicked
        enterButton.pack(pady=10) # Add some vertical padding around the button

        root.mainloop()