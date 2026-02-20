import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

backgroundColor = "#2c0a0a"
buttonColor = "#570202"

# Sent the valid pin to create back to the menu
def createPasswdWindow():
        global passwd
        passwd = ""
        root = tk.Tk()

        root.tk.call('tk', 'scaling', 1.5) # Set the scaling factor to 1.5 for better visibility on high-DPI displays
        root.title("Password Manager - Create Pin") # Set the window title to "Password Manager - Create Pin"
        root.geometry("400x400") # Set the window size to 1200x900 pixels
        root.configure(bg=backgroundColor) # Set the background color to a dark shade of red
        root.resizable(False, False) # Disable window resizing

        frame = tk.Frame(root, bg=backgroundColor) # Create a frame to hold the login widgets, with the same background color
        frame.pack(expand=True) # Pack the frame to fill the available space and center it

        def capEntry(newValue):
                if len(newValue) > 10: # Check if the new value exceeds the maximum length of 20 characters
                        return False # If it does, reject the input by returning False
                return True # Otherwise, accept the input by returning True
        validateCommand = root.register(capEntry)
        
        createPasswdLabel = tk.Label(frame, text="Create a new password", bg=backgroundColor, fg="white", font=("Arial", 18))
        createPasswdLabel.pack(pady=10)

        createPasswdEntry = tk.Entry(frame, show="*", font=("Arial", 18), validate="key", validatecommand=(validateCommand, "%P"),bg="#1a0b0b", fg="white", insertbackground="white")
        createPasswdEntry.pack(pady=10)

        createPasswdLabel2 = tk.Label(frame, text="Enter the same password", bg=backgroundColor, fg="white", font=("Arial", 18))
        createPasswdLabel2.pack(pady=10)

        createPasswdEntry2 = tk.Entry(frame, show="*", font=("Arial", 18), validate="key", validatecommand=(validateCommand, "%P"),bg="#1a0b0b", fg="white", insertbackground="white")
        createPasswdEntry2.pack(pady=10)

        def submitPassword(password, password2, root):
                if password != password2:
                        messagebox.showerror("Error", "Passwords do not match. Please try again.")
                        return
                elif len(password) == 0:
                        messagebox.showerror("Error", "Password cannot be empty. Please try again.")
                        return
                elif password.find('"') != -1:
                        messagebox.showerror("Error", "Invalid character \" . Please try again.")
                        return
                else:
                        global passwd
                        passwd = password
                        root.destroy()

         # Run the submitPassword function when the user presses the Enter key while the password entry field is focused
        def on_enter_key(event):
                submitPassword(createPasswdEntry.get(), createPasswdEntry2.get(), root)

        createPasswdEntry.bind('<Return>', on_enter_key)
        createPasswdEntry2.bind('<Return>', on_enter_key)

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

        enterButton = ttk.Button(frame, text="Enter", style="Custom.TButton", command=lambda: submitPassword(createPasswdEntry.get(), createPasswdEntry2.get(), root))
        enterButton.pack(pady=20)

        root.mainloop()
        return passwd