# Word search game:
# We are gonna create a word search game with pygame or tkinter
# so for that we need to create a table of the words where should include 
# the hidden words.

# The game should have the following:
# - Table of words
# - Words to find
# - Timer
# - Score
# - Hints
# - Menu

# The game should start with a menu where you can choose the difficulty
# and the words to find, then the game should start with the timer
# and the score, the words to find should be displayed in the screen
# and the table of words should be displayed with the hidden words
# and the rest of the table should be filled with random letters.
# The words to find should be displayed in the screen and when you
# find a word it should be displayed in the screen with a different
# color and the score should be increased.

import tkinter as tk
import ctypes
import random
import json
import re
import customtkinter as ctk
from . import settings as cf
from PIL import ImageTk

class GameWordSearch(ctk.CTk):
    def __init__(self, title_game = cf.GAME_NAME, data = cf.DEFAULT_DATA, difficulty = cf.DEFAULT_DIFFICULTY):
        super().__init__()
        self.title(title_game)
        self.color_ui = (cf.BG_COLOR_DARK, cf.BG_COLOR_LIGHT)

        self.configure(
            background = self.color_ui
        )

        # setting header
        self.data = data
        self.difficulty = difficulty
        
        self.game = GameFrame(
            master = self,
            data = self.data,
            difficulty = self.difficulty
        )

        self.game.pack(
            side = tk.BOTTOM,
            expand = True,
            padx = 5,
            pady = 10,
            fill = "both"
        )

        self.header = GameHeaderFrame(
            master = self,
            data = data,
            difficulty = self.difficulty
        )
        self.header.pack(
            side = tk.BOTTOM,
            padx = 5,
            pady = 10,
            fill = "x"
        )

        # setting the icon
        # try:
        #     icon_ctk = ImageTk.PhotoImage(file = cf.ICON_IMAGE)
        #     self.wm_iconbitmap()
        #     self.iconphoto(False, icon_ctk)
        #     self.myappid = "word.search.game.1"
        #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        # except:
        #     pass

        self.geometry("810x700")
        self.maxsize(810, 700)

        self.game.word_list_frame.bind("<<GameWon>>", self.header.win_game)

    def run(self):
        self.mainloop()

    def reload_game(self, difficulty = cf.DEFAULT_DIFFICULTY):
        self.game.reload_words(difficulty)
        self.header.reload_timer()


