from pyrevit import script, forms
from pyrevit import DB, UI
from System import EventHandler, Uri
from Autodesk.Revit.UI import TaskDialog
__title__ = 'ViewMonitor'
__context__ = 'zero'

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    classfication = ["DOCUMENTATION", "WORK", "REFERENCE", "EXPORT"]
    def log_function(sender, args):
        viewUse = args.CurrentActiveView.LookupParameter('view use').AsString()
        if viewUse.ToString() == '' or viewUse is None:
            selSheet = forms.SelectFromList.show(classfication, multiselect=False,
                                                 button_name='Select View Use')
            t = DB.Transaction(args.Document, 'Patch View Use')
            t.Start()
            args.CurrentActiveView.LookupParameter('view use').Set(selSheet)
            t.Commit()
    __rvt__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](log_function)

if __name__ == '__main__':
    print('Please do not click this button again.')