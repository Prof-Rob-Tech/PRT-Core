from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets import PRTCard, PRTLabel


class DownloadsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        card = PRTCard("Downloads")

        card.add_widget(
            PRTLabel("Área de Downloads")
        )

        layout.addWidget(card)

        layout.addStretch()