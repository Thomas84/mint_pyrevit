import clr,sys
# import datetime
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from System.Collections.Generic import List
from Autodesk.Revit.UI import RibbonPanel
from pyrevit import script, DB, revit, UI
from pyrevit import forms
import pyrevit
from pyrevit import framework
import ConfigParser
from os.path import expanduser
from pyrevit.coreutils import envvars
'''
home = expanduser("~")
# print(os.path.dirname(os.path.realpath(__file__).split(".extension")[0] + ".extension\\packages\\"))
cfgfile = open(home + "\\MintTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\MintTools.ini")
# Master Path
syspath1 = config.get('SysDir', 'MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir', 'SecondaryPackage')
sys.path.append(syspath2)
clr.AddReference('System')
'''
__doc__ = 'Auto Button by BIM Group to attach auto scripts.'

from Autodesk.Revit.DB import Document,\
    OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
import System
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from System import Guid
# from System import DateTime


# print(script.get_all_buttons())


def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    filePath = "C:\\Users\\loum\\Desktop\\acad\\"
    modelGUID = Guid("e77aa560-8776-4a0e-8192-3044c5e240df")
    projectGUID = Guid("20ac335a-5ba8-4520-b948-296e529c3306")

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
        Config.add_section('NavisFilePath')
        Config.set('NavisFilePath','DataPath',' ')

        # Add master new system folder setting
        Config.add_section('SysDir')
        Config.set('SysDir', 'MasterPackage', r'\\Uspadgv1dcl01\NY BIM GROUP\Tools\Repo\pyRevit_custom_Mint\CustomExtension.extension\packages\\')
        Config.set('SysDir', 'SecondaryPackage', r'\\Uspadgv1dcl01\BIM - B&F\00 - BIM Resources\06_BIM Tools\04-pyRevit\MintTools\CustomExtension.extension\packages\\')
    except:
        pass
    cfgfile = open(home + "\\MintTools.ini", 'w')
    Config.write(cfgfile)
    sys.path.append(r'\\Uspadgv1dcl01\NY BIM GROUP\Tools\Repo\pyRevit_custom_Mint\CustomExtension.extension\packages\\')

    modelsDic = dict(Config.items('Cloud'))

    # afterHours = DateTime.Parse("2020/1/1 21:00:00.000")
    # timeStamp = datetime.datetime.now().time()  # Throw away the date information
    # Timer after which time download model will start
    '''
    setTime = datetime.time(21, 00, 00)
    if Config.get('general', 'clouddownload') == "1" and setTime <= timeStamp:
        downloadModel = True
    elif Config.get('general', 'clouddownload') == "2":
        downloadModel = True
    else:
        pass
    '''

    if Config.get('General','clouddownload') == "1" :
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

    cfgfile.close()
    ribbons = __rvt__.GetRibbonPanels("MintTools")
    for i in ribbons:
        if i.Name == "Navis Data Import":
            buttons = i.GetItems()
            for b in buttons:
                if b.Name == 'Display':
                    b.Enabled = False



