import re
import sys
import random

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLabel, QPushButton, QMainWindow, \
    QFileDialog

# constants
DIFFICULTIES = {
    "easy": [2],
    "medium": [3],
    "hard": [4],
    "impossible": [5]
}
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800


# todo: make more classes (currently just two)
# todo: fix displaying issue with alignment / margin / padding
# todo: still have to display that win-pop-up (QMessageBox)


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
        for ele in self.buttons:
            if self.buttons[ele] == color:
                color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                self.check_for_color_duplicates(color)

    def create_color_for_button(self, button: QPushButton) -> None:
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.check_for_color_duplicates(color)
        self.buttons[button] = color

    def create_single_guess_button(self, x: int, y: int) -> None:
        button = QPushButton()
        self.create_color_for_button(button)

        button.setStyleSheet(
            f"background-color:rgb({self.buttons[button][0]}, {self.buttons[button][1]}, {self.buttons[button][2]})")
        button.setFixedSize((WINDOW_WIDTH - 50) // (self.active_difficulty * 2),
                            (WINDOW_HEIGHT - 50) // self.active_difficulty)

        self.layout.addWidget(button, x, y)

    def create_guess_buttons(self) -> None:
        for x in range(0, self.active_difficulty):
            for y in range(0, self.active_difficulty):
                self.create_single_guess_button(x, y)

    # --- check if clicked button is correct or incorrect ---
    def get_correct_color(self) -> None:
        self.correct_color = random.choice(list(self.buttons.values()))

    def check_clicked_button(self) -> None:
        for ele in self.buttons:
            if self.buttons[ele] == self.correct_color:
                ele.clicked.connect(lambda: self.render_new_game(self.active_difficulty))
            else:
                ele.clicked.connect(lambda: self.update_tries_on_click("set"))

    # --- create correct button ---
    def create_correct_button(self) -> None:
        self.correct_color_button = QPushButton("True Color")

        self.correct_color_button.setStyleSheet(
            f"font-size: 18px; background-color:rgb({self.correct_color[0]}, {self.correct_color[1]},"
            f"{self.correct_color[2]})")
        self.correct_color_button.setFixedSize((400 - 50), (200 - 50))

        self.layout.addWidget(self.correct_color_button, 0, self.active_difficulty + 1)

    # --- create tries button ---
    def create_tries_label(self) -> None:
        self.tries_label = QLabel(f"Tries: {self.tries}")

        self.tries_label.setStyleSheet("font-size: 18px")
        self.tries_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_color_button.setFixedSize((400 - 50), (200 - 50))
        self.layout.addWidget(self.tries_label, 1, self.active_difficulty + 1)

    def update_tries_on_click(self, _type: str) -> None:
        if _type == "set":
            self.tries += 1
            self.tries_label.setText(f"Tries: {self.tries}")
        elif _type == "reset":
            self.tries = 0
            self.tries_label.setText(f"Tries: {self.tries}")

    # --- render new game on win ---
    def reset_buttons(self):
        for ele in self.buttons:
            ele.deleteLater()

    def render_new_game(self, _difficulty: int) -> None:
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


# todo: re-comment this section here
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
    def write_in_file(self, filename, window) -> None:
        try:
            with open(filename, "w") as file:
                file.write(f"{window.active_difficulty}\n{window.tries}\n")
                # file.write(f"{window.tries}\n")

        except FileNotFoundError:
            print("file not found")
            self.close_main_window()

    def read_from_file(self, filename) -> list:
        try:
            with open(filename, "r") as file:
                return file.readlines()

        except FileNotFoundError:
            print("file not found")
            self.close_main_window()

    # --- file handling ---

    def menu_file_load_file(self, window) -> None:
        file_filter = ["Text files (*.txt)", "All files (*)"]
        filters_filer = ";;".join(file_filter)

        filename = QFileDialog.getOpenFileName(self, filter=filters_filer, initialFilter=filters_filer[0])
        read_data = self.read_from_file(filename[0])

        difficulty = int(read_data[0])
        tries = int(read_data[1])

        window.render_new_game_from_load(difficulty, tries)

    def menu_file_save_file(self, window) -> None:
        file_filter = ["Text files (*.txt)", "All files (*)"]
        filters_filer = ";;".join(file_filter)

        filename = QFileDialog.getSaveFileName(self, filter=filters_filer, initialFilter=filters_filer[0])[0]

        self.write_in_file(filename, window)

    def menu_bar(self, window) -> None:
        menu_file = self.menu.addMenu("&File")
        menu_file.addSeparator()

        menu_file.addAction(self.menu_file_button_save_file)
        menu_file.addAction(self.menu_file_button_load_file)

        self.menu_file_button_save_file.triggered.connect(lambda: self.menu_file_save_file(window))
        self.menu_file_button_load_file.triggered.connect(lambda: self.menu_file_load_file(window))

        menu_difficulty = self.menu.addMenu("&Difficulty")
        menu_difficulty.addSeparator()

        for ele in DIFFICULTIES:
            action = QAction(ele, self)
            DIFFICULTIES[ele].append(action)

            menu_difficulty.addAction(action)

    def difficulty_handler(self, window) -> None:
        for ele in DIFFICULTIES:
            if ele == "easy":
                easy = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(easy))
            if ele == "medium":
                medium = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(medium))
            if ele == "hard":
                hard = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(hard))
            if ele == "impossible":
                impossible = DIFFICULTIES[ele][0]
                DIFFICULTIES[ele][1].triggered.connect(lambda: window.render_new_game(impossible))


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
