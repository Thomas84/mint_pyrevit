from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework, forms
import Autodesk.Windows
ribbon = Autodesk.Windows.ComponentManager.Ribbon
import time
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException
from System import EventHandler, Uri
from threading import Thread
from Autodesk.Revit.UI import TaskDialog
from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from System.Windows.Forms import MessageBox
import clr, sys, datetime, os
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import InvalidOperationException
import rpw
from pyrevit.forms import WPFWindow
from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent, TaskDialog
from System import EventHandler, Uri
from pyrevit import script
import SyncUtility
from os.path import expanduser

#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'IdleMonitor'
__context__ = 'zero-doc'
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc
home = expanduser("~")
__persistentengine__ = True

# Simple function we want to run
def yes_click():
    # Refresh Time
    script.set_envvar('IdleShow', 0)

def no_click():
    SyncUtility.SyncandCloseRevit(__revit__, home)
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
yes_event_handler = SimpleEventHandler(yes_click)
yes_ext_event = ExternalEvent.Create(yes_event_handler)
no_event_handler = SimpleEventHandler(no_click)
no_ext_event = ExternalEvent.Create(no_event_handler)

# A simple WPF form used to call the ExternalEvent
class ModelessForm(WPFWindow):
    """
    Simple modeless form sample
    """
    script.set_envvar('Idle', 0)
    windowTimer = DispatcherTimer()
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)

        def OnWindowTimerTick(sender, args):
            t = script.get_envvar('IdleWindowTimer')
            if t >= 0:
                self.close_text.Text = "This Window will close in {0} seconds".format(str(t))
                script.set_envvar('IdleWindowTimer', t - 1)
            else:
                self.windowTimer.Stop()
                self.Hide()
                no_ext_event.Raise()

        if script.get_envvar('IdleShow') == 1:
            script.set_envvar('IdleWindowTimer', 30)
            self.simple_text.Text = "Are you still there?"
            self.close_text.Text = "This Window will close in 30 seconds"
            #self.simple_text.Text = script.get_envvar('IdleTest')
            self.Show()
            self.windowTimer.Tick += EventHandler(OnWindowTimerTick)
            self.windowTimer.Interval = TimeSpan(0, 0, 1)
            self.windowTimer.Start()

            script.set_envvar('IdleShow', 0)

    def yes_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        script.set_envvar('IdleShow', 1)
        self.windowTimer.Stop()
        yes_ext_event.Raise()
        self.Hide()

    def no_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        self.windowTimer.Stop()
        no_ext_event.Raise()
        self.Hide()

# Let's launch our beautiful and useful form !

def OnCheckActivityTick(sender, args):
    modeless_form = ModelessForm("ModelessForm.xaml")

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    inactivityCheckTimer = DispatcherTimer()
    inactivityCheckTimer.Tick += EventHandler(OnCheckActivityTick)
    inactivityCheckTimer.Interval = TimeSpan(0, 0, 1800)
    inactivityCheckTimer.Start()

    def update_time():
        global lastActiveTime
        lastActiveTime = datetime.datetime.now()


    def app_inti_idle_function(sender, args):
        update_time()

    def document_changed_idle_function(sender, args):
        update_time()

    def document_opened_idle_function(sender, args):
        update_time()

    def document_synced_idle_function(sender, args):
        update_time()

    def view_activated_idle_function(sender, args):
        update_time()

    __rvt__.Application.ApplicationInitialized += EventHandler[DB.Events.ApplicationInitializedEventArgs](app_inti_idle_function)
    __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](
        document_changed_idle_function)
    __rvt__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](view_activated_idle_function)
    __rvt__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](document_opened_idle_function)
    __rvt__.Application.DocumentSynchronizedWithCentral += EventHandler[
        DB.Events.DocumentSynchronizedWithCentralEventArgs](document_synced_idle_function)
    return True


'''
class TimerWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        # create pattern maker window and process options
        forms.WPFWindow.__init__(self, xaml_file_name)
        self.stringValue_tb.Text = "Revit will close after 10 seconds"

    def word_string(self):
        return self.stringValue_tb.Text

    def wait(self, number):
        time.sleep(number)
        TaskDialog.Show("Trigger Close", "Debug 1")

    def word_set(self, number):
        self.stringValue_tb.Text = str(number)

    def select(self, sender, args):
        script.set_envvar('IdleMonitor', 0)
        script.set_envvar('IdleCount', 0)

        ext_event.Raise()
        self.Hide()

    def string_value_changed(self, sender, args):
        pass

global window
window = TimerWindow(r'..\TimerBox.xaml')
'''
if __name__ == '__main__':
    global window
    script.set_envvar('IdleMonitor', 1)

