import wx
from math import pi,sin,cos,tan,asin,acos,atan,dist
from math import degrees as rad2deg
from math import radians as deg2rad

class Location():
    def __init__(self,parent,Num):        
        self.parent=parent
        self.frame = wx.Dialog(parent.parent.frame,
                        id=wx.ID_ANY,
                        title='编辑零部件的位置',
                        pos=wx.DefaultPosition,
                        size=(720,590),
                        style=wx.CAPTION|wx.CLOSE_BOX)
        self.panel=wx.Panel(self.frame)
        if Num > 10:
            Num =10
        if Num <1:
            Num=1
        text=wx.TextCtrl(self.panel,-1,
                          '说明： 1. 坐标输入时支持运算符，+加 -减 *乘 /除 **幂 ()括号 以及备注中的函数。软件会将表达式计算出来。\n',
                          pos =(0,0),
                          size=(640, 40),
                          style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL)
        text.SetBackgroundColour((225,225,225)) 
        text.AppendText('          2. 例如坐标输入： 1000+2*500,100*2**(1/2),5*sin(deg2rad(45)) 是有效的。')
        wx.StaticText(self.panel,label ="序", pos =(5,50),size = (20,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="号", pos =(5,70),size = (20,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="上级部件", pos =(25,50),size = (50,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="基准点", pos =(25,70),size = (50,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="上一个零件", pos =(75,50),size = (60,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="基准点", pos =(75,70),size = (60,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="本零件基准点(红点)", pos =(155,50),size = (150,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="相对坐标", pos =(155,70),size = (150,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="导向点相对于红点", pos =(330,50),size = (150,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="相对坐标", pos =(355,70),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="建模?", pos =(450,70),size = (50,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="本零件基准点(红点)", pos =(480,50),size = (120,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="总体坐标", pos =(490,70),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="导向点", pos =(600,50),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="相对坐标", pos =(600,70),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="管口", pos =(700,50),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="符号", pos =(700,70),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="管口", pos =(800,50),size = (100,20),style=wx.TE_CENTER)
        wx.StaticText(self.panel,label ="用途", pos =(800,70),size = (100,20),style=wx.TE_CENTER)        
        self.cb81 = wx.Button(self.panel, label="管口信息\n-->", pos=(640, 0), size=(60, 40))
        self.cb82 = wx.Button(self.panel, label="确认\n&&\n返回", pos=(640, 345), size=(60,60))
        self.cb81.Bind(wx.EVT_BUTTON,self.OnButton81)
        self.cb82.Bind(wx.EVT_BUTTON,self.OnClose)
        self.cb81key=True
        text=wx.TextCtrl(self.panel,-1,'',
                          pos =(0,345),
                          size=(640, 200),
                          style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NO_VSCROLL)

        t1=['备注：\n',
            ' 1. 最多可编辑10个零件位置。\n',
            ' 2. pi 数学常数 π = 3.141592...，精确到可用精度。\n',
            ' 3. rad2deg(x) 将角度 x 从弧度转换为度数。\n',
            ' 4. deg2rad(x) 将角度 x 从度数转换为弧度。\n',
            ' 5. sin(x) 返回 x 弧度的正弦值。\n',
            ' 6. cos(x) 返回 x 弧度的余弦值。\n',
            ' 7. tan(x) 返回 x 弧度的正切值。\n',
            ' 8. asin(x) 返回以弧度为单位的 x 的反正弦值。 结果范围在 -pi/2 到 pi/2 之间。\n',
            ' 9. acos(x) 返回以弧度为单位的 x 的反余弦值。 结果范围在 0 到 pi 之间。\n',
            '10. atan(x) 返回以弧度为单位的 x 的反正切值。 结果范围在 -pi/2 到 pi/2 之间。']     
        for i in t1:
            text.AppendText(i)
        text.SetBackgroundColour((225,225,225))
        self.key=[]
        y=95
        j=0
        for i in range(Num):
            #在此经历了痛苦，各种常规方法都不行，不得不另设计了一个Table类。
            self.key.append(Table(self,self.panel,y))
            wx.StaticText(self.panel,label =str(i+1), pos =(1,y),size = (30,20),style=wx.TE_CENTER)
            y+=25
            j+=1
        self.frame.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnButton81(self,evt):
        if self.cb81key:
            self.cb81key=False
            self.frame.SetSize(920,590)
            self.cb81.SetLabel("管口信息\n<--")
        else:
            self.cb81key=True
            self.frame.SetSize(720,590)
            self.cb81.SetLabel("管口信息\n-->")
        
    def OnClose(self,evt):
        self.parent.LocList=self.GetDataPre()
        self.parent.base=eval(self.key[0].cb5.GetValue())
        self.parent.rot=eval(self.key[0].cb6.GetValue())
        self.frame.Destroy()
        #print('self.parent.base=',self.parent.base)
        #print('self.parent.rot=',self.parent.rot)

    def GetDataPre(self):
        rest=[]
        for i in self.key:
            rest.append(i.GetData())
        return rest

    def GetData(self):
        return self.parent.LocList

    def SetData(self,data):
        k=0
        for i in self.key:
            try:
                i.SetData(data[k])
            except:
                pass
            k+=1
    
class Table():
    def __init__(self,parent,panel,y):
        self.parent=parent
        self.cb1=wx.CheckBox(panel, label = '', pos = (45,y))
        self.cb2=wx.CheckBox(panel, label = '', pos = (90,y))
        self.cb3=wx.TextCtrl(panel, value = '', pos =(120,y), size = (200,20),style=wx.TE_CENTER)
        self.cb4=wx.TextCtrl(panel, value = '', pos =(320,y), size = (140,20),style=wx.TE_CENTER)
        self.cb9=wx.CheckBox(panel, label = '', pos = (469,y)) #增加了一个建模选项
        self.cb5=wx.TextCtrl(panel, value = '', pos =(490,y), size = (110,20),style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb6=wx.TextCtrl(panel, value = '', pos =(600,y), size = (100,20),style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb7=wx.TextCtrl(panel, value = '', pos =(700,y), size = (100,20),style=wx.TE_CENTER)
        self.cb8=wx.TextCtrl(panel, value = '', pos =(800,y), size = (100,20),style=wx.TE_CENTER)
        self.cb1.SetValue(False)
        self.cb2.SetValue(True)
        self.cb9.SetValue(True)
        self.cb3.Bind(wx.EVT_TEXT,self.Oncb3)
        self.cb4.Bind(wx.EVT_TEXT,self.Oncb4)
        self.cb1.Bind(wx.EVT_CHECKBOX,self.Oncb1)
        self.cb2.Bind(wx.EVT_CHECKBOX,self.Oncb2)
        self.prebase,self.prerot,self.preHkey = self.parent.parent.GetPreBaseRotHkey()
        self.topbase,self.toprot,self.topHkey = self.parent.parent.GetTopBaseRotHkey()
        self.FreshData(self.prebase,self.prerot,self.preHkey)
            
    def FreshData(self,base,rot,Hkey):
        p=dist(rot,(0,0,0))
        if p != 0:
            rot=(rot[0]/p,rot[1]/p,rot[2]/p)
        base=(Hkey*rot[0],Hkey*rot[1],Hkey*rot[2])
        self.cb3.SetValue(str(base)[1:-1]) #去掉括号
        self.cb4.SetValue(str(rot)[1:-1])   

    def SetData(self,data):
        self.cb1.SetValue(data[0])
        self.cb2.SetValue(data[1])
        self.cb3.SetValue(data[2])
        self.cb4.SetValue(data[3])
        self.cb7.SetValue(data[4])
        self.cb8.SetValue(data[5])
        self.cb9.SetValue(data[6])
   
    def GetData(self):
        return [self.cb1.GetValue(),
                self.cb2.GetValue(),
                self.cb3.GetValue(),
                self.cb4.GetValue(),
                self.cb7.GetValue(),
                self.cb8.GetValue(),
                self.cb9.GetValue()
                ]
        
    def Oncb1(self,evt):
        self.OnCheckBox(self.cb1,self.cb2)
        self.Oncb3(True)

    def Oncb2(self,evt):
        self.OnCheckBox(self.cb2,self.cb1)       
        self.Oncb3(True)

    def Oncb3(self,evt):
        if self.cb2.GetValue():
            base,rot,Hkey = self.parent.parent.GetPreBaseRotHkey()
        else:
            base,rot,Hkey = self.parent.parent.GetTopBaseRotHkey()
        rest=[0,0,0]
        try:
            tem=eval(self.cb3.GetValue())
            for i in range(3):
                rest[i]=base[i]+tem[i]
        except:
            pass
        rest=tuple(rest)
        self.cb5.SetValue(str(rest))
        return rest

    def Oncb4(self,evt):
        tem=self.cb4.GetValue()
        try:
            rot=eval(tem)
            p=dist(rot,(0,0,0))
            rot=(round(rot[0]/p,2),round(rot[1]/p,2),round(rot[2]/p,2))
        except:
            rot=(0,0,0)
        self.cb6.SetValue(str(rot))
        return rot

    def OnCheckBox(self,a,b):
      if a.GetValue():
          b.SetValue(False)
      else:
          b.SetValue(True)


