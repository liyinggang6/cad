from math import pi, sin, cos, tan, asin, acos, atan, dist
from math import degrees as rad2deg
from math import radians as deg2rad

class Calculate():
    Kong = [None, "", " ", "  ", "   ", "     ", "      ", ]

    def __init__(self):
        self.m_langanver=0
        self.m_langanhor=0
        self.m_hushou=0
        self.m_huawenban=0
        self.m_jiaqiangjin=0
        self.m_bianliang=0
        self.m_anquanmen=0
    # 初始化时将起步标高和全部梯子平台数据传递过来

    def plat(self, datalist, Ptype):  #将梯子平台界面获取的数据转化成绘图所需要的数据
##        print('data in Calculator.plat is ',datalist)
##        print('Ptype in Calculator.plat is ',Ptype)
        data=datalist[0][1][1]
        biaogao = int(data[1])  # 起步标高
        rest1=[[datalist[0][0],[biaogao,0]]]
        for data1ist1 in datalist[1:]: #跳过data[0]这个基础参数
            data=data1ist1[1][1]
            for i in range(len(data)):
                if data[i] in self.Kong:
                    data[i] = '0'   #将数据中的空值转化成0
            alf=int(data[1])        #托架标准夹角
            dno=int(data[2])        #塔外径
            if data[3]:
                jianxi=250
            else:
                jianxi=150           #塔外径与平台内边线间隙
            biaogao = int(data[4])   # 平台标高
            kuand = int(float(data[5]))  # 平台宽度,不包含顶平台的内伸长度
            ysheng = int(float(data[8]))  # 顶平台的内伸长度
            dn1 = int(float(data[9]) * 2 + 40)  # 顶平台内边线1的直径
            bta0 = float(data[10]) + 7200  # 爬梯所在的方位角 °
            bta1 = float(data[11]) + 7200  # 平台起始方位角 ° 0°在上
            bta2 = float(data[12]) + 7200  # 平台终止方位角 °，方向按顺时针，
            bta0 = bta0 - int(bta0 / 360) * 360
            bta1 = bta1 - int(bta1 / 360) * 360
            bta2 = bta2 - int(bta2 / 360) * 360
            if bta1 == bta2:  # 当起始和终止角度相等时调整起始和终止角度到梯子两侧
                bta1 = bta0 + alf / 2
                bta2 = bta0 - alf / 2
            while bta2 < bta1:
                bta2 += 360
            if (bta0 + 360) > bta1 and (bta0 + 360) < bta2:
                bta0 += 360
            jiaodu1, jiaodu2 = [], []
            bta3, bta4 = 0, 0
            if bta0 > (bta1 + alf / 2 + 2) and bta0 < (bta2 - alf / 2 - 2):
                bta4 = bta2
                bta2 = bta0 - alf / 2
                bta3 = bta0 + alf / 2
                num = int((bta4 - bta3) / alf-999)+999
                gap = (bta4 - bta3) / num
                for i in range(num):
                    jiaodu2.append(bta3+int(i*gap))
                jiaodu2.append(bta4)
            num = int((bta2 - bta1) / alf-999)+999
            gap = (bta2 - bta1) / num
            for i in range(num):
                jiaodu1.append(bta1+int(i*gap))
            jiaodu1.append(bta2)
# 用于储存托架方位，当有跨越360°时，跨越的部分+了360°，因此需要以下程序处理
            for i in range(len(jiaodu1)):
                while jiaodu1[i] >=360:
                    jiaodu1[i]-=360
                if int(jiaodu1[i])==jiaodu1[i]:
                    jiaodu1[i]=int(jiaodu1[i])
                else:
                    jiaodu1[i] = int(jiaodu1[i]*10)/10
            for i in range(len(jiaodu2)):
                while jiaodu2[i] >=360:
                    jiaodu2[i]-=360
                if int(jiaodu2[i])==jiaodu2[i]:
                    jiaodu2[i]=int(jiaodu2[i])
                else:
                    jiaodu2[i] = int(jiaodu2[i]*10)/10
            if int(bta0) == bta0:
                bta0 = int(bta0)
            else:
                bta0 = int(bta0 * 10) / 10
            Radius1 = dno / 2  # 设备外径
            Radius2 = Radius1 + jianxi  # 平台内径
            Radius3 = Radius2 + kuand  # 平台外径
            Radius5 = dn1 / 2
            Radius51 = Radius5 - ysheng
            Radius52 = Radius5 + kuand
            if '塔顶' in data[7]:
                Radius2 = Radius51
                Radius3 = Radius52
            rest1.append([data1ist1[0],[biaogao,bta0,Radius1,Radius2,Radius3],jiaodu1,jiaodu2]) #先得到中间数据，后续继续处理
        rest2=[rest1[0][1][0:2]]   #仅储存标高及梯子方位
        prebta0 = rest1[0][1][1]
        for data in rest1:
            bta0 = data[1][1]
            rest2.append(data[1][0:2])
            if prebta0 == bta0:
                del rest2[-2]
            prebta0=bta0
