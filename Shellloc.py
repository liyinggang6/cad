import wx
from Location import Location
from MXB import MXB

class Shell():
    def __init__(self):
        self.frame = wx.Frame(None,
                    id=wx.ID_ANY,
                    title='python输出测试',
                    pos=wx.DefaultPosition,
                    size=(702,200),
                    style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self.frame)
        panel4 = wx.Panel(panel, id=wx.ID_ANY, pos=(2, 5), size=(680, 55), style=wx.BORDER_THEME)
        self.mxb=MXB(self,panel4)
##      self.location=Location(self,1)
##        self.cb46=wx.TextCtrl(panel,-1,
##                     '2',
##                     pos=(50,100),
##                     size = (200,30),
##                     style=wx.TE_CENTER)
##        self.cb46.Bind(wx.EVT_LEFT_DCLICK,self.OnTextCtrl46)
##    def OnTextCtrl46(self,evt):
##        num=self.cb46.GetValue()
##        b=''
##        for i in num:
##            if i in '-+0123456789':
##                b+=i
##            else:
##                break
##        num=int(b)
##        self.location=Location(self,num)        
##        self.location.frame.ShowModal()



   
if __name__ == '__main__':
    app = wx.App()
    a=Shell()
    a.frame.Show()
    app.MainLoop()
