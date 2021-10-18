from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework, forms
import Autodesk.Windows
ribbon = Autodesk.Windows.ComponentManager.Ribbon
import time, clr
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import SendKeys
import clr, sys, datetime, os
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


doc = rpw.revit.doc
uidoc = rpw.revit.uidoc
home = expanduser("~")
__persistentengine__ = True

# Simple function we want to run


def yes_click():
    # Refresh Time
    script.set_envvar('IdleShow', 1)
    script.set_envvar('IdleOverwrite', 0)
    script.set_envvar('LastActiveTime', datetime.datetime.now())


def no_click():
    script.set_envvar('IdleShow', 0)
    script.set_envvar('IdleOverwrite', 7)
    SyncUtility.SyncandCloseRevit(__revit__, home)
    script.set_envvar('LastActiveTime', datetime.datetime.now())


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
            print(InvalidOperationException.Message)

    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"


# Now we need to make an instance of this handler. Moreover, it shows that the same class could be used to for
# different functions using different handler class instances

# A simple WPF form used to call the ExternalEvent
class ModelessForm(WPFWindow):
    """
    Simple modeless form sample
    """
    script.set_envvar('Idle', 0)
    windowTimer = DispatcherTimer()
    handler = ()
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)

        def OnWindowTimerTick(sender, args):
            t = script.get_envvar('IdleWindowTimer')
            if t >= 0:
                self.close_text.Text = "This Window will close in {0} seconds".format(str(t))
                script.set_envvar('IdleWindowTimer', t - 1)
            else:
                self.windowTimer.Stop()
                self.Close()
                #self.Hide()
                no_ext_event.Raise()

        # if script.get_envvar('IdleShow') == 1:
        # if datetime.datetime.now() > script.get_envvar('LastActiveTime') + datetime.timedelta(minutes=1):
        #and script.get_envvar('IdleShow') == 1
        if script.get_envvar('IdleShow') == 1 and \
                (datetime.datetime.now() > script.get_envvar('LastActiveTime') + datetime.timedelta(minutes=150)):
            SendKeys.SendWait("{ESC}")
            script.set_envvar('IdleWindowTimer', 900)
            self.simple_text.Text = "Are you still there?"
            self.close_text.Text = "This Window will close in 900 seconds"
            # self.simple_text.Text = script.get_envvar('IdleTest')
            self.Show()
            self.handler = EventHandler(OnWindowTimerTick)
            self.windowTimer.Tick += self.handler
            self.windowTimer.Interval = TimeSpan(0, 0, 1)
            self.windowTimer.Start()

            script.set_envvar('IdleShow', 0)
            #script.set_envvar('IdleOverwrite', 7)

    def yes_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        # script.set_envvar('IdleShow', 1)
        self.windowTimer.Stop()
        self.windowTimer.Tick -= self.handler
        yes_ext_event.Raise()
        #self.Close()
        self.Hide()
        script.set_envvar('IdleWindowTimer', 900)

    def no_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        self.windowTimer.Stop()
        self.windowTimer.Tick -= self.handler
        no_ext_event.Raise()
        #self.Close()
        self.Hide()
        script.set_envvar('IdleWindowTimer', 900)

    def window_close(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        # script.set_envvar('IdleShow', 1)
        self.windowTimer.Stop()
        self.windowTimer.Tick -= self.handler
        yes_ext_event.Raise()
        # self.Close()
        self.Hide()
        script.set_envvar('IdleWindowTimer', 900)


# Let's launch our beautiful and useful form !

def OnCheckActivityTick(sender, args):
    modeless_form = ModelessForm("ModelessForm.xaml")


def DialogShwoing(sender, args):
    if script.get_envvar('IdleOverwrite') != 0:
        args.OverrideResult(script.get_envvar('IdleOverwrite'))

def update_time():
    script.set_envvar('LastActiveTime', datetime.datetime.now())

def document_changed_idle_function(sender, args):
    update_time()

def document_opened_idle_function(sender, args):
    update_time()

def document_synced_idle_function(sender, args):
    update_time()

def view_activated_idle_function(sender, args):
    update_time()

yes_event_handler = SimpleEventHandler(yes_click)
yes_ext_event = ExternalEvent.Create(yes_event_handler)
no_event_handler = SimpleEventHandler(no_click)
no_ext_event = ExternalEvent.Create(no_event_handler)

inactivityCheckTimer = DispatcherTimer()
inactivityCheckTimer.Tick += EventHandler(OnCheckActivityTick)
inactivityCheckTimer.Interval = TimeSpan(0, 15, 0)
inactivityCheckTimer.Start()
script.set_envvar('IdleShow', 1)

update_time()

__revit__.DialogBoxShowing += EventHandler[UI.Events.DialogBoxShowingEventArgs](DialogShwoing)
__revit__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](
    document_changed_idle_function)
__revit__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](view_activated_idle_function)
__revit__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](document_opened_idle_function)
__revit__.Application.DocumentSynchronizedWithCentral += EventHandler[
    DB.Events.DocumentSynchronizedWithCentralEventArgs](document_synced_idle_function)
#modeless_form = ModelessForm("ModelessForm.xaml")