##        if rest1[0][1][1]==rest1[1][1][1]:  2024.3.1修改了第一层平台梯子不能在0°的bug
##            print('rest1=', rest1)
##            print('rest1[0][1][1]=',rest1[0][1][1])
##            rest.insert(0, rest1[0][1][0:2])
###        print('rest2=', rest2)
        restu100 = []
        restu120 = []
# 11.25增加梯子材料计算
        m_shugan=0
        m_hulonggu=0
        m_tagun=0
        m_tiliang=0
        biaogao1 = rest2[0][0]
        for data in rest2[1:]:
            biaogao2=data[0]
            gao=biaogao2-biaogao1
            num=int((biaogao2-biaogao1-1)/3000)+1
            gap=int((biaogao2-biaogao1)/num)
            for j in range(num):
                restu120.append([biaogao1+450+gap*j,data[1]])
            restu100.append([biaogao2 + 450,data[1]])
            m_shugan+=(gao+1200-2000)*6
            m_hulonggu+=int((gao+1200-2000)/650*700*pi/100)*100
            m_tiliang+=gao*2+1050*2
            biaogao1=biaogao2
        m_tagun=int(m_tiliang/2/300) 
##       print('restu100 =',restu100 ,'restu120 =',restu120 )
        rest3=[]
        biaogao1=rest1[0][1][0]
        bta01=rest1[0][1][1]
        huazuoyou = 1
        for data in rest1[1:]:
            biaogao2 = data[1][0]
            bta02= data[1][1]
            if bta01 != bta02:
                huazuoyou*=-1
            restu100i = []
            restu120i = []
            for j in restu100:
                if j[0] > biaogao1+449 and j[0] <biaogao2+451 and j[1]==data[1][1]:
                    restu100i.append(j[0])
            for j in restu120:
                if j[0] > biaogao1+449 and j[0] <biaogao2+451 and j[1]==data[1][1]:
                    restu120i.append(j[0])
            list1 = [biaogao1, biaogao2, 0, 0]
            list2 = [data[1][2], data[1][3], data[1][4], data[1][1], huazuoyou]
            list3= [list1, list2, [data[2], data[3]], [restu100i.copy(), restu120i.copy()]]
            rest3.append([data[0], list3])
            biaogao1 = biaogao2
            bta01 = bta02
##      print('rest3=',rest3)
        self.m_shugan=m_shugan
        self.m_hulonggu=m_hulonggu
        self.m_tagun=m_tagun
        self.m_tiliang=m_tiliang 
        return rest3 #,m_shugan,m_hulonggu,m_tiliang,m_tagun   #不包含所有梯子平台面板上的数据,2022.11.25增加了梯子材料数据

    def calzhierlist(self, data, Ptype, rest): #传一层平台的数据过来，然后计算支耳表、材料表
##        print('data=',data)
##        print('Ptype=',Ptype)
##        print('rest=',rest)
   
