import wx
    
class Weight():
    def __init__(self,parent, panel):
        self.parent=parent
        posx=5
        posy=5
        posz=25
        self.cb311=wx.StaticText(panel,label ="    重量", pos =(posx,posy+0*posz))
        self.cb31=wx.TextCtrl(panel,pos=(posx+55,posy+0*posz),size = (80,22),value ='0', style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb312=wx.StaticText(panel,label ="Kg/件", pos =(posx+140,posy+0*posz))
        self.cb321=wx.StaticText(panel,label ="   其中不锈钢", pos =(posx,posy+1*posz))
        self.cb32=wx.TextCtrl(panel,pos=(posx+80,posy+1*posz),size = (55,22),value ='0', style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb322=wx.StaticText(panel,label ="Kg/件", pos =(posx+140,posy+1*posz))

        self.cb331=wx.StaticText(panel,label ="重量调节系数：", pos =(posx,posy+2*posz))
        self.cb33=wx.Slider(panel, id=wx.ID_ANY, value=15, minValue=0, maxValue=100,
                             pos =(0,posy+3*posz),
                             size = (150,22),
                             style=wx.SL_HORIZONTAL)
        self.cb332=wx.TextCtrl(panel,pos=(posx+145,posy+3*posz),size = (40,22),value ='1.15', style=wx.TE_CENTER)
        self.cb341=wx.StaticText(panel,label ="    重量", pos =(posx,posy+4*posz))
        self.cb34=wx.TextCtrl(panel,pos=(posx+55,posy+4*posz),size = (80,22),value ='0', style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb342=wx.StaticText(panel,label ="Kg/件", pos =(posx+140,posy+4*posz))
        self.cb351=wx.StaticText(panel,label ="   其中不锈钢", pos =(posx,posy+5*posz))
        self.cb35=wx.TextCtrl(panel,pos=(posx+80,posy+5*posz),size = (55,22),value ='0', style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb352=wx.StaticText(panel,label ="Kg/件", pos =(posx+140,posy+5*posz))
        self.cb33.Bind(wx.EVT_SCROLL,self.OnSlider33)
        self.cb332.Bind(wx.EVT_TEXT,self.OnTextCtrl332)
        self.cb31.Bind(wx.EVT_TEXT,self.OnTextCtrl332)
        self.cb32.Bind(wx.EVT_TEXT,self.OnTextCtrl332)
#        self.frame.Bind(wx.EVT_SET_FOCUS,self.OnFocus)

    def OnSlider33(self,evt):
        t=self.cb33.GetValue()
        t=1+t/100
        t=('%.2f' % t)
        self.cb332.SetValue(str(t))

    def OnTextCtrl332(self,evt):
        ta=self.cb332.GetValue()
        try:
            t=float(ta)
            t=int((t-1)*100)
            if t>=100:
                t=100
            if t<=0:
                t=0
        except:
            t=0
        self.cb33.SetValue(t)
        t=float(ta)
        t1=self.cb31.GetValue()
        t2=self.cb32.GetValue()
        t3=int(float(t1)*t)
        t4=int(float(t2)*t)
        self.cb34.SetValue(str(t3))
        self.cb35.SetValue(str(t4))
        self.parent.SlideScChanged()
#        print(self.GetWeightCS())
#        print(self.GetWeightSS())

    def GetData(self):
        return [self.cb31.GetValue(),
            self.cb32.GetValue(),
            self.cb33.GetValue(),
            self.cb332.GetValue(),
            self.cb34.GetValue(),
            self.cb35.GetValue()
            ]
    
    def SetData(self,data):
            self.cb31.ChangeValue(data[0])
            self.cb32.ChangeValue(data[1])
            self.cb33.SetValue(data[2])
            self.cb332.ChangeValue(data[3])
            self.cb34.ChangeValue(data[4])
            self.cb35.ChangeValue(data[5])

    def SetWeightCS(self, weightcs=0.0):
        weightss=float(self.cb32.GetValue())
        self.cb31.SetValue('%.1f' % (weightcs+weightss))

    def SetWeightSS(self, weightss=0.0):
        self.cb32.SetValue('%.1f' % (weightss))

    def GetWeightCS(self):
        return float(self.cb34.GetValue())-self.GetWeightSS()

    def GetWeightSS(self):
        return float(self.cb35.GetValue())

    def GetWeight(self):
        #获取公称重量
        t1=self.GetWeightCS()
        t2=self.GetWeightSS()
        t=int((t1+t2+4.5)/5)*5
        return t
    
if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, '测试Weight类',pos=(10, 10), size=(800, 600))
    frame.Center()
    panel = wx.Panel(frame)
    panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 5), size=(195, 195), style=wx.BORDER_THEME)
    data=['123', '000', 15, '1.15', '123', '0.0']
    pt1=Weight(None,panel1)
    print(pt1.GetData())
    pt1.SetData(data)
    pt1.SetWeightCS(388.6)
    pt1.SetWeightSS(38.8)
    frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
