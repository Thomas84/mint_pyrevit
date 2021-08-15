import RevitPerformance

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Prints performance issues, advices and instances counts.'

RevitPerformance.PerformanceCollector(doc)




