import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from widgets import PRTButton, PRTLabel, PRTCard

def main() -> int:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PRT Widgets Test")
    window.resize(360, 180)

    layout = QVBoxLayout(window)

    card = PRTCard()

    card.add_widget(PRTLabel("Primeiro Card do PRT Core"))
    card.add_widget(PRTButton("Download"))

    layout.addWidget(card)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())