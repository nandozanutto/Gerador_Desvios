import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from ttkthemes import ThemedTk
from absModule import AbsModule

class TableModule(AbsModule):
    def __init__(self):
        super().__init__()
        
    def createStructure(self, **kwargs):
        '''
        -> tableSpan: specifies distance between table (self.__table) and widgets around it measure in pixels.
            It has to be a tuple e.g: 
                        tableSpan = (padx,pady), or
                        tableSpan = ((padx(leftside),padx(rightside)),(pady(upside),pady(downside)))
            DEFAULT VALUE = ((5,5),(5,5))
            
        -> tableBd: specifies table (self.__table) borderwidth measured in pixels.
            It has to be an integer. e.g:
                    tableBd = 3
            DEFAULT VALUE = 1
        
        -> tableRelief: specifies the table (self.__table) relief.
            It has to be a string and a valid tkinter relief value. e.g:
                    tableRelief = GROOVE, or
                    tableRelief = RIDGE
            DEFAULT VALUE = GROOVE
            
        -> widget (from updateItem method): specifies the widget that will be updated.
            It has to be a string and a valid tkinter name (used to create the widget)
                    widget = frame1.projectvalue, or
                    widget = frame2, or
                    widget = frame2.statusvalue
            THERE IS NOT DEFAULT VALUE. NEED TO BE SET
            
        '''
        super().createStructure(**kwargs)
        
        tableSpan = kwargs.get('tableSpan')
        if tableSpan == None:
            tableSpan = ((5,5),(5,5))
        elif not isinstance(tableSpan,tuple):
            raise TypeError("descriptor 'createStructure' of 'tableModule' object needs tableSpan argument as a Tuple class with two arguments. e.g: (padx,pady) or"
                            "((padx(left),padx(right)),(pady(up),pady(down))).")
        
        tableBd = kwargs.get('tableBd')
        if tableBd == None:
            tableBd = 1
        elif not isinstance(tableBd,int):
            raise TypeError("descriptor 'createStructure' of 'tableModule' object needs tableBd argument as a Integer class. e.g: 1.")
            
        tableRelief = kwargs.get('tableRelief')
        if tableRelief == None:
            tableRelief = GROOVE
        elif not isinstance(tableRelief,str):
            raise TypeError("descriptor 'createStructure' of 'tableModule' object needs tableRelief argument as a String class and valid TK relief. e.g: GROOVE or"
                            "RIDGE.")
            
        #Frame
        self.__table = tk.Frame(master=self._labelFrame, bd=tableBd, relief=tableRelief)
        self.__table.grid(row=0, column=0, sticky='nsew', padx=tableSpan[0], pady=tableSpan[1])
        self.__table.columnconfigure(0, weight=1)
        self.__table.rowconfigure(0, weight=1)
        
        #Scrollbar
        self.__scrollBar = ttk.Scrollbar(self.__table, orient='vertical')
        self.__scrollBar.grid(row=0, column=1, sticky='ns')
         
        #Canvas
        self.__infoShowcase = tk.Canvas(self.__table)
        self.__infoShowcase.grid(row=0, column=0, sticky='nsew')
        self.__infoShowcase.columnconfigure(0, weight=1)
        
        #Frame
        self.__infoWindow = tk.Frame(master=self.__infoShowcase)
        self.__infoWindow.columnconfigure(0, weight=1)
        
        #Elements configuration
        self.__infoShowcase.create_window(0, 0, window=self.__infoWindow, anchor="nw",tags='self.__infoWindow')
        self.__infoShowcase.config(yscrollcommand=self.__scrollBar.set)
        self.__infoShowcase.bind('<Configure>', self.__frameWidth)
        self.__infoWindow.bind("<Configure>", self.__onFrameConfigure)
        self.__scrollBar.config(command=self.__infoShowcase.yview)
        
    @property
    def infoWindow(self):
        return self.__infoWindow
    
    def fillTable(self, newFrameList, keepInfo):
        
        #Keepinfo decides __clearTable
        if not keepInfo:
            self.__clearTable(newFrameList)
        
        #Counts nº o mapped widget to fill in correct row
        self.offset = 0
        for index,child in enumerate(self.__infoWindow.winfo_children()):
            if child.winfo_ismapped() == 1:
                self.offset += 1
         
        #Iteration in frames to create them 
        try:
            for i,frame in enumerate(newFrameList):
                frame.grid(row= i + self.offset,column=0,sticky='nsew')
            return True
        except:
            return False

    def __clearTable(self,newFrameList):
        #Verification if no need to clear
        if len(self.__infoWindow.winfo_children()) == 0:
            return False
        
        #Destroy mapped frames
        try:
            for index,child in enumerate(self.__infoWindow.winfo_children()):
                if child.winfo_ismapped() == 1:
                    child.destroy()
            return True
        except:
            return False
        
    def __onFrameConfigure(self, event):
        self.__infoShowcase.configure(scrollregion=self.__infoShowcase.bbox('all'))

    def __frameWidth(self, event):
        canvas_width = event.width
        self.__infoShowcase.itemconfig('self.__infoWindow', width=canvas_width)
        
    def updateItem(self, **kwargs):
        #Get widget name that will be updated
        targetWidget = kwargs.get('widget')
        if targetWidget == None:
            raise TypeError("descriptor 'updateWidget' of 'tableModule' object needs widget argument as a String class. e.g: 'frame1.projectvalue'")
        
        #Remove kwargs from the dictionnary
        paramDict = kwargs
        del paramDict['widget']
        
        #Update widget depending on what was set by user
        self.__infoWindow.nametowidget(targetWidget).configure(**paramDict)
        
