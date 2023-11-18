import speech_recognition
import pyttsx3
from . import settings as cf


class LogicalAssist():
    def __init__(self, database):
        self.database = database
        self.current_directory = self.database
        self.username = "Usuario"
        self.query = None

    def assist_menu_response(self):
        presentation = self.current_directory.get(cf.PRESENTATION_KEY)
        options = self.get_list_menu()
        return presentation, options

    def assist_content_response(self):
        content = self.is_concept()
        imgs = self.current_directory.get(cf.IMAGES_KEY)
        return content, imgs
    
    def get_list_menu(self):
        return list(self.current_directory.get(cf.OPTIONS_KEY).keys())

    def access_to(self, command_key):
        if command_key:
            pre_directory = self.is_menu().get(command_key.capitalize())
            print(pre_directory)
        if pre_directory:
            self.current_directory = pre_directory
        print(self.current_directory)
        return self.current_directory

    def is_concept(self):
        return self.current_directory.get(cf.CONTENT_KEY)
    
    def is_menu(self):
        return self.current_directory.get(cf.OPTIONS_KEY)
    
    def is_question(self):
        return self.current_directory.get("Test")
    
    def get_keyword_query(self):
        if not self.is_menu():
            return
        for key in self.is_menu():
            if key.lower() in self.query.lower():
                return key
            
        return None

    def text_to_voice(sentence):
        answer = pyttsx3.init()
        answer.say(sentence)
        answer.runAndWait()

    @staticmethod
    def recognize_voice():
        # return input()
        # Initialize recognizer
        query = None
        microphone = speech_recognition.Microphone()
        voice_recognizer = speech_recognition.Recognizer()

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