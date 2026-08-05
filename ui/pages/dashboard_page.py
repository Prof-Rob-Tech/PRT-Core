"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: DashboardPage

Description:
    Real-time dashboard displaying system hardware metrics,
    network traffic speeds, and application download stats.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from services.download_manager import PRTDownloadManager
from services.system_monitor import PRTSystemMonitor
from ui.pages.base_page import BasePage


class DashboardMetricCard(QFrame):
    """Card visual estilizado para exibir métricas do sistema."""

    def __init__(self, title: str, icon: str, parent=None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 10px;
            }
            """
        )
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(10)

        # Header do Card
        header_layout = QHBoxLayout()
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #8E8E93; font-size: 13px; font-weight: bold; border: none;")

        header_layout.addWidget(lbl_icon)
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        self._layout.addLayout(header_layout)

        # Valor Principal
        self.lbl_value = QLabel("--")
        self.lbl_value.setStyleSheet("color: #FFFFFF; font-size: 26px; font-weight: bold; border: none;")
        self._layout.addWidget(self.lbl_value)

        # Subtítulo / Detalhe
        self.lbl_detail = QLabel("")
        self.lbl_detail.setStyleSheet("color: #007ACC; font-size: 12px; border: none;")
        self._layout.addWidget(self.lbl_detail)

        # Barra de Progresso
        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(6)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet(
            """
            QProgressBar {
                background-color: #1F1F23;
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 3px;
            }
            """
        )
        self._layout.addWidget(self.pbar)

    def update_data(self, value_str: str, detail_str: str, percent: int = 0) -> None:
        self.lbl_value.setText(value_str)
        self.lbl_detail.setText(detail_str)
        self.pbar.setValue(percent)


class DashboardPage(BasePage):
    """Página de Dashboard interativa com métricas de sistema ao vivo."""

    def __init__(self) -> None:
        super().__init__()

        self._layout = QVBoxLayout(self)
        self._configure()
        self._build_ui()
        self._connect_signals()

    def _configure(self) -> None:
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        title = QLabel("Dashboard do Sistema")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(15)

        # Cards
        self.card_cpu = DashboardMetricCard("Processador (CPU)", "💻")
        self.card_ram = DashboardMetricCard("Memória (RAM)", "⚡")
        self.card_net_down = DashboardMetricCard("Download de Rede", "📥")
        self.card_net_up = DashboardMetricCard("Upload de Rede", "📤")

        self.card_storage = DashboardMetricCard("Cursos em Disco", "🎬")
        self.card_active_dl = DashboardMetricCard("Downloads na Fila", "⚡")

        grid.addWidget(self.card_cpu, 0, 0)
        grid.addWidget(self.card_ram, 0, 1)
        grid.addWidget(self.card_net_down, 0, 2)

        grid.addWidget(self.card_net_up, 1, 0)
        grid.addWidget(self.card_storage, 1, 1)
        grid.addWidget(self.card_active_dl, 1, 2)

        self._layout.addLayout(grid)
        self._layout.addStretch()

        self._update_app_stats()

    def showEvent(self, event) -> None:
        """Atualiza dados do app quando a página é visualizada."""
        super().showEvent(event)
        self._update_app_stats()

    def _connect_signals(self) -> None:
        """Conecta com o monitor de hardware e gerenciador de downloads."""
        monitor = PRTSystemMonitor.instance()
        monitor.metrics_updated.connect(self._on_metrics_updated)

        manager = PRTDownloadManager.instance()
        manager.progress_updated.connect(lambda *_: self._update_app_stats())
        manager.cleared_signal.connect(self._update_app_stats)

    def _on_metrics_updated(
        self,
        cpu: float,
        ram: float,
        rx_speed: str,
        tx_speed: str,
        ram_used_gb: float,
        ram_total_gb: float,
    ) -> None:
        # CPU
        self.card_cpu.update_data(
            value_str=f"{int(cpu)}%",
            detail_str=f"Uso de Processamento",
            percent=int(cpu),
        )

        # RAM
        self.card_ram.update_data(
            value_str=f"{int(ram)}%",
            detail_str=f"{ram_used_gb:.1f} GB de {ram_total_gb:.1f} GB",
            percent=int(ram),
        )

        # Rede Download
        self.card_net_down.update_data(
            value_str=rx_speed,
            detail_str="Tráfego de Entrada",
            percent=100 if "MB/s" in rx_speed else 30,
        )

        # Rede Upload
        self.card_net_up.update_data(
            value_str=tx_speed,
            detail_str="Tráfego de Saída",
            percent=100 if "MB/s" in tx_speed else 15,
        )

    def _update_app_stats(self) -> None:
        """Calcula estatísticas de arquivos locais e downloads ativos."""
        manager = PRTDownloadManager.instance()
        
        # Downloads ativos
        active_count = len([d for d in manager.downloads if d.status == "Baixando"])
        total_in_manager = len(manager.downloads)

        self.card_active_dl.update_data(
            value_str=f"{active_count} ativos",
            detail_str=f"Total na lista: {total_in_manager}",
            percent=100 if active_count > 0 else 0,
        )

        # Cursos baixados em disco
        folder_path = manager.get_download_folder()
        video_count = 0
        total_size = 0

        if os.path.exists(folder_path):
            video_exts = (".mp4", ".mkv", ".webm", ".avi", ".mov", ".ts", ".m4a")
            for root, _, files in os.walk(folder_path):
                for f in files:
                    if f.lower().endswith(video_exts):
                        video_count += 1
                        total_size += os.path.getsize(os.path.join(root, f))

        size_str = self._format_bytes(total_size)
        self.card_storage.update_data(
            value_str=f"{video_count} vídeos",
            detail_str=f"Espaço ocupado: {size_str}",
            percent=min(video_count * 10, 100),
        )

    def _format_bytes(self, size_bytes: float) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