if __name__ == '__main__':
    root = ThemedTk(theme="win")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
    
    table = TableModule()
    table.createStructure(master=root,rootFrameSpan =((5,5),(5,5)),labelText='Table Section')
    
    padx_value = (10,0)
    padx_label = (5,0)
    pady_std = 5
    
    def testeClearTable():
        frame3 = ttk.Frame(master=table.infoWindow,relief=RIDGE,name='frame3')
        frame3.columnconfigure(0,weight=1)
        frame3.columnconfigure(1,weight=1)
        frame3.columnconfigure(2,weight=1)
        projectLabel = ttk.Label(frame3,text="PROJECT:",name='projectlabel')
        projectLabel.grid(row=0, column=0, padx=padx_label,pady=pady_std, sticky='nsw') 
        regionLabel = ttk.Label(frame3,text="REGION:",name='regionlabel')
        regionLabel.grid(row=0, column=1, padx=padx_label, pady=pady_std,sticky='nsw')
        statusLabel = ttk.Label(frame3,text="STATUS:",name='statuslabel')
        statusLabel.grid(row=0, column=2, padx=padx_label, pady=pady_std,sticky='nsw')
        project = 'EFGHI'
        projectValue = ttk.Label(frame3,text=project,name='projectvalue')
        projectValue.grid(row=1, column=0, padx=padx_value, pady=pady_std,sticky='nsw')
        region = 'São Paulo'
        regionValue = ttk.Label(frame3,text=region,name='regionvalue')
        regionValue.grid(row=1, column=1,  padx=padx_value, pady=pady_std,sticky='nsw')
        status = 'Pending'
        statusValue = ttk.Label(frame3,text=status,name='statusvalue',font=('Arial',14,'italic'))
        statusValue.grid(row=1, column=2,  padx=padx_value, pady=pady_std,sticky='nsw')
        table.fillTable([frame3],False)
    
    
    
    frame1 = ttk.Frame(master=table.infoWindow,relief=RIDGE,name='frame1')
    frame1.columnconfigure(0,weight=1,uniform='frame1')
    frame1.columnconfigure(1,weight=1,uniform='frame1')
    frame1.columnconfigure(2,weight=1,uniform='frame1')
    projectLabel = ttk.Label(frame1,text="PROJECT:",name='projectlabel')
    projectLabel.grid(row=0, column=0, padx=padx_label,pady=pady_std, sticky='nsw') 
    regionLabel = ttk.Label(frame1,text="REGION:",name='regionlabel')
    regionLabel.grid(row=0, column=1, padx=padx_label, pady=pady_std,sticky='nsw')
    statusLabel = ttk.Label(frame1,text="STATUS:",name='status')
    statusLabel.grid(row=0, column=2, padx=padx_label, pady=pady_std,sticky='nsw')
    project = 'ABCDE'
    projectValue = ttk.Label(frame1,text=project,name='projectvalue')
    projectValue.grid(row=1, column=0, padx=padx_value, pady=pady_std,sticky='nsw')
    region = 'Curitiba'
    regionValue = ttk.Label(frame1,text=region,name='regionvalue')
    regionValue.grid(row=1, column=1,  padx=padx_value, pady=pady_std,sticky='nsw')
    status = 'OK'
    statusValue = ttk.Label(frame1,text=status,name='statusvalue')
    statusValue.grid(row=1, column=2,  padx=padx_value, pady=pady_std,sticky='nsw')
    frame1.bind('<Button-1>', lambda event: testeClearTable())
    
    frame2 = ttk.Frame(master=table.infoWindow,relief=RIDGE,name='frame2')
    frame2.columnconfigure(0,weight=1,uniform='frame2')
    frame2.columnconfigure(1,weight=1,uniform='frame2')
    frame2.columnconfigure(2,weight=1,uniform='frame2')
    projectLabel = ttk.Label(frame2,text="PROJECT:",name='projectlabel')
    projectLabel.grid(row=0, column=0, padx=padx_label,pady=pady_std, sticky='nsw') 
    regionLabel = ttk.Label(frame2,text="REGION:",name='regionlabel')
    regionLabel.grid(row=0, column=1, padx=padx_label, pady=pady_std,sticky='nsw')
    statusLabel = ttk.Label(frame2,text="STATUS:",name='statuslabel')
    statusLabel.grid(row=0, column=2, padx=padx_label, pady=pady_std,sticky='nsw')
    project = 'EFGHI'
    projectValue = ttk.Label(frame2,text=project,name='projectvalue')
    projectValue.grid(row=1, column=0, padx=padx_value, pady=pady_std,sticky='nsw')
    region = 'São Paulo'
    regionValue = ttk.Label(frame2,text=region,name='regionvalue')
    regionValue.grid(row=1, column=1,  padx=padx_value, pady=pady_std,sticky='nsw')
    status = 'Pending'
    statusValue = ttk.Label(frame2,text=status,name='statusvalue')
    statusValue.grid(row=1, column=2,  padx=padx_value, pady=pady_std,sticky='nsw')
    
    myList = [frame1,frame2]   
    table.fillTable(myList,True)
    
    table.updateItem(widget = 'frame1',borderwidth=3)
    table.updateItem(widget = 'frame2.regionvalue',text='Lyon',font=('Arial',20,'bold'))
    table.updateItem(widget = 'frame2.statusvalue',text='OK',background="#85DE87")
    
    root.mainloop()
    