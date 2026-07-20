import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from widgets import PRTButton, PRTLabel


def main() -> int:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PRT Widgets Test")
    window.resize(360, 180)

    layout = QVBoxLayout(window)

    layout.addWidget(PRTLabel("Primeiros widgets do PRT Core"))
    layout.addWidget(PRTButton("Testar botão"))

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())