from abc import ABC,abstractmethod
import tkinter.ttk as ttk

class AbsModule(ABC):
    def __init__(self):
        self._mainFrame = None
        self.__loadStyles()
    
    @classmethod
    @abstractmethod
    def createStructure(self,**kwargs):
        if not kwargs.get('master'):
            raise RuntimeError("ERROR: Module root not defined.")
        else:
            self._master = kwargs.get('master')
          
        rootFrameSpan = kwargs.get('rootFrameSpan')
        if rootFrameSpan == None:
            rootFrameSpan = ((5,5),(5,5))
            print('WARNING: Argument rootFrameSpan was not defined, so it will be set its default value: ((5,5),(5,5))')
        elif not isinstance(rootFrameSpan,tuple):
            raise TypeError("descriptor 'createStructure' of 'AbsModule' object needs rootFrameSpan argument as a Tuple class with two arguments. e.g: (padx,pady) or"
                            "((padx(left),padx(right)),(pady(up),ipady(down))).") 
            
        self._mainFrame = ttk.Frame(master=self._master)
        self._mainFrame.grid(row=kwargs.get('row',0), column=kwargs.get('column',0),padx=rootFrameSpan[0],pady=rootFrameSpan[1],sticky='nsew')
        self._mainFrame.columnconfigure(0,weight=1)
        self._mainFrame.rowconfigure(0,weight=1)
        
        self._labelFrame = ttk.LabelFrame(master=self._mainFrame,text=kwargs.get('labelText', self.__name__))
        self._labelFrame.grid(row=0, column=0,sticky='nsew')
        self._labelFrame.columnconfigure(0,weight=1)
        self._labelFrame.rowconfigure(0,weight=1)
        
    def __loadStyles(self):
        self.style = ttk.Style()
        #TABLE
        self.style.configure('OKTable.TLabel', font=('Segoe UI', 10),background="#85DE87")
        self.style.configure('OKBold.TLabel', font=('Segoe UI', 10,'bold'),background="#85DE87")
        self.style.configure('NOKTable.TLabel', font=('Segoe UI', 10),background="#F2F2F2")
        self.style.configure('NOKBold.TLabel', font=('Segoe UI', 10,'bold'),background="#F2F2F2")
        self.style.configure('White.TLabel', font=('Segoe UI', 12), background="#FFFFFF")
        self.style.configure('WhiteBold.TLabel', font=('Segoe UI', 12,'bold'), background="#FFFFFF")
        self.style.configure('TEntry', font=('Segoe UI', 13), background="#FFFFFF")
        self.style.configure('NOK.TFrame', background="#F2F2F2")
        self.style.configure('OK.TFrame', background="#85DE87")
        #LOG
        self.style.configure("ERROR.TLabel", font=('Segoe UI', 10,'bold'), background="#FF6961")
        self.style.configure("WARNING.TLabel", font=('Segoe UI', 10,'bold'), background="#FDFD96")
        self.style.configure("SUCESSFULL.TLabel", font=('Segoe UI', 10,'bold'), background="#89c689")
        self.style.configure("MAIN.TLabel", font=('Segoe UI', 10))