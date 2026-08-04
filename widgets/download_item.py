"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTDownloadItem

Description:
    Reusable widget representing a single active download.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from theme.manager import ThemeManager
from widgets.progress import PRTProgressBar


class PRTDownloadItem(QFrame):
    """Reusable widget representing a download."""

    def __init__(
        self,
        title: str,
        source: str,
        downloaded: str,
        total: str,
        progress: int,
        speed: str,
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(parent)

        self._title = title
        self._source = source
        self._downloaded = downloaded
        self._total = total
        self._speed = speed

        self._thumbnail = QLabel("64x64")

        self._title_label = QLabel(title)
        self._info_label = QLabel(
            f"{source} • {downloaded} de {total}"
        )

        self._speed_label = QLabel(speed)
        self._percent_label = QLabel(f"{progress}%")

        self._progress = PRTProgressBar(progress)

        self._build_ui()

    def _build_ui(self) -> None:

        self.setObjectName("PRTDownloadItem")

        self.setStyleSheet(
            """
            QFrame#PRTDownloadItem{
                background:transparent;
                border:none;
            }
            """
        )

        layout = QGridLayout(self)

        layout.setContentsMargins(8,8,8,8)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(6)

        self._thumbnail.setFixedSize(64,64)

        self._thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._thumbnail.setStyleSheet(
            """
            background:#3A3F46;
            border-radius:6px;
            color:#909090;
            """
        )

        self._title_label.setStyleSheet(
            f"""
            color:{ThemeManager.text_color()};
            font-size:12pt;
            font-weight:600;
            """
        )

        self._info_label.setStyleSheet(
            """
            color:#A7ADB5;
            font-size:10pt;
            """
        )

        self._speed_label.setStyleSheet(
            """
            color:#65D46E;
            font-size:10pt;
            font-weight:600;
            """
        )

        self._percent_label.setStyleSheet(
            """
            color:#D0D0D0;
            font-size:10pt;
            """
        )

        self._progress.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout.addWidget(self._thumbnail,0,0,3,1)

        layout.addWidget(self._title_label,0,1)

        layout.addWidget(
            self._speed_label,
            0,
            2,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        layout.addWidget(self._info_label,1,1)

        layout.addWidget(
            self._percent_label,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        layout.addWidget(self._progress,2,1,1,2)