"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: DownloadsPage

Description:
    Interactive downloads management page connected to
    real-time progress updates from PRTDownloadManager.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Dict
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from services.download_manager import PRTDownloadItem, PRTDownloadManager
from ui.pages.base_page import BasePage
from widgets.new_download_dialog import PRTNewDownloadDialog


class DownloadsPage(BasePage):
    """Downloads management page with live simulation."""

    def __init__(self) -> None:
        super().__init__()

        self._row_map: Dict[str, int] = {}  # Mapeia ID do download para a linha da tabela
        self._layout = QVBoxLayout(self)

        self._configure()
        self._build_ui()
        self._connect_manager()

    def _configure(self) -> None:
        """Configure page margins and spacing."""
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        """Build the user interface."""

        title = QLabel("Gerenciador de Downloads")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)

        button_style = """
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
            QPushButton#Primary {
                background-color: #007ACC;
                border-color: #007ACC;
            }
            QPushButton#Primary:hover {
                background-color: #005A9E;
            }
        """

        btn_new = QPushButton("⚡ Novo Download")
        btn_new.setObjectName("Primary")
        btn_new.setCursor(Qt.PointingHandCursor)
        btn_new.setStyleSheet(button_style)
        btn_new.clicked.connect(self._open_new_download_dialog)

        btn_pause = QPushButton("⏸ Pausar Tudo")
        btn_pause.setStyleSheet(button_style)

        btn_resume = QPushButton("▶ Retomar Tudo")
        btn_resume.setStyleSheet(button_style)

        btn_clear = QPushButton("🗑 Limpar Concluídos")
        btn_clear.setStyleSheet(button_style)

        toolbar_layout.addWidget(btn_new)
        toolbar_layout.addWidget(btn_pause)
        toolbar_layout.addWidget(btn_resume)
        toolbar_layout.addWidget(btn_clear)
        toolbar_layout.addStretch()

        self._layout.addLayout(toolbar_layout)

        # Tabela
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Nome do Arquivo", "Tamanho", "Status", "Progresso", "Velocidade"]
        )

        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 200)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: #141416;
                color: #FFFFFF;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #1A1A1E;
                color: #8E8E93;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #26262B;
                padding: 10px;
                text-align: left;
            }
            QTableWidget::item {
                padding: 5px 10px;
                border-bottom: 1px solid #1A1A1E;
            }
            QTableWidget::item:selected {
                background-color: #1F2937;
            }
            """
        )
        self._layout.addWidget(self.table)

        # Carrega os itens do gerenciador
        self._load_initial_downloads()

    def _connect_manager(self) -> None:
        """Conecta com os sinais do gerenciador de downloads."""
        manager = PRTDownloadManager.instance()
        manager.download_added.connect(self._on_download_added)
        manager.progress_updated.connect(self._on_progress_updated)

    def _load_initial_downloads(self) -> None:
        """Insere os downloads existentes na tabela."""
        for item in PRTDownloadManager.instance().downloads:
            self._add_item_to_table(item)

    def _open_new_download_dialog(self) -> None:
        dialog = PRTNewDownloadDialog(self)
        if dialog.exec():
            url = dialog.get_url()
            if url:
                PRTDownloadManager.instance().add_download(url)

    def _add_item_to_table(self, item: PRTDownloadItem) -> None:
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        self._row_map[item.id] = row_idx

        self.table.setItem(row_idx, 0, QTableWidgetItem(item.name))
        self.table.setItem(row_idx, 1, QTableWidgetItem(item.size_str))

        status_item = QTableWidgetItem(item.status)
        self._style_status(status_item, item.status)
        self.table.setItem(row_idx, 2, status_item)

        progress_bar = QProgressBar()
        progress_bar.setValue(item.progress)
        progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #1F1F23;
                border: none;
                border-radius: 4px;
                text-align: center;
                color: white;
                font-size: 11px;
                margin: 5px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 4px;
            }
            """
        )
        self.table.setCellWidget(row_idx, 3, progress_bar)
        self.table.setItem(row_idx, 4, QTableWidgetItem(item.speed))

    def _on_download_added(self, item: PRTDownloadItem) -> None:
        self._add_item_to_table(item)

    def _on_progress_updated(
        self, download_id: str, progress: int, speed: str, status: str
    ) -> None:
        if download_id not in self._row_map:
            return

        row = self._row_map[download_id]

        # Atualiza Status
        status_item = self.table.item(row, 2)
        if status_item:
            status_item.setText(status)
            self._style_status(status_item, status)

        # Atualiza Barra de Progresso
        pbar = self.table.cellWidget(row, 3)
        if isinstance(pbar, QProgressBar):
            pbar.setValue(progress)

        # Atualiza Velocidade
        speed_item = self.table.item(row, 4)
        if speed_item:
            speed_item.setText(speed)

    def _style_status(self, item: QTableWidgetItem, status: str) -> None:
        if status == "Concluído":
            item.setForeground(Qt.GlobalColor.green)
        elif status == "Baixando":
            item.setForeground(Qt.GlobalColor.cyan)
        else:
            item.setForeground(Qt.GlobalColor.gray)