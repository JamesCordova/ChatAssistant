import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from . import settings as cf

class MessageFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_hover_color = ("#b4b4b4", "#3c3c3c"),
            height=0
        )

        self.columnconfigure((0,1,2), weight = 1)
        rows = tuple(range(16))
        self.rowconfigure(rows, weight = 1)
        self.max_rows = 10
        self.messages = []
        self.current_row = 0
        while self.current_row < 14:
            assist_message = AssistMessage(self, root = parent, image=True, text="Hello, may be i can help you")
            assist_message.grid(row=self.current_row, column=0, columnspan=2, sticky="ew")
            self.add_message(assist_message)
            print("assist" + str(self.current_row))
            
            user_message = UserMessage(self, text="Yes, help me with this")
            user_message.grid(row=self.current_row, column=1, columnspan=2, sticky="e")
            self.add_message(user_message)
            print("user" + str(self.current_row))

        pass

    def add_message(self, widget):
        # if len(self.messages) > self.max_rows:
        #     self.messages.pop(0)
        #     return widget
        self.messages.append(widget)
        self.current_row += 1
        self._scrollbar.set(start_value=1, end_value=1)
        print()
        return widget

class AssistMessage(ctk.CTkFrame):
    def __init__(self, parent, root, image = None, text = ""):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        ctk.CTkLabel(self, text = text, corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).pack(anchor="w")

        self.image_message = image
        if self.image_message:
            self.image_message = ImageFrame(
                parent = self,
                root = root
            )
            self.image_message.pack(anchor="nw", pady=5, expand=True, fill="both")
            self.image_message.resize_image()

class UserMessage(ctk.CTkFrame):
    def __init__(self, parent, text = ""):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.message = ctk.CTkLabel(self, corner_radius=15, text = text, fg_color=("#b4b4b4", "#3c3c3c"))
        self.message.pack(anchor="e")
        pass


class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, root):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.root = root

        # image 
        self.image = Image.open("imgs/raccoon.jpg")
        
        self.resize_image()

        ctk.CTkLabel(self, image=self.image_tk, text="", corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b")).place(relx=0, rely=0, relwidth=1, relheight=1)


    def resize_image(self):
        real_w, real_h = self.image.size
        window_height = self.root.winfo_height()
        print(window_height)
        self.image_height = window_height * 1
        self.image_width = real_w * (self.image_height/real_h)
        self.image_tk = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(self.image_width, self.image_height))


class ActionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            master = parent,
            fg_color = "transparent"
        )
        self.parent = parent
        self.columnconfigure((0, 2, 4), weight=1, uniform="a")
        self.columnconfigure((1, 3), weight=3, uniform="a")
        self.rowconfigure(0, weight=1)
        self.voice_button = ctk.CTkButton(
            master = self,
            text = "O",
            corner_radius = 999,
            command = self.active_micro
        )
        self.keyboard_button = ctk.CTkButton(
            master = self,
            text = "T",
            corner_radius = 999,
            command = self.active_keyboard
        )
        self.text_input = ctk.CTkEntry(
            master = self,
            corner_radius = 20,
            placeholder_text = "Escribe tu petición",
            fg_color = "transparent"
        )
        self.text_input.bind("<Return>", lambda: print())
        self.micro_mode = True

        self.grid_buttons()

    def active_micro(self):
        if self.micro_mode:
            print(self.micro_mode)
            assist_message = AssistMessage(self.parent.message_window, root = self.parent, image=True, text="Hello, may be i can help you")
            assist_message.grid(row=self.parent.message_window.current_row, column=0, columnspan=2, sticky="ew")
            self.parent.message_window.add_message(assist_message)
            self.parent.message_window._scrollbar.set(start_value=0.9, end_value=1)
            
            # user_message = UserMessage(self.parent.message_window, text="Yes, help me with this")
            # user_message.grid(row=self.parent.message_window.current_row+1, column=1, columnspan=2, sticky="e")
            # self.parent.message_window.add_message(user_message)
            pass
        self.keyboard_button.grid_forget()
        self.text_input.grid_forget()
        self.grid_buttons()
        self.micro_mode = True
        pass

    def active_keyboard(self):
        self.keyboard_button.grid_forget()
        self.voice_button.grid_forget()
        self.voice_button.grid(
            row = 0,
            column = 4,
            padx = 10,
            pady = 10,
            sticky = "nsew"            
        )
        self.voice_button.grid_info()
        self.grid_text()
        self.micro_mode = False
        pass
    
    def grid_buttons(self):
        self.voice_button.grid(
            row = 0,
            column = 2,
            padx = 10,
            pady = 10,
            sticky = "nsew"            
        )
        self.keyboard_button.grid(
            row = 0,
            column = 4,
            padx = 10,
            pady = 10,
            sticky = "nsew"            
        )
    
    def grid_text(self):
        self.text_input.grid(
            row = 0,
            column = 0,
            columnspan = 4,
            padx = 10,
            pady = 10,
            sticky = "nsew"
        )