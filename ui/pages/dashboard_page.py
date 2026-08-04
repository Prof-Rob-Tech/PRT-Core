"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: DashboardPage

Description:
    Two-column Dashboard page connected to global Download Manager.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from services.download_manager import PRTDownloadManager
from ui.pages.base_page import BasePage
from widgets import PRTStatCard
from widgets.connectors_panel import PRTConnectorsPanel
from widgets.new_download_dialog import PRTNewDownloadDialog
from widgets.quick_access import PRTQuickAccess
from widgets.storage_panel import PRTStoragePanel


class DashboardPage(BasePage):
    """Dashboard page featuring summary metrics and live shortcuts."""

    def __init__(self) -> None:
        super().__init__()

        self._layout = QHBoxLayout(self)

        self._configure()
        self._build_ui()
        self._connect_signals()

    def _configure(self) -> None:
        """Configure page margins and spacing."""
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(15)

    def _build_ui(self) -> None:
        """Build the user interface."""

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        grid_layout.addWidget(PRTStatCard("Downloads", "152", "Arquivos baixados"), 0, 0)
        grid_layout.addWidget(PRTStatCard("Cursos", "48", "Disponíveis"), 0, 1)
        grid_layout.addWidget(PRTStatCard("Licença", "Ativa", "Status"), 1, 0)
        grid_layout.addWidget(PRTStatCard("Atualizações", "3", "Pendentes"), 1, 1)

        left_layout.addLayout(grid_layout)

        self.quick_access = PRTQuickAccess()
        left_layout.addWidget(self.quick_access)
        left_layout.addStretch()

        right_container = QWidget()
        right_container.setFixedWidth(280)
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.connectors_panel = PRTConnectorsPanel()
        right_layout.addWidget(self.connectors_panel)
        right_layout.addSpacing(15)

        self.storage_panel = PRTStoragePanel()
        right_layout.addWidget(self.storage_panel)
        right_layout.addStretch()

        self._layout.addWidget(left_container, stretch=1)
        self._layout.addWidget(right_container)

    def _connect_signals(self) -> None:
        """Connect widget signals."""
        self.quick_access.new_download_clicked.connect(self._open_new_download_dialog)

    def _open_new_download_dialog(self) -> None:
        """Opens modal and registers new download to global manager."""
        dialog = PRTNewDownloadDialog(self)
        if dialog.exec():
            url = dialog.get_url()
            if url:
                PRTDownloadManager.instance().add_download(url)