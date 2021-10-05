from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException
import rpw
from pyrevit.forms import WPFWindow
from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from System import EventHandler, Uri
from pyrevit import script

doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

__doc__ = "A simple modeless form sample"
__title__ = "Modeless Form"
__persistentengine__ = True

# Simple function we want to run
def delete_elements():
    with rpw.db.Transaction("Delete selection"):
        for elid in uidoc.Selection.GetElementIds():
            doc.Delete(elid)
        script.set_envvar('IdleShow', 0)

def enable_elements():
    with rpw.db.Transaction("Delete selection"):
        for elid in uidoc.Selection.GetElementIds():
            doc.Delete(elid)
        script.set_envvar('IdleShow', 0)

# Create a subclass of IExternalEventHandler
class SimpleEventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this

    # Execute method run in Revit API environment.
    def Execute(self, uiapp):
        try:
            self.do_this()
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print("InvalidOperationException catched")

    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"


# Now we need to make an instance of this handler. Moreover, it shows that the same class could be used to for
# different functions using different handler class instances
simple_event_handler = SimpleEventHandler(delete_elements)
# We now need to create the ExternalEvent
ext_event = ExternalEvent.Create(simple_event_handler)

# A simple WPF form used to call the ExternalEvent
class ModelessForm(WPFWindow):
    """
    Simple modeless form sample
    """
    def __init__(self, xaml_file_name):

        def OnWindowShowTick(sender, args):
            self.Hide()
        WPFWindow.__init__(self, xaml_file_name)
        if script.get_envvar('IdleShow') == 1:
            self.simple_text.Text = "Hello World"
            self.simple_text.Text = script.get_envvar('IdleTest')
            self.Show()

            windowTimer = DispatcherTimer()
            windowTimer.Tick += EventHandler(OnWindowShowTick)
            windowTimer.Interval = TimeSpan(0, 0, 10)
            windowTimer.Start()
            script.set_envvar('IdleShow', 0)

    def yes_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        script.set_envvar('IdleShow', 1)
        ext_event.Raise()
        self.Hide()

    def no_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        ext_event.Raise()
        self.Hide()

# Let's launch our beautiful and useful form !

def OnCheckActivityTick(sender, args):
    modeless_form = ModelessForm("ModelessForm.xaml")

inactivityCheckTimer = DispatcherTimer()
inactivityCheckTimer.Tick += EventHandler(OnCheckActivityTick)
inactivityCheckTimer.Interval = TimeSpan(0, 0, 3)
inactivityCheckTimer.Start()