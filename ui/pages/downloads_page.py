"""
===========================================================
PRT Labs - UI / Pages
Class: DownloadsPage / PRTDownloadsPage

Description:
    Gerenciador visual de Downloads com suporte a abertura de pasta.
===========================================================
"""

import os
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QProgressBar, QScrollArea
)

try:
    from ui.pages.base_page import BasePage
except Exception:
    class BasePage(QWidget):
        pass

from core.download_manager import download_manager
from database.db_manager import db_manager


class DownloadsPage(BasePage):
    """Página de Gerenciamento e Progresso dos Downloads."""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        try:
            super().__init__()
        except TypeError:
            try:
                super().__init__(parent)
            except Exception:
                QWidget.__init__(self)

        if parent is not None and isinstance(parent, QWidget):
            try:
                self.setParent(parent)
            except Exception:
                pass

        self.title = "Downloads"
        self.subtitle = "Gerenciador de Mídias em Fila"
        self.icon = "⬇️"
        self.page_id = "downloads"

        self.cards: dict = {}

        self.setStyleSheet("""
            QWidget {
                background-color: #09090B;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        main_layout = self.layout()
        if main_layout is None:
            main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { background: #09090B; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #27272A; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #3F3F46; }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        self.cards_layout = QVBoxLayout(container)
        self.cards_layout.setContentsMargins(24, 24, 24, 24)
        self.cards_layout.setSpacing(16)

        # Header
        header_box = QVBoxLayout()
        lbl_title = QLabel("⬇️ Fila de Downloads")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none;")
        lbl_subtitle = QLabel("Acompanhe a extração e o download de conteúdos em tempo real.")
        lbl_subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none;")
        header_box.addWidget(lbl_title)
        header_box.addWidget(lbl_subtitle)

        self.cards_layout.addLayout(header_box)

        # Estado Vazio
        self.empty_card = QFrame()
        self.empty_card.setStyleSheet("""
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
            QLabel { border: none; background: transparent; }
        """)
        empty_layout = QVBoxLayout(self.empty_card)
        empty_layout.setContentsMargins(40, 50, 40, 50)
        empty_layout.setAlignment(Qt.AlignCenter)

        lbl_icon = QLabel("📥")
        lbl_icon.setStyleSheet("font-size: 40px;")
        lbl_icon.setAlignment(Qt.AlignCenter)

        lbl_empty_t = QLabel("Nenhum download ativo no momento")
        lbl_empty_t.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; margin-top: 8px;")
        lbl_empty_t.setAlignment(Qt.AlignCenter)

        lbl_empty_d = QLabel("Utilize o Navegador ou os Conectores laterais para adicionar links à fila.")
        lbl_empty_d.setStyleSheet("font-size: 13px; color: #71717A; margin-top: 4px;")
        lbl_empty_d.setAlignment(Qt.AlignCenter)

        empty_layout.addWidget(lbl_icon)
        empty_layout.addWidget(lbl_empty_t)
        empty_layout.addWidget(lbl_empty_d)

        self.cards_layout.addWidget(self.empty_card)
        self.cards_layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _connect_signals(self) -> None:
        download_manager.task_added.connect(self._on_task_added)
        download_manager.task_updated.connect(self._on_task_updated)
        download_manager.task_completed.connect(self._on_task_completed)
        download_manager.task_failed.connect(self._on_task_failed)

    @Slot(object)
    def _on_task_added(self, task) -> None:
        self.empty_card.setVisible(False)

        card = QFrame()
        card.setObjectName(f"card_{task.task_id}")
        card.setStyleSheet("""
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QLabel { border: none; background: transparent; }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        # Topo
        top_layout = QHBoxLayout()
        lbl_title = QLabel(task.title)
        lbl_title.setObjectName("lbl_title")
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E4E4E7;")

        status_str = getattr(task.status, 'value', str(task.status))
        lbl_status = QLabel(status_str)
        lbl_status.setObjectName("lbl_status")
        lbl_status.setStyleSheet("font-size: 12px; font-weight: 600; color: #6366F1;")

        btn_folder = QPushButton("📂 Abrir Pasta")
        btn_folder.setObjectName("btn_folder")
        btn_folder.setVisible(False)
        btn_folder.setCursor(Qt.PointingHandCursor)
        btn_folder.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #E4E4E7;
                border: 1px solid #3F3F46;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #3F3F46; color: #FFFFFF; }
        """)
        
        save_dir = task.save_path if task.save_path else os.path.join(os.path.expanduser("~"), "Downloads", "PRT_Nexus")
        btn_folder.clicked.connect(lambda: os.startfile(save_dir) if os.path.exists(save_dir) else None)

        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        top_layout.addWidget(btn_folder)
        top_layout.addWidget(lbl_status)
        card_layout.addLayout(top_layout)

        # Barra
        pbar = QProgressBar()
        pbar.setObjectName("pbar")
        pbar.setValue(task.progress)
        pbar.setFixedHeight(8)
        pbar.setTextVisible(False)
        pbar.setStyleSheet("""
            QProgressBar {
                background-color: #09090B;
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #6366F1;
                border-radius: 4px;
            }
        """)
        card_layout.addWidget(pbar)

        # Rodapé
        bot_layout = QHBoxLayout()
        size_val = getattr(task, 'file_size', '-- MB')
        lbl_info = QLabel(f"Plataforma: {task.platform.capitalize()} | Size: {size_val} | Speed: {task.speed} | ETA: {task.eta}")
        lbl_info.setObjectName("lbl_info")
        lbl_info.setStyleSheet("font-size: 11px; color: #71717A;")

        lbl_pct = QLabel(f"{task.progress}%")
        lbl_pct.setObjectName("lbl_pct")
        lbl_pct.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFFFF;")

        bot_layout.addWidget(lbl_info)
        bot_layout.addStretch()
        bot_layout.addWidget(lbl_pct)
        card_layout.addLayout(bot_layout)

        self.cards[task.task_id] = card
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

    @Slot(object)
    def _on_task_updated(self, task) -> None:
        if task.task_id in self.cards:
            card = self.cards[task.task_id]
            pbar = card.findChild(QProgressBar, "pbar")
            lbl_title = card.findChild(QLabel, "lbl_title")
            lbl_status = card.findChild(QLabel, "lbl_status")
            lbl_info = card.findChild(QLabel, "lbl_info")
            lbl_pct = card.findChild(QLabel, "lbl_pct")

            if lbl_title and task.title:
                lbl_title.setText(task.title)

            if pbar:
                pbar.setValue(task.progress)

            if lbl_pct:
                lbl_pct.setText(f"{task.progress}%")

            if lbl_status:
                status_str = getattr(task.status, 'value', str(task.status))
                lbl_status.setText(status_str)

            if lbl_info:
                size_val = getattr(task, 'file_size', '-- MB')
                lbl_info.setText(f"Plataforma: {task.platform.capitalize()} | Size: {size_val} | Speed: {task.speed} | ETA: {task.eta}")

    @Slot(object)
    def _on_task_completed(self, task) -> None:
        self._on_task_updated(task)
        if task.task_id in self.cards:
            card = self.cards[task.task_id]
            lbl_status = card.findChild(QLabel, "lbl_status")
            btn_folder = card.findChild(QPushButton, "btn_folder")

            if lbl_status:
                lbl_status.setText("✅ Concluído")
                lbl_status.setStyleSheet("font-size: 12px; font-weight: 600; color: #10B981;")

            if btn_folder:
                btn_folder.setVisible(True)

        db_manager.add_download(
            task_id=task.task_id,
            title=task.title,
            url=task.url,
            platform=task.platform,
            file_path=task.save_path,
            status="Concluído"
        )
        db_manager.add_history(title=task.title, url=task.url, platform=task.platform)

    @Slot(object, str)
    def _on_task_failed(self, task, error_msg: str) -> None:
        if task.task_id in self.cards:
            card = self.cards[task.task_id]
            lbl_status = card.findChild(QLabel, "lbl_status")
            lbl_info = card.findChild(QLabel, "lbl_info")

            if lbl_status:
                lbl_status.setText("❌ Erro no Download")
                lbl_status.setStyleSheet("font-size: 12px; font-weight: 600; color: #EF4444;")

            if lbl_info:
                lbl_info.setText(f"Detalhe: {error_msg[:90]}...")
                lbl_info.setStyleSheet("font-size: 11px; color: #EF4444;")

    def on_show(self) -> None:
        pass


PRTDownloadsPage = DownloadsPage