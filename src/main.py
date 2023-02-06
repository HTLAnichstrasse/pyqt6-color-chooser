import sys
import random

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLineEdit, QLabel, QPushButton, \
    QMainWindow, QFileDialog, QVBoxLayout, QMenu, QMenuBar, QToolBar, QStatusBar

# constants
DIFFICULTIES = {
    "easy": 2,
    "medium": 3,
    "hard": 4,
    "impossible": 5
}
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800


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
        self.navbar()
        self.create_guess_buttons()
        self.get_correct_color()
        self.create_correct_button()
        self.create_tries_label()
        self.check_clicked_button()

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
        self.layout.addWidget(self.tries_label, 1, self.active_difficulty + 1)

    def update_tries_on_click(self, _type):
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

    # --- Menu ---
    # todo:
    def navbar(self):
        # button = QPushButton("Hello World")
        # menu_bar = QToolBar(self)
        # self.addToolBar(menu_bar)
        # self.layout.addWidget(menu_bar, 0, 0)
        print("#")

    # --------------------------------------------------------------------------------


def main():
    app = QApplication(sys.argv)

    window = Window()
    main_window = QMainWindow()
    main_window.setCentralWidget(window)
    toolbar = QToolBar("Hi")
    button_action = QAction("Your button", main_window)
    button_action.setStatusTip("This is your button")
    button_action.triggered.connect(lambda: print(f"test"))
    toolbar.addAction(button_action)
    main_window.addToolBar(toolbar)
    main_window.show()
    window.run()

    try:
        app.exec()
    except KeyboardInterrupt:
        print("Quited Game, Interrupt")


if __name__ == '__main__':
    main()
