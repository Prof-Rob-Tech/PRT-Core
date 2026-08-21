"""
===============================================================================
 PRT Core
-------------------------------------------------------------------------------
 Project.....: PRT Core
 Module......: Bootstrap
 Description.: Application entry point.

 Organization: PRT Labs
 Developer...: Prof Rob Tech
===============================================================================
"""

import os
import sys

# Flags exatas que funcionaram no teste isolado
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox --log-level=3"
os.environ["QT_LOGGING_RULES"] = "qt.webenginecontext.debug=false;*.debug=false"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)

import traceback
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


def log_uncaught_exceptions(exctype, value, tb):
    print("\n" + "=" * 80)
    print("❌ ERRO CRÍTICO NÃO TRATADO:")
    print("".join(traceback.format_exception(exctype, value, tb)))
    print("=" * 80 + "\n")


sys.excepthook = log_uncaught_exceptions


def main() -> int:
    from core.application import Application
    application = Application()
    return application.run()


if __name__ == "__main__":
    sys.exit(main())