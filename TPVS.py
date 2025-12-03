import wx
from ALLPartData import PartsData
   
class TPVS():
    def __init__(self,parent, panel):
        self.panel=panel
        self.parent=parent
        self.vol=0.0
        self.surf=0.0
        px = 5
        py = 5
        self.cb11 = wx.CheckBox(panel, label = '继承', pos = (px,py))
        self.cb12 = wx.CheckBox(panel, label = '继承', pos = (px,py+25))
        self.cb13 = wx.CheckBox(panel, label = '计算', pos = (px,py+50))
        self.cb14 = wx.CheckBox(panel, label = '计算', pos = (px,py+75))
        wx.StaticText(panel,label ='设计温度', pos =(px+50,py))
        wx.StaticText(panel,label ='设计压力', pos =(px+50,py+25))
        wx.StaticText(panel,label ='内容积', pos =(px+50,py+50))
        wx.StaticText(panel,label ='外表面积', pos =(px+50,py+75))
        self.cb16 = wx.TextCtrl(panel, value = "", pos =(px+100,py), size = (50,20),style=wx.TE_CENTER)
        self.cb17 = wx.TextCtrl(panel, value = "", pos =(px+100,py+25), size = (50,20),style=wx.TE_CENTER)
        self.cb18 = wx.TextCtrl(panel, value = "", pos =(px+100,py+50), size = (50,20),style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb19 = wx.TextCtrl(panel, value = "", pos =(px+100,py+75), size = (50,20),style=wx.TE_CENTER|wx.TE_READONLY)
        wx.StaticText(panel,label ='℃', pos =(px+152,py))
        wx.StaticText(panel,label ='MPa', pos =(px+152,py+25))
        wx.StaticText(panel,label ='m^3', pos =(px+152,py+50))
        wx.StaticText(panel,label ='m^2', pos =(px+152,py+75))
        self.cb11.Bind(wx.EVT_CHECKBOX,self.OnCheckBox11)
        self.cb12.Bind(wx.EVT_CHECKBOX,self.OnCheckBox12)
        self.cb13.Bind(wx.EVT_CHECKBOX,self.OnCheckBox13)
        self.cb14.Bind(wx.EVT_CHECKBOX,self.OnCheckBox14)
    
    def OnCheckBox11(self,evt):
      if self.cb11.GetValue():
          self.cb16.Enable(False) 
          tem=self.parent.GetFatherTemp()
          self.cb16.SetValue(tem)
      else:
          self.cb16.Enable(True)
      
    def OnCheckBox12(self,evt):       
      if self.cb12.GetValue():
          self.cb17.Enable(False)
          pre=self.parent.GetFatherPre()
          self.cb17.SetValue(pre)
      else:
         self.cb17.Enable(True)
         
    def OnCheckBox13(self,evt):
      if self.cb13.GetValue():
         self.cb18.SetValue('%.2f' % self.vol)
      else:
         self.cb18.SetValue(' ')
      
    def OnCheckBox14(self,evt):
      if self.cb14.GetValue():
         self.cb19.SetValue('%.2f' % self.surf)
      else:
         self.cb19.SetValue('')

    def SetT(self, t=''):
        try:
            self.cb16.SetValue(t)
        except:
            self.cb16.SetValue('')
            wx.MessageBox('设计温度数据有误。', '出错', wx.OK)

    def GetT(self):
        return self.cb16.GetValue()

    def SetP(self, p=''):
        try:
            self.cb17.SetValue(p)
        except:
            self.cb17.SetValue('')
            wx.MessageBox('设计压力数据有误。', '出错', wx.OK)

    def GetP(self):
        return self.cb17.GetValue()

    def SetV(self, v=0.00):
        self.vol=v
        if self.cb13.GetValue():
            try:
                self.cb18.SetValue('%.2f' % v)
            except:
                self.cb18.SetValue('0.00')
        else:
            self.cb18.SetValue('')
            
    def GetV(self):
        t1=self.cb18.GetValue()
        if t1 in ['','0','0.0','0.00']:
            vol=0
        else:
            vol=float(t1)
        return vol

    def SetS(self, s=0.00):
        self.surf=s
        if self.cb14.GetValue():
            try:
                self.cb19.SetValue('%.2f' % s)
            except:
                self.cb19.SetValue('0.00')
        else:
            self.cb19.SetValue('')

    def GetS(self):
        t1=self.cb19.GetValue()
        if t1 in ['','0','0.0','0.00']:
            surf=0
        else:
            surf=float(t1)
        return surf
    
    def Enable(self,value=True):
        self.panel.Enable(value)
    
    def TPNonInheritable(self):
        self.cb11.SetValue(False)
        self.cb11.Enable(False)
        self.cb12.SetValue(False)
        self.cb12.Enable(False)

    def VSUncalculable(self):
        self.vol=0.0
        self.surf=0.0
        self.cb13.SetValue(False)
        self.cb13.Enable(False)
        self.cb14.SetValue(False)
        self.cb14.Enable(False)
        self.cb18.SetValue('')
        self.cb19.SetValue('')
        
    def GetData(self):
       return [self.cb11.IsEnabled(),
                 self.cb11.GetValue(),
                 self.cb16.GetValue(),
                 self.cb12.IsEnabled(),
                 self.cb12.GetValue(),
                 self.cb17.GetValue(),
                 self.cb13.IsEnabled(),
                 self.cb13.GetValue(),
                 self.cb18.GetValue(),
                 self.cb14.IsEnabled(),
                 self.cb14.GetValue(),
                 self.cb19.GetValue(),
                 self.vol,
                 self.surf
               ]
    
    def SetData(self,data):
        #SetValue会产生一个wx.EVT_TEXT事件而ChangeValue不会产生wx.EVT_TEXT事件
        self.cb11.Enable(data[0])
        self.cb11.SetValue(data[1])
        self.cb16.ChangeValue(data[2])
        if data[1]:
            self.cb16.Enable(False)
        else:
            self.cb16.Enable(True)
        self.cb12.Enable(data[3])
        self.cb12.SetValue(data[4])
        self.cb17.ChangeValue(data[5])
        if data[4]:
            self.cb17.Enable(False)
        else:
            self.cb17.Enable(True)
        self.cb13.Enable(data[6])
        self.cb13.SetValue(data[7])
        self.cb18.SetValue(data[8])
        self.cb14.Enable(data[9])
        self.cb14.SetValue(data[10])
        self.cb19.SetValue(data[11])
        self.vol=data[12]
        self.surf=data[13]

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, '测试TPVS类',pos=(10, 10), size=(280, 500))
    frame.Center()
    panel = wx.Panel(frame)
    panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 2), size=(195, 110), style=wx.BORDER_THEME)
    data=[True, True, '120',True, True, '2.5', True, False, '', True, False, '',0.00,0.00]
    pt1=TPVS(None,panel1)
    pt1.SetData(data)
    frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
