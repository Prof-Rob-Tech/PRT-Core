"""
===========================================================
PRT Labs - Icon Generator
Gera automaticamente os arquivos icon.ico e icon.png no
diretório resources/ usando PySide6 QPainter.
===========================================================
"""

import os
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QGuiApplication,
    QImage,
    QPainter,
    QColor,
    QFont,
    QPainterPath,
    QPen,
    QLinearGradient
)


def generate_prt_icon() -> None:
    # Inicializa o contexto gráfico do Qt
    app = QGuiApplication([])

    size = 256
    image = QImage(size, size, QImage.Format_ARGB32)
    image.fill(Qt.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing)

    # 1. Fundo escuro com cantos arredondados
    rect = QRectF(10, 10, size - 20, size - 20)
    bg_path = QPainterPath()
    bg_path.addRoundedRect(rect, 48, 48)

    grad = QLinearGradient(0, 0, size, size)
    grad.setColorAt(0.0, QColor("#18181B"))
    grad.setColorAt(1.0, QColor("#09090B"))
    painter.fillPath(bg_path, grad)

    # Borda Azul Neon (#007ACC)
    pen = QPen(QColor("#007ACC"), 6)
    painter.setPen(pen)
    painter.drawPath(bg_path)

    # 2. Ícone de Play Neon no Centro
    play_path = QPainterPath()
    play_path.moveTo(98, 72)
    play_path.lineTo(172, 115)
    play_path.lineTo(98, 158)
    play_path.closeSubpath()

    painter.fillPath(play_path, QColor("#00A6FF"))

    # 3. Texto "PRT" estilizado na parte inferior
    font = QFont("Segoe UI", 28, QFont.Bold)
    painter.setFont(font)
    painter.setPen(QColor("#FFFFFF"))
    painter.drawText(QRectF(0, 172, size, 50), Qt.AlignCenter, "PRT")

    painter.end()

    # Cria a pasta resources se não existir e salva o ícone
    os.makedirs("resources", exist_ok=True)
    ico_path = os.path.join("resources", "icon.ico")
    png_path = os.path.join("resources", "icon.png")

    image.save(ico_path)
    image.save(png_path)

    print(f"✨ Ícone gerado com sucesso!")
    print(f" └─> {os.path.abspath(ico_path)}")


if __name__ == "__main__":
    generate_prt_icon()