import sys
import os
# Add project root to sys.path to allow importing bindings
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bindings  # type: ignore
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

backgroundColor = "#2c0a0a"
buttonColor = "#570202"
addWindowInstance = None

def addWindow(accounts, updatePanelCallback):
        global addWindowInstance
        # Look if there is any other add window open, if there is, lift it and return
        if addWindowInstance is not None and tk.Toplevel.winfo_exists(addWindowInstance):
                addWindowInstance.deiconify() # Restore the window if it was minimized
                addWindowInstance.lift()  # Bring to front
                addWindowInstance.focus_force()  # Focus the window
                return

        root = tk.Toplevel()
        addWindowInstance = root
        root.title("Add Account")
        root.geometry("400x425")
        root.configure(bg=backgroundColor)
        root.resizable(False, False)

        # Create labels and entry fields for account details
        tk.Label(root, text="Company:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        companyEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        companyEntry.pack(pady=5)

        tk.Label(root, text="Email:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        emailEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        emailEntry.pack(pady=5)

        tk.Label(root, text="Username:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        usernameEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        usernameEntry.pack(pady=5)

        tk.Label(root, text="Password:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        passwordEntry = tk.Entry(root, width=20, show="*", bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        passwordEntry.pack(pady=5)

        # Create frame for the buttons
        buttonFrame = tk.Frame(root, bg=backgroundColor)
        buttonFrame.pack(pady=20)

        # Create add button
        def onAdd():
                if addAccount(companyEntry.get(), emailEntry.get(), usernameEntry.get(), passwordEntry.get(), accounts):
                        updatePanelCallback()
                        root.destroy()
        addButton = tk.Button(buttonFrame, text="Add", bg=buttonColor, fg="white", font=("Arial", 16), cursor="hand2", command=onAdd)
        addButton.pack(side=tk.LEFT, padx=10)

        # Create cancel button
        cancelButton = tk.Button(buttonFrame, text="Cancel", bg=buttonColor, fg="white", font=("Arial", 16), cursor="hand2", command=root.destroy)
        cancelButton.pack(side=tk.LEFT, padx=10)

        # Set the addWindowInstance to None when the window is closed
        def onClose():
                global addWindowInstance
                addWindowInstance = None
                root.destroy()
        root.protocol("WM_DELETE_WINDOW", onClose)



def addAccount(company, email, username, password, accounts):
        if company == "" or email == "" or password == "":
                messagebox.showerror("Error", "Please fill in all fields")
                return False
        
        # Verify the account
        if (username != ""):
                acc = bindings.Account(company, email, password, username)
        else:
                acc = bindings.Account(company, email, password)
        
        code = bindings.verifyAccount(acc, accounts)
        if code == 0:
                accounts.append(acc)
                return True
        elif code == 1:
                messagebox.showerror("Error", "Account with the same company and email already exists")
                return False
        elif code == 2:
                messagebox.showerror("Error", "Invalid email format")
                return False
        elif code == 3:
                messagebox.showerror("Error", "Invalid password format")
                return False
        elif code == 4:
                messagebox.showerror("Error", "Invalid company format")
                return False
        elif code == 5 and username != "":
                messagebox.showerror("Error", "Invalid username format")
                return False