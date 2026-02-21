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

def displayWindow(accounts, account, updatePanelCallback):
        root = tk.Toplevel()
        root.geometry("400x425")
        root.configure(bg=backgroundColor)
        root.resizable(False, False)
        root.title(f"{account.getCompany()} - {account.getEmail()}")

        # Create a main frame to hold everything
        mainFrame = tk.Frame(root, bg=backgroundColor)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        # Create entries to display the account information
        tk.Label(root, text="Company:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        companyEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        companyEntry.pack(pady=5)
        companyEntry.insert(0, account.getCompany())

        tk.Label(root, text="Email:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        emailEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        emailEntry.pack(pady=5)
        emailEntry.insert(0, account.getEmail())

        tk.Label(root, text="Username:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        usernameEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        usernameEntry.pack(pady=5)
        usernameEntry.insert(0, account.getName())

        tk.Label(root, text="Password:", bg=backgroundColor, fg="white", font=("Arial", 16)).pack(pady=5)
        passwordEntry = tk.Entry(root, width=20, bg="#1a0b0b", fg="white", insertbackground="white", font=("Arial", 16))
        passwordEntry.pack(pady=5)
        passwordEntry.insert(0, account.getPassword())

        # Create a frame for the buttons
        buttonFrame = tk.Frame(root, bg=backgroundColor)
        buttonFrame.pack(pady=20)

        # Create save button
        def onSave():
                if saveAccount(accounts, account, companyEntry.get(), emailEntry.get(), usernameEntry.get(), passwordEntry.get()):
                        updatePanelCallback()
                        root.destroy()
        saveButton = tk.Button(buttonFrame, text="Save", bg=buttonColor, fg="white", font=("Arial", 16), cursor="hand2", command=onSave)
        saveButton.pack(side=tk.LEFT, padx=5)

        # Create delete button
        def onDelete():
                if deleteAccount(accounts, account):
                        updatePanelCallback()
                        root.destroy()
        deleteButton = tk.Button(buttonFrame, text="Delete", bg=buttonColor, fg="white", font=("Arial", 16), cursor="hand2", command=onDelete)
        deleteButton.pack(side=tk.LEFT, padx=5)

        # Create cancel button
        cancelButton = tk.Button(buttonFrame, text="Cancel", bg=buttonColor, fg="white", font=("Arial", 16), cursor="hand2", command=root.destroy)
        cancelButton.pack(side=tk.LEFT, padx=5)



def saveAccount(accounts,account, company, email, username, password):
        if company == "" or email == "" or password == "":
                messagebox.showerror("Error", "Please fill in all fields")
                return False

        # Make a temp account to sent to the verify function
        if (username != ""):
                acc = bindings.Account(company, email, password, username)
        else:
                acc = bindings.Account(company, email, password)


        code = bindings.verifyAccount(acc, accounts)

        # if there is already in the list on another account and not the same account, show error, otherwise save the account
        # SPECIAL CASE if the email and company are not the same as before and we change to something that is already in the list,
        # the verify will return 1 but we wanna show error
        if(company != account.getCompany() and email != account.getEmail() and code == 1):
                messagebox.showerror("Error", "An account with this email and company already exists")
                return False


        if code == 0 or code == 1:
                account.setCompany(company)
                account.setEmail(email)
                account.setName(username)
                account.setPassword(password)
                return True
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

        return True

def deleteAccount(accounts, account):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this account?"):
                accounts.remove(account)
                return True
        return False