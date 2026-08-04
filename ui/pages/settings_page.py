"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: SettingsPage

Description:
    Application settings page for managing download paths,
    system preferences, and notifications.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from ui.pages.base_page import BasePage


class SettingsPage(BasePage):
    """Settings page for user preferences."""

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
        title = QLabel("Configurações do Sistema")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        group_style = """
            QGroupBox {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 10px;
                margin-top: 10px;
                padding: 20px 15px 15px 15px;
                color: #007ACC;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #1A1A1E;
                border: 1px solid #28282D;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007ACC;
            }
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #24242A;
                border-color: #007ACC;
            }
            QCheckBox {
                color: #FFFFFF;
                font-size: 13px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #28282D;
                background-color: #1A1A1E;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
                border-color: #007ACC;
            }
        """

        # --- Grupo 1: Downloads & Armazenamento ---
        storage_box = QGroupBox("Downloads & Armazenamento")
        storage_box.setStyleSheet(group_style)
        storage_layout = QVBoxLayout(storage_box)
        storage_layout.setSpacing(12)

        path_label = QLabel("Pasta padrão para salvamento de cursos:")
        path_layout = QHBoxLayout()

        self.path_input = QLineEdit("C:\\Users\\robso\\Downloads\\PRT-Nexus")
        btn_browse = QPushButton("Procurar...")
        btn_browse.setCursor(Qt.PointingHandCursor)

        path_layout.addWidget(self.path_input, stretch=1)
        path_layout.addWidget(btn_browse)

        storage_layout.addWidget(path_label)
        storage_layout.addLayout(path_layout)

        # --- Grupo 2: Sistema & Comportamento ---
        system_box = QGroupBox("Comportamento do Sistema")
        system_box.setStyleSheet(group_style)
        system_layout = QVBoxLayout(system_box)
        system_layout.setSpacing(14)

        chk_autostart = QCheckBox("Iniciar o PRT NEXUS junto com o Windows")
        chk_tray = QCheckBox("Minimizar para a bandeja do sistema ao fechar")
        chk_notify = QCheckBox("Exibir notificação no Windows ao concluir um download")

        chk_tray.setChecked(True)
        chk_notify.setChecked(True)

        system_layout.addWidget(chk_autostart)
        system_layout.addWidget(chk_tray)
        system_layout.addWidget(chk_notify)

        # Adiciona os grupos na tela
        self._layout.addWidget(storage_box)
        self._layout.addWidget(system_box)

        # Botão de Salvar no Rodapé
        save_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Salvar Alterações")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            """
        )
        save_layout.addStretch()
        save_layout.addWidget(btn_save)

        self._layout.addLayout(save_layout)
        self._layout.addStretch()