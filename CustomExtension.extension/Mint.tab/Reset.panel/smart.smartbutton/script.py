
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from Autodesk.Revit.DB import Document, \
        OpenOptions, WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption, \
        ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
import System
import CommandUtils
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from System import Guid
from os.path import expanduser
import ConfigParser
import clr,sys, datetime, os
import os.path
from os import path
from pyrevit import HOST_APP, framework
from pyrevit import script
from pyrevit import DB, UI
from Autodesk.Revit.UI import TaskDialog
from pyrevit import framework
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, DialogBoxShowingEventArgs 
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'Reset'
__context__ = 'zero'

import os
print(os.getenv('APPDATA') + "\\pyRevit\\pyRevit_config.ini")
def event_handler_function(sender, args):
   print("View activating")

# I'm using ViewActivating event here as example.
# The handler function will be executed every time a Revit view is activated:


config = script.get_config()

def OpenCloudFiles(modelGUID, projectGUID, app, audit):
    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    # openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertCloudGUIDsToCloudPath(projectGUID, modelGUID)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc

def SaveCloudModel(document, filePath):
    worksharingOptions = WorksharingSaveAsOptions()
    worksharingOptions.SaveAsCentral = True
    saveOpt = SaveAsOptions()
    saveOpt.SetWorksharingOptions(worksharingOptions)
    saveOpt.OverwriteExistingFile = True
    saveOpt.Compact = True
    document.SaveAs(filePath + document.Title + ".rvt", saveOpt)
    document.Close()

def SaveCloudModelandChangeName(document, filePath, Name):
    worksharingOptions = WorksharingSaveAsOptions()
    worksharingOptions.SaveAsCentral = True
    saveOpt = SaveAsOptions()
    saveOpt.SetWorksharingOptions(worksharingOptions)
    saveOpt.OverwriteExistingFile = True
    saveOpt.Compact = True
    document.SaveAs(filePath + Name + ".rvt", saveOpt)
    document.Close()

def test_function(sender, args):
    print("test")

# do the even stuff here
def event_handler_function(sender, args):
    pass
    # TaskDialog.Show("Test", args.DialogId.ToString())
    # do the even stuff here
    # I'm using ViewActivating event here as example.
    # The handler function will be executed every time a Revit view is activated:

def transaction_handler_function(sender, args):
    '''
    transNames = args.GetTransactionNames()
    for name in transNames:
        if name == "Family":
            #args.Dispose()
            TaskDialog.Show("Warning", "Please do not use model in place!")
    '''
    f = open("C:\\Users\\mlou\\OneDrive - Kohn Pedersen Fox Associates 1\\Desktop\\testdemofile2.txt", "w")
    f.write("Now the file has more content!")
    f.close()
    #TaskDialog.Show("Warning", "Please do not use model in place!")
    # do the even stuff here
    # I'm using ViewActivating event here as example.
    # The handler function will be executed every time a Revit view is activated:


# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    #try:
    #__rvt__.Application.DocumentChanged += (Logger.test_function)
    #__rvt__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)
    #__rvt__.Application.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    #HOST_APP.app.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    #except:
        #print("Logging Disabled.")
    #message =
    #__rvt__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)
    #__rvt__.Application.DocumentChanged += EventHandler[DocumentChangedEventArgs](transaction_handler_function)
    #__rvt__.DialogBoxShowing  += EventHandler[DialogBoxShowingEventArgs](event_handler_function)

    impUtil = CommandUtils.ImportUtil(__rvt__)
    # lets create that config file for next time...
    home = expanduser("~")
    '''
    __rvt__.DocumentOpened += \
        framework.EventHandler[
            UI.Events.RibbonItemEventArgs](SetbuttonStatus)
            '''
    # cfgfile = open(home + "\\MintTools.ini",'w')
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings to the structure of the file, and lets write it out...
    try:
        #Config.add_section('NavisFilePath')
        #Config.set('NavisFilePath', 'DataPath', ' ')
        # Add master new system folder setting
        Config.add_section('SysDir')
        Config.set('SysDir', 'MasterPackage',
                   os.path.dirname(os.path.realpath(__file__).split(".extension")[0] + ".extension\\packages\\"))
        Config.set('SysDir', 'SecondaryPackage',
                   os.path.dirname(os.path.realpath(__file__).split(".extension")[0] + ".extension\\packages\\"))
    except:
        pass
    cfgfile = open(home + "\\MintTools.ini", 'w')
    Config.write(cfgfile)

    try:
        modelsDic = dict(Config.items('Cloud'))
        pyCfgFile = open(home + "\\MintTools.ini", 'w')
        Config.write(cfgfile)
        if Config.get('General', 'clouddownload') == "1":
            n = 1
            for i in modelsDic.values():
                list = i.split(";")
                modelGUID = Guid(list[0])
                projectGUID = Guid(list[1])
                modelFilePath = list[2]
                appVersion = str(list[3])
                name = str(list[4])
                if str(__rvt__.Application.VersionName) == appVersion:
                    openedDoc = OpenCloudFiles(modelGUID, projectGUID, __rvt__.Application, audit=False)
                    SaveCloudModelandChangeName(openedDoc, modelFilePath, name)
                    print("Cloud Download Complete")
                else:
                    print("Model {} was not downloaded due to version mismatch".format(str(n)))
                n += 1
    except:
        pass
    cfgfile.close()

    '''`
    ribbons = __rvt__.GetRibbonPanels("MintTools")
    for i in ribbons:
        if i.Name == "Navis Data Import":
            buttons = i.GetItems()
            for b in buttons:
                if b.Name == 'Display':
                    b.Enabled = False
    '''
    return True

if __name__ == '__main__':
    print('Please do not click this button again.')