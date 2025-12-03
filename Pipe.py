import wx
#from softwareEvaluation import soft_evaluation
from ALLPartData import PartsData
from Shell import Shell
from TPVS import TPVS
from Material import Material
from MXB import MXB
from Control import ControlForShell
from Image import ImageForShell
class ImageForPipe(ImageForShell):
     def SetLuoji(self):
        pass
class ControlForPipe(ControlForShell):
    def __init__(self,parent,panel):
        self.parent=parent
        self.allpart_data=PartsData()
        posx=5
        posy=5
        posz=25
        self.cb20=wx.StaticText(panel,label ="标   准", pos =(posx,posy+0*posz))
        self.cb30=wx.ComboBox(panel,pos=(posx+50,posy+0*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cb21=wx.StaticText(panel,label ="类   型", pos =(posx,posy+1*posz))
        self.cb31=wx.ComboBox(panel,pos=(posx+50,posy+1*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cb22=wx.StaticText(panel,label ="系   列", pos =(posx,posy+2*posz))
        self.cb32=wx.ComboBox(panel,pos=(posx+50,posy+2*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cb23=wx.StaticText(panel,label ="直  径 1", pos =(posx,posy+3*posz))
        self.cb33=wx.ComboBox(panel,pos=(posx+50,posy+3*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cb24=wx.StaticText(panel,label ="直  径 2", pos =(posx,posy+4*posz))
        self.cb34=wx.ComboBox(panel,pos=(posx+50,posy+4*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        wx.StaticText(panel,label ="壁  厚", pos =(posx,posy+5*posz))
        self.cb35=wx.ComboBox(panel,pos=(posx+50,posy+5*posz),size = (130,22),choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cb361 = wx.CheckBox(panel, label = '无缝', pos = (posx+60,posy+6*posz), style = 1)
        self.cb362 = wx.CheckBox(panel, label = '焊接', pos = (posx+120,posy+6*posz), style = 1)
        a=[]
        for i in self.allpart_data.PipeCTR:
            if i[0] not in a:
                a.append(i[0])
        self.cb30.SetItems(a)
        self.cb30.Bind(wx.EVT_COMBOBOX,self.OnCombobox3)
        self.cb31.Bind(wx.EVT_COMBOBOX,self.OnCombobox3)
        self.cb32.Bind(wx.EVT_COMBOBOX,self.OnCombobox3)
        self.cb33.Bind(wx.EVT_COMBOBOX,self.OnCombobox3)
        self.cb361.Bind(wx.EVT_CHECKBOX,self.OnCheck361)
        self.cb362.Bind(wx.EVT_CHECKBOX,self.OnCheck362)
        self.cb35.Bind(wx.EVT_COMBOBOX,self.OnCombobox35)

    def saixuan(self,cb1,cb2,xuanlist,index,cb3):
        #cb1选择完成后预测cb2的值,index为cb1值在xuanlist中的索引
        #返回根据cb1筛选后的列表
        #print('xuanlist[0] is:',xuanlist[0])
        b1=cb1.GetValue()
        b2=cb2.GetValue()
        a=[] #筛选后的列表
        c=[] #b2对应的可选列表
        for i in xuanlist:
            if i[index] == b1:
                a.append(i)
        for i in a:
            if i[index+1] not in c:
                c.append(i[index+1])        
        if len(c)==0:
            cb2.SetItems([''])
            cb2.SetValue('')
            cb2.Enable(False)
            cb3.Enable(False)  #SetForegroundColour(wx.Colour(128, 128, 128))  # 设置为灰色
        elif len(c)==1:
            cb2.SetItems([c[0]])
            cb2.SetValue(c[0])
            cb2.Enable(False)
            cb3.SetForegroundColour(wx.Colour(0, 0, 0))  # 设置为黑色
            if c[0] in self.allpart_data.Kong:
                cb3.Enable(False)  #SetForegroundColour(wx.Colour(128, 128, 128))  # 设置为灰色
        else:
            cb2.Enable(True)
            cb2.SetItems(c)
            cb3.Enable(True)  #SetForegroundColour(wx.Colour(0, 0, 0))  # 设置为黑色
            if b2 in c:
                cb2.SetValue(b2)
            else:
                cb2.SetValue(c[0])
        return a
    
    def Weld_or_not(self):
        #返回'焊接','无缝信息',''
        if self.cb361.GetValue():
            return '无缝'
        elif self.cb362.GetValue():
            return '焊接'
        else:
            return ''

    def OnCombobox3(self,evt):
        #print('a1=self.saixuan(self.cb30,self.cb31,self.allpart_data.PipeCTR,0) is called')
        a1=self.saixuan(self.cb30,self.cb31,self.allpart_data.PipeCTR,0,self.cb21)
        #print('a2=self.saixuan(self.cb31,self.cb32,a1,1) is called')
        a2=self.saixuan(self.cb31,self.cb32,a1,1,self.cb22)
        #print('a3=self.saixuan(self.cb32,self.cb33,a2,2) is called')
        a3=self.saixuan(self.cb32,self.cb33,a2,2,self.cb23)
        #print('a4=self.saixuan(self.cb33,self.cb34,a3,3) is called')
        a4=self.saixuan(self.cb33,self.cb34,a3,3,self.cb24)
        #print('a5=self.saixuan(self.cb34,self.cb35,a4,4) is called')
        b2=self.cb32.GetValue()  #保存系列信息
        b3=self.cb33.GetValue()  #保存直径1信息
        b4=self.cb34.GetValue()  #保存直径2信息
        b5=self.cb35.GetValue()  #保存壁厚信息
        c1=[]
        for i in self.allpart_data.Pipe:
            if i[1]==b2 and i[2]==b3:
                c1.append(i[3]+'  '+i[4])
        self.cb35.SetItems(c1)
        if b5 in c1: #如果壁厚信息在可选列表中，则设置默认值
            self.cb35.SetValue(b5)
        else:
            self.cb35.SetValue(c1[0])
        a5=[] 
        for i in a4:
            if i[6] not in a5:
               a5.append(i[6]) #无缝/焊接信息
        if len(a5)<=1:
            self.cb361.SetValue(False)
            self.cb362.SetValue(False)
            self.cb361.Enable(False)
            self.cb362.Enable(False)
        else:
            self.cb361.Enable(True)
            self.cb362.Enable(True)
            self.cb361.SetValue(True)
        self.listdata=a4 #保存main管件数据筛选后的列表
        self.b4=b4 #保存直径2信息
        self.b6=self.Weld_or_not() #保存是否无缝信息
        self.OnCombobox35(True) 

    def OnCombobox35(self,evt):
        self.Do1=''
        self.Do2=''
        b2=self.cb32.GetValue()  #保存系列信息
        b3=self.cb33.GetValue()  #保存直径1信息
        b4=self.cb34.GetValue()  #保存直径2信息
        b5=self.cb35.GetValue()  #保存壁厚信息
        self.bihou=b5.split('  ')[1]   #颈部壁厚
        self.bihousch=b5.split('  ')[0]   #颈部壁厚sch或mm
        for i in self.allpart_data.PipeN:
            if i[0]==b2 and i[1]==b3:
                self.Do1=i[3]
            if i[0]==b2 and i[1]==b4:
                self.Do2=i[3]
        self.Oneline(True)


    def OnCheck361(self,evt): 
        if self.cb361.GetValue():
            self.cb362.SetValue(False)
        else:
            self.cb362.SetValue(True)
        # self.b6=self.Weld_or_not() #保存是否无缝信息
        # self.Oneline(True)

    def OnCheck362(self,evt):
        if self.cb362.GetValue():
            self.cb361.SetValue(False)
        else:
            self.cb361.SetValue(True)
        # self.b6=self.Weld_or_not() #保存是否无缝信息
        # self.Oneline(True)

    def Oneline(self,evt):
        '''将尺寸数据库定位到一行数据上'''
        if len(self.listdata)==1:
            self.pipesizedata=self.listdata[0]
        else:
            for i in self.listdata:
                if i[4]==self.b4:  #直径2信息匹配
                    if i[6]==self.b6:  #无缝/焊接信息匹配
                        self.pipesizedata=i
                        break
                self.pipesizedata=i
        '''将主控数据定位到一行上'''
        self.pipemaindata=self.allpart_data.PipeMain[0]
        for i in self.allpart_data.PipeMain:
            if self.pipesizedata[0] in i[0] and (self.pipesizedata[1] in i[1] or self.pipesizedata[1] in self.allpart_data.Kong):
                self.pipemaindata=i
                break
        print("self.pipemaindata=",self.pipemaindata)
        print("self.pipesizedata=",self.pipesizedata)
        ctrl_list=[]
        for j in range(9,14):
            tem = self.pipemaindata[j]
            if tem not in self.allpart_data.Kong:
                ctrl_list.append(eval(tem))
            else:
                ctrl_list.append('')
        ctrl_data = [
                [
                  [self.pipemaindata[2],(0,0),(0,0)],[ctrl_list,]
                ],
            ] 
        b0=self.cb30.GetValue()
        self.parent.StandardChanged(b0)
        print('ctrl_data in Pipe is:', ctrl_data)
        self.parent.ImageChanged(ctrl_data)
        self.parent.image.SetData([self.Do1,self.bihou,self.Do2]+self.pipesizedata[7:])
        self.parent.VSChanged()

    def SetData(self,data):
        self.cb30.ChangeValue(data[0])
        self.cb31.ChangeValue(data[1])
        self.cb32.ChangeValue(data[2])
        self.cb33.ChangeValue(data[3])
        self.cb34.ChangeValue(data[4])
        self.cb35.ChangeValue(data[5])
        self.cb361.SetValue(data[6])
        self.cb362.SetValue(data[7])
        
    def GetData(self):
        return [self.cb30.GetValue(),
                self.cb31.GetValue(),
                self.cb32.GetValue(),
                self.cb33.GetValue(),
                self.cb34.GetValue(),
                self.cb35.GetValue(),
                self.cb361.GetValue(),
                self.cb362.GetValue()]

    def GetCtrl(self,data): #
        i=self.pipemaindata
        list1=[i[3],i[4],i[5],i[6],i[7],i[8]]
                #[0外表面积,1内容积,2基层体积,3复层体积,4明细栏,5名称]
        px={'px01':data[0],
            'px02':data[1],
            'px03':data[2],
            'px04':data[3],
            'px05':data[4],
            'pi':'3.14159265'}  
        list2=[]
        for i in list1:
            t1=str(i)
            for k in px:
                if px[k] in self.allpart_data.Kong:
                    px[k]='0'
                t1=t1.replace(k,str(px[k]))
            list2.append(t1)
        #print('list2=',list2)
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
        # print('cltr_list in Pipe is:', ctrl_list)
        # ['HG/T 20553-2011','04-1484','04-70995','GB/T 12459-2017']
        b0 = self.pipesizedata[0] #标准
        b1 = self.pipesizedata[1] #类型
        b2 = self.pipesizedata[2] #系列
        b3 = self.pipesizedata[3] #直径1
        b4 = self.pipesizedata[4] #直径2
        b51 = self.bihou #壁厚
        b52 = self.bihousch #壁厚单位
        b6 = self.pipesizedata[6] #无缝/焊接
        #self.parent.image.SetData([self.Do1,self.bihou,self.Do2]+self.pipesizedata[7:])
        if 'Sch' in b52:
            tem1=b52
        else:
            tem1='S='+b51
        if b0 == 'HG/T 20553-2011':
            tem2 = '接管 Φ'+self.Do1+'×'+b51
        elif b0 in ['04-1484','04-70995']:
            tem2 ='t'+data[4]+'补强管'+' DN'+b3+b2.replace('型','')
            if data[6]:
                tem2 += (' S='+data[5])
        elif b0 == 'GB/T 12459-2017':
            if b4:
                tem3='×'+b4
            else:
                tem3=''
            if b6:
                tem4 = ' W'
            else:
                tem4 = ''
            tem2=b1+' DN'+b3+tem3+' '+tem1+tem4
        else:
            tem2='未知管件'
        return tem2
    
    def GetDraw(self,data):
        t2=self.GetCtrl(data)[5]
        return t2

    def GetSP3D(self,data):
        pass
 
    def GetNote(self,data):
        return ''
class Pipe(Shell):
    allpart_data=PartsData()
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                     pos=wx.DefaultPosition,
                     size=(702,605)
                     )
        self.frame.SetLabel('管子&管件')
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
#        panel1.Disable()
        self.material=Material(self,panel2)
        self.control=ControlForPipe(self,panel3)
        self.mxb=MXB(self,panel4)
        self.image = ImageForPipe(self,panel5)
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


    def SetData(self,data):
        pass
        '''
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
        '''

    def VSChanged(self):
        self.QuantityChanged()
        data=self.image.GetData()
        name=self.control.GetName(data)
        self.mxb.SetName(name)
        weightcs,weightss=self.WeightCal()
        self.mxb.SetWeight(weightcs,weightss)

    def VSCal(self):
        data=self.image.GetData()
        print('image.GetData() in Pipe is:',data)
        vol=self.control.GetVol(data)
        surf=self.control.GetSurf(data)
        return vol,surf
    

       
        
        
    
