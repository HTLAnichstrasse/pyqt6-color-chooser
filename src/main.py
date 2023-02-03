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
# todo: Difficulties: Easy(2|2) Medium(3|3) Hard(4|4) Impossible(5|5)
# todo: implement correct color-guess
# todo: implement try's
# todo: save game & load game


class Button(QWidget):
    def __init__(self):
        super().__init__()

        self.rgb_correct = []
        self.buttons = {}
        self.rgb = []

        self.layout = QGridLayout()

        self.window_ui()
        self.create_colors()
        self.add_button()
        self.correct_color_button()
        self.check_color_on_click()

    def window_ui(self):
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def correct_color_button(self):
        correct_color = self.correct_color()
        button = QPushButton("Target-Color")

        button.setStyleSheet(f"background-color:rgb({correct_color[0]},{correct_color[1]},{correct_color[2]})")
        button.setFixedSize((400 - 50), (200 - 50))

        font = button.font()
        font.setPointSize(18)
        button.setFont(font)

        self.layout.addWidget(button, 0, len(self.rgb[0]) + 1)

    def correct_color(self):
        self.rgb_correct = self.rgb[random.randint(0, len(self.rgb) - 1)][random.randint(0, len(self.rgb[0]) - 1)]
        return self.rgb_correct

    def check_color_on_click(self):
        for element in self.buttons:
            if self.buttons[element] == self.rgb_correct:
                element.clicked.connect(lambda: self.correct_color_clicked())
            else:
                element.clicked.connect(lambda: print(f"incorrect"))

    def correct_color_clicked(self):
        print(f"correct")

    def add_button(self):
        for x in range(0, FIELD_Y_COUNT, 1):
            for y in range(0, FIELD_X_COUNT, 1):
                button = QPushButton()
                button.setStyleSheet(
                    f"background-color:rgb({self.rgb[x][y][0]},{self.rgb[x][y][1]},{self.rgb[x][y][2]})")
                button.setFixedSize((WINDOW_WIDTH - 50) // (FIELD_X_COUNT * 2),
                                    (WINDOW_HEIGHT - 50) // FIELD_Y_COUNT)

                self.buttons[button] = self.rgb[x][y]
                self.layout.addWidget(button, x, y)

    def create_colors(self):
        for x in range(0, FIELD_Y_COUNT, 1):
            temp = []
            for y in range(0, FIELD_X_COUNT, 1):
                tmp = []
                for three_colors in range(0, 3, 1):
                    tmp.append(random.randint(0, 255))

                duplicate = self.check_duplicate_in_array(tmp)
                if duplicate:
                    y -= 1
                else:
                    temp.append(tmp)

            self.rgb.append(temp)

    def check_duplicate_in_array(self, arr):
        for element in self.rgb:
            for e in element:
                if arr != e:
                    return 0
                else:
                    return 1


def main():
    app = QApplication(sys.argv)

    window = Button()
    window.show()

    try:
        app.exec()
    except KeyboardInterrupt:
        print("Quited Game, Interrupt")


if __name__ == '__main__':
    main()
