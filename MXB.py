import wx
from Location import Location

class MXB():
    def __init__(self,parent,panel):
        self.parent=parent
        posx=5
        posy=5
        jian=4   #控件间隙
        high=20  #控件高度
        chang=[115,195,30,120,50,50,82]  #控件长度
        self.cb44=wx.TextCtrl(panel,-1,"",pos=(posx,posy),
                              size = (chang[0],high),style=wx.TE_CENTER)
        self.cb45=wx.TextCtrl(panel,-1,"",pos=(posx+chang[0]+jian,posy),
                              size = (chang[1],high),style=wx.TE_CENTER)
        self.cb46=wx.TextCtrl(panel,-1,"1",pos=(posx+chang[0]+chang[1]+2*jian,posy),
                              size = (chang[2],high),style=wx.TE_CENTER)
        self.cb47=wx.TextCtrl(panel,-1,"",pos=(posx+chang[0]+chang[1]+chang[2]+3*jian,posy),
                              size = (chang[3],high),style=wx.TE_CENTER)
        self.cb48=wx.TextCtrl(panel,-1,"",pos=(posx+chang[0]+chang[1]+chang[2]+chang[3]+4*jian,posy),
                              size = (chang[4],high),style=wx.TE_CENTER)
        self.cb49=wx.TextCtrl(panel,-1,"",pos=(posx+chang[0]+chang[1]+chang[2]+chang[3]+chang[4]+5*jian,posy),
                              size = (chang[5],high),style=wx.TE_CENTER|wx.TE_READONLY)
        self.cb410=wx.TextCtrl(panel,-1,"",pos=(posx+chang[0]+chang[1]+chang[2]+chang[3]+chang[4]+chang[5]+6*jian,posy),
                               size = (chang[6],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="图号或标准号", pos =(posx,posy+high+jian),size = (chang[0],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="名称", pos =(posx+chang[0]+jian,posy+high+jian),size = (chang[1],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="数量", pos =(posx+chang[0]+chang[1]+2*jian,posy+high+jian),size = (chang[2],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="材料", pos =(posx+chang[0]+chang[1]+chang[2]+3*jian,posy+high+jian),size = (chang[3],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="单重Kg", pos =(posx+chang[0]+chang[1]+chang[2]+chang[3]+4*jian,posy+high+jian),size = (chang[4],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="总重Kg", pos =(posx+chang[0]+chang[1]+chang[2]+chang[3]+chang[4]+5*jian,posy+high+jian),size = (chang[5],high),style=wx.TE_CENTER)
        wx.StaticText(panel,label ="备注", pos =(posx+chang[0]+chang[1]+chang[2]+chang[3]+chang[4]+chang[5]+6*jian,posy+high+jian),size = (chang[6],high),style=wx.TE_CENTER)
        self.cb46.Bind(wx.EVT_TEXT,self.OnTextCtrl46)
        self.cb48.Bind(wx.EVT_TEXT,self.OnTextCtrl48)
        self.cb46.Bind(wx.EVT_LEFT_DCLICK,self.OnTextCtrl46d1)
        self.weightcs=0
        self.weightss=0
        self.sc=1 #碳钢占的重量比例
        self.LocList=[]
        

    def OnTextCtrl46d(self,evt):
        num=self.cb46.GetValue()
        b=''
        for i in num:
            if i in '-+0123456789':
                b+=i
            else:
                break
        num=int(b)
        self.location=Location(self,num)
        if self.LocList==[]:
            pass
        else:
            self.location.SetData(self.LocList)

    def OnTextCtrl46d1(self,evt):
        self.OnTextCtrl46d(True)
        self.location.frame.ShowModal()

    def OnTextCtrl46(self,evt):
        self.OnTextCtrl48(True)
        self.parent.QuantityChanged()
        
    def OnTextCtrl48(self,evt):
       a=self.GetQuantity()
       b=self.cb48.GetValue()
       if b=='':
           b='0'
       
       c=''
       for i in b:
           if i in '-0123456789.':
               c+=i
           else:
               break
       b=float(c)
       c=a*b
       self.weightcs = self.sc*c
       self.weightss = (1-self.sc)*c
       c=('%.1f' % c)
       self.cb49.SetValue(c)

    def SetStandard(self, standard=''):
        self.cb44.SetValue(standard)

    def SetName(self,name=''):
        self.cb45.SetValue(name)

    def GetQuantity(self):
        a=self.cb46.GetValue()
        if a=='':
            a='0'
        c=''
        for i in a:
            if i in '-0123456789.':
                c+=i
            else:
                break
        return float(c)

    def SetMaterial(self, material=''):
        self.cb47.SetValue(material)
    
    def SetWeight(self, weightcs=0.0, weightss=0.0):
        #weight为单重float型
        weight=weightcs+weightss
        try:
            self.sc=weightcs/weight
        except:
            self.sc=1
        self.cb48.SetValue('%.1f' % weight)
        self.weightcs = self.sc*weight*self.GetQuantity()
        self.weightss = (1-self.sc)*weight*self.GetQuantity()
        
    def GetWeights(self):
        #weights为总重float型
        return self.weightcs,self.weightss
        
    def SetNote(self,note=''):
        self.cb410.SetValue(note)

    def GetPreBaseRotHkey(self):
        node = self.parent.currentnode
        tree = self.parent.Main.tree
        item = tree.GetPrevSibling(node)
        while item.IsOk():
            a = tree.GetItemData(item)
            if hasattr(a,'mxb'):
                base = a.mxb.base
                rot = a.mxb.rot
                Hkey = 0
                return base,rot,Hkey
            item = tree.GetPrevSibling(item)
        base,rot,Hkey=self.GetTopBaseRotHkey()
        return base,rot,Hkey

    def GetTopBaseRotHkey(self):
        node = self.parent.currentnode
        tree = self.parent.Main.tree
        item = tree.GetItemParent(node)
        a = tree.GetItemData(item)
        if hasattr(a,'mxb'):
            base = a.mxb.base
            rot = a.mxb.rot
            Hkey = 0
        else:
            base = (0,0,0)
            rot = (0,1,0)
            Hkey = 0 
        return base,rot,Hkey
    
    def SetData(self,data):
        self.cb44.ChangeValue(data[0])
        self.cb45.ChangeValue(data[1])
        self.cb46.ChangeValue(data[2])
        self.cb47.ChangeValue(data[3])
        self.cb48.ChangeValue(data[4])
        self.cb49.ChangeValue(data[5])
        self.cb410.ChangeValue(data[6])
        self.weightcs=data[7]
        self.weightss=data[8]

    def GetData(self):
        return [self.cb44.GetValue(),
               self.cb45.GetValue(),
               self.cb46.GetValue(),
               self.cb47.GetValue(),
               self.cb48.GetValue(),
               self.cb49.GetValue(),
               self.cb410.GetValue(),
               self.weightcs,
               self.weightss,]  

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, '测试MXB类',pos=(10, 10), size=(800, 600))
    frame.Center()
    panel = wx.Panel(frame)
    panel1 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 507), size=(680, 55), style=wx.BORDER_THEME)
    data=['04-71186', ' 吊耳 20', '1', 'Q345R', '0.5', '0.5', '',0.5,0]
    pt1=MXB(frame,panel1)
    pt1.SetData(data)
    frame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
