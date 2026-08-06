"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: DownloadsPage

Description:
    Downloads Page for PRT NEXUS featuring Auto-Clipboard URL detection,
    aligned table cells, focus outline removal, and live progress tracking.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
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
    """Página do Gerenciador de Downloads."""

    def __init__(self) -> None:
        super().__init__()
        self._last_pasted_url = ""
        self._build_ui()
        self._connect_signals()
        self._reload_table()

    def showEvent(self, event) -> None:
        """Sempre que a aba abre, verifica a área de transferência do Windows para colar a URL."""
        super().showEvent(event)
        self._check_and_auto_paste_clipboard()

    def _check_and_auto_paste_clipboard(self) -> None:
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()

        if text.startswith("http://") or text.startswith("https://"):
            if not self.txt_url.text() and text != self._last_pasted_url:
                self.txt_url.setText(text)
                self.txt_url.selectAll()
                self._last_pasted_url = text
                print(f"📋 [PRT NEXUS] Link colado automaticamente: {text}")

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # 1. Título
        lbl_title = QLabel("Gerenciador de Downloads")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold; border: none; background: transparent;")
        layout.addWidget(lbl_title)

        # 2. Barra Superior (Input + Combo + Botão Baixar)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(10)

        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("Cole o link do vídeo ou aula aqui (YouTube, etc)...")
        self.txt_url.setStyleSheet(
            """
            QLineEdit {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 6px;
                padding: 8px 12px;
                color: #FFFFFF;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
            """
        )
        top_bar_layout.addWidget(self.txt_url, stretch=1)

        self.cbo_quality = QComboBox()
        self.cbo_quality.addItems(["Melhor (1080p+)", "Alta (720p)", "Médio (480p)", "Apenas Áudio (MP3)"])
        self.cbo_quality.setStyleSheet(
            """
            QComboBox {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 6px;
                padding: 8px 12px;
                color: #FFFFFF;
                font-size: 13px;
            }
            """
        )
        top_bar_layout.addWidget(self.cbo_quality)

        self.btn_download = QPushButton("📥 Baixar")
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                border: none;
                border-radius: 6px;
                padding: 9px 20px;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
            QPushButton:pressed {
                background-color: #005999;
            }
            """
        )
        top_bar_layout.addWidget(self.btn_download)

        layout.addLayout(top_bar_layout)

        # 3. Barra de Ações Rápidas
        actions_bar_layout = QHBoxLayout()
        actions_bar_layout.setSpacing(10)

        self.btn_pause_all = QPushButton("⏸️ Pausar Todos")
        self.btn_pause_all.setStyleSheet("background-color: #141416; border: 1px solid #26262B; color: #FFF; padding: 6px 12px; border-radius: 4px;")
        self.btn_pause_all.setCursor(Qt.PointingHandCursor)

        self.btn_resume_all = QPushButton("▶️ Retomar Todos")
        self.btn_resume_all.setStyleSheet("background-color: #141416; border: 1px solid #26262B; color: #FFF; padding: 6px 12px; border-radius: 4px;")
        self.btn_resume_all.setCursor(Qt.PointingHandCursor)

        self.btn_clear_completed = QPushButton("🧹 Limpar Concluídos")
        self.btn_clear_completed.setStyleSheet("background-color: #141416; border: 1px solid #26262B; color: #FFF; padding: 6px 12px; border-radius: 4px;")
        self.btn_clear_completed.setCursor(Qt.PointingHandCursor)

        actions_bar_layout.addWidget(self.btn_pause_all)
        actions_bar_layout.addWidget(self.btn_resume_all)
        actions_bar_layout.addStretch()
        actions_bar_layout.addWidget(self.btn_clear_completed)

        layout.addLayout(actions_bar_layout)

        # 4. Tabela de Downloads
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setFocusPolicy(Qt.NoFocus)  # Remove caixas/bordas de foco ao clicar
        self.table.setSelectionMode(QTableWidget.NoSelection)  # Evita destaques indesejados nas células

        self.table.setHorizontalHeaderLabels([
            "Título / Conteúdo", "Qualidade", "Tamanho", "Progresso", "Velocidade", "Status", "Ações"
        ])

        # Dimensionamento e Alinhamento das Colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)

        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 140)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 60)

        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
                gridline-color: #1F1F23;
                color: #FFFFFF;
                outline: none;
            }
            QTableWidget::item {
                padding: 4px 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: #FFFFFF;
            }
            QTableWidget::item:focus {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QHeaderView::section {
                background-color: #0B0B0C;
                color: #8E8E93;
                padding: 8px;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }
            """
        )
        layout.addWidget(self.table)

    def _connect_signals(self) -> None:
        mgr = PRTDownloadManager.instance()

        self.btn_download.clicked.connect(self._on_add_clicked)
        self.txt_url.returnPressed.connect(self._on_add_clicked)

        self.btn_pause_all.clicked.connect(mgr.pause_all)
        self.btn_resume_all.clicked.connect(mgr.resume_all)
        self.btn_clear_completed.clicked.connect(mgr.clear_completed)

        mgr.download_added.connect(self._on_download_added)
        mgr.download_removed.connect(self._reload_table)
        mgr.download_cleared.connect(self._reload_table)
        if hasattr(mgr, "cleared_signal"):
            mgr.cleared_signal.connect(self._reload_table)

        mgr.progress_updated.connect(self._on_progress_updated)
        mgr.title_updated.connect(self._on_title_updated)
        mgr.status_updated.connect(self._on_status_updated)

    def _on_add_clicked(self) -> None:
        url = self.txt_url.text().strip()
        if not url:
            return

        quality_key = self.cbo_quality.currentText()
        mgr = PRTDownloadManager.instance()
        if hasattr(mgr, "add_download"):
            mgr.add_download(url, quality=quality_key)
        else:
            mgr.add_item(url, quality_key)
            mgr.start_download(url, quality_key)

        self.txt_url.clear()
        self._last_pasted_url = url
        self._reload_table()

    def _on_download_added(self, item: PRTDownloadItem) -> None:
        self._reload_table()

    def _on_title_updated(self, url: str, title: str) -> None:
        self._update_row_for_url(url, col=0, text=title)

    def _on_status_updated(self, url: str, status: str) -> None:
        self._update_row_for_url(url, col=5, text=status)

    def _on_progress_updated(self, url: str, title: str, speed: str, size: str, percentage: float, status: str) -> None:
        row = self._find_row_by_url(url)
        if row != -1:
            pbar = self.table.cellWidget(row, 3)
            if isinstance(pbar, QProgressBar):
                pbar.setValue(int(percentage))

            item_size = self.table.item(row, 2)
            if item_size and size:
                item_size.setText(size)

            item_speed = self.table.item(row, 4)
            if item_speed:
                item_speed.setText(speed)

            item_status = self.table.item(row, 5)
            if item_status:
                item_status.setText(status)

    def _reload_table(self) -> None:
        mgr = PRTDownloadManager.instance()
        items = mgr.downloads

        self.table.setRowCount(0)
        for row_idx, item in enumerate(items):
            self.table.insertRow(row_idx)

            # 0. Título (Alinhado à Esquerda)
            lbl_title = QTableWidgetItem(item.title)
            lbl_title.setData(Qt.UserRole, item.url)
            lbl_title.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row_idx, 0, lbl_title)

            # 1. Qualidade (Centralizado)
            item_q = QTableWidgetItem(item.quality)
            item_q.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, item_q)

            # 2. Tamanho (Centralizado)
            item_s = QTableWidgetItem(item.size)
            item_s.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 2, item_s)

            # 3. Barra de Progresso
            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(int(item.progress))
            pbar.setTextVisible(True)
            pbar.setStyleSheet(
                """
                QProgressBar {
                    border: 1px solid #26262B;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #0B0B0C;
                    color: #FFF;
                    font-size: 10px;
                }
                QProgressBar::chunk {
                    background-color: #007ACC;
                    border-radius: 3px;
                }
                """
            )
            self.table.setCellWidget(row_idx, 3, pbar)

            # 4. Velocidade (Centralizado)
            item_sp = QTableWidgetItem(item.speed)
            item_sp.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 4, item_sp)

            # 5. Status (Centralizado)
            item_st = QTableWidgetItem(item.status)
            item_st.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 5, item_st)

            # 6. Ações (Botão Remover)
            btn_remove = QPushButton("❌")
            btn_remove.setStyleSheet("background: transparent; border: none; font-size: 12px;")
            btn_remove.setCursor(Qt.PointingHandCursor)
            btn_remove.clicked.connect(lambda _, u=item.url: mgr.remove_item(u))
            self.table.setCellWidget(row_idx, 6, btn_remove)

    def _find_row_by_url(self, url: str) -> int:
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item and item.data(Qt.UserRole) == url:
                return r
        return -1

    def _update_row_for_url(self, url: str, col: int, text: str) -> None:
        row = self._find_row_by_url(url)
        if row != -1:
            item = self.table.item(row, col)
            if item:
                item.setText(text)


# Aliases de compatibilidade
DownloadsView = DownloadsPage
DownloadsWidget = DownloadsPage