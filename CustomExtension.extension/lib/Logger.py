import os.path
import datetime


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
            logFile.write(str(date) + "_" + user + "_" + "Log Start\n")
            logFile.close()
        try:
            writeFile = open(self.fileLocation, "a+")
            writeFile.write(content)
            writeFile.close()
        except:
            print("Failed")

