"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: SettingsPage

Description:
    System configuration page allowing users to customize
    download directories, system behavior, and app settings.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,  # <--- Adicione este import
    QPushButton,
    QVBoxLayout,
)

from services.download_manager import PRTDownloadManager
from ui.pages.base_page import BasePage


class SettingsPage(BasePage):
    """System settings page."""

    def __init__(self) -> None:
        super().__init__()
        self._settings = QSettings("PRTLabs", "PRTNexus")
        self._layout = QVBoxLayout(self)

        self._configure()
        self._build_ui()
        self._load_saved_settings()

    def _configure(self) -> None:
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        # Título
        title = QLabel("Configurações do Sistema")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        # Seção 1: Downloads e Armazenamento
        sec1_title = QLabel("Downloads e Armazenamento")
        sec1_title.setStyleSheet("color: #007ACC; font-size: 14px; font-weight: bold;")
        self._layout.addWidget(sec1_title)

        lbl_path = QLabel("Pasta padrão para salvamento de cursos:")
        lbl_path.setStyleSheet("color: #CCCCCC; font-size: 13px;")
        self._layout.addWidget(lbl_path)

        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        self.input_download_path = QLineEdit()
        self.input_download_path.setPlaceholderText("Selecione a pasta de downloads...")
        self.input_download_path.setStyleSheet(
            """
            QLineEdit {
                background-color: #141416;
                border: 1px solid #28282D;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007ACC;
            }
            """
        )

        btn_browse = QPushButton("Procurar...")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet(
            """
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #24242A;
                border-color: #007ACC;
            }
            """
        )
        btn_browse.clicked.connect(self._on_browse_clicked)

        path_layout.addWidget(self.input_download_path)
        path_layout.addWidget(btn_browse)
        self._layout.addLayout(path_layout)

        self._layout.addSpacing(15)

        # Seção 2: Comportamento do Sistema
        sec2_title = QLabel("Comportamento do Sistema")
        sec2_title.setStyleSheet("color: #007ACC; font-size: 14px; font-weight: bold;")
        self._layout.addWidget(sec2_title)

        chk_style = """
            QCheckBox {
                color: #CCCCCC;
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #28282D;
                border-radius: 4px;
                background-color: #141416;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
                border-color: #007ACC;
            }
        """

        self.chk_autostart = QCheckBox("Iniciar o PRT NEXUS junto com o Windows")
        self.chk_autostart.setStyleSheet(chk_style)

        self.chk_minimize_tray = QCheckBox("Minimizar para a bandeja do sistema ao fechar")
        self.chk_minimize_tray.setStyleSheet(chk_style)

        self.chk_notifications = QCheckBox("Exibir notificação no Windows ao concluir um download")
        self.chk_notifications.setStyleSheet(chk_style)

        self._layout.addWidget(self.chk_autostart)
        self._layout.addWidget(self.chk_minimize_tray)
        self._layout.addWidget(self.chk_notifications)

        self._layout.addStretch()

        # Botão Salvar
        save_layout = QHBoxLayout()
        save_layout.addStretch()

        btn_save = QPushButton("💾 Salvar Alterações")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 22px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            """
        )
        btn_save.clicked.connect(self._on_save_clicked)
        save_layout.addWidget(btn_save)

        self._layout.addLayout(save_layout)

    def _load_saved_settings(self) -> None:
        """Carrega o caminho salvo do QSettings ou usa a pasta padrão 'downloads'."""
        default_dir = os.path.abspath("downloads")
        saved_dir = self._settings.value("download_dir", default_dir)
        self.input_download_path.setText(saved_dir)

        self.chk_autostart.setChecked(self._settings.value("autostart", False, type=bool))
        self.chk_minimize_tray.setChecked(self._settings.value("minimize_tray", True, type=bool))
        self.chk_notifications.setChecked(self._settings.value("notifications", True, type=bool))

    def _on_browse_clicked(self) -> None:
        """Abre a caixa de diálogo nativa do Windows/SO para escolher a pasta."""
        current_path = self.input_download_path.text().strip()
        if not current_path or not os.path.exists(current_path):
            current_path = os.path.abspath("downloads")

        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta para Downloads e Cursos",
            current_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if selected_dir:
            selected_dir = os.path.normpath(selected_dir)
            self.input_download_path.setText(selected_dir)

    def _on_save_clicked(self) -> None:
        """Salva as alterações no registro, atualiza o gerenciador e avisa o usuário."""
        new_path = self.input_download_path.text().strip()
        if new_path:
            os.makedirs(new_path, exist_ok=True)
            self._settings.setValue("download_dir", new_path)
            PRTDownloadManager.instance().set_download_folder(new_path)

        self._settings.setValue("autostart", self.chk_autostart.isChecked())
        self._settings.setValue("minimize_tray", self.chk_minimize_tray.isChecked())
        self._settings.setValue("notifications", self.chk_notifications.isChecked())

        # Pop-up de confirmação visual
        QMessageBox.information(
            self,
            "PRT NEXUS",
            "Configurações salvas com sucesso!"
        )
