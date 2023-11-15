import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from main_window import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main App")
        self.geometry("600x500")
        self.minsize(600,500)
        self.configure(
            background=("#1f2125", "#ffffff")
        )
        ctk.set_appearance_mode("light")
        self.message_window = MessageFrame(self)
        self.message_window.place(relx=0, rely=0, relheight=0.9, relwidth=1)
        self.response_frame = ctk.CTkFrame(self)
        self.response_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)
        
        self.mainloop()

App()