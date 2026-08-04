"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Core
Description: Navigation identifiers used by the framework.

Developer..: Prof Rob Tech
===========================================================
"""

from enum import Enum


class Navigation(Enum):
    DASHBOARD = "dashboard"
    DOWNLOADS = "downloads"
    COURSES = "courses"
    SETTINGS = "settings"
    LICENSE = "license"