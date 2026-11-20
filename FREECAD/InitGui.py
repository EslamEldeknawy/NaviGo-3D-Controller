# -*- coding: utf-8 -*-
import os
import sys

try:
    _ADDON_DIR = os.path.dirname(os.path.realpath(__file__))
except NameError:
    import FreeCAD
    _ADDON_DIR = os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "NaviGo")

if _ADDON_DIR not in sys.path:
    sys.path.insert(0, _ADDON_DIR)

import navigo_freecad
navigo_freecad.schedule_start(_ADDON_DIR)