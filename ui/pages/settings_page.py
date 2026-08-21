"""
===========================================================
PRT Labs - UI / Settings Page
File: ui/pages/settings.py (ou settings_page.py)
Description: Tela de configurações com contraste correto para Tema Escuro e Claro
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QPushButton, QFrame, QApplication
)


class PRTThemeCard(QPushButton):
    """Card selecionável para troca de tema."""

    def __init__(self, icon_str: str, title: str, subtitle: str, theme_key: str, parent=None):
        super().__init__(parent)
        self.theme_key = theme_key
        self.setCheckable(True)
        self.setFixedHeight(70)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"{icon_str}  {title}\n({subtitle})")


class PRTSettingsPage(QWidget):
    """Página de configurações do PRT Nexus com suporte total a Temas."""

    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self._theme_cards = []
        self._current_theme = "dark"
        self._setup_ui()
        self.apply_theme("dark")  # Garante contraste escuro na inicialização

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Título da Tela
        self.title_label = QLabel("⚙️ Configurações do Sistema")
        self.title_label.setObjectName("titleLabel")
        main_layout.addWidget(self.title_label)

        # Seção 1: Aparência
        self.lbl_sec_appearance = QLabel("APARÊNCIA E PERSONALIZAÇÃO")
        self.lbl_sec_appearance.setObjectName("sectionHeader")
        main_layout.addWidget(self.lbl_sec_appearance)

        self.appearance_card = QFrame()
        self.appearance_card.setObjectName("cardContainer")
        card_layout = QHBoxLayout(self.appearance_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        themes = [
            ("🌙", "Tema Escuro", "Slate Dark", "dark"),
            ("☀️", "Tema Claro", "Clean White", "light"),
            ("⚡", "Nexus Cyber", "Neon Vivid", "cyber")
        ]

        for icon_str, title, subtitle, t_key in themes:
            card = PRTThemeCard(icon_str, title, subtitle, t_key)
            card.clicked.connect(lambda checked=False, k=t_key: self._on_theme_selected(k))
            card_layout.addWidget(card)
            self._theme_cards.append((card, t_key))

        main_layout.addWidget(self.appearance_card)

        # Seção 2: Comportamento
        self.lbl_sec_behavior = QLabel("COMPORTAMENTO DO APLICATIVO")
        self.lbl_sec_behavior.setObjectName("sectionHeader")
        main_layout.addWidget(self.lbl_sec_behavior)

        self.behavior_card = QFrame()
        self.behavior_card.setObjectName("cardContainer")
        behavior_layout = QVBoxLayout(self.behavior_card)
        behavior_layout.setContentsMargins(16, 16, 16, 16)
        behavior_layout.setSpacing(14)

        self.chk_startup = QCheckBox("Iniciar junto com o Windows")
        self.chk_tray = QCheckBox("Minimizar para a bandeja ao fechar (Tray Icon)")
        self.chk_notifications = QCheckBox("Exibir notificações do sistema")
        self.chk_notifications.setChecked(True)

        behavior_layout.addWidget(self.chk_startup)
        behavior_layout.addWidget(self.chk_tray)
        behavior_layout.addWidget(self.chk_notifications)

        main_layout.addWidget(self.behavior_card)
        main_layout.addStretch()

        self._update_card_states("dark")

    def _on_theme_selected(self, theme_key: str):
        self._current_theme = theme_key
        self._update_card_states(theme_key)
        self.apply_theme(theme_key)
        self.theme_changed.emit(theme_key)

        # Tenta aplicar tema globalmente no aplicativo se houver gerenciador de tema
        app = QApplication.instance()
        if hasattr(app, "set_theme"):
            app.set_theme(theme_key)

    def _update_card_states(self, theme_key: str):
        for card, key in self._theme_cards:
            card.setChecked(key == theme_key)

    def apply_theme(self, theme_key: str):
        """Define cores com contraste forçado para não deixar os textos pretos no fundo escuro."""
        is_light = (theme_key == "light")

        if is_light:
            bg_card = "#FFFFFF"
            border_card = "#E2E8F0"
            text_primary = "#0F172A"
            text_secondary = "#475569"
            btn_bg = "#F8FAFC"
            btn_border = "#CBD5E1"
            card_active_bg = "#EFF6FF"
        else:  # Dark & Cyber
            bg_card = "#0F172A"
            border_card = "#1E293B"
            text_primary = "#F8FAFC"
            text_secondary = "#94A3B8"
            btn_bg = "#1E293B"
            btn_border = "#334155"
            card_active_bg = "#1E3A8A"

        style = f"""
            QWidget#settingsPage {{
                background-color: transparent;
            }}
            QLabel#titleLabel {{
                font-size: 20px;
                font-weight: bold;
                color: {text_primary} !important;
                border: none;
            }}
            QLabel#sectionHeader {{
                font-size: 11px;
                font-weight: 800;
                color: {text_secondary} !important;
                letter-spacing: 0.5px;
                border: none;
            }}
            QFrame#cardContainer {{
                background-color: {bg_card};
                border: 1px solid {border_card};
                border-radius: 8px;
            }}
            QCheckBox {{
                font-size: 13px;
                font-weight: 500;
                color: {text_primary} !important;
                spacing: 10px;
                border: none;
                background: transparent;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid {btn_border};
                background-color: {btn_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: #2563EB;
                border-color: #2563EB;
            }}
            QPushButton {{
                background-color: {btn_bg};
                border: 1px solid {btn_border};
                border-radius: 8px;
                color: {text_primary} !important;
                font-size: 13px;
                font-weight: 600;
                text-align: center;
            }}
            QPushButton:hover {{
                border: 1px solid #3B82F6;
                color: #60A5FA !important;
            }}
            QPushButton:checked {{
                border: 2px solid #2563EB;
                background-color: {card_active_bg};
                color: #FFFFFF !important;
                font-weight: bold;
            }}
        """
        self.setStyleSheet(style)


# Aliases para compatibilidade total com importações do sistema
SettingsPage = PRTSettingsPage
SettingsView = PRTSettingsPage
settings_page = PRTSettingsPage