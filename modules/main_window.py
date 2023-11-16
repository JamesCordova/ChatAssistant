import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class MessageFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(
            fg_color = "transparent",
            height=0
        )

        self.columnconfigure((0,1,2,3), weight = 1)
        rows = tuple(range(40))
        self.rowconfigure(rows, weight = 1)
        for y in range(0, 40, 2):
            ctk.CTkLabel(self, text="Hello, may be i can help you", corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).grid(row=y, column=0, columnspan=2, sticky="w")
            ctk.CTkLabel(self, text="Yes, help me with this", corner_radius=15, fg_color=("#b4b4b4", "#3c3c3c")).grid(row=y+1, column=2, columnspan=2, sticky="e")

        # for x in range(20):
        #     ctk.CTkLabel(self, text="Hello, may be i can help you", corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).pack(side="left", pady=10)
        #     ctk.CTkLabel(self, text="Yes, help me with this", corner_radius=15, fg_color=("#b4b4b4", "#3c3c3c")).pack(side="right", pady=10)

        pass