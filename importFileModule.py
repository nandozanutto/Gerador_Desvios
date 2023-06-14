import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
from absModule import AbsModule
from tkinter import *

class ImportFileModule(AbsModule):
    
    def __init__(self):
        super().__init__()
        self.__boxText = tk.StringVar()
    
    def createStructure(self,**kwargs):
        ''' This method will create the importFileModule structure. Some parameters can be set and they are listed below:
        
        -> boxText: specifies the text that will be inside the entry when created.
            It has to be a string. e.g:
                    boxText = 'Hello World'
            DEFAULT VALUE = ''
            
        -> boxSpan: specifies the distance, between boxText and elements around it, in pixels.
            It has to be a tuple e.g: 
                    boxSpan = (padx,pady), or
                    boxSpan = ((padx(leftside),padx(rightside)),(pady(upside),pady(downside)))
            DEFAULT VALUE = ((2,2),(2,2))
        
        -> boxSticky = specifies the position of boxText inside the frame.
            It has to be a string and a tkinter sticky value. e.g:
                    boxSticky = 'nsew' or
                    boxSticky = 'w'
            DEFAULT VALUE = 'w'
        
        -> boxWidth: specifies the absolute width of entry area as a number of characters.
            It has to be an integer. e.g:
                    boxWidth = 30
            DEFAULT VALUE = 20
        
        -> boxRelief: specifies box  relief.
            It has to be a string and a valid tkinter relief value. e.g:
                    boxRelief = GROOVE, or
                    boxRelief = RIDGE
            DEFAULT VALUE = GROOVE
            
        -> browseBtnText: specifies the text that appears inside the button. This button opens a file or directory dialog.
            It has to be a string. e.g:
                    browseBtnText = 'Choose File'
            DEFAULT VALUE = 'Browse'
        
        -> browseBtnSpan: specifies distance, between browseBtn and the elements around it, in pixels.
            It has to be a tuple e.g: 
                        browseBtnSpan = (padx,pady), or
                        browseBtnSpan = ((padx(leftside),padx(rightside)),(pady(upside),pady(downside)))
            DEFAULT VALUE = ((2,2),(2,2))
        
        -> browseBtnSticky: specifies the position of browseBtn inside the frame.
            It has to be a string and a tkinter sticky value. e.g:
                        browseBtnSticky = 'nsew' or
                        browseBtnSticky = 'w'
            DEFAULT VALUE = 'w'
            
        -> btnsWidth: specifies the absolute width of the text area on the button, as a number of characters.
            It has to be an integer. e.g:
                    btnsWidth = 30
            DEFAULT VALUE = ''
        
        -> processBtn: specifies the presence of the processBtn. This button doesn't have a command when created.
            It has to be a bool. e.g:
                    processBtnText = False
            DEFAULT VALUE = True 
            
        -> processBtnText: specifies the text that appears inside the button. This button doesn't have a command when created.
            It has to be a string. e.g:
                    processBtnText = 'Start Process'
            DEFAULT VALUE = 'Process' 
            
        -> processBtnSpan: specifies distance, between processBtn and the elements around it, in pixels.
            It has to be a tuple e.g: 
                        processBtnSpan = (padx,pady), or
                        processBtnSpan = ((padx(leftside),padx(rightside)),(pady(upside),pady(downside)))
            DEFAULT VALUE = ((2,2),(2,2))
        
        ->  processBtnSticky: specifies the position of processBtn inside the frame.
            It has to be a string and a tkinter sticky value. e.g:
                    processBtnSticky  = 'nsew' or
                    processBtnSticky  = 'w'
            DEFAULT VALUE = 'w'
            
        -> orientation: specifies the orientation of all three widgets (btn, entry, btn).
            It has to be a string and only two values are accepted.. e.g:
                    orientation = 'vertical'
                    orientation = 'horizontal'
            DEFAULT VALUE = 'horizontal'
            
        -> isFile: specifies if browse button will askfile or askdirectory.
            It has to be a boolean. e.g:
                    isFile = True
                    isFile = False
            DEFAULT VALUE = True
            
        -> fitInFrame: if set True configures the importFileModule to expand inside frame's size.
            If not set as parameter it won't be configured.
            It has to be boolean. e.g:
                    fitInFrame = True/False
            DEFAULT VALUE = ''
        '''
        super().createStructure(**kwargs)
        
        boxSpan = kwargs.get('boxSpan')
        if boxSpan == None:
            boxSpan = ((2,2),(2,2))
        elif not isinstance(boxSpan,tuple):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs boxSpan argument as a Tuple class with two arguments. e.g: (padx,pady) or"
                            "((padx(left),padx(right)),(pady(up),pady(down))).")
        
        boxSticky = kwargs.get('boxSticky')
        if  boxSticky == None:
            boxSticky = 'w'
        elif not isinstance(boxSticky,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs  boxSticky argument as a Str class and a tkinter sticky value. e.g: w,e,nsew:")
        
        boxWidth = kwargs.get('boxWidth')
        if boxWidth == None:
            boxWidth = 20
        elif not isinstance(boxWidth,int):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs boxWidth argument as a Int class with two arguments. e.g: 20")
        
        boxRelief = kwargs.get('boxRelief')
        if boxRelief == None:
            boxRelief = GROOVE
        elif not isinstance(boxRelief,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs boxRelief argument as a string and a valid tkinter relief value. e.g:boxRelief = GROOVE")
        
        browseBtnText = kwargs.get('browseBtnText')
        if browseBtnText == None:
            browseBtnText = 'Browse'
        elif not isinstance(browseBtnText,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs browseBtnText argument as a Str class. e.g: 'Browse button'") 
        
        browseBtnSpan = kwargs.get('browseBtnSpan')
        if browseBtnSpan == None:
            browseBtnSpan = ((2,2),(2,2))
        elif not isinstance(browseBtnSpan,tuple):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs browseBtnSpan argument as a Tuple class with two arguments. e.g: (padx,pady) or"
                            "((padx(left),padx(right)),(pady(up),pady(down))).")
        
        browseBtnSticky = kwargs.get('browseBtnSticky')
        if  browseBtnSticky == None:
             browseBtnSticky = 'w'
        elif not isinstance( browseBtnSticky,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs  browseBtnSticky argument as a Str class and a tkinter sticky value. e.g: w,e,nsew:")
        
        browseBtnWidth = kwargs.get('browseBtnWidth')
        if browseBtnWidth == None:
            browseBtnWidth = ''
        elif not isinstance(browseBtnWidth,int):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs browseBtnWidth argument as a Int class with two arguments. e.g: 20") 
        
        processBtn = kwargs.get('processBtn')
        if processBtn == None:
            processBtn = True
        elif not isinstance(processBtn,bool):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs processBtn argument as a Bolean class. e.g: False") 

        processBtnText = kwargs.get('processBtnText')
        if processBtnText == None:
            processBtnText = 'Process'
        elif not isinstance(processBtnText,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs processBtnText argument as a Str class. e.g: 'Process button'") 
        
        processBtnSpan = kwargs.get('processBtnSpan')
        if processBtnSpan == None:
            processBtnSpan = ((2,2),(2,2))
        elif not isinstance(processBtnSpan,tuple):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs processBtnSpan argument as a Tuple class with two arguments. e.g: (padx,pady) or"
                            "((padx(left),padx(right)),(pady(up),pady(down))).") 
        
        processBtnSticky = kwargs.get('processBtnSticky')
        if processBtnSticky == None:
            processBtnSticky = 'w'
        elif not isinstance(processBtnSticky,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs processBtnSticky argument as a Str class and a tkinter sticky value. e.g: w,e,nsew:")
        
        processBtnWidth = kwargs.get('processBtnWidth')
        if processBtnWidth == None:
            processBtnWidth = ''
        elif not isinstance(processBtnWidth,int):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs processBtnWidth argument as a Str class and a tkinter sticky value. e.g: w,e,nsew:")
        
        orientation = kwargs.get('orientation')
        if orientation == None:
            orientation = 'horizontal'
        elif not isinstance(orientation,str):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs orientation as Str class. Options are only vertical or horizontal.")
        
        self.__isFile = kwargs.get('isFile')
        if self.__isFile == None:
            self.__isFile = True
        elif not isinstance(self.__isFile,bool):
            raise TypeError("descriptor 'createStructure' of 'importFileModule' object needs isFIle as a Bool class.")
        
        #Creates browseBtn, entryBox,processBtn
        self.__browseBtn = ttk.Button(master=self._labelFrame,text=browseBtnText,width=browseBtnWidth,
                                      command= self.__importFile if self.__isFile else self.__importDir)
        
        self.__boxText.set(kwargs.get('boxText',''))
        self.__pathBox = tk.Entry(master=self._labelFrame,text=self.__boxText,width=boxWidth,relief=boxRelief)
        if processBtn:
            self.processBtn = ttk.Button(master=self._labelFrame,text=processBtnText,width=processBtnWidth)
        
        # Widgets orientation
        if orientation == 'horizontal':
            self.__browseBtn.grid(row=0,column=0,padx=browseBtnSpan[0],pady=browseBtnSpan[1],sticky = browseBtnSticky)
            self.__pathBox.grid(row=0,column=1,padx=boxSpan[0],pady=boxSpan[1],sticky = boxSticky)
            if processBtn:
                self.processBtn.grid(row=0,column=2,padx=processBtnSpan[0],pady=processBtnSpan[1],sticky = processBtnSticky)
            if kwargs.get('fitInFrame'):
                self._labelFrame.columnconfigure(1,weight=1)
                self._labelFrame.columnconfigure(2,weight=1)
        elif orientation == 'vertical':
            self.__browseBtn.grid(row=0,column=0,padx=browseBtnSpan[0],pady=browseBtnSpan[1],sticky = browseBtnSticky)
            self.__pathBox.grid(row=1,column=0,padx=boxSpan[0],pady=boxSpan[1],sticky = boxSticky)
            if processBtn:
                self.processBtn.grid(row=2,column=0,padx=processBtnSpan[0],pady=processBtnSpan[1],sticky = processBtnSticky)
            if kwargs.get('fitInFrame'):
                self._labelFrame.rowconfigure(1,weight=1)
                self._labelFrame.rowconfigure(2,weight=1)
        else:
            raise RuntimeError("ERROR: orientation needs to be set as 'vertical' or 'horizontal.'")

            
    def __importFile(self):
        f = filedialog.askopenfilename()
        if f != None:
            self.__boxText.set(f)
            
    def __importDir(self):
        f = filedialog.askdirectory()
        if f != None:
            self.__boxText.set(f)
    
    def getPath(self):
        return self.__boxText.get()
    
if __name__ == "__main__":
    root = ThemedTk(theme="win")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
    imp = ImportFileModule()
    imp.createStructure(master=root,row=0,column=0,labelText='Import Section',orientation='vertical',
                                browseBtnText='Browse Folder',isFile=False,boxWidth=27,
                                processBtnText='Start Upload',processBtnSpan=((3,3),(40,3)),processBtnWidth=26,fitInFrame=True)
    
    def importFile(filePath):
        #do stuff with path, like load and other operations..
        print('File: '+ filePath + ' imported..')
    
    def setImportCallBack():
        filepath = (imp.getPath())
        importFile(filepath)
    
    imp.processBtn.configure(command=setImportCallBack())
    root.mainloop()
    