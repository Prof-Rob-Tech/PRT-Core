"""
===============================================================================
 PRT Core
-------------------------------------------------------------------------------
 Project.....: PRT Core
 Module......: Bootstrap
 Description.: Application entry point with WebEngine black screen & GPU logs fix.

 Organization: PRT Labs
 Developer...: Prof Rob Tech
===============================================================================
"""

import os
import sys

# -----------------------------------------------------------------------------
# CORREÇÃO DE GPU E SILENCIADOR DE LOGS DO CHROMIUM (DEVE FICAR NO TOPO)
# -----------------------------------------------------------------------------
# Unifica a desativação de aceleração gráfica com o silenciador de logs no terminal
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-gpu "
    "--disable-software-rasterizer "
    "--no-sandbox "
    "--log-level=3"
)
os.environ["QT_LOGGING_RULES"] = "qt.webenginecontext.debug=false;*.debug=false"
sys.argv.append('--disable-gpu')

# -----------------------------------------------------------------------------
# DIRETORES E CAMINHOS DO PROJETO
# -----------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)

# -----------------------------------------------------------------------------
# IMPORTAÇÕES DO QT E APLICAÇÃO
# -----------------------------------------------------------------------------
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from core.application import Application


def main() -> int:
    # Garante o compartilhamento correto de contexto OpenGL
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    application = Application()
    return application.run()


if __name__ == "__main__":
    sys.exit(main())

import traceback

def log_uncaught_exceptions(exctype, value, tb):
    """Captura exceções não tratadas e imprime detalhes no terminal."""
    print("\n" + "=" * 80)
    print("❌ ERRO CRÍTICO NÃO TRATADO:")
    print("".join(traceback.format_exception(exctype, value, tb)))
    print("=" * 80 + "\n")

# Registra o hook global no Python
sys.excepthook = log_uncaught_exceptions