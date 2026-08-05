"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: PRTSystemMonitor

Description:
    Real-time system hardware (CPU, RAM) and Network traffic monitor
    using psutil and PySide6 QTimer.

Developer..: Prof Rob Tech
===========================================================
"""

import time
from typing import Optional
from PySide6.QtCore import QObject, QTimer, Signal

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class PRTSystemMonitor(QObject):
    """Singleton service monitoring CPU, RAM, and Network I/O speeds."""

    # Sinais: (cpu_percent, ram_percent, download_speed_str, upload_speed_str, ram_used_gb, ram_total_gb)
    metrics_updated = Signal(float, float, str, str, float, float)

    _instance: Optional["PRTSystemMonitor"] = None

    @classmethod
    def instance(cls) -> "PRTSystemMonitor":
        if cls._instance is None:
            cls._instance = PRTSystemMonitor()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

        self._last_bytes_recv = 0
        self._last_bytes_sent = 0
        self._last_time = time.time()

        if HAS_PSUTIL:
            net_io = psutil.net_io_counters()
            self._last_bytes_recv = net_io.bytes_recv
            self._last_bytes_sent = net_io.bytes_sent
            # Chama uma vez para inicializar o contador interno de CPU do psutil
            psutil.cpu_percent(interval=None)

        self._timer = QTimer(self)
        self._timer.setInterval(1000)  # Atualiza a cada 1 segundo
        self._timer.timeout.connect(self._update_metrics)
        self._timer.start()

    def _update_metrics(self) -> None:
        if not HAS_PSUTIL:
            self.metrics_updated.emit(0.0, 0.0, "0.0 KB/s", "0.0 KB/s", 0.0, 0.0)
            return

        # CPU e RAM
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        ram_used_gb = mem.used / (1024 ** 3)
        ram_total_gb = mem.total / (1024 ** 3)

        # Tráfego de Rede
        now = time.time()
        net_io = psutil.net_io_counters()

        elapsed = now - self._last_time
        if elapsed <= 0:
            elapsed = 1.0

        rx_bytes = net_io.bytes_recv - self._last_bytes_recv
        tx_bytes = net_io.bytes_sent - self._last_bytes_sent

        self._last_bytes_recv = net_io.bytes_recv
        self._last_bytes_sent = net_io.bytes_sent
        self._last_time = now

        rx_speed = rx_bytes / elapsed
        tx_speed = tx_bytes / elapsed

        rx_str = self._format_speed(rx_speed)
        tx_str = self._format_speed(tx_speed)

        self.metrics_updated.emit(cpu, ram_percent, rx_str, tx_str, ram_used_gb, ram_total_gb)

    def _format_speed(self, speed_bytes: float) -> str:
        if speed_bytes >= 1024 * 1024:
            return f"{round(speed_bytes / (1024 * 1024), 1)} MB/s"
        elif speed_bytes >= 1024:
            return f"{round(speed_bytes / 1024, 1)} KB/s"
        else:
            return f"{round(speed_bytes, 1)} B/s"