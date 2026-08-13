"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: SettingsPage

Description:
    Settings Page for PRT NEXUS with direct theme application
    and system preferences management.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

THEMES = {
    "dark": """
        QMainWindow, QWidget#centralWidget, QStackedWidget {
            background-color: #09090B;
            color: #F4F4F5;
            font-family: 'Segoe UI', sans-serif;
        }
        PRTSidebar, QFrame#sidebar {
            background-color: #121215;
            border-right: 1px solid #27272A;
        }
        QWidget#browserNavBar {
            background-color: #121215;
            border-bottom: 1px solid #27272A;
        }
        QFrame#cardFrame {
            background-color: #121215;
            border: 1px solid #27272A;
            border-radius: 8px;
        }
        QLineEdit {
            background-color: #18181B;
            color: #FFFFFF;
            border: 1px solid #27272A;
            border-radius: 6px;
            padding: 8px 12px;
        }
        QLineEdit:focus { border: 1px solid #6366F1; }
        QPushButton {
            background-color: #27272A;
            color: #FFFFFF;
            border: 1px solid #3F3F46;
            border-radius: 6px;
            padding: 8px 14px;
        }
        QPushButton:hover { background-color: #3F3F46; }
        QLabel { color: #F4F4F5; }
    """,
    "light": """
        QMainWindow, QWidget#centralWidget, QStackedWidget {
            background-color: #F8FAFC;
            color: #0F172A;
            font-family: 'Segoe UI', sans-serif;
        }
        PRTSidebar, QFrame#sidebar {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }
        QWidget#browserNavBar {
            background-color: #FFFFFF;
            border-bottom: 1px solid #E2E8F0;
        }
        QFrame#cardFrame {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
        }
        QLineEdit {
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 8px 12px;
        }
        QLineEdit:focus { border: 1px solid #6366F1; }
        QPushButton {
            background-color: #E2E8F0;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 8px 14px;
        }
        QPushButton:hover { background-color: #CBD5E1; }
        QLabel { color: #0F172A; }
    """,
    "cyber": """
        QMainWindow, QWidget#centralWidget, QStackedWidget {
            background-color: #0B0518;
            color: #00F0FF;
            font-family: 'Segoe UI', sans-serif;
        }
        PRTSidebar, QFrame#sidebar {
            background-color: #150A2A;
            border-right: 1px solid #FF007F;
        }
        QWidget#browserNavBar {
            background-color: #150A2A;
            border-bottom: 1px solid #FF007F;
        }
        QFrame#cardFrame {
            background-color: #150A2A;
            border: 1px solid #FF007F;
            border-radius: 8px;
        }
        QLineEdit {
            background-color: #1A0D36;
            color: #00F0FF;
            border: 1px solid #FF007F;
            border-radius: 6px;
            padding: 8px 12px;
        }
        QLineEdit:focus { border: 1px solid #00F0FF; }
        QPushButton {
            background-color: #24114A;
            color: #00F0FF;
            border: 1px solid #00F0FF;
            border-radius: 6px;
            padding: 8px 14px;
        }
        QPushButton:hover { background-color: #381A72; }
        QLabel { color: #00F0FF; }
    """,
}


class SettingsPage(QWidget):
    """Página de Configurações do PRT NEXUS."""

    theme_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.settings = QSettings("PRTLabs", "PRTNexus")
        self.theme_buttons = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título da Página
        lbl_title = QLabel("⚙️ Configurações do Sistema")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_title)

        # CARD DE SELEÇÃO DE TEMA
        theme_card = QFrame()
        theme_card.setObjectName("cardFrame")
        theme_card_layout = QVBoxLayout(theme_card)
        theme_card_layout.setContentsMargins(15, 15, 15, 15)
        theme_card_layout.setSpacing(12)

        lbl_theme_title = QLabel("Aparência e Personalização")
        lbl_theme_title.setStyleSheet(
            "color: #8E8E93; font-size: 12px; font-weight: bold; text-transform: uppercase;"
        )
        theme_card_layout.addWidget(lbl_theme_title)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        themes_info = [
            ("dark", "🌙 Tema Escuro\n(Slate Dark)"),
            ("light", "☀️ Tema Claro\n(Clean White)"),
            ("cyber", "⚡ Nexus Cyber\n(Neon Vivid)"),
        ]

        saved_theme = self.settings.value("theme", "dark")

        for theme_id, label_text in themes_info:
            btn = QPushButton(label_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setFixedHeight(65)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #3F3F46;
                    border-radius: 8px;
                    padding: 8px;
                    font-weight: bold;
                    font-size: 12px;
                    text-align: center;
                }
                QPushButton:hover {
                    border-color: #6366F1;
                }
                QPushButton:checked {
                    border-color: #6366F1;
                    background-color: rgba(99, 102, 241, 0.2);
                }
            """)
            btn.clicked.connect(lambda _, t=theme_id: self._select_theme(t))
            cards_layout.addWidget(btn)
            self.theme_buttons[theme_id] = btn

        theme_card_layout.addLayout(cards_layout)
        layout.addWidget(theme_card)

        # CARD DE COMPORTAMENTO DO APLICATIVO
        card = QFrame()
        card.setObjectName("cardFrame")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(12)

        lbl_card_title = QLabel("Comportamento do Aplicativo")
        lbl_card_title.setStyleSheet(
            "color: #8E8E93; font-size: 12px; font-weight: bold; text-transform: uppercase;"
        )
        card_layout.addWidget(lbl_card_title)

        self.chk_minimize_to_tray = QCheckBox(
            "Manter aplicativo rodando na bandeja do sistema ao fechar (X)"
        )
        self.chk_minimize_to_tray.setCursor(Qt.PointingHandCursor)
        self.chk_minimize_to_tray.setStyleSheet("font-size: 13px; spacing: 8px;")

        # --- CORREÇÃO DA LEITURA SEGURA E CHAVE UNIFICADA ---
        val = self.settings.value("minimize_to_tray", True)
        if isinstance(val, str):
            minimize_to_tray = val.lower() in ("true", "1")
        else:
            minimize_to_tray = bool(val)

        self.chk_minimize_to_tray.setChecked(minimize_to_tray)
        self.chk_minimize_to_tray.toggled.connect(self._on_close_to_tray_toggled)

        card_layout.addWidget(self.chk_minimize_to_tray)
        layout.addWidget(card)

        layout.addStretch()

        self._update_button_states(saved_theme)

    def _select_theme(self, theme_id: str) -> None:
        """Salva o tema e aplica IMEDIATAMENTE no aplicativo inteiro."""
        self.settings.setValue("theme", theme_id)
        self._update_button_states(theme_id)

        style = THEMES.get(theme_id, THEMES["dark"])
        app = QApplication.instance()
        if app:
            app.setStyleSheet(style)
            for widget in app.allWidgets():
                widget.style().unpolish(widget)
                widget.style().polish(widget)
                widget.update()

        self.theme_changed.emit(theme_id)

    def _update_button_states(self, active_theme_id: str) -> None:
        """Marca o botão do tema atual como ativo."""
        for theme_id, btn in self.theme_buttons.items():
            btn.setChecked(theme_id == active_theme_id)

    def _on_close_to_tray_toggled(self, checked: bool) -> None:
        """Salva a chave exata 'minimize_to_tray' e sincroniza a legada 'close_to_tray'."""
        self.settings.setValue("minimize_to_tray", checked)
        self.settings.setValue("close_to_tray", checked)