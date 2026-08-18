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
        """
        Recebe os dados da mídia interceptada pelo navegador e 
        envia para o Gerenciador de Downloads.
        """
        if not media_data:
            return

        # Busca as chaves de forma segura sem dar KeyError
        url = media_data.get("url", "")
        platform = media_data.get("platform", "WEB")
        media_type = media_data.get("media_type", "VIDEO")
        quality = media_data.get("quality", "1080p")
        title = media_data.get("title") or media_data.get("page_title") or ""

        if not url:
            return

        # Envia para a página de Downloads com o título capturado
        if hasattr(self, "downloads_page"):
            self.downloads_page.add_download(
                url=url,
                media_type=media_type,
                quality=quality,
                title=title
            )
            # Alterna automaticamente para a aba de Downloads se desejado
            # self.sidebar.select_tab("downloads")

    def run(self) -> int:
        """Exibe a interface e inicia o loop de eventos Qt."""
        self.main_window.showMaximized()
        return self.qt_app.exec()