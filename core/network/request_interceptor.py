"""
===========================================================
PRT Labs - Core / Network
Class: PRTNetworkInterceptor

Description:
    Interceptador de tráfego HTTP/HTTPS para Chromium/QtWebEngine.
    Captura automaticamente URLs de streaming (HLS/M3U8, DASH, MP4, YouTube),
    mídias protegidas e extrai os cabeçalhos de requisição reais.
===========================================================
"""

import re
from PySide6.QtCore import QObject, Signal
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInfo, QWebEngineUrlRequestInterceptor


class SnifferSignals(QObject):
    """Sinais Qt para comunicação segura entre a Thread do Chromium e a UI."""

    media_detected = Signal(dict)


class PRTNetworkInterceptor(QWebEngineUrlRequestInterceptor):
    """Interceptador de requisições de rede para sniffer de mídias."""

    # Padrões flexíveis regex para captura universal de mídias e players
    MEDIA_PATTERNS = [
        (r"googlevideo\.com/videoplayback", "YouTube Video Stream", "youtube"),
        (r"youtube\.com/watch\?v=", "YouTube Page", "youtube"),
        (r"\.m3u8", "HLS Playlist", "m3u8"),
        (r"\.mpd", "DASH Manifest", "mpd"),
        (r"\.mp4", "Vídeo Direct MP4", "mp4"),
        (r"vimeo\.com", "Vimeo Stream", "vimeo"),
        (r"b-api\.videodelivery\.net", "Cloudflare Stream", "cloudflare"),
        (r"pandavideo\.com\.br", "Panda Video Stream", "panda"),
        (r"hotmart\.com", "Hotmart Stream", "hotmart"),
        (r"kiwify\.com\.br", "Kiwify Stream", "kiwify"),
    ]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.signals = SnifferSignals()
        self._captured_cache = set()

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        """Método executado dinamicamente pelo Chromium para cada requisição HTTP."""
        raw_url = info.requestUrl().toString()

        # Evita duplicar logs da exata mesma requisição
        if raw_url in self._captured_cache:
            return

        # Análise de correspondência com os padrões de mídia
        for pattern, media_type, platform_tag in self.MEDIA_PATTERNS:
            if re.search(pattern, raw_url, re.IGNORECASE):
                self._captured_cache.add(raw_url)

                captured_headers = self._extract_headers(info)

                payload = {
                    "url": raw_url,
                    "type": media_type,
                    "platform": platform_tag,
                    "method": info.requestMethod().data().decode("utf-8", errors="ignore"),
                    "headers": captured_headers,
                }

                print(f"🎯 [PRT Sniffer] Interceptado ({media_type}): {raw_url[:90]}...")

                self.signals.media_detected.emit(payload)
                break

    def _extract_headers(self, info: QWebEngineUrlRequestInfo) -> dict[str, str]:
        """Captura os headers da requisição."""
        headers = {}
        try:
            first_party = info.firstPartyUrl().toString()
            if first_party:
                headers["Referer"] = first_party
        except Exception:
            pass
        return headers

    def clear_cache(self) -> None:
        """Limpa o histórico de mídias capturadas."""
        self._captured_cache.clear()