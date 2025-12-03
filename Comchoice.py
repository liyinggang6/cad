import wx
from abc import ABCMeta, abstractmethod

class Interface(metaclass=ABCMeta):
    @abstractmethod
    def GetName(self):
        pass #获取类型名称

    @abstractmethod
    def GetFluid(self):
        pass

    @abstractmethod
    def GetDensity(self):
        pass

    @abstractmethod
    def GetCA(self): #获取腐蚀余量CORROSION ALLOWANCE
        pass

    @abstractmethod
    def GetData(self):
        pass
    
    @abstractmethod
    def SetData(self,data):
        pass
    
class ControlForComponent(Interface):
    def __init__(self,parent, panel):
        self.parent=parent
        px=5
        py=5
        pz=25
        wx.StaticText(panel,label ="部件类型", pos =(px,py+0*pz))
        wx.StaticText(panel,label ="介    质", pos =(px,py+1*pz))
        wx.StaticText(panel,label ="介质密度", pos =(px,py+2*pz))
        wx.StaticText(panel,label ="Kg/m3", pos =(px+155,py+2*pz))
        wx.StaticText(panel,label ="腐蚀余量", pos =(px,py+3*pz))
        wx.StaticText(panel,label ="mm(单面)", pos =(px+155,py+3*pz))
        wx.StaticText(panel,label ="装量系数", pos =(px,py+4*pz))
        self.cb11=wx.ComboBox(panel,
                              pos=(px+50,py+0*pz),
                              size = (130,22),
                              choices=["容器","壳程","管程","外夹套","外伴管","内伴管","内浮头","组合件",],
                              style=wx.CB_DROPDOWN)
        self.cb12=wx.ComboBox(panel,
                              pos=(px+50,py+1*pz),
                              size = (130,22),
                              choices=["水/蒸汽","工艺气","工艺液","循环水","冷冻水","合成气",],
                              style=wx.CB_DROPDOWN)
        self.cb13=wx.ComboBox(panel,
                              pos=(px+50,py+2*pz),
                              size = (100,22),
                              choices=["600","650","800","900","1000","1200",],
                              style=wx.CB_DROPDOWN)
        self.cb14=wx.ComboBox(panel,
                              pos=(px+50,py+3*pz),
                              size = (100,22),
                              choices=['3.0','2.0','1.5','1.0','0'],
                              style=wx.CB_DROPDOWN)
        self.cb15=wx.ComboBox(panel,
                              pos=(px+50,py+4*pz),
                              size = (100,22),
                              choices=['1.0','0.95','0.9','0.85','0.8','0.75','0.7'],
                              style=wx.CB_DROPDOWN)   
        self.cb21 = wx.CheckBox(panel, label = '晶间腐蚀', pos = (px,py+5*pz))
        self.cb22 = wx.CheckBox(panel, label = '氢腐蚀', pos = (px,py+6*pz))
        self.cb23 = wx.CheckBox(panel, label = '湿H2S腐蚀', pos = (px,py+7*pz))
        self.cb24 = wx.CheckBox(panel, label = '严重湿H2S腐蚀', pos = (px,py+8*pz))
        self.cb25 = wx.CheckBox(panel, label = 'NH3腐蚀', pos = (px,py+9*pz))
        self.cb26 = wx.CheckBox(panel, label = '易燃', pos = (px+130,py+5*pz))
        self.cb27 = wx.CheckBox(panel, label = '易爆', pos = (px+130,py+6*pz))
        self.cb28 = wx.CheckBox(panel, label = '中度危害', pos = (px+130,py+7*pz))
        self.cb29 = wx.CheckBox(panel, label = '高度危害', pos = (px+130,py+8*pz))
        self.cb210 = wx.CheckBox(panel, label = '极度危害', pos = (px+130,py+9*pz))
        self.cb11.Bind(wx.EVT_TEXT,self.OnCombobox11)
        self.cb22.Bind(wx.EVT_CHECKBOX,self.OnCheckBox22)
        self.cb23.Bind(wx.EVT_CHECKBOX,self.OnCheckBox23)
        self.cb24.Bind(wx.EVT_CHECKBOX,self.OnCheckBox24)
        self.cb25.Bind(wx.EVT_CHECKBOX,self.OnCheckBox25)
        self.cb26.Bind(wx.EVT_CHECKBOX,self.OnCheckBox26)
        self.cb27.Bind(wx.EVT_CHECKBOX,self.OnCheckBox27)
        self.cb28.Bind(wx.EVT_CHECKBOX,self.OnCheckBox28)
        self.cb29.Bind(wx.EVT_CHECKBOX,self.OnCheckBox29)
        self.cb210.Bind(wx.EVT_CHECKBOX,self.OnCheckBox210)

    def OnCombobox11(self,evt):
        t1='部件->'+self.cb11.GetValue()
        self.parent.frame.SetLabel(t1)
        self.parent.Main.tree.SetItemText(self.parent.currentnode, t1)
        self.parent.mxb.SetName(self.cb11.GetValue())
        
        
    def OnCheckBox22(self,evt):
        if self.cb22.GetValue():
            self.cb25.SetValue(False)
            
    def OnCheckBox23(self,evt):
        if self.cb23.GetValue():
            self.cb24.SetValue(False)

    def OnCheckBox24(self,evt):
        if self.cb24.GetValue():
            self.cb23.SetValue(False)

    def OnCheckBox25(self,evt):
        if self.cb25.GetValue():
            self.cb22.SetValue(False)

    def OnCheckBox26(self,evt):
        if self.cb26.GetValue():
            self.cb27.SetValue(False)

    def OnCheckBox27(self,evt):
        if self.cb27.GetValue():
            self.cb26.SetValue(False)

    def OnCheckBox28(self,evt):
        if self.cb28.GetValue():
            self.cb29.SetValue(False)
            self.cb210.SetValue(False)

    def OnCheckBox29(self,evt):
        if self.cb29.GetValue():
            self.cb28.SetValue(False)
            self.cb210.SetValue(False)

    def OnCheckBox210(self,evt):
        if self.cb210.GetValue():
            self.cb28.SetValue(False)
            self.cb29.SetValue(False)
  
    def GetName(self):
        return self.cb11.GetValue()

    def GetFluid(self):
        return self.cb12.GetValue()

    def GetDensity(self):
        return self.cb13.GetValue()

    def GetCA(self): 
        return self.cb14.GetValue()

    def GetData(self):
        return [self.cb11.GetValue(),
                self.cb12.GetValue(),
                self.cb13.GetValue(),
                self.cb14.GetValue(),
                self.cb15.GetValue(),
                self.cb21.GetValue(),
                self.cb22.GetValue(),
                self.cb23.GetValue(),
                self.cb24.GetValue(),
                self.cb25.GetValue(),
                self.cb26.GetValue(),
                self.cb27.GetValue(),
                self.cb28.GetValue(),
                self.cb29.GetValue(),
                self.cb210.GetValue(),
                ]
    
    def SetData(self,data):
        self.cb11.ChangeValue(data[0])
        self.cb12.ChangeValue(data[1])
        self.cb13.ChangeValue(data[2])
        self.cb14.ChangeValue(data[3])
        self.cb15.ChangeValue(data[4])
        self.cb21.SetValue(data[5])
        self.cb22.SetValue(data[6])
        self.cb23.SetValue(data[7])
        self.cb24.SetValue(data[8])
        self.cb25.SetValue(data[9])
        self.cb26.SetValue(data[10])
        self.cb27.SetValue(data[11])
        self.cb28.SetValue(data[12])
        self.cb29.SetValue(data[13])
        self.cb210.SetValue(data[14])
    
if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, '测试Comchoice类',pos=(10, 10), size=(800, 600))
    frame.Center()
    panel = wx.Panel(frame)
    panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 5), size=(220, 260), style=wx.BORDER_THEME)
    data=['壳程', '水/蒸汽', '650', '2.0','0.85', True, False, False, True, False, True, False, True, False, False]
    pt1=ControlForComponent(None,panel1)
    pt1.SetData(data)
    frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
