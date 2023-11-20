import tkinter as tk
import threading
import pyttsx3
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageOps, ImageSequence
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
        self.current_row = 0

        pass

    def add_message(self, widget):
        self.messages.append(widget)
        self.current_row += 1
        self._scrollbar.set(start_value=0.9, end_value=1)
        if type(widget) is UserMessage:
            self.event_generate("<<UserQuery>>")
        return widget

class AssistMessage(ctk.CTkFrame):
    def __init__(self, parent, root, images = [], text_list = [], is_menu = False):
        super().__init__(
            master = parent,
            fg_color="transparent"
        )
        self.current_images = []
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
        root.update_idletasks()

        # if self.is_menu:
        #     for i, option in enumerate(text, start = 1):
        #         formatted_text = str(f"{str(i)}) {option.capitalize()}\n").format(username = cf.USERNAME, topic = cf.TOPIC)
        #         self.string_message.set(self.string_message.get() + formatted_text)
        #         root.update()
        #         threading.Thread(target = assist.LogicalAssist.text_to_voice(formatted_text)).start()
        # elif type(text) is list:
        #     for sentence in text:
        #         formatted_text = sentence.format(username = cf.USERNAME, topic = cf.TOPIC)
        #         self.string_message.set(self.string_message.get() + f"{formatted_text} ")
        #         root.update()
        #         threading.Thread(target = assist.LogicalAssist.text_to_voice(formatted_text)).start()
        # else:
        #     self.string_message.set(text)
        #     root.update()
        #     threading.Thread(target = assist.LogicalAssist.text_to_voice(text)).start()

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
        if self.sentence_list and self.current_index < len(self.sentence_list):
            if self.is_menu:
                current_sentence = str(f"{str(self.current_index + 1)}) {self.sentence_list[self.current_index].capitalize()}\n").format(username = cf.USERNAME, topic = cf.TOPIC)
            else:
                current_sentence = str(self.sentence_list[self.current_index] + " ").format(username = cf.USERNAME, topic = cf.TOPIC)
            self.text_var.set(self.text_var.get() + current_sentence)  # Set the text before speaking
            self.current_index += 1
            self.speak_text(current_sentence)
            # job = threading.Thread(target=self.speak_text(current_sentence))
            # job.start()
            # job.join()
        
    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
        self.master.root.after(1000, self.speak_next_sentence)

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
            relwidth = 1,
            relheight = 1,
        )
        self.show_current_image()

        # buttons
        if len(self.image_paths) > 1:
            self.place_navigation_buttons()

        self.image_label.bind("<Button-1>", self.open_current_image_system)
        

    def show_current_image(self):
        current_image = Image.open(self.image_paths[self.current_index])
        current_ctk_image = self.resize_ctk_image(current_image)
        self.image_label.configure(
            image = current_ctk_image
        )
    def place_navigation_buttons(self):
        default_arrow = Image.open(cf.ARROW_IMAGE)
        mirror_arrow = ImageOps.mirror(default_arrow)
        self.right_arrow = ctk.CTkImage(light_image = default_arrow)
        self.left_arrow = ctk.CTkImage(light_image = mirror_arrow)
        self.prev_button = ctk.CTkButton(
            master = self,
            text = "",
            image = self.left_arrow,
            compound = "left",
            corner_radius = 15,
            border_width = 0,
            border_spacing = 0,
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            fg_color = ("#dcdcdc", "#2b2b2b"),
            bg_color = ("#dcdcdc", "#2b2b2b"),
            command = self.show_prev_image
        )
        self.prev_button.place(
            relx = 0,
            rely = 0.4,
            relwidth = 0.05,
            relheight = 0.2
        )

        self.next_button = ctk.CTkButton(
            master = self,
            text = "",
            image = self.right_arrow,
            compound = "right",
            corner_radius = 15,
            hover_color = (cf.MESSAGE_COLOR_LIGHT, cf.MESSAGE_COLOR_DARK),
            fg_color = ("#dcdcdc", "#2b2b2b"),
            bg_color = ("#dcdcdc", "#2b2b2b"),
            command = self.show_next_image
        )
        self.next_button.place(
            relx = 0.95,
            rely = 0.4,
            relwidth = 0.05,
            relheight = 0.2
        )

    def resize_ctk_image(self, open_image):
        real_w, real_h = open_image.size
        window_height = self.root.winfo_height()
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
        self.current_frame = 0
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
            self._canvas.event_generate("<<MicrophoneOn>>")
            pass
        self.keyboard_button.grid_forget()
        self.text_input.grid_forget()
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