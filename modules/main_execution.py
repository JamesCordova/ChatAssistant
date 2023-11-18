from . import main_app
import tkinter as tk
from . import settings as cf
from . import logic_assistant as assist
import json

class MainExecution():
    def __init__(self):
        self.database = self.load_database()
        self.assistant = assist.LogicalAssist(self.database)
        self.main_window = main_app.App()
        self.main_window.action_window.voice_button.configure(
            command = self.send_audio_message
        )
        


    def load_database(self):
        with open("info.json", 'r', encoding="utf-8") as file:
            info_dictionary = json.load(file)
        return info_dictionary
    
    def send_message(self, event):
        self.assistant.query = self.main_window.action_window.query
        print("done")
        print(self.assistant.query)