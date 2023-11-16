import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image

class MessageFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(
            fg_color = "transparent",
            height=0
        )

        self.columnconfigure((0,1,2), weight = 1)
        rows = tuple(range(40))
        self.rowconfigure(rows, weight = 1)
        for y in range(0, 40, 3):
            assist_frame = ctk.CTkFrame(self, fg_color="transparent")
            ctk.CTkLabel(assist_frame, text="Hello, may be i can help you", corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).pack(anchor="w")
            assist_frame.grid(row=y, column=0, columnspan=2, rowspan= 2, sticky="w")

            image_message = ImageFrame(assist_frame, parent)
            
            user_frame = ctk.CTkFrame(self)
            
            ctk.CTkLabel(user_frame, text="Yes, help me with this", corner_radius=15, fg_color=("#b4b4b4", "#3c3c3c")).pack()
            user_frame.grid(row=y+2, column=1, columnspan=2, sticky="e")


        # for x in range(20):
        #     ctk.CTkLabel(self, text="Hello, may be i can help you", corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).pack(side="left", pady=10)
        #     ctk.CTkLabel(self, text="Yes, help me with this", corner_radius=15, fg_color=("#b4b4b4", "#3c3c3c")).pack(side="right", pady=10)

        pass

class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, root):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(anchor="w", pady=5, expand=True, fill="both")
        self.root = root

        # image 
        self.image = Image.open("imgs/raccoon.jpg")
        
        self.resize_image()

        ctk.CTkLabel(self, image=self.image_tk, text="", corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).place(relx=0, rely=0, relwidth=1, relheight=1)


    def resize_image(self):
        real_w, real_h = self.image.size
        window_height = self.root.winfo_height()
        self.image_height = window_height * 1
        self.image_width = real_w * (self.image_height/real_h)
        self.image_tk = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(self.image_width, self.image_height))


class ActionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = "transparent"
        )
        self.columnconfigure(tuple(range(5)), weight=1, uniform="a")
        self.rowconfigure(0, weight=1)
        self.voice_button = ctk.CTkButton(
            master = self,
            text = "O",
            command = self.active_micro
        )
        self.keyboard_button = ctk.CTkButton(
            master = self,
            text = "T",
            command = self.active_keyboard
        )

        self.voice_button.grid(
            row = 0,
            column = 2
        )
        self.keyboard_button.grid(
            row = 0,
            column = 4
        )

    def active_micro(self):
        pass

    def active_keyboard(self):
        pass