import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from widgets import PRTButton


def main() -> int:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PRTButton Test")
    window.resize(360, 180)

    layout = QVBoxLayout(window)
    layout.addWidget(PRTButton("Testar botão"))

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())