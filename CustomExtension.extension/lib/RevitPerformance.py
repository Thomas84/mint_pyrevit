from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
import pyrevit


# TODO: INFORM USER HOW MANY INSTANCES WILL BE SHOWN AND ASK HOW MANY WANT TO BE SHOWN NEXT
def PerformanceCollectorByItem(doc):
    out = []
    text = []
    pTypes = DB.PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds()
    failureMessages = DB.PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, pTypes)
    for i in failureMessages:
        if not str(i.GetDescriptionText()) in text:
            text.append(i.GetDescriptionText())

    sel_warning = forms.SelectFromList.show(text, button_name='Select Item',
                                            multiselect=True)
    output = pyrevit.output.get_output()
    outprint = script.get_output()
    count = 1
    tab = ' '
    for message in failureMessages:
        elementIds = message.GetFailingElements()
        des = message.GetDescriptionText()
        if des in str(sel_warning):
            output.print_md("**#** {}-----------------\n\n"
                            "- Warning Item:{}\n\n"
                            .format(count,
                                    des))
            for elementId in elementIds:
                wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(doc, elementId)
                owner = wti.Owner
                creator = wti.Creator
                changedBy = wti.LastChangedBy
                print(tab + format(outprint.linkify(elementId)) + tab + 'Creator: ' + creator + tab +
                      'Last Changed by: ' + changedBy)
        count += 1

    return out

def PerformanceCollector(doc):
    out = []
    all = []
    text = []
    pTypes = DB.PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds()
    failureMessages = DB.PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, pTypes)
    print('Below are all performance adviser categories: ' + str(len(failureMessages)))
    for i in failureMessages:
        all.append(i.GetDescriptionText())
        if not str(i.GetDescriptionText()) in text:
            text.append(i.GetDescriptionText())
    for t in text:
        print(t + '--------' + str(all.count(t)) + ' Instances in model.')
    return out