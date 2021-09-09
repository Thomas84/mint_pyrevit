
import sys, clr
import ConfigParser
from os.path import expanduser
# Set system path


from Autodesk.Revit.DB import Document, FilteredElementCollector, Transaction, FilterElement, WorksharingUtils, View
from pyrevit import revit, DB, forms
clr.AddReference('System')
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def GetOwner(doc, ElementIds):
    result = {}
    for ele in ElementIds:
        owner = WorksharingUtils.GetWorksharingTooltipInfo(doc, ele).Owner.ToString()
        if owner and owner != doc.Application.Username:
            result[ele.IntegerValue.ToString()] = owner
    return result

# Pick Copying Process
processes = ["Copy from existing view templates", "Add filters"]
selProcess = forms.CommandSwitchWindow.show(processes, message='Select Copy Option')

# Only add filters
if selProcess == "Add filters":
    ff = {}
    filters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()
    for filter in filters:
        ff[filter.Name] = filter
    selFilters = forms.SelectFromList.show(ff.keys(), multiselect=True,  button_name='Select Filters')

    vv= {}
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if view.IsTemplate:
            vv[view.Title] = view
    selViews = forms. SelectFromList.show(vv.keys(), multiselect=True, button_name='Select Templates')

    t = Transaction(doc, 'Add Filter to Templates')
    t.Start()
    count = 0


    # Check Ownership of the elements that is about to change
    checkResult = True
    selectedViewId = []
    for checkedView in selViews:
        view = vv[checkedView]
        selectedViewId.append(view.Id)
    ownerCheck = GetOwner(doc, selectedViewId)
    message = ""
    if ownerCheck:
        for id in ownerCheck.keys():
            message += ("ID: " + id + " owned by " + ownerCheck[id] + "\n")
        checkResult = forms.alert("You may have to request ownership if you proceed", title = "Ownership Check",
                                  sub_msg= message,
                                  ok = True,
                                  cancel =True)
    if checkResult:
        with forms.ProgressBar(title='Copying Filters') as pb:
            for selectedView in selViews:
                view = vv[selectedView]
                for selectedFilter in selFilters:
                    filter = ff[selectedFilter].Id
                    try:
                        view.AddFilter(filter)
                    except:
                        pass
                pb.update_progress(count, len(selViews))
                count += 1
        t.Commit()
    else:
        t.RollBack()

# Copy Filters from a View Template
elif selProcess == "Copy from existing view templates":
    vv= {}
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if view.IsTemplate:
            vv[view.Title] = view
    # get source view template and target view template
    selView = forms. SelectFromList.show(vv.keys(), multiselect=False, button_name='Select Source Template')
    targetViews = forms. SelectFromList.show(vv.keys(), multiselect=True, button_name='Select Target Template')


    filterData = []
    source = vv[selView]
    filters = source.GetFilters()
    for filter in filters:
        overrides = source.GetFilterOverrides(filter)
        vis = source.GetFilterVisibility(filter)
        filterData.append([filter, overrides, vis])

    # Copy Data to
    t = Transaction(doc, 'Add Filter to Templates')
    t.Start()
    count = 0
    # Check Ownership of the elements that is about to change
    checkResult = True
    selectedViewId = []
    for checkedView in targetViews:
        view = vv[checkedView]
        selectedViewId.append(view.Id)
    ownerCheck = GetOwner(doc, selectedViewId)
    #print(ownerCheck)
    message = ""
    if ownerCheck:
        for id in ownerCheck.keys():
            message += ("ID: " + id + " owned by " + ownerCheck[id] + "\n")
        checkResult = forms.alert("You may have to request ownership if you proceed", title = "Ownership Check",
                                  sub_msg= message,
                                  ok = True,
                                  cancel =True)
    if checkResult:
        with forms.ProgressBar(title='Copying Filters') as pb:
            for targetView in targetViews:
                target = vv[targetView]
                for fd in filterData:
                    try:
                        target.AddFilter(fd[0])
                        target.SetFilterOverrides(fd[0], fd[1])
                        target.SetFilterVisibility(fd[0], fd[2])
                    except:
                        pass
                pb.update_progress(count, len(targetViews))
                count += 1
        t.Commit()
    else:
        t.RollBack()
