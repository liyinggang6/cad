from pyautocad import Autocad, APoint
from math import pi, sin, cos, tan, asin, acos, atan, dist
from math import degrees as rad2deg
from math import radians as deg2rad
from CADDrawing import CADDrawing

class DrawPlat(CADDrawing):
    TiebanType=[                              #梯子平台贴板类型
        [1,'Circle',230],                     #'梯梁支撑', 'U型支撑 100x10', 'TZE-1',
        [2,'Rectangle',[(130,340,170,250),]], #'塔顶托架', 'DTJ', 'DZE',
        [3,'Rectangle',[(130,10,170,260),]],  #'悬臂式托架', 'XTJ', 'XZE',
        [4,'Rectangle',[(130,10,170,260),(130,815,170,235),]],  #'角撑式托架', 'CTJ', 'CZE', '1500',
        [5,'Rectangle',[(130,10,170,260),(130,790,170,260),]],  #保温型'角撑式托架', 'CTJ', 'CZE', '1500',
        [6,'Rectangle',[(130,10,170,260),(130,960,170,251),]],  #'角撑式托架', 'CTJ', 'CZE', '2000',
        [7,'Rectangle',[(130,10,170,260),(130,925,170,281),]],  #保温型'角撑式托架', 'CTJ', 'CZE', '2000',
        [8,'Rectangle',[(40,340,170,250),]], #2s
        [9,'Rectangle',[(40,10,170,260),]],  #3s
        [10,'Rectangle',[(40,10,170,260),(40,815,170,235),]],  #4s
        [11,'Rectangle',[(40,10,170,260),(40,790,170,260),]],  #5s
        [12,'Rectangle',[(40,10,170,260),(40,960,170,251),]],  #6s
        [13,'Rectangle',[(40,10,170,260),(40,925,170,281),]],  #7s     
        ]

    def DrawTieban(self, biaogao,fangwei,tawaijing,tiebantype):
        # 根据标高方位和绘制贴板
        acad, base, sc = self.acad, self.base, self.sc
        base1=APoint(base[0]+tawaijing*3.14159265*fangwei/360, base[1]+biaogao)
        for i in self.TiebanType:
            if tiebantype==i[0]:
                 if i[1]=='Circle':
                     LineObj = acad.model.AddCircle(base1, i[2]/2) #绘制梯子贴板
                     LineObj.Linetype = 'CONTINUOUS' 
                     LineObj.Color = 4
                 if i[1]=='Rectangle':
                     x0,y0=base1[0],base1[1]
                     for j in i[2]:
                         x1,y1,x2,y2=j[0],j[1],j[2],j[3]
                         pt1 = APoint(x0-x1, y0-y1)
                         pt2 = APoint(x0-x1+x2,y0-y1)
                         pt3 = APoint(x0-x1, y0-y1-y2)
                         pt4 = APoint(x0-x1+x2,y0-y1-y2)
                         LineObj = acad.model.AddLine(pt1,pt2)   #绘制平台贴板
                         LineObj.Linetype = 'CONTINUOUS'  # 'CONTINUOUS' 'CENTER' 'DASHDOT-M' 'HIDDEN-M' 'DIVIDE-M'
                         LineObj.Color = 4  # 1红 2黄 3绿 4青 5蓝 6粉 7白
                         LineObj = acad.model.AddLine(pt1,pt3)
                         LineObj.Linetype = 'CONTINUOUS' 
                         LineObj.Color = 4
                         LineObj = acad.model.AddLine(pt2,pt4)
                         LineObj.Linetype = 'CONTINUOUS' 
                         LineObj.Color = 4
                         LineObj = acad.model.AddLine(pt3,pt4)
                         LineObj.Linetype = 'CONTINUOUS' 
                         LineObj.Color = 4
                 break
      
    def DrawVer(self, data, acad=None, base=-1, sc=-1):  # 绘制塔平台立面图
        biaogao = data[0][1]
        prebiaogao = data[0][0]
        Radius1 = data[1][0]  # 塔外半径
        Radius2 = data[1][1]  # 平台内半径
        Radius3 = data[1][2]  # 平台外半径
        Radius4 = Radius3 + 400  # 用于写角度
        Rat = 350  # 梯子护笼半径
        Radius7 = Radius1 + 420 + Rat  # 梯子护笼中心线距离
        fx = data[1][4]  # -1表示左,1表示右
        acad, base, sc = self.GetActiveCAD(acad, base, sc)
        pt1 = APoint(-Radius1, 0) + base
        pt2 = APoint(-Radius1, biaogao - prebiaogao) + base
        LineObj = acad.model.AddLine(pt1, pt2)  # 左塔外壁
        LineObj.Linetype = 'DIVIDE-M'  # 'CONTINUOUS' 'CENTER' 'DASHDOT-M' 'HIDDEN-M' 'DIVIDE-M'
        LineObj.Color = 3  # 1红 2黄 3绿 4青 5蓝 6粉 7白
        pt1 = APoint(Radius1, 0) + base
        pt2 = APoint(Radius1, biaogao - prebiaogao) + base
        LineObj = acad.model.AddLine(pt1, pt2)  # 右塔外壁
        LineObj.Linetype = 'DIVIDE-M'  # 'CONTINUOUS' 'CENTER' 'DASHDOT-M' 'HIDDEN-M' 'DIVIDE-M'
        LineObj.Color = 3  # 1红 2黄 3绿 4青 5蓝 6粉 7白
        gao = biaogao - prebiaogao
        zuo = -Radius3
        you = Radius7 + Rat
        pt1 = APoint(zuo * fx, gao) + base
        pt2 = APoint(you * fx, gao) + base
        LineObj = acad.model.AddLine(pt1, pt2)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        pt3 = APoint(zuo * fx, gao + 400) + base
        pt4 = APoint(you * fx, gao + 400) + base
        LineObj = acad.model.AddLine(pt3, pt4)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        pt5 = APoint(zuo * fx, gao + 800) + base
        pt6 = APoint(you * fx, gao + 800) + base
        LineObj = acad.model.AddLine(pt5, pt6)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        pt7 = APoint(zuo * fx, gao + 1200) + base
        pt8 = APoint(you * fx, gao + 1200) + base
        LineObj = acad.model.AddLine(pt7, pt8)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        gap = 1000  # 栏杆间距
        key = 0
        num = int(2 * pi * Radius3 / gap) + 1
        gap = gap / Radius3  # 栏杆间距角度 弧度
        while True:
            x = -cos(key * gap) * Radius3
            if x > Radius7 - Rat or x > Radius3 - 50:
                break
            else:
                pt1 = APoint(x * fx, gao + 1200) + base
                pt2 = APoint(x * fx, gao) + base
                LineObj = acad.model.AddLine(pt1, pt2)
                LineObj.Linetype = 'CONTINUOUS'
                LineObj.Color = 4
            key += 1
        hren = 2000
        if gao < hren:
            hren = gao
        pt1 = APoint((Radius7 - Rat) * fx, gao + 1350) + base
        pt2 = APoint((Radius7 - Rat) * fx, 300) + base
        LineObj = acad.model.AddLine(pt1, pt2)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        pt1 = APoint((Radius7 - 0.55 * Rat) * fx, gao + 1200) + base
        pt2 = APoint((Radius7 - 0.55 * Rat) * fx, hren) + base
        LineObj = acad.model.AddLine(pt1, pt2)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        pt1 = APoint((Radius7 + 0.55 * Rat) * fx, gao + 1200) + base
        pt2 = APoint((Radius7 + 0.55 * Rat) * fx, hren) + base
        LineObj = acad.model.AddLine(pt1, pt2)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        pt1 = APoint((Radius7 + Rat) * fx, gao + 1200) + base
        pt2 = APoint((Radius7 + Rat) * fx, hren) + base
        LineObj = acad.model.AddLine(pt1, pt2)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 4
        gap = 650
        y = hren
        while y < gao - 100:
            pt1 = APoint((Radius7 - Rat) * fx, y) + base
            pt2 = APoint((Radius7 + Rat) * fx, y) + base
            LineObj = acad.model.AddLine(pt1, pt2)
            LineObj.Linetype = 'CONTINUOUS'
            LineObj.Color = 4
            y += gap
        pt1 = APoint(Radius4 + 10 * sc, gao) + base
        pt2 = APoint(Radius4 + 60 * sc, gao) + base
        pt3 = APoint(Radius4 + 30 * sc, gao + 2 * sc) + base
        LineObj = acad.model.AddLine(pt1, pt2)
        LineObj.Linetype = 'CONTINUOUS'
        LineObj.Color = 7
        TextObj = acad.model.AddText('EL ' + str(biaogao), pt3, 6 * sc)
        TextObj.Color = 7

        def DrawU(hu=100, zhierbiaogao=500):  # 绘制爬梯U型支撑和支耳TZE-1
            linobj = []
            x1, y1 = -50, 0
            x2, y2 = Radius7 - Radius1 - Rat + 50, 0
            x1, x2 = fx * x1, fx * x2
            linobj1 = acad.model.AddLine(APoint(x1, y1), APoint(x2, y2))  # 绘制中心线
            linobj.append(linobj1)
            x1, y1 = 0, 168 / 2
            x2, y2 = 220, 168 / 2
            x1, x2 = fx * x1, fx * x2
            linobj.append(acad.model.AddLine(APoint(x1, y1), APoint(x2, y2)))
            x1, y1 = 0, -168 / 2
            x2, y2 = 220, -168 / 2
            x1, x2 = fx * x1, fx * x2
            linobj.append(acad.model.AddLine(APoint(x1, y1), APoint(x2, y2)))
            x1, y1 = 220, 230 / 2
            x2, y2 = 220, -230 / 2
            x1, x2 = fx * x1, fx * x2
            linobj.append(acad.model.AddLine(APoint(x1, y1), APoint(x2, y2)))
            x1, y1 = 220, hu / 2
            x2, y2 = Radius7 - Radius1 - Rat, hu / 2
            x1, x2 = fx * x1, fx * x2
            linobj.append(acad.model.AddLine(APoint(x1, y1), APoint(x2, y2)))
            x1, y1 = 220, -hu / 2
            x2, y2 = Radius7 - Radius1 - Rat, -hu / 2
            x1, x2 = fx * x1, fx * x2
            linobj.append(acad.model.AddLine(APoint(x1, y1), APoint(x2, y2)))
            base7 = base + APoint(fx * Radius1, zhierbiaogao - prebiaogao)
            for i in linobj:
                i.Move(APoint(0, 0), base7)
                i.Linetype = 'CONTINUOUS'
                i.Color = 4
            linobj1.Linetype = 'DASHDOT-M'
            linobj1.Color = 1

        for i in data[3][0]:
            DrawU(hu=100, zhierbiaogao=i)
        for i in data[3][1]:
            DrawU(hu=120, zhierbiaogao=i)

    def DrawHor(self, data, acad=None, base=-1, sc=-1):  # 绘制塔平台平面图
        biaogao = data[0][1]
        prebiaogao = data[0][0]
        Radius1 = data[1][0]  # 塔外半径
        Radius2 = data[1][1]  # 平台内半径
        Radius3 = data[1][2]  # 平台外半径
        Radius4 = Radius3 + 10*sc  # 用于写角度
        Rat = 350  # 梯子护笼半径
        Radius7 = Radius1 + 420 + Rat  # 梯子护笼中心线距离
        acad, base, sc = self.GetActiveCAD(acad, base, sc)
        cad_obj = []
        LineObj = acad.model.AddCircle(APoint(0, 0), Radius1) #绘制塔外壁
        LineObj.Linetype = 'DIVIDE-M'
        LineObj.Color = 3
        cad_obj.append(LineObj)
        pt1 = APoint(-Radius4, 0)
        pt2 = APoint(Radius4, 0)
        LineObj = acad.model.AddLine(pt1, pt2) #绘制水平中心线
        LineObj.Linetype = 'DASHDOT-M'
        LineObj.Color = 1
        cad_obj.append(LineObj)
        pt1 = APoint(0, -Radius4)
        pt2 = APoint(0, Radius4)
        LineObj = acad.model.AddLine(pt1, pt2) #绘制垂直中心线
        LineObj.Linetype = 'DASHDOT-M'
        LineObj.Color = 1
        cad_obj.append(LineObj)
        for i1 in data[2]:
            if len(i1) >= 2:
                j1, j2 = deg2rad(450 - i1[-1]), deg2rad(450 - i1[0])
                LineObj = acad.model.AddArc(APoint(0, 0), Radius2, j1, j2)  #绘制平台内边线
                LineObj.Linetype = 'CONTINUOUS'
                LineObj.Color = 4
                cad_obj.append(LineObj)
                LineObj = acad.model.AddArc(APoint(0, 0), Radius3, j1, j2) #绘制平台外边线
                LineObj.Linetype = 'CONTINUOUS'
                LineObj.Color = 4
                cad_obj.append(LineObj)
                pmid = []
                for i2 in i1:
                    tcta = deg2rad(450 - i2)
                    p01 = APoint(Radius1 * cos(tcta), Radius1 * sin(tcta))
                    p02 = APoint(Radius2 * cos(tcta), Radius2 * sin(tcta))
                    p03 = APoint(Radius3 * cos(tcta), Radius3 * sin(tcta))
                    pmid.append((p02 + p03) / 2)
                    if i2 % 90 == 0:
                        Radius4 = 1.06 * Radius4
                    p04 = APoint(Radius4 * cos(tcta), Radius4 * sin(tcta))
                    if Radius1 < Radius2:
                        LineObj = acad.model.AddLine(p01, p02)
                        LineObj.Linetype = 'CONTINUOUS'
                        LineObj.Color = 4
                        cad_obj.append(LineObj)
                    LineObj = acad.model.AddLine(p02, p03)
                    if i2 == i1[0] or i2 == i1[-1]:
                        LineObj.Linetype = 'CONTINUOUS'
                        LineObj.Color = 4
                    else:
                        LineObj.Linetype = 'HIDDEN-M'
                        LineObj.Color = 6
                    cad_obj.append(LineObj)
                    TextObj = acad.model.AddText(str(i2) + '%%d', APoint(0, 0), 4 * sc)  #写托架角度
                    TextObj.Alignment = 4
                    TextObj.TextAlignmentPoint = p04
                    cad_obj.append(TextObj)
                    if i2 == i1[0]:
                        fy = -1
                    else:
                        fy = 1
                    p01 = APoint(Radius3 - 220, (50 + 70) * fy)
                    p02 = APoint(Radius3 - 220, 50 * fy)
                    p03 = APoint(Radius3 - 60, 50 * fy)
                    p04 = APoint(Radius3 - 60, (50 + 70) * fy)
                    LineObj = acad.model.AddLine(p01, p02)  #绘制槽钢符号
                    LineObj.Rotate(APoint(0, 0), tcta)
                    LineObj.Linetype = 'CONTINUOUS'
                    LineObj.Color = 7
                    cad_obj.append(LineObj)
                    LineObj = acad.model.AddLine(p02, p03)  #绘制槽钢符号
                    LineObj.Rotate(APoint(0, 0), tcta)
                    LineObj.Linetype = 'CONTINUOUS'
                    LineObj.Color = 7
                    cad_obj.append(LineObj)
                    LineObj = acad.model.AddLine(p03, p04)  #绘制槽钢符号
                    LineObj.Rotate(APoint(0, 0), tcta)
                    LineObj.Linetype = 'CONTINUOUS'
                    LineObj.Color = 7
                    cad_obj.append(LineObj)
                p01 = pmid[0]
                if Radius1 < Radius2:
                    for j in range(len(pmid) - 1):
                        p02 = pmid[j + 1]
                        LineObj = acad.model.AddLine(p01, p02) #绘制加强筋
                        LineObj.Linetype = 'HIDDEN-M'
                        LineObj.Color = 6
                        cad_obj.append(LineObj)
                        p01 = p02
                
        p04 = APoint(0, Radius4 + 15*sc)
        TextObj = acad.model.AddText('EL' + str(biaogao), APoint(0,0), 6 * sc)  #写塔平台标高
        TextObj.Color = 7
        TextObj.Alignment = 4
        TextObj.TextAlignmentPoint = p04
        cad_obj.append(TextObj)
        bta0 = data[1][3]
        alf7 = deg2rad(450 - bta0)
        base7 = APoint((Radius7) * cos(alf7), (Radius7) * sin(alf7))
        La = 225
        j1, j2 = pi + asin(La / Rat), pi - asin(La / Rat)
        linobj = []
        linobj.append(acad.model.AddArc(APoint(0, 0), Rat, j1, j2))  #绘制护笼
        pt = [
            APoint(Rat * cos(j1), La),
            APoint(-500, La),
            APoint(Rat * cos(j1), -La),
            APoint(-500, -La),
            APoint(-Rat, La),
            APoint(-Rat, -La),
            APoint(-Radius1 - 420 - 350, 0),
            APoint(Radius4 - Radius1 - 420 - 350 - 100, 0),
        ]
        linobj.append(acad.model.AddLine(pt[0], pt[1]))  #绘制护笼
        linobj.append(acad.model.AddLine(pt[2], pt[3]))  #绘制护笼
        linobj.append(acad.model.AddLine(pt[4], pt[5]))  #绘制护笼
        for i in linobj:
            i.Linetype = 'CONTINUOUS'
            i.Color = 4
        if bta0 % 90 != 0:
            linobj1 = acad.model.AddLine(pt[6], pt[7])    #绘梯子中心线
            linobj1.Linetype = 'DASHDOT-M'
            linobj1.Color = 1
            linobj.append(linobj1)
        for i in linobj:
            i.Rotate(APoint(0, 0), alf7)
            i.Move(APoint(0, 0), base7)
            cad_obj.append(i)
        p04 = APoint(Radius4 * 1.06 * cos(alf7), Radius4 * 1.06 * sin(alf7))
        TextObj = acad.model.AddText(str(bta0) + '%%d', APoint(0, 0), 4 * sc)  #写梯子中心线角度
        TextObj.Color = 7
        TextObj.Alignment = 4
        TextObj.TextAlignmentPoint = p04
        cad_obj.append(TextObj)
        for j in cad_obj:
            j.Move(APoint(0, 0), base)

    def DrawHorF(self,data):   #根据data数据绘制卧式平台立面图
        data1=[10000, 8900, 7600, 7000, 2024, 4000, 30, 900 , 100, 200, 500, 4200]
        # 0平台标高，1中心标高，2底板标高，3起步标高，4设备外径，5切线长度，6保温厚度，
        # 7W1,8W1',9距左切线，10内边线距中心,11平台长度
        acad, base, sc = self.acad, self.base, self.sc
        base1=self.add(base,(-data[5]/2,data[1]-data[3],0))
        obj=[]
        obj+=self.drawEllipse(a=data[4]/2,b=data[4]/4,rt=0.345,
                         base=base1,rot=(-1,0,0),acad=acad)

        obj+=self.drawEllipse(a=data[4]/2+data[6],b=data[4]/4+data[6],rt=0.345,
                         base=base1,rot=(-1,0,0),acad=acad)

        base1=self.add(base,(data[5]/2,data[1]-data[3],0))
        obj+=self.drawEllipse(a=data[4]/2,b=data[4]/4,rt=0.345,
                         base=base1,rot=(1,0,0),acad=acad)

        obj+=self.drawEllipse(a=data[4]/2+data[6],b=data[4]/4+data[6],rt=0.345,
                         base=base1,rot=(1,0,0),acad=acad)
        pt1=APoint(base[0]-data[5]/2,base[1]+data[1]-data[3]-data[4]/2-data[6])
        pt2=APoint(base[0]+data[5]/2,base[1]+data[1]-data[3]-data[4]/2-data[6])
        obj.append(acad.model.AddLine(pt1,pt2))
        pt3=APoint(base[0]-data[5]/2,base[1]+data[1]-data[3]-data[4]/2)
        pt4=APoint(base[0]+data[5]/2,base[1]+data[1]-data[3]-data[4]/2)
        obj.append(acad.model.AddLine(pt3,pt4))
        pt5=APoint(base[0]-data[5]/2,base[1]+data[1]-data[3]+data[4]/2)
        pt6=APoint(base[0]+data[5]/2,base[1]+data[1]-data[3]+data[4]/2)
        obj.append(acad.model.AddLine(pt5,pt6))
        pt7=APoint(base[0]-data[5]/2,base[1]+data[1]-data[3]+data[4]/2+data[6])
        pt8=APoint(base[0]+data[5]/2,base[1]+data[1]-data[3]+data[4]/2+data[6])
        obj.append(acad.model.AddLine(pt7,pt8))
        L1=data[5] #切线长度
        L2=int(0.7*L1) #鞍座间距
        L3=int(min(0.2*L1,500,data[4]/6)) #鞍座基础厚度
        L4=int(L3*0.8)  #鞍座底板宽度
        L5=int(L3*0.9)  #鞍座垫板宽度
        h1=data[2]-data[3]
        h2=data[1]-data[2]-data[4]/2
        p1=APoint(base[0]-L1/2,base[1])
        p2=APoint(base[0]-L2/2-L3/2,base[1])
        p3=APoint(base[0]-L2/2-L3/2,base[1]+h1)
        p4=APoint(base[0]-L2/2+L3/2,base[1]+h1)
        p5=APoint(base[0]-L2/2+L3/2,base[1])
        p6=APoint(base[0]+L2/2-L3/2,base[1])
        p7=APoint(base[0]+L2/2-L3/2,base[1]+h1)
        p8=APoint(base[0]+L2/2+L3/2,base[1]+h1)
        p9=APoint(base[0]+L2/2+L3/2,base[1])
        p10=APoint(base[0]+L1/2,base[1])
        p11=APoint(base[0]-L2/2-L4/2,base[1]+h1)
        p12=APoint(base[0]-L2/2-L4/2,base[1]+h1+h2)
        p13=APoint(base[0]-L2/2+L4/2,base[1]+h1)
        p14=APoint(base[0]-L2/2-L4/2+L5,base[1]+h1+h2)
        p15=APoint(base[0]+L2/2+L4/2,base[1]+h1)
        p16=APoint(base[0]+L2/2+L4/2,base[1]+h1+h2)
        p17=APoint(base[0]+L2/2-L4/2,base[1]+h1)
        p18=APoint(base[0]+L2/2+L4/2-L5,base[1]+h1+h2)
        
        obj.append(acad.model.AddLine(p1,p2))
        obj.append(acad.model.AddLine(p2,p3))
        obj.append(acad.model.AddLine(p3,p4))
        obj.append(acad.model.AddLine(p4,p5))
        obj.append(acad.model.AddLine(p5,p6))
        obj.append(acad.model.AddLine(p6,p7))
        obj.append(acad.model.AddLine(p7,p8))
        obj.append(acad.model.AddLine(p8,p9))
        obj.append(acad.model.AddLine(p9,p10))
        obj.append(acad.model.AddLine(p11,p12))
        obj.append(acad.model.AddLine(p13,p14))
        obj.append(acad.model.AddLine(p15,p16))
        obj.append(acad.model.AddLine(p17,p18))
        for i in obj:
            i.Linetype = 'DIVIDE-M'
            i.Color = 3
        obj=[]

        obj.append(acad.model.AddLine(pt3,pt5))
        obj.append(acad.model.AddLine(pt4,pt6))
        pt1=APoint(base[0]-data[5]/2-data[4]/2,base[1]+data[1]-data[3])
        pt2=APoint(base[0]+data[5]/2+data[4]/2,base[1]+data[1]-data[3])
        obj.append(acad.model.AddLine(pt1,pt2))
        for i in obj:
            i.Linetype = 'DASHDOT-M'
            i.Color = 1
