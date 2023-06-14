import tkinter as tk
import tkinter.ttk as ttk
import os
import time
from tkinter import *
from ttkthemes import ThemedTk
from tableModule import TableModule
from queue import Queue

class LogModule(TableModule):
    def __init__(self):
        super().__init__()
        self.__logQueue = Queue()
   
    def createStructure(self, **kwargs):
        super().createStructure(**kwargs)
        
    def write(self,msg):
        self.__logQueue.put(msg)
    
    def readQueue(self):
        try:
            message = self.__logQueue.get(0)
            if isinstance(message,tuple):
                targetMsg, targetStyle = message
                if targetStyle == 'INVISIBLE':
                    self.__registerLog(" - ".join([time.strftime("%H:%M", time.localtime()),targetMsg]))
                    return
                targetStyle = targetStyle.upper() + '.TLabel'
                labelLog = ttk.Label(master=self.infoWindow, text=" - ".join([time.strftime("%H:%M", time.localtime()),targetMsg]),
                                     style=targetStyle)
            else:
                labelLog = ttk.Label(master=self.infoWindow, text=" - ".join([time.strftime("%H:%M", time.localtime()),message]),
                                     style = 'MAIN.TLabel')
                
            self.fillTable([labelLog],True)
            self.__registerLog(labelLog.cget('text'))
        except:
            pass
        #root.after(1000,self.readQueue)
        
    def __registerLog(self,message):
        myPath = os.getcwd() + "/log"
        
        #Creates log path if doesnt exist
        if not os.path.exists(myPath):
            os.mkdir(myPath)
        
        #Get date and make self.__logFilePath
        today = time.strftime("%Y_%m_%d", time.localtime())
        self.__logFilePath = myPath + "/" + today
        
        #Create file with todayDate if doesnt exists
        if not os.path.exists(self.__logFilePath + '.dev'):
            self.__logFile = open(self.__logFilePath + '.dev','x')
            self.__logFile.close()
        
        #Rename file to be able to write on it
        os.rename(self.__logFilePath + '.dev', self.__logFilePath + '.txt')
        
        #Append information on file
        self.__logFile = open(self.__logFilePath + '.txt','a')
        self.__logFile.write(message + '\n')
        self.__logFile.close()
        
        #Rename it back so user can't read it
        os.rename(self.__logFilePath + '.txt',self.__logFilePath + '.dev')
        
if __name__ == '__main__':
    root = ThemedTk(theme="win")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
    
    log = LogModule()
    log.createStructure(master = root,labelText = 'Log Section')
    
    for i in range(30):
        if (i % 5) == 0:
            log.write(('Testing ' + str(i),'ERROR'))
        elif (i % 3) == 0:
            log.write(('Testing ' + str(i),'WARNING'))
        else:
            log.write('Testing ' + str(i))
            
    root.after(1000,log.readQueue)
    root.mainloop()