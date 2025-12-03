import wx
from ALLPartData import PartsData

class Material():
    def __init__(self,parent,panel):
        self.parent=parent
        self.allpart_data=PartsData()
        self.Material=self.allpart_data.Material
        self.SMaterial=self.allpart_data.SMaterial
        self.jicengmidu=7.85
        self.jicengtype='CS'
        self.fucengmidu=7.9
        self.fucengtype='SS'
##        for i in self.Material:
##            print(i)
##        for i in self.SMaterial:
##            print(i)    
        px=5
        py=5
        self.cb21 = wx.CheckBox(panel, label = '继承材料', pos = (px,py), style = 1)
        self.cb22 = wx.CheckBox(panel, label = '主体材料', pos = (px+110,py), style = 1)
        self.cb23 = wx.CheckBox(panel, label = '继承材料', pos = (px,py+115), style = 1)
        self.cb24 = wx.CheckBox(panel, label = '复层材料', pos = (px+110,py+115), style = 1)
        wx.StaticText(panel,label ='材料类型', pos =(px+5,py+25))
        wx.StaticText(panel,label ='材料标准', pos =(px+5,py+50))
        wx.StaticText(panel,label ='材料名称', pos =(px+5,py+75))
        wx.StaticText(panel,label ='复层类型', pos =(px+5,py+140))
        wx.StaticText(panel,label ='复层材料', pos =(px+5,py+165))
        self.cb25 = wx.ComboBox(panel,pos=(px+55,py+25),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb26 = wx.ComboBox(panel,pos=(px+55,py+50),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb27 = wx.ComboBox(panel,pos=(px+55,py+75),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb28 = wx.ComboBox(panel,pos=(px+55,py+140),size = (130,22),choices=[], style=wx.CB_DROPDOWN)                
        self.cb29 = wx.ComboBox(panel,pos=(px+55,py+165),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb21.Bind(wx.EVT_CHECKBOX,self.OnCheckBox21)
        self.cb23.Bind(wx.EVT_CHECKBOX,self.OnCheckBox23)
        self.cb24.Bind(wx.EVT_CHECKBOX,self.OnCheckBox24)
        self.cb25.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox25)
        self.cb26.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox26)
        self.cb27.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox27)
        self.cb27.Bind(wx.EVT_COMBOBOX,self.OnCombobox27a)        
        self.cb27.Bind(wx.EVT_TEXT,self.OnMfhc)
        self.cb28.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox28)
        self.cb29.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox29)
        self.cb29.Bind(wx.EVT_COMBOBOX,self.OnCombobox29a)  
        self.cb29.Bind(wx.EVT_TEXT,self.OnMfhc)
        self.cb28.Enable(False)
        self.cb29.Enable(False)
        
    def SetData(self,data):
        self.cb21.Enable(data[0])
        self.cb21.SetValue(data[1])
        self.cb22.Enable(data[2])
        self.cb22.SetValue(data[3])
        self.cb25.ChangeValue(data[4])
        self.cb26.ChangeValue(data[5])
        self.cb27.ChangeValue(data[6])
        self.jcmidu=data[7]
        if data[1]:
            self.cb25.Enable(False)
            self.cb26.Enable(False)
            self.cb27.Enable(False)
        else:
            self.cb25.Enable(True)
            self.cb26.Enable(True)
            self.cb27.Enable(True)          
        self.cb23.Enable(data[8])
        self.cb23.SetValue(data[9])
        self.cb24.Enable(data[10])
        self.cb24.SetValue(data[11])
        self.cb28.ChangeValue(data[12])
        self.cb29.ChangeValue(data[13])
        self.fcmidu=data[14]
        if data[8] or (not data[11]):
            self.cb28.Enable(False)
            self.cb29.Enable(False)
        else:
            self.cb29.Enable(True)
            self.cb24.Enable(True)

    def GetData(self):
        return [self.cb21.IsEnabled(),
               self.cb21.GetValue(),
               self.cb22.IsEnabled(),
               self.cb22.GetValue(),
               self.cb25.GetValue(),
               self.cb26.GetValue(),
               self.cb27.GetValue(),
               self.jicengmidu,
               self.cb23.IsEnabled(),
               self.cb23.GetValue(),
               self.cb24.IsEnabled(),
               self.cb24.GetValue(),
               self.cb28.GetValue(),
               self.cb29.GetValue(),
               self.fucengmidu]
        
    def OnMfhc(self,evt):
        #向明细栏中构造材料名称并写入
        self.parent.MaterialChanged()
        # wx.MessageBox(self.GetMaterial(), '出错', wx.OK)
        # print(self.GetMaterial())
 
    def OnCombobox25(self,evt):
       a=[]
       for i in self.Material:
            a.append(i[1])
       self.cb25.SetItems(self.allpart_data.ToCombox(a))
       self.cb26.SetValue("")
       self.cb27.SetValue("")

    def OnCombobox26(self,evt):
       a=[]
       b1=self.cb25.GetValue()
       for i in self.Material:
           if (i[1] == b1) or (b1 in self.allpart_data.Kong) :
               a.append(i[3])
       self.cb26.SetItems(self.allpart_data.ToCombox(a))
       self.cb27.SetValue("")

    def OnCombobox27(self,evt):
       a=[]
       b1=self.cb25.GetValue()
       b2=self.cb26.GetValue()
       for i in self.Material:
           if ((i[1] == b1) or (b1 in self.allpart_data.Kong)) and ((i[3] == b2) or (b2 in self.allpart_data.Kong)):
               a.append(i[4])
       self.cb27.SetItems(self.allpart_data.ToCombox(a))

    def OnCombobox27a(self,evt):
      #获取基层材料密度 获取基层材料类型
      item1=self.cb27.GetValue()
      for i in self.Material:
           if (i[4] == item1) :
               self.jicengmidu=i[5]
               self.jicengtype=i[6]
               break

    def OnCombobox28(self,evt):
       a=[]
       for i in self.SMaterial:
            a.append(i[1])
       self.cb28.SetItems(self.allpart_data.ToCombox(a))
       self.cb29.SetValue("")

    def OnCombobox29(self,evt):
       a=[]
       b1=self.cb28.GetValue()
       for i in self.SMaterial:
           if (i[1] == b1) :
               a.append(i[4])
       self.cb29.SetItems(self.allpart_data.ToCombox(a))
       
    def OnCombobox29a(self,event):
      #获取复合层材料密度 获取复层材料类型
      item1=self.cb29.GetValue()
      for i in self.SMaterial:
           if (i[4] == item1) :
               self.fucengmidu=i[5]
               self.fucengtype=i[6]
               break
      if item1 in self.allpart_data.Kong:
          self.fucengmidu=self.jicengmidu
          self.fucengtype=self.jicengtype
                   
    def OnCheckBox21(self,evt):      
      if self.cb21.GetValue():
         self.cb22.Enable(False)
         self.cb25.Enable(False)
         self.cb26.Enable(False)
         self.cb27.Enable(False)
         material=self.parent.GetFatherBaseMat()
         self.SetBaseMaterial(material)
      else:
         self.cb22.Enable(True)
         self.cb25.Enable(True)
         self.cb26.Enable(True)
         self.cb27.Enable(True)

    def OnCheckBox23(self,evt):
        if self.cb23.GetValue():
            self.cb24.Enable(False) 
            self.cb28.Enable(False)
            self.cb29.Enable(False)
            smaterial= self.parent.GetFatherCladMat()
            self.cb24.SetValue(True)
            self.SetCladMaterial(smaterial)
        else:
            self.cb24.Enable(True) 
            self.cb28.Enable(True)
            self.cb29.Enable(True)
        self.OnCombobox29a(True)
         
    def OnCheckBox24(self,evt): 
      if self.cb24.GetValue():
         self.cb28.Enable(True)
         self.cb29.Enable(True)
      else:
         self.cb28.Enable(False)
         self.cb29.Enable(False)
         self.cb28.SetValue("")
         self.cb29.SetValue("")
         
    def GetBaseMaterial(self):
        return [self.cb22.GetValue(),
               self.cb25.GetValue(),
               self.cb26.GetValue(),
               self.cb27.GetValue(),
               ]
    def SetBaseMaterial(self,material):
        self.cb22.SetValue(material[0]) #是否是主体材料
        self.cb25.SetValue(material[1])
        self.cb26.SetValue(material[2])
        self.cb27.SetValue(material[3])

    def GetCladMaterial(self):
        return [self.cb28.GetValue(),
               self.cb29.GetValue(),
               ]
    
    def SetCladMaterial(self,smaterial):
        # 给定一个覆层材料信息 格式： ['不锈钢复合','S11306']
        self.cb28.SetValue(smaterial[0])
        self.cb29.SetValue(smaterial[1])
        
    def GetMaterial(self):
        fhc={'不锈钢复合' : '+',
        '不锈钢堆焊': '堆',
        '镍及镍合金复合': '+',
        '钛及钛合金复合': '+',
        '铜及铜合金复合': '+',
        '衬环': '衬',
        '垫板': '/'}
         
        try:
            b=self.cb28.GetValue()
            a=fhc[b]
        except:
            a="/"
        if self.cb29.GetValue()=='':
            a=''
        return self.cb27.GetValue()+a+self.cb29.GetValue()
        
    def GetMainMaterial(self):
        if self.cb22.GetValue():
            main_material=self.cb27.GetValue()
        else:
            main_material=''
        return main_material
    
    def GetBaseDensityType(self):
        self.OnCombobox27a(True)
        return self.jicengmidu,self.jicengtype
    
    def GetCladDensityType(self):
        self.OnCombobox29a(True)
        return self.fucengmidu,self.fucengtype

    
if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, '测试Material',pos=(10, 10), size=(280, 500))
    frame.Center()
    panel = wx.Panel(frame)
    panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 117), size=(195, 200), style=wx.BORDER_THEME)
    data=[True, False, True, True, '板材', 'GB/T 713-2014', 'Q345R', 7.85, True, False, True, False, '', '', 7.9]
    pt2=Material(None,panel1)
    frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
