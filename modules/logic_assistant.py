import speech_recognition
import pyttsx3
from settings import *


class LogicalAssist():
    def __init__(self, database):
        self.database = database
        self.current_directory = self.database
        self.username = "Usuario"

    def structure_assist_response(self):
        presentation = self.current_directory.get(PRESENTATION_KEY)
        options = self.get_list_menu()
        return presentation, options

    def structure_user_response(self):
        content = self.is_concept()
        imgs = self.current_directory.get(IMAGES_KEY)
        return content, imgs
    
    def get_list_menu(self):
        return list(self.current_directory.get(OPTIONS_KEY).keys())

    def access_to(self, command_key):
        return self.current_directory.get(command_key)

    def is_concept(self):
        return self.current_directory.get(CONTENT_KEY)
    
    def is_menu(self):
        return self.current_directory.get(OPTIONS_KEY)
    
    def is_question(self):
        return self.current_directory.get("Test")

    def text_to_voice(sentence):
        answer = pyttsx3.init()
        answer.say(sentence)
        answer.runAndWait()

    def recognize_voice(microphone, voice_recognizer):
        # query = input()
        # Initialize recognizer
        query = None

        # Use microphone as source
        try:
            with microphone as source:
                voice_recognizer.adjust_for_ambient_noise(source)
                print("Escuchando...")
                audio = voice_recognizer.listen(source, None)
        except:
            print("No se pudo acceder al micrófono")
            query = input()
            return query

        # Recognize speech using Google Speech Recognition
        try:
            print("Reconociendo...")
            query = voice_recognizer.recognize_google(audio, language='es-PE')
            print(f"Has dicho {query}\n")
            return query

        except speech_recognition.RequestError:
            print("Hubo un error(externo) con la solicitud de reconocimiento")

        except speech_recognition.UnknownValueError:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado")

        query = input()
        return query