"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: CoursesPage

Description:
    Courses library page featuring a grid of course cards
    with progress tracking and action buttons.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.pages.base_page import BasePage


class PRTCourseCard(QWidget):
    """Card widget representing an individual course."""

    def __init__(
        self,
        title: str,
        category: str,
        progress: int,
        total_lessons: int,
        completed_lessons: int,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("PRTCourseCard")
        self.setStyleSheet(
            """
            QWidget#PRTCourseCard {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 10px;
            }
            QWidget#PRTCourseCard:hover {
                border-color: #007ACC;
            }
            QLabel#TitleLabel {
                color: #FFFFFF;
                font-size: 15px;
                font-weight: bold;
            }
            QLabel#CategoryLabel {
                color: #007ACC;
                font-size: 11px;
                font-weight: bold;
            }
            QLabel#ProgressText {
                color: #8E8E93;
                font-size: 12px;
            }
            QProgressBar {
                background-color: #1F1F23;
                border: none;
                border-radius: 3px;
                height: 6px;
            }
            QProgressBar::chunk {
                background-color: #34C759;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #007ACC;
                border-color: #007ACC;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Categoria / Tag
        cat_lbl = QLabel(category.upper())
        cat_lbl.setObjectName("CategoryLabel")
        layout.addWidget(cat_lbl)

        # Título
        title_lbl = QLabel(title)
        title_lbl.setObjectName("TitleLabel")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        # Barra de Progresso
        pbar = QProgressBar()
        pbar.setValue(progress)
        pbar.setTextVisible(False)
        layout.addWidget(pbar)

        # Aulas + Botão de Ação
        bottom_layout = QHBoxLayout()

        prog_text = QLabel(f"{completed_lessons}/{total_lessons} aulas")
        prog_text.setObjectName("ProgressText")

        btn_open = QPushButton("▶ Acessar")
        btn_open.setCursor(Qt.PointingHandCursor)

        bottom_layout.addWidget(prog_text)
        bottom_layout.addStretch()
        bottom_layout.addWidget(btn_open)

        layout.addLayout(bottom_layout)


class CoursesPage(BasePage):
    """Courses library page with grid layout."""

    def __init__(self) -> None:
        super().__init__()

        self._layout = QVBoxLayout(self)

        self._configure()
        self._build_ui()

    def _configure(self) -> None:
        """Configure page margins and spacing."""
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        """Build the user interface."""

        # Título
        title = QLabel("Minha Biblioteca de Cursos")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        # Grade de Cursos (2 colunas)
        grid = QGridLayout()
        grid.setSpacing(15)

        mock_courses = [
            ("Python Impressionador - Completo", "Python", 75, 120, 90),
            ("Formação Dev Full Stack", "Web Dev", 40, 200, 80),
            ("Automações com PySide6 e Qt", "Interface", 100, 45, 45),
            ("Engenharia de Prompt Avançada", "IA / LLM", 20, 50, 10),
        ]

        for index, (c_title, c_cat, c_prog, c_tot, c_comp) in enumerate(
            mock_courses
        ):
            card = PRTCourseCard(c_title, c_cat, c_prog, c_tot, c_comp)
            row = index // 2
            col = index % 2
            grid.addWidget(card, row, col)

        self._layout.addLayout(grid)
        self._layout.addStretch()