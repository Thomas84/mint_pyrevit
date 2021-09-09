import os
from pyrevit import DB, UI

def FamilySizeCheckWindow(block):
    FamilySizeWarning = UI.TaskDialog("FamilySizeWarning")
    FamilySizeWarning.MainIcon = UI.TaskDialogIcon.TaskDialogIconWarning
    FamilySizeWarning.Title = "Family Size Warning"
    FamilySizeWarning.TitleAutoPrefix = True
    FamilySizeWarning.AllowCancellation = False
    if block:
        FamilySizeWarning.MainInstruction = "Family is larger than 5MB, please clean up the family before loading into the project."
        FamilySizeWarning.ExpandedContent = None
        FamilySizeWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink1,
                                         "Ok, I will clean up the family.")
    else:
        FamilySizeWarning.MainInstruction = "Family is larger than 5MB, please consider clean up the family before loading into the project."
        FamilySizeWarning.ExpandedContent = None
        FamilySizeWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink1,
                                         "Ok, I will clean up the family.")
        FamilySizeWarning.AddCommandLink(UI.TaskDialogCommandLinkId.CommandLink2,
                                         "No, I still want to Load the Family.")

    FamilySizeWarning.CommonButtons = UI.TaskDialogCommonButtons.NoneS
    return FamilySizeWarning




def FamilySizeControl_function(sender, args):
    size = os.path.getsize(args.FamilyPath + args.FamilyName + ".rfa")
    # UI.TaskDialog.Show(args.FamilyName, str(size))
    result = None
    if size > 5242880:
        result = FamilySizeCheckWindow(True).Show()
    elif 5242880 >= size > 3145728:
        result = FamilySizeCheckWindow(False).Show()
    else:
        pass
    if result == UI.TaskDialogResult.CommandLink1:
        args.Cancel()
        # args.Dispose()
        UI.UIApplication(args.Document.Application).OpenAndActivateDocument(
            args.FamilyPath + args.FamilyName + ".rfa")
    elif result == UI.TaskDialogResult.CommandLink2:
        pass
    else:
        pass