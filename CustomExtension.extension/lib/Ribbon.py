import Selection, FileUtilities, Warnings, QuestionableMath, FileUtilities, MEPUtilities
import sys
from pyrevit.coreutils import envvars
from pyrevit import DB, UI
import getpass
import CommandUtils
import Autodesk.Windows
import System.Windows.Media
import System.Windows.Media.Imaging
import System.Drawing

ribbon = Autodesk.Windows.ComponentManager.Ribbon



uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def ChangeRibbonColor(int):
    colors = []
    creamColor = System.Windows.Media.Color.FromRgb(255, 253, 208)
    roseColor = System.Windows.Media.Color.FromRgb(247, 202, 201)
    fuchsiaColor = System.Windows.Media.Color.FromRgb(255, 0, 255)
    redColor = System.Windows.Media.Color.FromRgb(255, 0, 0)
    colors.append(redColor)
    colors.append(fuchsiaColor)
    colors.append(roseColor)
    colors.append(creamColor)
    for tab in ribbon.Tabs:
        for panel in tab.Panels:
            panel.CustomPanelBackground = System.Windows.Media.SolidColorBrush(colors[int])
