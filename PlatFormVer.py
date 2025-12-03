import wx
#from softwareEvaluation import soft_evaluation
from pyautocad import Autocad, APoint
from PlatFormAll import PlatFormAll
from Calculate import Calculate
from DrawPlat import DrawPlat
import os
from math import pi,sin,cos,tan,asin,acos,atan,dist
from math import degrees as rad2deg
from math import radians as deg2rad

class PlatFormVer(PlatFormAll):
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                                      id=wx.ID_ANY,
                                      title='塔平台',
                                      pos=wx.DefaultPosition,
                                      size=(580, 375),
                                      style=wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self.frame)
        self.frame.Bind(wx.EVT_CLOSE, self.OnClose)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb11 = wx.StaticText(self.panel, label="托架标准夹角：", pos=(15, 5), style=wx.TE_RIGHT)
        self.cb12 = wx.StaticText(self.panel, label="    塔体外径：", pos=(15, 30), style=wx.TE_RIGHT)
        self.cb13 = wx.StaticText(self.panel, label="  是否有保温：", pos=(15, 55), style=wx.TE_RIGHT)
        self.cb14 = wx.StaticText(self.panel, label="    平台标高：", pos=(15, 80), style=wx.TE_RIGHT)
        self.cb15 = wx.StaticText(self.panel, label="    平台宽度：", pos=(15, 105), style=wx.TE_RIGHT)
        self.cb16 = wx.StaticText(self.panel, label="    载荷等级：", pos=(15, 130), style=wx.TE_RIGHT)
        self.cb17 = wx.StaticText(self.panel, label="    托架型式：", pos=(15, 155), style=wx.TE_RIGHT)
        self.cb18 = wx.StaticText(self.panel, label="  内延伸长度：", pos=(15, 180), style=wx.TE_RIGHT)
        self.cb19 = wx.StaticText(self.panel, label="顶平台支耳距设备中心线：L1=", pos=(5, 205), style=wx.TE_RIGHT)
        self.cb20 = wx.StaticText(self.panel, label="    梯子方位：°", pos=(40, 230), style=wx.TE_RIGHT)
        self.cb21 = wx.StaticText(self.panel, label="平台起始/终止角：°", pos=(15, 255), style=wx.TE_RIGHT)
        t1 = []
        for i in self.DNO:
            t1.append(i[0] + '  ' + i[1] + '°')
        self.cb31 = wx.ComboBox(self.panel, pos=(100, 5), size=(160, 22), choices=t1,
                                style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.cb32 = wx.ComboBox(self.panel, pos=(100, 30), size=(160, 22),
                                choices=[],
                                style=wx.CB_DROPDOWN)
        self.cb33 = wx.CheckBox(self.panel, label='保温厚度≤90mm时不勾选', pos=(100, 55), style=1)
        self.cb34 = wx.ComboBox(self.panel, pos=(100, 80), size=(160, 22),
                                choices=['5000', '10000', '15000', '20000', '25000', '30000', '40000', '50000'],
                                style=wx.CB_DROPDOWN)
        self.cb35 = wx.ComboBox(self.panel, pos=(100, 105), size=(160, 22), choices=[],
                                style=wx.CB_DROPDOWN)  #平台宽度
        self.cb36 = wx.ComboBox(self.panel, pos=(100, 130), size=(160, 22), choices=[],
                                style=wx.CB_DROPDOWN)
        self.cb37 = wx.ComboBox(self.panel, pos=(100, 155), size=(160, 22), choices=[],
                                style=wx.CB_DROPDOWN)
        self.cb38 = wx.ComboBox(self.panel, pos=(100, 180), size=(160, 22), choices=self.Nschang,
                                style=wx.CB_DROPDOWN)
        self.cb39 = wx.ComboBox(self.panel, pos=(175, 205), size=(85, 22),
                                choices=['500', '600', '700', '800', '900', '1000', '1200', '1400', '1500', '1600',
                                         '1800'],
                                style=wx.CB_DROPDOWN)
        self.cb40 = wx.ComboBox(self.panel, pos=(140, 230), size=(120, 22), choices=self.cta, style=wx.CB_DROPDOWN)
        self.cb41 = wx.ComboBox(self.panel, pos=(140, 255), size=(60, 22), choices=self.cta, style=wx.CB_DROPDOWN)
        self.cb42 = wx.ComboBox(self.panel, pos=(200, 255), size=(60, 22), choices=self.cta, style=wx.CB_DROPDOWN)

        self.cb811 = wx.Button(self.panel, label="立面图->", pos=(5, 280), size=(60, 22))
        self.cb812 = wx.Button(self.panel, label="平面图->", pos=(70, 280), size=(60, 22))
        self.cb813 = wx.Button(self.panel, label="托架表->", pos=(135, 280), size=(60, 22))
        self.cb814 = wx.Button(self.panel, label="支耳表->", pos=(200, 280), size=(60, 22))
        self.cb81 = wx.Button(self.panel, label="确定&&关闭", pos=(470, 310), size=(80, 22))
        self.cb32.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCombobox32)
        self.cb34.Bind(wx.EVT_TEXT, self.OnCombobox34)
        self.cb35.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCombobox35)
        self.cb36.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCombobox36)
        self.cb37.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCombobox37x)
        self.cb37.Bind(wx.EVT_COMBOBOX, self.OnCombobox37)
        self.cb811.Bind(wx.EVT_BUTTON, self.OnButton811)
        self.cb812.Bind(wx.EVT_BUTTON, self.OnButton812)
        self.cb813.Bind(wx.EVT_BUTTON, self.OnButton813)
        self.cb814.Bind(wx.EVT_BUTTON, self.OnButton814)
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
        self.panel.Bind(wx.EVT_PAINT,self.OnPaint)
        self.cb40.Bind(wx.EVT_TEXT, self.OnPaint)
        self.cb41.Bind(wx.EVT_TEXT, self.OnPaint)
        self.cb42.Bind(wx.EVT_TEXT, self.OnPaint)
        self.dc = wx.ClientDC(self.panel)
        self.Main.tawaijing = ['2032', '2632']
        self.Main.Ptype = self.Ptype
        token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJleHAiOjE2Njk5MDA1MDUsInVzZXJuYW1lIjoi5byg\
