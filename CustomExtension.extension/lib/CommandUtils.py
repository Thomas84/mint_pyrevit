import clr,sys
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
import System
from Autodesk.Revit.DB import Document
from Autodesk.Revit.UI import RevitCommandId, Events, TaskDialog

class ImportUtil:

    def __init__(self, app):
        #self.uiapp = None
        self.uiControlApp = app
        self.ImportCadWarning = None
        self.importBinding = None
        self.handler = None
        self.Module_Startup()

    def Module_Startup(self):
        if self.uiControlApp != None:
            commandId = RevitCommandId.LookupCommandId("ID_FILE_IMPORT")
            try:
                self.importBinding = self.uiControlApp.CreateAddInCommandBinding(commandId)
                self.handler = System.EventHandler[Events.ExecutedEventArgs](self.importReplacement)
                self.importBinding.Executed += self.handler
            except:
                TaskDialog.Show("Error", "Fail!")


    def importReplacement(sender, args):
        TaskDialog.Show("Stop!", "Do not import!")

    def ViewActivatedHandler(self):
        pass
        #__rvt__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)
