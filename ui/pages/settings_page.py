"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: SettingsPage

Description:
    Settings page for PRT NEXUS. Supports visual folder selection,
    explicit save action with visual feedback, and persistence.

Developer..: Prof Rob Tech
===========================================================
"""

import json
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.download_manager import PRTDownloadManager


class SettingsPage(QWidget):
    """Página de Configurações do Sistema."""

    def __init__(self) -> None:
        super().__init__()
        self._config_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
        )
        self._pending_folder = ""

        self._build_ui()
        self._load_saved_settings()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Título da Página
        lbl_header = QLabel("Configurações do Sistema")
        lbl_header.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_header)

        # Card: Diretório de Downloads
        card_downloads = QFrame()
        card_downloads.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            """
        )
        card_layout = QVBoxLayout(card_downloads)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        lbl_section_dl = QLabel("📁 Diretório de Downloads")
        lbl_section_dl.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold; border: none;")
        card_layout.addWidget(lbl_section_dl)

        lbl_desc = QLabel("Escolha a pasta padrão onde os vídeos e aulas baixados serão salvos:")
        lbl_desc.setStyleSheet("color: #8E8E93; font-size: 12px; border: none;")
        card_layout.addWidget(lbl_desc)

        # Seletor de Caminho
        selector_layout = QHBoxLayout()
        selector_layout.setSpacing(10)

        self.txt_path = QLineEdit()
        self.txt_path.setReadOnly(True)
        current_folder = PRTDownloadManager.instance().get_download_folder()
        self.txt_path.setText(current_folder)
        self._pending_folder = current_folder
        self.txt_path.setStyleSheet(
            """
            QLineEdit {
                background-color: #1C1C1F;
                border: 1px solid #28282D;
                border-radius: 6px;
                color: #A0A0A5;
                padding: 8px 12px;
                font-size: 12px;
            }
            """
        )
        selector_layout.addWidget(self.txt_path)

        self.btn_browse = QPushButton("Procurar...")
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.setStyleSheet(
            """
            QPushButton {
                background-color: #28282D;
                color: #FFFFFF;
                border: 1px solid #3A3A40;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3A3A40;
            }
            """
        )
        self.btn_browse.clicked.connect(self._select_folder)
        selector_layout.addWidget(self.btn_browse)

        card_layout.addLayout(selector_layout)

        # Linha inferior de ações (Botão Salvar + Feedback)
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(0, 5, 0, 0)

        self.lbl_feedback = QLabel("")
        self.lbl_feedback.setStyleSheet("color: #34C759; font-size: 12px; font-weight: bold; border: none;")
        action_layout.addWidget(self.lbl_feedback)

        action_layout.addStretch()

        self.btn_save = QPushButton("💾 Salvar Alterações")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
            """
        )
        self.btn_save.clicked.connect(self._apply_and_save)
        action_layout.addWidget(self.btn_save)

        card_layout.addLayout(action_layout)
        layout.addWidget(card_downloads)

        # Card: Informações do Aplicativo
        card_info = QFrame()
        card_info.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            """
        )
        info_layout = QVBoxLayout(card_info)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(10)

        lbl_info_title = QLabel("ℹ️ Sobre o PRT NEXUS")
        lbl_info_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold; border: none;")
        info_layout.addWidget(lbl_info_title)

        lbl_version = QLabel(
            "Versão: 1.0.0 Core\n"
            "Desenvolvido por: Prof Rob Tech (PRT Labs)\n"
            "Motor de Download: yt-dlp Integrado\n"
            "Interface: PySide6 Qt Multimedia UI"
        )
        lbl_version.setStyleSheet("color: #8E8E93; font-size: 12px; border: none; line-height: 1.6;")
        info_layout.addWidget(lbl_version)

        layout.addWidget(card_info)
        layout.addStretch()

    def _select_folder(self) -> None:
        """Abre a caixa de diálogo para pré-seleção do diretório."""
        current_dir = self._pending_folder or PRTDownloadManager.instance().get_download_folder()
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta de Downloads",
            current_dir,
        )

        if selected_dir:
            self._pending_folder = os.path.abspath(selected_dir)
            self.txt_path.setText(self._pending_folder)

    def _apply_and_save(self) -> None:
        """Aplica as alterações no sistema, salva no JSON e dá feedback visual."""
        if not self._pending_folder:
            return

        # Aplica no Gerenciador Ativo
        PRTDownloadManager.instance().set_download_folder(self._pending_folder)

        # Salva no arquivo de configuração
        self._save_settings(self._pending_folder)

        # Exibe mensagem de confirmação por 3 segundos
        self.lbl_feedback.setText("✅ Configurações salvas com sucesso!")
        QTimer.singleShot(3000, lambda: self.lbl_feedback.setText(""))

    def _save_settings(self, download_path: str) -> None:
        """Persiste o caminho em config.json."""
        try:
            data = {"download_folder": download_path}
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def _load_saved_settings(self) -> None:
        """Carrega a configuração salva ao iniciar a tela."""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    saved_path = data.get("download_folder")
                    if saved_path and os.path.exists(saved_path):
                        self._pending_folder = saved_path
                        self.txt_path.setText(saved_path)
                        PRTDownloadManager.instance().set_download_folder(saved_path)
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")