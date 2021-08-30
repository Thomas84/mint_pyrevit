import CommandUtils
import ConfigParser
import os.path
import FileUtilities
import datetime
from System import Guid
from os.path import expanduser
import Ribbon
'''
def SetUpConfig(__revit__):

    impUtil = CommandUtils.ImportUtil(__revit__)
    # lets create that config file for next time...
    home = os.path.expanduser("~")
    
    #__rvt__.DocumentOpened += framework.EventHandler[UI.Events.RibbonItemEventArgs](SetbuttonStatus)
            
    # cfgfile = open(home + "\\MintTools.ini",'w')
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings to the structure of the file, and lets write it out...
    try:
        # Config.add_section('NavisFilePath')
        # Config.set('NavisFilePath', 'DataPath', ' ')
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
                if str(__revit__.Application.VersionName) == appVersion:
                    openedDoc = FileUtilities.OpenCloudFiles(modelGUID, projectGUID, __rvt__.Application, audit=False)
                    FileUtilities.SaveCloudModelandChangeName(openedDoc, modelFilePath, name)
                    print("Cloud Download Complete")
                else:
                    print("Model {} was not downloaded due to version mismatch".format(str(n)))
                n += 1
    except:
        pass
    cfgfile.close()
'''




def LocktoCollabToolBar(sender, args):
    pass

def WriteModelOpenTimeConfig(model, hashcode, time):
    home = expanduser("~")
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings
    try:
        Config.set('OpenModels', hashcode + "_" + model, str(time.strftime("%m/%d/%y %H:%M:%S")))
    except:
        pass
    cfgfile = open(home + "\\MintTools.ini", 'w')
    Config.write(cfgfile)
    ChangeRibbonColor(4)

def WipeTimeConfig(model, hashcode):
    home = expanduser("~")
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings
    try:
        Config.set('OpenModels', hashcode + "_" + model, None)
    except:
        pass
    cfgfile = open(home + "\\MintTools.ini", 'w')
    Config.write(cfgfile)

def CheckSyncTimeConfig(model, hashcode, time, deltas):
    home = expanduser("~")
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings

    timeText = Config.get('OpenModels', hashcode + "_" + model)
    #TaskDialog.Show(model, timeText)
    if timeText is not None:
        lastSyncedTime = datetime.datetime.strptime(timeText, "%m/%d/%y %H:%M:%S")
        if time > lastSyncedTime + datetime.timedelta(minutes=deltas[0]):
            #TaskDialog.Show(model, "1")
            ChangeRibbonColor(0)
            return True
        elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[1]):
            #TaskDialog.Show(model, "2")
            ChangeRibbonColor(1)
            return False
        elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[2]):
            #TaskDialog.Show(model, "3")
            ChangeRibbonColor(2)
            return False
        elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[3]):
            #TaskDialog.Show(model, "4")
            ChangeRibbonColor(3)
            return False
        else:
            #TaskDialog.Show(model, "5")
            ChangeRibbonColor(4)
            return False
    else:
        return False

def ChangeRibbonColor(int):
    colors = []

    defaultColor = System.Windows.Media.Color.FromRgb(238, 238, 238)
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
