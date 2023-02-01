import sys
import random
import time
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLineEdit, QLabel, QPushButton


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.red = []
        self.green = []
        self.blue = []
        self.true_color = []

        self.layout = QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.Title("Hello World")
        self.Button(self.red, self.green, self.blue)
        self.True_Color(self.true_color, self.red, self.green, self.blue)
        self.True_Button(self.true_color, self.red)
        self.Check_Button()

    def True_Color(self, true_rgb, red, green, blue):
        first_digit = random.randint(0, len(blue) - 1)
        second_digit = random.randint(0, len(blue[first_digit]) - 1)
        true_rgb += red[first_digit][second_digit], green[first_digit][second_digit], blue[first_digit][second_digit]

    def True_Button(self, true_rgb, red):
        button = QPushButton()
        button.setStyleSheet(
            f"background-color:rgb({true_rgb[0]},{true_rgb[1]},{true_rgb[2]})")
        self.layout.addWidget(button, 0, len(red))
        print(f"{true_rgb}")


    def Check_Button(self, true_rgb):
        true_rgb =


    def Button(self, red, green, blue):
        # todo: check if some colors are duplicates
        for i in range(0, 5, 1):
            red_temp = []
            green_temp = []
            blue_temp = []
            for j in range(0, 5, 1):

                red_temp.append(random.randint(0, 254))
                green_temp.append(random.randint(0, 254))
                blue_temp.append(random.randint(0, 254))

                button = QPushButton()
                button.setStyleSheet(
                    f"background-color:rgb({red_temp[j]},{green_temp[j]},{blue_temp[j]})")
                self.layout.addWidget(button, i, j)

            red.append(red_temp)
            green.append(green_temp)
            blue.append(blue_temp)

    def Title(self, title):
        self.setWindowTitle(title)

def main():
    app = QApplication(sys.argv)
    window = Window()
    # print(f"red: {window.red}")
    # print(f"true_color: {window.true_color}")

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