#开始画平台栏杆
        L1=data[11]
        n=int(L1/1000)+1 #栏杆格子数
        L2=int(L1/n)  #栏杆间距
        listx=[]
        for i in range(n-1):
            listx.append(i*L2)
        listx.append(L1)
        h2=1235  #栏杆高度
        listy=[0,100,100+400,100+400+400,h2]
        obj=[]
        for x in listx:
            pt1=APoint(base[0]-data[5]/2+data[9]+x,base[1]+data[0]-data[3]+listy[0])
            pt2=APoint(base[0]-data[5]/2+data[9]+x,base[1]+data[0]-data[3]+listy[-1])
            obj.append(acad.model.AddLine(pt1,pt2))
        for y in listy:
            pt1=APoint(base[0]-data[5]/2+data[9]+listx[0],base[1]+data[0]-data[3]+y)
            pt2=APoint(base[0]-data[5]/2+data[9]+listx[-1],base[1]+data[0]-data[3]+y)
            obj.append(acad.model.AddLine(pt1,pt2))
        for i in obj:
            i.Linetype = 'CONTINUOUS'
            i.Color = 4

#开始写标高
        for h in data[0:4]:
            data[5]/2
            pt1 = APoint(-data[5]/2-data[4]-30 * sc, h-data[3]) + base
            pt2 = APoint(-data[5]/2-data[4]+10 * sc, h-data[3]) + base
            pt3 = APoint(-data[5]/2-data[4]-20 * sc, h-data[3]+2*sc) + base
            LineObj = acad.model.AddLine(pt1, pt2)
            LineObj.Linetype = 'CONTINUOUS'
            LineObj.Color = 7
            TextObj = acad.model.AddText('EL ' + str(h), pt3, 6 * sc)
            TextObj.Color = 7
        
