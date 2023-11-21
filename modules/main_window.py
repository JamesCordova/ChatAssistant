import tkinter as tk
import threading
import pyttsx3
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageOps
from . import settings as cf
from . import logic_assistant as assist

class MessageFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            height=0
        )
        self.root = parent
        self.columnconfigure((0,1), weight = 1, uniform = "a")
        self.columnconfigure((2), weight = 2, uniform = "a")
        rows = tuple(range(16))
        self.rowconfigure(rows, weight = 2)
        self.max_rows = 10
        self.messages = []
        self.current_message = ctk.CTkLabel(self)
        self.current_row = 0

        pass

    def add_message(self, widget):
        self.messages.append(widget)
        self.current_row += 1
        self._scrollbar.set(start_value=0.9, end_value=1)
        if type(widget) is UserMessage:
            self.event_generate("<<UserQuery>>")
        else:
            self.current_message = widget
        return widget

class AssistMessage(ctk.CTkFrame):
    def __init__(self, parent, root, images = [], text_list = [], is_menu = False):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.current_images = []
        self.responding = True
        self.text_var = tk.StringVar()
        self.sentence_list = text_list
        self.current_index = 0
        self.text_var.set("")
        self.is_menu = is_menu
            
        self.message = ctk.CTkLabel(
            master = self,
            textvariable = self.text_var,
            corner_radius = 15,
            fg_color=("#dcdcdc", "#2b2b2b"),
            wraplength = 400,
            justify="left"
        )
        self.message.pack(anchor="w", pady=5, ipadx=2, ipady=10)
        root.update()

        self.engine = pyttsx3.init()
        if images:
            self.image_message = ImageFrame(
                parent = self,
                root = root,
                images = images
            )
            self.image_message.pack(anchor="nw", pady=5, expand = True, fill = "both")
    
    def speak_sentences(self):
       self.speak_next_sentence()

    def speak_next_sentence(self):
        if not(self.sentence_list and self.current_index < len(self.sentence_list)):
            self.responding = False
            self.master.event_generate("<<AvailableInput>>")
            return
        
        current_sentence = str(self.sentence_list[self.current_index] + " ").format(username = cf.USERNAME, topic = cf.TOPIC)
        self.text_var.set(self.text_var.get() + current_sentence)  # Set the text before speaking
        self.current_index += 1
        job = threading.Thread(target=self.speak_text, args=(current_sentence,))
        job.start()
        # job.join()
        
    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.speak_next_sentence()
        # self.master.root.after(500, self.speak_next_sentence)

