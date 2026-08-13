"""
===========================================================
PRT Labs - UI / Pages
Class: BrowserPage
Description: Navegador Web integrado com Sniffer de Mídias otimizado.
             Correção de tela branca no YouTube e carregamento fluido.
===========================================================
"""

import os
from urllib.parse import urlparse
from PySide6.QtCore import QUrl, Qt, QObject, Signal, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

try:
    from PySide6.QtWebEngineCore import (
        QWebEngineUrlRequestInterceptor,
        QWebEngineSettings,
        QWebEngineProfile
    )
    from PySide6.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False


if HAS_WEBENGINE:
    class InterceptorSignals(QObject):
        media_detected = Signal(dict)

    class LightHeaderInterceptor(QWebEngineUrlRequestInterceptor):
        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self.signals = InterceptorSignals()

        def interceptRequest(self, info) -> None:
            url_str = info.requestUrl().toString()
            url_lower = url_str.lower()

            # Ignora totalmente tráfego do YouTube/GoogleVideo no interceptador para não travar
            if "googlevideo.com" in url_lower or "youtube.com" in url_lower or "ytimg.com" in url_lower:
                return

            # Ignora recursos estáticos
            if any(ext in url_lower for ext in [".png", ".jpg", ".jpeg", ".css", ".js", ".woff", ".woff2", ".svg", ".ico"]):
                return

            # Ignora segmentos HLS/DASH
            if (".ts" in url_lower or ".m4s" in url_lower) and not ("playlist" in url_lower or "master" in url_lower or "index" in url_lower):
                return

            is_panda_embed = "pandavideo.com.br" in url_lower and ("embed" in url_lower or "player" in url_lower or "playlist" in url_lower)
            is_master_playlist = ("playlist.m3u8" in url_lower or "master.m3u8" in url_lower or "index.m3u8" in url_lower or ".mpd" in url_lower)
            is_direct_video = ".mp4" in url_lower

            is_audio_file = any(ext in url_lower for ext in [".mp3", ".m4a", ".aac", ".ogg", ".wav"])

            if is_panda_embed or is_master_playlist or is_direct_video:
                self.signals.media_detected.emit({"url": url_str, "type": "video"})
            elif is_audio_file:
                self.signals.media_detected.emit({"url": url_str, "type": "audio"})


