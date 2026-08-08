"""
===========================================================
PRT Labs - UI / Pages
Class: BrowserPage

Description:
    Navegador Chromium embutido do PRT NEXUS com suporte
    a Sniffer de tráfego de mídia em tempo real e User-Agent
    autêntico para evitar bloqueios de bot/CAPTCHA.
===========================================================
"""

import re
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.network.request_interceptor import PRTNetworkInterceptor


class BrowserPage(QWidget):
    """Página de navegação com Sniffer de Mídias ativo em segundo plano."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Barra de Endereço / Ferramentas
        layout.addLayout(self._create_toolbar())

        # 2. Configurar perfil WebEngine com User-Agent real e Sniffer
        self.profile = QWebEngineProfile("PRT_Nexus_Profile", self)
        
        # User-Agent atualizado de Chrome padrão no Windows
        chrome_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
        self.profile.setHttpUserAgent(chrome_user_agent)

        self.interceptor = PRTNetworkInterceptor(self)
        self.profile.setUrlRequestInterceptor(self.interceptor)

        # Conectar sinal do sniffer para receber mídias capturadas
        self.interceptor.signals.media_detected.connect(self._on_media_captured)

        # 3. View do Navegador
        page = QWebEnginePage(self.profile, self)
        self.web_view = QWebEngineView(self)
        self.web_view.setPage(page)

        # Sinais da página web
        self.web_view.urlChanged.connect(self._on_url_changed)

        layout.addWidget(self.web_view, stretch=1)

        # Carregar página inicial diretamente
        self.web_view.load(QUrl("https://www.youtube.com"))

    def _create_toolbar(self) -> QHBoxLayout:
        """Cria a barra de controle superior do navegador."""
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(12, 8, 12, 8)
        toolbar.setSpacing(8)

        # Botões de navegação
        self.btn_back = QPushButton("◀")
        self.btn_forward = QPushButton("▶")
        self.btn_reload = QPushButton("🔄")

        for btn in (self.btn_back, self.btn_forward, self.btn_reload):
            btn.setFixedWidth(36)
            btn.setFixedHeight(32)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #18181B;
                    color: #FFFFFF;
                    border: 1px solid #27272A;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #27272A;
                }
            """
            )

        self.btn_back.clicked.connect(lambda: self.web_view.back())
        self.btn_forward.clicked.connect(lambda: self.web_view.forward())
        self.btn_reload.clicked.connect(lambda: self.web_view.reload())

        # Campo de URL
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("Digite uma URL (ex: youtube.com) ou pesquise...")
        self.txt_url.setFixedHeight(32)
        self.txt_url.setStyleSheet(
            """
            QLineEdit {
                background-color: #18181B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """
        )
        self.txt_url.returnPressed.connect(self._navigate_to_url)

        # Badge indicador do Sniffer
        self.lbl_sniffer_status = QLabel("⚡ Sniffer Ativo")
        self.lbl_sniffer_status.setStyleSheet(
            """
            QLabel {
                background-color: rgba(34, 197, 94, 0.15);
                color: #22C55E;
                border: 1px solid #22C55E;
                border-radius: 6px;
                padding: 4px 10px;
                font-weight: bold;
                font-size: 11px;
            }
        """
        )

        toolbar.addWidget(self.btn_back)
        toolbar.addWidget(self.btn_forward)
        toolbar.addWidget(self.btn_reload)
        toolbar.addWidget(self.txt_url, stretch=1)
        toolbar.addWidget(self.lbl_sniffer_status)

        return toolbar

    def _navigate_to_url(self) -> None:
        """Trata o texto digitado para direcionar diretamente para o site ou pesquisa."""
        url_text = self.txt_url.text().strip()
        if not url_text:
            return

        # Se já tiver protocolo, usa diretamente
        if url_text.startswith(("http://", "https://")):
            target_url = url_text
        # Se parecer com um domínio (ex: youtube.com, kiwify.app, hotmart.com)
        elif "." in url_text and " " not in url_text:
            target_url = f"https://{url_text}"
        # Caso contrário, trata como termo de pesquisa
        else:
            target_url = f"https://www.google.com/search?q={url_text}"

        self.web_view.load(QUrl(target_url))

    def _on_url_changed(self, url: QUrl) -> None:
        """Atualiza a barra de endereço quando o usuário muda de página."""
        self.txt_url.setText(url.toString())

    def _on_media_captured(self, media_data: dict) -> None:
        """Slot acionado sempre que o sniffer intercepta uma mídia."""
        print(
            f"\n🔥 [BrowserPage] Nova mídia interceptada!"
            f"\n   Plataforma: {media_data['platform'].upper()}"
            f"\n   Tipo: {media_data['type']}"
            f"\n   URL: {media_data['url']}\n"
        )