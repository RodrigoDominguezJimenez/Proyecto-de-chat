from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication, QMainWindow)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        container = QWidget()

        layout = QVBoxLayout()
        self.lcd = QLCDNumber(self)
        layout.addWidget(self.lcd)

        slider = CustomSlider(0, 100)
        layout.addWidget(slider)
        slider.moved.connect(self.updateLcd)

        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setGeometry(300, 300, 250, 150)

    def updateLcd(self, value):
        self.lcd.display(value)


class CustomSlider(QSlider):
    # Se define una senal que emitira valores int
    moved = pyqtSignal(int)

    def __init__(self, min: int, max: int):
        super().__init__(Qt.Horizontal)
        self.setMinimum(min)
        self.setMaximum(max)

        self.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, newValue):
        # Emitir el nuevo valor usando la senal moved
        self.moved.emit(newValue)


if __name__ == '__main__':
    app = QApplication([])
    window = VentanaPrincipal()
    window.show()

    app.exec_()
