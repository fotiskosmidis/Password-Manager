import sys
import os
# Add project root to sys.path to allow importing bindings
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bindings  # type: ignore
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import frontEnd.addWindow as addWindow

mainFrameColor = "#15011a"
backgroundColor = "#2c0a0a"
buttonColor = "#570202"

def mainWindow():
        root = tk.Tk()
        
        key = bindings.getKey()
        accounts = bindings.loadAccounts(key)

        dpi = root.winfo_fpixels('1i') # Get the screen's DPI (dots per inch) of the screen
        scaling_factor = dpi / 72 # Calculate the scaling factor based on the DPI
        root.tk.call('tk', 'scaling', scaling_factor)
        screen_width = int(root.winfo_screenwidth()*0.80) # Get the screen width and apply the scaling factor
        screen_height = int(root.winfo_screenheight()*0.80)
        root.geometry(f"{screen_width}x{screen_height}")
        root.configure(bg=backgroundColor)
        root.resizable(False, False)
        root.title("Password Manager")

        # Create a main frame to hold everything
        mainFrame = tk.Frame(root, bg=mainFrameColor)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        # Create an add account button to the left of the main frame
        addAccountButton = tk.Button(mainFrame, text="+", bg=buttonColor, fg="white", font=("Arial", 18), cursor="hand2", command=lambda: addWindow.addWindow(accounts, lambda: panelUpdate(accounts, frame)))
        addAccountButton.pack(side=tk.LEFT, anchor="nw", padx=5, pady=5) 
        addAccountButton.bind("<Button-1>", lambda e: addWindow.addWindow(accounts, lambda: panelUpdate(accounts, frame)))

        # Create a canvas to hold the account labels and a scrollbar
        canvas = tk.Canvas(mainFrame, bg=mainFrameColor)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the canvas
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' is more modern than 'default'
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background="#444",
                        darkcolor="#222",
                        lightcolor="#666",
                        troughcolor="#222",
                        bordercolor="#222",
                        arrowcolor="#fff",
                        relief="flat",
                        borderwidth=0)
        scrollbar = ttk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas to hold the account labels
        frame = tk.Frame(canvas, bg=backgroundColor)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Bind the mouse wheel to scroll the canvas
        def _on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")

        # Windows and MacOS
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        panelUpdate(accounts, frame)

        
        

        # Save accounts when the window is closed
        def onClose():
                bindings.saveAccounts(accounts, key)
                root.destroy()
        root.protocol("WM_DELETE_WINDOW", onClose)

        root.mainloop()


# This function will be used to update the account panel when changes are made to the accounts
def panelUpdate(accounts, frame):
        # Clear the current account labels
        for widget in frame.winfo_children():
                widget.destroy()

        # Make new labels
        rows = 0
        cols = -1
        for account in accounts:
                cols += 1
                if cols == 5:
                        cols = 0
                        rows += 1
                accountLabel = tk.Label(frame, text=f"{account.getCompany()}\n{account.getEmail()}", bg=buttonColor, fg="white", font=("Arial", 18),cursor="hand2",width=18, height=5) # Create a label for the account name
                accountLabel.grid(row=rows, column=cols, padx=10, pady=10) # Place the label in the grid with some padding

        frame.update_idletasks()
        canvas = frame.master  # canvas is the parent of frame
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Check if there is a need for a scrollbar and show/hide it accordingly
        if frame.winfo_height() < canvas.winfo_height():
                canvas.master.children['!scrollbar'].pack_forget()  # Hide scrollbar
        else:
                canvas.master.children['!scrollbar'].pack(side=tk.RIGHT, fill=tk.Y)  # Show scrollbar