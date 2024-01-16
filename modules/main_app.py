import tkinter as tk
import ctypes
from PIL import Image, ImageTk
import random
import customtkinter as ctk
from games import exec_games as execute
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
        try:
            icon_ctk = ImageTk.PhotoImage(file = cf.ASSIST_ICON_IMAGE)
            self.wm_iconbitmap()
            self.iconphoto(False, icon_ctk)
            self.myappid = "personal.assistant.chat.1"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        except:
            pass

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


        self.message_frame.bind("<<WinGame>>", self.render_again)

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
    
    def render_again(self, event):
        self.assistant.current_directory = self.assistant.database
        # self.add_message_menu()

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
        if cf.USERNAME == None:
            cf.USERNAME = self.assistant.query.capitalize()
            # self.add_assist_message(["Mucho gusto " + str(cf.USERNAME) + "."])
            self.assistant.current_directory = self.assistant.database
            self.add_message_menu()
            return
        
        command = None
        global_command = None
        command = self.assistant.get_keyword_query(self.assistant.current_directory)
        global_command = self.assistant.recognize_global_commands(command)
        self.assistant.access_to(command)

        if not global_command and not self.assistant.is_question():
            self.add_assist_message(["No reconocido"])
            return

        # Show interaction
        if self.assistant.is_menu():
            self.add_message_menu()
        elif self.assistant.is_concept():
            self.add_assist_message(self.assistant.current_directory.get(cf.CONTENT_KEY), images=self.assistant.current_directory.get(cf.IMAGES_KEY))
        elif self.assistant.is_question():
            if self.assistant.index_question > 0:
                previous_question = self.assistant.is_question()[self.assistant.index_question - 1]
                command = self.assistant.get_keyword_query(previous_question)
                command = self.assistant.get_keyword_by_number(command, previous_question)
                self.add_advice(previous_question.get(cf.OPTIONS_KEY).get(command))
            self.add_question()
            self.assistant.index_question += 1
        elif self.assistant.is_images():
            self.add_images()
        elif self.assistant.is_games():
            pr = self.assistant.current_directory.get(cf.PRESENTATION_KEY)
            img = self.assistant.current_directory.get(cf.IMAGES_KEY)
            mn = self.assistant.is_games()
            self.add_interact_menu(message = pr, images = img, options = mn, speechable = False)
            # self.add_game()
        else:
            print("Error")
    

    def add_interact_menu(self, message, images, options, speechable):
        button_message = main_window.ButtonMessage(
            parent = self.message_frame,
            root = self,
            images = images,
            text_list = message,
            options = list(options.keys()),
            speechable = speechable
        )
        button_message.grid(
            row = self.message_frame.current_row,
            column = 0,
            columnspan = 2,
            sticky = "ew"
        )
        button_message.speak_sentences()
        # self.update()
        self.message_frame.add_message(button_message)

    def add_advice(self, is_correct):
        if is_correct:
            self.message_frame.current_message.message.configure(
                fg_color = (cf.SUCCESS_COLOR_LIGHT, cf.SUCCESS_COLOR_DARK)
            )
            self.assistant.correct_answers += 1
        else:
            self.message_frame.current_message.message.configure(
                fg_color = (cf.ERROR_COLOR_LIGHT, cf.ERROR_COLOR_DARK)
            )

    def add_game(self, game_name):
        if game_name == cf.DEFAULT_GAME:
            self.hang_game()
            return
        execute.exec_game(game_name)
        

    def hang_game(self):
        variacion = random.choice(self.assistant.is_games().get("Ahorcado").get("Variaciones"))
        sentence = variacion.get("Enunciado")
        secret_word = variacion.get("Palabra")[0]
        self.add_assist_message(sentence, speechable=False)
        game = main_window.HangGame(
            parent = self.message_frame,
            word = secret_word
        )
        game.grid(
            row = self.message_frame.current_row,
            column = 0,
            columnspan = 2,
            sticky = "ew"
        )
              
        self.message_frame.add_message(game)

    def add_images(self):
        images_list = []
        if type(self.assistant.is_images()) is list:
            images_list = images_list + self.assistant.is_images()
        else:
            images_list = self.list_for_dictionary_values(self.assistant.is_images())
        
        self.add_assist_message(images = images_list)
    
    def list_for_dictionary_values(self, dictionary):
        list_values = []
        for value in dictionary.values():
            if isinstance(value, dict):
                list_values = list_values + self.list_for_dictionary_values(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        list_values = list_values + self.list_for_dictionary_values(item)
                    else:
                        list_values.append(item)
            else:
                list_values.append(value)
        
        return list_values

    def add_message_menu(self):
        message_to_speech = []
        menu = [f"\n{index + 1}) {item}" for index, item in enumerate(self.assistant.get_list_menu())]
        message_to_speech = self.assistant.current_directory.get(cf.PRESENTATION_KEY) + ["\n"] + menu
        self.add_assist_message(message_to_speech)
    
    def add_question(self):
        if self.assistant.index_question >= len(self.assistant.current_directory.get(cf.QUESTION_KEY)):
            self.assistant.index_question = -1
            self.assistant.current_directory = self.assistant.database
            final_message = [f"Has acertado {self.assistant.correct_answers} de {self.assistant.num_questions}"]
            self.assistant.correct_answers = 0
            self.add_assist_message(final_message, speechable=False)
            self.add_message_menu()
            return
        current_question = self.assistant.current_question
        question_message = []
        images_question = []
        statement = current_question.get(cf.STATEMENT_KEY)
        alternatives = list(current_question.get(cf.OPTIONS_KEY).keys())
        menu = [f"\n{index + 1}) {item}" for index, item in enumerate(alternatives)]
        question_message = statement + ["\n"] + menu
        images_question = current_question.get(cf.IMAGES_KEY)
        self.add_assist_message(question_message, images=images_question)
    
    def add_assist_message(self, assist_message = [], images = [], speechable = True):
        assist_message = main_window.AssistMessage(
            parent = self.message_frame,
            root = self,
            images = images,
            text_list = assist_message,
            speechable = speechable
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
