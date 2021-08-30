import os.path
import datetime
import getpass

class MintLogger():
    # Constructor
    def __init__(self, address):
        self.fileLocation = address
    #Logger
    def Log(self, content, user):
        date = datetime.datetime.now()
        if not os.path.exists(os.path.dirname(self.fileLocation)):
            os.mkdir(os.path.dirname(self.fileLocation))
        if not os.path.exists(self.fileLocation):
            logFile = open(self.fileLocation, "w")
            logFile.close()
        try:
            writeFile = open(self.fileLocation, "a+")
            writeFile.write(content)
            writeFile.close()
        except:
            print("Failed")

'''
def log_function(sender, args):
    home = os.getenv('USERPROFILE')

    user = getpass.getuser()
    cloudLogLocation = "\\\\kpf.com\\corporate\\Zdrive\\0002_03_BIM\\05_Research\\Log-Files\\Mint\\"
    d = datetime.datetime.now()
    localPath = home + "\\" + str(d.year) + "_" + \
                str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLog.txt"

    serverPath = cloudLogLocation + user + "\\" + str(d.year) + "_" + \
                 str(d.month) + "_" + str(d.day) + "_" + user + "_RevitLog.txt"

    localLogger = Logger.MintLogger(localPath)
    cloudLogger = Logger.MintLogger(serverPath)

    separator = ","
    docTitle = args.GetDocument().Title
    message = str(datetime.datetime.now()) + \
              ";_Title:" + docTitle + \
              ";_Transactions:" + separator.join(args.GetTransactionNames()) + \
              ";_Added:" + separator.join(str(ele.IntegerValue) for ele in args.GetAddedElementIds()) + \
              ";_Deleted:" + separator.join(str(ele.IntegerValue) for ele in args.GetDeletedElementIds()) + \
              ";_Modified:" + separator.join(str(ele.IntegerValue) for ele in args.GetModifiedElementIds()) + \
              "\n"

    if os.path.exists(cloudLogLocation):
        try:
            cloudLogger.Log(message, user)
        except:
            pass
    else:
        try:
            localLogger.Log(message, user)
        except:
            pass
'''