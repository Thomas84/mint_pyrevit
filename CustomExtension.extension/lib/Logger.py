import datetime
import os.path


class MintLogger():
    # Constructor
    def __init__(self, address):
        self.fileLocation = address
    #Logger
    def Log(self, content, user):
        date = datetime.datetime
        if not os.path.exists(os.path.dirname(self.fileLocation)):
            os.mkdir(os.path.dirname(self.fileLocation))
        if not os.path.exists(self.fileLocation):
            logFile = open(self.fileLocation, "w")
            logFile.write(str(datetime.datetime) + "_" + user + "_" + "Log Start")
            logFile.close()
        try:
            writeFile = open(self.fileLocation, "a+")
            writeFile.write(content)
            writeFile.close()
        except:
            print("Failed")

def log_function(sender, args):
    event_uidoc = sender.ActiveUIDocument
    event_doc = sender.ActiveUIDocument.Document
    logger = MintLogger("")
    separator = ","
    docTitle = args.GetDocument().Title
    message = str(datetime.datetime) + \
              " ;_Title:" + docTitle + \
              " ;_Transactions:" + separator.join(args.GetTransactionNames()) + \
              " ;_Added:" + separator.join(args.GetAddedElementIds()) + \
              " ;_Deleted:" + separator.join(args.GetDeletedElementIds()) + \
              " ;_Modified:" + separator.join(args.GetModifiedElementIds())
    logger.Log(message, sender.ActiveUIDocument.Document.Application.Username)
