"""
===========================================================
PRT Labs - UI / Pages
Class: BrowserPage
Description: Navegador Web integrado com Sniffer de Mídias
             e suporte nativo ao Tema Claro no Chromium.
===========================================================
"""

import os
from PySide6.QtCore import QUrl, Qt, QObject, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Força o motor Chromium a simular Modo Claro nativo para todos os sites
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=preferredColorScheme=0"

try:
    from PySide6.QtWebEngineCore import (
        QWebEngineUrlRequestInterceptor,
        QWebEngineSettings
    )
    from PySide6.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False


if HAS_WEBENGINE:
    class InterceptorSignals(QObject):
        """Sinais emitidos pelo interceptador para o Sniffer do PRT Core."""
        media_detected = Signal(dict)

    class LightHeaderInterceptor(QWebEngineUrlRequestInterceptor):
        """Intercepta as requisições, força o cabeçalho claro e notifica o Sniffer."""

        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self.signals = InterceptorSignals()

        def interceptRequest(self, info) -> None:
            # 1. Cabeçalho HTTP de preferência de cor
            info.setHttpHeader(b"Sec-CH-UA-Color-Scheme", b'"light"')
            info.setHttpHeader(b"sec-ch-ua-color-scheme", b'"light"')

            # 2. Sniffer de Mídias
            url_str = info.requestUrl().toString()
            if any(ext in url_str.lower() for ext in [".m3u8", ".mp4", ".mp3", ".m4s"]):
                self.signals.media_detected.emit({
                    "url": url_str,
                    "type": "audio" if ".mp3" in url_str.lower() else "video"
                })


class BrowserPage(QWidget):
    """Página de Navegador Web com Sniffer de Mídias."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.interceptor = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Barra de Navegação
        nav_card = QFrame()
        nav_card.setObjectName("cardFrame")
        nav_layout = QHBoxLayout(nav_card)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        nav_layout.setSpacing(6)

        self.btn_back = QPushButton("◀")
        self.btn_forward = QPushButton("▶")
        self.btn_reload = QPushButton("🔄")

        for btn in (self.btn_back, self.btn_forward, self.btn_reload):
            btn.setFixedWidth(36)
            btn.setCursor(Qt.PointingHandCursor)

        self.txt_url = QLineEdit()
        self.txt_url.setText("https://www.google.com")
        self.txt_url.returnPressed.connect(self._load_url)

        btn_go = QPushButton("Ir")
        btn_go.setCursor(Qt.PointingHandCursor)
        btn_go.clicked.connect(self._load_url)

        self.btn_sniffer = QPushButton("🎬 Mídias (0)")
        self.btn_sniffer.setCursor(Qt.PointingHandCursor)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addWidget(self.txt_url, stretch=4)
        nav_layout.addWidget(btn_go)
        nav_layout.addWidget(self.btn_sniffer)

        layout.addWidget(nav_card)

        # Área Conteúdo: WebEngine + Painel do Sniffer
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        if HAS_WEBENGINE:
            self.web_view = QWebEngineView()
            page = self.web_view.page()

            # Cor de fundo padrão da janela web
            page.setBackgroundColor(QColor("#FFFFFF"))

            # Registra interceptador (Sniffer + Cabeçalho)
            try:
                self.interceptor = LightHeaderInterceptor(self)
                page.profile().setUrlRequestInterceptor(self.interceptor)
            except Exception:
                pass

            # Garante que ForceDarkMode do Chromium não está ativo
            try:
                settings = page.settings()
                if hasattr(QWebEngineSettings.WebAttribute, "ForceDarkMode"):
                    settings.setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, False)
            except Exception:
                pass

            self.web_view.setUrl(QUrl("https://www.google.com"))

            self.btn_back.clicked.connect(self.web_view.back)
            self.btn_forward.clicked.connect(self.web_view.forward)
            self.btn_reload.clicked.connect(self.web_view.reload)
            content_layout.addWidget(self.web_view, stretch=3)
        else:
            placeholder_web = QFrame()
            placeholder_web.setObjectName("cardFrame")
            p_layout = QVBoxLayout(placeholder_web)
            lbl = QLabel("🌐 Navegador Web (QtWebEngine Módulo)")
            lbl.setAlignment(Qt.AlignCenter)
            p_layout.addWidget(lbl)
            content_layout.addWidget(placeholder_web, stretch=3)

        # Painel Lateral do Sniffer
        self.card_sniffer = QFrame()
        self.card_sniffer.setObjectName("cardFrame")
        self.card_sniffer.setFixedWidth(280)

        sniffer_layout = QVBoxLayout(self.card_sniffer)
        sniffer_layout.setContentsMargins(12, 12, 12, 12)
        sniffer_layout.setSpacing(8)

        lbl_s_title = QLabel("🕵️‍♂️ Mídias Sniffadas na Página")
        lbl_s_title.setStyleSheet("font-weight: bold; font-size: 12px;")

        lbl_s_desc = QLabel("Captura automática de arquivos .m3u8, .mp4 e streams HLS ao navegar.")
        lbl_s_desc.setStyleSheet("color: #8E8E93; font-size: 11px;")
        lbl_s_desc.setWordWrap(True)

        sniffer_layout.addWidget(lbl_s_title)
        sniffer_layout.addWidget(lbl_s_desc)
        sniffer_layout.addStretch()

        content_layout.addWidget(self.card_sniffer)
        layout.addLayout(content_layout)

    def _load_url(self) -> None:
        url_text = self.txt_url.text().strip()
        if not url_text.startswith(("http://", "https://")):
            url_text = "https://" + url_text
        if HAS_WEBENGINE and hasattr(self, "web_view"):
            self.web_view.setUrl(QUrl(url_text))