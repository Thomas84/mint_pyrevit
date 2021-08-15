import RevitPerformance
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Prints the Element Id of selected performance issues category\n' \
          'Step 1: Select the performance issue you want to address.\n' \
          'Step 2: Keep the printed window on top or another screen to navigate.'

RevitPerformance.PerformanceCollector(doc)




