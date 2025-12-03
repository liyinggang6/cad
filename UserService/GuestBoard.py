import wx
import wx.adv
import pymysql
import socket
import datetime

class GuestBoardForm(wx.Dialog):
    def __init__(self,  db):
        self.db = db
        self.MainFrame = wx.MDIParentFrame(None, -1, ' -TEST ', pos=(10, 10),
                                           size=(800, 600))
        self.frame = wx.Dialog(self.MainFrame,
                               id=wx.ID_ANY,
                               title='感谢您的意见和建议',
                               pos=wx.DefaultPosition,
                               size=(600, 300),
                               style=wx.CAPTION | wx.CLOSE_BOX)
        self.panel = wx.Panel(self.frame)
        self.text = wx.TextCtrl(self.panel, -1,
                                '',
                                pos=(2, 0),
                                size=(580, 200),
                                style=wx.TE_MULTILINE)
        # self.text.SetBackgroundColour((255, 223, 255))
        font1 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.text.SetFont(font1)
        self.btn_commit = wx.Button(self.panel, label="提交", pos=(260, 210), size=(80, 40))
        self.btn_commit.Bind(wx.EVT_BUTTON, self.Commit)

    def Commit(self, evt):
        content = self.text.GetValue()
        if(len(content.strip()) == 0):
            wx.MessageBox('请填写内容后再提交',
                          '提醒',
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.LeaveMessage(content)
            wx.MessageBox('提交成功',
                          '感谢您的意见和建议',
                          wx.OK | wx.ICON_INFORMATION)


    def LeaveMessage(self, content):
        # 获取留言用户信息
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.db.cursor()
        queryID_sql = 'SELECT IDS FROM Liuyan'  #查询所有的记录的id
        cursor.execute(queryID_sql)
        ids = cursor.fetchall()
        ids_list = [id1[0] for id1 in ids]
        new_id = max(ids_list) + 1  #计算新id
        insert_sql = 'INSERT Liuyan VALUES (%s,%s,%s,%s,%s)'
        insert_content=(new_id,content,name,ip,localtime)
        cursor.execute(insert_sql,insert_content)
        self.db.commit()
        print("留言完成")

if __name__ == '__main__':
    app = wx.App()
    db = pymysql.connect(
        host='10.6.117.44',
        user='xql1806',
        password='Xiequanli1806',
        database='ALLPart',
        charset='utf8')
    print('正在留言中...')
    GuestBoard = GuestBoardForm(db)
    GuestBoard.frame.ShowModal()
    app.MainLoop()

    # 主程序中调用方法如下：
    # import GuestBoardForm
    #
    # db = pymysql.connect(
    #     host='10.6.70.118',
    #     user='xql1806',
    #     password='Xiequanli1806',
    #     database='PlatForm',
    #     charset='utf8')
    # GuestBoard = GuestBoardForm.GuestBoardForm(db)
    # GuestBoard.frame.ShowModal()
    # print('正在留言中...')