#开始画爬梯和护笼
        L1=data[9]-data[5]/2+(n-1)*L2 #梯子中心线距离左封头切线
        h1=data[0]-data[3]
        Lt1=500 #梯梁间距
        Lt2=700 #护笼直径
        p1=APoint(base[0]+L1-Lt1/2,base[1])
        p2=APoint(base[0]+L1+Lt1/2,base[1])
        p3=APoint(base[0]+L1-Lt2/2,base[1]+2000)
        p4=APoint(base[0]+L1+Lt2/2,base[1]+2000)
        p5=APoint(base[0]+L1-Lt1/2,base[1]+h1)
        p6=APoint(base[0]+L1+Lt1/2,base[1]+h1)
        p7=APoint(base[0]+L1-Lt2/2,base[1]+h1+h2)
        p8=APoint(base[0]+L1+Lt2/2,base[1]+h1+h2)
        obj=[]
        obj.append(acad.model.AddLine(p1,p5))
        obj.append(acad.model.AddLine(p5,p7))
        obj.append(acad.model.AddLine(p7,p3))
        obj.append(acad.model.AddLine(p3,p4))
        obj.append(acad.model.AddLine(p4,p8))
        obj.append(acad.model.AddLine(p8,p6))
        obj.append(acad.model.AddLine(p6,p2))
        hh=350
        while hh<h1:
            p1=APoint(base[0]+L1-Lt1/2,base[1]+hh)
            p2=APoint(base[0]+L1+Lt1/2,base[1]+hh)
            obj.append(acad.model.AddLine(p1,p2))
            hh+=300
        hl=int((h1-2000)/(int((h1-2000)/700)+1))
        hh=2000+hl
        while hh<(h1+100):
            p1=APoint(base[0]+L1-Lt2/2,base[1]+hh)
            p2=APoint(base[0]+L1+Lt2/2,base[1]+hh)
            obj.append(acad.model.AddLine(p1,p2))
            hh+=hl
        for i in obj:
            i.Linetype = 'CONTINUOUS'
            i.Color = 4
        p1=APoint(base[0]+L1,base[1]-300)
        p2=APoint(base[0]+L1,base[1]+h1+h2+300)
        obj=acad.model.AddLine(p1,p2)
        obj.Linetype = 'DASHDOT-M'
        obj.Color = 1
        
    def DrawHorL(self,data):   #根据data数据绘制卧式平台左视图
        acad, base, sc = self.acad, self.base, self.sc
        h1=data[0]-data[3]
        h2=1235  #栏杆高度
        h3=data[1]-data[3]
        h4=data[2]-data[3]
        L1=int(data[4]*0.9)  #基础底板长度
        L2=int(data[4]*0.7)  #鞍座底板长度
        L3=data[10]*2
        L4=(data[7]+data[8]+data[10])*2
        pt1=APoint(-L1*1.5, 0) + base
        pt2=APoint(-L1/2, 0) + base
        pt3=APoint(-L1/2, h4) + base
        pt4=APoint(-L2/2, h4) + base
        pt5=APoint(L2/2, h4) + base
        pt6=APoint(L1/2, h4) + base
        pt7=APoint(L1/2, 0) + base
        pt8=APoint(L1, 0) + base
        pt9=APoint(-data[4]/2*cos(30*pi/180), h3-data[4]/2*sin(30*pi/180)) + base
        pt10=APoint(data[4]/2*cos(30*pi/180), h3-data[4]/2*sin(30*pi/180)) + base
        pt11=APoint(0, h3) + base
        obj=[]
