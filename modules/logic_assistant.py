import speech_recognition
import pyttsx3
from . import settings as cf


class LogicalAssist():
    def __init__(self, root, database):
        self.root = root
        self.database = database
        # self.current_directory = {
        #     "Solicitud": ["Hola. Soy tu Asistente Virtual. Fui creada para instruirte todo respecto a la Estructura de un computador.", "Antes de empezar ¿Podrias decirme tu nombre?"],
        #     "Ejecución de instrucciones": self.database
        # }
        self.current_directory = self.database
        self.index_question = 0
        self.current_question = None
        self.global_commands = {
            "Salir": exit,
            "salir": exit,
            "Volver al inicio": self.database,
            "volver al inicio": self.database,
            "Regresar": self.database,
            "regresar": self.database
        }
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
        pre_directory = None
        if command_key:
            pre_directory = self.is_menu().get(command_key.capitalize())
        if pre_directory:
            self.global_commands["Regresar"] = self.current_directory
            self.global_commands["regresar"] = self.current_directory
            self.current_directory = pre_directory
        return self.current_directory

    def recognize_global_commands(self, command):
        func = ""
        for key in list(self.global_commands.keys()):
            if key in self.query.lower():
                func = self.global_commands.get(key)
        if type(func) is dict:
            self.current_directory = func
            return "None is valid"
        elif callable(func):
            return func(0)
        else:
            return command
        
    def is_request(self):
        return self.current_directory.get(cf.REQUEST_KEY)

    def is_concept(self):
        return self.current_directory.get(cf.CONTENT_KEY)
    
    def is_menu(self):
        return self.current_directory.get(cf.OPTIONS_KEY)
    
    def is_question(self):
        questions =  self.current_directory.get(cf.QUESTION_KEY)
        if questions and self.index_question < len(questions):
            self.current_question = questions[self.index_question]
        return questions
    
    def get_keyword_query(self, current_directory):
        if not current_directory.get(cf.OPTIONS_KEY):
            return
        for key in current_directory.get(cf.OPTIONS_KEY):
            if key.lower() in self.query.lower():
                return key
            
        return None
    
    @staticmethod
    def text_to_voice(sentence):
        answer = pyttsx3.init()
        answer.say(sentence)
        answer.runAndWait()

    def recognize_voice(self):
        # return input()
        # Initialize recognizer
        query = ""
        microphone = speech_recognition.Microphone()
        voice_recognizer = speech_recognition.Recognizer()
        # Use microphone as source
        try:
            with microphone as source:
                voice_recognizer.adjust_for_ambient_noise(source)
                self.root.action_frame.hearing_button()
                self.root.update()
                audio = voice_recognizer.listen(source, None)
        except:
            print("No se pudo acceder al micrófono")
            self.query = input()
            return self.query

        # Recognize speech using Google Speech Recognition
        try:
            self.root.action_frame.default_button()
            self.root.update()
            query = voice_recognizer.recognize_google(audio, language='es-PE')
            print(f"Has dicho {query}\n")
            return query

        except speech_recognition.RequestError:
            print("Hubo un error(externo) con la solicitud de reconocimiento")

        except speech_recognition.UnknownValueError:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado")
        self.query = input()
        return self.query