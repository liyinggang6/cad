import wx
from Nestle import Nestle
from TPVS import TPVS
from Material import Material
from Weight import Weight
from MXB import MXB
from Comchoice import ControlForComponent

class Component(Nestle):
    def __init__(self,main):
        self.Main=main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                     pos=wx.DefaultPosition,
                     size=(700,425)
                     )
        self.frame.SetLabel('部件')
        panel = wx.Panel(self.frame)
        panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 2), size=(195, 110), style=wx.BORDER_THEME)
        panel2 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 117), size=(195, 200), style=wx.BORDER_THEME)
        panel3 = wx.Panel(panel, id=wx.ID_ANY, pos=(215, 2), size=(195, 182), style=wx.BORDER_THEME)
        panel4 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 327), size=(680, 55), style=wx.BORDER_THEME)
        panel5 = wx.Panel(panel, id=wx.ID_ANY, pos=(460,2), size=(220,260), style=wx.BORDER_THEME)
        self.cb81 = wx.Button(panel, label="确定&&关闭", pos=(614, 300), size=(68, 22))
        self.tpvs=TPVS(self,panel1)
        self.material=Material(self,panel2)
        self.weight=Weight(self,panel3)
        self.mxb=MXB(self,panel4)
        self.mxb.cb48.SetEditable(False)
        #self.mxb.cb48.Enable(False)
        #self.mxb.cb48.SetWindowStyleFlag(wx.TE_CENTER|wx.TE_READONLY)
        self.control=ControlForComponent(self,panel5)
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
        
    def SetData(self,data):
        self.SetLableData(data[0])  #前面也加一句设置self.nestle_english_name
        self.tpvs.SetData(data[1])
        self.material.SetData(data[2])
        self.control.SetData(data[3])
        self.mxb.SetData(data[4])
        self.mxb.OnTextCtrl46d(True)
        self.mxb.location.SetData(data[6])
        self.mxb.location.OnClose(True)
        self.weight.SetData(data[7])
        self.SetLableData(data[0])  #这句话需要放在最后
    
    def GetData(self):
        list1 = self.GetLableData()
        return [list1,
                self.tpvs.GetData(),
                self.material.GetData(),
                self.control.GetData(),
                self.mxb.GetData(),
                [],
                self.mxb.location.GetData(),
                self.weight.GetData()]

    def GetFatherTemp(self):
        parent = self.Main.tree.GetItemParent(self.currentnode)
        parent_class = self.Main.tree.GetItemData(parent)
        temp=parent_class.tpvs.GetT()
        return temp

    def GetFatherPre(self):
        parent = self.Main.tree.GetItemParent(self.currentnode)
        parent_class = self.Main.tree.GetItemData(parent)
        pre=parent_class.tpvs.GetP()
        return pre

    def GetFatherBaseMat(self):
        parent = self.Main.tree.GetItemParent(self.currentnode)
        parent_class = self.Main.tree.GetItemData(parent)
        material=parent_class.material.GetBaseMaterial()
        return material

    def GetFatherCladMat(self):
        parent = self.Main.tree.GetItemParent(self.currentnode)
        parent_class = self.Main.tree.GetItemData(parent)
        smaterial=parent_class.material.GetCladMaterial()
        return smaterial
    
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
        weightcs,weightss=self.WeightCal()
        self.weight.SetWeightSS(weightss)
        self.weight.SetWeightCS(weightcs)
        weightcs=self.weight.GetWeightCS()
        weightss=self.weight.GetWeightSS()
        self.mxb.SetWeight(weightcs,weightss)
        
    def SlideScChanged(self):
        weightcs=self.weight.GetWeightCS()
        weightss=self.weight.GetWeightSS()
        self.mxb.SetWeight(weightcs,weightss)
    
    def VSCal(self): ##计算时增加刷新tpvs、meterial继承数据 2022.12.19
        item=self.Main.tree.GetFirstChild(self.currentnode)[0]
        vol=0
        surf=0
        while item.IsOk():
            b=self.Main.tree.GetItemData(item)
            b.tpvs.OnCheckBox11(True)
            b.tpvs.OnCheckBox12(True)
            b.material.OnCheckBox21(True)
            b.material.OnCheckBox23(True)
            b.material.OnCheckBox24(True)
            vol1,surf1=b.VSCal()
            n=b.mxb.GetQuantity()
            b.tpvs.SetV(vol1*n)
            b.tpvs.SetS(surf1*n)
            vol1=b.tpvs.GetV()
            surf1=b.tpvs.GetS()
            vol+=vol1
            surf+=surf1
            item=self.Main.tree.GetNextSibling(item)
        return vol,surf

    def WeightCal(self):   
        item=self.Main.tree.GetFirstChild(self.currentnode)[0]
        weightcs=0
        weightss=0 
        while item.IsOk():
            b=self.Main.tree.GetItemData(item)
            #不直接计算重量，读取mxb中的重量，这样用户可以修改零件重量
            if b.nestle_english_name in ['Component']:
                weightcs1,weightss1=b.WeightCal()
                b.weight.SetWeightSS(weightss1)
                b.weight.SetWeightCS(weightcs1)
            weightcs1, weightss1=b.mxb.GetWeights()
            weightcs+=weightcs1
            weightss+=weightss1
            item=self.Main.tree.GetNextSibling(item)
        return weightcs,weightss

    def OnFocus(self, evt):
        self.Main.currentnode = self.currentnode
        self.VSChanged()
    
        
if __name__ == '__main__':
    app = wx.App()
    mainapp=Component(None)
    mainapp.frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
