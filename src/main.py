import sys
import random

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLineEdit, QLabel, QPushButton, \
    QMainWindow, QFileDialog, QVBoxLayout, QMenu, QMenuBar, QToolBar, QStatusBar
from PyQt6.uic.properties import QtGui

# constants
DIFFICULTIES = {
    "easy": 2,
    "medium": 3,
    "hard": 4,
    "impossible": 5
}
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800


# todo: implement icons to display save and load options nicely - currently the save & load option is just an empty
#  gray icon
# todo: write cards and navbar in a separate class object
# todo: also write an class for every grid layout and then add it to the window_handler function
# todo: Difficulties: Easy(2|2) Medium(3|3) Hard(4|4) Impossible(5|5)
# todo: save game & load game


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

    def run(self):
        self.window_ui()
        # self.navbar()
        self.create_guess_buttons()
        self.get_correct_color()
        self.create_correct_button()
        self.create_tries_label()
        self.check_clicked_button()

    def close_window(self):
        Window.close(self)

    def window_ui(self):
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # --------------------------------------------------------------------------------
    # --- guesser button ---
    def check_for_color_duplicates(self, color: list[int, int, int]):
        for ele in self.buttons:
            if self.buttons[ele] == color:
                color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                self.check_for_color_duplicates(color)

    def create_color_for_button(self, button):
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.check_for_color_duplicates(color)
        self.buttons[button] = color

    def create_single_guess_button(self, x: int, y: int):
        button = QPushButton()
        self.create_color_for_button(button)

        button.setStyleSheet(
            f"background-color:rgb({self.buttons[button][0]}, {self.buttons[button][1]}, {self.buttons[button][2]})")
        button.setFixedSize((WINDOW_WIDTH - 50) // (self.active_difficulty * 2),
                            (WINDOW_HEIGHT - 50) // self.active_difficulty)

        self.layout.addWidget(button, x, y)

    def create_guess_buttons(self):
        for x in range(0, self.active_difficulty):
            for y in range(0, self.active_difficulty):
                self.create_single_guess_button(x, y)

    # --- check if clicked button is correct or incorrect ---
    def get_correct_color(self):
        self.correct_color = random.choice(list(self.buttons.values()))

    def check_clicked_button(self):
        for ele in self.buttons:
            if self.buttons[ele] == self.correct_color:
                ele.clicked.connect(lambda: self.render_new_game())
            else:
                ele.clicked.connect(lambda: self.update_tries_on_click("set"))

    # --- create correct button ---
    def create_correct_button(self):
        self.correct_color_button = QPushButton("True Color")

        self.correct_color_button.setStyleSheet(
            f"font-size: 18px; background-color:rgb({self.correct_color[0]}, {self.correct_color[1]},"
            f" {self.correct_color[2]})")
        self.correct_color_button.setFixedSize((400 - 50), (200 - 50))

        self.layout.addWidget(self.correct_color_button, 0, self.active_difficulty + 1)

    # --- create tries button ---
    def create_tries_label(self):
        self.tries_label = QLabel(f"Tries: {self.tries}")

        self.tries_label.setStyleSheet("font-size: 18px")
        self.tries_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_color_button.setFixedSize((400 - 50), (200 - 50))
        self.layout.addWidget(self.tries_label, 1, self.active_difficulty + 1)

    def update_tries_on_click(self, _type: str):
        if _type == "set":
            self.tries += 1
            self.tries_label.setText(f"Tries: {self.tries}")
        elif _type == "reset":
            self.tries = 0
            self.tries_label.setText(f"Tries: {self.tries}")

    # --- render new game on win ---
    def render_new_game(self):
        self.buttons = {}

        self.update_tries_on_click("reset")
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

        self.buttons = window.buttons
        self.correct_color = window.correct_color

    def run(self):
        self.window_ui()
        self.menu_file()

    def close_main_window(self):
        MainWindow.close(self)

    def window_ui(self):
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # --------------------------------------------------------------------------------

    # --- read & write func ---
    def read_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                return file.readlines()

        except FileNotFoundError:
            self.close_main_window()

    def write_in_file(self, filename, written_data):
        try:
            with open(filename, "w") as file:
                file.write(written_data + "\n")

        except FileNotFoundError:
            self.close_main_window()

    # --- file handling ---
    def menu_file_load_file(self):
        file_filter = ["Text files (*.txt)", "All files (*)"]
        filters_filer = ";;".join(file_filter)

        filename = QFileDialog.getOpenFileName(self, filter=filters_filer, initialFilter=filters_filer[0])

        read_data = self.read_from_file(filename[0])[0]
        print(read_data)

    def menu_file_save_file(self):
        file_filter = ["Text files (*.txt)", "All files (*)"]
        filters_filer = ";;".join(file_filter)

        filename = QFileDialog.getSaveFileName(self, filter=filters_filer, initialFilter=filters_filer[0])[0]

        self.write_in_file(filename, str(list(self.buttons)))
        print(str(list(self.buttons)))

    def menu_file(self):
        menu_file = self.menu.addMenu("&File")
        menu_file.addSeparator()

        menu_file.addAction(self.menu_file_button_save_file)
        menu_file.addAction(self.menu_file_button_load_file)

        self.menu_file_button_save_file.triggered.connect(lambda: self.menu_file_save_file())
        self.menu_file_button_load_file.triggered.connect(lambda: self.menu_file_load_file())

        # self.setStyleSheet("background-color:rgb(230, 230, 230)")

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------


def window_handler():
    app = QApplication(sys.argv)

    window = Window()
    # window.show()
    window.run()

    main_window = MainWindow(window)
    main_window.setCentralWidget(window)
    main_window.show()
    main_window.run()

    try:
        app.exec()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


def main():
    window_handler()


if __name__ == '__main__':
    main()
