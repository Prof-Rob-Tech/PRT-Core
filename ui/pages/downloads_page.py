"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: DownloadsPage

Description:
    Complete Download Manager interface page for PRT NEXUS.
    Includes URL input, quality dropdown selector, active downloads table,
    progress bars, control actions, and real-time manager binding.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
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


class DownloadsPage(QWidget):
    """Página principal do gerenciador de downloads."""

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._connect_signals()
        self._reload_table()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Cabeçalho
        lbl_header = QLabel("Gerenciador de Downloads")
        lbl_header.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_header)

        # 1. Painel de Adicionar Download (URL + Qualidade + Botão)
        input_card = QFrame()
        input_card.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            """
        )
        input_layout = QHBoxLayout(input_card)
        input_layout.setContentsMargins(15, 12, 15, 12)
        input_layout.setSpacing(10)

        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("Cole o link do vídeo ou aula aqui (YouTube, etc.)...")
        self.txt_url.setStyleSheet(
            """
            QLineEdit {
                background-color: #1C1C1F;
                color: #FFFFFF;
                border: 1px solid #26262B;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
            """
        )
        input_layout.addWidget(self.txt_url, stretch=4)

        # Seletor de Qualidade
        self.combo_quality = QComboBox()
        self.combo_quality.addItems([
            "🎬 Melhor (1080p+)",
            "📺 HD (720p)",
            "📱 SD (480p)",
            "🎵 Apenas Áudio (MP3)"
        ])
        self.combo_quality.setStyleSheet(
            """
            QComboBox {
                background-color: #1C1C1F;
                color: #FFFFFF;
                border: 1px solid #26262B;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1C1C1F;
                color: #FFFFFF;
                selection-background-color: #007ACC;
            }
            """
        )
        input_layout.addWidget(self.combo_quality, stretch=2)

        # Botão Adicionar
        btn_add = QPushButton("📥 Baixar")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
            """
        )
        btn_add.clicked.connect(self._on_add_clicked)
        input_layout.addWidget(btn_add)

        layout.addWidget(input_card)

        # 2. Barra de Ferramentas / Controles Globais
        controls_layout = QHBoxLayout()

        btn_pause_all = QPushButton("⏸️ Pausar Todos")
        btn_pause_all.setStyleSheet(self._button_style("#26262B", "#323238"))
        btn_pause_all.clicked.connect(lambda: PRTDownloadManager.instance().pause_all())

        btn_resume_all = QPushButton("▶️ Retomar Todos")
        btn_resume_all.setStyleSheet(self._button_style("#26262B", "#323238"))
        btn_resume_all.clicked.connect(lambda: PRTDownloadManager.instance().resume_all())

        btn_clear_completed = QPushButton("🧹 Limpar Concluídos")
        btn_clear_completed.setStyleSheet(self._button_style("#26262B", "#323238"))
        btn_clear_completed.clicked.connect(lambda: PRTDownloadManager.instance().clear_completed())

        controls_layout.addWidget(btn_pause_all)
        controls_layout.addWidget(btn_resume_all)
        controls_layout.addStretch()
        controls_layout.addWidget(btn_clear_completed)

        layout.addLayout(controls_layout)

        # 3. Tabela de Downloads
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título / Conteúdo", "Qualidade", "Tamanho", "Progresso", "Velocidade", "Status", "Ações"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)  # Oculta ID interno

        # Estilo Tabela Dark
        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: #141416;
                color: #FFFFFF;
                border: 1px solid #26262B;
                border-radius: 8px;
                gridline-color: #1C1C1F;
            }
            QHeaderView::section {
                background-color: #1C1C1F;
                color: #8E8E93;
                font-weight: bold;
                border: none;
                padding: 8px;
                font-size: 11px;
            }
            """
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 160)
        self.table.setColumnWidth(7, 100)

        layout.addWidget(self.table)

    def _button_style(self, bg_color: str, hover_color: str) -> str:
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def _connect_signals(self) -> None:
        mgr = PRTDownloadManager.instance()
        mgr.download_added.connect(self._on_download_added)
        mgr.progress_updated.connect(self._on_progress_updated)
        mgr.title_updated.connect(self._on_title_updated)
        mgr.size_updated.connect(self._on_size_updated)
        mgr.cleared_signal.connect(self._reload_table)

    def _on_add_clicked(self) -> None:
        url = self.txt_url.text().strip()
        if not url:
            return

        selected_text = self.combo_quality.currentText()
        quality_key = "best"
        if "720p" in selected_text:
            quality_key = "720p"
        elif "480p" in selected_text:
            quality_key = "480p"
        elif "MP3" in selected_text:
            quality_key = "mp3"

        PRTDownloadManager.instance().add_download(url, quality=quality_key)
        self.txt_url.clear()

    @Slot(object)
    def _on_download_added(self, item: PRTDownloadItem) -> None:
        self._add_row(item)

    def _add_row(self, item: PRTDownloadItem) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)

        # ID
        self.table.setItem(row, 0, QTableWidgetItem(item.id))

        # Nome
        self.table.setItem(row, 1, QTableWidgetItem(item.name))

        # Qualidade Formatada
        qual_display = item.quality.upper() if item.quality != "best" else "MAX"
        self.table.setItem(row, 2, QTableWidgetItem(qual_display))

        # Tamanho
        self.table.setItem(row, 3, QTableWidgetItem(item.size_str))

        # Progresso (ProgressBar Embutida)
        pbar = QProgressBar()
        pbar.setValue(item.progress)
        pbar.setFixedHeight(12)
        pbar.setTextVisible(False)
        pbar.setStyleSheet(
            """
            QProgressBar {
                background-color: #1C1C1F;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 4px;
            }
            """
        )
        self.table.setCellWidget(row, 4, pbar)

        # Velocidade
        self.table.setItem(row, 5, QTableWidgetItem(item.speed))

        # Status
        self.table.setItem(row, 6, QTableWidgetItem(item.status))

        # Ações (Botão Cancelar)
        btn_cancel = QPushButton("❌")
        btn_cancel.setToolTip("Cancelar Download")
        btn_cancel.setStyleSheet("background: transparent; border: none; font-size: 12px;")
        btn_cancel.clicked.connect(lambda _, d_id=item.id: PRTDownloadManager.instance().cancel_download(d_id))

        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.addWidget(btn_cancel)

        self.table.setCellWidget(row, 7, action_widget)

    def _find_row_by_id(self, download_id: str) -> int:
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text() == download_id:
                return row
        return -1

    @Slot(str, int, str, str)
    def _on_progress_updated(self, download_id: str, progress: int, speed: str, status: str) -> None:
        row = self._find_row_by_id(download_id)
        if row != -1:
            pbar = self.table.cellWidget(row, 4)
            if isinstance(pbar, QProgressBar):
                pbar.setValue(progress)

            self.table.item(row, 5).setText(speed)
            self.table.item(row, 6).setText(status)

    @Slot(str, str)
    def _on_title_updated(self, download_id: str, title: str) -> None:
        row = self._find_row_by_id(download_id)
        if row != -1:
            self.table.item(row, 1).setText(title)

    @Slot(str, str)
    def _on_size_updated(self, download_id: str, size_str: str) -> None:
        row = self._find_row_by_id(download_id)
        if row != -1:
            self.table.item(row, 3).setText(size_str)

    def _reload_table(self) -> None:
        self.table.setRowCount(0)
        mgr = PRTDownloadManager.instance()
        for item in mgr.downloads:
            self._add_row(item)