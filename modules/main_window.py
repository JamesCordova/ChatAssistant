import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class MessageFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(
            fg_color = "transparent"
        )
        # print(self._scrollbar)

        ctk.CTkLabel(self, text="Hello").pack(side="top", expand=True, fill="both")
        pass