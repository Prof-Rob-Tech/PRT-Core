from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets import PRTCard, PRTLabel


class LicensePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        card = PRTCard("Licença")

        card.add_widget(
            PRTLabel("Área da Licença")
        )

        layout.addWidget(card)

        layout.addStretch()