#开始画设备轮廓
        obj.append(acad.model.AddLine(pt1,pt2))
        obj.append(acad.model.AddLine(pt2,pt3))
        obj.append(acad.model.AddLine(pt3,pt6))
        obj.append(acad.model.AddLine(pt6,pt7))
        obj.append(acad.model.AddLine(pt7,pt8))
        obj.append(acad.model.AddLine(pt4,pt9))
        obj.append(acad.model.AddLine(pt5,pt10))
        obj.append(acad.model.AddCircle(pt11, data[4]/2))
        obj.append(acad.model.AddCircle(pt11, data[4]/2+data[6]))
        for i in obj:
            i.Linetype = 'DIVIDE-M'
            i.Color = 3
        pt1=APoint(-data[4]/2-data[6]-10*sc, h3) + base
        pt2=APoint(data[4]/2+data[6]+10*sc, h3) + base
        pt3=APoint(0, 1.1*h1) + base
        pt4=APoint(0, -10*sc) + base
        obj=[]
        obj.append(acad.model.AddLine(pt1,pt2))
        obj.append(acad.model.AddLine(pt3,pt4))
        pt1=APoint(-500-L4/2,h1+h2+150)+base
        pt2=APoint(-500-L4/2,2000-150)+base
        obj.append(acad.model.AddLine(pt1,pt2))
        for i in obj:
            i.Linetype = 'DASHDOT-M'
            i.Color = 1
