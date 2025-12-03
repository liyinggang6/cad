import wx
from ALLPartData import PartsData
from Component import Component
from TPVS import TPVS
from Material import Material
from MXB import MXB
from Control import ControlForShell
from Image import ImageForShell
from Location import Location

class Shell(Component):
    allpart_data=PartsData()
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                     pos=wx.DefaultPosition,
                     size=(702,605)
                     )
        self.frame.SetLabel('常用件')
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
        self.control=ControlForShell(self,panel3)
        self.mxb=MXB(self,panel4)  #MXB内部已经给本类增加了location
##      self.location=Location(self,1)
##        i=self.allpart_data.equipment_design_data[2]
##        ctrl_data=[[[i[0][3],(0,0),(0,0)],i[1]],]
        self.image=ImageForShell(self,panel5)
        self.cb81 = wx.Button(panel, label="确定&&关闭", pos=(614, 480), size=(68, 22))
        self.cb811 = wx.Button(panel, label="绘制明细栏-->", pos=(230, 480), size=(100, 22))
        self.cb812 = wx.Button(panel, label="绘图-->", pos=(350, 480), size=(60, 22))
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
        self.cb811.Bind(wx.EVT_BUTTON,self.OnWait)
        self.cb812.Bind(wx.EVT_BUTTON,self.OnWait)

    def OnButton821(self,evt):
        print(self.GetData())
        
    def OnButton811(self,evt):
        print('---------------------------------------')
        print(self.control.GetSc())
        print(self.control.GetTukuangAndKeyPoint())
        print(self.control.GetTuType())
        print(self.control.GetSiteType())
        print('---------------------------------------')
        print(self.tpvs.GetData())
        print(self.material.GetData())
        print(self.control.GetData())
        print(self.image.GetData())
        print(self.weight.GetData())
        print('---------------------------------------')
            
    def SetData(self,data):
        self.SetLableData(data[0])
        self.tpvs.SetData(data[1])
        self.material.SetData(data[2])
        self.control.SetData(data[3])
        self.image.SetData(data[5])
        self.mxb.SetData(data[4])
        self.mxb.OnTextCtrl46d(True)
        self.mxb.location.SetData(data[6])
        self.mxb.location.OnClose(True)
        self.SetLableData(data[0])
        
    def GetData(self):
        list1 = self.GetLableData()
        return [list1,
                self.tpvs.GetData(),
                self.material.GetData(),
                self.control.GetData(),
                self.mxb.GetData(),
                self.image.GetData(),
                self.mxb.location.GetData(),
                ]

    def StandardChanged(self, newstandard=''):
        self.mxb.SetStandard(newstandard)

    def NameChanged(self,newname=''):
        self.mxb.SetName(newname)

    def NoteChanged(self,newnote=''):
        self.mxb.SetNote(newnote)
      
    def MaterialChanged(self):
        self.mxb.SetMaterial(self.material.GetMaterial())
        weightcs,weightss=self.WeightCal()
        self.mxb.SetWeight(weightcs,weightss)

    def QuantityChanged(self):
        vol,surf=self.VSCal()
        n=self.mxb.GetQuantity()
        self.tpvs.SetV(vol*n)
        self.tpvs.SetS(surf*n)
        
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

    def WeightCal(self): #得到的是单重
        jicengmidu,jicengtype = self.material.GetBaseDensityType()
        fucengmidu,fucengtype = self.material.GetCladDensityType()
        data=self.image.GetData()
        jicengvol = self.control.GetJicengVol(data)
        fucengvol = self.control.GetFucengVol(data)
        weightjiceng = jicengvol*jicengmidu/1000000
        weightfuceng = fucengvol*fucengmidu/1000000
        weightcs=0
        weightss=0
        if jicengtype == 'CS':
            weightcs+= weightjiceng
        else:
            weightss+= weightjiceng
        if fucengtype == 'CS':
            weightcs+= weightfuceng
        else:
            weightss+= weightfuceng
        return weightcs,weightss
        
    def ImageChanged(self,ctrl_data):
        #将图片和控件进行组合成以下列表，交由Image类进行呈现
        #[[[图片,(0,0)]，[[控件组]，[控件组]]],[[[图片,(0,0)]，[[控件组]，[控件组]]]]
        data=self.image.GetData()
        self.image.SetImage(ctrl_data,scale=1)
        self.image.SetLuoji()
        self.image.SetData(data)

    def OnFocus(self, evt):
        self.Main.currentnode = self.currentnode
