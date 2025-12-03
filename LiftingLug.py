import wx
#from softwareEvaluation import soft_evaluation
from ALLPartData import PartsData
from Shell import Shell
from TPVS import TPVS
from Material import Material
from MXB import MXB
from Control import ControlForLiftingLug
from Image import ImageForLiftingLug
    
class LiftingLug(Shell):
    allpart_data=PartsData()
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                     pos=wx.DefaultPosition,
                     size=(702,605)
                     )
        self.frame.SetLabel('吊耳')
        panel = wx.Panel(self.frame)
        panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 2), size=(195, 110), style=wx.BORDER_THEME)
        panel2 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 117), size=(195, 200), style=wx.BORDER_THEME)
        panel3 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 322), size=(195, 182), style=wx.BORDER_THEME)
        panel4 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 507), size=(680, 55), style=wx.BORDER_THEME)
        panel5 = wx.Panel(panel, id=wx.ID_ANY, pos=(200,2), size=(485,475), style=wx.BORDER_SUNKEN)
        panel5.SetBackgroundColour((255,255,255))
        self.weightcs=0
        self.weightss=0
        self.tpvs=TPVS(self,panel1)
        panel1.Disable()
        self.material=Material(self,panel2)
        self.control=ControlForLiftingLug(self,panel3)
        self.mxb=MXB(self,panel4)
        self.image = ImageForLiftingLug(self,panel5)
        self.cb81 = wx.Button(panel, label="确定&&关闭", pos=(614, 480), size=(68, 22))
        self.cb811 = wx.Button(panel, label="绘制明细栏-->", pos=(230, 480), size=(100, 22))
        self.cb812 = wx.Button(panel, label="绘图-->", pos=(350, 480), size=(60, 22))
#       self.cb818 = wx.Button(panel, label="测试", pos=(450, 480), size=(60, 22))
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
#       self.cb818.Bind(wx.EVT_BUTTON, self.OnButton818)
        self.cb811.Bind(wx.EVT_BUTTON,self.OnWait)
        self.cb812.Bind(wx.EVT_BUTTON,self.OnWait)
        token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJleHAiOjE2Njk5MDA1MDUsInVzZXJuYW1lIjoi5byg\
5LiJIn0.Q6YFZVEte9syYnUNv_drVDyqvZdyCQ7iRAKwj_\
kYxYI2ac44369-d85d-4716-a33a-71e49831660c'
        type_name="22720_化工设备梯子平台绘图软件"
        try:
            evaluation=soft_evaluation.soft_evaluation(token,type_name,
                                                   '正在处理吊耳...')
        except:
            evaluation='未能提交吊耳后评价信息。'
        print(evaluation)

    def SetData(self,data):
        self.SetLableData(data[0])
        self.material.SetData(data[2])
        self.control.SetData(data[3])
        self.control.OnCombobox33a(True)
        self.image.SetData(data[5])
        self.mxb.SetData(data[4])
        self.mxb.OnTextCtrl46d(True)
        self.mxb.location.SetData(data[6])
        self.mxb.location.OnClose(True)
        self.SetLableData(data[0])

    def VSChanged(self):
        self.QuantityChanged()
        data=self.image.GetData()
        name=self.control.GetName(data)
        self.mxb.SetName(name)
        weightcs,weightss=self.WeightCal()
        self.mxb.SetWeight(weightcs,weightss)

    def VSCal(self):
        data=self.image.GetData()
        print('image.GetData() in LiftingLug is:',data)
        vol=self.control.GetVol(data)
        surf=self.control.GetSurf(data)
        return vol,surf
    

       
        
        
    
