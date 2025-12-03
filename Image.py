import wx
from ALLPartData import PartsData
import time
import subprocess
import pyautogui
     
class ImageForEquipment():
    # mage这个类比较特殊，需要ctrl_data这个数据在图像上放置控件
    #将图片和控件进行组合成以下列表，交由Image类进行呈现
    #ctrl_data数据格式
##     [         大小  位置
##       [[图片,(0,0),(0,0)]，[[控件组]，[控件组]]],
##       [[图片,(0,0),(0,0)]，[[控件组]，[控件组]]],
##      ]
## 示例如下：
##[
##    [
##        ['B-换热器.bmp', (0, 0), (0, 0)],
##        [
##            ['',
##             ((40, 8), (80, 8), 1, ['--', 'Ⅰ/D1',]),
##             '',
##             ((40, 16), (80, 8), 1, ['--', '10', '15', '20', '25']),
##             ((40, 32), (40, 8), 1, ['--']),
##            ]
##        ]
##    ]
##]
    def __init__(self, parent, panel):
        self.parent=parent
        self.panel=panel
        self.allpart_data=PartsData()
        self.vol=0
        self.surf=0
        self.cb51=[]
        
    def SetImage(self, ctrl_data, scale=2.58):
        self.ctrl_data=ctrl_data
        self.cb51=[]
        self.img=[]
        self.panel.DestroyChildren()
        size=ctrl_data[0][0][1]
        for i in ctrl_data:
