"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Widgets
Class......: PRTVideoPlayerWidget

Description:
    Custom PySide6 video player with control panel, seek slider,
    volume control, duration labels, and sleek dark UI.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from PySide6.QtCore import Qt, QUrl, QTime
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QFrame,
    QStyle
)


class PRTVideoPlayerWidget(QWidget):
    """Componente reutilizável de Player de Vídeo."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._current_file_path = ""
        self._is_slider_down = False

        self._init_player()
        self._build_ui()
        self._connect_signals()

    def _init_player(self) -> None:
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.8)  # Volume inicial em 80%

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tela de Vídeo
        self.video_container = QFrame()
        self.video_container.setStyleSheet("background-color: #000000; border-radius: 8px;")
        container_layout = QVBoxLayout(self.video_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget()
        self.player.setVideoOutput(self.video_widget)
        container_layout.addWidget(self.video_widget)

        main_layout.addWidget(self.video_container, stretch=1)

        # Barra de Controles
        controls_frame = QFrame()
        controls_frame.setFixedHeight(60)
        controls_frame.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border-top: 1px solid #26262B;
            }
            """
        )
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(15, 6, 15, 6)
        controls_layout.setSpacing(4)

        # 1. Slider de Progresso
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 0)
        self.seek_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 4px;
                background: #28282D;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #007ACC;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:hover {
                background: #007ACC;
            }
            """
        )
        controls_layout.addWidget(self.seek_slider)

        # 2. Botões e Informações de Tempo
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)

        # Botão Play / Pause
        self.btn_play = QPushButton("▶")
        self.btn_play.setFixedSize(32, 32)
        self.btn_play.setCursor(Qt.PointingHandCursor)
        self.btn_play.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border-radius: 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
            """
        )
        bottom_row.addWidget(self.btn_play)

        # Título do Vídeo Ativo
        self.lbl_title = QLabel("Nenhum vídeo selecionado")
        self.lbl_title.setStyleSheet("color: #FFFFFF; font-weight: 500; font-size: 12px;")
        bottom_row.addSpacing(10)
        bottom_row.addWidget(self.lbl_title)

        bottom_row.addStretch()

        # Rótulo do Tempo (00:00 / 00:00)
        self.lbl_time = QLabel("00:00 / 00:00")
        self.lbl_time.setStyleSheet("color: #8E8E93; font-size: 11px;")
        bottom_row.addWidget(self.lbl_time)
        bottom_row.addSpacing(15)

        # Ícone de Volume
        lbl_vol_icon = QLabel("🔊")
        lbl_vol_icon.setStyleSheet("color: #8E8E93; font-size: 12px;")
        bottom_row.addWidget(lbl_vol_icon)

        # Slider de Volume
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 3px;
                background: #28282D;
                border-radius: 1px;
            }
            QSlider::sub-page:horizontal {
                background: #8E8E93;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                width: 8px;
                margin: -3px 0;
                border-radius: 4px;
            }
            """
        )
        bottom_row.addWidget(self.volume_slider)

        controls_layout.addLayout(bottom_row)
        main_layout.addWidget(controls_frame)

    def _connect_signals(self) -> None:
        self.btn_play.clicked.connect(self.toggle_play)

        self.player.positionChanged.connect(self._on_position_changed)
        self.player.durationChanged.connect(self._on_duration_changed)

        self.seek_slider.sliderPressed.connect(self._on_slider_pressed)
        self.seek_slider.sliderReleased.connect(self._on_slider_released)
        self.seek_slider.sliderMoved.connect(self._on_slider_moved)

        self.volume_slider.valueChanged.connect(self._on_volume_changed)

    def load_video(self, file_path: str, title: str = "") -> None:
        """Carrega e inicia a execução do arquivo de vídeo local."""
        if not os.path.exists(file_path):
            return

        self._current_file_path = file_path
        self.lbl_title.setText(title or os.path.basename(file_path))

        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.play()
        self.btn_play.setText("⏸")

    def toggle_play(self) -> None:
        """Alterna entre Play e Pause."""
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play.setText("▶")
        else:
            if self._current_file_path:
                self.player.play()
                self.btn_play.setText("⏸")

    def _on_position_changed(self, position_ms: int) -> None:
        if not self._is_slider_down:
            self.seek_slider.setValue(position_ms)
        self._update_time_label(position_ms, self.player.duration())

    def _on_duration_changed(self, duration_ms: int) -> None:
        self.seek_slider.setRange(0, duration_ms)
        self._update_time_label(self.player.position(), duration_ms)

    def _on_slider_pressed(self) -> None:
        self._is_slider_down = True

    def _on_slider_released(self) -> None:
        self._is_slider_down = False
        self.player.setPosition(self.seek_slider.value())

    def _on_slider_moved(self, position: int) -> None:
        self._update_time_label(position, self.player.duration())

    def _on_volume_changed(self, value: int) -> None:
        self.audio_output.setVolume(value / 100.0)

    def _update_time_label(self, current_ms: int, total_ms: int) -> None:
        curr_str = self._format_ms(current_ms)
        tot_str = self._format_ms(total_ms)
        self.lbl_time.setText(f"{curr_str} / {tot_str}")

    @staticmethod
    def _format_ms(ms: int) -> str:
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        hours = int((ms / (1000 * 60 * 60)) % 24)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
