from pyautocad import Autocad,APoint
from math import pi,sin,cos,tan,asin,acos,atan,dist
from math import degrees as rad2deg
from math import radians as deg2rad
class DrawPart():
    def __init__(self,p1=-99,p2=-99): 
        acad = Autocad(create_if_not_exists = True)
        acad.prompt( "欢迎进入华陆科技化工设备智能设计平台......" )
        acad.prompt("ALLpart软件正在 AutoCAD 中绘图...")
        self.acaddoc = acad.ActiveDocument
        self.acadmod = acad.model
        self.p1=(0,0,0)
        self.p2=(0,1,0)
        if p1==-99:
            self.p1=self.acaddoc.Utility.getpoint(APoint(0,0),"请输插入点：")
        else:
            self.p1=p1
        if p2==-99:
            self.p2=self.acaddoc.Utility.getpoint(APoint(self.p1[0],self.p1[1]),"请指明绘制方向：")
            self.p2=(self.p2[0]-self.p1[0],self.p2[1]-self.p1[1],self.p2[2]-self.p1[2])
        else:
           self.p2=p2 
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
    
    def drawEllipse(self,a=1000,b=500,rt=0.345,base=(0,0,0),rot=(0,1,0)):
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
        self.acadmod.AddArc(Center1,r1,ct,pi/2-gama+ct)
        self.acadmod.AddArc(Center2,r2,pi/2-gama+ct,pi/2+gama+ct,)
        self.acadmod.AddArc(Center3,r1,pi/2+gama+ct,pi+ct)

    def draw1201(self,d1=2000,h1=4000,t1=16,base=(0,0,0),rot=(0,1,0)):
        p01=self.rot3d((-d1/2,0,0),(0,1,0),rot)
        p02=self.rot3d((-d1/2,h1,0),(0,1,0),rot)
        p03=self.rot3d((d1/2,0,0),(0,1,0),rot)
        p04=self.rot3d((d1/2,h1,0),(0,1,0),rot)
        p05=self.rot3d((-d1/2-t1,0,0),(0,1,0),rot)
        p06=self.rot3d((-d1/2-t1,h1,0),(0,1,0),rot)
        p07=self.rot3d((d1/2+t1,0,0),(0,1,0),rot)
        p08=self.rot3d((d1/2+t1,h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        p03=APoint(p03[0],p03[1],p03[2])+APoint(base[0],base[1],base[2])
        p04=APoint(p04[0],p04[1],p04[2])+APoint(base[0],base[1],base[2])
        p05=APoint(p05[0],p05[1],p05[2])+APoint(base[0],base[1],base[2])
        p06=APoint(p06[0],p06[1],p06[2])+APoint(base[0],base[1],base[2])
        p07=APoint(p07[0],p07[1],p07[2])+APoint(base[0],base[1],base[2])
        p08=APoint(p08[0],p08[1],p08[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        self.acadmod.AddLine(p03,p04)
        self.acadmod.AddLine(p05,p06)
        self.acadmod.AddLine(p07,p08)
        self.acadmod.AddLine(p05,p07)

    def draw1202(self,d1=2000,h1=4000,t1=16,t2=4,base=(0,0,0),rot=(0,1,0)):
        p01=self.rot3d((-d1/2,0,0),(0,1,0),rot)
        p02=self.rot3d((-d1/2,h1,0),(0,1,0),rot)
        p03=self.rot3d((d1/2,0,0),(0,1,0),rot)
        p04=self.rot3d((d1/2,h1,0),(0,1,0),rot)
        p05=self.rot3d((-d1/2-t2,0,0),(0,1,0),rot)
        p06=self.rot3d((-d1/2-t2,h1,0),(0,1,0),rot)
        p07=self.rot3d((d1/2+t2,0,0),(0,1,0),rot)
        p08=self.rot3d((d1/2+t2,h1,0),(0,1,0),rot)
        p09=self.rot3d((-d1/2-t2-t1,0,0),(0,1,0),rot)
        p10=self.rot3d((-d1/2-t2-t1,h1,0),(0,1,0),rot)
        p11=self.rot3d((d1/2+t2+t1,0,0),(0,1,0),rot)
        p12=self.rot3d((d1/2+t2+t1,h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        p03=APoint(p03[0],p03[1],p03[2])+APoint(base[0],base[1],base[2])
        p04=APoint(p04[0],p04[1],p04[2])+APoint(base[0],base[1],base[2])
        p05=APoint(p05[0],p05[1],p05[2])+APoint(base[0],base[1],base[2])
        p06=APoint(p06[0],p06[1],p06[2])+APoint(base[0],base[1],base[2])
        p07=APoint(p07[0],p07[1],p07[2])+APoint(base[0],base[1],base[2])
        p08=APoint(p08[0],p08[1],p08[2])+APoint(base[0],base[1],base[2])
        p09=APoint(p09[0],p09[1],p09[2])+APoint(base[0],base[1],base[2])
        p10=APoint(p10[0],p10[1],p10[2])+APoint(base[0],base[1],base[2])
        p11=APoint(p11[0],p11[1],p11[2])+APoint(base[0],base[1],base[2])
        p12=APoint(p12[0],p12[1],p12[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        self.acadmod.AddLine(p03,p04)
        self.acadmod.AddLine(p05,p06)
        self.acadmod.AddLine(p07,p08)
        self.acadmod.AddLine(p09,p10)
        self.acadmod.AddLine(p11,p12)
        self.acadmod.AddLine(p09,p11)

    def draw1203(self,d1=2000,d2=1000,h1=4000,t1=16,base=(0,0,0),rot=(0,1,0)):
        y=(d1-d2)/2
        x=h1
        r=(x**2+y**2)**0.5
        t1=t1/(x/r)
        p01=self.rot3d((-d1/2,0,0),(0,1,0),rot)
        p02=self.rot3d((-d2/2,h1,0),(0,1,0),rot)
        p03=self.rot3d((d1/2,0,0),(0,1,0),rot)
        p04=self.rot3d((d2/2,h1,0),(0,1,0),rot)
        p05=self.rot3d((-d1/2-t1,0,0),(0,1,0),rot)
        p06=self.rot3d((-d2/2-t1,h1,0),(0,1,0),rot)
        p07=self.rot3d((d1/2+t1,0,0),(0,1,0),rot)
        p08=self.rot3d((d2/2+t1,h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        p03=APoint(p03[0],p03[1],p03[2])+APoint(base[0],base[1],base[2])
        p04=APoint(p04[0],p04[1],p04[2])+APoint(base[0],base[1],base[2])
        p05=APoint(p05[0],p05[1],p05[2])+APoint(base[0],base[1],base[2])
        p06=APoint(p06[0],p06[1],p06[2])+APoint(base[0],base[1],base[2])
        p07=APoint(p07[0],p07[1],p07[2])+APoint(base[0],base[1],base[2])
        p08=APoint(p08[0],p08[1],p08[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        self.acadmod.AddLine(p03,p04)
        self.acadmod.AddLine(p05,p06)
        self.acadmod.AddLine(p07,p08)
        self.acadmod.AddLine(p05,p07)

    def draw1204(self,d1=2000,d2=1000,h1=4000,t1=16,t2=4,base=(0,0,0),rot=(0,1,0)):
        y=(d1-d2)/2
        x=h1
        r=(x**2+y**2)**0.5
        t1=t1/(x/r)
        t2=t2/(x/r)
        p01=self.rot3d((-d1/2,0,0),(0,1,0),rot)
        p02=self.rot3d((-d2/2,h1,0),(0,1,0),rot)
        p03=self.rot3d((d1/2,0,0),(0,1,0),rot)
        p04=self.rot3d((d2/2,h1,0),(0,1,0),rot)
        p05=self.rot3d((-d1/2-t2,0,0),(0,1,0),rot)
        p06=self.rot3d((-d2/2-t2,h1,0),(0,1,0),rot)
        p07=self.rot3d((d1/2+t2,0,0),(0,1,0),rot)
        p08=self.rot3d((d2/2+t2,h1,0),(0,1,0),rot)
        p09=self.rot3d((-d1/2-t2-t1,0,0),(0,1,0),rot)
        p10=self.rot3d((-d2/2-t2-t1,h1,0),(0,1,0),rot)
        p11=self.rot3d((d1/2+t2+t1,0,0),(0,1,0),rot)
        p12=self.rot3d((d2/2+t2+t1,h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        p03=APoint(p03[0],p03[1],p03[2])+APoint(base[0],base[1],base[2])
        p04=APoint(p04[0],p04[1],p04[2])+APoint(base[0],base[1],base[2])
        p05=APoint(p05[0],p05[1],p05[2])+APoint(base[0],base[1],base[2])
        p06=APoint(p06[0],p06[1],p06[2])+APoint(base[0],base[1],base[2])
        p07=APoint(p07[0],p07[1],p07[2])+APoint(base[0],base[1],base[2])
        p08=APoint(p08[0],p08[1],p08[2])+APoint(base[0],base[1],base[2])
        p09=APoint(p09[0],p09[1],p09[2])+APoint(base[0],base[1],base[2])
        p10=APoint(p10[0],p10[1],p10[2])+APoint(base[0],base[1],base[2])
        p11=APoint(p11[0],p11[1],p11[2])+APoint(base[0],base[1],base[2])
        p12=APoint(p12[0],p12[1],p12[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        self.acadmod.AddLine(p03,p04)
        self.acadmod.AddLine(p05,p06)
        self.acadmod.AddLine(p07,p08)
        self.acadmod.AddLine(p09,p10)
        self.acadmod.AddLine(p11,p12)
        self.acadmod.AddLine(p09,p11)

    def draw1206(self,d1=2000,h1=40,t1=16,base=(0,0,0),rot=(0,1,0)):
        a=0.5*d1
        b=0.25*d1
        self.drawEllipse(a,b,rt=0.345,base=base,rot=rot)
        p01=self.rot3d((-a,0,0),(0,1,0),rot)
        p02=self.rot3d((-a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        p01=self.rot3d((a,0,0),(0,1,0),rot)
        p02=self.rot3d((a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        a=0.5*d1+t1
        b=0.25*d1+t1
        self.drawEllipse(a,b,rt=0.345,base=base,rot=rot)
        p01=self.rot3d((-a,0,0),(0,1,0),rot)
        p02=self.rot3d((-a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        p01=self.rot3d((a,0,0),(0,1,0),rot)
        p02=self.rot3d((a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)

    def draw1207(self,d1=2000,h1=40,t1=16,t2=4,base=(0,0,0),rot=(0,1,0)):
        a=0.5*d1
        b=0.25*d1
        self.drawEllipse(a,b,rt=0.345,base=base,rot=rot)
        p01=self.rot3d((-a,0,0),(0,1,0),rot)
        p02=self.rot3d((-a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        p01=self.rot3d((a,0,0),(0,1,0),rot)
        p02=self.rot3d((a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        a=0.5*d1+t2
        b=0.25*d1+t2
        self.drawEllipse(a,b,rt=0.345,base=base,rot=rot)
        p01=self.rot3d((-a,0,0),(0,1,0),rot)
        p02=self.rot3d((-a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        p01=self.rot3d((a,0,0),(0,1,0),rot)
        p02=self.rot3d((a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        a=0.5*d1+t2+t1
        b=0.25*d1+t2+t1
        self.drawEllipse(a,b,rt=0.345,base=base,rot=rot)
        p01=self.rot3d((-a,0,0),(0,1,0),rot)
        p02=self.rot3d((-a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)
        p01=self.rot3d((a,0,0),(0,1,0),rot)
        p02=self.rot3d((a,-h1,0),(0,1,0),rot)
        p01=APoint(p01[0],p01[1],p01[2])+APoint(base[0],base[1],base[2])
        p02=APoint(p02[0],p02[1],p02[2])+APoint(base[0],base[1],base[2])
        self.acadmod.AddLine(p01,p02)  

if __name__ == '__main__':
    draw=Draw()
    base=draw.p1
    rot=draw.p2
    base1=base
    draw.draw1206(2000,40,16,base1,(-rot[0],-rot[1],-rot[2]))
    base1=draw.rot3d((0,40,0),(0,1,0),rot)
    base1=draw.add(base,base1)
    draw.draw1201(2000,3000,16,base1,rot)
    base1=draw.rot3d((0,3040,0),(0,1,0),rot)
    base1=draw.add(base,base1)
    draw.draw1203(2000,1500,2000,16,base1,rot)
    base1=draw.rot3d((0,5040,0),(0,1,0),rot)
    base1=draw.add(base,base1)
    draw.draw1201(1500,2000,16,base1,rot)
    base1=draw.rot3d((0,7065,0),(0,1,0),rot)
    base1=draw.add(base,base1)
    draw.draw1206(1500,25,16,base1,rot)
