import wx
from abc import ABCMeta, abstractmethod
from TPVS import TPVS
from Material import Material
from MXB import MXB

class Interface(metaclass=ABCMeta):
    @abstractmethod
    def SetData(self,data):
        pass
    
    @abstractmethod
    def GetData(self):
        pass

    @abstractmethod
    def MaterialChanged(self):
        pass

    @abstractmethod
    def VSChanged(self):
        pass

class Support(Interface):
    def __init__(self,parent):
        self.parent=parent
        self.frame = wx.Frame(None, -1, '测试Support',
                     pos=wx.DefaultPosition,
                     size=(700,605)
                     )
        self.frame.Center()
        panel = wx.Panel(self.frame)
        panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 2), size=(195, 110), style=wx.BORDER_THEME)
        panel2 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 117), size=(195, 200), style=wx.BORDER_THEME)
        panel3 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 322), size=(195, 182), style=wx.BORDER_THEME)
        panel4 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 507), size=(680, 55), style=wx.BORDER_THEME)
        panel5 = wx.Panel(panel, id=wx.ID_ANY, pos=(200,2), size=(485,475), style=wx.BORDER_SUNKEN)
        panel5.SetBackgroundColour((255,255,255))
        self.tpvs=TPVS(self,panel1)
        self.material=Material(self,panel2)
        self.mxb=MXB(self,panel4)
        
    def SetData(self,data):
        pass
    
    def GetData(self):
        pass

    def GetFatherTemp(self):
        temp='-19/250'
        return temp

    def GetFatherPre(self):
        pre='-0.1/2.5'
        return pre

    def GetFatherBaseMat(self):
        material=[True,'板材', 'GB/T 713-2014', 'Q345R',]
        return material

    def GetFatherCladMat(self):
        smaterial= ['不锈钢复合','S11306',]
        return smaterial
    
    def MaterialChanged(self):
        mat=self.material.GetMaterial()
        self.mxb.SetMaterial(material=mat)

    def VSChanged(self):
        vol=20
        surf=30
        n=self.mxb.GetQuantity()
        self.tpvs.SetV(vol*n)
        self.tpvs.SetS(surf*n)

    
    
if __name__ == '__main__':
    app = wx.App()
    mainapp=Support(None)
    mainapp.frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
