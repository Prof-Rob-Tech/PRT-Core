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

import sys

from core.application import Application


def main() -> int:
    application = Application()
    return application.run()


if __name__ == "__main__":
    sys.exit(main())