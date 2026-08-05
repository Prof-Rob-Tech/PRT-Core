"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: CoursesPage

Description:
    Advanced Video Player for PRT NEXUS supporting custom speed controls,
    global application-level keyboard shortcuts (F / ESC / Space),
    position memory per video, and direct local course library playback.

Developer..: Prof Rob Tech
===========================================================
"""

import json
import os
from PySide6.QtCore import Qt, QTime, QUrl, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from services.download_manager import PRTDownloadManager


class ClickableVideoWidget(QVideoWidget):
    """QVideoWidget personalizado com suporte a duplo clique e teclas de escape/fullscreen."""

    double_clicked = Signal()
    escape_pressed = Signal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event) -> None:
        self.setFocus()
        super().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.escape_pressed.emit()
            event.accept()
            return
        super().keyPressEvent(event)


class CoursesPage(QWidget):
    """Página do Player de Vídeo e Aulas do PRT NEXUS."""

    def __init__(self) -> None:
        super().__init__()
        self._current_video_path = ""
        self._history_file = self._get_history_path()

        self._build_ui()
        self._setup_player()
        self._setup_shortcuts()
        self._load_history()

    def _get_history_path(self) -> str:
        appdata = os.getenv("APPDATA") or os.path.expanduser("~")
        config_dir = os.path.join(appdata, "PRT NEXUS")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "playback_history.json")

    def _load_history(self) -> dict:
        if os.path.exists(self._history_file):
            try:
                with open(self._history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_position(self, video_path: str, position_ms: int) -> None:
        if not video_path or position_ms <= 0:
            return
        history = self._load_history()
        history[video_path] = position_ms
        try:
            with open(self._history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"[Player Error] Não foi possível salvar histórico: {e}")

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Cabeçalho e Seleção de Vídeo
        top_layout = QHBoxLayout()
        self.lbl_title = QLabel("🎬 Aulas e Cursos Baixados")
        self.lbl_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold;")
        top_layout.addWidget(self.lbl_title)
        top_layout.addStretch()

        btn_open = QPushButton("📁 Abrir Vídeo")
        btn_open.setCursor(Qt.PointingHandCursor)
        btn_open.setStyleSheet(
            """
            QPushButton {
                background-color: #26262B;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #323238; }
            """
        )
        btn_open.clicked.connect(self._open_file_dialog)
        top_layout.addWidget(btn_open)

        layout.addLayout(top_layout)

        # Tela de Vídeo Customizada
        self.video_widget = ClickableVideoWidget()
        self.video_widget.setStyleSheet("background-color: #000000; border-radius: 8px;")
        self.video_widget.double_clicked.connect(self._toggle_fullscreen)
        self.video_widget.escape_pressed.connect(self._exit_fullscreen)
        layout.addWidget(self.video_widget, stretch=1)

        # Barra de Controles
        controls_card = QFrame()
        controls_card.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            """
        )
        controls_vlayout = QVBoxLayout(controls_card)
        controls_vlayout.setContentsMargins(12, 10, 12, 10)
        controls_vlayout.setSpacing(8)

        # 1. Slider de Progresso + Tempo
        progress_layout = QHBoxLayout()
        self.lbl_time_current = QLabel("00:00")
        self.lbl_time_current.setStyleSheet("color: #8E8E93; font-size: 11px;")

        self.slider_progress = QSlider(Qt.Horizontal)
        self.slider_progress.setRange(0, 0)
        self.slider_progress.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 4px;
                background: #26262B;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #007ACC;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                width: 12px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 6px;
            }
            """
        )
        self.slider_progress.sliderMoved.connect(self._set_position)

        self.lbl_time_total = QLabel("00:00")
        self.lbl_time_total.setStyleSheet("color: #8E8E93; font-size: 11px;")

        progress_layout.addWidget(self.lbl_time_current)
        progress_layout.addWidget(self.slider_progress)
        progress_layout.addWidget(self.lbl_time_total)

        controls_vlayout.addLayout(progress_layout)

        # 2. Botões de Ação (Play, Volume, Velocidade, Fullscreen)
        action_layout = QHBoxLayout()

        self.btn_play = QPushButton("▶️ Play")
        self.btn_play.setCursor(Qt.PointingHandCursor)
        self.btn_play.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover { background-color: #0098FF; }
            """
        )
        self.btn_play.clicked.connect(self._toggle_play)
        action_layout.addWidget(self.btn_play)

        # Volume
        lbl_vol_icon = QLabel("🔊")
        lbl_vol_icon.setStyleSheet("border: none; font-size: 14px;")
        action_layout.addWidget(lbl_vol_icon)

        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(80)
        self.slider_volume.setFixedWidth(90)
        self.slider_volume.setStyleSheet(self.slider_progress.styleSheet())
        self.slider_volume.valueChanged.connect(self._set_volume)
        action_layout.addWidget(self.slider_volume)

        action_layout.addStretch()

        # Seletor de Velocidade
        lbl_speed = QLabel("Velocidade:")
        lbl_speed.setStyleSheet("color: #8E8E93; font-size: 12px; border: none;")
        action_layout.addWidget(lbl_speed)

        self.combo_speed = QComboBox()
        self.combo_speed.addItems(["0.5x", "1.0x (Normal)", "1.25x", "1.5x", "2.0x"])
        self.combo_speed.setCurrentIndex(1)
        self.combo_speed.setStyleSheet(
            """
            QComboBox {
                background-color: #1C1C1F;
                color: #FFFFFF;
                border: 1px solid #26262B;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #1C1C1F;
                color: #FFFFFF;
                selection-background-color: #007ACC;
            }
            """
        )
        self.combo_speed.currentIndexChanged.connect(self._change_speed)
        action_layout.addWidget(self.combo_speed)

        # Botão Tela Cheia
        btn_fullscreen = QPushButton("⛶ Tela Cheia (F)")
        btn_fullscreen.setCursor(Qt.PointingHandCursor)
        btn_fullscreen.setStyleSheet(
            """
            QPushButton {
                background-color: #26262B;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #323238; }
            """
        )
        btn_fullscreen.clicked.connect(self._toggle_fullscreen)
        action_layout.addWidget(btn_fullscreen)

        controls_vlayout.addLayout(action_layout)
        layout.addWidget(controls_card)

    def _setup_player(self) -> None:
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        self.player.positionChanged.connect(self._on_position_changed)
        self.player.durationChanged.connect(self._on_duration_changed)

    def _setup_shortcuts(self) -> None:
        """Configura atalhos globais no nível de aplicativo (Qt.ApplicationShortcut)."""
        # Atalho 'F' para alternar Tela Cheia
        self.shortcut_f = QShortcut(QKeySequence(Qt.Key_F), self)
        self.shortcut_f.setContext(Qt.ApplicationShortcut)
        self.shortcut_f.activated.connect(self._toggle_fullscreen)

        # Atalho 'ESC' para sair da Tela Cheia
        self.shortcut_esc = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.shortcut_esc.setContext(Qt.ApplicationShortcut)
        self.shortcut_esc.activated.connect(self._exit_fullscreen)

        # Atalho 'Espaço' para Play / Pause
        self.shortcut_space = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.shortcut_space.setContext(Qt.ApplicationShortcut)
        self.shortcut_space.activated.connect(self._toggle_play)

    def load_video(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            return

        self._current_video_path = file_path
        self.lbl_title.setText(f"🎬 {os.path.basename(file_path)}")
        self.player.setSource(QUrl.fromLocalFile(file_path))

        history = self._load_history()
        saved_pos = history.get(file_path, 0)
        if saved_pos > 0:
            self.player.setPosition(saved_pos)

        self.player.play()
        self.btn_play.setText("⏸️ Pausa")

    def _open_file_dialog(self) -> None:
        default_dir = PRTDownloadManager.instance().get_download_folder()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Aula ou Vídeo",
            default_dir,
            "Vídeos (*.mp4 *.mkv *.avi *.webm *.mov)"
        )
        if file_path:
            self.load_video(file_path)

    def _toggle_play(self) -> None:
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play.setText("▶️ Play")
            self._save_position(self._current_video_path, self.player.position())
        else:
            self.player.play()
            self.btn_play.setText("⏸️ Pausa")

    def _set_position(self, position: int) -> None:
        self.player.setPosition(position)

    def _set_volume(self, value: int) -> None:
        self.audio_output.setVolume(value / 100.0)

    def _change_speed(self) -> None:
        speed_map = {
            "0.5x": 0.5,
            "1.0x (Normal)": 1.0,
            "1.25x": 1.25,
            "1.5x": 1.5,
            "2.0x": 2.0,
        }
        text = self.combo_speed.currentText()
        rate = speed_map.get(text, 1.0)
        self.player.setPlaybackRate(rate)

    def _toggle_fullscreen(self) -> None:
        if self.video_widget.isFullScreen():
            self._exit_fullscreen()
        else:
            self.video_widget.setFullScreen(True)

    def _exit_fullscreen(self) -> None:
        if self.video_widget.isFullScreen():
            self.video_widget.setFullScreen(False)

    def _on_position_changed(self, position: int) -> None:
        self.slider_progress.setValue(position)
        self.lbl_time_current.setText(self._format_time(position))

        if position > 0 and position % 5000 < 500:
            self._save_position(self._current_video_path, position)

    def _on_duration_changed(self, duration: int) -> None:
        self.slider_progress.setRange(0, duration)
        self.lbl_time_total.setText(self._format_time(duration))

    def _format_time(self, ms: int) -> str:
        time = QTime(0, 0, 0).addMSecs(ms)
        return time.toString("hh:mm:ss") if ms >= 3600000 else time.toString("mm:ss")