#开始画梯子平台
        obj=[]
        y=h1+h2
        pt11=APoint(-L4/2-850, y) + base
        pt12=APoint(-L3/2, y) + base
        pt13=APoint(L3/2, y) + base
        pt14=APoint(L4/2, y) + base
        obj.append(acad.model.AddLine(pt11,pt12))
        obj.append(acad.model.AddLine(pt13,pt14))
        y=h1+100+400+400
        pt21=APoint(-L4/2-850, y) + base
        pt22=APoint(-L3/2, y) + base
        pt23=APoint(L3/2, y) + base
        pt24=APoint(L4/2, y) + base
        obj.append(acad.model.AddLine(pt21,pt22))
        obj.append(acad.model.AddLine(pt23,pt24))
        y=h1+100+400
        pt21=APoint(-L4/2-850, y) + base
        pt22=APoint(-L3/2, y) + base
        pt23=APoint(L3/2, y) + base
        pt24=APoint(L4/2, y) + base
        obj.append(acad.model.AddLine(pt21,pt22))
        obj.append(acad.model.AddLine(pt23,pt24))
        y=h1+100
        pt31=APoint(-L4/2, y) + base
        pt32=APoint(-L3/2, y) + base
        pt33=APoint(L3/2, y) + base
        pt34=APoint(L4/2, y) + base
        obj.append(acad.model.AddLine(pt31,pt34))
        y=h1
        pt31=APoint(-L4/2, y) + base
        pt32=APoint(-L3/2, y) + base
        pt33=APoint(L3/2, y) + base
        pt34=APoint(L4/2, y) + base
        obj.append(acad.model.AddLine(pt31,pt34))
        obj.append(acad.model.AddLine(pt14,pt34))
        obj.append(acad.model.AddLine(pt13,pt33))
        obj.append(acad.model.AddLine(pt12,pt32))
        pt1=APoint(-L4/2, h1+h2) + base
        obj.append(acad.model.AddLine(pt1,pt31))
        pt1=APoint(-L4/2-150, 0) + base
        pt2=APoint(-L4/2-150, h1+h2) + base
        obj.append(acad.model.AddLine(pt1,pt2))
        pt1=APoint(-L4/2-850, 2000) + base
        obj.append(acad.model.AddLine(pt1,pt11))
        pt2=APoint(-L4/2-150, 2000) + base
        obj.append(acad.model.AddLine(pt1,pt2))
        pt1=pt1+APoint(100,0)
        pt2=pt11+APoint(100,0)
        obj.append(acad.model.AddLine(pt1,pt2))
        pt1=pt1+APoint(150,0)
        pt2=pt2+APoint(150,0)
        obj.append(acad.model.AddLine(pt1,pt2))
        pt1=pt1+APoint(200,0)
        pt2=pt2+APoint(200,0)
        obj.append(acad.model.AddLine(pt1,pt2))
        pt1=pt1+APoint(150,0)
        pt2=pt2+APoint(150,0)
        obj.append(acad.model.AddLine(pt1,pt2))
        hl=int((h1-2000)/(int((h1-2000)/700)+1))
        hh=2000+hl
        while hh<(h1+100):
            p1=APoint(-850-L4/2,hh)+base
            p2=APoint(-150-L4/2,hh)+base
            obj.append(acad.model.AddLine(p1,p2))
            hh+=hl
        for i in obj:
            i.Linetype = 'CONTINUOUS'
            i.Color = 4
