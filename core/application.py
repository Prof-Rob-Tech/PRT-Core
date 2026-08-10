"""
===========================================================
PRT Labs - Core
Class: Application

Description:
    Classe principal de orquestração do PRT NEXUS.
    Gerencia a janela, o Sniffer e o Download Manager.
===========================================================
"""

import sys
from PySide6.QtWidgets import QApplication

from core.download import PRTDownloadManager

# Tenta importar com o nome da classe da janela (PRTMainWindow ou MainWindow)
try:
    from ui.main_window import PRTMainWindow as MainWindow
except ImportError:
    from ui.main_window import MainWindow

from ui.widgets.sidebar import PRTSidebar
from core.download_manager import download_manager
from services.extractor_service import extractor_service

# Dentro do __init__ da classe Application:
download_manager.register_engine(extractor_service.download_media_task)


class Application:
    """Orquestrador do ciclo de vida da aplicação PRT NEXUS."""

    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("PRT NEXUS")

        # 1. Instanciar a Janela Principal e Sidebar
        self.main_window = MainWindow()
        self.sidebar = PRTSidebar()

        # 2. Instanciar o Gerenciador Global de Downloads
        self.download_manager = PRTDownloadManager(self.main_window)

        # Conectar sinais
        self.sidebar.connect_main_window(self.main_window)
        self._connect_sniffer()

    def _connect_sniffer(self) -> None:
        """Conecta as mídias capturadas pelo Sniffer diretamente ao Gerenciador de Downloads."""
        browser_page = getattr(self.main_window, "pages", {}).get("navegador")
        if browser_page and hasattr(browser_page, "interceptor"):
            browser_page.interceptor.signals.media_detected.connect(
                self._on_media_intercepted
            )

    def _on_media_intercepted(self, media_data: dict) -> None:
        """Slot acionado quando o Sniffer detecta uma mídia."""
        url = media_data["url"]
        platform = media_data["platform"]

        print(f"\n⚡ [Application] Mídia detectada no Sniffer ({platform.upper()})!")
        print(f"📥 Disparando download de teste via PRTDownloadManager...")

        # Inicia o download em segundo plano
        self.download_manager.add_download(
            url=url, 
            title=f"Video_Capturado_{platform}"
        )

    def run(self) -> int:
        """Exibe a interface e inicia o loop de eventos Qt."""
        self.main_window.show()
        return self.qt_app.exec()