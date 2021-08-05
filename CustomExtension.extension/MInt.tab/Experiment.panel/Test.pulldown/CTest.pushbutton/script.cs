using System;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;

namespace HelloWorld {
   public class Test2 : IExternalCommand {
      public Result Execute(ExternalCommandData revit,
                            ref string message, ElementSet elements) {
         TaskDialog.Show("123", "123");
         return Result.Succeeded;
      }
   }
}