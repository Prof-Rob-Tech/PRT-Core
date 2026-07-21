from PySide6.QtWidgets import QGridLayout, QWidget

from widgets import PRTStatCard


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        layout.addWidget(
            PRTStatCard(
                "Downloads",
                "152",
                "Arquivos baixados",
            ),
            0,
            0,
        )

        layout.addWidget(
            PRTStatCard(
                "Cursos",
                "48",
                "Disponíveis",
            ),
            0,
            1,
        )

        layout.addWidget(
            PRTStatCard(
                "Licença",
                "Ativa",
                "Status",
            ),
            1,
            0,
        )

        layout.addWidget(
            PRTStatCard(
                "Atualizações",
                "3",
                "Pendentes",
            ),
            1,
            1,
        )