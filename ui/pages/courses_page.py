from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets import PRTCard, PRTLabel


class CoursesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        card = PRTCard("Cursos")

        card.add_widget(
            PRTLabel("Área de Cursos")
        )

        layout.addWidget(card)

        layout.addStretch()