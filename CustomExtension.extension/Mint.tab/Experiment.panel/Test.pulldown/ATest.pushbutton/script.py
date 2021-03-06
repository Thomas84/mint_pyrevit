
import sys, clr, os, re
import ConfigParser
from os.path import expanduser
# Set system path
import Selection
clr.AddReference('System')
from rpw import revit, db, ui
from pyrevit import forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import framework
from pyrevit import script
import datetime, os
from pyrevit import HOST_APP, framework
import uuid
import shutil
import rpw
from rpw import db

__doc__ = 'To be run in a Revit Model.'\
          'Step 1: Please select the folder that contains Revit families.'\
          'Step 2: Please select the destination folder to save new families.'\
          'Note: Please check the log after running this. ' \
          'Program will not modify or upgrade families despite it saying so in revit.'

selection = Selection.get_selected_elements(doc)
print(doc.GetElement(selection[0].GetRefGridLines(None, None)[0]).FullCurve.GetEndPoint(0).Z)