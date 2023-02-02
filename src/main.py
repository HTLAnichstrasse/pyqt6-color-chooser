import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLineEdit, QLabel, QPushButton, QMainWindow

# constants
FIELD_X_COUNT = 3
FIELD_Y_COUNT = 3
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.rgb_correct = []
        self.rgb = []

        self.layout = QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setFixedWidth(800)
        self.setFixedHeight(700)
        self.setLayout(self.layout)

        self.main_window_ui()
        self.create_colors()
        self.add_button()
        self.correct_color()

    def main_window_ui(self):
        self.setWindowTitle("Color Chooser")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def correct_color(self):
        self.rgb_correct = self.rgb[random.randint(0, len(self.rgb) - 1)][random.randint(0, len(self.rgb[0]) - 1)]
        return self.rgb_correct

    def add_button(self):
        for x in range(0, FIELD_Y_COUNT, 1):
            for y in range(0, FIELD_X_COUNT, 1):
                button = QPushButton()
                button.setStyleSheet(
                    f"background-color:rgb({self.rgb[x][y][0]},{self.rgb[x][y][1]},{self.rgb[x][y][2]})")
                button.setFixedHeight(WINDOW_WIDTH // FIELD_X_COUNT)
                button.setFixedHeight(WINDOW_HEIGHT // FIELD_Y_COUNT)

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
    Window().show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
