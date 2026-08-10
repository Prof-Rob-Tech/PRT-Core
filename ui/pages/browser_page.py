"""
===========================================================
PRT Labs - UI / Pages
Class: BrowserPage / PRTBrowserPage

Description:
    Navegador Web integrado com Sniffer de Rede (Interceptor).
    Captura automaticamente links .m3u8, .mp4 e streams HLS
    enquanto você navega por áreas de membros ou sites.
===========================================================
"""

import os
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QListWidget, QListWidgetItem, QSplitter
)

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWebEngineCore import QWebEngineProfile
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False

try:
    from ui.pages.base_page import BasePage
except Exception:
    class BasePage(QWidget):
        pass

from services.network_interceptor import url_interceptor
from core.download_manager import download_manager


class BrowserPage(BasePage):
    """Navegador Web com Sniffer de Mídias em Tempo Real."""

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

        self.title = "Navegador"
        self.subtitle = "Sniffer de Mídias Web"
        self.icon = "🌐"
        self.page_id = "navegador"

        self.sniffed_urls = []

        self.setStyleSheet("""
            QWidget {
                background-color: #09090B;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        self._setup_ui()
        self._init_interceptor()

    def _setup_ui(self) -> None:
        main_layout = self.layout()
        if main_layout is None:
            main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Barra de Ferramentas / Endereço
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #18181B;
                border-bottom: 1px solid #27272A;
                padding: 4px;
            }
        """)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 8, 12, 8)
        tb_layout.setSpacing(8)

        # Botões de Navegação
        self.btn_back = QPushButton("◀")
        self.btn_forward = QPushButton("▶")
        self.btn_reload = QPushButton("🔄")

        for btn in (self.btn_back, self.btn_forward, self.btn_reload):
            btn.setFixedSize(32, 32)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #27272A;
                    color: #FFFFFF;
                    border: 1px solid #3F3F46;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3F3F46;
                }
            """)

        tb_layout.addWidget(self.btn_back)
        tb_layout.addWidget(self.btn_forward)
        tb_layout.addWidget(self.btn_reload)

        # Campo de URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Digite uma URL ou pesquise no Google (ex: https://hotmart.com)...")
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: #09090B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366F1;
            }
        """)
        self.url_input.returnPressed.connect(self._navigate_from_input)
        tb_layout.addWidget(self.url_input)

        # Botão Acessar
        btn_go = QPushButton("Ir")
        btn_go.setCursor(Qt.PointingHandCursor)
        btn_go.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                padding: 6px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        btn_go.clicked.connect(self._navigate_from_input)
        tb_layout.addWidget(btn_go)

        # Botão de Mídias Detectadas (Painel)
        self.btn_media_count = QPushButton("🎬 Mídias (0)")
        self.btn_media_count.setCursor(Qt.PointingHandCursor)
        self.btn_media_count.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #10B981;
                border: 1px solid #10B981;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #10B981;
                color: #FFFFFF;
            }
        """)
        self.btn_media_count.clicked.connect(self._toggle_media_panel)
        tb_layout.addWidget(self.btn_media_count)

        main_layout.addWidget(toolbar)

        # 2. Área Principal com WebEngine e Painel Lateral de Sniffer
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #27272A; width: 2px; }")

        # Visualizador Web
        if HAS_WEBENGINE:
            self.web_view = QWebEngineView()
            self.web_view.setUrl(QUrl("https://www.google.com"))
            self.web_view.urlChanged.connect(lambda qurl: self.url_input.setText(qurl.toString()))

            self.btn_back.clicked.connect(self.web_view.back)
            self.btn_forward.clicked.connect(self.web_view.forward)
            self.btn_reload.clicked.connect(self.web_view.reload)

            splitter.addWidget(self.web_view)
        else:
            fallback_label = QLabel("⚠️ PySide6.QtWebEngineWidgets não está disponível no sistema.")
            fallback_label.setAlignment(Qt.AlignCenter)
            fallback_label.setStyleSheet("color: #EF4444; font-size: 14px;")
            splitter.addWidget(fallback_label)

        # Painel Lateral de Mídias Interceptadas
        self.media_panel = QFrame()
        self.media_panel.setVisible(True)
        self.media_panel.setFixedWidth(320)
        self.media_panel.setStyleSheet("""
            QFrame {
                background-color: #18181B;
                border-left: 1px solid #27272A;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)
        panel_layout = QVBoxLayout(self.media_panel)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(10)

        panel_title = QLabel("📡 Mídias Sniffadas na Página")
        panel_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
        panel_layout.addWidget(panel_title)

        panel_desc = QLabel("Captura automática de arquivos .m3u8, .mp4 e streams HLS ao navegar.")
        panel_desc.setWordWrap(True)
        panel_desc.setStyleSheet("font-size: 11px; color: #71717A;")
        panel_layout.addWidget(panel_desc)

        # Lista de Mídias
        self.media_list = QListWidget()
        self.media_list.setStyleSheet("""
            QListWidget {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 6px;
                color: #FFFFFF;
            }
            QListWidget::item {
                border-bottom: 1px solid #18181B;
                padding: 4px;
            }
        """)
        panel_layout.addWidget(self.media_list)

        splitter.addWidget(self.media_panel)
        main_layout.addWidget(splitter)

    def _init_interceptor(self) -> None:
        """Conecta o sniffer ao profile e define User-Agent de Chrome Desktop oficial."""
        if HAS_WEBENGINE and hasattr(self, "web_view"):
            try:
                profile = self.web_view.page().profile()
                
                # Injeta a identidade oficial do Google Chrome de Windows 11/10
                chrome_user_agent = (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
                profile.setHttpUserAgent(chrome_user_agent)

                profile.setUrlRequestInterceptor(url_interceptor)
                url_interceptor.signal_handler.media_detected.connect(self._on_media_sniffed)
            except Exception as e:
                print(f"[Sniffer] Erro ao registrar interceptador: {e}")
                
    def _navigate_from_input(self) -> None:
        text = self.url_input.text().strip()
        if not text:
            return

        if not text.startswith("http://") and not text.startswith("https://"):
            if "." in text and " " not in text:
                text = "https://" + text
            else:
                text = f"https://www.google.com/search?q={text}"

        if HAS_WEBENGINE and hasattr(self, "web_view"):
            self.web_view.setUrl(QUrl(text))

    def _on_media_sniffed(self, media_url: str, resource_type: int) -> None:
        """Callback acionado sempre que uma mídia é interceptada na rede."""
        if media_url not in self.sniffed_urls:
            self.sniffed_urls.append(media_url)
            self.btn_media_count.setText(f"🎬 Mídias ({len(self.sniffed_urls)})")

            # Cria card visual na lista lateral
            item_widget = self._create_media_item_widget(media_url)
            list_item = QListWidgetItem(self.media_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.media_list.setItemWidget(list_item, item_widget)

    def _create_media_item_widget(self, media_url: str) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Nome limpo / Extensão
        ext = ".m3u8" if ".m3u8" in media_url else (".mp4" if ".mp4" in media_url else "Stream")
        lbl_type = QLabel(f"⚡ Mídia Detectada [{ext}]")
        lbl_type.setStyleSheet("font-size: 11px; font-weight: bold; color: #10B981;")

        lbl_url = QLabel(media_url)
        lbl_url.setWordWrap(True)
        lbl_url.setStyleSheet("font-size: 10px; color: #A1A1AA;")

        btn_download = QPushButton("⬇️ Enviar pro Download")
        btn_download.setCursor(Qt.PointingHandCursor)
        btn_download.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        btn_download.clicked.connect(lambda checked=False, u=media_url: self._send_to_download_manager(u))

        layout.addWidget(lbl_type)
        layout.addWidget(lbl_url)
        layout.addWidget(btn_download)
        return widget

    def _send_to_download_manager(self, url: str) -> None:
        """Envia a URL interceptada diretamente para a fila do DownloadManager."""
        download_manager.add_download(
            url=url,
            title=f"Mídia Web Sniffada ({url[:25]}...)",
            platform="navegador"
        )

    def _toggle_media_panel(self) -> None:
        """Abre/Fecha o painel lateral de mídias."""
        self.media_panel.setVisible(not self.media_panel.isVisible())

    def on_show(self) -> None:
        pass


# Alias de compatibilidade
PRTBrowserPage = BrowserPage