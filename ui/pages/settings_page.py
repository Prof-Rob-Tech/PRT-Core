from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets import PRTCard, PRTLabel


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        card = PRTCard("Configurações")

        card.add_widget(
            PRTLabel("Área de Configurações")
        )

        layout.addWidget(card)

        layout.addStretch()