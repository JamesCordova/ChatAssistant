import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from . import settings as cf

class MessageFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            height=0
        )

        self.columnconfigure((0,1,2), weight = 1)
        rows = tuple(range(16))
        self.rowconfigure(rows, weight = 1)
        self.max_rows = 10
        self.messages = []
        self.current_row = 0

        pass

    def add_message(self, widget):
        # if len(self.messages) > self.max_rows:
        #     self.messages.pop(0)
        #     return widget
        self.messages.append(widget)
        self.current_row += 1
        self._scrollbar.set(start_value=0.9, end_value=1)
        if type(widget) is UserMessage:
            self.event_generate("<<UserQuery>>")
        print()
        return widget

class AssistMessage(ctk.CTkFrame):
    def __init__(self, parent, root, images = [], text = "", is_menu = False):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.current_images = []
        self.string_message = ""
        self.is_menu = is_menu
        print(text)
        if self.is_menu:
            for i, option in enumerate(text, start = 1):
                self.string_message += f"{str(i)}) {option.capitalize()}\n"
        elif type(text) is list:
            for sentence in text:
                self.string_message += f"{sentence} "
        else:
            self.string_message = text

            
        ctk.CTkLabel(self, text = self.string_message, corner_radius=15, fg_color=("#dcdcdc", "#2b2b2b"), wraplength=300, justify="left").pack(anchor="w", pady=5, ipadx=5, ipady=10)

        if images:
            self.image_message = ImageFrame(
                parent = self,
                root = root,
                images = images
            )
            self.image_message.pack(anchor="nw", pady=5, expand=True, fill="both")

class UserMessage(ctk.CTkFrame):
    def __init__(self, parent, text = ""):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.message = ctk.CTkLabel(self, corner_radius=15, text = text, fg_color=(cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK))
        self.message.pack(anchor="e", pady=5)
        pass


class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, root, images = []):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.root = root

        # images
        self.image_paths = list(map(lambda filename_image: cf.IMAGES_PATH + "/" + str(filename_image), images))
        self.current_index = 0

        self.current_image = Image.open(self.image_paths[self.current_index])
        self.current_ctk_image = ctk.CTkImage(light_image=self.current_image)
        self.image_label = ctk.CTkLabel(master = root,text="image",corner_radius = 15,fg_color=("#dcdcdc", "#2b2b2b"))
        self.image_label = ctk.CTkLabel(
                master = self,
                text="image",
                corner_radius = 15,
                fg_color=("#dcdcdc", "#2b2b2b")
        )
        self.image_label.pack(side="top")
        self.show_current_image()

        # buttons
        self.prev_button = ctk.CTkButton(
            master = self, 
            text = "<",
            text_color = cf.MESSAGE_COLOR_LIGHT,
            corner_radius = 15,
            fg_color = ("#dcdcdc", "#2b2b2b"),
            command = self.show_prev_image
        )
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = ctk.CTkButton(
            master = self,
            text = ">",
            text_color = cf.MESSAGE_COLOR_LIGHT,
            command = self.show_next_image
        )
        self.next_button.pack(side=tk.RIGHT)

        self.image_label.bind("<Button-1>", self.open_current_image_system)
        

    def show_current_image(self):
        current_image = Image.open(self.image_paths[self.current_index])
        current_ctk_image = self.resize_ctk_image(current_image)
        self.image_label.configure(
            image = current_ctk_image
        )

    def resize_ctk_image(self, open_image):
        real_w, real_h = open_image.size
        window_height = self.root.winfo_height()
        print(window_height)
        image_height = window_height * 0.4
        image_width = real_w * (image_height / real_h)
        current_ctk_image = ctk.CTkImage(
            light_image = open_image,
            size = (image_width, image_height)
        )
        return current_ctk_image
    
    def show_prev_image(self):
        # Decrement the index
        self.current_index = (self.current_index - 1) % len(self.image_paths)

        # Show the previous image
        self.show_current_image()
    
    def show_next_image(self):
        # Increment the index
        self.current_index = (self.current_index + 1) % len(self.image_paths)

        # Show the next image
        self.show_current_image()
    
    def open_current_image_system(self, event):
        self.current_image.show()



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
        self.micro_image = ctk.CTkImage(light_image = Image.open(cf.MICROPHONE_IMAGE))
        self.keyboard_image = ctk.CTkImage(light_image = Image.open(cf.KEYBOARD_IMAGE))
        self.voice_button = ctk.CTkButton(
            master = self,
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            image = self.micro_image,
            corner_radius = 999,
            command = self.active_micro
        )
        self.keyboard_button = ctk.CTkButton(
            master = self,
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            image = self.keyboard_image,
            corner_radius = 999,
            command = self.active_keyboard
        )
        self.text_input = ctk.CTkEntry(
            master = self,
            corner_radius = 20,
            placeholder_text = "Escribe tu petición",
            fg_color = "transparent"
        )
        self.text_input.bind("<Return>", self.send_text_query)
        self.query = None
        self.micro_mode = True

        self.grid_buttons()

    def active_micro(self):
        if self.micro_mode:
            self.query = "start"
            self._canvas.event_generate("<<DoneQuery>>")
            
            # user_message = UserMessage(self.parent.message_window, text="Yes, help me with this")
            # user_message.grid(row=self.parent.message_window.current_row+1, column=1, columnspan=2, sticky="e")
            # self.parent.message_window.add_message(user_message)
            pass
        self.keyboard_button.grid_forget()
        self.text_input.grid_forget()
        self.grid_buttons()
        self.micro_mode = True

    def send_audio_query(self):

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
    
    def send_text_query(self, event):
        self.query = self.text_input.get()
        self.text_input.delete(0,tk.END)
        self._canvas.event_generate("<<DoneQuery>>")
    
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