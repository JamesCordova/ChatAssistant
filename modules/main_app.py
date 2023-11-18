import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from . import main_window
from . import settings as cf

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main App")
        self.color_ui = (cf.BG_COLOR_DARK, cf.BG_COLOR_LIGHT)
        self.geometry("600x500")
        self.minsize(600,500)
        self.configure(
            background = self.color_ui
        )
        # ctk.set_appearance_mode("light")
        self.message_window = main_window.MessageFrame(self)
        self.message_window.place(relx=0, rely=0, relheight=0.9, relwidth=1)
        # self.response_frame = ctk.CTkFrame(self)
        # self.response_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

        self.action_window = main_window.ActionFrame(self)
        self.action_window.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)


        self.mainloop()

App()