#开始写标高
        for h in data[0:4]:
            pt1 = APoint(data[4]+30 * sc, h-data[3]) + base
            pt2 = APoint(data[4]+70 * sc, h-data[3]) + base
            pt3 = APoint(data[4]+40 * sc, h-data[3]+2*sc) + base
            LineObj = acad.model.AddLine(pt1, pt2)
            LineObj.Linetype = 'CONTINUOUS'
            LineObj.Color = 7
            TextObj = acad.model.AddText('EL ' + str(h), pt3, 6 * sc)
            TextObj.Color = 7
            

    def DrawHorT(self,data):   #根据data数据绘制卧式平台俯视图
        acad, base, sc = self.acad, self.base, self.sc
        base1=self.add(base,(-data[5]/2,0,0))
        obj=[]
        obj+=self.drawEllipse(a=data[4]/2,b=data[4]/4,rt=0.345,
                         base=base1,rot=(-1,0,0),acad=acad)

        obj+=self.drawEllipse(a=data[4]/2+data[6],b=data[4]/4+data[6],rt=0.345,
                         base=base1,rot=(-1,0,0),acad=acad)

        base1=self.add(base,(data[5]/2,0,0))
        obj+=self.drawEllipse(a=data[4]/2,b=data[4]/4,rt=0.345,
                         base=base1,rot=(1,0,0),acad=acad)

        obj+=self.drawEllipse(a=data[4]/2+data[6],b=data[4]/4+data[6],rt=0.345,
                         base=base1,rot=(1,0,0),acad=acad)
        pt1=APoint(base[0]-data[5]/2,base[1]-data[4]/2-data[6])
        pt2=APoint(base[0]+data[5]/2,base[1]-data[4]/2-data[6])
        obj.append(acad.model.AddLine(pt1,pt2))
        pt3=APoint(base[0]-data[5]/2,base[1]-data[4]/2)
        pt4=APoint(base[0]+data[5]/2,base[1]-data[4]/2)
        obj.append(acad.model.AddLine(pt3,pt4))
        pt5=APoint(base[0]-data[5]/2,base[1]+data[4]/2)
        pt6=APoint(base[0]+data[5]/2,base[1]+data[4]/2)
        obj.append(acad.model.AddLine(pt5,pt6))
        pt7=APoint(base[0]-data[5]/2,base[1]+data[4]/2+data[6])
        pt8=APoint(base[0]+data[5]/2,base[1]+data[4]/2+data[6])
        obj.append(acad.model.AddLine(pt7,pt8))
        L1=data[5] #切线长度
        L2=int(0.7*L1) #鞍座间距
        L3=int(min(0.2*L1,500,data[4]/6)) #鞍座基础厚度
        L4=int(L3*0.8)  #鞍座底板宽度
        L5=int(data[4]*0.8)  #鞍座底板长度
        p1=APoint(base[0]-L2/2-L4/2,base[1]-L5/2)
        p2=APoint(base[0]-L2/2+L4/2,base[1]-L5/2)
        p3=APoint(base[0]-L2/2-L4/2,base[1]+L5/2)
        p4=APoint(base[0]-L2/2+L4/2,base[1]+L5/2)
        p5=APoint(base[0]+L2/2-L4/2,base[1]-L5/2)
        p6=APoint(base[0]+L2/2+L4/2,base[1]-L5/2)
        p7=APoint(base[0]+L2/2-L4/2,base[1]+L5/2)
        p8=APoint(base[0]+L2/2+L4/2,base[1]+L5/2)
        obj.append(acad.model.AddLine(p1,p2))
        obj.append(acad.model.AddLine(p2,p4))
        obj.append(acad.model.AddLine(p4,p3))
        obj.append(acad.model.AddLine(p3,p1))
        obj.append(acad.model.AddLine(p5,p6))
        obj.append(acad.model.AddLine(p6,p8))
        obj.append(acad.model.AddLine(p8,p7))
        obj.append(acad.model.AddLine(p7,p5))
        for i in obj:
            i.Linetype = 'DIVIDE-M'
            i.Color = 3
        obj=[]
        p1=APoint(base[0]-L2/2,base[1]-L5/2-50)
        p2=APoint(base[0]-L2/2,base[1]+L5/2+50)
        p3=APoint(base[0]+L2/2,base[1]-L5/2-50)
        p4=APoint(base[0]+L2/2,base[1]+L5/2+50)
        p5=APoint(base[0]-data[5]/2-data[4]/2,base[1])
        p6=APoint(base[0]+data[5]/2+data[4]/2,base[1])
        obj.append(acad.model.AddLine(pt3,pt5)) #封头切线
        obj.append(acad.model.AddLine(pt4,pt6)) #封头切线
        obj.append(acad.model.AddLine(p1,p2)) #鞍座中心线
        obj.append(acad.model.AddLine(p3,p4)) #鞍座中心线
        obj.append(acad.model.AddLine(p5,p6)) #设备中心线
        for i in obj:
            i.Linetype = 'DASHDOT-M'
            i.Color = 1
