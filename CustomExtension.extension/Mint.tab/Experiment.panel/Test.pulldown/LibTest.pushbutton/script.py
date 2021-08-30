import Selection, FileUtilities, Warnings, QuestionableMath, FileUtilities, MEPUtilities
import sys
from pyrevit.coreutils import envvars
from pyrevit import DB, UI
import getpass
import CommandUtils
import Autodesk.Windows
import System.Windows.Media
import System.Windows.Media.Imaging
ribbon = Autodesk.Windows.ComponentManager.Ribbon
import System.Drawing
import ConfigParser
from os.path import expanduser

creamColor = System.Windows.Media.Color.FromRgb(255, 253, 208)
roseColor = System.Windows.Media.Color.FromRgb(247, 202, 201)
fuchsiaColor = System.Windows.Media.Color.FromRgb(255, 0, 255)
redColor = System.Windows.Media.Color.FromRgb(255, 0, 0)

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


'''
print("\n".join(sys.path))

envvars.set_pyrevit_env_var('MINT_CONFIG', {'FAMILY_VIEW_ACTIVATED': False})
print('FAMILY_VIEW_ACTIVATED: ' + str(envvars.get_pyrevit_env_vars()['MINT_CONFIG']['FAMILY_VIEW_ACTIVATED']))


print(getpass.getuser())

#wallOpeningFam = CommandUtils.GetFamily(__revit__.ActiveUIDocument.Document, 'Wall Opening_DD', 'Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa')
#print(wallOpeningFam)
#t = DB.Transaction(__revit__.ActiveUIDocument.Document, 'Test')
#t.Start()
#wallOpeningFam = __revit__.ActiveUIDocument.Document.LoadFamily('Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa', CommandUtils.FamilyOption())
#print(wallOpeningFam)
#t.Commit()



#print(wallOpeningFam)

class MyCustomExternalEventHandler(UI.IExternalEventHandler):
    name = 'MyCustomExternalEventHandler'

    def Execute(self, uiapp):
        wallOpeningFam = CommandUtils.GetFamily(uiapp.ActiveUIDocument.Document, 'Wall Opening_DD',
                                                'Z:\\0002_03_BIM\\03_Workflows\\KPFTools\\Family\\Wall Opening_DD.rfa')
        uidoc.PostRequestForElementTypePlacement(wallOpeningFam)

    def GetName(self):
        """String identification of the event handler."""
        return self.name

extevent_hndlr = MyCustomExternalEventHandler()
extevent = UI.ExternalEvent.Create(extevent_hndlr)
extevent.Raise()

t = DB.Transaction(doc, 'Test')
t.Start()
doc.Regenerate()
t.Commit()
'''