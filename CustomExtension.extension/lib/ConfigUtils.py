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




def WriteModelOpenTimeConfig(model, hashcode, time):
    home = expanduser("~")
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\MintTools.ini")
    # add the settings
    try:
        Config.set('OpenModels', hashcode + "_" + model, str(time))
    except:
        pass
    cfgfile = open(home + "\\MintTools.ini", 'w')
    Config.write(cfgfile)

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
    try:
        Config.add_section('NavisFilePath')
        Config.set('NavisFilePath', 'DataPath', ' ')
        timeText = Config.get('OpenModels', hashcode + "_" + model)
        if timeText is not None:
            lastSyncedTime = datetime.datetime.strptime(Config.get('OpenModels', hashcode + "_" + model))
            if time > lastSyncedTime + datetime.timedelta(minutes=deltas[0]):
                Ribbon.ChangeRibbonColor(0)
                return True
            elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[1]):
                Ribbon.ChangeRibbonColor(1)
                return False
            elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[2]):
                Ribbon.ChangeRibbonColor(2)
                return False
            elif time > lastSyncedTime + datetime.timedelta(minutes=deltas[3]):
                Ribbon.ChangeRibbonColor(3)
                return False
            else:
                return False
        else:
            return False
    except:
        return False