#画完设备轮廓，开始画平台
        L1=data[11] #平台长度
        n=int(L1/1000)+1 #栏杆格子数
        L2=int(L1/n)  #栏杆间距
        L11=data[9]-data[5]/2+(n-1)*L2  #梯子中心线距离中心点
        L6=data[10] #内边线距中心
        L7=data[7]+data[8] #平台宽度
        L12=data[9]   #平台距左切线
        p1=APoint(base[0]-data[5]/2+L12,base[1]+L6)
        p2=APoint(base[0]-data[5]/2+L12,base[1]+L6+L7)
        p3=APoint(base[0]-data[5]/2+L1+L12,base[1]+L6+L7)
        p4=APoint(base[0]-data[5]/2+L1+L12,base[1]+L6)
        p5=APoint(base[0]-data[5]/2+L12,base[1]-L6)
        p6=APoint(base[0]-data[5]/2+L12,base[1]-L6-L7)
        p7=APoint(base[0]-data[5]/2+L1+L12,base[1]-L6-L7)
        p8=APoint(base[0]-data[5]/2+L1+L12,base[1]-L6)
        
        p9=APoint(base[0]-data[5]/2+L12+1000,base[1]-L6)
        p10=APoint(base[0]-data[5]/2+L12+1500,base[1]-L6)
        p11=APoint(base[0]-data[5]/2+L12+1000,base[1]+L6)
        p12=APoint(base[0]-data[5]/2+L12+1500,base[1]+L6)
        p13=(p9+p11)/2
        obj=[]
        obj.append(acad.model.AddLine(p1,p2))
        obj.append(acad.model.AddLine(p2,p3))
        obj.append(acad.model.AddLine(p3,p4))
        obj.append(acad.model.AddLine(p4,p1))
        obj.append(acad.model.AddLine(p5,p6))
        obj.append(acad.model.AddLine(p6,p7))
        obj.append(acad.model.AddLine(p7,p8))
        obj.append(acad.model.AddLine(p8,p5))
        obj.append(acad.model.AddLine(p9,p11))
        obj.append(acad.model.AddLine(p10,p12))
        for i in obj:
            i.Linetype = 'CONTINUOUS'
            i.Color = 4
# 开始画平台虚线
        obj=[]
        obj.append(acad.model.AddLine(p13,p12))
        obj.append(acad.model.AddLine(p13,p10))
        la=int((L1-400)/(int((L1-400)/1200)+1))
        lb=200
        while lb<(L1-200):
            p1=APoint(base[0]-data[5]/2+L12+lb,base[1]-L6-L7)
            p2=APoint(base[0]-data[5]/2+L12+lb,base[1]-L6)
            p3=APoint(base[0]-data[5]/2+L12+lb,base[1]+L6)
            p4=APoint(base[0]-data[5]/2+L12+lb,base[1]+L6+L7)
            obj.append(acad.model.AddLine(p1,p2))
            obj.append(acad.model.AddLine(p3,p4))
            lb+=la
        for i in obj:
            i.Linetype = 'HIDDEN-M'
            i.Color = 6
