import wx
#from softwareEvaluation import soft_evaluation
from pyautocad import Autocad, APoint
from ALLPartData import PartsData
from  Nestle import  Nestle
from DrawPlat import DrawPlat
import os

class PlatFormHor( Nestle):
    allpart_data=PartsData()
    tukuang_list=allpart_data.tukuang_list
    def __init__(self, main):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                                      id=wx.ID_ANY,
                                      title='卧式平台',
                                      pos=wx.DefaultPosition,
                                      size=(282, 508),
                                      style=wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self.frame)
        wx.StaticText(self.panel, label='梯子平台图号', pos=(10, 10))
        self.cb11 = wx.TextCtrl(self.panel, value="", pos=(90, 10), size=(140, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label='平台类型', pos=(10, 35))
        self.cb12 = wx.ComboBox(self.panel, pos=(70, 35), size=(190, 22),
                                choices=['Ⅰ型（单侧）DN1000~3200',
                                         'Ⅱ型（双侧）DN1000~3200',
                                         'Ⅲ型（单侧）DN3000~5000',
                                         'Ⅳ型（双侧）DN3000~5000'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='平台标高', pos=(10, 60))
        wx.StaticText(self.panel, label='mm', pos=(235, 60))
        self.cb13 = wx.ComboBox(self.panel, pos=(90, 60), size=(140, 22),
                                choices=['5000', '6000', '7000', '8000'],style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='设备中心标高', pos=(10, 85))
        wx.StaticText(self.panel, label='mm', pos=(235, 85))
        self.cb14 = wx.ComboBox(self.panel, pos=(90, 85), size=(140, 22),
                                choices=['4000', '5000', '6000', '7000'],style=wx.CB_DROPDOWN)    

        wx.StaticText(self.panel, label='鞍座底板标高', pos=(10, 110))
        wx.StaticText(self.panel, label='mm', pos=(235, 110))
        self.cb15 = wx.ComboBox(self.panel, pos=(90, 110), size=(140, 22),
                                choices=['3000', '4000', '5000', '6000'],style=wx.CB_DROPDOWN)

        wx.StaticText(self.panel, label='起步（地面）标高', pos=(10, 135))
        wx.StaticText(self.panel, label='mm', pos=(235, 135))
        self.cb16 = wx.ComboBox(self.panel, pos=(120, 135), size=(110, 22),
                                choices=['2000', '3000', '4000', '5000'],style=wx.CB_DROPDOWN)      

        wx.StaticText(self.panel, label='设备外径', pos=(60, 160))
        wx.StaticText(self.panel, label='mm', pos=(235, 160))
        self.cb17 = wx.TextCtrl(self.panel, value="", pos=(120, 160), size=(110, 22), style=wx.TE_LEFT)

        wx.StaticText(self.panel, label='切线长度', pos=(60, 185))
        wx.StaticText(self.panel, label='mm', pos=(235, 185))
        self.cb18 = wx.TextCtrl(self.panel, value="", pos=(120, 185), size=(110, 22), style=wx.TE_LEFT)

        wx.StaticText(self.panel, label='保温厚度', pos=(60, 210))
        wx.StaticText(self.panel, label='mm', pos=(235, 210))
        self.cb19 = wx.TextCtrl(self.panel, value="", pos=(120, 210), size=(110, 22), style=wx.TE_LEFT)

        wx.StaticText(self.panel, label='平台宽度W1', pos=(8, 235))
        self.cb20 = wx.ComboBox(self.panel,  choices=['800','900','1000','1200',],
                                pos=(80, 235), size=(60, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label="W1'", pos=(145, 235))
        wx.StaticText(self.panel, label='mm', pos=(235, 235))
        self.cb21 =wx.ComboBox(self.panel,  choices=['0','100','150','200','300',],
                                pos=(170, 235), size=(60, 22), style=wx.TE_LEFT)

        wx.StaticText(self.panel, label="平台左边线距左封头切线", pos=(10, 260))
        wx.StaticText(self.panel, label='mm', pos=(215, 260))
        self.cb22 = wx.TextCtrl(self.panel, value="", pos=(150, 260), size=(60, 22), style=wx.TE_LEFT)

        wx.StaticText(self.panel, label="平台内边线距设备中心线", pos=(10, 285))
        wx.StaticText(self.panel, label='mm', pos=(215, 285))
        self.cb23 = wx.TextCtrl(self.panel, value="", pos=(150, 285), size=(60, 22), style=wx.TE_LEFT)

        wx.StaticText(self.panel, label="平台长度", pos=(33, 310))
        wx.StaticText(self.panel, label='mm', pos=(215, 310))
        self.cb24 = wx.TextCtrl(self.panel, value="", pos=(90, 310), size=(120, 22), style=wx.TE_LEFT)
        
        wx.StaticText(self.panel, label='图框大小', pos=(33, 335))
        self.cb25 = wx.ComboBox(self.panel, pos=(90, 335), size=(140, 22),
                                choices=["A0", "A0V", "A1", "A1V", "A2x3", "A2x3V", "A2x4", "A2x4V"],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='总图比例', pos=(33, 360))
        self.cb26 = wx.ComboBox(self.panel, pos=(90, 360), size=(140, 22),
                                choices=['1:5', '1:10', '1:15', '1:20', '1:30', '1:40', '1:50'],
                                style=wx.CB_DROPDOWN)
        self.cb31 = wx.Button(self.panel, label='立面图-->', pos=(10, 389), size=(120, 22))
        self.cb32 = wx.Button(self.panel, label='左视图-->', pos=(140, 389), size=(120, 22))
        self.cb33 = wx.Button(self.panel, label='俯视图-->', pos=(10, 416), size=(120, 22))
        self.cb34 = wx.Button(self.panel, label='全自动绘图', pos=(140, 416), size=(120, 22))
#       self.cb35 = wx.Button(self.panel, label='调试', pos=(10, 448), size=(60, 22))
        self.cb31.Bind(wx.EVT_BUTTON, self.OnButton31)
        self.cb32.Bind(wx.EVT_BUTTON, self.OnButton32)
        self.cb33.Bind(wx.EVT_BUTTON, self.OnButton33)
        self.cb34.Bind(wx.EVT_BUTTON, self.OnButton34)
#       self.cb35.Bind(wx.EVT_BUTTON, self.OnButton35)
        self.cb12.Enable(False) 
        self.cb81 = wx.Button(self.panel, label='确定&&关闭', pos=(192, 445), size=(68, 22))
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
        self.cb13.Bind(wx.EVT_TEXT, self.OnCombobox13)
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJleHAiOjE2Njk5MDA1MDUsInVzZXJuYW1lIjoi5byg\
5LiJIn0.Q6YFZVEte9syYnUNv_drVDyqvZdyCQ7iRAKwj_\
kYxYI2ac44369-d85d-4716-a33a-71e49831660c'
        type_name="22720_化工设备梯子平台绘图软件"
        try:
            evaluation=soft_evaluation.soft_evaluation(token,type_name,
                                                   '正在处理卧式平台...')
        except:
            evaluation='未能提交塔平台后评价信息。'
        print(evaluation)
        
    def OnCombobox13(self, evt):  # 打开下拉列表时 导航栏显示平台标高
        t1 = '卧式平台-->' + ' EL' + self.cb13.GetValue()
        self.frame.SetLabel(t1)
        
    def GetData(self):
        list1 = self.GetLableData()
        list2 = [self.cb11.GetValue(),
                self.cb12.GetValue(),
                self.cb13.GetValue(),
                self.cb14.GetValue(),
                self.cb15.GetValue(),
                self.cb16.GetValue(),
                self.cb17.GetValue(),
                self.cb18.GetValue(),
                self.cb19.GetValue(),
                self.cb20.GetValue(),
                self.cb21.GetValue(),
                self.cb22.GetValue(),
                self.cb23.GetValue(),
                self.cb24.GetValue(),
                self.cb25.GetValue(),
                self.cb26.GetValue(),
                 ]
        return [list1, list2, ]
        
    def SetData(self,data):
        self.cb11.SetValue(data[1][0])
        self.cb12.SetValue(data[1][1])
        self.cb13.SetValue(data[1][2])
        self.cb14.SetValue(data[1][3])
        self.cb15.SetValue(data[1][4])
        self.cb16.SetValue(data[1][5])
        self.cb17.SetValue(data[1][6])
        self.cb18.SetValue(data[1][7])
        self.cb19.SetValue(data[1][8])
        self.cb20.SetValue(data[1][9])
        self.cb21.SetValue(data[1][10])
        self.cb22.SetValue(data[1][11])
        self.cb23.SetValue(data[1][12])
        self.cb24.SetValue(data[1][13])
        self.cb25.SetValue(data[1][14])
        self.cb26.SetValue(data[1][15])
        self.SetLableData(data[0])
        
    def OnButton31(self,evt):
        data=self.OnButton35(True)
        draw=DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        draw.DrawHorF(data)

    def OnButton32(self,evt):
        data=self.OnButton35(True)
        draw=DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        draw.DrawHorL(data)

    def OnButton33(self,evt):
        data=self.OnButton35(True)
        draw=DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        draw.DrawHorT(data)

    def OnButton34(self,evt):
        data=self.OnButton35(True)
        a=self.cb13.GetValue()        #"A1V"
        for i in self.tukuang_list:
            if a==i[0]:
                a3=i[1]  #a1v.DWG
                a4=i[2]  #图框中关键点定位坐标
                break
            a3='a1.DWG'  #a1v.DWG
            a4=((25,10),(831,584),(651,95))
        draw = DrawPlat()
        acad, base, sc=draw.GetActiveCAD(acad=None, base=(0,0), sc=self.sc)
        path1 = acad.ActiveDocument.Path  # 文件存放路径C:\Users\xql1806\Documents
        path2 = acad.ActiveDocument.Application.Path  # CAD程序路径 C:\Program Files\AutoCAD 2010
        path3 = os.getcwd()
        copystr = "copy " + path3 + "\\dwg\\"+ a3 +" " + path1 + "\\"
        print(copystr)
        os.system(copystr)  #将图框拷贝到当前目录下，以便成功插入图框
        Pnt1 = APoint(0, 0)
        acad.model.InsertBlock(Pnt1, a3, sc, sc, 1, 0 )
        root_nestle=self.Main.tree.GetItemData(self.Main.root)
        content=[]
        content.append(['0',(5,-27),4,0.7])
        content.append(['供 施 工',(32,-27),4,0.7])
        content.append([root_nestle.cb12.GetValue(),(135,-48),4,0.7]) #项目名称
        content.append([root_nestle.cb11.GetValue(),(170,-48),3,0.7]) #项目代号
        parent = self.Main.tree.GetItemParent(self.currentnode)
        parent_class = self.Main.tree.GetItemData(parent)
        content.append([parent_class.control.cb73.GetValue(),(156,-57),4,0.7]) #主项名称代号
        content.append([root_nestle.cb13.GetValue(),(140,-66),4,0.7]) #设计阶段          
        tuhao1=[root_nestle.cb11.GetValue()+'-'+self.cb11.GetValue(),(135,-74),4,0.7] #梯子图号
        tuhao2=[root_nestle.cb11.GetValue()+'-'+parent_class.control.cb77.GetValue()+"-0?",(135,-74),4,0.7] #支耳图号
        content.append(tuhao1)
        content.append([self.cb26.GetValue(),(120,-83),4,0.7]) #比例
        eqname=parent_class.control.cb71.GetValue()+'('+parent_class.control.cb72.GetValue()+')'
        content.append([eqname,(50,-66),6,0.7]) #设备名称
        content.append(['梯子平台',(50,-83),5,0.8]) #工程图 装配图
        for text in content:
            pt=APoint((a4[2][0]+text[1][0])*sc,(a4[2][1]+text[1][1])*sc)
            textObj=acad.model.AddText((text[0]),pt,text[2]*sc)
            textObj.Color=3    #1红 2黄 3绿 4青 5蓝 6粉 7白
            textObj.ScaleFactor = text[3]
            textObj.Alignment = 1
            textObj.TextAlignmentPoint=pt
            textObj.StyleName = "HUALUC"    
        draw.base=APoint(300*sc,300*sc)
        base=draw.base
        draw.DrawHorF(data)
        draw.base=APoint(base[0]+data[5]+data[4],base[1],base[2])
        draw.DrawHorL(data)   
        draw.base=APoint(base[0],base[1]-data[4]*2,base[2])
        draw.DrawHorT(data)
# 开始写技术要求
        text1 = "              说 明\n"
        text2 = "1. 梯子、平台的制造、安装和验收按华陆标准图04-8902进行。\n"
        text3 = "2. 图中所有节点见标准图，图中引用的节点标记与标准图相同。\n"
        text4 = "3. 平台标高确定在托架梁上翼缘顶面处。\n"
        tuhao3=root_nestle.cb11.GetValue() + '-' + parent_class.control.cb77.GetValue() + "-01"
        text5 = "注：本梯子平台安装在"+eqname+"上，装配图图号为"+tuhao3+"。"
        text=text1+text2+text3+text4+text5
        Pnt4 = APoint((a4[2][0]) * sc, (a4[2][1]+100) * sc)
        textObj = acad.model.AddMText(Pnt4, 180 * sc, text)
        textObj.StyleName = "STADHLSD"
        textObj.Height = sc * 6

    def OnButton35(self,evt):
        data=self.GetData()
        dat=[]
        for da in data[1][2:14]:
            dat.append(int(da))
        b = self.cb26.GetValue()  # '1:20'
        try:
           b=b.split(":")
           self.sc=float(b[1])/float(b[0])
        except:
           self.sc=1
        return dat

if __name__ == '__main__':
    app = wx.App()
    frame = wx.MDIParentFrame(None, -1, "华陆化工设备梯子平台绘图软件",
                                           pos=(10, 10), size=(400, 700))
    frame.Center()
    menubar = wx.MenuBar()
    menu1 = wx.Menu()
    menu1.Append(5101, "新建", "新建一个ALLPart文件")
    menu1.Append(5102, "打开", "打开一个ALLPart文件")
    menu1.Append(5103, "保存", "保存一个ALLPart文件")
    menu1.Append(5104, "另存为...", "保存一个ALLPart文件备份")
    menu1.Append(5105, "退出", "退出ALLpart软件")
    menubar.Append(menu1, "文件")
    frame.SetMenuBar(menubar)
    data=[['PlatFormHor', 3, '卧式设备平台', '卧式平台--> EL10000'],
         ['8317', 'Ⅱ型（双侧）DN1000~3200', '10000', '8500',
          '7600', '7000', '2024', '4000', '30', '900', '100',
          '200', '500', '4200', 'A1', '1:30']]
    platformhor = PlatFormHor(frame,data)
    frame.Show()
    platformhor.frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
