import wx
import os
import shutil
from ALLPartData import PartsData
from Nestle import Nestle
from TPVS import TPVS
from Material import Material
from Weight import Weight
from Control import ControlForEquipment
from Image import ImageForEquipment
from CADDrawing import CADDrawing
from pyautocad import Autocad, APoint
import xlwings as xw #wx.Frame与openpyxl的wb.save(filename)冲突，无法打开EXCEL
#from win32com.client import Dispatch
   
class Equipment(Nestle):
    allpart_data=PartsData()
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                     pos=wx.DefaultPosition,
                     size=(795,735)
                     )
        self.frame.SetLabel('设备')
        panel = wx.Panel(self.frame)
        panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 2), size=(195, 110), style=wx.BORDER_THEME)
        panel2 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 117), size=(195, 200), style=wx.BORDER_THEME)
        panel3 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 507), size=(195, 182), style=wx.BORDER_THEME)
        panel5 = wx.Panel(panel, id=wx.ID_ANY, pos=(200,2), size=(485,475), style=wx.BORDER_SUNKEN)
        panel5.SetBackgroundColour((255,255,255))
        panel7 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 322), size=(195, 182), style=wx.BORDER_THEME)
        self.tpvs=TPVS(self,panel1)
        self.material=Material(self,panel2)
        self.control=ControlForEquipment(self,panel3)
        i=self.allpart_data.equipment_design_data[2]
        ctrl_data=[[[i[0][3],(0,0),(0,0)],i[1]],]
        self.image=ImageForEquipment(self,panel5)
        self.weight=Weight(self,panel7)
        self.tpvs.TPNonInheritable()
#        self.tpvs.Enable(False)
        self.cb81 = wx.Button(panel, label="确定&&关闭", pos=(695, 669), size=(68, 22))
        self.cb811 = wx.Button(panel, label="图框&数据表-->", pos=(228, 615), size=(100, 22))
        self.cb812 = wx.Button(panel, label="管口表-->", pos=(338, 615), size=(100, 22))
        self.cb813 = wx.Button(panel, label="材料明细表-->", pos=(448, 615), size=(100, 22))
        self.cb814 = wx.Button(panel, label="管口许用载荷-->", pos=(558, 615), size=(100, 22))
        self.cb815 = wx.Button(panel, label="受压元件表-->", pos=(228, 642), size=(100, 22))
        self.cb816 = wx.Button(panel, label="输出SP3D数据", pos=(338, 642), size=(100, 22))
        self.cb817 = wx.Button(panel, label="显示3D模型", pos=(448, 642), size=(100, 22))
        self.cb818 = wx.Button(panel, label="输出Excel材料表", pos=(558, 642), size=(100, 22))
        self.cb819 = wx.Button(panel, label="设备图绘制-->", pos=(228, 669), size=(100, 22))
        self.cb820 = wx.Button(panel, label="技术要求(A)", pos=(338, 669), size=(100, 22))
        self.cb821 = wx.Button(panel, label="技术要求(B)", pos=(448, 669), size=(100, 22))
        self.cb822 = wx.Button(panel, label="输出SW建模数据", pos=(558, 669), size=(100, 22))
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
        self.cb811.Bind(wx.EVT_BUTTON,self.OnButton811)
        self.cb812.Bind(wx.EVT_BUTTON,self.OnButton812)
        self.cb813.Bind(wx.EVT_BUTTON,self.OnButton813)
        self.cb814.Bind(wx.EVT_BUTTON,self.OnButton814)
        self.cb818.Bind(wx.EVT_BUTTON,self.OnButton818)
        self.cb820.Bind(wx.EVT_BUTTON,self.OnWait)
        self.cb821.Bind(wx.EVT_BUTTON,self.OnWait)
        self.cb815.Enable(False)
        self.cb816.Enable(False)
        self.cb817.Enable(False)
        self.cb819.Enable(False)