class GameHeaderFrame(ctk.CTkFrame):
    def __init__(self, master, data = cf.DEFAULT_DATA, difficulty = cf.DEFAULT_DIFFICULTY):
        super().__init__(
            master = master,
            fg_color = "transparent"
        )

        self.data = data
        self.current_difficulty = difficulty

        self.set_widgets()
        self.timer_label.bind("<<Timeout>>", self.lose_game)
    
    def get_real_time(self):
        time = self.data.get(cf.CONFIG_KEY)
        if time is None:
            return
        time = time.get(cf.DIFFICULTY_KEY)
        if time is None:
            return
        time = time.get(self.current_difficulty)
        time = time.get(cf.TIME_KEY)
        if time is None:
            return
        else:
            return time
    
    def set_widgets(self):
        # Title
        self.title = ctk.CTkLabel(
            master = self,
            text = "Sopa de letras",
            fg_color = "transparent",
            bg_color = "transparent",
            font = ("Arial", 20)
        )

        self.info_label = ctk.CTkLabel(
            master = self,
            text = "Perdiste, se te acabo el tiempo",
            corner_radius = 20,
            fg_color = (cf.ERROR_COLOR_LIGHT, cf.ERROR_COLOR_DARK),
        )
        
        # Difficulty combobox
        difficulties = list(self.data.get(cf.CONFIG_KEY).get(cf.DIFFICULTY_KEY).keys())
        self.difficulty_combobox = ctk.CTkComboBox(
            master = self,
            bg_color = "transparent",
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            border_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            button_color = (cf.HOVER_COLOR_LIGHT, cf.HOVER_COLOR_DARK),
            button_hover_color = (cf.WIDGET_COLOR_LIGHT, cf.WIDGET_COLOR_DARK),
            dropdown_fg_color = (cf.HOVER_COLOR_LIGHT, cf.HOVER_COLOR_DARK),
            values = difficulties,
            state = "readonly",
            justify = "center",
            command = self.reload
        )
        self.difficulty_combobox.set(cf.DEFAULT_DIFFICULTY)
        # Timer
        self.timer_label = TimerLabel(self, time = self.get_real_time())
        self.timer_label.start_timer()

        self.columnconfigure(0, weight = 1, uniform = "a")
        self.columnconfigure(1, weight = 3, uniform = "a")
        self.columnconfigure(2, weight = 1, uniform = "a")

        self.rowconfigure([0, 1], uniform = "a")

        self.timer_label.grid(row = 0, column = 0, sticky = "w", rowspan = 2, padx = 20)
        self.title.grid(row = 0, column = 1, sticky = "nsew")
        self.difficulty_combobox.grid(row = 0, column = 2, sticky = "e", rowspan = 2, padx = 20)

    def lose_game(self, event):
        self.info_label.configure(
            text = "Perdiste, se te acabo el tiempo",
            fg_color = (cf.ERROR_COLOR_LIGHT, cf.ERROR_COLOR_DARK),
        )
        self.info_label.grid(row = 1, column = 1, padx = 10)
        self.master.game.disable_grid()

    def win_game(self, event):
        self.timer_label.stop_timer()
        self.info_label.configure(
            text = "Ganaste, descubriste las palabras",
            fg_color = (cf.SUCCESS_COLOR_LIGHT, cf.SUCCESS_COLOR_DARK),
        )
        self.info_label.grid(row = 1, column = 1, padx = 10)
        self.master.game.disable_grid()
    
    def reload_timer(self):
        self.timer_label.stop_timer()
        self.timer_label.start_timer(time = self.get_real_time())
    
    def reload(self, event):
        self.info_label.grid_forget()
        self.current_difficulty = self.difficulty_combobox.get()
        self.master.reload_game(difficulty = self.current_difficulty)
        self.reload_timer()

