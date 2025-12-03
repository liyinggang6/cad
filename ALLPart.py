print("华陆工程科技有限责任公司 版权所有")
print("软件作者 谢全利 等 发布日期：2024.4.18")
print("正在初始化软件界面...")
import wx
import wx.aui as aui
import wx.adv
from openpyxl import load_workbook, Workbook
import os,sys
import Update as Up
import subprocess
from ALLPartData import PartsData
from Nestle import Nestle
from Equipment import Equipment
from Component import Component
from Shell import Shell
from NozzleFlange import NozzleFlange
from LiftingLug import LiftingLug
from Pipe import Pipe
from PlatFormAll import PlatFormAll
from PlatFormVer import PlatFormVer
from PlatFormHor import PlatFormHor
# from chatGPT import ChatGPT

class ALLPart():
    MainList = []  # 主数据
    MainID = 0  # 自增后用于给Nestle编号
    allpart_data=PartsData()
    default_data=allpart_data.default_data
    key_mode=allpart_data.key_mode
    #NozzleFlange=allpart_data.NozzleFlange   #这两项是预加载，为了真正用法兰时速度快
    #NozzleFlange_size=allpart_data.NozzleFlange_size
            
    def __init__(self):
        self.appname = "华陆化工设备智能设计平台"
        self.apprev = "3.8"
        self.filename = '未命名'
        self.MainFrame = wx.MDIParentFrame(None, -1, self.appname + self.apprev + ' - ' + self.filename,
                                           pos=(10, 10), size=(1000, 800))
        self.MainFrame.Center()
        self.MainFrame.SetBackgroundColour(wx.Colour(224, 224, 224))
        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(5101, "新建", "新建一个ALLPart文件")
        menu1.Append(5102, "打开", "打开一个ALLPart文件")
        menu1.Append(5103, "保存", "保存一个ALLPart文件")
        menu1.Append(5104, "另存为...", "保存一个ALLPart文件备份")
        menu1.Append(5105, "退出", "退出ALLpart软件")
        menubar.Append(menu1, "文件")

        menu2 = wx.Menu()
        menu2.Append(5201, "添加设备", "添加一台设备")
        menu2.Append(5202, "添加部件", "添加压力腔部件")
        menubar.Append(menu2, "设备")
        
        menu3 = wx.Menu()
        menu3.Append(5203, "常用件", "添加常用件类零件")
        menu3.Append(5204, "管法兰", "添加管法兰")
        menu3.Append(5209, "吊耳", "添加吊耳")
        menu3.Append(5306, "管子&管件", "添加管子&管件")
        menubar.Append(menu3, "零部件")

##        menu3.Append(5205, "容器法兰", "添加容器法兰")
##        menu3.Append(5206, "管子&管件", "添加管子&管件")
##        menu3.Append(5207, "容器支座", "添加容器支座")
##        menu3.Append(5208, "人孔&手孔", "添加人孔&手孔")
##        menu3.Append(5209, "吊耳", "添加吊耳")
##        menu3.Append(5305, "  容器法兰", "添加容器法兰")
        
##        menu3.Append(5307, "  容器支座", "添加容器支座")
##        menu3.Append(5308, "  人孔&手孔", "添加人孔&手孔")
##        menu3.Append(5309, "  吊耳", "添加吊耳")
        menu4 = wx.Menu()
        menu4.Append(5210, "塔器平台", "添加塔器梯子平台")
        menu4.Append(5211, "  单层塔器平台", "添加单层塔器平台")
        menu4.Append(5212, "卧式平台", "添加卧式容器梯子平台")
        menubar.Append(menu4, "梯子平台")
        
        menu5 = wx.Menu()
        menu5.Append(5501, "立式容器")
        menu5.Append(5502, "卧式容器")
        menu5.Append(5503, "塔器")
        menu5.Append(5504, "固定管板换热器(立式)")
        menu5.Append(5505, "固定管板换热器(卧式)")
        menu5.Append(5506, "U型管换热器")
        menu5.Append(5507, "浮头式换热器")
        menu5.Append(5508, "常压容器")
        menu5.Append(5509, "大型储罐")
        menu5.Append(5510, "料仓")
