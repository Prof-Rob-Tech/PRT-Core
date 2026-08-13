"""
===========================================================
PRT Labs - UI / Pages
Class: DownloadsPage
Description: Gerenciador de Downloads com suporte anti-bloqueio 403 (yt-dlp)
             e tratamento de erros limpos no PySide6.
===========================================================
"""

import os
import sys
import re
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar, QHeaderView,
    QFileDialog, QMessageBox, QFrame
)

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False


def sanitize_filename(name: str) -> str:
    """Higieniza o nome do arquivo para gravação em disco."""
    if not name or name.startswith("http://") or name.startswith("https://"):
        return "Video_Download"
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name)
    return cleaned.strip()


class DownloadWorker(QThread):
    progress_signal = Signal(float, str)
    title_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, url: str, quality: str, download_folder: str, custom_title: str = None, parent=None):
        super().__init__(parent)
        self.url = url
        self.quality = quality
        self.download_folder = download_folder
        self.custom_title = sanitize_filename(custom_title) if custom_title else ""

    def run(self):
        if not HAS_YTDLP:
            self.finished_signal.emit(False, "yt-dlp não está instalado. Execute: pip install -U yt-dlp")
            return

        final_title = self.custom_title or "Video_Download"
        self.title_signal.emit(final_title)

        # Seleção de qualidade
        format_option = "bestvideo+bestaudio/best"
        if "1080p" in self.quality:
            format_option = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        elif "720p" in self.quality:
            format_option = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        elif "480p" in self.quality:
            format_option = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
        elif "Áudio" in self.quality or "MP3" in self.quality:
            format_option = "bestaudio/best"

        def ytdl_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                speed = d.get('_speed_str', '').strip()
                eta = d.get('_eta_str', '').strip()

                if total > 0:
                    pct = (downloaded / total) * 100
                    pct = min(pct, 99.0)
                    status_str = f"{speed} | Restante: {eta}"
                    self.progress_signal.emit(pct, status_str)
                else:
                    mb_downloaded = downloaded / (1024 * 1024) if downloaded else 0
                    status_str = f"Baixando... {mb_downloaded:.1f} MB ({speed})"
                    self.progress_signal.emit(50.0, status_str)

            elif d['status'] == 'finished':
                self.progress_signal.emit(99.0, "Processando / Salvando...")

        output_template = os.path.join(self.download_folder, f"{final_title}.%(ext)s")

        # Configurações com Bypass Anti-403 Forbidden para YouTube
        ydl_opts = {
            'format': format_option,
            'outtmpl': output_template,
            'progress_hooks': [ytdl_hook],
            'quiet': True,
            'no_warnings': True,
            'no_color': True,  # Remove códigos de cor tipo ANSI ([]0;31m) das mensagens
            'nocheckcertificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web', 'mweb']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            },
        }

        if "Áudio" in self.quality or "MP3" in self.quality:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.progress_signal.emit(100.0, "Download Concluído!")
            self.finished_signal.emit(True, "Sucesso")
        except Exception as e:
            # Limpa mensagens de erro brutas do terminal
            clean_error = str(e).replace('\033[0;31mERROR:\033[0m', '').strip()
            self.finished_signal.emit(False, clean_error)


class DownloadsPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.active_workers = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        header_card = QFrame()
        header_card.setObjectName("cardFrame")
        h_layout = QHBoxLayout(header_card)

        title = QLabel("⬇️ Gerenciador de Downloads")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        h_layout.addWidget(title)
        h_layout.addStretch()

        btn_folder = QPushButton("📁 Mudar Pasta de Destino")
        btn_folder.setCursor(Qt.PointingHandCursor)
        btn_folder.clicked.connect(self._select_download_folder)
        h_layout.addWidget(btn_folder)

        layout.addWidget(header_card)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nome / Mídia", "Tipo", "Qualidade", "Progresso", "Ação"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 260)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

    def _select_download_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Selecione a pasta de destino", self.download_folder)
        if folder:
            self.download_folder = folder

    def add_download(self, url: str, media_type: str = "VIDEO", quality: str = "1080p", title: str = None) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row, 60)

        initial_name = title if title else "Iniciando Download..."
        item_name = QTableWidgetItem(initial_name)
        self.table.setItem(row, 0, item_name)

        item_type = QTableWidgetItem(media_type)
        item_type.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 1, item_type)

        item_quality = QTableWidgetItem(quality)
        item_quality.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, item_quality)

        progress_widget = QWidget()
        p_layout = QVBoxLayout(progress_widget)
        p_layout.setContentsMargins(6, 4, 6, 4)

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setFixedHeight(14)

        status_label = QLabel("Conectando...")
        status_label.setStyleSheet("font-size: 11px; color: #A1A1AA;")

        p_layout.addWidget(progress_bar)
        p_layout.addWidget(status_label)
        self.table.setCellWidget(row, 3, progress_widget)

        btn_action = QPushButton("📁 Abrir Pasta")
        btn_action.setCursor(Qt.PointingHandCursor)
        btn_action.clicked.connect(lambda: os.startfile(self.download_folder) if sys.platform == "win32" else None)
        self.table.setCellWidget(row, 4, btn_action)

        worker = DownloadWorker(url, quality, self.download_folder, custom_title=title)
        self.active_workers[row] = worker

        worker.title_signal.connect(lambda t, r=row: self._update_title(r, t))
        worker.progress_signal.connect(lambda pct, st, pb=progress_bar, sl=status_label: self._update_progress(pb, sl, pct, st))
        worker.finished_signal.connect(lambda ok, msg, pb=progress_bar, sl=status_label, r=row: self._on_download_finished(r, ok, msg, pb, sl))

        worker.start()

    def _update_title(self, row: int, title_text: str) -> None:
        item = self.table.item(row, 0)
        if item:
            item.setText(title_text)

    def _update_progress(self, pbar: QProgressBar, status_lbl: QLabel, percentage: float, status_text: str) -> None:
        pbar.setValue(int(percentage))
        status_lbl.setText(status_text)

    def _on_download_finished(self, row: int, success: bool, msg: str, pbar: QProgressBar, status_lbl: QLabel) -> None:
        if success:
            pbar.setValue(100)
            status_lbl.setText("✅ Download Concluído!")
            status_lbl.setStyleSheet("font-size: 11px; color: #10B981; font-weight: bold;")
        else:
            status_lbl.setText("❌ Erro no Download")
            status_lbl.setStyleSheet("font-size: 11px; color: #EF4444; font-weight: bold;")
            QMessageBox.critical(self, "Erro no Download", f"Falha ao baixar:\n{msg}")

        if row in self.active_workers:
            del self.active_workers[row]