class UserMessage(ctk.CTkFrame):
    def __init__(self, parent, text = ""):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.message = ctk.CTkLabel(
            master = self,
            corner_radius = 15,
            text = text,
            wraplength = 400,
            justify = "right",
            fg_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK))
        self.message.pack(
            ipadx=2,
            ipady=5,
            anchor="e",
            pady=5
        )
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
                text="",
                corner_radius = 15,
                fg_color=("#dcdcdc", "#2b2b2b")
        )
        self.image_label.place(
            relx = 0,
            rely = 0,
            relwidth = 0.91,
            relheight = 1,
        )
        self.show_current_image()

        # buttons
        if len(self.image_paths) > 1:
            self.place_navigation_buttons()

        self.image_label.bind("<Button-1>", self.open_current_image_system)
        

    def show_current_image(self):
        self.current_image = Image.open(self.image_paths[self.current_index])
        current_ctk_image = self.resize_ctk_image(self.current_image)
        self.image_label.configure(
            image = current_ctk_image
        )
    def place_navigation_buttons(self):
        default_arrow = Image.open(cf.ARROW_IMAGE)
        flip_arrow = ImageOps.flip(default_arrow)
        self.left_arrow = ctk.CTkImage(light_image = default_arrow)
        self.right_arrow = ctk.CTkImage(light_image = flip_arrow)
        self.prev_button = ctk.CTkButton(
            master = self,
            text = "",
            image = self.left_arrow,
            compound = "top",
            corner_radius = 15,
            border_width = 0,
            border_spacing = 0,
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            fg_color = ("#dcdcdc", "#2b2b2b"),
            bg_color = "transparent",
            command = self.show_prev_image
        )
        self.prev_button.place(
            relx = 0.915,
            rely = 0,
            relwidth = 0.085,
            relheight = 0.1
        )

        self.next_button = ctk.CTkButton(
            master = self,
            text = "",
            image = self.right_arrow,
            compound = "bottom",
            corner_radius = 15,
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            fg_color = ("#dcdcdc", "#2b2b2b"),
            bg_color = "transparent",
            command = self.show_next_image
        )
        self.next_button.place(
            relx = 0.915,
            rely = 0.9,
            relwidth = 0.085,
            relheight = 0.1
        )

    def resize_ctk_image(self, open_image):
        real_w, real_h = open_image.size
        if real_w > real_h:
            window_height = self.root.winfo_height()
            image_height = window_height * 0.3
            image_width = real_w * (image_height / real_h)
        else:
            window_width = self.root.winfo_width()
            image_width = window_width * 0.5
            image_height = real_h * (image_width / real_w)
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
        self.micro_off_image = ctk.CTkImage(light_image = Image.open(cf.MICROPHONE_OFF_IMAGE))
        self.micro_on_image = ctk.CTkImage(light_image = Image.open(cf.MICROPHONE_ON_IMAGE))
        self.keyboard_image = ctk.CTkImage(light_image = Image.open(cf.KEYBOARD_IMAGE))
        self.voice_button = ctk.CTkButton(
            master = self,
            text = "",
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            image = self.micro_off_image,
            compound = "top",
            corner_radius = 999,
            command = self.active_micro
        )
        self.keyboard_button = ctk.CTkButton(
            master = self,
            text = "",
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            image = self.keyboard_image,
            corner_radius = 999,
            command = self.active_keyboard
        )
        self.text_frame = ctk.CTkFrame(
            master = self,
            fg_color = "transparent"
        )
        self.text_input = ctk.CTkEntry(
            master = self.text_frame,
            corner_radius = 20,
            placeholder_text = "Escribe tu petición",
            fg_color = "transparent"
        )
        self.error_label = ctk.CTkLabel(
            master = self.text_frame,
            text = "!",
            corner_radius = 50,
            fg_color = (cf.ERROR_COLOR_LIGHT, cf.ERROR_COLOR_DARK)
        )
        self.text_input.bind("<Return>", self.send_text_query)
        self.parent.message_frame.bind("<<AvailableInput>>", self.active_input)
        self.query = None
        self.micro_mode = True

        self.grid_buttons()

    def active_micro(self):
        if self.parent.message_frame.current_message.responding:
            self.voice_button.configure(
                image = ctk.CTkImage(light_image = Image.open(cf.MICROPHONE_DISABLE_IMAGE))
            )
            return
        if self.micro_mode:
            self._canvas.event_generate("<<MicrophoneOn>>")
            return
        self.text_frame.grid_forget()
        self.grid_buttons()
        self.micro_mode = True

    def hearing_button(self):
        self.voice_button.configure(
            image = self.micro_on_image
        )

    def default_button(self):
        self.voice_button.configure(
            image = self.micro_off_image
        )

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
        if self.parent.message_frame.current_message.responding:
            self.error_label.place(
                relx = 0.935,
                rely = 0.222,
                relwidth = 0.04,
                relheight = 0.6
            )
            self.update()
            return
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
    
    def active_input(self,event):
        self.voice_button.configure(
            image = self.micro_off_image
        )
        self.error_label.place_forget()

    def grid_text(self):
        self.text_frame.grid(
            row = 0,
            column = 0,
            columnspan = 4,
            padx = 10,
            pady = 10,
            sticky = "ew"
        )
        self.text_input.place(
            relx = 0,
            rely = 0,
            relheight = 1,
            relwidth = 1
        )