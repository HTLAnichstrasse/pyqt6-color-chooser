import sys
import random

from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLabel, QPushButton, QMainWindow, \
    QFileDialog

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800
DIFFICULTIES = {
    "easy": [2],
    "medium": [3],
    "hard": [4],
    "impossible": [5]
}


# todo: what still isn't that beautiful = that it's all together a GridLayout and not 2 different Layouts with (
#  QBoxLayout & QGridLayout - parent & child) ==> gonna make classes for the Layouts so it's more readable and the
#  tries get displayed correctly


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.buttons = {}
        self.correct_color = []
        self.tries = 0
        self.active_difficulty = 2
        self.tries_label = None
        self.correct_color_button = None

    def run(self) -> None:
        self.window_ui()
        self.create_guess_buttons()
        self.get_correct_color()
        self.create_correct_button()
        self.create_tries_label()
        self.check_clicked_button()

    def close_window(self) -> None:
        Window.close(self)

    def window_ui(self) -> None:
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # --------------------------------------------------------------------------------
    # --- guesser button ---
    def check_for_color_duplicates(self, color: list[int, int, int]) -> None:
        # checks if there are any duplicated colors - handling = recursively

        for ele in self.buttons:
            if self.buttons[ele] == color:
                color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                self.check_for_color_duplicates(color)

    def create_color_for_button(self, button: QPushButton) -> None:
        # creates the rgb-color-code for a single button in the button-field

        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.check_for_color_duplicates(color)
        self.buttons[button] = color

    def create_single_guess_button(self, x: int, y: int) -> None:
        # creates a single button in the button-field

        button = QPushButton()
        self.create_color_for_button(button)

        button.setStyleSheet(
            f"background-color:rgb({self.buttons[button][0]}, {self.buttons[button][1]}, {self.buttons[button][2]})")
        button.setFixedSize((WINDOW_WIDTH - 50) // (self.active_difficulty * 2),
                            (WINDOW_HEIGHT - 50) // self.active_difficulty)

        self.layout.addWidget(button, x, y)

    def create_guess_buttons(self) -> None:
        # creates button-field

        for x in range(0, self.active_difficulty):
            for y in range(0, self.active_difficulty):
                self.create_single_guess_button(x, y)

    # --- check if clicked button is correct or incorrect ---
    def get_correct_color(self) -> None:
        # chooses a random color out of all colors

        self.correct_color = random.choice(list(self.buttons.values()))

    def check_clicked_button(self) -> None:
        # check if correct or incorrect button was clicked

        for ele in self.buttons:
            if self.buttons[ele] == self.correct_color:
                ele.clicked.connect(lambda: self.render_new_game(self.active_difficulty, "win"))
            else:
                ele.clicked.connect(lambda: self.update_tries_on_click("set"))

    # --- create correct button ---
    def create_correct_button(self) -> None:
        # displays the button on the side which represents the color the user is looking for

        self.correct_color_button = QPushButton("True Color")

        self.correct_color_button.setStyleSheet(
            f"font-size: 18px; background-color:rgb({self.correct_color[0]}, {self.correct_color[1]},"
            f"{self.correct_color[2]})")
        self.correct_color_button.setFixedSize((400 - 50), (200 - 50))

        self.layout.addWidget(self.correct_color_button, 0, (self.active_difficulty * 100))

    # --- create tries button ---
    def create_tries_label(self) -> None:
        # creates the tries label

        self.tries_label = QLabel(f"Tries: {self.tries}")

        self.tries_label.setStyleSheet("font-size: 18px")
        self.tries_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_color_button.setFixedSize((400 - 50), (200 - 50))

        self.layout.addWidget(self.tries_label, 1, self.active_difficulty * 100)

    def update_tries_on_click(self, _type: str) -> None:
        # resets or sets the tries-counter

        if _type == "set":
            self.tries += 1
            self.tries_label.setText(f"Tries: {self.tries}")
        if _type == "reset":
            self.tries = 0
            self.tries_label.setText(f"Tries: {self.tries}")

    # --- render new game on win ---
    def reset_buttons(self):
        # resets the buttons

        for ele in self.buttons:
            ele.deleteLater()

    def display_win_alert_message(self):
        # displays the win alert message (popup)

        win_alert = QMessageBox()
        win_alert.setIcon(QMessageBox.Icon.Information)
        win_alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        win_alert.setWindowTitle("win-message")
        win_alert.setText(f"You guessed the correct color. Congrats!")
        win_alert.setInformativeText(f"Tries: {self.tries}")
        win_alert.exec()

    def render_new_game(self, _difficulty: int, _type: str) -> None:
        # renders the new game when difficulty changed / correct guess
        
        if _type == "win":
            self.display_win_alert_message()

        self.active_difficulty = _difficulty

        self.reset_buttons()
        self.buttons = {}

        self.update_tries_on_click("reset")
        self.create_guess_buttons()
        self.get_correct_color()

        self.correct_color_button.setStyleSheet(
            f"font-size: 18px; background-color:rgb({self.correct_color[0]}, {self.correct_color[1]},"
            f" {self.correct_color[2]})")

        self.check_clicked_button()

    def render_new_game_from_load(self, _difficulty: int, _tries: int) -> None:
        # renders the new game when it's loaded from a file

        self.active_difficulty = _difficulty
        self.tries_label.setText(f"Tries: {_tries}")

        self.reset_buttons()
        self.buttons = {}

        self.create_guess_buttons()
        self.get_correct_color()

        self.correct_color_button.setStyleSheet(
            f"font-size: 18px; background-color:rgb({self.correct_color[0]}, {self.correct_color[1]},"
            f" {self.correct_color[2]})")

        self.check_clicked_button()


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self, window):
        super().__init__()
        self.layout = QGridLayout()

        self.menu = self.menuBar()

        self.menu_file_button_save_file = QAction("Save File")
        self.menu_file_button_load_file = QAction("Load File")

        self.menu_difficulty_button_easy = QAction("easy")
        self.menu_difficulty_button_medium = QAction("medium")
        self.menu_difficulty_button_hard = QAction("hard")

        self.buttons = window.buttons
        self.correct_color = window.correct_color
        self.active_difficulty = window.active_difficulty

    def run(self, window) -> None:
        self.window_ui()
        self.menu_bar(window)
        self.difficulty_handler(window)

    def close_main_window(self) -> None:
        MainWindow.close(self)

    def window_ui(self) -> None:
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # --------------------------------------------------------------------------------

    # --- read & write func ---
    def read_from_file(self, filename) -> list:
        # reads file
        try:
            with open(filename, "r") as file:
                return file.readlines()

        except FileNotFoundError:
            print("file not found")
            self.close_main_window()

    def write_in_file(self, filename, window) -> None:
        # writes in file

        try:
            with open(filename, "w") as file:
                file.write(f"{window.active_difficulty}\n{window.tries}\n")
                # file.write(f"{window.tries}\n")

        except FileNotFoundError:
            print("file not found")
            self.close_main_window()

    # --- file handling ---

    def menu_file_read_file(self, window) -> None:
        # filters the file type selection & handles it afterwards

        file_filter = ["Text files (*.txt)", "All files (*)"]
        filters_filer = ";;".join(file_filter)

        filename = QFileDialog.getOpenFileName(self, filter=filters_filer, initialFilter=filters_filer[0])
        read_data = self.read_from_file(filename[0])

        difficulty = int(read_data[0])
        tries = int(read_data[1])

        window.render_new_game_from_load(difficulty, tries)

    def menu_file_write_file(self, window) -> None:
        # filters the file type selection & handles it afterwards

        file_filter = ["Text files (*.txt)", "All files (*)"]
        filters_filer = ";;".join(file_filter)

        filename = QFileDialog.getSaveFileName(self, filter=filters_filer, initialFilter=filters_filer[0])[0]

        self.write_in_file(filename, window)

    # --- general navbar ---
    def menu_bar(self, window) -> None:
        # general setup for the menubar & handles the sub-menus (actions)

        menu_file = self.menu.addMenu("&File")
        menu_file.addSeparator()

        menu_file.addAction(self.menu_file_button_save_file)
        menu_file.addAction(self.menu_file_button_load_file)

        self.menu_file_button_save_file.triggered.connect(lambda: self.menu_file_write_file(window))
        self.menu_file_button_load_file.triggered.connect(lambda: self.menu_file_read_file(window))

        menu_difficulty = self.menu.addMenu("&Difficulty")
        menu_difficulty.addSeparator()

        for ele in DIFFICULTIES:
            action = QAction(ele, self)
            DIFFICULTIES[ele].append(action)

            menu_difficulty.addAction(action)

    # --- handles the different difficulties ---
    def difficulty_handler(self, window) -> None:
        # handles difficulty based on which is selected in the sub-menu
        # hardcoded

        for ele in DIFFICULTIES:
            if ele == "easy":
                easy = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(easy, "new"))
            if ele == "medium":
                medium = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(medium, "new"))
            if ele == "hard":
                hard = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(hard, "new"))
            if ele == "impossible":
                impossible = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(impossible, "new"))


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


def window_handler() -> None:
    app = QApplication(sys.argv)

    window = Window()
    # window.show()
    window.run()

    main_window = MainWindow(window)
    main_window.setCentralWidget(window)
    main_window.show()
    main_window.run(window)

    try:
        app.exec()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


def main():
    window_handler()


if __name__ == '__main__':
    main()
