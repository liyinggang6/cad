import mayavi.mlab as mlab
from numpy import exp,sin,cos,tan,random,mgrid,ogrid,linspace,sqrt,pi

class Base():
    jingdu=50
    def __init__(self):
        pass
    def Rotxyz(self,x1,y1,z1,rotx,roty,rotz):
        x2=x1*cos(rotz*pi/180)-y1*sin(rotz*pi/180)
        y2=x1*sin(rotz*pi/180)+y1*cos(rotz*pi/180)
        z2=z1
        y3=y2*cos(rotx*pi/180)-z2*sin(rotx*pi/180)
        z3=y2*sin(rotx*pi/180)+z2*cos(rotx*pi/180)
        x3=x2
        z=z3*cos(roty*pi/180)-x3*sin(roty*pi/180)
        x=z3*sin(roty*pi/180)+x3*cos(roty*pi/180)
        y=y2
        return x,y,z
    
    def Circle(self,x1,y1,z1,r1,r2,color,rotx,roty,rotz):
        #以x1,y1,z1为圆心，绘制一个内径为、外径为r2的圆环面
        xt,yt = mgrid[r1:r2:self.jingdu*1j,0:2*pi:self.jingdu*1j]
        x=xt*cos(yt)
        y=xt*sin(yt)
        z=xt*0+yt*0+0
        x,y,z=self.Rotxyz(x,y,z,rotx,roty,rotz)
        x+=x1
        y+=y1
        z+=z1
        mlab.mesh(x,y,z,color=color)

    def Cone(self,x1,y1,z1,r1,r2,h1,yf,color,rotx,roty,rotz):
        #绘制一个底面中心在x1,y1,z1半径为r1,顶面半径为r2的圆锥面,向y方向偏yf
        alf= linspace(0,2*pi,self.jingdu)
        xt1=r1*cos(alf)
        yt1=r1*sin(alf)
        xt2=r2*cos(alf)
        yt2=r2*sin(alf)+yf
        zt1=linspace(z1,z1,self.jingdu)
        zt2=linspace(z1+h1,z1+h1,self.jingdu)
        x=linspace(xt1,xt2,self.jingdu)
        y=linspace(yt1,yt2,self.jingdu)
        z=linspace(zt1,zt2,self.jingdu)
        x,y,z=self.Rotxyz(x,y,z,rotx,roty,rotz)
        x+=x1
        y+=y1
        z+=z1
        mlab.mesh(x,y,z,color=color)
    
    def Rec(self,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4,rotx,roty,rotz):
        #根据4个点绘制四边形 未完待续
        x=[[x1,x2],[x3,x4]]
        y=[[y1,y2],[y3,y4]]
        z=[[z1,z2],[z3,z4]]
        
        #mlab.mesh(x,y,z)

    def Ellip(self,x1,y1,z1,r1,h1,color,rotx,roty,rotz):
        '''绘制凸面'''
        xt,yt = mgrid[0:r1:self.jingdu*1j,0:2*pi:self.jingdu*1j]
        xa=xt*cos(yt)
        ya=xt*sin(yt)
        za=sqrt(abs(1-(xa**2+ya**2)/r1**2))*h1
        xa,ya,za=self.Rotxyz(xa,ya,za,rotx,roty,rotz)
        x=xa+x1
        y=ya+y1
        z=za+z1
        mlab.mesh(x,y,z,color=color)
    
class Box(Base):
    pass
    #根据8点绘制六面体


class Ellip(Base):
#封头  rotx,roty,rotz绕坐标轴旋转，单位角度
    def __init__(self,x1,y1,z1,r1,h1,color,rotx,roty,rotz):
       self.Circle(x1,y1,z1,0,r1,color,rotx,roty,rotz)
       self.Ellip(x1,y1,z1,r1,h1,color,rotx,roty,rotz)

class Cone(Base):
#实心偏锥
    def __init__(self,x1,y1,z1,r1,r2,h1,yf,color,rotx,roty,rotz):
       self.Circle(x1,y1,z1,0,r1,color,rotx,roty,rotz)
       x2,y2,z2=self.Rotxyz(0,yf,h1,rotx,roty,rotz)
       x2+=x1
       y2+=y1
       z2+=z1
       self.Circle(x2,y2,z2,0,r2,color,rotx,roty,rotz)
       self.Cone(x1,y1,z1,r1,r2,h1,yf,color,rotx,roty,rotz)

class CylindderS(Base):
#实心圆柱
    def __init__(self,x1,y1,z1,r1,h1,color,rotx,roty,rotz):
       self.Circle(x1,y1,z1,0,r1,color,rotx,roty,rotz)
       x2,y2,z2=self.Rotxyz(0,0,h1,rotx,roty,rotz)
       x2+=x1
       y2+=y1
       z2+=z1
       self.Circle(x2,y2,z2,0,r1,color,rotx,roty,rotz)
       self.Cone(x1,y1,z1,r1,r1,h1,0,color,rotx,roty,rotz)
       
class CylindderK(Base):
#空心圆柱
    def __init__(self,x1,y1,z1,r1,r2,h1,color,rotx,roty,rotz):
       self.Circle(x1,y1,z1,r1,r2,color,rotx,roty,rotz)
       x2,y2,z2=self.Rotxyz(0,0,h1,rotx,roty,rotz)
       x2+=x1
       y2+=y1
       z2+=z1
       self.Circle(x2,y2,z2,r1,r2,color,rotx,roty,rotz)
       self.Cone(x1,y1,z1,r1,r1,h1,0,color,rotx,roty,rotz)
       self.Cone(x1,y1,z1,r2,r2,h1,0,color,rotx,roty,rotz)
   
if __name__ == '__main__':
    #绘制一个直径带斜锥的釜式设备
   Ellip(x1=0,y1=0,z1=0,r1=1000/2,h1=1000/4,color=(0, 1, 0),rotx=0,roty=-90,rotz=0)
   CylindderS(x1=0,y1=0,z1=0,r1=1000/2,h1=25,color=(0, 1, 0),rotx=0,roty=90,rotz=0)
   CylindderS(x1=25,y1=0,z1=0,r1=1000/2,h1=500,color=(0, 1, 1),rotx=0,roty=90,rotz=0)
   Cone(x1=525,y1=0,z1=0,r1=1000/2,r2=1500/2,h1=1000,yf=250,color=(0, 1, 0),rotx=0,roty=90,rotz=0)
   CylindderK(x1=1525,y1=250,z1=0,r1=1400/2,r2=1500/2,h1=2000,color=(0, 1, 1),rotx=0,roty=90,rotz=0)
   Ellip(x1=3525,y1=250,z1=0,r1=1500/2,h1=1500/4,color=(0, 1, 0),rotx=0,roty=90,rotz=0)
   
    
    

    
    

