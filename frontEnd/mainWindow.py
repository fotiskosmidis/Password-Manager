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