class BrowserPage(QWidget):
    # Emite (url_de_download, tipo, qualidade, titulo_do_video)
    download_requested = Signal(str, str, str, str)

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent)
        self.interceptor = None
        self.detected_medias = []
        self._build_ui()

    def _load_url(self) -> None:
        url_text = self.txt_url.text().strip()
        if not url_text.startswith(("http://", "https://")):
            url_text = "https://" + url_text
        if HAS_WEBENGINE and hasattr(self, "web_view"):
            self.web_view.setUrl(QUrl(url_text))

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        nav_card = QFrame()
        nav_card.setObjectName("cardFrame")
        nav_layout = QHBoxLayout(nav_card)
        nav_layout.setContentsMargins(8, 8, 8, 8)

        self.btn_back = QPushButton("◀")
        self.btn_forward = QPushButton("▶")
        self.btn_reload = QPushButton("🔄")

        for btn in (self.btn_back, self.btn_forward, self.btn_reload):
            btn.setFixedWidth(36)
            btn.setCursor(Qt.PointingHandCursor)

        self.txt_url = QLineEdit()
        self.txt_url.setText("https://www.youtube.com")
        self.txt_url.returnPressed.connect(self._load_url)

        btn_go = QPushButton("Ir")
        btn_go.setCursor(Qt.PointingHandCursor)
        btn_go.clicked.connect(self._load_url)

        self.btn_sniffer = QPushButton("🎬 Mídias (0)")
        self.btn_sniffer.setCursor(Qt.PointingHandCursor)
        self.btn_sniffer.setCheckable(True)
        self.btn_sniffer.clicked.connect(self._toggle_sniffer)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addWidget(self.txt_url, stretch=4)
        nav_layout.addWidget(btn_go)
        nav_layout.addWidget(self.btn_sniffer)

        layout.addWidget(nav_card)

        content_layout = QHBoxLayout()

        if HAS_WEBENGINE:
            self.web_view = QWebEngineView()
            page = self.web_view.page()

            # Identificação do Chrome para compatibilidade total
            profile = page.profile()
            profile.setHttpUserAgent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )

            # Ativa suporte total a reprodução e execução de scripts
            settings = page.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

            # Eventos de navegação e carregamento
            self.web_view.urlChanged.connect(self._on_url_changed)
            self.web_view.loadFinished.connect(self._on_load_finished)

            try:
                self.interceptor = LightHeaderInterceptor(self)
                self.interceptor.signals.media_detected.connect(
                    self._add_detected_media, Qt.QueuedConnection
                )
                profile.setUrlRequestInterceptor(self.interceptor)
            except Exception:
                pass

            self.web_view.setUrl(QUrl("https://www.youtube.com"))

            self.btn_back.clicked.connect(self.web_view.back)
            self.btn_forward.clicked.connect(self.web_view.forward)
            self.btn_reload.clicked.connect(self.web_view.reload)
            content_layout.addWidget(self.web_view, stretch=3)

        self.card_sniffer = QFrame()
        self.card_sniffer.setObjectName("cardFrame")
        self.card_sniffer.setFixedWidth(330)
        self.card_sniffer.setVisible(False)

        sniffer_layout = QVBoxLayout(self.card_sniffer)
        sniffer_layout.setContentsMargins(12, 12, 12, 12)

        lbl_s_title = QLabel("🕵️‍♂️ Mídias Encontradas")
        lbl_s_title.setStyleSheet("font-weight: bold; font-size: 13px;")

        btn_capture_page = QPushButton("🎥 Capturar Vídeo da Página Atual")
        btn_capture_page.setCursor(Qt.PointingHandCursor)
        btn_capture_page.setStyleSheet("background-color: #2196F3; color: #FFF; font-weight: bold; padding: 7px; border-radius: 4px;")
        btn_capture_page.clicked.connect(self._capture_current_page_media)

        sniffer_layout.addWidget(lbl_s_title)
        sniffer_layout.addWidget(btn_capture_page)

        self.scroll_media = QScrollArea()
        self.scroll_media.setWidgetResizable(True)
        self.scroll_media.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.container_media = QWidget()
        self.layout_media_list = QVBoxLayout(self.container_media)
        self.layout_media_list.addStretch()

        self.scroll_media.setWidget(self.container_media)
        sniffer_layout.addWidget(self.scroll_media)

        btn_clear = QPushButton("🗑️ Limpar Capturas")
        btn_clear.clicked.connect(self._clear_detected_medias)
        sniffer_layout.addWidget(btn_clear)

        content_layout.addWidget(self.card_sniffer)
        layout.addLayout(content_layout)

    def _on_url_changed(self, qurl: QUrl) -> None:
        url_str = qurl.toString()
        self.txt_url.setText(url_str)
        if "watch?v=" in url_str or "vimeo.com/" in url_str:
            QTimer.singleShot(1500, self._capture_current_page_media)

    def _on_load_finished(self, ok: bool) -> None:
        if ok and hasattr(self, "web_view"):
            url_str = self.web_view.url().toString()
            if "watch?v=" in url_str or "vimeo.com/" in url_str:
                self._capture_current_page_media()

    def _toggle_sniffer(self) -> None:
        if hasattr(self, "card_sniffer"):
            is_visible = self.card_sniffer.isVisible()
            self.card_sniffer.setVisible(not is_visible)

    def _capture_current_page_media(self) -> None:
        if hasattr(self, "web_view"):
            page_url = self.web_view.url().toString()
            if page_url and not page_url.startswith("chrome://"):
                self._add_detected_media({"url": page_url, "type": "video"})

    def _add_detected_media(self, media_info: dict) -> None:
        raw_url = media_info.get("url", "")
        m_type = media_info.get("type", "video").upper()

        if not raw_url:
            return

        current_page_url = self.web_view.url().toString() if hasattr(self, "web_view") else ""
        current_page_title = self.web_view.title() if hasattr(self, "web_view") else ""

        if "youtube.com" in current_page_url or "youtu.be" in current_page_url:
            final_url = current_page_url
            media_title = current_page_title.replace("- YouTube", "").strip() or "Vídeo do YouTube"
        elif "vimeo.com" in current_page_url:
            final_url = current_page_url
            media_title = current_page_title or "Vídeo do Vimeo"
        else:
            final_url = raw_url
            media_title = current_page_title or "Vídeo Capturado"

        if any(m["url"] == final_url for m in self.detected_medias):
            return

        self.detected_medias.append({"url": final_url, "title": media_title, "type": m_type})
        self.btn_sniffer.setText(f"🎬 Mídias ({len(self.detected_medias)})")

        card = QFrame()
        card.setObjectName("cardFrame")
        c_layout = QVBoxLayout(card)

        lbl_name = QLabel(f"📹 [{m_type}] {media_title[:35]}")
        lbl_name.setStyleSheet("font-weight: bold; font-size: 11px;")
        lbl_name.setWordWrap(True)

        combo_quality = QComboBox()
        if m_type == "VIDEO":
            combo_quality.addItems([
                "1080p (Full HD - Máxima)",
                "720p (HD - Recomendado)",
                "480p (Médio)",
                "Apenas Áudio (MP3 / 320kbps)"
            ])
        else:
            combo_quality.addItems(["Áudio MP3 (320kbps)", "Áudio Original"])

        btn_download = QPushButton("⬇️ Baixar nesta Qualidade")
        btn_download.setCursor(Qt.PointingHandCursor)
        btn_download.setStyleSheet("background-color: #00E676; color: #000; font-weight: bold; padding: 6px;")

        btn_download.clicked.connect(
            lambda _, u=final_url, t=m_type, q=combo_quality, title=media_title, btn=btn_download: self._send_to_downloads(u, t, q.currentText(), title, btn)
        )

        c_layout.addWidget(lbl_name)
        c_layout.addWidget(combo_quality)
        c_layout.addWidget(btn_download)

        self.layout_media_list.insertWidget(self.layout_media_list.count() - 1, card)

    def _send_to_downloads(self, url: str, media_type: str, quality: str, title: str, button: QPushButton) -> None:
        button.setText("✅ Enviado!")
        button.setStyleSheet("background-color: #2196F3; color: #FFF; font-weight: bold; padding: 6px;")
        QTimer.singleShot(2000, lambda: button.setText("⬇️ Baixar nesta Qualidade"))

        self.download_requested.emit(url, media_type, quality, title)

    def _clear_detected_medias(self) -> None:
        self.detected_medias.clear