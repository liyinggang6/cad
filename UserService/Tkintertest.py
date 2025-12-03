import tkinter
import time
def JieShu():
    pass   #覆盖了右上角关闭功能
fram1=tkinter.Tk()
fram1.protocol("WM_DELETE_WINDOW", JieShu)
fram1.title('华陆化工设备智能化设计平台')
fram1.geometry("600x200+100+100")
fram1.config(background="#6fb765")
dstr=tkinter.StringVar()
ystr='开始更新软件'
dstr.set(ystr)
text=tkinter.Label(fram1,textvariable=dstr,font=('Times', 20, 'bold italic'),bg="#6fb765")
text.pack()
fram1.update()
time.sleep(1)
ystr+='\n正在进行软件更新.....'
dstr.set(ystr)
fram1.update()
time.sleep(3)
ystr+='\n软件更新完毕!'
dstr.set(ystr)
fram1.update()
btn1=tkinter.Button(fram1,text='关闭',font=('Times', 20, 'bold'),
                    width=5,command=fram1.destroy,bg="#6fb765")  #height=2,
btn1.pack(side="bottom")
fram1.mainloop()
