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

#from Autodesk.Revit.DB.Events import DocumentChangedEventArgs, DocumentOpenedEventArgs
__title__ = 'IdleMonitor'
__context__ = 'zero-doc'

idleTimer = 120
global lastActiveTime

config = script.get_config()
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

def delete_elements():
    #time.sleep(12)
    TaskDialog.Show("Trigger Close", "Debug 5")
simple_event_handler = SimpleEventHandler(delete_elements)
# We now need to create the ExternalEvent
ext_event = ExternalEvent.Create(simple_event_handler)


def OnCheckActivityTick(sender, args):
    print("123")
    #MessageBox.Show("123")



def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    script.set_envvar('IdleMonitor', 0)
    script.set_envvar('IdleCount', 0)

    global lastActiveTime
    lastActiveTime = datetime.datetime.now()
    inactivityCheckTimer = DispatcherTimer()
    inactivityCheckTimer.Tick += EventHandler(OnCheckActivityTick)
    inactivityCheckTimer.Interval = TimeSpan(0, 0, idleTimer)
    inactivityCheckTimer.Start()

    global window
    def count(sender, args):
        global window
        if script.get_envvar('IdleMonitor') == 1:
            window.show(modal=False)
            script.set_envvar('IdleMonitor', 2)
            args.SetRaiseWithoutDelay()
        elif script.get_envvar('IdleMonitor') == 2:
            i = script.get_envvar('IdleCount')
            if i < 10:
                time.sleep(1)
                script.set_envvar('IdleCount', i + 1)
            else:
                script.set_envvar('IdleMonitor', 3)
                script.set_envvar('IdleCount', 0)
            args.SetRaiseWithoutDelay()
        elif script.get_envvar('IdleMonitor') == 3:
            script.set_envvar('IdleMonitor', 0)
            script.set_envvar('IdleCount', 0)
            TaskDialog.Show("Trigger Close", "Debug")

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

    __rvt__.Idling += EventHandler[UI.Events.IdlingEventArgs](count)
    __rvt__.Application.ApplicationInitialized += EventHandler[DB.Events.ApplicationInitializedEventArgs](app_inti_idle_function)
    __rvt__.Application.DocumentChanged += EventHandler[DB.Events.DocumentChangedEventArgs](
        document_changed_idle_function)
    __rvt__.ViewActivated += EventHandler[UI.Events.ViewActivatedEventArgs](view_activated_idle_function)
    __rvt__.Application.DocumentOpened += EventHandler[DB.Events.DocumentOpenedEventArgs](document_opened_idle_function)
    __rvt__.Application.DocumentSynchronizedWithCentral += EventHandler[
        DB.Events.DocumentSynchronizedWithCentralEventArgs](document_synced_idle_function)
    return True



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

if __name__ == '__main__':
    global window
    script.set_envvar('IdleMonitor', 1)

