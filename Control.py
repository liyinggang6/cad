import wx
from abc import ABCMeta, abstractmethod
from ALLPartData import PartsData
from Image import ImageForNozzleFlange
# from Image import ImageForShell

class Interface(metaclass=ABCMeta):
    @abstractmethod
    def GetData(self):
        pass
    
    @abstractmethod
    def SetData(self,data):
        pass
        
class ControlForEquipment(Interface):
    def __init__(self,parent, panel):
        self.parent=parent
        self.allpart_data=PartsData()
        wx.StaticText(panel,label ='设备名称', pos =(10,5))
        self.cb71 = wx.ComboBox(panel,pos=(60,5),size = (130,22),
                                choices=[],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(panel,label ='设备位号', pos =(10,30))
        self.cb72 = wx.ComboBox(panel,pos=(60,30),size = (130,22),
                                choices=[],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(panel,label ='主项代号', pos =(10,55))
        self.cb73 = wx.ComboBox(panel,pos=(60,55),size = (130,22),
                                choices=[],
                                style=wx.CB_DROPDOWN)
        self.OnCombobox73(True)
        wx.StaticText(panel,label ='设备类型', pos =(10,80))
        list1=[]
        for i in self.allpart_data.equipment_list:
            list1.append(i[1])
        self.cb74 = wx.ComboBox(panel,pos=(60,80),size = (130,22),
                                choices=list1,
                                style=wx.CB_DROPDOWN)
        wx.StaticText(panel,label ='图纸类型', pos =(10,105))
        list2=[]
        for i in ['工程图','装配图']:
            for j in self.allpart_data.tukuang_list:
                list2.append(i+' '+j[0])
        self.cb75 = wx.ComboBox(panel,pos=(60,105),size = (130,22),
                                choices=list2,
                                style=wx.CB_DROPDOWN)
        wx.StaticText(panel,label ='总图比例', pos =(10,130))
        self.cb76 = wx.ComboBox(panel,pos=(60,130),size = (130,22),
                                choices=['1:5','1:10','1:15','1:20','1:30','2:1','5:1'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(panel,label ='图  号', pos =(10,155))
        self.cb77 = wx.ComboBox(panel,pos=(60,155),size = (130,22),
                                choices=[],
                                style=wx.CB_DROPDOWN)
#        print(data)
#       self.SetData(data)
        self.cb71.Bind(wx.EVT_TEXT,self.OnCombobox712)
        self.cb72.Bind(wx.EVT_TEXT,self.OnCombobox712)
        self.cb73.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox73)
        self.cb74.Bind(wx.EVT_COMBOBOX,self.OnCombobox74)
        

    def OnCombobox712(self, evt):
        t1=self.cb71.GetValue()+' '+self.cb72.GetValue()
        self.parent.frame.SetLabel(t1)
        self.parent.Main.tree.SetItemText(self.parent.currentnode, t1)
        
    def OnCombobox73(self,evt):
        project_info=self.parent.GetProjectInfo()
        a=project_info[3].split('\n')
        self.cb73.SetItems(self.allpart_data.ToCombox(a))
        
    def OnCombobox74(self,evt):
        #将图片和控件进行组合成以下列表，交由Image类进行呈现
        #[[[图片,(0,0)]，[[控件组]，[控件组]]],[[[图片,(0,0)]，[[控件组]，[控件组]]]]
        #(0,0)是图片定位坐标
        #self.allpart_data.equipment_design_data的一行数据格式如下：
        i=[[1,'常压容器', 'B-常压容器.dwg',   'B-常压容器.bmp',[1],(180,168)],
           [
             [((40,8),(40,8),1,['--','10','15','20','25']),
             ((40,16),(40,8),1,['--']),...
             ],
             [((40,80),(40,8),1,['3.0','2.0','1.5','1.0']),
              ((40,88),(40,8),1,['1.0/1.0','0.9/1.0','0.85/1.0','0.85/0.85']),...
             ]
             ]
           ]
#将图片和控件进行组合成以下列表，交由Image类进行呈现
#[[图片，[控件组，控件组]],[图片，[控件组，控件组]]]
        
        for i in self.allpart_data.equipment_design_data:
            if i[0][1]==self.cb74.GetValue():
                ctrl_data=[[[i[0][3],(0,0),(0,0)],i[1]],]
                self.parent.ImageChanged(ctrl_data)
                break

    def GetEquipmentDesignSheet(self):
        sheet = self.allpart_data.equipment_design_data[0]
        for i in self.allpart_data.equipment_design_data:
            if i[0][1]==self.cb74.GetValue():
                sheet=i
                break
        return sheet

    def GetData(self):
       return [self.cb71.GetValue(),
               self.cb72.GetValue(),
               self.cb73.GetValue(),
               self.cb74.GetValue(),
               self.cb75.GetValue(),
               self.cb76.GetValue(),
               self.cb77.GetValue(),
               ]
    
    def SetData(self,data):
        self.cb71.ChangeValue(data[0])
        self.cb72.ChangeValue(data[1])
        self.cb73.ChangeValue(data[2])
        self.cb74.ChangeValue(data[3])
        self.cb75.ChangeValue(data[4])
        self.cb76.ChangeValue(data[5])
        self.cb77.ChangeValue(data[6])
        self.OnCombobox74(True)

    def GetSc(self): #获取总图比例 float型
        b=self.cb76.GetValue()    #'1:20'
        try:
           b=b.split(":")
           sc=float(b[1])/float(b[0])           
        except:
           sc=1
        return sc

    def GetTukuangAndKeyPoint(self):
        #获取图框及关键点坐标 数据格式示例 ['a1v.DWG',((10,10),(584,816),(404,95))]
        a=self.cb75.GetValue().split(" ")    #"工程图 A1V"
        a1=a[0]  #工程图
        a2=a[1]  #A1V
        for i in self.allpart_data.tukuang_list:
            if a2==i[0]:
                a3=i[1]  #a1v.DWG
                a4=i[2]  #图框中关键点定位坐标
                break
            a3='a1v.DWG'  #a1v.DWG
            a4=((25,10),(831,584),(651,95))
        return [a3,a4]
        
    def GetTuType(self):
        #获取标题栏填写数据
        a=self.cb75.GetValue().split(" ")    #"工程图 A1V"
        a1=a[0]  #工程图 或 装配图
        a2=a[1]  #A1V
        a3=self.parent.GetProjectInfo()
        if a1=='装配图':
            b1=a3[0]+'-'+self.cb77.GetValue()+'-01'
            b2='装配图'
            b3='供 施 工'
        else:
            b1=a3[0]+'-48-'+self.cb77.GetValue()
            b2='工程图'
            b3='供 设 计'
#        数据内容：版次 说明 设备名称(位号) 图纸类型 项目名称 项目代号 主项名称代号 设计阶段 图号 比例
        return [
            ['0',(5,-27),4,0.7],  #版次
            [b3, (32,-27),4,0.7],  #说明
            [self.cb71.GetValue()+'('+self.cb72.GetValue()+')',(50,-66),6,0.7], #设备名称(位号)
            [b2,(50,-84),4,0.7],  #图纸类型
            [a3[1],(135,-48),4,0.7], #项目名称
            [a3[0],(170,-48),3,0.7], #项目代号
            [self.cb73.GetValue(),(156,-57),4,0.7], #主项名称代号
            [a3[2],(140,-66),4,0.7], #设计阶段
            [b1,(135,-74),4,0.7],
            [self.cb76.GetValue(),(120,-83),4,0.7]
                ]
     
    def GetSiteType(self): 
        #获取自然条件表及数据等
        #数据格式示例 ["B-自然条件表(除大型储罐).dwg",['450','350', '-28.6', '8(0.2g)','Ⅱ/第三组', 'C',]]
        a=self.parent.GetSiteInfo()
        if '储罐' in self.cb74.GetValue():
            b1= "B-自然条件表(大型储罐).dwg"
            b2=[a[0],a[1],a[3],a[4],a[5],a[6],]
        else:
            b1= "B-自然条件表(除大型储罐).dwg"
            b2=[a[0],a[1],a[2],a[4],a[5],a[6],]
        return [b1,b2]


class ControlForShell(Interface):
    def __init__(self,parent, panel):
        self.parent=parent
        self.allpart_data=PartsData()
        posx=5
        posy=5
        posz=25
        self.cb311=wx.StaticText(panel,label ="零件标准", pos =(posx,posy+0*posz))
        self.cb31=wx.ComboBox(panel,pos=(posx+50,posy+0*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb312=wx.StaticText(panel,label =" ", pos =(posx+185,posy+0*posz))
        self.cb321=wx.StaticText(panel,label ="零件类型", pos =(posx,posy+1*posz))
        self.cb32=wx.ComboBox(panel,pos=(posx+50,posy+1*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb322=wx.StaticText(panel,label =" ", pos =(posx+185,posy+1*posz))
        self.cb31.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox31)
        self.cb31.Bind(wx.EVT_COMBOBOX,self.OnCombobox31a)
        self.cb32.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox32)
        self.cb32.Bind(wx.EVT_COMBOBOX,self.OnCombobox32a)

    def OnCombobox31(self,evt):
       a=[]
       for i in self.allpart_data.shell_data:
            a.append(i[1])
       self.cb31.SetItems(self.allpart_data.ToCombox(a))
       self.cb32.SetValue("")


    def OnCombobox31a(self,evt):
       item1=self.cb31.GetValue()
       if item1 in ['无','',' ']:
            newstandard=''
       else:
            newstandard=item1
       self.parent.StandardChanged(newstandard)

       
    def OnCombobox32(self,evt):
       a=[]
       b1=self.cb31.GetValue()
       for i in self.allpart_data.shell_data:
           if (i[1] == b1 or b1 in self.allpart_data.Kong) :
               a.append(i[3])
       self.cb32.SetItems(self.allpart_data.ToCombox(a))

    def OnCombobox32a(self,evt):
        for i in self.allpart_data.shell_data:
            if i[3]==self.cb32.GetValue():
                ctrl_list=[]
                for j in range(11,18):
                    if i[j] not in self.allpart_data.Kong:
                        # print(i[j])
                        ctrl_list.append(eval(i[j]))
                    else:
                        ctrl_list.append('')
                ctrl_data=[[[i[4],(485,475),(0,0)],[ctrl_list,]],] 
                self.parent.ImageChanged(ctrl_data)
                break
        t1=self.cb32.GetValue() #取消了 '常用件->'+
        self.parent.frame.SetLabel(t1)
        self.parent.Main.tree.SetItemText(self.parent.currentnode, t1)
        self.parent.VSChanged()

    def SetData(self,data):
        self.cb31.ChangeValue(data[0])
        self.cb32.SetValue(data[1])
        self.OnCombobox32a(True)
        
    def GetData(self):
        return [self.cb31.GetValue(),
               self.cb32.GetValue()]

    def GetCtrl(self,data):
        for i in self.allpart_data.shell_data:
            if i[3] == self.cb32.GetValue():
                list1=[i[5],i[6],i[7],i[8],i[9],i[18],i[19]]
                #[0外表面积,1内容积,2基层体积,3复层体积,4名称,5绘图,6SP3D]
                break
        px={'px01':data[0],
            'px02':data[1],
            'px03':data[2],
            'px04':data[3],
            'px05':data[4],
            'px06':data[5],
            'px07':data[6],
            'pi':'3.14159265'}
#       print(list1)
        list2=[]
        for i in list1:
            t1=str(i)
            for k in px:
                if px[k] in self.allpart_data.Kong:
                    px[k]='0'
                t1=t1.replace(k,str(px[k]))
            list2.append(t1)
        print('list2=',list2)
        return list2

    def GetSurf(self,data):
        t1=self.GetCtrl(data)[0]
        t2=eval(t1)/1000000
        return t2

    def GetVol(self,data):
        t1=self.GetCtrl(data)[1]
        t2=eval(t1)/1000000000
        return t2

    def GetJicengVol(self,data):
        t1=self.GetCtrl(data)[2]
        t2=eval(t1)
        return t2
    
    def GetFucengVol(self,data):
        t1=self.GetCtrl(data)[3]
        t2=eval(t1)
        return t2

    def GetName(self,data):
        t2=self.GetCtrl(data)[4]
        return t2
    
    def GetDraw(self,data):
        t2=self.GetCtrl(data)[5]
        return t2

    def GetSP3D(self,data):
        t2=self.GetCtrl(data)[6]
        return t2
 
    def GetNote(self,data):
        return ''
    
class ControlForLiftingLug(ControlForShell):
    def __init__(self,parent, panel):
        self.parent=parent
        self.allpart_data=PartsData()
        posx=5
        posy=5
        posz=25
        self.cb311=wx.StaticText(panel,label ="吊耳标准", pos =(posx,posy+0*posz))
        self.cb31=wx.ComboBox(panel,pos=(posx+50,posy+0*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb312=wx.StaticText(panel,label =" ", pos =(posx+185,posy+0*posz))
        self.cb321=wx.StaticText(panel,label ="吊耳类型", pos =(posx,posy+1*posz))
        self.cb32=wx.ComboBox(panel,pos=(posx+50,posy+1*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb322=wx.StaticText(panel,label =" ", pos =(posx+185,posy+1*posz))
        self.cb331=wx.StaticText(panel,label ="公称吊重", pos =(posx,posy+2*posz))
        self.cb33=wx.ComboBox(panel,pos=(posx+50,posy+2*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb332=wx.StaticText(panel,label =" ", pos =(posx+185,posy+2*posz))
        self.cb341=wx.StaticText(panel,label ="垫板厚度", pos =(posx,posy+3*posz))
        self.cb34=wx.ComboBox(panel,pos=(posx+50,posy+3*posz),size = (130,22),
                              choices=['4','6','8','10','12','14','16','18','20'],
                              style=wx.CB_DROPDOWN)
        self.cb342=wx.StaticText(panel,label =" ", pos =(posx+185,posy+3*posz))
        self.cb31.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox31)
        self.cb31.Bind(wx.EVT_COMBOBOX,self.OnCombobox31a)
        self.cb32.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox32)
        self.cb33.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox33)
        self.cb33.Bind(wx.EVT_COMBOBOX,self.OnCombobox33a)
        self.cb34.Bind(wx.EVT_TEXT,self.OnCombobox34)

    def OnCombobox31(self,evt):
       a=[]
       for i in self.allpart_data.LiftingLugA:
            a.append(i[1])
       self.cb31.SetItems(self.allpart_data.ToCombox(a))
       self.cb32.SetValue("")
       self.cb33.SetValue("")
    
    def OnCombobox31a(self,evt):
       b1=self.cb31.GetValue()
       self.parent.StandardChanged(b1)
       
    def OnCombobox32(self,evt):
       a=[]
       b1=self.cb31.GetValue()
       for i in self.allpart_data.LiftingLugA:
           if (i[1] == b1) :
               a.append(i[2])
       self.cb32.SetItems(self.allpart_data.ToCombox(a))
       self.cb33.SetValue("")
    
    def OnCombobox33(self,evt):
       a=[]
       b1=self.cb31.GetValue()
       b2=self.cb32.GetValue()
       for i in self.allpart_data.LiftingLugA: 
           if i[1] == b1 and i[2] == b2:
               for j in self.allpart_data.LiftingLugB:
                   if j[0] == i[3]:
                       a.append(j[2]+"   "+str(j[3])+'t')
       self.cb33.SetItems(self.allpart_data.ToCombox(a))

    def OnCombobox33a(self,evt):
        b1 = self.cb31.GetValue()
        b2 = self.cb32.GetValue()
        b3 = self.cb33.GetValue()
        b30 = b3.split("   ")[0]
        for i in self.allpart_data.LiftingLugA: 
           if i[1] == b1 and i[2] == b2 and (i[3] in b3 or '04' in b2):
               pt5a = i
               self.pt5a = pt5a
               break
        b4 = self.cb34.GetValue() #临时存一下垫板厚度
        if b4 != '':
            self.dianbanhoudu = b4
        for i in self.allpart_data.LiftingLugB:
             pt5b = i
             self.pt5b = pt5b
             if i[2] == b30:
                  break
        if pt5b[0] in ['TPA','SP','APA','APB','04-71186','04-1485']: #无垫板的情况
            self.cb34.ChangeValue('')
            self.cb34.Enable(False)
        else:
            self.cb34.ChangeValue(self.dianbanhoudu) #有垫板的情况
            self.cb34.Enable(True)
        ctrl_list=[]
        for j in range(11,25):
            tem = pt5a[j]
            if tem not in self.allpart_data.Kong:
                ctrl_list.append(eval(tem))
            else:
                ctrl_list.append('')
        # print('cltr_list in LiftingLug is:', ctrl_list)
        ctrl_data = [
                [
                  [pt5a[4],(0,0),(0,0)],[ctrl_list,]
                ],
            ] 
        print('ctrl_data=',ctrl_data)
        self.parent.ImageChanged(ctrl_data)
        self.parent.image.SetData(pt5b[5:])
        self.parent.VSChanged()
        
    def OnCombobox34(self,evt):
        # self.parent.frame.SetLabel('吊耳')
        # self.parent.Main.tree.SetItemText(self.parent.currentnode, '吊耳')
        self.parent.VSChanged()
        
    def SetData(self,data):
        self.cb31.ChangeValue(data[0])
        self.cb32.ChangeValue(data[1])
        self.cb33.ChangeValue(data[2])  #用SetValue以便显示图像
        self.cb34.ChangeValue(data[3])
                 
    def GetData(self):
        return [self.cb31.GetValue(),
               self.cb32.GetValue(),
               self.cb33.GetValue(),
               self.cb34.GetValue()]
    
    def GetCtrl(self,data):   
        #print('data in GetCtrl is:',data)
        a = self.cb33.GetValue().split('-')[0]
        b = self.cb31.GetValue()
        c = self.cb34.GetValue()
        try:
            c1 = eval(c)
        except:
            c1 = 0
        for i in self.allpart_data.LiftingLugA:
            if (i[3] == a) or (i[3] == b):
                list1=[i[5],i[6],i[7],i[8],i[9],i[25],i[26]]
                #[0外表面积,1内容积,2基层体积,3复层体积,4名称,5绘图,6SP3D]
                break
        px={'px01':data[0],
            'px02':data[1],
            'px03':data[2],
            'px04':data[3],
            'px05':data[4],
            'px06':data[5],
            'px07':data[6],
            'px08':data[7],
            'px09':data[8],
            'px10':data[9],
            'px11':data[10],
            'px12':data[11],
            'px13':data[12],
            'px14':data[13],
            'px15':str(c1),  #垫板厚度
            'pi':'3.14159265',
            }
#       print(list1)
        list2=[]
        for i in list1:
            t1=str(i)
            for k in px:
                if px[k] in self.allpart_data.Kong:
                    px[k]='0'
                t1=t1.replace(k,str(px[k]))
            list2.append(t1)
        return list2

    def GetSurf(self,data):
        t1=self.GetCtrl(data)[0]
        t2=eval(t1)/1000000
        return t2

    def GetVol(self,data):
        t1=self.GetCtrl(data)[1]
        t2=eval(t1)/1000000000
        return t2

    def GetJicengVol(self,data):
        t1=self.GetCtrl(data)[2]
        t2=eval(t1)
        return t2
    
    def GetFucengVol(self,data):
        t1=self.GetCtrl(data)[3]
        t2=eval(t1)
        return t2

    def GetName(self,data):
        if self.pt5a[10] in self.allpart_data.Kong:
            tem1=''
        else:
            tem1=self.pt5a[10]
        tem2 = tem1 +  self.pt5b[2]
        tem1 = self.cb34.GetValue()
        if tem1 not in self.allpart_data.Kong:
            tem2 += ('-' + tem1)
        return tem2
    
    def GetDraw(self,data):
        t2=self.GetCtrl(data)[5]
        return t2

    def GetSP3D(self,data):
        t2=self.GetCtrl(data)[6]
        return t2
 
    def GetNote(self,data):
        return ''

class ControlForNozzleFlange(ControlForShell):
    def __init__(self,parent, panel):
        self.parent=parent
        self.allpart_data=PartsData()
        self.NozzleFlange=self.allpart_data.NozzleFlange
        self.NozzleFlange_size=self.allpart_data.NozzleFlange_size
        self.ctrl_data=[]
        posx=5
        posy=5
        posz=25
        self.cb311=wx.StaticText(panel,label ="法兰标准", pos =(posx,posy+0*posz))
        self.cb31=wx.ComboBox(panel,pos=(posx+50,posy+0*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb321=wx.StaticText(panel,label ="法兰类型", pos =(posx,posy+1*posz))
        self.cb32=wx.ComboBox(panel,pos=(posx+50,posy+1*posz),size = (60,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb331=wx.StaticText(panel,label ="系列", pos =(posx+115,posy+1*posz))
        self.cb33=wx.ComboBox(panel,pos=(posx+140,posy+1*posz),size = (40,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb341=wx.StaticText(panel,label ="压力等级", pos =(posx,posy+2*posz))
        self.cb34=wx.ComboBox(panel,pos=(posx+50,posy+2*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb351=wx.StaticText(panel,label ="密封面", pos =(posx,posy+3*posz))
        self.cb35=wx.ComboBox(panel,pos=(posx+50,posy+3*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb361=wx.StaticText(panel,label ="公称直径", pos =(posx,posy+4*posz))
        self.cb36=wx.ComboBox(panel,pos=(posx+50,posy+4*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)
        self.cb371=wx.StaticText(panel,label ="配对接管", pos =(posx,posy+5*posz))
        self.cb37=wx.ComboBox(panel,pos=(posx+50,posy+5*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN)

        self.cb31.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox31)
        self.cb31.Bind(wx.EVT_COMBOBOX,self.OnCombobox)
        self.cb32.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox32) 
        self.cb32.Bind(wx.EVT_COMBOBOX,self.OnCombobox32a)
        # self.cb33.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox33)
        self.cb33.Bind(wx.EVT_COMBOBOX,self.OnCombobox)
        self.cb34.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox34)
        self.cb34.Bind(wx.EVT_COMBOBOX,self.OnCombobox)
        self.cb35.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox35)
        self.cb35.Bind(wx.EVT_COMBOBOX,self.OnCombobox)
        self.cb36.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox36)
        self.cb36.Bind(wx.EVT_COMBOBOX,self.OnCombobox)
        self.cb37.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox37)
        self.cb37.Bind(wx.EVT_COMBOBOX,self.OnCombobox)    
        
    def PT3_SetData(self,data):
        self.cb31.SetValue(data[0])
        self.cb32.SetValue(data[1])
        self.cb33.SetValue(data[2])
        self.cb34.SetValue(data[3])
                 
    def PT3_GetData(self):
        return [self.cb31.GetValue(),
               self.cb32.GetValue(),
               self.cb33.GetValue(),
               self.cb34.GetValue()]
               
    def OnCombobox31(self,evt):
        a=[]
        for i in self.NozzleFlange:
            if i[0] not in self.allpart_data.Kong:
                a.append(i[0])
        self.cb31.SetItems(self.allpart_data.ToCombox(a))

    def OnCombobox32(self,evt):
        b0=self.cb31.GetValue()
        a=[]
        for i in self.NozzleFlange:
            if i[0]==b0 and i[1] not in self.allpart_data.Kong:
                a.append(i[1])
        self.cb32.SetItems(self.allpart_data.ToCombox(a))

    def OnCombobox32a(self,evt):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        a=[]
        for i in self.NozzleFlange_size:
            if i[0]+i[1]==b0+b1:
                a.append(i[2])
        b=self.allpart_data.ToCombox(a)
        if len(b) == 1:
            self.cb33.SetValue(b[0])
            self.cb33.Enable(False)
        else:
            self.cb33.Enable(True)
        b2=self.cb33.GetValue()
        self.cb33.SetItems(b)
        self.cb33.SetValue(b2)
        self.OnCombobox(True)

    def OnCombobox34(self,evt):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b2=self.cb33.GetValue()
        a=[]
        for i in self.NozzleFlange_size:
            if i[0]+i[1]+i[2]==b0+b1+b2 and i[3] not in self.allpart_data.Kong:
                a.append(i[3])
        b=self.allpart_data.ToCombox(a)
        c=[]
        for i in b:
            for j in self.allpart_data.NozzleFlange_class_pn:
                if i == j[1]:
                    if j[2] not in self.allpart_data.Kong:
                        t1='  '+j[2]
                    else:
                        t1=''
                    c.append(j[1]+t1)
        self.cb34.SetItems(c)

    def OnCombobox35(self,evt):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b2=self.cb33.GetValue()
        b3=self.cb34.GetValue().split("  ")[0]
        a=[]
        for i in self.NozzleFlange_size:
            if i[0]+i[1]+i[2]+i[3]==b0+b1+b2+b3 and i[4] not in self.allpart_data.Kong:
                a.append(i[4])
        self.cb35.SetItems(self.allpart_data.ToCombox(a))

    def OnCombobox36(self,evt):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b2=self.cb33.GetValue()
        b3=self.cb34.GetValue().split("  ")[0]
        b4=self.cb35.GetValue()
        a=[]
        for i in self.NozzleFlange_size:
            if i[0]+i[1]+i[2]+i[3]+i[4]==b0+b1+b2+b3+b4 and i[5] not in self.allpart_data.Kong:
                a.append(i[5])
        b=self.allpart_data.ToCombox(a)
        c=[]
        if b0 in ["HG/T 20592-2009",] and b2 in ['B',]:
            iaii='II系列'
        else:
            iaii='Ia系列'
        for i in b:
            for j in self.allpart_data.PipeN:
                if i == j[1] and iaii == j[0]:
                    if j[2] not in self.allpart_data.Kong:
                        t1='  '+j[2]
                    else:
                        t1=''
                    c.append(j[1]+t1)
        self.cb36.SetItems(c)
        self.cb37.SetValue('')

    def OnCombobox37(self,evt):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b2=self.cb33.GetValue()
        b5=self.cb36.GetValue().split("  ")[0]
        if b0 in ["HG/T 20592-2009",] and b2 in ['B',]:
            iaii='II系列'
        else:
            iaii='Ia系列'
        for i in self.allpart_data.PipeN:
            if iaii+b5 == i[0]+i[1]:
                do=i[3]
                nps=i[2]
                break
        c=[]
        for i in self.allpart_data.Pipe:
            if iaii+b5 == i[1]+i[2]:
                c.append(i[3]+'  '+do+'×'+i[4])
        self.cb37.SetItems(self.allpart_data.ToCombox(c))

    def OnCombobox(self,evt):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b2=self.cb33.GetValue()
        b3=self.cb34.GetValue().split("  ")[0]
        b4=self.cb35.GetValue()
        b5=self.cb36.GetValue().split("  ")[0]
        b6=self.cb37.GetValue().split("  ")[-1]
        ctrl_list1=[]
        for i in self.allpart_data.NozzleFlange:
            if b0+b1 == i[0]+i[1]:
                bmp1=i[3]
                for j in range(9,20):
                    if i[j] not in self.allpart_data.Kong:
                        # print(i[j])
                        ctrl_list1.append(eval(i[j]))
                    else:
                        ctrl_list1.append('')
        ctrl_list2=[]
        for i in self.allpart_data.NozzleFlange:
            if b0+b4 == i[0]+i[2]:
                bmp2=i[3]
                for j in range(9,20):
                    if i[j] not in self.allpart_data.Kong:
                        # print(i[j])
                        ctrl_list2.append(eval(i[j]))
                    else:
                        ctrl_list2.append('')
        ctrl_data=[]
        if ctrl_list1 != []:
            ctrl_data=[[[bmp1,(485,475),ctrl_list1[0],],[ctrl_list1[1:],]],]
        if ctrl_list2 != []:
            ctrl_data.append([[bmp2,(485,475),ctrl_list2[0],],[ctrl_list2[1:],]])
        if ctrl_data !=[] and ctrl_data !=self.ctrl_data:
            self.parent.ImageChanged(ctrl_data)
            self.ctrl_data=ctrl_data.copy()
        data1=['','','','','','','','','','',]
        data2=['','','','','','','','',]
        if b0 in ["HG/T 20592-2009",] and b2 in ['B',]:
            iaii='II系列'
        else:
            iaii='Ia系列'
        for i in self.allpart_data.PipeN:
            if iaii+b5 == i[0]+i[1]:
                do=i[3]
                nps=i[2]
                break 
        for i in self.allpart_data.NozzleFlange_size:
            if i[0]+i[1]+i[2]+i[3]+i[4]+i[5] == b0+b1+b2+b3+b4+b5:
                if b6 not in self.allpart_data.Kong:
                    thk=b6.split("×")[1]
                    neijing='%0.1f' % (float(do)-2*float(thk))
                else:
                    thk=''
                    neijing=''
                if b1 in ['WN']:
                    data1=[do,i[6],i[7],i[10]+'-φ'+i[8]+'配'+i[9],i[11],neijing,i[13],i[14],i[15],i[16]]
                else:
                    data1=[do,i[6],i[7],i[10]+'-φ'+i[8]+'配'+i[9],i[11],i[12],i[13],i[14],i[15],i[16]]
                break
        for i in self.allpart_data.NozzleFlange_mfm:
            if i[0]+i[1]+i[2]+i[3]  == b0+b3+b4+b5:  #示例'HG/T 20592-2009', 'PN25', 'FM', '200','',
                if b0 not in ['HG/T 20623-2009']: #只有RF分AB类型
                    data2=i[5:]
                    break
                elif i[4] == b2:
                        data2=i[5:]
                        break
        self.parent.image.SetData(data1+data2)
        self.parent.StandardChanged(b0)
        self.parent.VSChanged()
                    
    def SetData(self,data):
        self.cb31.ChangeValue(data[0])
        self.cb32.ChangeValue(data[1])
        self.cb33.ChangeValue(data[2])
        self.cb34.ChangeValue(data[3])
        self.cb35.ChangeValue(data[4])
        self.cb36.ChangeValue(data[5])
        self.cb37.ChangeValue(data[6])
        self.OnCombobox(True)
        
    def GetData(self):
        return [self.cb31.GetValue(),
                self.cb32.GetValue(),
                self.cb33.GetValue(),
                self.cb34.GetValue(),
                self.cb35.GetValue(),
                self.cb36.GetValue(),
                self.cb37.GetValue(),
                ]

    def GetCtrl(self,data):  #获取Main.xlsx文件中所述的值
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b4=self.cb35.GetValue()
        for i in self.allpart_data.NozzleFlange:
            if i[0]+i[1] == b0+b1:
                list1=[i[4],i[5],i[6],i[7],i[8],i[20],i[21]]
                #[0外表面积,1内容积,2基层体积,3复层体积,4名称,5绘图,6SP3D]
                break
        for i in self.allpart_data.NozzleFlange:
            if i[0]+i[2] == b0+b4:
                list2=[i[4],i[5],i[6],i[7],i[8],i[20],i[21]]
                #[0外表面积,1内容积,2基层体积,3复层体积,4名称,5绘图,6SP3D]
                break
        
        px={'px01':data[0],
            'px02':data[1],
            'px03':data[2],
            'px04':data[3],
            'px05':data[4],
            'px06':data[5],
            'px07':data[6],
            'px08':data[7],
            'px09':data[8],
            'px10':data[9],
            'px11':data[10],
            'px12':data[11],
            'px13':data[12],
            'px14':data[13],
            'px15':data[14],
            'px16':data[15],
            'px17':data[16],
            'px18':data[17],
            'px19':data[18],
            'px20':data[19],
            'pi':'3.14159265'}
#       print(list1)
        list3=[]
        for i in list1+list2:
            t1=str(i)
            for k in px:
                if px[k] in self.allpart_data.Kong:
                    px[k]='0'
                t1=t1.replace(k,str(px[k]))
            list3.append(t1)
        return list3  #返回的是啥呀

    def GetSurf(self,data):
        t1=self.GetCtrl(data)[0]+'+'+self.GetCtrl(data)[7]
        t2=eval(t1)/1000000
        return t2

    def GetVol(self,data):
        t1=self.GetCtrl(data)[1]+'+'+self.GetCtrl(data)[8]
        t2=eval(t1)/1000000000
        return t2

    def GetJicengVol(self,data):
        t1=self.GetCtrl(data)[2]+'+'+self.GetCtrl(data)[9]
        t2=eval(t1)
        return t2
    
    def GetFucengVol(self,data):
        t1=self.GetCtrl(data)[3]+'+'+self.GetCtrl(data)[10]
        t2=eval(t1)
        return t2

    def GetName(self,data):
        b0=self.cb31.GetValue()
        b1=self.cb32.GetValue()
        b2=self.cb33.GetValue()
        b3=self.cb34.GetValue().split("  ")[0]
        b4=self.cb35.GetValue()
        b5=self.cb36.GetValue().split("  ")[0]
        b6=self.cb37.GetValue().split("  ")[0]
        if b1.lower() in ['wn']:
            if 'm' in b6:
                b61="S="+b6
            elif 'ch' in b6:
                b61=b6
            else:
                b61=b6
        else:
            b61=''
        t2=self.GetCtrl(data)[4]+b1+" "+b2+" "+b3+"-DN"+b5+' '+b4+' '+b61
        return t2
    
    def GetDraw(self,data):
        t2=self.GetCtrl(data)[5]+'+'+self.GetCtrl(data)[12]
        return t2

    def GetSP3D(self,data):
        t2=self.GetCtrl(data)[6]+'+'+self.GetCtrl(data)[13]
        return t2
 
    def GetNote(self,data):
        return ''



class main:
    def __init__(self):
        self.allpart_data=PartsData()
        self.frame = wx.Frame(None, -1, '测试ControlForLiftingLug类',pos=(10, 10), size=(300, 400))
        self.frame.Center()
        panel = wx.Panel(self.frame)
        panel3 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 2), size=(195, 182), style=wx.BORDER_THEME)
        panel5 = wx.Panel(panel, id=wx.ID_ANY, pos=(200,2), size=(485,475), style=wx.BORDER_THEME) #style=wx.BORDER_SUNKEN)
#       panel5.SetBackgroundColour((255,255,255))
#       data=self.allpart_data.default_data[111][3]
        self.control=ControlForLiftingLug(self,panel3)
##        
##        i=self.allpart_data.equipment_design_data[2]
##        ctrl_data=[[[i[0][3],(0,0),(0,0)],i[1]],]
##        data=self.allpart_data.default_data[111][5]
        self.image=ImageForNozzleFlange(self,panel5)
        self.frame.Show()
        self.cb81 = wx.Button(panel, label="调试按钮", pos=(5, 260), size=(60, 22))
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)

    def GetProjectInfo(self):
        return ['25006', '面向未来的大项目', '详细设计','工艺装置1（001）\n工艺装置2（002）\n工艺装置3（003）',]

    def GetSiteInfo(self):
        return ['450','350', '-17.8','-28.6', '8(0.2g)','Ⅱ/第三组', 'C',]

    def ImageChanged(self,ctrl_data):
        #将图片和控件进行组合成以下列表，交由Image类进行呈现
        #[[[图片,(0,0)]，[[控件组]，[控件组]]],[[[图片,(0,0)]，[[控件组]，[控件组]]]]
        data=self.image.GetData()
        self.image.SetImage(ctrl_data)
        self.image.SetLuoji()
        self.image.SetData(data)

    def OnButton81(self,evt):
        print('ControlForEquipment.GetData=\n',self.control.GetData())
        print('ControlForEquipment.GetSc=\n',self.control.GetSc())
        print('ControlForEquipment.GetTukuangAndKeyPoint=\n',self.control.GetTukuangAndKeyPoint())
        print('ControlForEquipment.GetTuType=\n',self.control.GetTuType())
        print('ControlForEquipment.GetSiteType=\n',self.control.GetSiteType())

if __name__ == '__main__':
    app = wx.App()
    main()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()