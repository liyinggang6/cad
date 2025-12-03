import wx
#from softwareEvaluation import soft_evaluation
from ALLPartData import PartsData
from Shell import Shell
from TPVS import TPVS
from Material import Material
from MXB import MXB
from Control import ControlForNozzleFlange
from Image import ImageForNozzleFlange
    
class NozzleFlange(Shell):
    allpart_data=PartsData()
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                     pos=wx.DefaultPosition,
                     size=(702,605)
                     )
        self.frame.SetLabel('管法兰')
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
        self.material=Material(self,panel2)
        self.control=ControlForNozzleFlange(self,panel3)
        self.mxb=MXB(self,panel4)
        self.image=ImageForNozzleFlange(self,panel5)
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
                                                   '正在处理管法兰...')
        except:
            evaluation='未能提交管法兰后评价信息。'
        print(evaluation)
        
    def VSChanged(self):
        self.QuantityChanged()
        data=self.image.GetData()
        name=self.control.GetName(data)
        self.mxb.SetName(name)
        weightcs,weightss=self.WeightCal()
        self.mxb.SetWeight(weightcs,weightss)

    def VSCal(self):
        data=self.image.GetData()
        vol=self.control.GetVol(data)
        surf=self.control.GetSurf(data)
        return vol,surf
    
    def GetGuanKou(self):
        #获取管口信息供管口表和管口载荷表使用
        b0=self.control.cb31.GetValue() #法兰标准 HG/T 20615-2009
        b1=self.control.cb32.GetValue() #法兰类型 WN SO
        b2=self.control.cb33.GetValue() # 系列 A B
        b3=self.control.cb34.GetValue().split("  ")[0] #压力等级 PN20
        b4=self.control.cb35.GetValue() #密封面 RF
        b5=self.control.cb36.GetValue().split("  ")[0] # 公称直径 100 80
        b6=self.control.cb37.GetValue().split("  ")[0] # 配对接管 Sch.80 8mm
        c=self.mxb.LocList
        # 中的数据格式
        # [[基准点，基准点，基点相对坐标，导向点相对坐标，管口符号，管口用途，是否建模],[...]...]
        b61='--'
        if 'm' in b6:
            b61="S="+b6
        if 'ch' in b6:
            b61=b6
        guankou_list=[]
        for i in c:
            if i[4] not in self.allpart_data.Kong:
                guankou_list.append([i[4],b5,b3,b61,b0+b2+' '+b1,b4,'见图',i[5],i[6]])
        return guankou_list
       
        
        
    
