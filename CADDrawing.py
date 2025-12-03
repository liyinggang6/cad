from pyautocad import Autocad, APoint
from math import pi,sin,cos,tan,asin,acos,atan,dist
import os
import shutil

class CADDrawing:
    def __init__(self):
        self.acad = Autocad(create_if_not_exists=False)
        self.base = APoint(0, 0)
        self.sc = 1

    def GetActiveCAD(self, acad=None, base=-1, sc=-1):
        if acad == None:
            acad = Autocad(create_if_not_exists=False)
            acad.prompt("欢迎使用华陆化工设备智能设计软件......")
        if base == -1:
            base = acad.ActiveDocument.Utility.getpoint(APoint(0, 0), "请输插入点：")
        base = APoint(base[0], base[1])
        if sc == -1:
            sc = acad.ActiveDocument.Utility.getstring(1, "请输入比例系数:")
            key = 0
            for i in sc:
                if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
                    key += 1
                else:
                    break
            b = sc[:key]
            try:
                sc = float(b)
            except:
                sc = 1.0
        acad.ActiveDocument.SetVariable('LTSCALE', sc)
        self.acad, self.base, self.sc=acad, base, sc
        return acad, base, sc

    def Drawbiao(self,data,datahead,             #绘制和填充表格，插入基点在左下
                 loc=[0,30,60,90,115,140,180],   #表列的位置
                 lot=[9,9,9,8,8,12],             #表所能容纳最长字符
                 loh0=8,loh1=12):                 #表行的高度
        acad, base, sc = self.acad, self.base, self.sc
        num=len(data)
        lineobj=[]
        y=num*loh0+loh1
        for x in loc:
            lineobj.append(acad.model.AddLine(APoint(x,0),APoint(x,y)))
        for i in range(num):
            y=i*loh0
            lineobj.append(acad.model.AddLine(APoint(0,y),APoint(180,y)))
            key=0
            for x in loc[:-1]:
                content=str(data[i][key])
                textObj=acad.model.AddText((content), APoint(x+1,y+1), 4)
                if lot[key] < len(content):
                    textObj.ScaleFactor = 0.7 * lot[key]/len(content)    #文字宽度缩放
                else:
                    textObj.ScaleFactor = 0.7
                lineobj.append(textObj)
                key+=1
        y=num*loh0
        lineobj.append(acad.model.AddLine(APoint(0,y),APoint(180,y)))
        key=0
        for x in loc[:-1]:
            lineobj.append(acad.model.AddText(datahead[key], APoint(x+3,y+3), 4))
            key+=1
        y=num*loh0+loh1
        lineobj.append(acad.model.AddLine(APoint(0,y),APoint(180,y)))
        for i in lineobj:
            i.ScaleEntity(APoint(0,0),sc)
            i.Move(APoint(0,0),base)

    def Drawbiao1(self,data,head='',             #绘制和填充表格,表头靠插入块,插入基点在右上
                 loc=[0,30,60,90,115,140,180],   #表列的位置,loc[-1]为表头的宽度
                 lot=[9,9,9,8,8,12],             #表所能容纳最长字符
                 loh0=8,loh1=12):                #表行的高度 loh1为表头高度
 
        acad, base, sc = self.acad, self.base, self.sc
        obj=[]
        if '.dwg' in head:
            path1 = acad.ActiveDocument.Path  # 文件存放路径C:\Users\xql1806\Documents
            path2 = acad.ActiveDocument.Application.Path  # CAD程序路径 C:\Program Files\AutoCAD 2010
            path3 = os.getcwd()
            sourcePath = path3 + "\\dwg\\"
            targetPath = path1 + "\\"
            shutil.copy(sourcePath + head, targetPath)
            obj.append(acad.model.InsertBlock(APoint(0, 0), head, 1, 1, 1, 0 ))
            os.remove(targetPath + head)
        num=len(data)
        y=num*loh0+loh1
        for x in loc:
            x=-loc[-1]+x
            obj.append(acad.model.AddLine(APoint(x,-y),APoint(x,-loh1)))
        for i in range(num):
            y=-i*loh0-loh0-loh1
            obj.append(acad.model.AddLine(APoint(-loc[-1],y),APoint(0,y)))
            key=0
            for x in loc[:-1]:
                x=-loc[-1]+x
                content=str(data[i][key])
                textObj=acad.model.AddText((content), APoint(x+2,y+2), 4)
                if lot[key] < len(content):
                    textObj.ScaleFactor = 0.7 * lot[key]/len(content)    #文字宽度缩放
                else:
                    textObj.ScaleFactor = 0.7
                obj.append(textObj)
                key+=1
        for i in obj:
            i.ScaleEntity(APoint(0,0),sc)
            i.Move(APoint(0,0),base)
            
    def add(self,p,q):
        changdu=min(len(p),len(q))
        a=[]
        for i in range(changdu):
            a.append(p[i]+q[i])
        return tuple(a)

    def rot3d(self,P,Q1,Q2):
        #Q1旋转到Q2后,P点新坐标 经过深入研究，终于将坐标旋转算法修改正确了。2021.10.14
        #Q2在三维空间时好像有点问题
        x=P[0]
        y=P[1]
        z=P[2]
        Ra=(Q1[0]**2+Q1[1]**2)**0.5
        Rb=(Q1[0]**2+Q1[1]**2+Q1[2]**2)**0.5
        sinct=Q1[1]/Ra
        cosct=Q1[0]/Ra
        x1=x*cosct+y*sinct
        y1=y*cosct-x*sinct
        z1=z
        sinct=Q1[2]/Rb 
        cosct=Ra/Rb    
        x2=x1*cosct+z1*sinct
        z2=z1*cosct-x1*sinct
        y2=y1
        Ra=(Q2[0]**2+Q2[1]**2)**0.5
        Rb=(Q2[0]**2+Q2[1]**2+Q2[2]**2)**0.5
        sinct=Q2[2]/Rb
        cosct=Ra/Rb
        x3=x2*cosct-z2*sinct
        z3=x2*sinct+z2*cosct
        y3=y2
        sinct=Q2[1]/Ra
        cosct=Q2[0]/Ra
        x=x3*cosct-y3*sinct
        y=x3*sinct+y3*cosct
        z=z3
        return (x,y,z)

    def P2Rx0y0z0(self,p1,p2,p3):
        # 根据不共线的空间三点计算圆心坐标和半径
       x1,y1,z1=p1[0],p1[1],p1[2]
       x2,y2,z2=p2[0],p2[1],p2[2]
       x3,y3,z3=p3[0],p3[1],p3[2]
       a1 = (y1*z2 - y2*z1 - y1*z3 + y3*z1 + y2*z3 - y3*z2)
       b1 = -(x1*z2 - x2*z1 - x1*z3 + x3*z1 + x2*z3 - x3*z2)
       c1 = (x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
       d1 = -(x1*y2*z3 - x1*y3*z2 - x2*y1*z3 + x2*y3*z1 + x3*y1*z2 - x3*y2*z1)
       a2 = 2 * (x2 - x1)
       b2 = 2 * (y2 - y1)
       c2 = 2 * (z2 - z1)
       d2 = x1*x1 + y1*y1 + z1*z1 - x2*x2 - y2*y2 - z2*z2
       a3 = 2 * (x3 - x1)
       b3 = 2 * (y3 - y1)
       c3 = 2 * (z3 - z1)
       d3 = x1*x1 + y1*y1 + z1*z1 - x3*x3 - y3*y3 - z3*z3
       cx = -(b1*c2*d3 - b1*c3*d2 - b2*c1*d3 + b2*c3*d1 + b3*c1*d2 - b3*c2*d1)\
             /(a1*b2*c3 - a1*b3*c2 - a2*b1*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1)
       cy =  (a1*c2*d3 - a1*c3*d2 - a2*c1*d3 + a2*c3*d1 + a3*c1*d2 - a3*c2*d1)\
            /(a1*b2*c3 - a1*b3*c2 - a2*b1*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1)
       cz = -(a1*b2*d3 - a1*b3*d2 - a2*b1*d3 + a2*b3*d1 + a3*b1*d2 - a3*b2*d1)\
            /(a1*b2*c3 - a1*b3*c2 - a2*b1*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1)
       r=((cx-x1)**2+(cy-y1)**2+(cz-z1)**2)**0.5
       return (cx,cy,cz),r
    
    def drawEllipse(self,a=1000,b=500,rt=0.345,base=(0,0,0),rot=(0,1,0),acad=None):
        #用三个圆弧绘制类椭圆
        r1=rt*a
        p01=(a-r1,0,0)
        p02=(0,b-r1,0)
        p03=(-a+r1,0,0)
        Center1=self.rot3d(p01,(0,1,0),rot)
        Center2,r2=self.P2Rx0y0z0(p01,p02,p03)
        gama=asin((a-r1)/r2)
        r2=r2+r1
        Center2=self.rot3d(Center2,(0,1,0),rot)
        Center3=self.rot3d(p03,(0,1,0),rot)
        r_rot=(rot[0]**2+rot[1]**2+rot[2]**2)**0.5
        if rot[0]<0:
            ct=acos(rot[1]/r_rot)   #Rot与Y轴(0,1,0)之间的夹角
        else:
            ct=2*pi-acos(rot[1]/r_rot)
        Center1=APoint(Center1[0],Center1[1],Center1[2])+APoint(base[0],base[1],base[2])
        Center2=APoint(Center2[0],Center2[1],Center2[2])+APoint(base[0],base[1],base[2])
        Center3=APoint(Center3[0],Center3[1],Center3[2])+APoint(base[0],base[1],base[2])
        obj1=acad.model.AddArc(Center1,r1,ct,pi/2-gama+ct)
        obj2=acad.model.AddArc(Center2,r2,pi/2-gama+ct,pi/2+gama+ct,)
        obj3=acad.model.AddArc(Center3,r1,pi/2+gama+ct,pi+ct)
        return [obj1,obj2,obj3]


if __name__ == '__main__':
    draw = CADDrawing()
    acad, base, sc=draw.GetActiveCAD()
    data=[['N1','200','123456','123456','123456','123456','123456','123456'],
          ['N2','300','123456','123456','123456','123456','123456','123456']]
    draw.Drawbiao1(data,head='B-管口许用载荷表.dwg',       #绘制和填充表格,表头靠插入块
                 loc=[0,15,30,55,80,105,130,155,180],     #表列的位置
                 lot=[5,5,7,7,7,7,7,7],             #表所能容纳最长字符
                 loh0=8,loh1=76)                          #表行的高度loh1为表头高度
    draw.GetActiveCAD(acad=acad, base=-1, sc=sc)
    data=[['N1','200','CL300','Sch80','HG/T 20615-2009','RF','2000','工艺气进口'],
          ['N2','300','CL300','Sch80','HG/T 20615-2009','RF','2000','工艺气出口']]   
    draw.Drawbiao1(data,head='B-管口表.dwg',       #绘制和填充表格,表头靠插入块
                 loc=[0,15,30,45,60,105,120,135,180],     #表列的位置
                 lot=[5,5,5,5,15,5,5,15],             #表所能容纳最长字符
                 loh0=8,loh1=16)                          #表行的高度loh1为表头高度
