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
        ctk.set_appearance_mode("light")
        self.database = self.load_database()
        self.assistant = assist.LogicalAssist(self.database)
        self.message_frame = main_window.MessageFrame(self)
        self.message_frame.place(relx=0, rely=0, relheight=0.9, relwidth=1)
        self.add_assist_message(self.assistant.current_directory.get(cf.PRESENTATION_KEY), optionable=False)
        self.add_assist_message(self.assistant.get_list_menu(), optionable=True)
        # self.response_frame = ctk.CTkFrame(self)
        # self.response_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

        self.user_messsage = None
        self.action_frame = main_window.ActionFrame(self)
        self.action_frame._canvas.bind("<<DoneQuery>>", self.add_user_message)
        self.action_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

        self.message_frame.bind("<<UserQuery>>", self.respond_user)
        
    def load_database(self):
        with open("info.json", 'r', encoding="utf-8") as file:
            info_dictionary = json.load(file)
        return info_dictionary
    
    def add_user_message(self, event):
        self.assistant.query = self.action_frame.query
        print(self.assistant.query)
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
        command = self.assistant.get_keyword_query()
        if not command:
            # assist_message = self.assistant.not_recognized()
            self.add_assist_message("No reconocido")
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
            text = assist_message,
            is_menu = optionable
        )
        assist_message.grid(
            row = self.message_frame.current_row,
            column=0,
            columnspan=2,
            sticky="ew"
        )
        self.message_frame.add_message(assist_message)

App()