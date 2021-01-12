#pylint: disable=C0103,E0401
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from Autodesk.Revit.DB import Document, \
        OpenOptions, WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption, \
        ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
import System
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from System import Guid
from os.path import expanduser
import ConfigParser
import clr,sys, datetime
import os.path
from os import path
from pyrevit import HOST_APP, framework
from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
__title__ = 'Decom'
__context__ = 'zero'

import os



def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    prConfig = os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini"
    Config = ConfigParser.ConfigParser()
    Config.read(prConfig)
    # add the settings to the structure of the file, and lets write it out...

    Config.set('core', 'userextensions',
                   ['\\USPAPHL1FS05.stvgroup.stvinc.com\Vol1\CAD\Standards\Mint Inc\CAD_BIM Dev\pyRevit\MintTools'])

    cfgfile = open(prConfig, "w")
    Config.write(cfgfile)
if __name__ == '__main__':
    print('Please do not click this button again.')