from . import main_app
from settings import *
from logic_assistant import *
import json

class MainExecution():
    def __init__(self):
        self.database = self.load_database()
        self.assistant = LogicalAssist(self.database)
        self.voice_recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.main_window = main_app.App()
        self.main_window.action_window.set_button_command(self.execute_command)
        self.main_window.message_window.set_message(self.assistant.structure_assist_response())
        self.main_window.message_window.set_message(self.assistant.structure_user_response())
        self.main_window.message_window.set_message(self.assistant.structure_assist_response())

    def load_database(self):
        with open("info.json", 'r', encoding="utf-8") as file:
            info_dictionary = json.load(file)
        return info_dictionary