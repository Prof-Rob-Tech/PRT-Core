"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: DashboardPage

Description:
    Real-time dynamic dashboard for PRT NEXUS. Displays real storage usage,
    active downloads count, completion stats, and live transfer speeds.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from services.download_manager import PRTDownloadManager


class MetricCard(QFrame):
    """Card reutilizável para exibição de métricas dinamicas."""

    def __init__(self, title: str, value: str, icon: str, color: str = "#007ACC") -> None:
        super().__init__()
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }}
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        header_layout = QHBoxLayout()
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet("font-size: 18px; border: none;")
        header_layout.addWidget(lbl_icon)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #8E8E93; font-size: 12px; font-weight: bold; border: none;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(
            f"color: {color}; font-size: 22px; font-weight: bold; border: none; margin-top: 5px;"
        )
        layout.addWidget(self.lbl_value)

    def set_value(self, value: str) -> None:
        self.lbl_value.setText(value)


class DashboardPage(QWidget):
    """Página do Dashboard com métricas dinâmicas reais."""

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._connect_signals()

        # Timer para atualizar métricas de disco e velocidade a cada 1.5s
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_app_stats)
        self._timer.start(1500)

        self.update_app_stats()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Cabeçalho
        lbl_header = QLabel("Visão Geral do Sistema")
        lbl_header.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_header)

        # Linha de Cards de Métricas
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.card_active = MetricCard("DOWNLOADS ATIVOS", "0", "⚡", "#007ACC")
        self.card_completed = MetricCard("AULAS CONCLUÍDAS", "0", "✅", "#34C759")
        self.card_storage = MetricCard("ESPAÇO UTILIZADO", "0.0 MB", "💾", "#FF9500")
        self.card_speed = MetricCard("VELOCIDADE ATUAL", "0.0 KB/s", "🚀", "#AF52DE")

        cards_layout.addWidget(self.card_active)
        cards_layout.addWidget(self.card_completed)
        cards_layout.addWidget(self.card_storage)
        cards_layout.addWidget(self.card_speed)

        layout.addLayout(cards_layout)

        # Painel de Resumo / Estado do Motor
        card_status = QFrame()
        card_status.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            """
        )
        status_layout = QVBoxLayout(card_status)
        status_layout.setContentsMargins(20, 20, 20, 20)
        status_layout.setSpacing(15)

        lbl_status_title = QLabel("🖥️ Status do Motor yt-dlp & Sistema")
        lbl_status_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold; border: none;")
        status_layout.addWidget(lbl_status_title)

        self.lbl_folder_path = QLabel("Diretório Atual: ...")
        self.lbl_folder_path.setStyleSheet("color: #8E8E93; font-size: 12px; border: none;")
        status_layout.addWidget(self.lbl_folder_path)

        # Barra de Progresso Visual de Utilização
        self.lbl_activity_title = QLabel("Atividade Recente dos Workers")
        self.lbl_activity_title.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold; border: none;")
        status_layout.addWidget(self.lbl_activity_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #1C1C1F;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 4px;
            }
            """
        )
        status_layout.addWidget(self.progress_bar)

        layout.addWidget(card_status)
        layout.addStretch()

    def _connect_signals(self) -> None:
        """Conecta com o Gerenciador de Downloads para reatividade instantânea."""
        mgr = PRTDownloadManager.instance()
        mgr.download_added.connect(self.update_app_stats)
        mgr.progress_updated.connect(lambda *args: self.update_app_stats())
        mgr.download_completed.connect(lambda *args: self.update_app_stats())
        mgr.cleared_signal.connect(self.update_app_stats)

    def update_app_stats(self) -> None:
        """Calcula estatísticas reais e atualiza a interface."""
        mgr = PRTDownloadManager.instance()
        download_folder = mgr.get_download_folder()

        # Atualiza a label do caminho
        self.lbl_folder_path.setText(f"📁 Pasta Ativa: {download_folder}")

        # 1. Contagem de downloads ativos e concluídos na fila
        active_count = sum(1 for item in mgr.downloads if item.status in ["Baixando", "Iniciando..."])

        # 2. Arquivos baixados reais no disco
        total_files = 0
        total_bytes = 0

        if os.path.exists(download_folder):
            for root, _, files in os.walk(download_folder):
                for f in files:
                    total_files += 1
                    file_path = os.path.join(root, f)
                    try:
                        total_bytes += os.path.getsize(file_path)
                    except OSError:
                        pass

        # 3. Formatação do tamanho em MB/GB
        if total_bytes >= 1024 * 1024 * 1024:
            size_str = f"{total_bytes / (1024 ** 3):.2f} GB"
        else:
            size_str = f"{total_bytes / (1024 ** 2):.1f} MB"

        # 4. Velocidade atual (pega a maior velocidade informada ou status)
        active_speeds = [item.speed for item in mgr.downloads if item.speed not in ["-", "0.0 KB/s"]]
        current_speed = active_speeds[0] if active_speeds else "0.0 KB/s"

        # Atualização dos Cards
        self.card_active.set_value(str(active_count))
        self.card_completed.set_value(str(total_files))
        self.card_storage.set_value(size_str)
        self.card_speed.set_value(current_speed)

        # Atualiza barra de progresso com base na média dos ativos
        if active_count > 0:
            avg_progress = int(sum(item.progress for item in mgr.downloads) / len(mgr.downloads))
            self.progress_bar.setValue(avg_progress)
        else:
            self.progress_bar.setValue(0)