5LiJIn0.Q6YFZVEte9syYnUNv_drVDyqvZdyCQ7iRAKwj_\
kYxYI2ac44369-d85d-4716-a33a-71e49831660c'
        type_name="22720_化工设备梯子平台绘图软件"
        try:
            evaluation=soft_evaluation.soft_evaluation(token,type_name,
                                                   '正在处理塔平台...')
        except:
            evaluation='未能提交塔平台后评价信息。'
        print(evaluation)
   
        
    def OnPaint(self,evt):
        alf1=self.cb41.GetValue()
        try:
            alf1=float(alf1)
        except:
            alf1=0
        alf2=self.cb42.GetValue()
        try:
            alf2=float(alf2)
        except:
            alf2=0
        alf3=self.cb40.GetValue()
        try:
            alf3=float(alf3)
        except:
            alf3=0
        if alf1 == alf2:
            alf1=alf3+15
            alf2=alf3-15
        x=420
        y=130
        r1=50
        r2=110
        r3=20
        alf1=deg2rad(alf1+270)
        alf2=deg2rad(alf2+270)
        alf1,alf2=alf2,alf1
        alf3=deg2rad(alf3+270)
        pen1=wx.Pen('RED',width=1,style=wx.DOT_DASH)
        pen2=wx.Pen('BLACK',width=2,style=wx.SOLID)
        self.dc.Clear()
        self.dc.SetPen(pen1)
        self.dc.DrawLine(x-r2-10,y,x+r2+10,y)
        self.dc.DrawLine(x,y-r2-10,x,y+r2+10)
        self.dc.DrawLine(x,y,
                    int(x+(r2+10)*cos(alf3)),int(y+(r2+10)*sin(alf3)))
        self.dc.SetPen(pen2)
        self.dc.DrawArc(int(x+r1*cos(alf1)),int(y+r1*sin(alf1)),
                   int(x+r1*cos(alf2)),int(y+r1*sin(alf2)),
                   x,y)
        self.dc.DrawArc(int(x+r2*cos(alf1)),int(y+r2*sin(alf1)),
                   int(x+r2*cos(alf2)),int(y+r2*sin(alf2)),
                   x,y)
        self.dc.DrawLine(int(x+r1*cos(alf1)),int(y+r1*sin(alf1)),
                    int(x+r2*cos(alf1)),int(y+r2*sin(alf1)))
        self.dc.DrawLine(int(x+r1*cos(alf2)),int(y+r1*sin(alf2)),
                    int(x+r2*cos(alf2)),int(y+r2*sin(alf2)))
        x=int(x+(r1+r2)*cos(alf3)/2)
        y=int(y+(r1+r2)*sin(alf3)/2)
        self.dc.DrawArc(int(x+r3*cos(alf3-10)),int(y+r3*sin(alf3-10)),
                   int(x+r3*cos(alf3+10)),int(y+r3*sin(alf3+10)),
                   x,y)   
              
    def OnCombobox32(self, evt):  # 打开下拉列表时 显示最近输入过的塔外径
        arr = self.ToCombox(self.Main.tawaijing)
        arrint = self.bubbleSort(arr)
        arr = []
        for i in arrint:
            arr.append(str(i))
        self.cb32.SetItems(arr)

    def OnCombobox34(self, evt):  # 打开下拉列表时 导航栏显示平台标高
        t1 = '塔平台-->' + ' EL' + self.cb34.GetValue()
        self.frame.SetLabel(t1)
        t2 = 'EL' + self.cb34.GetValue()
        self.Main.tree.SetItemText(self.currentnode, t2)

    def OnCombobox35(self, evt):  # 打开下拉列表时 平台宽度
        t1 = []
        for i in self.Ptype:
            if i[3] != None:
                t1.append(i[3])
        item35 = self.ToCombox(t1)
        self.cb35.SetItems(item35)
        self.cb37.SetValue('') #2024.5.10

    def OnCombobox36(self, evt):  # 打开下拉列表时 载荷等级
        v35 = self.cb35.GetValue()
        t1 = []
        for i in self.Ptype:
            if i[3] == v35:
                t1.append(i[4])
        item = self.ToCombox(t1)
        self.cb36.SetItems(item)

    def OnCombobox37x(self, evt):  # 托架型式
        v35 = self.cb35.GetValue()
        v36 = self.cb36.GetValue()
        t1 = []
        for i in self.Ptype:
            if i[3] == v35 and i[4] == v36:
                t1.append(i[0] + '  ' + i[1])

        item = self.ToCombox(t1)
        self.cb37.SetItems(item)

    def OnCombobox37(self, evt):  #选中托架型式后 关闭打开相关选项
        t = self.cb37.GetValue()
        if t == '塔顶托架  DTJ':
            self.cb38.Enable(True)
            self.cb18.Enable(True)
            self.cb39.Enable(True)
            self.cb19.Enable(True)
            self.cb41.SetValue('')
            self.cb42.SetValue('')
            self.cb41.Enable(False)
            self.cb21.Enable(False)
            self.cb42.Enable(False)
            self.ding = 1
        else:
            self.cb38.Enable(False)
            self.cb18.Enable(False)
            self.cb39.Enable(False)
            self.cb19.Enable(False)
            self.cb38.SetValue('')
            self.cb39.SetValue('')
            self.cb41.Enable(True)
            self.cb21.Enable(True)
            self.cb42.Enable(True)
            self.ding = 0

    def GetData(self):
        self.OnCombobox37(True)
        list1 = self.GetLableData()
        t = self.cb31.GetValue().split('  ')
        t1 = t[0]
        t2 = t[1][:-1]  # 删除末尾的°
        list2 = [t1, t2, self.cb32.GetValue(),
                 self.cb33.GetValue(), self.cb34.GetValue(),
                 self.cb35.GetValue(), self.cb36.GetValue(),
                 self.cb37.GetValue(), self.cb38.GetValue(),
                 self.cb39.GetValue(), self.cb40.GetValue(),
                 self.cb41.GetValue(), self.cb42.GetValue()]
        return [list1, list2, ]

    def SetData(self, data):
        self.cb31.SetValue(data[1][0] + '  ' + data[1][1] + '°')
        self.cb32.SetValue(data[1][2])
        self.cb33.SetValue(data[1][3])
        self.cb34.SetValue(data[1][4])
        self.cb35.SetValue(data[1][5])
        self.cb36.SetValue(data[1][6])
        self.cb37.SetValue(data[1][7])
        self.cb38.SetValue(data[1][8])
        self.cb39.SetValue(data[1][9])
        self.cb40.SetValue(data[1][10])
        self.cb41.SetValue(data[1][11])
        self.cb42.SetValue(data[1][12])
        self.OnCombobox37(True)
        self.SetLableData(data[0])

    def OnButton81(self, evt): #确认关闭
        self.NestleList = self.GetData()
        self.Main.tawaijing.append(self.cb32.GetValue())
        self.frame.Show(False)

    def OnButton811(self, evt):  # 绘制平面
        parent=self.Main.tree.GetItemParent(self.currentnode)
        parent_class=self.Main.tree.GetItemData(parent)
        if parent_class.OnButton31_38(True):
            self.sc=parent_class.sc
            draw = DrawPlat()
            acad, base, sc=draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
            draw.DrawVer(self.platdata, acad, base, sc)

    def OnButton812(self, evt):  # 绘制立面
        parent=self.Main.tree.GetItemParent(self.currentnode)
        parent_class=self.Main.tree.GetItemData(parent)
        if parent_class.OnButton31_38(True):
            self.sc=parent_class.sc
            draw = DrawPlat()
            acad, base, sc=draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
            draw.DrawHor(self.platdata, acad, base, sc)

    def OnButton813_814(self):  # 计算托架表
        parent=self.Main.tree.GetItemParent(self.currentnode)
        parent_class=self.Main.tree.GetItemData(parent)
        if parent_class.OnButton31_38(True):
            self.sc=parent_class.sc
            list1=self.GetData()
            zhierlist=Calculate().calzhierlist(list1[1],self.Ptype,self.platdata)
        return zhierlist
        
    def OnButton813(self, evt):  # 绘制托架表
        zhierlist=self.OnButton813_814()
        data=[]
        for i in zhierlist:
            del i[1]
            data.append(i)
        datahead=['型 号','标高 (mm)','角  度α(°)','L1 (mm)','L2 (mm)','备 注']
        draw = DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        draw.Drawbiao(data,datahead)

    def OnButton814(self, evt):  # 绘制支耳表
        zhierlist = self.OnButton813_814()
        data = []
        for i in zhierlist:
            del i[0]
            data.append(i)
        datahead = ['型 号', '标高 (mm)', '角  度α(°)', 'L1 (mm)', 'L2 (mm)', '备 注']
        draw = DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        draw.Drawbiao(data, datahead)

    def ToCombox(self, one_list):
        temp_list = []
        for one in one_list:
            if one not in temp_list:
                temp_list.append(one)
        return temp_list

    def bubbleSort(self, arr1):
        '''冒泡法排序'''
        arr = []
        for i in arr1:
            try:
                arr.append(int(i))
            except:
                pass
        for i in range(1, len(arr)):
            for j in range(0, len(arr) - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