#        menubar.Append(menu5, "&常用设备")

        menu6 = wx.Menu()
        menu6.Append(5601, "容器类别划分", "打开容器类别划分软件")
        menu6.Append(5602, "计算水压试验", "打开计算水压试验表")
#        menubar.Append(menu6, "常用工具")

        menu9 = wx.Menu()
        menu9.Append(5901, "显示导航栏")
#        menu9.Append(5902, "检查更新")
        menu9.Append(5903, "系统默认设置")
        menu9.Append(5904, "帮助")
        menu9.Append(5905, "意见建议")
        menu9.Append(5906, "关于")
#       menu9.Append(5907, "智能秘书2.2(chatGPT)")
        menubar.Append(menu9, "设置&&帮助")
        self.MainFrame.SetMenuBar(menubar)
        
        self.MainFrame.Bind(wx.EVT_MENU, self.Onshowtree, id=5901)
        statusbar = self.MainFrame.CreateStatusBar()
        statusbar.SetFieldsCount(3)
        statusbar.SetStatusWidths([-1, -1, -1])

        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self.MainFrame)
        self.tree = wx.TreeCtrl(self.MainFrame, -1, size=(150, -1),
                                style=wx.TR_EDIT_LABELS | wx.TR_MULTIPLE | wx.TR_HAS_BUTTONS)  # |wx.TR_HIDE_ROOT
        self.mgr.AddPane(self.tree, aui.AuiPaneInfo().Left().Caption("导航栏"))
        self.tree.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.root = self.tree.AddRoot('我的项目', image=0)
        self.currentnode = self.root
        self.parent = self.root
        a = Nestle(self)
        a.currentnode = self.root
        a.MainID=self.MainID
        a.nestle_english_name='Nestle'
        a1=[
    ['Nestle',0,'我的项目','ALLPart软件-->我的项目参数设置'],
    ['25006', '面向未来的大项目', '详细设计','工艺装置1（001）\n工艺装置2（002）\n工艺装置3（003）',
     '450','350', '-17.8','-28.6', '8(0.2g)','Ⅱ/第三组', 'C',]
  ]
        a.SetData(a1)
        self.tree.SetItemData(self.root, data=a)
        toolbar = wx.ToolBar(self.MainFrame, -1, wx.DefaultPosition, wx.DefaultSize)
        bmp = wx.Bitmap('icon/New.png', wx.BITMAP_TYPE_ANY)
        toolbar.AddTool(6301, '', bmp, '新建一个ALLPart文件', wx.ITEM_NORMAL)
        bmp = wx.Bitmap('icon/Open.png', wx.BITMAP_TYPE_ANY)
        toolbar.AddTool(6302, '', bmp, '打开一个ALLPart文件', wx.ITEM_NORMAL)
        bmp = wx.Bitmap('icon/Save.png', wx.BITMAP_TYPE_ANY)
        toolbar.AddTool(6303, '', bmp, '保存一个ALLPart文件', wx.ITEM_NORMAL)
        bmp = wx.Bitmap('icon/SaveAs.png', wx.BITMAP_TYPE_ANY)
        toolbar.AddTool(6304, '', bmp, '另存一个ALLPart文件', wx.ITEM_NORMAL)
        bmp = wx.Bitmap('icon/fresh.png', wx.BITMAP_TYPE_ANY)
        toolbar.AddTool(6305, '', bmp, '关闭全部子窗口', wx.ITEM_NORMAL)
        toolbar.SetToolBitmapSize(wx.Size(20, 20))
        toolbar.Realize()
        self.MainFrame.SetToolBar(toolbar)
        self.mgr.Update()

        self.MainFrame.Bind(wx.EVT_MENU, self.OnNew, id=5101)
        self.MainFrame.Bind(wx.EVT_MENU, self.OnOpen, id=5102)
        self.MainFrame.Bind(wx.EVT_MENU, self.OnSave, id=5103)
        self.MainFrame.Bind(wx.EVT_MENU, self.OnSaveAs, id=5104)
        self.MainFrame.Bind(wx.EVT_CLOSE, self.OnExit)
        self.MainFrame.Bind(wx.EVT_MENU, self.OnExit, id=5105)

        self.MainFrame.Bind(wx.EVT_MENU, self.On5201, id=5201) #添加设备
        self.MainFrame.Bind(wx.EVT_MENU, self.On5202, id=5202) #添加部件
        self.MainFrame.Bind(wx.EVT_MENU, self.On5203, id=5203) #常用件
        self.MainFrame.Bind(wx.EVT_MENU, self.On5204, id=5204) #管法兰
        self.MainFrame.Bind(wx.EVT_MENU, self.On5209, id=5209) #吊耳
        self.MainFrame.Bind(wx.EVT_MENU, self.On5306, id=5306) #管子&管件
        self.MainFrame.Bind(wx.EVT_MENU, self.On5210, id=5210)
        self.MainFrame.Bind(wx.EVT_MENU, self.On5211, id=5211)
        self.MainFrame.Bind(wx.EVT_MENU, self.On5212, id=5212)
        self.MainFrame.Bind(wx.EVT_MENU, self.Onshowtree, id=5901)