#           print(i)
            image = i[0][0]
            image = wx.Image('img/'+image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            imagesize=image.GetSize()
            if size==(0,0):
                size=imagesize
            self.panel.SetSize(size)
            pos=i[0][2]
            img101=wx.StaticBitmap(self.panel, -1, image, pos)
            self.img.append(img101)
            j=i[1]
            for j1 in j:
              for k in j1:
                if k not in self.allpart_data.Kong:
#                   print('k=\n',k)
                    str1=((int(k[0][0]*scale),int(k[0][1]*scale)),
                          (int(k[1][0]*scale),int(k[1][1]*scale)),
                          k[2],k[3])
                    if str1[2]==1:
                        self.cb51.append(wx.ComboBox(img101,pos=str1[0],size =str1[1],
                                    choices=str1[3],
                                    style=wx.CB_DROPDOWN))
                    elif str1[2]==2:
                        self.cb51.append(wx.ComboBox(img101,pos=str1[0],size =str1[1],
                                    choices=str1[3],
                                    style=wx.CB_DROPDOWN|wx.CB_READONLY))
                    elif str1[2]==3:
                        self.cb51.append(wx.TextCtrl(img101,pos=str1[0],size =str1[1]))
                    elif str1[2]==4:
                        self.cb51.append(wx.TextCtrl(img101,pos=str1[0],size =str1[1],
                                    style=wx.TE_MULTILINE))
                    elif str1[2]==5:
                        self.cb51.append(wx.TextCtrl(img101,pos=str1[0],size =str1[1],
                                    style=wx.TE_READONLY))
                    elif str1[2]==6:
                        self.cb51.append(wx.CheckBox(img101, label = '在明细栏中显示？', pos=str1[0],size =str1[1],
                                                     style = 1))
                        
                    else:
                        self.cb51.append(None)
                else:
                        self.cb51.append(None)    

    def SetLuoji(self):
        list1=[231,21,27,209,210,14,148,51,52,160,161,150,152,153,154,165,181,85,86,22,23,25,26,216,
               218,107,106,108,221,222,224,225,226,227,228,230,81,82,83,84,255]
        list2=[]
        for i in list1:
            for j in self.allpart_data.Standard:
                if i==j[0]:
                    list2.append(j[1]+'《'+j[2]+'》')
        for i in range(39,47,1):
            if self.cb51[i] != None:
                self.cb51[i].SetItems(self.allpart_data.ToCombox(list2))
        if self.cb51[1] != None:
            t1=self.cb51[1].GetItems()
            t1.append("计算...")
            self.cb51[1].SetItems(t1)
            self.cb51[1].Bind(wx.EVT_COMBOBOX,self.OnCombobox511)
        if self.cb51[5] != None:
            self.cb51[5].Bind(wx.EVT_COMBOBOX_DROPDOWN,self.OnCombobox515)

        if self.cb51[9] != None:
            self.cb51[9].Bind(wx.EVT_COMBOBOX_DROPDOWN,
                              lambda evt: self.ItemsAdd(evt,
                              self.parent.tpvs.cb16.GetValue())
                             )
        if self.cb51[34] != None:
            self.cb51[34].Bind(wx.EVT_COMBOBOX_DROPDOWN,
                              lambda evt: self.ItemsAdd(evt,
                              str(self.parent.weight.GetWeight()))
                             )

    def ItemsAdd(self,evt,value): #给下拉列表增加一个推荐值
        obj=evt.GetEventObject()
        t1=obj.GetItems()
        if t1[0]=='--':
            t1.insert(0,value)
        elif t1[1]=='--':
            t1[0]=value
        else:
            t1.insert(0,'--')
            t1.insert(0,value)
        obj.SetItems(t1)
        
    def OnCombobox515(self,evt):           
        self.ItemsAdd(evt,self.parent.tpvs.cb17.GetValue())

    def OnCombobox511(self,evt):
        if self.cb51[1].GetValue() == "计算...":
            pyautogui.PAUSE = 0.1
            pyautogui.FAILSAFE = True
            subprocess.Popen('bin/压力容器划类软件(TSG21-2016) V5.2.exe')
            for i in range(10):
                time.sleep(0.1)
                coords = pyautogui.locateOnScreen('bin/压力容器划类软件界面win64.PNG')
                if coords:
                    break
            pyautogui.leftClick(coords[0]+13,coords[1]+12)
            pyautogui.leftClick(coords[0]+88,coords[1]+43)
            pyautogui.typewrite(self.parent.tpvs.cb17.GetValue())
            pyautogui.leftClick(coords[0]+88,coords[1]+73)
            pyautogui.typewrite(self.parent.tpvs.cb18.GetValue())
##            pyautogui.leftClick(coords[0]+88,coords[1]+106)
##            pyautogui.typewrite("2.5")
##            pyautogui.leftClick(coords[0]+88,coords[1]+135)
##            pyautogui.typewrite("80")
##            shot='screenshot2.png'
##            pyautogui.screenshot(shot, region=(coords[0]+72, coords[1]+212, 96, 17))
##            time.sleep(0.2)
            pyautogui.leftClick(coords[0]+72,coords[1]+263)
            evt.GetEventObject().SetValue('Ⅱ/D2')

##    def GetV(self):
##        return self.vol
##
##    def GetS(self):
##        return self.surf
    
    def GetData(self):
        list1=[]
        for i in self.cb51:
            if i == None:
                list1.append(None)
            else:
                list1.append(i.GetValue())
        return list1
    
    def SetData(self,data):
        key=0
        for i in self.cb51:
            if i != None:
                try:
                    i.ChangeValue(data[key])
                except:
                    i.ChangeValue('')
            key+=1

class ImageForShell(ImageForEquipment):
    DNo=['159','219','273','325','377','426']
    DNi=['300','350','400','450','500','550','600','650','700','800','850','900','950',
         '1000','1100','1200','1300','1400','1500','1600','1700','1800','1900',
         '2000','2100','2200','2300','2400','2500','2600','2700','2800','2900',
         '3000','3100','3200','3300','3400','3500','3600','3700','3800','3900',
         '4000','4100','4200','4300','4400','4500','4600','4700','4800','4900',
         '5000','5100','5200','5300','5400','5500','5600','5700','5800','5900',
         '5000']
    TN=['2','3','4','5','6','8','10','12','14','16','18','20','22','24','26','28',
        '30','32','36','40','42','45','48','50','52','55','58','60','65','70','75',
        '80','85','90','95','100']
    TNf=['2','2.5','3','3.5','4','5','6']
    LN1=['25','40','50']
    LN2=['100','200','300','400','500','600','700','800','900','1000','2000','3000','4000','5000','6000']
    ALF=['0','45','90','135','180','225','270','315']


    def SetLuoji(self):
        if self.ctrl_data[0][0][0] in ['img1208.bmp','img1209.bmp']:
            self.cb51[0].SetItems(self.DNo)
        else:
            self.cb51[0].SetItems(self.DNi)
        self.cb51[0].Bind(wx.EVT_TEXT,self.VSChanged)
        if self.cb51[1] != None:
            self.cb51[1].SetItems(self.DNi)
            self.cb51[1].Bind(wx.EVT_TEXT,self.VSChanged)
        if self.cb51[2] != None:
            self.cb51[2].SetItems(self.TN)
            self.cb51[2].Bind(wx.EVT_TEXT,self.OnComboBox512)
        if self.cb51[4] != None:
            self.cb51[4].SetItems(self.TNf)
            self.cb51[4].Bind(wx.EVT_TEXT,self.OnComboBox514)
        if self.cb51[6] != None:
            self.cb51[6].SetItems(self.LN2)
            self.cb51[6].Bind(wx.EVT_TEXT,self.VSChanged)
        if self.ctrl_data[0][0][0] in ['img1206.bmp','img1207.bmp','img1208.bmp','img1209.bmp',]:
            self.cb51[6].SetItems(self.LN1)
        if self.ctrl_data[0][0][0] in ['img1211.bmp']:
            t1=[]
            for i in self.allpart_data.Tube:
                t1.append(str(i[0]))
            self.cb51[1].SetItems(self.allpart_data.ToCombox(t1))
        if self.ctrl_data[0][0][0] in ['img1212.bmp']:
            t1=[]
            for i in self.allpart_data.Tube:
                t1.append(str(i[0]))
            self.cb51[0].SetItems(self.allpart_data.ToCombox(t1))
            self.cb51[2].Bind(wx.EVT_COMBOBOX_DROPDOWN,self.TubeThk)
        
    def TubeThk(self,evt):
        a=self.cb51[0].GetValue()
        t1=[]
        for i in self.allpart_data.Tube:
            if a == str(i[0]):
                t1.append(str(i[1]))
        self.cb51[2].SetItems(self.allpart_data.ToCombox(t1))
        
    def OnComboBox512(self,evt):
        if self.cb51[3] != None:
            temp=self.cb51[2].GetValue()
            try:
                a=float(temp)
            except:
                a=0
            a=0.88*a
            a=str('%.1f' % a)
            try:
                self.cb51[3].SetValue(a)
            except:
                self.cb51[3].SetValue('')
        self.VSChanged(True)

    def OnComboBox514(self,evt):
        if self.cb51[3] != None:
            temp=self.cb51[4].GetValue()
            try:
                a=float(temp)
            except:
                a=0
            a=0.88*a
            a=str('%.1f' % a)
            try:
                self.cb51[5].SetValue(a)
            except:
                self.cb51[5].SetValue('')
        self.VSChanged(True)

    def GetData(self):
        list1=[]
        for i in self.cb51:
            if i == None:
                list1.append('0')
            else:
                t1=i.GetValue()
                if t1 in self.allpart_data.Kong:
                    t1='0'
                list1.append(t1)
        return list1
    
    def VSChanged(self,evt):
        self.parent.VSChanged()

class ImageForNozzleFlange(ImageForShell):
    def SetLuoji(self):
        if self.cb51[4] != None:
            self.cb51[4].Bind(wx.EVT_TEXT,self.VSChanged)
        if self.cb51[5] != None:
            self.cb51[5].Bind(wx.EVT_TEXT,self.VSChanged1)
        if self.cb51[7] != None:
            self.cb51[7].Bind(wx.EVT_TEXT,self.VSChanged)
    def VSChanged(self,evt):
        self.parent.VSChanged()
        note='C='+self.cb51[4].GetValue()+',H='+self.cb51[7].GetValue()
        self.parent.NoteChanged(note)
        
    def VSChanged1(self,evt):
        self.parent.VSChanged()

class ImageForLiftingLug(ImageForShell):
    def SetLuoji(self):
        pass
    
    