##'''
##需要传入的数据格式如下
##data=['2000＜OD≤3100', '30', '2632', True, '10000', '1000', '1 级，2.0kN/m2', '悬臂式托架  XTJ', '', '', '210', '30', '300']
##
##rest=[
##         [1000, 5000, 0, 0],  上层标高、本层标高
##         [1316.0, 1566.0, 2566.0, 90, -1],  塔外半径,平台内半径,平台外半径,梯子方位，画左右
##         [[30, 52, 75], [105, 130, 155, 180] ],  托架方位
##         [[], [1450, 4450] ]   爬梯支耳标高 U100 U120
##      ]
##'''
##2022.10.8增加计算TiebanType
##2022.11.4增加计算材料表计算
        pi=3.1415926
        ta1=0    #一层多块平台扇形总角度 弧度
        bta1=0
        bta2=0
        for bta in rest[2]:
            if len(bta)>1:
                bta1=bta[0]
                bta2=bta[-1]
                if bta1>bta2:
                    bta2+=360
            ta1+=(bta2-bta1)*pi/180
        alf=float(data[1])
        bta0=float(data[10])
        bta1=float(data[11])
        bta2=float(data[12])
        if bta1>bta2:
                bta2+=360
        if bta0>(bta1+alf/2+5) and bta0<(bta2-alf/2-5):
            m_anquanmen=2
        else:
            m_anquanmen=1
        if '塔顶' in data[7]:
            ta1=2*pi
            m_anquanmen=2
        Radius3=rest[1][2]
        Radius2=rest[1][1]
        La1=ta1*Radius3+(Radius3-Radius2)
        m_langanver=int(La1/990*1250/10)*10
        m_langanhor=int(La1*3*1.1/10)*10
        m_hushou=int(La1*1.1/10)*10
        m_huawenban=int(ta1*(Radius3**2-Radius2**2)/2*1.1/10000)
        m_jiaqiangjin=int((Radius3+Radius2)/2*ta1/10*1.1)*10
        m_bianliang=int((ta1*(Radius3+Radius2)+2*(Radius3-Radius2))*1.1/10)*10
          
        kuand=int(float(data[5]))      #平台宽度,不包含顶平台的内伸长度
        if data[8] in self.Kong:
            ysheng=0
        else:
            ysheng=int(float(data[8]))     #顶平台的内伸长度
        if data[9] in (self.Kong+[0,'0']):
            L1='--'
        else:
            L1=data[9]       #L1   
        biaogao=data[4]      #平台标高
        if data[3]:
            t1='b'
        else:
            t1=''
        t2='-'+str(int(float(data[5])/100))
        if '塔顶' in data[7]:
            t3=''
            if ysheng>0:
                t6='y(y='+data[8]+')'
            else:
                t6=''
        else:
            t3='-'+data[6][:1]
            t6=''  
        t4=data[7][-3:]
        for i in Ptype:
            if i[0]==data[7].split('  ')[0]:
                t7=i[2]
        zhichengliang=[]
        if rest[2][0] !=[]:
            for i in range(len(rest[2][0])):
                if i==0:
                    t5='s'
                else:
                    t5=''
                tj=t4+t5+t2+t3+t1+t6  #托架标注
                zr=t7+t5+t2+t3+t1     #支耳标注
                # ['托架型号','支耳型号','标高 (mm)','角  度α(°)','L1 (mm)','L2 (mm)','备 注']
                zhichengliang.append([tj,zr,biaogao,str(rest[2][0][i]),L1,'--',' ',data[5]])
        if rest[2][1] !=[]:
            for i in range(len(rest[2][1])):
                if i==0:
                    t5='s'
                else:
                    t5=''
                tj=t4+t5+t2+t3+t1+t6  #托架标注
                zr=t7+t5+t2+t3+t1     #支耳标注
                zhichengliang.append([tj,zr,biaogao,str(rest[2][1][i]),L1,'--',' ',data[5]])
        for i in rest[3][0]:
            zhichengliang.append([Ptype[12][1],Ptype[12][2],str(i),data[10],'--','--',' ',None])
        for i in rest[3][1]:
            zhichengliang.append([Ptype[13][1],Ptype[13][2],str(i),data[10],'--','--',' ',None])

        for i in zhichengliang:   #type8为绘制展开图的贴板编号
            for j in Ptype:
                if j[1] in i[0] and j[3]==i[7]:
                    type8=j[7]          #当托架型式没有重新选择，和平台宽度不匹配时，这里会出错。2024.5.10
            if ('b'in i[0]) and (type8 in [4,6]):
                type8+=1
            if ('s'in i[0]) and (type8 in [2,3,4,5,6,7]):
                type8+=6
            i.append(type8)
            i.append(float(data[2]))
            print(i)
        #想不到其他好办法，只好把梯子平台材料设置成本类的属性
        self.m_langanver+=m_langanver
        self.m_langanhor+=m_langanhor
        self.m_hushou+=m_hushou
        self.m_huawenban+=m_huawenban
        self.m_jiaqiangjin+=m_jiaqiangjin
        self.m_bianliang+=m_bianliang
        self.m_anquanmen+=m_anquanmen
        return zhichengliang #,m_langanver,m_langanhor,m_hushou,m_huawenban,m_jiaqiangjin,m_bianliang,m_anquanmen
                
if __name__ == '__main__':
    cal = Calculate()
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
    data=['2000＜OD≤3100', '30', '2632', True, '10000', '1000', '1 级，2.0kN/m2', '悬臂式托架  XTJ', '', '', '210', '30', '300']
    rest=[
             [1000, 5000, 0, 0],  #上层标高、本层标高
             [1316.0, 1566.0, 2566.0, 90, -1],  #塔外半径,平台内半径,平台外半径,梯子方位，画左右
             [[30, 52, 75], [105, 130, 155, 180] ],  #托架方位
             [[100,1200], [1450, 4450] ]   #爬梯支耳标高 U100 U120
          ]
    cal.calzhierlist(data, Ptype, rest)