#       self.MainFrame.Bind(wx.EVT_MENU, self.CheckAndUpdate, id=5902)
        self.MainFrame.Bind(wx.EVT_MENU, self.OnWait, id=5903)
        self.MainFrame.Bind(wx.EVT_MENU, self.OnHelp, id=5904)
        self.MainFrame.Bind(wx.EVT_MENU, self.LeaveMessage, id=5905)
        self.MainFrame.Bind(wx.EVT_MENU, self.ShowAboutDialog, id=5906)
#       self.MainFrame.Bind(wx.EVT_MENU, self.OnChatGPT, id=5907)

        self.MainFrame.Bind(wx.EVT_TOOL, self.OnNew, id=6301)
        self.MainFrame.Bind(wx.EVT_TOOL, self.OnOpen, id=6302)
        self.MainFrame.Bind(wx.EVT_TOOL, self.OnSave, id=6303)
        self.MainFrame.Bind(wx.EVT_TOOL, self.OnSaveAs, id=6304)
        self.MainFrame.Bind(wx.EVT_TOOL, self.OnCloseall, id=6305)
        self.tree.Bind(wx.EVT_TREE_KEY_DOWN, lambda evt:(print("绑定按键"),self.OnKeyDown(evt)))
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
#        self.tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnLabelChanged)
        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.tree.Bind(wx.EVT_TREE_END_DRAG, self.OnEndDrag)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick)

    def OnChatGPT(self,evt):
        #main=ChatGPT()
        #main.frame.Show()
        pass

    def OnRead(self, filename):
        with open(filename, encoding='utf-8') as file:
            line = file.readline()
            header = []
            header.append(line.find('['))
            a = Nestle(self)
            a.currentnode = self.root
            a.MainID=self.MainID
            a.nestle_english_name='Nestle'
            a.SetData(eval(line))
            self.tree.SetItemData(self.root, data=a)
            nodelist = []
            nodelist.append(self.root)
            while True:
                line = file.readline()
                if line == "":
                    break
                else:
                    header.append(line.find('['))
                    if header[-1] == header[-2]:
                        nodelist.append(self.LoadNestle(nodelist[-1], eval(line), level=0))
                    elif header[-1] > header[-2]:
                        nodelist.append(self.LoadNestle(nodelist[-1], eval(line), level=1))
                    elif header[-1] < header[-2]:
                        j = 0
                        for i in header[:-1]:
                            if i == header[-1]:
                                key = j
                            j += 1
                        nodelist.append(self.LoadNestle(nodelist[key], eval(line), level=0))

    def OnNew(self, evt):
        item = self.tree.GetFirstChild(self.root)[0]
        if item.IsOk():
            key = wx.MessageDialog(self.MainFrame,
                                   '是否保存当前信息并重新开启一个文件',
                                   '软件提示',
                                   wx.YES_NO | wx.ICON_INFORMATION | wx.CANCEL)
            modal = key.ShowModal()
            if modal == wx.ID_NO:
                self.del_node0(item)
                self.tree.GetItemData(self.root).OnClose(True)
                self.filename = '未命名'
                self.MainFrame.SetLabel(self.appname + self.apprev + ' - ' + self.filename)
                return True
            if modal == wx.ID_YES:
                if self.OnSave(True):
                    try:
                        self.del_node0(item)
                        self.tree.GetItemData(self.root).OnClose(True)
                        self.filename = '未命名'
                        self.MainFrame.SetLabel(self.appname + self.apprev + ' - ' + self.filename)
                    except:
                        pass
                    return True
                else:
                    return False
            if modal == wx.ID_CANCEL:
                return False
        return True

    def OnOpen(self, evt):
        if self.OnNew(True):
            with wx.FileDialog(self.MainFrame,
                               "打开一个ALLPart文件",
                               wildcard="APt files (*.APt)|*.APt",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return False
                else:
                    filename = fileDialog.GetPath()
                    self.OnRead(filename)
                    self.filename = filename
                    self.MainFrame.SetLabel(self.appname + self.apprev + ' - ' + self.filename)
                    return True

    def Save(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            header = ''

            def preOrder(item):
                nonlocal header
                if not item.IsOk():
                    header = header[2:]
                    return
                a = self.tree.GetItemData(item)
                file.write(header + str(a.GetData()) + '\n')
                header += '  '
                preOrder(self.tree.GetFirstChild(item)[0])
                preOrder(self.tree.GetNextSibling(item))

            preOrder(self.root)

    def OnSaveAs(self, evt):
        with wx.FileDialog(self.MainFrame,
                           "另存一个ALLPart文件",
                           wildcard="APt files (*.APt)|*.APt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return False
            filename = fileDialog.GetPath()
            self.Save(filename)
            self.filename = filename
            self.MainFrame.SetLabel(self.appname + self.apprev + ' - ' + self.filename)
            return True

    def OnSave(self, evt):
        if self.filename == '未命名':
            if self.OnSaveAs(True):
                return True
            else:
                return False
        else:
            self.Save(self.filename)
            return True

    def OnCloseall(self, evt):
        def preOrder(item):
            if not item.IsOk():
                return
            a = self.tree.GetItemData(item)
            # a.frame.Show(False)
            a.OnClose(True)
            preOrder(self.tree.GetFirstChild(item)[0])
            preOrder(self.tree.GetNextSibling(item))
        preOrder(self.root)

    def get_keynode(self, key):
        '''根据当前节点向上搜索key所在的节点'''
        node = self.currentnode
        while node.IsOk():
            a = self.tree.GetItemData(node)
            if a.nestle_english_name == key:
                break
            node = self.tree.GetItemParent(node)
        if node.IsOk():
            return node
        else:
            return self.currentnode

    def On5201(self, evt):
        node=self.LoadNestle(self.currentnode, 11)  #自动寻找层级
        data = self.allpart_data.default_data[111]
        if node != False:
           a = self.tree.GetItemData(node)
           a.SetData(data)

    def On5202(self, evt):
        node=self.LoadNestle(self.currentnode, 21)
        data = self.allpart_data.default_data[211]
        if node != False:
           a = self.tree.GetItemData(node)
           a.SetData(data)
        
    def On5203(self, evt): #常用件
        node=self.LoadNestle(self.currentnode, 51)
        data = self.allpart_data.default_data[511]
        if node != False:
           a = self.tree.GetItemData(node)
           a.SetData(data)
                  
    def On5204(self, evt): #管法兰
        node=self.LoadNestle(self.currentnode, 52)
        data = self.allpart_data.default_data[521]
        if node != False:
           a = self.tree.GetItemData(node)
           a.SetData(data)

    def On5209(self, evt): #吊耳
        node=self.LoadNestle(self.currentnode, 57)
        data = self.allpart_data.default_data[571]
        if node != False:
           a = self.tree.GetItemData(node)
           a.SetData(data)
    
    def On5306(self, evt): #管子&管件
        node=self.LoadNestle(self.currentnode, 54)
        data = self.allpart_data.default_data[541]
        if node != False:
           a = self.tree.GetItemData(node)
           a.SetData(data)

    def On5210(self, evt):
        node = self.get_keynode('Equipment')
        data = self.allpart_data.default_platform_all
        self.LoadNestle(node, data, 1)

    def On5211(self, evt):
        node = self.get_keynode('PlatFormAll')
        data = self.allpart_data.default_platform_ver
        self.LoadNestle(node, data, 1)

    def On5212(self, evt):
        node = self.get_keynode('Equipment')
        data = self.allpart_data.default_platform_hor
        self.LoadNestle(node, data, 1)

    def LoadNestle(self, node, data=11, level=-1, favorite=False): #根据data创建一个节点及界面,-1代表调用时不指定层级
        #data为key_mode的模块代码时或模块名称英文，建一个空白的面板
        #data为完整list数据时，建一个带数据的面板用于打开文件
        if node == self.root:
            level = 1
            parent = self.root
        else:
            parent = self.tree.GetItemParent(node)
        lable_data0 = self.tree.GetItemData(parent).GetLableData()    #点击处的父节点的标签数据
        lable_data1 = self.tree.GetItemData(node).GetLableData()      #点击处的节点的标签数据
        if type(data)==type([]):
            key_name=data[0][0]
        else:
            key_name=data
        for key in self.key_mode:
            if key[1] == lable_data0[0]:
                nestle0_ID = key[0]  #点击处的父节点NestleID
            if key[1] == lable_data1[0]:
                nestle1_ID = key[0]  #点击处的节点NestleID
            if key[1] == key_name or key[0] == key_name:
                nestleID = key[0]  #正在添加的节点的ID
                nestleIDlist = key[3]
                nestle_chinese_name=key[2]
                nestle_english_name=key[1]
        if level == -1:  #不指定层级时
            if nestle1_ID == 21: #如果点击的是部件
                ret = wx.MessageBox('是否在部件内部创建?', '来自系统的询问', wx.YES_NO | wx.CANCEL)
                if ret == wx.YES:
                    level=1   
                elif ret == wx.NO:
                    level=0 
                else:
                    return False
            else:
                level=0  
        if level == 0 and (nestle0_ID in nestleIDlist):
            new_node = self.tree.InsertItem(parent, node, nestle_chinese_name)
        elif nestle1_ID in nestleIDlist:
            new_node = self.tree.AppendItem(node, nestle_chinese_name)
        else:
            wx.MessageBox('您在导航栏点选的位置下无法创建' + nestle_chinese_name + '，请重新点选再试', '出错', wx.OK)
            return False
        self.MainID+=1
#       a = eval(data[0][0] + "(self,data=data)")  # 构造一个nestle对象
        print("Nestle=",self.allpart_data.Factory(key_name))
        a = eval(self.allpart_data.Factory(key_name))
        a.currentnode = new_node
        a.MainID=self.MainID
        a.nestle_english_name=nestle_english_name
        print("data in LoadNestle is:",data)
        if type(data)==type([]):
            a.SetData(data)
        self.tree.SetItemData(new_node, data=a)
        try:
            self.tree.ExpandAll()
        except:
            pass
        # a.frame.Show()
        # a.frame.SetFocus()
        # self.tree.SetFocusedItem(new_node)
        return new_node

    def Onshowtree(self, evt):
        self.mgr.GetPane(self.tree).Left().Show()
        self.mgr.Update()

    def OnSelChanged(self, evt):
        self.currentnode = evt.GetItem()
        CurrentNestle = self.tree.GetItemData(self.currentnode)
        CurrentNestle.frame.Show(False)
        CurrentNestle.frame.Show(True)
        CurrentNestle.frame.SetFocus()
        self.tree.SetFocusedItem(self.currentnode)

##    def OnLabelChanged(self, evt):
##        self.currentnode = evt.GetItem()
##        a = self.tree.GetItemData(self.currentnode)
##        a.NestleList[0][1] = self.tree.GetItemText(self.currentnode)
##        a.frame.SetLabel(a.NestleList[0][1])

    def OnKeyDown(self, evt):
        print(evt)
        key = evt.GetKeyCode()
        print('正在按键的编号是：', key)
        self.DoCopyAndPaste(True, key)

    def DoCopyAndPaste(self, evt, key):
        print('DoCopyAndPaste key=：', key)
        if key == 127:  # Del
            node = self.currentnode
            self.currentnode = self.root
            self.del_node(node)
        if key == 88:  # X
            try:
                node = self.currentnode
                self.currentnode = self.tree.GetNextSibling(self.currentnode)
            except:
                self.currentnode = self.root
            self.copy_data = self.copy_node(node)
            self.del_node(node)
        if key == 67:  # C
            self.copy_data = self.copy_node(self.currentnode)
        if key == 86:  # V
            try:
                self.create_node(self.currentnode, self.copy_data)
            except:
                print('粘贴出错......')

    def OnBeginDrag(self, event):
        node = event.GetItem()
        if node == self.root:
            pass
        else:
            event.Allow()
            self.cut_node = node
            self.copy_data = self.copy_node(node)

    def del_node(self, node):  # 删除本节点及其子节点
        item = self.tree.GetFirstChild(node)[0]
        if item.IsOk():
            self.del_node0(item)
        try:
            a = self.tree.GetItemData(node)
        except:
            pass
        try:
            a.frame.Destroy()
        except:
            pass
        try:
            self.tree.Delete(node)
        except:
            pass

    def del_node0(self, node):  # 删除本节点及其兄弟节点
        nodelist = []

        def preOrder(item):
            nonlocal nodelist
            if not item.IsOk():
                return
            nodelist.append(item)
            preOrder(self.tree.GetFirstChild(item)[0])
            preOrder(self.tree.GetNextSibling(item))

        preOrder(node)
        nodelist.reverse()
        for node in nodelist:
            try:
                a = self.tree.GetItemData(node)
            except:
                pass
            try:
                a.frame.Destroy()
            except:
                pass
            try:
                self.tree.Delete(node)
            except:
                pass

    def copy_node(self, node):  # 拷贝本节点及其子节点
        key = []
        level = 0
        a1 = self.tree.GetItemData(node).GetData()
        a2 = self.tree.GetItemText(node)
        key.append([a1, level, a2])
        item = self.tree.GetFirstChild(node)[0]
        if item.IsOk():
            def preOrder(item):
                nonlocal key, level
                if not item.IsOk():
                    level -= 1
                    return
                level += 1
                a1 = self.tree.GetItemData(item).GetData()
                a2 = self.tree.GetItemText(item)
                key.append([a1, level, a2])  #采用数据、层级、节点上文字的数据格式储存拷贝内容
                preOrder(self.tree.GetFirstChild(item)[0])
                preOrder(self.tree.GetNextSibling(item))
            preOrder(item)
        return key

    def create_node(self, node, key):  #在node下创建key储存的节点系
        level = key[0][1]
        nodelist = []
        kj = 0
        for key1 in key:
            if key1[1] == level:
                node = self.LoadNestle(node, key1[0], 0)
            elif key1[1] > level:
                node = self.LoadNestle(node, key1[0], 1)
            elif key1[1] < level:
                j = 0
                for key2 in key[:kj]:
                    if key2[1] == level:
                        keylevel = j
                    j += 1
                node = nodelist[keylevel]
                node = self.LoadNestle(node, key1[0], 0)
            if node==False:
                return False
            nodelist.append(node)
            level = key1[1]
            kj += 1

    def OnEndDrag(self, event):
        event.Allow()
        node = event.GetItem()
        self.currentnode = node
        if node.IsOk():
            if self.create_node(node, self.copy_data) != False:
                self.del_node(self.cut_node)
        else:
            wx.MessageBox('没有找到零件位置，调整零件位置失败。', '调整零件位置出错', wx.OK)

    def OnRightClick(self, event):
        """Setup and Open a popup menu."""
        self.currentnode = event.GetItem()
        itemData = self.tree.GetItemData(self.currentnode)
        self.tree.SelectItem(self.currentnode)
        self.tree.SetFocusedItem(self.currentnode)
        popupmenu = wx.Menu()
        entries = {'&剪切 X': 88, '&复制 C': 67, '&粘贴 V': 86, '&删除 Del': 127}
        i = 5800
        for entry in entries:
            i = i + 1
            menuItem = popupmenu.Append(i, entry)
            self.MainFrame.Bind(wx.EVT_MENU, lambda evt, key=entries[entry]: self.DoCopyAndPaste(evt, key), id=i)
        if self.currentnode == self.root:
            pass
        else:
            self.MainFrame.PopupMenu(popupmenu, event.GetPoint())

    def OnExit(self, evt):
        ret = wx.MessageBox('是否保存当前文件?', '退出确认', wx.YES_NO | wx.CANCEL)
        if ret == wx.YES:
            if self.OnSave(True):
                pass
            else:
                return False
        if ret == wx.CANCEL:
            return False
        '''
        msg=''
        isLastestVersion = None
        update = Up.Update()
        msg = update.Parse_Config()   #读取本地配置文件
        if not msg:
            isLastestVersion, lastest_version, msg = update.Check_Revision()
            save_path=os.path.dirname(os.path.realpath(sys.argv[0]))
        if isLastestVersion == False:
            ret = wx.MessageBox('发现新版本!  是否进行软件更新?', '提示', wx.YES_NO)
            if ret == wx.YES:
                isDownload, msg =update.download(app_package_name='Update.zip', download_path=save_path, unpack_path=save_path)
                subprocess.Popen('Update.exe')
        '''
        self.mgr.UnInit()
        evt.Skip()
        self.MainFrame.Destroy()

    def OnHelp(self, evt):
        wx.MessageBox('软件说明信息如下：\n  \
1. 软件启动后点击导航栏内的‘我的项目’，可以修改项目信息。\n  \
2. 主项一览表可以输入多行，后续添加的设备可以选择此处添加的主项。\n  \
3. 点击下拉式菜单‘添加部件’-->‘设备’ 可以添加一台设备。\n  \
4. 点击导航栏内刚添加的‘设备’可显示和修改设备信息。\n  \
5. 导航栏内选中需要添加零部件的设备，然后可以添加常用件、法兰等或添加部件。\n  \
6. 部件下面可添加部件或常用件、法兰等\n  \
7. 导航栏内选中需要添加平台的设备，然后可以添加塔平台或卧式平台。\n  \
8. 我的项目下可以添加多台设备，每台设备下可以添加多个平台。\n  \
9. 每个塔平台下可以添加多层平台。\n  \
10. 当在导航栏内选中某个项，并添加同层级的项时，添加的项插入到选中项的后面。\n  \
11. 当在导航栏内选中某个项，并添加下一层级的项时，添加的项插入到选中项下一层级的最后面。\n  \
12. 不符合层级关系添加项会弹出出错信息。\n  \
13. 导航栏内目录树上点击右键可以弹出 剪切 复制 粘贴 删除 菜单，均可执行相应操作。\n  \
14. 按钮上带有->字符的代表需要连接AutoCAD进行绘图。\n  \
15. 需要绘图时要先打开AutoCAD并处于等待绘图状态。\n  \
16. 已测试AutoCAD 2010、AutoCAD 2004版本可以使用。\n  \
17. AutoCAD中预先要有使用到的线型。\n  \
18. 当执行自动绘图命令时，软件会拷贝图框等文件到图纸文件所在的目录。某些情况下\n  \
会因为拷贝命令执行不成功导致自动绘图失败。遇到这种情况可以手动拷贝图框、a3T.dwg\n  \
、PN.dwg到图纸文件所在的目录。\n  \
19. 意见建议请联系：谢全利 <xql1806@chinahualueng.com>\n',
                      '帮助',
                      wx.OK | wx.ICON_INFORMATION)

    def ShowAboutDialog(self, evt):
        info = wx.adv.AboutDialogInfo()
        info.SetName(self.appname)
        info.SetVersion(self.apprev)
        info.SetDescription("This program does something great.")
        info.SetCopyright("(C) 2022 谢全利 <xql1806@chinahualueng.com>")
        wx.adv.AboutBox(info)

    def CheckAndUpdate(self,evt):
        msg=''
        isLastestVersion = None
        update = Up.Update()
        msg = update.Parse_Config()   #读取本地配置文件
        if not msg:
            isLastestVersion, lastest_version, msg = update.Check_Revision()
            save_path=os.path.dirname(os.path.realpath(sys.argv[0]))
        else:
            wx.MessageBox( msg, "提示", wx.OK)
        if isLastestVersion == False:
            ret = wx.MessageBox('发现新版本! 是否保存当前文件，并进行软件更新?', '提示 更新需要关闭本软件', wx.YES_NO | wx.CANCEL)
            if ret == wx.YES:
                if self.OnSave(True):
                    pass
                else:
                    return False
            if ret == wx.CANCEL:
                return False
            isDownload, msg =update.download(app_package_name='Update.zip', download_path=save_path, unpack_path=save_path)
            subprocess.Popen('Update.exe')
            self.mgr.UnInit()
            evt.Skip() 
            self.MainFrame.Destroy()
        elif isLastestVersion == True:
            wx.MessageBox('恭喜！你使用的软件是最新版本。', '新版本检查', wx.OK)
        else:
            wx.MessageBox(msg, '新版本检查', wx.OK)
       
    def LeaveMessage(self,evt):
        import pymysql
        import UserService.GuestBoard as GuestBoard
        with open("settings.ini", encoding='utf-8') as file:
            for line in file:
                if "LiuyanIP" in line:
                    LiuyanIP=line.split("=")[1]
                    break
        if LiuyanIP:
            try:
                db = pymysql.connect(
                    host=LiuyanIP,
                    user='xql1806',
                    password='Xiequanli1806',
                    database='ALLPart',
                    charset='utf8')
            except:
                wx.MessageBox('连接留言的服务器出错!','出现错误', wx.OK | wx.ICON_INFORMATION)
            else:
                Board = GuestBoard.GuestBoardForm(db)
                Board.frame.ShowModal()
                print('正在留言中...')
        else:
            wx.MessageBox('没有找到存放留言的服务器!','出现错误', wx.OK | wx.ICON_INFORMATION)

    def OnWait(self, evt):
        wx.MessageBox('意见建议请联系：谢全利 <xql1806@chinahualueng.com>', '该功能正在建设...', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    mainapp = ALLPart()
    mainapp.MainFrame.Show()
    print('软件已启动，欢迎您使用...')
    app.MainLoop()