#       self.cb820.Enable(False)
#       self.cb821.Enable(False)
        self.cb822.Enable(False)        

    def OnButton821(self,evt):
        print(self.GetData())
        
    def OnButton811(self,evt):
        draw=CADDrawing()
        sc=self.control.GetSc()
        acad, base, sc = draw.GetActiveCAD(acad=None, base=(0,0), sc=sc)
        tukuang_and_key_point = self.control.GetTukuangAndKeyPoint()
        design_sheet = self.control.GetEquipmentDesignSheet()
        tu_type = self.control.GetTuType()
        site_type = self.control.GetSiteType()
        path1 = acad.ActiveDocument.Path  # 文件存放路径C:\Users\xql1806\Documents
        path2 = acad.ActiveDocument.Application.Path  # CAD程序路径 C:\Program Files\AutoCAD 2010
        path3 = os.getcwd()
        sourcePath = path3 + "\\dwg\\"
        targetPath = path1 + "\\"
        obj=[]
        block=tukuang_and_key_point[0]
        if '.dwg' in block.lower():
            shutil.copy(sourcePath + block, targetPath)
            obj.append(acad.model.InsertBlock(APoint(0, 0), block, 1, 1, 1, 0 ))
            os.remove(targetPath + block)
        block=design_sheet[0][2]
#        print(tukuang_and_key_point)
        Pnt = APoint(tukuang_and_key_point[1][1][0], tukuang_and_key_point[1][1][1])
        if '.dwg' in block.lower():
            shutil.copy(sourcePath + block, targetPath)
            obj.append(acad.model.InsertBlock(Pnt, block, 1, 1, 1, 0 ))
            os.remove(targetPath + block)
        block=site_type[0]
        Pnt = APoint(tukuang_and_key_point[1][1][0],
                     tukuang_and_key_point[1][1][1]-design_sheet[0][5][1])
        if '.dwg' in block.lower():
            shutil.copy(sourcePath + block, targetPath)
            obj.append(acad.model.InsertBlock(Pnt, block, 1, 1, 1, 0 ))
            os.remove(targetPath + block)
        # 开始填写标题栏
        Pnt = APoint(tukuang_and_key_point[1][2][0], tukuang_and_key_point[1][2][1])
        for text in tu_type:
            pt=APoint((Pnt[0]+text[1][0]),(Pnt[1]+text[1][1]))
            textObj=acad.model.AddText((text[0]),pt,text[2])
            textObj.Color=3    #1红 2黄 3绿 4青 5蓝 6粉 7白
            textObj.ScaleFactor = text[3]
            textObj.Alignment = 1
            textObj.TextAlignmentPoint=pt
            textObj.StyleName = "HUALUC"
            obj.append(textObj)
        # 开始填写自然条件表
        zrtj1=site_type[1][0]
        zrtj2=site_type[1][1]
        zrtj3=site_type[1][2]
        zrtj4=site_type[1][3]
        zrtj5=site_type[1][4]
        zrtj6=site_type[1][5]
        content=[
            [zrtj1,(-103,-7),4,0.7],
            [zrtj2,(-103,-15),4,0.7],
            [zrtj3,(-103,-23),4,0.7],
            [zrtj4,(-19,-7),4,0.7],
            [zrtj5,(-19,-15),4,0.7],
            [zrtj6,(-19,-23),4,0.7],
            ]
        Pnt = APoint(tukuang_and_key_point[1][1][0],
                     tukuang_and_key_point[1][1][1]-design_sheet[0][5][1])
        for text in content:
            pt=APoint(Pnt[0]+text[1][0],Pnt[1]+text[1][1])
            textObj=acad.model.AddText((text[0]),pt,text[2])
            textObj.Color=3    #1红 2黄 3绿 4青 5蓝 6粉 7白
            textObj.ScaleFactor = text[3]
            textObj.Alignment = 1
            textObj.TextAlignmentPoint=pt
            textObj.StyleName = "STADHLSD"
            obj.append(textObj)

        # 开始填写设计数据表
        sheet=[]
#       print(design_sheet)
        for i in design_sheet[1]:
            t1=[]
            for j in i:
                if j not in self.allpart_data.Kong:
                    t1.append((j[0],j[1]))
                else:
                    t1.append(None)
            sheet.append(t1)
        if len(sheet)>1:   #将加宽了的换热器和夹套容器复原位置
            t1=[]
            key=0
            for i in sheet[0]:
                if i not in self.allpart_data.Kong:
                    if key in range(0,39):
                        if sheet[1][key] != None:
                            t2=((i[0][0],i[0][1]),(i[1][0]-20,i[1][1]))
                        else:
                            t2=((i[0][0],i[0][1]),(i[1][0]-40,i[1][1]))
                    else:
                        t2=((i[0][0]-40,i[0][1]),(i[1][0],i[1][1]))
                else:
                    t2=None
                t1.append(t2)
                key+=1
            sheet[0]=t1
            t1=[]
            key=0
            for i in sheet[1]:
                if i not in self.allpart_data.Kong:
                    if key in range(0,39):
                        if sheet[0][key] != None:
                            t2=((i[0][0]-20,i[0][1]),(i[1][0]-20,i[1][1]))
                        else:
                            t2=((i[0][0]-20,i[0][1]),(i[1][0]-40,i[1][1]))
                    else:
                        t2=((i[0][0]-40,i[0][1]),(i[1][0],i[1][1]))
                else:
                    t2=None
                t1.append(t2)
                key+=1
            sheet[1]=t1
        text = self.image.GetData()
