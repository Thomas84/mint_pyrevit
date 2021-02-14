import clr
import pprint
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")

doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Info about this panel,'\
          'and also who can you talk to if you need help.'

info = ['These tools are developed by Mengfan Lou using pyRevit which is Created by eirannejad or Ehsan Iran-Nejad.'
        'For internal use only.',
        'Contact Info:', 'mlou@kpf.com', '(p)(734)709-0971']

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(info)