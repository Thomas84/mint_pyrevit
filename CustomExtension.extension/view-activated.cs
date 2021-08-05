using System;
using System.IO;

using Autodesk.Revit.DB;
using Autodesk.Revit.UI;


namespace MyEvents {
    public class MyEventMgr {
        // executor needs to find the correct function signature and executes that
        // first argument name must be "sender", type must be object
        // second argument name must be either "e" or "args" and type must be the event argument type associated
        // with the hook event type
        public void MyEventMgr_UiApp_ViewActivated(object sender, Autodesk.Revit.UI.Events.ViewActivatedEventArgs e) {
            string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            File.AppendAllText(
                Path.Combine(desktopPath, "hooks.log"),
                string.Format("[view-activated-csharp] doc:\"{0}\" active_view:\"{1}\" prev_view:\"{2}\" status:\"{3}\"\n",
                    e.Document != null ? e.Document.ToString() : "",
                    e.CurrentActiveView != null ? e.CurrentActiveView.ToString() : "",
                    e.PreviousActiveView != null ? e.PreviousActiveView.ToString() : "",
                    e.Status.ToString()
                )
            );
        }
    }
}