#        print(text)
#        print(sheet)
        datakey=0
        for i in sheet:
            key=0
            for j in i:
                if (text[datakey] not in self.allpart_data.Kong) and (j not in self.allpart_data.Kong):
                    if key==47:
                        textObj=acad.model.AddMText(APoint(0,0),j[1][0]-3,text[datakey])
                        textObj.Height=4
                    else:
                        textObj=acad.model.AddText(text[datakey],APoint(0,0),4)
                        textObj.ScaleFactor = 0.7
                    textObj.Color=3    #1红 2黄 3绿 4青 5蓝 6粉 7白
                    textObj.StyleName = "STADHLSD"
                    z=tukuang_and_key_point[1][1]
                    if key in [39,40,41,42,43,44,45,46,47]:
                        x=j[0][0]-180+z[0]+2
                        y=-8-j[0][1]+z[1]+1
                        textObj.Move(APoint(0,0),APoint(x,y))
                    else:
                        x=j[0][0]-180+z[0]+j[1][0]/2
                        y=-8-j[0][1]+z[1]+1
                        textObj.Alignment = 1
                        textObj.TextAlignmentPoint=APoint(x,y)
                    obj.append(textObj)
                key+=1
                datakey+=1
        for i in obj:
            i.ScaleEntity(APoint(0,0),sc)
            #i.Move(APoint(0,0),base)
            
            
    def SetData(self,data):
        self.SetLableData(data[0])
        self.tpvs.SetData(data[1])
        self.material.SetData(data[2])
        self.control.SetData(data[3])
        #预留给MXB
        self.image.SetData(data[5])
        #预留给Location
        self.weight.SetData(data[7])
        self.SetLableData(data[0])
        
    def GetData(self):
        list1 = self.GetLableData()
        list2=  [list1,
                 self.tpvs.GetData(),
                self.material.GetData(),
                self.control.GetData(),
                [],
                self.image.GetData(),
                [],
                self.weight.GetData()]
        return list2

    def GetProjectInfo(self):
        class_nestle=self.Main.tree.GetItemData(self.Main.root)
        return class_nestle.GetProjectInfo()

    def GetSiteInfo(self):
        class_nestle=self.Main.tree.GetItemData(self.Main.root)
        return class_nestle.GetSiteInfo()

    def GetFatherBaseMat(self):
        material=[True,'板材', 'GB/T 713-2014', 'Q345R',]
        return material

    def GetFatherCladMat(self):
        smaterial= ['不锈钢复合','S31603',]
        return smaterial
    
    def MaterialChanged(self):
        pass

    def VSChanged(self):
        vol,surf=self.VSCal()
        self.tpvs.SetV(vol)
        self.tpvs.SetS(surf)
        weightcs,weightss=self.WeightCal()
        self.weight.SetWeightSS(weightss)
        self.weight.SetWeightCS(weightcs)

    def ImageChanged(self,ctrl_data):
        #将图片和控件进行组合成以下列表，交由Image类进行呈现
        #[[[图片,(0,0)]，[[控件组]，[控件组]]],[[[图片,(0,0)]，[[控件组]，[控件组]]]]
        data=self.image.GetData()
        self.image.SetImage(ctrl_data)
        self.image.SetLuoji()
        self.image.SetData(data)

    def SlideScChanged(self):
        pass
    
    def VSCal(self):
        ##计算时刷新tpvs上的数据
        item=self.Main.tree.GetFirstChild(self.currentnode)[0]
        vol=0
        surf=0
        while item.IsOk():
            b=self.Main.tree.GetItemData(item)
            if b.nestle_english_name in ['Component','Shell','NozzleFlange',
                                         'VesselFlange','Pipe','Support','ManWay','LiftingLug',]:
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
            if b.nestle_english_name in ['Component','Shell','NozzleFlange',
                                         'VesselFlange','Pipe','Support','ManWay','LiftingLug',]:
                weightcs1, weightss1 = b.mxb.GetWeights()
                weightcs+=weightcs1
                weightss+=weightss1
            item=self.Main.tree.GetNextSibling(item)
        return weightcs,weightss

    def OnFocus(self, evt):
        self.Main.currentnode = self.currentnode
        self.VSChanged()

    def OnButton813(self, evt):
        mxbcontent=self.GetMXBContent() #该方法在Nestle里，被继承过来了
        draw=CADDrawing()
        sc=self.control.GetSc()
        acad, base, sc = draw.GetActiveCAD(acad=None, base=-1, sc=sc)
        path1 = acad.ActiveDocument.Path  # 文件存放路径C:\Users\xql1806\Documents
        path2 = acad.ActiveDocument.Application.Path  # CAD程序路径 C:\Program Files\AutoCAD 2010
        path3 = os.getcwd()
        sourcePath = path3 + "\\dwg\\"
        targetPath = path1 + "\\"
        head='B-明细栏.dwg'
        shutil.copy(sourcePath + head, targetPath)
        obj=[]
        obj.append(acad.model.InsertBlock(APoint(0, 0), head, 1, 1, 1, 0 ))
        os.remove(targetPath + head)
        loc=[0,20,50,95,105,135,145,155,180] #明细表列的位置
        lot=[4,10.5,16,3,10,3,3,8]  #明细栏所能容纳最长字符
        loh=8 #明细表行的高度
        loh1=10 #明细栏表头高度
        num=len(mxbcontent)
        y=num*loh+loh1
        for x in loc:
            obj.append(acad.model.AddLine(APoint(x,loh1),APoint(x,y)))
        num=0
        for hang in mxbcontent:
            key=0
            for text in hang:
                textObj=acad.model.AddText(text, APoint(loc[key]+1,num*loh+loh1+1), 4)
                if lot[key] < len(text):
                    textObj.ScaleFactor = 0.7 * lot[key]/len(text)    #文字宽度缩放
                else:
                    textObj.ScaleFactor = 0.7
                obj.append(textObj)
                key+=1
            obj.append(acad.model.AddLine(APoint(loc[0],(num+1)*loh+loh1),APoint(loc[-1],(num+1)*loh+loh1)))
            num+=1
        for i in obj:
            i.ScaleEntity(APoint(0,0),sc)
            i.Move(APoint(0,0),base)
                
    def OnButton818(self, evt):
        mxbcontent=self.GetMXBContent() #该方法在Nestle里，被继承过来了
        for i in range(len(mxbcontent)):
            mxbcontent[i][0]="'"+mxbcontent[i][0]
        with wx.FileDialog(self.frame,
                           "将明细栏保存成为一个EXCEL文件",
                           wildcard="xlsx files (*.xlsx)|*.xlsx|xls files (*.xls)|*.xls",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                pass
            else:
                filename=fileDialog.GetPath()
                app = xw.App(visible=False, add_book=False)
                wb = app.books.add()
                ws1 = wb.sheets.active
                ws1.name="ALLPart 输出的明细栏"
                ws1.range('A1').value=['件号','图号或标准号','名      称','数量','材   料','单重(kg)','总重(kg)','备   注']
                i=0
                for j in mxbcontent:
                   ws1.range('A'+str(i+2)).value=j[0]
                   ws1.range('B'+str(i+2)).value=j[1]
                   ws1.range('C'+str(i+2)).value=j[2]
                   ws1.range('D'+str(i+2)).value=float(j[3])
                   ws1.range('E'+str(i+2)).value=j[4]
                   ws1.range('F'+str(i+2)).value= float(j[5])
                   ws1.range('G'+str(i+2)).value='=D'+str(i+2)+'*'+'F'+str(i+2)
                   ws1.range('H'+str(i+2)).value=j[7]
                   i+=1
                try:
                   wb.save(filename)
                   wb.close()
                   xl = Dispatch("Excel.Application")
                   xl.Visible = True # otherwise excel is hidden
                   xl.Workbooks.Open(filename)
                except:
                   wx.MessageBox('保存文件时发生了一个错误，请退出EXCEL进程再试试。','错误',wx.OK|wx.ICON_INFORMATION)   

    def OnButton812(self,evt):
        guankou_list=[]
        def preOrder(item):
            nonlocal guankou_list
            if not item.IsOk():
                return
            b=self.Main.tree.GetItemData(item)
            if hasattr(b,'GetGuanKou'):
                for i in b.GetGuanKou():
                    guankou_list.append(i[:-1])
            preOrder(self.Main.tree.GetFirstChild(item)[0])
            preOrder(self.Main.tree.GetNextSibling(item))
        preOrder(self.currentnode)
        draw=CADDrawing()
        sc=self.control.GetSc()
        draw.GetActiveCAD(acad=None, base=-1, sc=sc)
        head='B-管口表.dwg'
        draw.Drawbiao1(guankou_list,head=head,             #绘制和填充表格,表头靠插入块,插入基点在右上
                 loc=[0,15,30,45,60,105,120,135,180],   #表列的位置,loc[-1]为表头的宽度
                 lot=[5,5,5,5,16,5,5,16],             #表所能容纳最长字符
                 loh0=8,loh1=16)                #表行的高度 loh1为表头高度
            
    def OnButton814(self,evt):
        guankou_list=[]
        def preOrder(item):
            nonlocal guankou_list
            if not item.IsOk():
                return
            b=self.Main.tree.GetItemData(item)
            if hasattr(b,'GetGuanKou'):
                for i in b.GetGuanKou():
                    guankou_list.append(i)
            preOrder(self.Main.tree.GetFirstChild(item)[0])
            preOrder(self.Main.tree.GetNextSibling(item))
        preOrder(self.currentnode)
        zaihebiao=[]
        for i in guankou_list:
            if i[8]: #根据是否建模的勾选确定是否列入载荷表
                zaihebiao.append([i[0],i[1],i[2]])

        zaihebiao_list=[]
        key=0  #英制key=0，公制key=1
        for i in zaihebiao:
            for j in self.allpart_data.PipeN:
                if j[1]==i[1]:
                    dn1=j[4]
                    dn2=j[1]
                    break
            for j in self.allpart_data.NozzleFlange_class_pn:
                if j[1]==i[2]:
                    a_zhxs=j[3]
                    if j[1] in ['PN20','PN50','PN110','PN150','PN260','PN420']:
                        key=0
                    if j[1] in ['PN6','PN10','PN16','PN25','PN40','PN63','PN100','PN160']:
                        key=1
                    break
            if key==0:
                FR=self.allpart_data.guankouzaihe[0][0].replace('a',a_zhxs).replace('DN1',dn1)
                FL=self.allpart_data.guankouzaihe[0][1].replace('a',a_zhxs).replace('DN1',dn1)
                FC=self.allpart_data.guankouzaihe[0][2].replace('a',a_zhxs).replace('DN1',dn1)
                MT=self.allpart_data.guankouzaihe[0][3].replace('a',a_zhxs).replace('DN1',dn1)
                ML=self.allpart_data.guankouzaihe[0][4].replace('a',a_zhxs).replace('DN1',dn1)
                MC=self.allpart_data.guankouzaihe[0][5].replace('a',a_zhxs).replace('DN1',dn1)
            if key==1:
                FR=self.allpart_data.guankouzaihe[1][0].replace('a',a_zhxs).replace('DN2',dn2)
                FL=self.allpart_data.guankouzaihe[1][1].replace('a',a_zhxs).replace('DN2',dn2)
                FC=self.allpart_data.guankouzaihe[1][2].replace('a',a_zhxs).replace('DN2',dn2)
                MT=self.allpart_data.guankouzaihe[1][3].replace('a',a_zhxs).replace('DN2',dn2)
                ML=self.allpart_data.guankouzaihe[1][4].replace('a',a_zhxs).replace('DN2',dn2)
                MC=self.allpart_data.guankouzaihe[1][5].replace('a',a_zhxs).replace('DN2',dn2)         
            FR=str(int(eval(FR)))
            FL=str(int(eval(FL)))
            FC=str(int(eval(FC)))
            MT=str(int(eval(MT)))
            ML=str(int(eval(ML)))
            MC=str(int(eval(MC)))
            zaihebiao_list.append([i[0],i[1],FR,FL,FC,MT,ML,MC])
        draw=CADDrawing()
        sc=self.control.GetSc()
        draw.GetActiveCAD(acad=None, base=-1, sc=sc)
        head='B-管口许用载荷表.dwg'
        draw.Drawbiao1(zaihebiao_list,head=head,             #绘制和填充表格,表头靠插入块,插入基点在右上
                 loc=[0,15,30,55,80,105,130,155,180],   #表列的位置,loc[-1]为表头的宽度
                 lot=[5,5,8,8,8,8,8,8],             #表所能容纳最长字符
                 loh0=8,loh1=76)                #表行的高度 loh1为表头高度
                    
            
        
        



