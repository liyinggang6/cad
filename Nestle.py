import wx
class Nestle():
    def __init__(self, main):
        self.Main = main
        self.frame = wx.MDIChildFrame(main.MainFrame,
                                      id=wx.ID_ANY,
                                      title='我的项目',
                                      pos=wx.DefaultPosition,
                                      size=(332, 445),
                                      style=wx.DEFAULT_FRAME_STYLE)
        self.panel = wx.Panel(self.frame)
        wx.StaticText(self.panel, label='项目代号', pos=(40, 10))
        self.cb11 = wx.TextCtrl(self.panel, value="", pos=(90, 10), size=(150, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label='项目名称', pos=(40, 35))
        self.cb12 = wx.TextCtrl(self.panel, value="", pos=(90, 35), size=(220, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label='设计阶段', pos=(40, 60))
        self.cb13 = wx.ComboBox(self.panel, pos=(90, 60), size=(150, 22),
                                choices=['报价', '初步设计', '基础设计', '详细设计', '基础/详细设计'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='主项一览表', pos=(40, 85))
        self.cb14 = wx.TextCtrl(self.panel,
                                value='',
                                pos=(110, 85), size=(200, 95), style=wx.TE_MULTILINE)
        wx.StaticText(self.panel, label='注：', pos=(35, 115))
        wx.StaticText(self.panel, label='可填多行。', pos=(40, 135))
        wx.StaticText(self.panel, label='基本风压', pos=(140, 185))
        self.cb15 = wx.ComboBox(self.panel, pos=(190, 185), size=(100, 22),
                                choices=['300', '350', '400', '450', '500', '550', '600', '700', '800', '900'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='基本雪压', pos=(140, 210))
        self.cb16 = wx.ComboBox(self.panel, pos=(190, 210), size=(100, 22),
                                choices=['300', '350', '400', '450', '500'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='月平均最低气温最低值', pos=(60, 235))
        self.cb17 = wx.TextCtrl(self.panel, value="", pos=(190, 235), size=(100, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label='(仅用于大罐)日平均最低气温最低值', pos=(1, 260))
        self.cb18 = wx.TextCtrl(self.panel, value="", pos=(190, 260), size=(100, 22), style=wx.TE_LEFT)
        wx.StaticText(self.panel, label='地震设防烈度(基本地震加速度)', pos=(10, 285))
        self.cb19 = wx.ComboBox(self.panel, pos=(190, 285), size=(100, 22),
                                choices=['7(0.1g)', '7(0.15g)', '8(0.2g)', '8(0.3g)', '9(0.4g)'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='场地土类别/设计地震分组', pos=(40, 310))
        self.cb20 = wx.ComboBox(self.panel, pos=(190, 310), size=(100, 22),
                                choices=['Ⅰ/第一组', 'Ⅰ/第二组', 'Ⅰ/第三组',
                                         'Ⅱ/第一组', 'Ⅱ/第二组', 'Ⅱ/第三组',
                                         'Ⅲ/第一组', 'Ⅲ/第二组', 'Ⅲ/第三组',
                                         'Ⅳ/第一组', 'Ⅳ/第二组', 'Ⅳ/第三组'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='地面粗糙度', pos=(115, 335))
        self.cb21 = wx.ComboBox(self.panel, pos=(190, 335), size=(100, 22),
                                choices=['A', 'B', 'C', 'D'],
                                style=wx.CB_DROPDOWN)
        wx.StaticText(self.panel, label='Pa', pos=(290, 185))
        wx.StaticText(self.panel, label='Pa', pos=(290, 210))
        wx.StaticText(self.panel, label='℃', pos=(290, 235))
        wx.StaticText(self.panel, label='℃', pos=(290, 260))
        self.cb81 = wx.Button(self.panel, label='确定&&关闭', pos=(242, 380), size=(68, 22))
        self.frame.Bind(wx.EVT_CLOSE, self.OnButton81)
        self.frame.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.cb81.Bind(wx.EVT_BUTTON, self.OnButton81)

    def OnClose(self, evt):
        self.OnButton81(True) 

    def OnButton81(self, evt):
        '''这个方法需要被继承'''
        self.NestleList = self.GetData()
        self.frame.Show(False)
        print(self.NestleList)

    def OnFocus(self, evt):
        self.Main.currentnode = self.currentnode
        '''这个方法需要被继承'''

    def GetLableData(self):
        return [self.nestle_english_name, self.MainID,
                 self.Main.tree.GetItemText(self.currentnode),
                 self.frame.GetLabel()]
        '''这个方法需要被继承'''

    def SetLableData(self,data):
        self.nestle_english_name=data[0]
#       self.MainID=data[1]  #不执行这一句话，可以在打开文件时顺序化MainID
        self.Main.tree.SetItemText(self.currentnode,data[2])
        self.frame.SetLabel(data[3])
        
    def GetData(self):
        list1 = self.GetLableData()
        list2 = [list1,
                 [self.cb11.GetValue(),
                 self.cb12.GetValue(),
                 self.cb13.GetValue(),
                 self.cb14.GetValue(),
                 self.cb15.GetValue(),
                 self.cb16.GetValue(),
                 self.cb17.GetValue(),
                 self.cb18.GetValue(),
                 self.cb19.GetValue(),
                 self.cb20.GetValue(),
                 self.cb21.GetValue(),]
                 ]
        return list2
    
    def GetProjectInfo(self):
       return [self.cb11.GetValue(),
               self.cb12.GetValue(),
               self.cb13.GetValue(),
               self.cb14.GetValue(),]
 
    def GetSiteInfo(self):
       return [self.cb15.GetValue(),
               self.cb16.GetValue(),
               self.cb17.GetValue(),
               self.cb18.GetValue(),
               self.cb19.GetValue(),
               self.cb20.GetValue(),
               self.cb21.GetValue(),]
    
    def GetMXBContent(self):
        numlist=[0]
        mxbcontent=[]
        def preOrder(item):
            nonlocal numlist,mxbcontent
            if not item.IsOk():
                numlist.pop()
                return
            b=self.Main.tree.GetItemData(item)
            if hasattr(b,'mxb'):
                numlist[-1]+=1
                jianhao=''
                for i in numlist[1:]:
                    jianhao+=(str(i)+'-')
                jianhao=jianhao[:-1]
                hang=b.mxb.GetData()[:7]
                hang.insert(0,jianhao)
                mxbcontent.append(hang)
            numlist.append(0)
            preOrder(self.Main.tree.GetFirstChild(item)[0])
            preOrder(self.Main.tree.GetNextSibling(item))
        preOrder(self.currentnode)
        return mxbcontent
        
    def SetData(self, data):
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
        self.SetLableData(data[0])

    def OnWait(self, evt):
        wx.MessageBox('意见建议请联系：谢全利 <xql1806@chinahualueng.com>', '该功能正在建设...', wx.OK | wx.ICON_INFORMATION)

        

