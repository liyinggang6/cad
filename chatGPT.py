
import  wx
import requests,sys

class ChatGPT():
    def __init__(self):
        self.frame = wx.Frame(None, id=wx.ID_ANY,
                          title='智能秘书2.2   桥接模式                 软件编制：谢全利',
                          pos=wx.DefaultPosition,
                          size=(645, 455),
                          #style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN
                            )
        self.panel = wx.Panel(self.frame)
        
        self.text1 = wx.TextCtrl(self.panel, -1,
                                '写一首描述春暖花开诗词',
                                pos=(2, 5),
                                size=(580, 100),
                                style=wx.TE_MULTILINE)
        self.text2 = wx.TextCtrl(self.panel, -1,
                                '  ',
                                pos=(2, 110),
                                size=(620, 300),
                                style=wx.TE_MULTILINE)                      
        font1 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.text1.SetFont(font1)
        self.text2.SetFont(font1)
        self.btn_commit = wx.Button(self.panel, label="提交", pos=(585, 5), size=(40, 100))
        self.btn_commit.Bind(wx.EVT_BUTTON, self.Commit)
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer1.Add(self.text1, 1, wx.EXPAND)
        self.sizer1.Add(self.btn_commit, 0,)
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2.Add(self.sizer1,0, wx.EXPAND)
        self.sizer2.Add(self.text2, 1, wx.EXPAND)
        self.panel.SetSizer(self.sizer2)

    def Commit(self, evt):
        content = self.text1.GetValue()
        if(len(content.strip()) == 0):
            wx.MessageBox('请填写内容后再提交',
                          '提醒',
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.text2.SetValue("请稍候...")
            self.text2.Update()
            self.btn_commit.Enable(False)
            answer=self.GetAnswer(content)
            self.text2.SetValue(answer)
            self.btn_commit.Enable(True)

    def GetAnswer(self, content):
        ServerIP=False
        with open("settings.ini", encoding='utf-8') as file:
            for line in file:
                if "ServerIP" in line:
                    ServerIP=line.split("=")[1][:-1]
                    break
        if ServerIP:
            url ="http://" + ServerIP + "/openai/" + content
        else:
            return "配置文件中没有找到桥接服务器地址。"

        try:
            #print(url)
            resp = requests.get(url)  
            resp.encoding = 'UTF-8'
            if resp.status_code == 200:
                answer=resp.text
            else:
                answer="桥接服务器没有响应。"
        except:
            answer="桥接服务器连接出错。"
        return answer

if __name__ == '__main__':
    app = wx.App()
    main=ChatGPT()
    main.frame.Show()
    app.MainLoop()
