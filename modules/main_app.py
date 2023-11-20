import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from . import main_window
from . import settings as cf
from . import logic_assistant as assist
import json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Asistente")
        self.color_ui = (cf.BG_COLOR_DARK, cf.BG_COLOR_LIGHT)
        self.geometry("600x500")
        self.minsize(600,500)
        self.configure(
            background = self.color_ui
        )
        # ctk.set_appearance_mode("light")
        self.database = self.load_database()
        self.message_frame = main_window.MessageFrame(self)
        self.message_frame.place(relx=0, rely=0, relheight=0.9, relwidth=1)
        # self.response_frame = ctk.CTkFrame(self)
        # self.response_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

        self.user_messsage = None
        self.action_frame = main_window.ActionFrame(self)
        self.action_frame._canvas.bind("<<DoneQuery>>", self.add_user_message)
        self.action_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

        self.action_frame._canvas.bind("<<MicrophoneOn>>", self.active_micro_voice)

        self.message_frame.bind("<<UserQuery>>", self.respond_user)
        self.assistant = assist.LogicalAssist(self, self.database)
        self.add_assist_message(["Hola. Soy tu Asistente Virtual. Fui creada para instruirte todo respecto a la Estructura de un computador. Antes de empezar ¿Podrias decirme tu nombre?"])
        self.mainloop()
        
    def load_database(self):
        with open("info.json", 'r', encoding="utf-8") as file:
            info_dictionary = json.load(file)
        return info_dictionary

    def active_micro_voice(self, event):
        self.action_frame.query = self.assistant.recognize_voice()
        self.action_frame._canvas.event_generate("<<DoneQuery>>")
    
    def add_user_message(self, event):
        self.assistant.query = self.action_frame.query
        user_message = main_window.UserMessage(
            parent = self.message_frame,
            text = self.assistant.query
        )
        user_message.grid(
            row = self.message_frame.current_row,
            column = 1,
            columnspan = 2,
            sticky="e"
        )
        self.message_frame.add_message(user_message)

    def respond_user(self, event):
        if cf.USERNAME == "Usuario":
            cf.USERNAME = self.assistant.query
            self.add_assist_message(["Mucho gusto " + str(cf.USERNAME) + "."])
            self.add_assist_message(self.assistant.current_directory.get(cf.PRESENTATION_KEY))
            self.add_assist_message(self.assistant.get_list_menu(), optionable=True)
            return
        command = self.assistant.get_keyword_query()
        command = self.assistant.recognize_global_commands(command)
        if not command:
            # assist_message = self.assistant.not_recognized()s
            self.add_assist_message(["No reconocido"])
            return
        self.assistant.access_to(command)
        if self.assistant.is_menu():
            self.add_assist_message(self.assistant.current_directory.get(cf.PRESENTATION_KEY), optionable=False)
            self.add_assist_message(self.assistant.get_list_menu(), optionable=True)
        elif self.assistant.is_concept():
            self.add_assist_message(self.assistant.current_directory.get(cf.CONTENT_KEY), images=self.assistant.current_directory.get(cf.IMAGES_KEY), optionable=False)
        elif self.assistant.is_question():
            pass

    def add_assist_message(self, assist_message, images = [], optionable = False):
        assist_message = main_window.AssistMessage(
            parent = self.message_frame,
            root = self,
            images = images,
            text_list = assist_message,
            is_menu = optionable
        )
        assist_message.grid(
            row = self.message_frame.current_row,
            column=0,
            columnspan=2,
            sticky="ew"
        )
        self.update()
        assist_message.speak_sentences()
        self.message_frame.add_message(assist_message)
