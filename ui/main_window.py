"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: PRTMainWindow

Description:
    Main application window supporting external sidebar insertion,
    routing callbacks, page switching, live status bar, native OS notifications,
    and Ctrl+K global search filtering.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from services.download_manager import PRTDownloadManager
from services.system_monitor import PRTSystemMonitor
from ui.pages.courses_page import CoursesPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.downloads_page import DownloadsPage
from ui.pages.settings_page import SettingsPage


class PRTMainWindow(QMainWindow):
    """Janela principal do PRT NEXUS."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PRT NEXUS")
        self.resize(1100, 680)

        self._sidebar = None
        self._build_ui()
        self._setup_global_search()
        self._init_tray_icon()
        self._connect_monitors()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #0E0E10;")
        self.setCentralWidget(central_widget)

        self._main_layout = QHBoxLayout(central_widget)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        content_area = QWidget()
        self._content_layout = QVBoxLayout(content_area)
        self._content_layout.setContentsMargins(20, 15, 20, 0)
        self._content_layout.setSpacing(15)

        # Header Superior
        header_layout = QHBoxLayout()
        header_layout.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar cursos, arquivos ou conectores... (Ctrl+K)")
        self.search_input.setFixedWidth(380)
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 8px 12px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #007ACC;
            }
            """
        )
        header_layout.addWidget(self.search_input)

        user_badge = QLabel("RT")
        user_badge.setFixedSize(32, 32)
        user_badge.setAlignment(Qt.AlignCenter)
        user_badge.setStyleSheet(
            """
            background-color: #007ACC;
            color: #FFFFFF;
            font-weight: bold;
            border-radius: 16px;
            font-size: 12px;
            """
        )
        header_layout.addWidget(user_badge)

        self._content_layout.addLayout(header_layout)

        # Stack de Páginas (0=Dash, 1=Downloads, 2=Cursos, 3=Config)
        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(DashboardPage())
        self.page_stack.addWidget(DownloadsPage())
        self.page_stack.addWidget(CoursesPage())
        self.page_stack.addWidget(SettingsPage())

        self._content_layout.addWidget(self.page_stack)

        # Rodapé do Sistema (Status Bar)
        footer = QWidget()
        footer.setFixedHeight(30)
        footer.setStyleSheet("background-color: #0B0B0C; border-top: 1px solid #18181B;")

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)

        self.lbl_status_downloads = QLabel("Nenhum download ativo")
        self.lbl_status_downloads.setStyleSheet("color: #8E8E93; font-size: 11px;")

        self.lbl_status_system = QLabel("CPU: 0%  RAM: 0%")
        self.lbl_status_system.setStyleSheet("color: #8E8E93; font-size: 11px;")

        sync_lbl = QLabel("• Sincronizado")
        sync_lbl.setStyleSheet("color: #34C759; font-size: 11px; font-weight: bold;")

        footer_layout.addWidget(self.lbl_status_downloads)
        footer_layout.addStretch()
        footer_layout.addWidget(self.lbl_status_system)
        footer_layout.addSpacing(30)
        footer_layout.addWidget(sync_lbl)

        self._content_layout.addWidget(footer)
        self._main_layout.addWidget(content_area)

    def _setup_global_search(self) -> None:
        """Configura o atalho Ctrl+K e a busca em tempo real."""
        # Atalho do Teclado (Ctrl + K)
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_search.activated.connect(self._focus_search)

        # Evento ao digitar no campo de busca
        self.search_input.textChanged.connect(self._on_search_text_changed)

    def _focus_search(self) -> None:
        """Dá foco na caixa de texto do header e seleciona todo o conteúdo."""
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _on_search_text_changed(self, text: str) -> None:
        """Redireciona para a aba de Cursos e filtra os vídeos em tempo real."""
        if text.strip() and self.page_stack.currentIndex() != 2:
            self.navigate_to(2)  # Muda automaticamente para a aba de Cursos ao digitar

        courses_page = self.page_stack.widget(2)
        if isinstance(courses_page, CoursesPage):
            courses_page.filter_media(text)

    def _init_tray_icon(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        app_icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray_icon.setIcon(app_icon)
        self.tray_icon.setToolTip("PRT NEXUS")
        self.tray_icon.show()

    def add_sidebar(self, sidebar: QWidget) -> None:
        if self._sidebar is not None:
            self._main_layout.removeWidget(self._sidebar)
            self._sidebar.deleteLater()

        self._sidebar = sidebar
        self._main_layout.insertWidget(0, sidebar)

        for btn in sidebar.findChildren(QPushButton):
            btn.setCheckable(True)

        self.navigate_to(0)

    # --- Métodos requeridos pela sidebar.py ---
    def show_dashboard(self) -> None:
        self.navigate_to(0)

    def show_downloads(self) -> None:
        self.navigate_to(1)

    def show_courses(self) -> None:
        self.navigate_to(2)

    def show_settings(self) -> None:
        self.navigate_to(3)

    def show_license(self) -> None:
        self.navigate_to(0)

    def navigate_to(self, target: object) -> None:
        idx = 0
        if isinstance(target, int):
            idx = target
        elif isinstance(target, str):
            clean = target.lower().strip()
            mapping = {
                "dash": 0, "dashboard": 0,
                "download": 1, "downloads": 1,
                "curso": 2, "cursos": 2, "courses": 2,
                "config": 3, "configurações": 3, "configuracoes": 3, "settings": 3
            }
            for k, v in mapping.items():
                if k in clean:
                    idx = v
                    break

        if 0 <= idx < self.page_stack.count():
            self.page_stack.setCurrentIndex(idx)

        if self._sidebar:
            btns = self._sidebar.findChildren(QPushButton)
            for b_idx, btn in enumerate(btns):
                btn_text = btn.text().lower()
                is_active = False
                if idx == 0 and ("dash" in btn_text or b_idx == 0):
                    is_active = True
                elif idx == 1 and ("download" in btn_text or b_idx == 1):
                    is_active = True
                elif idx == 2 and ("curso" in btn_text or b_idx == 2):
                    is_active = True
                elif idx == 3 and ("config" in btn_text or b_idx == 3):
                    is_active = True

                btn.setChecked(is_active)

    def add_header(self, header: QWidget) -> None:
        self._content_layout.insertWidget(0, header)

    def set_content(self, widget: QWidget) -> None:
        self._content_layout.insertWidget(1, widget)

    def _connect_monitors(self) -> None:
        monitor = PRTSystemMonitor.instance()
        monitor.metrics_updated.connect(self._on_system_metrics_updated)

        manager = PRTDownloadManager.instance()
        manager.progress_updated.connect(lambda *_: self._update_download_status())
        manager.cleared_signal.connect(self._update_download_status)
        manager.download_completed.connect(self._show_download_notification)

    def _show_download_notification(self, title: str) -> None:
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.showMessage(
                "PRT NEXUS - Download Concluído! 🔔",
                f"O arquivo '{title}' já está pronto na sua biblioteca.",
                QSystemTrayIcon.Information,
                4000
            )

    def _on_system_metrics_updated(
        self,
        cpu: float,
        ram: float,
        rx_speed: str,
        tx_speed: str,
        ram_used_gb: float,
        ram_total_gb: float,
    ) -> None:
        self.lbl_status_system.setText(f"CPU: {int(cpu)}%   RAM: {int(ram)}%")

    def _update_download_status(self) -> None:
        manager = PRTDownloadManager.instance()
        active_items = [d for d in manager.downloads if d.status == "Baixando"]

        if not active_items:
            self.lbl_status_downloads.setText("Nenhum download ativo")
            self.lbl_status_downloads.setStyleSheet("color: #8E8E93; font-size: 11px;")
        else:
            speeds = [item.speed for item in active_items if item.speed != "-"]
            top_speed = speeds[0] if speeds else "0.0 KB/s"
            self.lbl_status_downloads.setText(f"↑ {len(active_items)} download(s) ativo(s)  {top_speed}")
            self.lbl_status_downloads.setStyleSheet("color: #34C759; font-size: 11px; font-weight: bold;")