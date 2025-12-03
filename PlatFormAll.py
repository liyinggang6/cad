import wx
import shutil
from ALLPartData import PartsData
#from pyautocad import Autocad, pyautocad
from pyautocad import Autocad
import pyautocad
from pyautocad import Autocad, APoint

from Calculate import Calculate
from  Nestle import  Nestle
from  DrawPlat import DrawPlat
import os

class PlatFormAll(Nestle):
    allpart_data=PartsData()
    tukuang_list=allpart_data.tukuang_list
    DNO = [
        ['800≤OD≤1000', '45'],
        ['1000＜OD≤2000', '36'],
        ['2000＜OD≤3100', '30'],
        ['3100＜OD≤4700', '24'],
        ['4700＜OD≤6000', '18'],
        ['6000＜OD≤8200', '15'],
        ['8200＜OD≤11000', '12']
    ]
    Ptype = [
        ['塔顶托架', 'DTJ', 'DZE', '800', '1 级，2.0kN/m2', '4-M16',1,2,], #增加一个Ptype代号和TiebanType代号
        ['塔顶托架', 'DTJ', 'DZE', '800', '2 级，4.0kN/m2', '4-M16',2,2,],
        ['塔顶托架', 'DTJ', 'DZE', '1000', '1 级，2.0kN/m2', '4-M16',3,2,],
        ['塔顶托架', 'DTJ', 'DZE', '1000', '2 级，4.0kN/m2', '4-M16',4,2,],
        ['悬臂式托架', 'XTJ', 'XZE', '1000', '1 级，2.0kN/m2', '4-M16',5,3,],
        ['悬臂式托架', 'XTJ', 'XZE', '1200', '1 级，2.0kN/m2', '4-M16',6,3,],
        ['悬臂式托架', 'XTJ', 'XZE', '1000', '2 级，4.0kN/m2', '4-M16',7,3,],
        ['悬臂式托架', 'XTJ', 'XZE', '1200', '2 级，4.0kN/m2', '4-M20',8,3,],
        ['角撑式托架', 'CTJ', 'CZE', '1500', '1 级，2.0kN/m2', '4-M16',9,4,],
        ['角撑式托架', 'CTJ', 'CZE', '1500', '2 级，4.0kN/m2', '4-M20',10,4,],
        ['角撑式托架', 'CTJ', 'CZE', '2000', '1 级，2.0kN/m2', '4-M20',11,6,],
        ['角撑式托架', 'CTJ', 'CZE', '2000', '2 级，4.0kN/m2', '4-M20',12,6,],
        ['梯梁支撑', 'U型支撑 100x10', 'TZE-1', None, None, '2-M16',13,1,],
        ['梯梁支撑', 'U型支撑 120x10', 'TZE-1', None, None, '2-M16',14,1,],
    ]
    Nschang = ['300', '350', '400', '450', '500', '550', '600', ]
    cta = ['15', '30', '45', '60', '75', '90', '105', '120', '135', '150', '165', '180', '195',
           '210', '225', '240', '255', '270', '285', '300', '315', '330', '345', '360']
    def __init__(self, main,):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                                      id=wx.ID_ANY,
                                      title='梯子平台',
                                      pos=wx.DefaultPosition,
                                      size=(282, 283),
                                      style=wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self.frame)
        wx.StaticText(self.panel, label='梯子平台图号', pos=(10, 10))
        self.cb11 = wx.TextCtrl(self.panel, value="", pos=(90, 10), size=(170, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label='梯子起步标高', pos=(10, 35))
        wx.StaticText(self.panel, label='mm', pos=(235, 35))
        self.cb12 = wx.ComboBox(self.panel, pos=(90, 35), size=(140, 22),
                                choices=['0', '5000', '10000', '15000', '20000'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='图框大小', pos=(33, 60))
        self.cb13 = wx.ComboBox(self.panel, pos=(90, 60), size=(140, 22),
                                choices=["A0", "A0V", "A1", "A1V", "A2x3", "A2x3V", "A2x4", "A2x4V"],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='总图比例', pos=(33, 85))
        self.cb14 = wx.ComboBox(self.panel, pos=(90, 85), size=(140, 22),
                                choices=['1:5', '1:10', '1:15', '1:20', '1:30', '1:40', '1:50'],
                                style=wx.CB_DROPDOWN)
        self.cb31 = wx.Button(self.panel, label='立面图-->', pos=(10, 110), size=(120, 22))
        self.cb32 = wx.Button(self.panel, label='平面图-->', pos=(140, 110), size=(120, 22))
        self.cb33 = wx.Button(self.panel, label='立面&&平面图-->', pos=(10, 137), size=(120, 22))
        self.cb34 = wx.Button(self.panel, label='托架表-->', pos=(140, 137), size=(120, 22))
        self.cb35 = wx.Button(self.panel, label='材料表-->', pos=(10, 164), size=(120, 22))
        self.cb36 = wx.Button(self.panel, label='支耳表-->', pos=(140, 164), size=(120, 22))
        self.cb37 = wx.Button(self.panel, label='自动生成梯子平台图纸-->', pos=(10, 191), size=(250, 22))
        self.cb38 = wx.Button(self.panel, label='塔外壁展开图-->', pos=(10, 218), size=(120, 22))
        self.cb81 = wx.Button(self.panel, label='确定&&关闭', pos=(192, 223), size=(68, 22))
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb31.Bind(wx.EVT_BUTTON, self.OnButton31)
        self.cb32.Bind(wx.EVT_BUTTON, self.OnButton32)
        self.cb34.Bind(wx.EVT_BUTTON, self.OnButton34)
        self.cb35.Bind(wx.EVT_BUTTON, self.OnButton35)        
        self.cb36.Bind(wx.EVT_BUTTON, self.OnButton36)
        self.cb37.Bind(wx.EVT_BUTTON, self.OnButton37)
        self.cb38.Bind(wx.EVT_BUTTON, self.OnButton38)        
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)
        self.cb33.Enable(False)

    def OnButton31_38(self, evt):
        #收集数据并剔除太近的平台
        b = self.cb14.GetValue()  # '1:20'
        try:
           b=b.split(":")
           self.sc=float(b[1])/float(b[0])
        except:
           self.sc=1
        arr = []
        currentclass = self.Main.tree.GetItemData(self.currentnode)
        arr.append([currentclass.currentnode, currentclass.GetData()])  #增加了一个节点对象到列表
        node = self.Main.tree.GetFirstChild(self.currentnode)[0]
        while node.IsOk():
            currentclass = self.Main.tree.GetItemData(node)
            arr.append([currentclass.currentnode, currentclass.GetData()])
            node = self.Main.tree.GetNextSibling(node)
        for i in range(2, len(arr)):  # 按标高进行排序
            for j in range(1, len(arr) - i):
                if int(arr[j][1][1][4]) > int(arr[j + 1][1][1][4]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        rest = []
        rest.append(arr[0])
        i = arr[1]
        rest.append(i)
        for j in arr[2:]:  # 标高差小于200的平台提醒后删除
            if int(j[1][1][4]) > int(i[1][1][4]) + 200:
                i = j
                rest.append(i)
            else:
                ret = wx.MessageBox('发现了一处相距太近的平台,是否自动去除？', '去除平台', wx.YES | wx.NO)
                if ret == wx.YES:
                    a = self.Main.tree.GetItemData(j[0])
                    a.frame.Destroy()
                    self.Main.tree.Delete(j[0])
                else:
                    return False
        self.cal = Calculate()
        rest3 = self.cal.plat(rest, self.Ptype)  # 将全部梯子平台输入数据发送给计算模块
        self.platdata=rest3
        for j in rest3:
            a=self.Main.tree.GetItemData(j[0])
            a.platdata=j[1]
        Radius3 = self.platdata[0][1][1][2]
        lunkuo=[Radius3*2+self.sc*50,self.platdata[-1][1][0][1]-self.platdata[0][1][0][0]+self.sc*30,
                Radius3*2+self.sc*30] #梯子平台绘图轮廓计算[立面图宽、立面图高、平面图高or宽]
        self.platorangedata=[]
        for i in rest:
            self.platorangedata.append(i[1])
        return lunkuo

    def OnButton34_36(self, evt):  # 计算托架表
        if self.OnButton31_38(True):
            zhierlist=[]
            key=0
            for i in self.platdata:
                key += 1
##                print(self.platorangedata[key][1])
##                print(i[1])
                zhierlist+=(self.cal.calzhierlist(self.platorangedata[key][1],self.Ptype,i[1]))
            return zhierlist
        return False

    def OnButton31(self, evt):  #执行绘制立面图
        if self.OnButton31_38(True):
            draw = DrawPlat()
            acad, base, sc=draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
            base1=[0,0,0]
            base1[0] = base[0]
            base1[1] = base[1]
            hh0=self.platdata[0][1][0][0]
            for j in self.platdata:
#                print('j in self.platdata:',j)
                draw.DrawVer(j[1], acad, base1, sc)
                base1[1]=base[1]+j[1][0][1]-hh0
#                print('j[1][0][1]=',j[1][0][1])

    def OnButton32(self, evt):   #执行绘制平面图
        if self.OnButton31_38(True):
            draw = DrawPlat()
            acad, base, sc=draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
            base1=[0,0,0]
            base1[0] = base[0]
            base1[1] = base[1]
            hh0=self.platdata[0][1][1][2]*2+80*sc
            key=0
            for j in self.platdata:
                base1[1] = base[1] + hh0 * key
                draw.DrawHor(j[1], acad, base1, sc)
                Nestle
                key+=1

    def OnButton34(self, evt):   #执行绘制托架表
        zhierlist =self.OnButton34_36(True)
        if zhierlist:
            data = []
            for i in zhierlist:
                del i[1]
                data.append(i)
            datahead = ['型 号', '标高 (mm)', '角  度α(°)', 'L1 (mm)', 'L2 (mm)', '备 注']
            draw = DrawPlat()
            draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
            draw.Drawbiao(data, datahead)

    def OnButton36(self, evt):   #执行绘制支耳表
        zhierlist =self.OnButton34_36(True)
##        print('zhierlist=', zhierlist)
        if zhierlist:
            data = []
            for i in zhierlist:
                del i[0]
                data.append(i)
            datahead = ['型 号', '标高 (mm)', '角  度α(°)', 'L1 (mm)', 'L2 (mm)', '备 注']
            draw = DrawPlat()
            draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
            draw.Drawbiao(data, datahead)

    def OnButton37(self, evt):   #执行全自动绘图
        a=self.cb13.GetValue()        #"A1V"
        for i in self.tukuang_list:
            if a==i[0]:
                a3=i[1]  #a1v.DWG
                a4=i[2]  #图框中关键点定位坐标
                break
            a3='a1v.DWG'  #a1v.DWG
            a4=((10,10),(584,816),(404,95))
        lunkuo=self.OnButton31_38(True)
        if lunkuo:
            draw = DrawPlat()
            acad, base, sc=draw.GetActiveCAD(acad=None, base=(0,0), sc=self.sc)
            path1 = acad.ActiveDocument.Path  # 文件存放路径C:\Users\xql1806\Documents
            path2 = acad.ActiveDocument.Application.Path  # CAD程序路径 C:\Program Files\AutoCAD 2010
            path3 = os.getcwd()
            sourcePath = path3 + "\\dwg\\"
            targetPath = path1 + "\\"
            block=a3
            Pnt1 = APoint(0, 0)
            shutil.copy(sourcePath + block, targetPath)
            acad.model.InsertBlock(Pnt1, block, sc, sc, 1, 0 )
            os.remove(targetPath + block)
            
            Pnt2 = APoint((a4[1][0]-180 - 30) * sc, (a4[1][1]-35) * sc)
            block='PN.DWG'
            shutil.copy(sourcePath + block, targetPath)
            acad.model.InsertBlock(Pnt2, block, sc, sc, 1, 0)
            os.remove(targetPath + block)
            
            Pnt3 = APoint((a4[1][0]+20)*sc, 0)
            block='a3T.DWG'
            shutil.copy(sourcePath + block, targetPath)
            blockObj=acad.model.InsertBlock(Pnt3,  block, sc, sc, 1, 0)
            os.remove(targetPath + block)
            blockObj.Explode
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
            content.append([self.cb14.GetValue(),(120,-83),4,0.7]) #比例
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
            base=[lunkuo[0]/2+10*sc,90*sc,0]
            base1=[0,0,0]
            base1[0] = base[0]
            base1[1] = base[1]
            hh0=self.platdata[0][1][0][0]
            for j in self.platdata:
                draw.DrawVer(j[1], acad, base1, sc)
                base1[1]=base[1]+j[1][0][1]-hh0
            base=[lunkuo[0]+lunkuo[2]/2+80*sc,lunkuo[2]/2+100*sc,0]
            base1=[0,0,0]
            base1[0] = base[0]
            base1[1] = base[1]
            hh0=self.platdata[0][1][1][2]*2+80*sc
            key=0
            for j in self.platdata:
                base1[1] = base[1] + hh0 * key
                draw.DrawHor(j[1], acad, base1, sc)
                key+=1
# 开始写技术要求
            text1 = "              技术要求\n"
            text2 = "1. 梯子、平台的制造、安装和验收按HG/T21543-2009进行。\n"
            text3 = "2. 图中所有节点见标准图，图中引用的节点标记与标准图相同。\n"
            text4 = "3. 平台标高确定在托架梁上翼缘顶面处。\n"
            tuhao3=root_nestle.cb11.GetValue() + '-' + parent_class.control.cb77.GetValue() + "-01"
            text5 = "注：本梯子平台安装在"+eqname+"上，装配图图号为"+tuhao3+"。"
            text=text1+text2+text3+text4+text5
            Pnt4 = APoint((a4[1][0]-180 + 20) * sc, (a4[1][1]-20) * sc)
            textObj = acad.model.AddMText(Pnt4, 180 * sc, text)
            textObj.StyleName = "STADHLSD"
            textObj.Height = sc * 6

    def OnButton38(self, evt):   #塔外壁展开图
        zhierlist =self.OnButton34_36(True)
        if zhierlist:
            data = []
            for i in zhierlist:
##                print(i)
                data.append([float(i[2]),float(i[3]),i[9],i[8]])
        draw = DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        biaogao=[0]
        for i in data:
            if i[0] not in biaogao:
                biaogao.append(i[0])
        biaogao1,biaogao2=min(biaogao),max(biaogao)
        tawaijing=data[0][2] #取第一个塔外径画竖线，还未考虑塔变径
        x0,y0=draw.base[0],draw.base[1]
        acad,sc=draw.acad,draw.sc
        for i in range(9):
            pt1=APoint(x0+i*45/360*tawaijing*3.1415926,y0)
            pt2=APoint(x0+i*45/360*tawaijing*3.1415926,y0+biaogao2)
            LineObj = acad.model.AddLine(pt1, pt2) #绘制竖直点划线
            LineObj.Linetype = 'DASHDOT-M'
            LineObj.Color = 1
            TextObj = acad.model.AddText(str(i*45) + '%%d', APoint(0, 0), 4 * sc)  #写竖直线角度
            TextObj.Color = 2
            TextObj.Alignment = 4
            TextObj.TextAlignmentPoint = pt1-APoint(0, 4*sc)
        for i in biaogao:
            pt1=APoint(x0-10*sc,y0+i)
            pt2=APoint(x0+tawaijing*3.1415926+10*sc,y0+i)
            LineObj = acad.model.AddLine(pt1, pt2) #绘制水平点划线
            LineObj.Linetype = 'DASHDOT-M'
            LineObj.Color = 1
            TextObj = acad.model.AddText('EL'+str(i), APoint(0, 0), 4 * sc)
            TextObj.Color = 2
            TextObj.Alignment = 1
            TextObj.TextAlignmentPoint = pt2+APoint(0, 2*sc)
        for i in data:
            draw.DrawTieban(biaogao=i[0],fangwei=i[1],tawaijing=i[2],tiebantype=i[3])      

    def OnButton35(self, evt):   #材料表
        zhierlist =self.OnButton34_36(True)
        if zhierlist:
            zhichengliang_name_num=[]  #数据格式为[['名称',数量],[]...
            name,name1=[],[]
            for i in zhierlist:
                name.append(i[0])
            for i in name:
                if i not in name1:
                    name1.append(i)
                    zhichengliang_name_num.append([i,name.count(i)])
        m_shugan=self.cal.m_shugan
        m_hulonggu=self.cal.m_hulonggu
        m_tagun=self.cal.m_tagun
        m_tiliang=self.cal.m_tiliang
        m_langanver=self.cal.m_langanver
        m_langanhor=self.cal.m_langanhor
        m_hushou=self.cal.m_hushou
        m_huawenban=self.cal.m_huawenban
        m_jiaqiangjin=self.cal.m_jiaqiangjin
        m_bianliang=self.cal.m_bianliang
        m_anquanmen=self.cal.m_anquanmen
        
        tizi=[
         ['梯梁 ∠63×6 L='+str(m_tiliang),'Q235B','1','',str(int(m_tiliang/100*5.72)/10)],
         ['踏棍 %%c20','Q235B',str(m_tagun),'1.20',str(int(m_tagun*12)/10)],
         ['护笼箍 50×5 L='+str(m_hulonggu),'Q235B','1','',str(int(m_hulonggu/100*1.9625)/10)],
         ['竖杆 40×5 L='+str(m_shugan),'Q235B','1','',str(int(m_shugan/100*1.57)/10)],
         ]
        num=0 #梯子用螺栓个数
        for i in zhichengliang_name_num:
            if "U型支撑 100x10" == i[0]:
                tizi.append(["U型支撑 100x10",'Q235B',str(i[1]),'7.10',str(int(i[1]*71)/10)])
                num+=i[1]
            if "U型支撑 120x10" == i[0]:
                tizi.append(["U型支撑 120x10",'Q235B',str(i[1]),'8.50',str(int(i[1]*85)/10)])
                num+=i[1]
        num*=2
        tizi.append(['安全门栏','Q235B',str(m_anquanmen),'27',str(int(m_anquanmen*270)/10)])
        tizi.append(['螺栓 M16×50','8.8',str(num),'--','--'])
        tizi.append(['螺母 M16','8',str(num),'--','--'])
        weight=[
              ['-8y',24.8],
              ['-8',12.2],
              ['-10y',27.7],
              ['-10',22.2],
              ['-12',25.1],
              ['-15',51.0],
              ['-20',73.5],
              ]
        pingtai=[]
        zhichengliang1=[]
        zhichengliang2=[]
        num20=0 #托架用M20螺栓个数
        num16=0 #托架用M16螺栓个数
        for i in zhichengliang_name_num:
            danzhong=26.2
            for j in weight:
                if j[0] in i[0]:
                    danzhong=j[1]
            if ('CTJ-15-2' in i[0]) or ('CTJs-15-2' in i[0]) or ('CTJ-20' in i[0]) or('CTJs-20' in i[0]):
                num20+=4*i[1]
                zhichengliang1.append([i[0],'Q235B',str(i[1]),str(danzhong),str(int(i[1]*danzhong*10)/10)])
            else:
                if 'U型' not in i[0]:  #剔除U型板，已经在梯子中统计过了
                    num16+=4*i[1]
                    zhichengliang2.append([i[0],'Q235B',str(i[1]),str(danzhong),str(int(i[1]*danzhong*10)/10)])
        pingtai+=zhichengliang1
        if num20 !=0:
            pingtai.append(['螺栓 M20×50','8.8',str(num20),'--','--'])
            pingtai.append(['螺母 M20','8',str(num20),'--','--'])
        pingtai+=zhichengliang2
        if num16 !=0:
            pingtai.append(['螺栓 M16×50','8.8',str(num16),'--','--'])
            pingtai.append(['螺母 M16','8',str(num16),'--','--'])
        pingtai+=[
            ['边梁 ∠100×80×6 L='+str(m_bianliang),'Q235B','1','',str(int(m_bianliang/100*8.35)/10)],
            ['加强筋 60×6 L='+str(m_jiaqiangjin),'Q235B','1','',str(int(m_jiaqiangjin/100*2.826)/10)],
            ['6mm花纹钢板 '+str(int(m_huawenban/10)/10)+'平方米','Q235B','1','',str(int(m_huawenban/10*47.1)/10)],
            ]
        langan=[
         ['扶手 38×2.5 L='+str(m_hushou),'Q235B','1','',str(int(m_hushou/100*2.189)/10)],
         ['横杆 30×4 L='+str(m_langanhor),'Q235B','1','',str(int(m_langanhor/100*0.942)/10)],
         ['立柱 ∠50×5 L='+str(m_langanver),'Q235B','1','',str(int(m_langanver/100*3.77)/10)],
         ]
        wei=0
        for i in tizi+pingtai+langan:
##            print(i)
            if i[4] not in ['--','-',' ','']:
                wei+=float(i[4])
            i.append('')
            
        print('梯子平台总重量:',('%.0f' % wei),'Kg')
        datahead=['规格','材料','数量','单重','总重','备 注']
        loc=[0,60,90,103,116,129,165]   #表列的位置
        lot=[22,12,4,4,4,12]             #表所能容纳最长字符
        loh0=8                          #表的行高度
        loh1=12                         #表头的行高度
        draw = DrawPlat()
        draw.GetActiveCAD(acad=None, base=-1, sc=self.sc)
        draw.Drawbiao(tizi+pingtai+langan,datahead,loc,lot,loh0,loh1)


    def GetData(self):
        list1 = self.GetLableData()
        list2 = [list1,
                 [self.cb11.GetValue(),
                 self.cb12.GetValue(),
                 self.cb13.GetValue(),
                 self.cb14.GetValue(),]
                 ]
        return list2

    def SetData(self, data):
        self.cb11.SetValue(data[1][0])
        self.cb12.SetValue(data[1][1])
        self.cb13.SetValue(data[1][2])
        self.cb14.SetValue(data[1][3])
        self.SetLableData(data[0])
