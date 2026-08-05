"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: DownloadsPage

Description:
    Downloads management UI with URL inputs, real-time progress,
    pause, resume, and cancellation buttons.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QClipboard, QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.download_manager import PRTDownloadItem, PRTDownloadManager
from ui.pages.base_page import BasePage


class DownloadsPage(BasePage):
    """Página de Gerenciamento de Downloads."""

    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._row_map = {}

        self._configure()
        self._build_ui()
        self._connect_signals()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._check_clipboard_for_url()

    def _configure(self) -> None:
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        # Título
        title = QLabel("Gerenciador de Downloads")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        # Entrada de URL
        input_container = QFrame()
        input_container.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #28282D;
                border-radius: 8px;
            }
            """
        )
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(10, 8, 10, 8)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole a URL do vídeo/curso aqui (YouTube, Vimeo, etc)...")
        self.url_input.setStyleSheet(
            """
            QLineEdit {
                background-color: transparent;
                border: none;
                color: #FFFFFF;
                font-size: 13px;
            }
            """
        )
        self.url_input.returnPressed.connect(self._add_download)

        btn_add = QPushButton("📥 Baixar")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            """
        )
        btn_add.clicked.connect(self._add_download)

        input_layout.addWidget(self.url_input)
        input_layout.addWidget(btn_add)
        self._layout.addWidget(input_container)

        # Barra de Ações Rápidas
        actions_layout = QHBoxLayout()

        btn_open_folder = QPushButton("📂 Abrir Pasta")
        btn_open_folder.setCursor(Qt.PointingHandCursor)
        btn_open_folder.setStyleSheet(
            """
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #24242A;
                border-color: #007ACC;
            }
            """
        )
        btn_open_folder.clicked.connect(self._open_downloads_folder)

        btn_clear = QPushButton("🧹 Limpar Concluídos")
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet(
            """
            QPushButton {
                background-color: #1A1A1E;
                color: #8E8E93;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #24242A;
                color: #FFFFFF;
            }
            """
        )
        btn_clear.clicked.connect(self._clear_completed)

        actions_layout.addWidget(btn_open_folder)
        actions_layout.addWidget(btn_clear)
        actions_layout.addStretch()
        self._layout.addLayout(actions_layout)

        # Tabela de Downloads
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nome / Curso", "Tamanho", "Progresso", "Velocidade", "Status", "Ações"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
                gridline-color: #1F1F23;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #1A1A1E;
                color: #8E8E93;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            """
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Fixed)

        self.table.setColumnWidth(2, 140)
        self.table.setColumnWidth(5, 90)

        self._layout.addWidget(self.table)
        self._reload_table()

    def _connect_signals(self) -> None:
        manager = PRTDownloadManager.instance()
        manager.download_added.connect(self._add_row)
        manager.progress_updated.connect(self._update_row_progress)
        manager.title_updated.connect(self._update_row_title)
        manager.size_updated.connect(self._update_row_size)
        manager.cleared_signal.connect(self._reload_table)

    def _check_clipboard_for_url(self) -> None:
        clipboard = QGuiApplication.clipboard()
        text = clipboard.text().strip()
        if (text.startswith("http://") or text.startswith("https://")) and not self.url_input.text():
            self.url_input.setText(text)

    def _add_download(self) -> None:
        url = self.url_input.text().strip()
        if url:
            PRTDownloadManager.instance().add_download(url)
            self.url_input.clear()

    def _reload_table(self) -> None:
        self.table.setRowCount(0)
        self._row_map.clear()
        for item in PRTDownloadManager.instance().downloads:
            self._add_row(item)

    def _add_row(self, item: PRTDownloadItem) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._row_map[item.id] = row

        # Nome
        name_item = QTableWidgetItem(item.name)
        name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)
        self.table.setItem(row, 0, name_item)

        # Tamanho
        size_item = QTableWidgetItem(item.size_str)
        size_item.setFlags(size_item.flags() ^ Qt.ItemIsEditable)
        self.table.setItem(row, 1, size_item)

        # Progresso (Barra)
        pbar = QProgressBar()
        pbar.setValue(item.progress)
        pbar.setStyleSheet(
            """
            QProgressBar {
                background-color: #1F1F23;
                border: none;
                border-radius: 4px;
                text-align: center;
                color: #FFFFFF;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 4px;
            }
            """
        )
        self.table.setCellWidget(row, 2, pbar)

        # Velocidade
        speed_item = QTableWidgetItem(item.speed)
        speed_item.setFlags(speed_item.flags() ^ Qt.ItemIsEditable)
        self.table.setItem(row, 3, speed_item)

        # Status
        status_item = QTableWidgetItem(item.status)
        status_item.setFlags(status_item.flags() ^ Qt.ItemIsEditable)
        self.table.setItem(row, 4, status_item)

        # Container de Ações (Pausar/Retomar + Cancelar)
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(4)
        actions_layout.setAlignment(Qt.AlignCenter)

        btn_toggle = QPushButton("⏸️" if item.status == "Baixando" else "▶")
        btn_toggle.setFixedSize(26, 26)
        btn_toggle.setCursor(Qt.PointingHandCursor)
        btn_toggle.setStyleSheet("QPushButton { background: #1F1F24; border: none; border-radius: 4px; color: white; } QPushButton:hover { background: #007ACC; }")
        btn_toggle.clicked.connect(lambda _, d_id=item.id: self._on_toggle_click(d_id))

        btn_cancel = QPushButton("❌")
        btn_cancel.setFixedSize(26, 26)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("QPushButton { background: #1F1F24; border: none; border-radius: 4px; color: white; } QPushButton:hover { background: #D32F2F; }")
        btn_cancel.clicked.connect(lambda _, d_id=item.id: PRTDownloadManager.instance().cancel_download(d_id))

        actions_layout.addWidget(btn_toggle)
        actions_layout.addWidget(btn_cancel)
        self.table.setCellWidget(row, 5, actions_widget)

    def _on_toggle_click(self, download_id: str) -> None:
        manager = PRTDownloadManager.instance()
        for item in manager.downloads:
            if item.id == download_id:
                if item.status == "Baixando":
                    manager.pause_download(download_id)
                else:
                    manager.resume_download(download_id)
                break

    def _update_row_progress(self, download_id: str, progress: int, speed: str, status: str) -> None:
        if download_id in self._row_map:
            row = self._row_map[download_id]
            pbar = self.table.cellWidget(row, 2)
            if pbar:
                pbar.setValue(progress)

            speed_item = self.table.item(row, 3)
            if speed_item:
                speed_item.setText(speed)

            status_item = self.table.item(row, 4)
            if status_item:
                status_item.setText(status)

            # Atualiza o botão de Ação
            actions_widget = self.table.cellWidget(row, 5)
            if actions_widget:
                btn_toggle = actions_widget.layout().itemAt(0).widget()
                if btn_toggle:
                    btn_toggle.setText("⏸️" if status == "Baixando" else "▶")

    def _update_row_title(self, download_id: str, title: str) -> None:
        if download_id in self._row_map:
            row = self._row_map[download_id]
            item = self.table.item(row, 0)
            if item:
                item.setText(title)

    def _update_row_size(self, download_id: str, size_str: str) -> None:
        if download_id in self._row_map:
            row = self._row_map[download_id]
            item = self.table.item(row, 1)
            if item:
                item.setText(size_str)

    def _open_downloads_folder(self) -> None:
        folder_path = PRTDownloadManager.instance().get_download_folder()
        os.makedirs(folder_path, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

    def _clear_completed(self) -> None:
        PRTDownloadManager.instance().clear_completed()