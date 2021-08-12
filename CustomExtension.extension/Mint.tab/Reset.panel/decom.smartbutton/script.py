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
    path = Config.get('core', 'userextensions')
    #print(path)
    oldPath = r"\\\\kpfny-nas01.kpf.com\\Deployment\\Autodesk\\KPFTools"
    newPath = r"\\\\kpf.com\\corporate\\Zdrive\\0002_03_BIM\\03_Workflows\\KPFTools"
    setting = path
    if oldPath in path and not newPath in path:
        setting = path.replace(oldPath, newPath)
        #print("Old path: " + oldPath + "replaced by: " + newPath)
    elif oldPath in path:
        setting = path.replace(oldPath, "")
        #print("Old path removed " + oldPath)
    #TODO: Add change path
    Config.set('core', 'userextensions', setting)
    cfgfile = open(prConfig, "w")
    Config.write(cfgfile)

if __name__ == '__main__':
    print('Please do not click this button again.')