class GameFrame(ctk.CTkFrame):
    def __init__(self, master, data = cf.DEFAULT_DATA, difficulty = cf.DEFAULT_DIFFICULTY):
        super().__init__(
            master = master,
            fg_color = "transparent"
        )
        self.data = data
        self.words = []
        self.added_words = []
        self.current_difficulty = difficulty
        self.get_words()
        # This order is neccesary
        self.orientations = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        self.weights_orientations = [1 for _ in range(len(self.orientations))]

        self.word_grid_frame = None
        self.word_list_frame = None


        self.render_words()

    def get_words(self):
        for word_statement in self.data.get(cf.WORDS_KEY):
            word = word_statement.get(cf.HIDDEN_WORD_KEY)[0].upper()
            self.words.append(word)
    
    def get_real_values(self, value_key):
        config = self.data.get(cf.CONFIG_KEY)
        if config is None:
            return
        config = config.get(cf.DIFFICULTY_KEY)
        if config is None:
            return
        config = config.get(self.current_difficulty)
        config = config.get(value_key)
        if config is None:
            return
        else:
            return config

    def create_table(self):
        self.cols = self.get_real_values(cf.COLS_KEY)
        self.rows = self.get_real_values(cf.ROWS_KEY)

        if self.cols is None or self.rows is None:
            self.cols = 20
            self.rows = 20
        
        self.grid_struct = [['_' for _ in range(self.cols)] for __ in range(self.rows)]

        for word in self.words:
            word_length = len(word)
            if word_length > self.cols or word_length > self.rows:
                continue

            for _ in range(cf.MAX_ITERATIONS):
                orientation = random.choices(self.orientations, weights = self.weights_orientations)[0]
                x_pos = random.randint(0, self.cols - 1)
                y_pos = random.randint(0, self.rows - 1)
                
                end_x = x_pos + word_length * orientation[0]
                end_y = y_pos + word_length * orientation[1]

                if end_x < 0 or end_x >= self.cols:
                    continue
                if end_y < 0 or end_y >= self.rows:
                    continue

                is_failed = False

                # We run through the characters of the word by a index and 
                # we replace with it if is possible
                aux_grid = self.grid_struct
                for i in range(word_length):
                    current_x = x_pos + i * orientation[0]
                    current_y = y_pos + i * orientation[1]
                    if self.grid_struct[current_y][current_x] != '_' and self.grid_struct[current_y][current_x] != word[i]:
                        is_failed = True
                        break;
                        
                # If we failed putting in the grid_struct then we should do this again
                if is_failed:
                    continue
                else:
                    for i in range(word_length):
                        current_x = x_pos + i * orientation[0]
                        current_y = y_pos + i * orientation[1]
                        self.grid_struct[current_y][current_x] = word[i]

                    self.added_words.append(word)
                    break

        self.replace_blanks()
        # print_grid(self.grid_struct)

    def replace_blanks(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid_struct[i][j] == '_':
                    self.grid_struct[i][j] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def render_words(self):
        possible_weight = self.get_real_values(cf.WEIGHTS_KEY)
        if possible_weight is not None:
            self.weights_orientations = possible_weight

        self.added_words = []
        self.create_table()

        self.word_grid_frame = WordGridFrame(self, plain_grid = self.grid_struct, current_words = self.added_words)

        # self.word_grid_frame.grid(row = 0, column = 0, sticky = "nsew", padx = 5)
        self.word_grid_frame.place(relx = 0, rely = 0, relwidth = 0.59, relheight = 1)

        self.word_list_frame = ListWordsFrame(self, data_word = self.data.get(cf.WORDS_KEY), current_words = self.added_words)

        # self.word_list_frame.grid(row = 0, column = 1, padx = 5)
        self.word_list_frame.place(relx = 0.6, rely = 0, relwidth = 0.4, relheight = 0.99)

        # Events
        self.word_grid_frame.bind("<<FoundWord>>", self.hide_question)

    def disable_grid(self):
        for child in self.word_grid_frame.winfo_children():
            child.configure(state = "disabled")

    def reload_words(self, difficulty = cf.DEFAULT_DIFFICULTY):
        self.current_difficulty = difficulty
        self.word_grid_frame.place_forget()
        self.word_list_frame.place_forget()
        self.render_words()
        self.master.game.word_list_frame.bind("<<GameWon>>", self.master.header.win_game)

    def hide_question(self, event):
        word = self.word_grid_frame.last_word
        self.word_list_frame.hide_question(word)

class WordGridFrame(ctk.CTkFrame):
    def __init__(self, master, plain_grid = [], current_words = []):
        super().__init__(
            master = master,
            fg_color = "transparent",
        )
        self.plain_grid = plain_grid
        self.current_words = current_words
        self.current_selection = {
            "Positions": [],
            "Direction": [0, 0],
            "Word": ""
        }
        self.set_grid()
        # self.render_grid()
    pass

    def set_grid(self):
        rows = len(self.plain_grid)
        cols = len(self.plain_grid[0])
        self.buttons = [[0 for _ in range(cols)] for __ in range(rows)]
        for y in range(rows):
            self.grid_rowconfigure(y, weight = 1, uniform = "a")
            for x in range(cols):
                self.grid_columnconfigure(x, weight = 1, uniform = "a")
                text = self.plain_grid[y][x]
                self.buttons[y][x] = LetterButton(
                    master = self, 
                    x_pos = x, 
                    y_pos = y, 
                    text = text
                )
                self.buttons[y][x].grid(row = y, column = x, sticky = "nsew")
    def button_pressing(self, x, y, text):

        self.buttons[y][x].configure(
            bg_color = cf.SELECT_COLOR_LIGHT,
            hover_color = (cf.SELECT_COLOR_LIGHT, cf.SELECT_COLOR_DARK)
        )

        if not self.is_adjacent(x,y) or not self.is_same_direction(x,y):
            self.recolor_selection(cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK)
            self.current_selection["Word"] = ""
            self.current_selection["Positions"] = []

        self.current_selection["Word"] += text
        self.current_selection.get("Positions").append([x, y])
        if self.current_selection["Word"] in self.current_words:
            # print(self.current_selection["Word"])
            self.last_word = self.current_selection["Word"]
            self._canvas.event_generate("<<FoundWord>>")
            self.recolor_selection(cf.SUCCESS_COLOR_LIGHT, cf.SUCCESS_COLOR_DARK, correct_word = False)
            self.current_selection["Word"] = ""
            self.current_selection["Positions"] = []

    def get_direction(self, first_xy, second_xy):
        x, y = second_xy[0] - first_xy[0], second_xy[1] - first_xy[1]
        return [x,y]
    
    def is_adjacent(self, cur_x, cur_y):
        if len(self.current_selection.get("Positions")) == 0:
            return True
        ls_x, ls_y = self.current_selection.get("Positions")[-1]
        if abs(cur_x - ls_x) > 1:
            return False
        if abs(cur_y - ls_y) > 1:
            return False
        return True
    
    def recolor_selection(self, light_color, dark_color, correct_word = True):
        for position in self.current_selection.get("Positions"):
            x, y = position
            if self.buttons[y][x].done_word is True:
                self.buttons[y][x].configure(
                    bg_color = (cf.SUCCESS_COLOR_LIGHT, cf.SUCCESS_COLOR_DARK)
                )
                continue
            self.buttons[y][x].configure(
                bg_color = (light_color, dark_color),
            )
            if correct_word is False:
                self.buttons[y][x].done_word = True
            

    def is_same_direction(self, x, y):
        if len(self.current_selection.get("Positions")) == 1 or len(self.current_selection.get("Positions")) == 0:
            self.current_selection["Direction"] = [0, 0]
            return True
        last_xy = self.current_selection.get("Positions")[-1]
        direction = self.get_direction(last_xy, [x, y])
        
        if len(self.current_selection.get("Positions")) == 2:
            first_xy = self.current_selection.get("Positions")[0]
            second_xy = self.current_selection.get("Positions")[1]
            x_direction, y_direction = self.get_direction(first_xy, second_xy)
            self.current_selection["Direction"] = [x_direction, y_direction]

        return self.current_selection["Direction"] == direction

class ListWordsFrame(ctk.CTkFrame):
    def __init__(self, master, data_word = cf.DEFAULT_DATA.get(cf.WORDS_KEY), current_words = []):
        super().__init__(
            master = master,
            fg_color = "transparent",
        )
        self.data = data_word
        self.current_words = current_words
        self.counter_words = 0
        self.number_label = ctk.CTkLabel(
            master = self,
            text = f"Buscarás {len(current_words)} palabras para estos enunciados:",
            fg_color = "transparent",
            bg_color = "transparent"
        )


        self.frame_scroll_questions = ctk.CTkScrollableFrame(
            master = self,
            fg_color = "transparent",
            bg_color = "transparent",
            scrollbar_button_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            scrollbar_button_hover_color = (cf.HOVER_COLOR_LIGHT, cf.HOVER_COLOR_DARK),
        )
        self.frame_scroll_questions.label_words = dict()
        
        self.set_list()
        
        # Placing widgets
        self.number_label.place(relx = 0, rely = 0)
        self.frame_scroll_questions.place(relx = 0, rely = 0.05, relwidth = 1, relheight = 0.95)

    def set_list(self):
        for word_statement in self.data:
            word_name = word_statement.get(cf.HIDDEN_WORD_KEY)[0].upper()
            if word_name not in self.current_words:
                continue
            self.frame_scroll_questions.label_words[word_name] = ctk.CTkLabel(
                master = self.frame_scroll_questions,
                wraplength = 270,
                justify = "left",
                corner_radius =  15,
                text = word_statement.get(cf.QUESTION_KEY)[0],
                fg_color = (cf.HOVER_COLOR_LIGHT, cf.HOVER_COLOR_DARK)
            )
            self.frame_scroll_questions.label_words[word_name].pack(ipadx = 5, ipady = 3, pady = 3, fill = "x")

    def hide_question(self, word):
        last_text = self.frame_scroll_questions.label_words[word].cget("text")
        current_text = re.sub(r'_+', word, last_text)
        self.frame_scroll_questions.label_words[word].configure(
            text = current_text,
            fg_color = (cf.SUCCESS_COLOR_LIGHT, cf.SUCCESS_COLOR_DARK),
        )
        self.counter_words += 1
        print(word)
        print("de la lista")
        print(list(self.frame_scroll_questions.label_words.keys()))
        if self.counter_words >= len(self.current_words):
            self._canvas.event_generate("<<GameWon>>")
        self.frame_scroll_questions.label_words[word].update()

class LetterButton(ctk.CTkButton):
    def __init__(self, master, x_pos = 0, y_pos = 0, text = ""):
        super().__init__(
            master = master,
            text = text,
            width = 3,
            height = 1,
            corner_radius = 0,
            text_color = ("#000000", "#ffffff"),
            fg_color = "transparent",
            hover_color = (cf.HOVER_COLOR_LIGHT, cf.HOVER_COLOR_DARK),
            command = lambda x = x_pos, y = y_pos, t = text: master.button_pressing(x, y, t)
        )
        self.done_word = False

class TimerLabel(ctk.CTkLabel):
    def __init__(self, master, time = 60):
        super().__init__(
            master = master,
            text = "00:00",
            fg_color = (cf.BG_COLOR_LIGHT, cf.BG_COLOR_DARK),
            bg_color = "transparent",
            font = ("Arial", 20)
        )
        self.bound_time = time
        self.time = time
        self.is_running = False

    def start_timer(self, time = None):
        self.is_running = True
        if time is not None:
            self.bound_time = time
            self.time = time
        else:
            self.time = self.bound_time
        self.update_timer()
    
    def stop_timer(self):
        self.is_running = False
        self.after_cancel(self.after_id)
    
    def update_timer(self):
        if self.time < 0 or not self.is_running:
            self.stop_timer()
            self._canvas.event_generate("<<Timeout>>")
            return

        minutes = self.time // 60
        seconds = self.time % 60
        time_to_str = f"{minutes}:{seconds:02}"
        self.configure(
            text = time_to_str
        )
        self.time -= 1

        if self.winfo_exists():
            self.after_id = self.after(1000, self.update_timer)
        else:
            self.stop_timer()
        

def print_grid(grid):
    for row in grid:
        print(row)
    print()

def darken_color(hex_color, factor=0.7):
    # Convert hexadecimal color to RGB
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # Darken each RGB component
    darkened_rgb = tuple(int(component * factor) for component in rgb)

    # Convert back to hexadecimal
    darkened_hex_color = "#{:02X}{:02X}{:02X}".format(*darkened_rgb)

    return darkened_hex_color

def run_game(data = None):
    if data is None:
        with open("info.json", 'r', encoding="utf-8") as file:
            info = json.load(file)
            info = info["Opciones"]["Juegos"]["Opciones de juego"]["SopaLetras"]
            data = info
    game = GameWordSearch(data = data)
    game.run()

if __name__ == "__main__":
    run_game()