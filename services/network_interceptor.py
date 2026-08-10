"""
===========================================================
PRT Labs - Services / Network Interceptor
Class: PRTUrlRequestInterceptor

Description:
    Interceptador de requisições do PySide6 WebEngine.
    Captura URLs de mídia (.m3u8, .mp4, HLS, DASH) durante
    a navegação em tempo real.
===========================================================
"""

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo


class PRTUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """Interceptador que analisa tráfego de rede e detecta mídias."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.signal_handler = InterceptorSignals()

        # Extensões e padrões de mídia monitorados
        self.media_extensions = (
            ".m3u8", ".mp4", ".m4s", ".ts", ".webm", ".mp3", ".aac", ".flv"
        )
        self.media_keywords = [
            "master.m3u8", "index.m3u8", "playlist.m3u8",
            "vod", "stream", "hls", "vimeo.com/external", "player.vimeo"
        ]

        self.captured_urls = set()

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        """Método executado a cada requisição de rede no navegador."""
        url_str = info.requestUrl().toString()

        # Evita duplicatas na mesma sessão
        if url_str in self.captured_urls:
            return

        url_lower = url_str.lower()

        # 1. Checa extensões diretas de arquivo
        is_media = any(url_lower.endswith(ext) or (ext + "?") in url_lower for ext in self.media_extensions)

        # 2. Checa palavras-chave de stream (HLS / m3u8)
        if not is_media:
            is_media = any(keyword in url_lower for keyword in self.media_keywords)

        if is_media:
            # Ignora segmentos pequenos .ts genéricos para não poluir
            if ".ts?" in url_lower or url_lower.endswith(".ts"):
                if "segment" in url_lower or "fragment" in url_lower:
                    return

            self.captured_urls.add(url_str)
            self.signal_handler.media_detected.emit(url_str, info.resourceType())


class InterceptorSignals(QObject):
    """Sinais do PySide6 para notificação em tempo real."""
    media_detected = Signal(str, int)  # (media_url, resource_type)


# Instância global do interceptador
url_interceptor = PRTUrlRequestInterceptor()