import tkinter as tk
import ctypes
from PIL import Image, ImageTk
import threading
import time
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
        
        # setting the icons 
        icon_ctk = ImageTk.PhotoImage(file = cf.ASSIST_ICON_IMAGE)
        self.wm_iconbitmap()
        self.iconphoto(False, icon_ctk)
        self.myappid = "personal.assistant.chat.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)

        self.geometry("600x720")
        self.minsize(600,720)
        self.maxsize(840,1010)
        self.configure(
            background = self.color_ui
        )
        # ctk.set_appearance_mode("light")
        self.database = self.load_database()
        self.advice_label = ctk.CTkLabel(master = self)
        self.message_frame = main_window.MessageFrame(self)
        self.message_frame.place(
            relx = 0,
            rely = 0,
            relheight = 0.92,
            relwidth = 1
        )
        # self.response_frame = ctk.CTkFrame(self)
        # self.response_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

        self.user_messsage = None
        self.action_frame = main_window.ActionFrame(self)
        self.action_frame._canvas.bind("<<DoneQuery>>", self.add_user_message)
        self.action_frame.place(
            relx = 0,
            rely = 0.92,
            relheight = 0.08,
            relwidth = 1
        )

        self.action_frame._canvas.bind("<<MicrophoneOn>>", self.active_micro_voice)

        self.message_frame.bind("<<UserQuery>>", self.respond_user)
        self.assistant = assist.LogicalAssist(self, self.database)
        self.add_assist_message(self.assistant.current_directory.get(cf.REQUEST_KEY))
        self.mainloop()
        
    def load_database(self):
        with open("info.json", 'r', encoding="utf-8") as file:
            info_dictionary = json.load(file)
        return info_dictionary

    def active_micro_voice(self, event):
        if self.message_frame.current_message.responding:
           return 
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
        # if cf.USERNAME == "Usuario":
        #     cf.USERNAME = self.assistant.query
        #     # self.add_assist_message(["Mucho gusto " + str(cf.USERNAME) + "."])
        #     self.add_message_menu()
        #     return
        # if self.assistant.is_question():
        #     command = self.assistant.get_keyword_query(self.assistant.current_question)
        #     self.assistant.index_question += 1
        # else:
        #     command = self.assistant.get_keyword_query(self.assistant.current_directory)
        #     command = self.assistant.recognize_global_commands(command)
        
        # if self.assistant.current_question:
        #     self.add_advice(self.assistant.current_question.get(cf.OPTIONS_KEY).get(command))
        # else:
        #     pass
        # if not command:
        #     # assist_message = self.assistant.not_recognized()
        #     self.add_assist_message(["No reconocido"])
        #     return
        # self.assistant.access_to(command)

        # self.assistant.query = ""
        command = None
        command = self.assistant.get_keyword_query(self.assistant.current_directory)
        self.assistant.access_to(command)

        # Show interaction
        if self.assistant.is_menu():
            self.add_message_menu()
        elif self.assistant.is_concept():
            self.add_assist_message(self.assistant.current_directory.get(cf.CONTENT_KEY), images=self.assistant.current_directory.get(cf.IMAGES_KEY))
        elif self.assistant.is_question():
            if self.assistant.index_question > 0:
                previous_question = self.assistant.is_question()[self.assistant.index_question - 1]
                print(previous_question)
                command = self.assistant.get_keyword_query(previous_question)
                print(command)
                self.add_advice(previous_question.get(cf.OPTIONS_KEY).get(command))
            self.add_question()
            self.assistant.index_question += 1
            print("Hecho")
            pass
        else:
            print("nothing")
    

    def add_advice(self, is_correct):
        if is_correct:
            self.message_frame.current_message.message.configure(
                fg_color = (cf.SUCCESS_COLOR_LIGHT, cf.SUCCESS_COLOR_DARK)
            )
        else:
            self.message_frame.current_message.message.configure(
                fg_color = (cf.ERROR_COLOR_LIGHT, cf.ERROR_COLOR_DARK)
            )

    def add_message_menu(self):
        message_to_speech = []
        menu = [f"\n{index + 1}) {item}" for index, item in enumerate(self.assistant.get_list_menu())]
        message_to_speech = self.assistant.current_directory.get(cf.PRESENTATION_KEY)+ ["\n"] + menu
        self.add_assist_message(message_to_speech)
    
    def add_question(self):
        if self.assistant.index_question >= len(self.assistant.current_directory.get(cf.QUESTION_KEY)):
            print(self.assistant.current_directory)
            return
        current_question = self.assistant.current_question
        question_message = []
        statement = current_question.get(cf.STATEMENT_KEY)
        alternatives = list(current_question.get(cf.OPTIONS_KEY).keys())
        menu = [f"\n{index + 1}) {item}" for index, item in enumerate(alternatives)]
        question_message = statement + ["\n"] + menu
        self.add_assist_message(question_message)
    
    def add_assist_message(self, assist_message, images = [], is_advice = False, optionable = False):
        assist_message = main_window.AssistMessage(
            parent = self.message_frame,
            root = self,
            images = images,
            text_list = assist_message,
            is_menu = optionable
        )
        assist_message.grid(
            row = self.message_frame.current_row,
            column = 0,
            columnspan = 2,
            sticky = "ew"
        )
        assist_message.speak_sentences()
        # self.update()
        self.message_frame.add_message(assist_message)
