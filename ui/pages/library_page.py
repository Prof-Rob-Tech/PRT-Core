"""
===========================================================
PRT Labs - UI / Pages
Class: LibraryPage / PRTLibraryPage

Description:
    Biblioteca visual de mídias conectada ao SQLite com 
    suporte total a deleção de itens e limpeza de biblioteca.
===========================================================
"""

import os
import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QScrollArea
)

try:
    from ui.pages.base_page import BasePage
except Exception:
    class BasePage(QWidget):
        pass

from database.db_manager import db_manager


class LibraryPage(BasePage):
    """Página da Biblioteca de Mídias baixadas."""

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

        self.title = "Biblioteca"
        self.subtitle = "Mídias Salvas"
        self.icon = "📁"
        self.page_id = "library"

        self.default_dir = os.path.join(os.path.expanduser("~"), "Downloads", "PRT_Nexus")
        os.makedirs(self.default_dir, exist_ok=True)

        self.all_items = []

        self.setStyleSheet("""
            QWidget {
                background-color: #09090B;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        self._setup_ui()

    def _get_db_connection(self):
        """Conecta diretamente ao banco de dados SQLite para executar queries de remoção."""
        db_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database", "nexus.db"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "nexus.db"),
            "nexus.db",
            "database/nexus.db"
        ]
        if hasattr(db_manager, "db_path") and getattr(db_manager, "db_path"):
            db_paths.insert(0, getattr(db_manager, "db_path"))

        for path in db_paths:
            if os.path.exists(path):
                try:
                    return sqlite3.connect(path)
                except Exception:
                    pass
        return None

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
        self.cards_layout.setSpacing(20)

        # 1. Header + Botões de Ação
        header_layout = QHBoxLayout()
        header_box = QVBoxLayout()
        lbl_title = QLabel("📁 Biblioteca de Mídias")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none;")
        lbl_subtitle = QLabel("Gerencie e visualize todas as mídias salvas localmente no computador.")
        lbl_subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none;")
        header_box.addWidget(lbl_title)
        header_box.addWidget(lbl_subtitle)

        # Botão Limpar Biblioteca
        btn_clear = QPushButton("🗑️ Limpar Biblioteca")
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #EF4444;
                border: 1px solid #3F3F46;
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7F1D1D;
                color: #FFFFFF;
                border-color: #EF4444;
            }
        """)
        btn_clear.clicked.connect(self._on_clear_library)

        # Botão Abrir Pasta
        btn_open_folder = QPushButton("📁 Abrir Pasta no Windows")
        btn_open_folder.setCursor(Qt.PointingHandCursor)
        btn_open_folder.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #E4E4E7;
                border: 1px solid #3F3F46;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3F3F46;
                color: #FFFFFF;
            }
        """)
        btn_open_folder.clicked.connect(self._on_open_main_folder)

        header_layout.addLayout(header_box)
        header_layout.addStretch()
        header_layout.addWidget(btn_clear)
        header_layout.addWidget(btn_open_folder)
        self.cards_layout.addLayout(header_layout)

        # 2. Barra de Pesquisa
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Pesquisar mídias na biblioteca...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #18181B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QLineEdit:focus { border-color: #6366F1; }
        """)
        self.search_input.textChanged.connect(self._filter_items)
        self.cards_layout.addWidget(self.search_input)

        # 3. Estado Vazio
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

        lbl_icon = QLabel("🎬")
        lbl_icon.setStyleSheet("font-size: 40px;")
        lbl_icon.setAlignment(Qt.AlignCenter)

        lbl_empty_t = QLabel("Sua biblioteca está vazia")
        lbl_empty_t.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; margin-top: 8px;")
        lbl_empty_t.setAlignment(Qt.AlignCenter)

        lbl_empty_d = QLabel("Os vídeos e conteúdos baixados através dos conectores e do navegador aparecerão listados aqui.")
        lbl_empty_d.setStyleSheet("font-size: 13px; color: #71717A; margin-top: 4px;")
        lbl_empty_d.setAlignment(Qt.AlignCenter)

        empty_layout.addWidget(lbl_icon)
        empty_layout.addWidget(lbl_empty_t)
        empty_layout.addWidget(lbl_empty_d)

        self.cards_layout.addWidget(self.empty_card)

        # Container dinâmico
        self.items_container = QWidget()
        self.items_container.setStyleSheet("background: transparent;")
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(12)

        self.cards_layout.addWidget(self.items_container)
        self.cards_layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.refresh_library()

    def _on_open_main_folder(self) -> None:
        if os.path.exists(self.default_dir):
            os.startfile(self.default_dir)

    def refresh_library(self) -> None:
        """Busca todas as mídias salvas no SQLite e re-renderiza a tela."""
        self.all_items = db_manager.get_all_downloads()

        if not self.all_items:
            self.empty_card.setVisible(True)
            self.items_container.setVisible(False)
        else:
            self.empty_card.setVisible(False)
            self.items_container.setVisible(True)
            self._render_items(self.all_items)

    def _render_items(self, items: list) -> None:
        for i in reversed(range(self.items_layout.count())):
            widget = self.items_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for item in items:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #18181B;
                    border: 1px solid #27272A;
                    border-radius: 10px;
                }
                QLabel { border: none; background: transparent; }
            """)
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            card_layout.setSpacing(14)

            icon_lbl = QLabel("🎵" if "audio" in item.get("title", "").lower() else "🎥")
            icon_lbl.setStyleSheet("font-size: 20px;")
            card_layout.addWidget(icon_lbl)

            info_box = QVBoxLayout()
            info_box.setSpacing(2)

            title_lbl = QLabel(item.get("title", "Mídia Sem Nome"))
            title_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")

            platform = item.get("platform", "web").capitalize()
            status = item.get("status", "Concluído")
            sub_lbl = QLabel(f"Plataforma: {platform}  •  Status: {status}")
            sub_lbl.setStyleSheet("font-size: 12px; color: #71717A;")

            info_box.addWidget(title_lbl)
            info_box.addWidget(sub_lbl)
            card_layout.addLayout(info_box, stretch=1)

            # Botões de Ação com callbacks isolados
            actions_layout = QHBoxLayout()
            actions_layout.setSpacing(8)

            btn_play = QPushButton("▶️ Executar")
            btn_play.setCursor(Qt.PointingHandCursor)
            btn_play.setStyleSheet("""
                QPushButton {
                    background-color: #6366F1;
                    color: #FFFFFF;
                    border: none;
                    padding: 6px 14px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: #4F46E5; }
            """)
            btn_play.clicked.connect(self._make_play_callback(item))

            btn_folder = QPushButton("📂 Pasta")
            btn_folder.setCursor(Qt.PointingHandCursor)
            btn_folder.setStyleSheet("""
                QPushButton {
                    background-color: #27272A;
                    color: #E4E4E7;
                    border: 1px solid #3F3F46;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: #3F3F46; color: #FFFFFF; }
            """)
            btn_folder.clicked.connect(self._make_folder_callback(item))

            btn_del = QPushButton("🗑️")
            btn_del.setToolTip("Remover esta mídia da biblioteca")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setStyleSheet("""
                QPushButton {
                    background-color: #27272A;
                    color: #EF4444;
                    border: 1px solid #3F3F46;
                    padding: 6px 10px;
                    border-radius: 6px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #7F1D1D;
                    color: #FFFFFF;
                    border-color: #EF4444;
                }
            """)
            btn_del.clicked.connect(self._make_del_callback(item))

            actions_layout.addWidget(btn_play)
            actions_layout.addWidget(btn_folder)
            actions_layout.addWidget(btn_del)

            card_layout.addLayout(actions_layout)
            self.items_layout.addWidget(card)

    def _make_play_callback(self, item: dict):
        return lambda: self._open_file(item)

    def _make_folder_callback(self, item: dict):
        return lambda: self._open_folder_of_file(item)

    def _make_del_callback(self, item: dict):
        return lambda: self._delete_single_item(item)

    def _open_file(self, item: dict) -> None:
        path = item.get("file_path") or self.default_dir
        title = item.get("title", "")

        if os.path.exists(path) and os.path.isfile(path):
            os.startfile(path)
            return

        target_dir = path if os.path.isdir(path) else self.default_dir
        if os.path.exists(target_dir):
            files = [
                os.path.join(target_dir, f) for f in os.listdir(target_dir)
                if os.path.isfile(os.path.join(target_dir, f))
            ]

            for f in files:
                if title and title.lower()[:15] in os.path.basename(f).lower():
                    os.startfile(f)
                    return

            if files:
                latest_file = max(files, key=os.path.getmtime)
                os.startfile(latest_file)
                return

        self._on_open_main_folder()

    def _open_folder_of_file(self, item: dict) -> None:
        path = item.get("file_path") or self.default_dir
        if os.path.exists(path):
            target_dir = os.path.dirname(path) if os.path.isfile(path) else path
            os.startfile(target_dir)
        else:
            self._on_open_main_folder()

    def _delete_single_item(self, item: dict) -> None:
        """Deleta o item do banco de dados SQLite e recarrega a página."""
        conn = self._get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                task_id = item.get("task_id")
                item_id = item.get("id")
                title = item.get("title")
                url = item.get("url")

                cursor.execute("""
                    DELETE FROM downloads 
                    WHERE (task_id IS NOT NULL AND task_id = ?)
                       OR (id IS NOT NULL AND id = ?)
                       OR (title = ? AND url = ?)
                """, (task_id, item_id, title, url))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"⚠️ Erro ao deletar do SQLite: {e}")

        self.refresh_library()

    def _on_clear_library(self) -> None:
        """Limpa todos os registros de downloads do banco de dados SQLite."""
        conn = self._get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM downloads")
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"⚠️ Erro ao limpar biblioteca no SQLite: {e}")

        self.refresh_library()

    def _filter_items(self, text: str) -> None:
        query = text.strip().lower()
        if not query:
            self._render_items(self.all_items)
        else:
            filtered = [
                item for item in self.all_items
                if query in item.get("title", "").lower() or query in item.get("platform", "").lower()
            ]
            self._render_items(filtered)

    def on_show(self) -> None:
        self.refresh_library()


PRTLibraryPage = LibraryPage