# 开始画爬梯
        La = 250  #梯子宽度
        Rat = 350 #护笼半径
        j1, j2 = pi + asin(La / Rat), pi - asin(La / Rat)
        obj = []
        obj.append(acad.model.AddArc(APoint(0, 0), Rat, j1, j2))  #绘制护笼
        pt = [
            APoint(Rat * cos(j1), La),
            APoint(-500, La),
            APoint(Rat * cos(j1), -La),
            APoint(-500, -La),
            APoint(-Rat, La),
            APoint(-Rat, -La),
            APoint(-600, 0),
            APoint(450, 0),
            APoint(0, 450),
            APoint(0, -450),
        ]
        obj.append(acad.model.AddLine(pt[0], pt[1]))  #绘制护笼
        obj.append(acad.model.AddLine(pt[2], pt[3]))  #绘制护笼
        obj.append(acad.model.AddLine(pt[4], pt[5]))  #绘制护笼
        for i in obj:
            i.Linetype = 'CONTINUOUS'
            i.Color = 4
        obj1 = acad.model.AddLine(pt[6], pt[7])    #绘梯子中心线
        obj1.Linetype = 'DASHDOT-M'
        obj1.Color = 1
        obj2 = acad.model.AddLine(pt[8], pt[9])    #绘梯子中心线
        obj2.Linetype = 'DASHDOT-M'
        obj2.Color = 1
        obj.append(obj1)
        obj.append(obj2)
        for i in obj:
            i.Rotate(APoint(0, 0), pi/2)
            i.Move(APoint(0, 0), APoint(base[0]+L11, base[1]+L6+L7+500))
            

if __name__ == '__main__':
    draw = DrawPlat()
    draw.GetActiveCAD()
    data=[10500, 8900, 7600, 7000, 2024, 8000, 120, 900 , 100, 200, 500, 8200]
    # 0平台标高，1中心标高，2底板标高，3起步标高，4设备外径，5切线长度，6保温厚度，
    # 7W1,8W1',9距左切线，10内边线距中心,11平台长度
    base=draw.base
    draw.DrawHorF(data)
    draw.base=APoint(base[0]+data[5]+data[4],base[1],base[2])
    draw.DrawHorL(data)   
    draw.base=APoint(base[0],base[1]-data[4]*2,base[2])
    draw.DrawHorT(data)

    # data 数据格式如下：
    # [
    # [上一层平台标高、本层平台标高、梯子起步高(相对于本层)、梯子终止高(相对于本层)]
    # [塔外半径、平台内半径、平台外半径,梯子角度、-1/1(画左面，画右面)]
    # [[托架角度1、角度2、角度3...],[角度1、角度2、角度3...]]
    # [[U型支撑 100×10 标高1、U型支撑 100×10 标高2...],[U型支撑 120×10 标高1、U型支撑 120×10 标高2...]
    # ]
##    data = [
##        [0, 5000, -3700, 130],
##        [2632, 2690, 5090, 90, 1],
##        [[95, 105, 125, 145, 165], [185, 205, 235, 265,295]],
##        [[5450], [450, 3000]]
##    ]
#    draw.DrawVer(data)
#    draw.DrawHor(data)
##    data=[
##        [5000,20,2500,2],[5000,40,2500,3],[5000,60,2500,3],[5000,80,2500,3],[5000,100,2500,3],[5000,120,2500,3],[5000,140,2500,3],
##        [8000,20,2600,2],[8000,40,2600,3],[8000,60,2600,3],[8000,80,2600,3],[8000,100,2600,3],[8000,120,2600,3],[8000,140,2600,3],
##        [12000,20,2600,2],[12000,40,2600,3],[12000,60,2600,3],[12000,80,2600,3],[12000,100,2600,3],[12000,120,2600,3],[12000,140,2600,3],
##        ]
##    draw.GetActiveCAD()
##    biaogao=[0]
##    for i in data:
##        if i[0] not in biaogao:
##            biaogao.append(i[0])
##    biaogao1,biaogao2=min(biaogao),max(biaogao)
##    tawaijing=data[0][2] #取第一个塔外径画竖线，还未考虑塔变径
##    x0,y0=draw.base[0],draw.base[1]
##    acad,sc=draw.acad,draw.sc
##    for i in range(9):
##        pt1=APoint(x0+i*45/360*tawaijing*3.1415926,y0)
##        pt2=APoint(x0+i*45/360*tawaijing*3.1415926,y0+biaogao2)
##        LineObj = acad.model.AddLine(pt1, pt2) #绘制竖直点划线
##        LineObj.Linetype = 'DASHDOT-M'
##        LineObj.Color = 1
##        TextObj = acad.model.AddText(str(i*45) + '%%d', APoint(0, 0), 4 * sc)  #写竖直线角度
##        TextObj.Color = 2
##        TextObj.Alignment = 4
##        TextObj.TextAlignmentPoint = pt1-APoint(0, 4*sc)
##    for i in biaogao:
##        pt1=APoint(x0-10*sc,y0+i)
##        pt2=APoint(x0+tawaijing*3.1415926+10*sc,y0+i)
##        LineObj = acad.model.AddLine(pt1, pt2) #绘制水平点划线
##        LineObj.Linetype = 'DASHDOT-M'
##        LineObj.Color = 1
##        TextObj = acad.model.AddText('EL'+str(i), APoint(0, 0), 4 * sc)
##        TextObj.Color = 2
##        TextObj.Alignment = 1
##        TextObj.TextAlignmentPoint = pt2+APoint(0, 2*sc)
##    for i in data:
##        draw.DrawTieban(biaogao=i[0],fangwei=i[1],tawaijing=i[2],tiebantype=i[3])

            
    
    
