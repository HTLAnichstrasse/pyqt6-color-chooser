import sys
import random
import math
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLineEdit, QLabel, QPushButton, \
    QMainWindow, QFileDialog, QVBoxLayout, QMenu, QMenuBar

# constants
FIELD_X_COUNT = 3
FIELD_Y_COUNT = 3
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800


# todo: convert rgb & buttons from list to dict
# lugas: eine color-Funktion, die für EINEN button EINE color erstellt => & dabei schaut, ob de color schon mal in an
# anderen element vom dict ist
# todo: Difficulties: Easy(2|2) Medium(3|3) Hard(4|4) Impossible(5|5)
# todo: implement correct color-guess
# todo: implement try's
# todo: save game & load game


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.buttons = {}
        self.correct_color = []

        self.run()

    def run(self):
        self.window_ui()
        self.create_guess_buttons()
        self.get_correct_color()
        self.create_correct_button()
        self.check_clicked_button()

    def window_ui(self):
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # --------------------------------------------------------------------------------
    # --- guesser button ---
    def check_for_color_duplicates(self, color):
        for ele in self.buttons:
            if self.buttons[ele] == color:
                color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                self.check_for_color_duplicates(color)
                print("duplicate")

    def create_color_for_button(self, button):
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.check_for_color_duplicates(color)
        self.buttons[button] = color

    def create_single_guess_button(self, x, y):
        button = QPushButton()
        self.create_color_for_button(button)

        button.setStyleSheet(
            f"background-color:rgb({self.buttons[button][0]}, {self.buttons[button][1]}, {self.buttons[button][2]})")
        button.setFixedSize((WINDOW_WIDTH - 50) // (FIELD_X_COUNT * 2), (WINDOW_HEIGHT - 50) // FIELD_Y_COUNT)

        self.layout.addWidget(button, x, y)

    def create_guess_buttons(self):
        # button_type = "guess_button"
        for x in range(FIELD_X_COUNT):
            for y in range(FIELD_Y_COUNT):
                self.create_single_guess_button(x, y)

    # --- check if clicked button is correct or incorrect ---
    def get_correct_color(self):
        self.correct_color = random.choice(list(self.buttons.values()))

    def check_clicked_button(self):
        # self.correct_color = random.choice(list(self.buttons.values()))
        for ele in self.buttons:
            if self.buttons[ele] == self.correct_color:
                ele.clicked.connect(lambda: print("correct"))
            else:
                ele.clicked.connect(lambda: print("incorrect"))

    # --- create correct button ---

    def create_correct_button(self):
        button = QPushButton("True Color")

        button.setStyleSheet(
            f"background-color:rgb({self.correct_color[0]}, {self.correct_color[1]}, {self.correct_color[2]})")
        button.setFixedSize((400 - 50), (200 - 50))

        font = button.font()
        font.setPointSize(18)
        button.setFont(font)

        self.layout.addWidget(button, 0, FIELD_X_COUNT + 1)

    # --------------------------------------------------------------------------------


def main():
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    try:
        app.exec()
    except KeyboardInterrupt:
        print("Quited Game, Interrupt")


if __name__ == '__main__':
    main()
