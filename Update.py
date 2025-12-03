# -*- coding: utf-8 -*-
import requests,sys
import os,shutil
# import win32api, win32con

class Update:
    def __init__(self):
        self.config_file_path = "settings.ini"
        self.root = None
        self.config_dict = {}
        self.bit=str(len(bin(sys.maxsize))-1)+"-bit"  #检测本机的操作系统 32-bit 64-bit

    def Parse_Config(self):
        '''
        function:解析settings.ini文件，从文件中读取配置，放在self.config_dict中
        '''
        msg = ''
        try:
            with open("settings.ini",encoding='utf-8') as file:
                for line in file:
                     if "=" in line:
                         text=line.replace('\n', '').split(" ")[0]
                         text=text.split("=")
                         key=text[0]
                         value=text[1]
                         self.config_dict.update({key:value})
        except FileNotFoundError:
            msg = "配置文件未找到!"
        except:
            msg = "配置文件解析出现异常!异常原因为：" + str(sys.exc_info()[1])

        # 正式发布版请注销以下两行代码
        print("配置文件内容如下：")
        for key,vale in self.config_dict.items():
            print(key,'=',vale)
        return msg

    def Check_Revision(self):
        '''
        function:检查更新
        :return:
        isLastestVersion：标记当前软件版本是否为最新版本
        msg：提示信息
        '''
        msg = '' #存放软件运行提示，报错或运行结果等
        isLastestVersion = None    #本地安装的软件是否为最新版本，None检查失败，True是最新，Flase不是最新
        lastest_version = ''
        try:
            # 判断是否从配置文件中读取到内容
            if bool(self.config_dict):
                app_name = self.config_dict['AppName']+" "+self.bit
                current_version = self.config_dict['CurrentVersion']  # 获取当前软件的版本
                print("软件名称：",app_name)
                print("当前版本：",current_version)
                # 拼接查询软件版本的url
                check_version_url ="http://" +self.config_dict['ServerIP'] + "/version/" + app_name
                print("查询软件版本的地址:",check_version_url)
                resp = requests.get(check_version_url)  # 查询服务器上最新的软件版本
                resp.encoding = 'UTF-8'
                # 判断服务器的连接状态
                if resp.status_code == 200:
                    # 如果服务器有响应，需要判断服务器的返回内容
                    if len(resp.text)!=0:
                        # 服务器返回内容不为空，说明查到软件版本了，需要进行版本比较
                        lastest_version = resp.text
                        if lastest_version == current_version:
                            # 如果已经是最新版本，提示用户
                            isLastestVersion=True
                            msg = '【版本检测】客户端版本已经是最新版，无需更新'
                        else:
                            isLastestVersion = False
                            msg = f'当前客户端软件名称为：{app_name}，当前版本为：{current_version} \n服务器上最新版本为：{lastest_version}'
                            print(f'当前客户端软件名称为：{app_name}，当前版本为：{current_version} \n服务器上最新版本为：{lastest_version}')
                    else:
                        # 服务器返回内容为空，说明没查到信息，提示用户
                        msg = f'【版本检测】未查询到"{app_name}"的最新版本信息'
                else:
                    # 服务器状态码不是200，说明连接有异常，提示用户
                    msg = f'【版本检测】服务器连接失败'

        except requests.exceptions.ConnectionError:
            msg = '【版本检测】服务器连接失败,请检查服务是否启动'
        except:
            msg = "软件运行出现异常，异常原因为：" + str(sys.exc_info()[1])
        return isLastestVersion, lastest_version, msg
    
    def download(self, app_package_name, download_path, unpack_path):
        '''
        下载文件
        :return
        isDownload:下载是否成功
        msg:提示信息
        '''
        isDownload = False

        # 获取解压缩后的文件夹路径
        # 文件夹结构如下：
        # ——D：
        #   |——ALLPart2.2 32-bit.zip
        #   |——ALLPart32-bit
        #       |——update.exe
        #       |——ALLPart.exe
        #       |——settings.ini
        # unpack_path = os.path.join(download_path, self.config_dict['app_name'])
        # unpack_path = download_path
        if not os.path.exists(unpack_path):
            os.makedirs(unpack_path)
        print('压缩包下载地址: ', download_path)
        print('解压缩地址: ', unpack_path)
        msg = ''
        try:

            # 下载链接，根据根链接及工具名称拼接
            download_url = "http://" + self.config_dict['ServerIP'] + "/download/" + app_package_name
            down_data = {"type": 2,
                         "file_path": download_path,
                         "file_name": app_package_name,
                         }

            resp = requests.get(url=download_url,params=down_data)
            resp.encoding = 'UTF-8'
            download_file_name = download_path + '/' + app_package_name
            # download_file_name示例：C:\Users\ytw2879\Desktop\temp\其他
            if resp.status_code == 200:
                # 将文件保存到指定路径（包含完整路径、文件名称和文件后缀）
                with open(download_file_name, "wb") as file:
                    file.write(resp.content)
                print(app_package_name,'下载完成')

                # 解压文件，将文件解压到目标路径下
                shutil.unpack_archive(
                    filename = download_file_name,
                    extract_dir = unpack_path
                )
                isDownload = True
            elif resp.status_code == 404:
                msg = f'服务器上无文件“{app_package_name}”！'
            else:
                msg = '服务器连接失败'
            msg = '软件更新成功！'
        except:
            msg = '下载最新版安装包失败，失败原因：' + str(sys.exc_info()[1])
        return isDownload, msg

if __name__ == "__main__":
    # 主程序中调用方法如下：
    update = Update()
    save_path = os.path.dirname(os.path.realpath(sys.argv[0])) #获取当前路径
    msg = update.Parse_Config()   #读取本地配置文件
    isLastestVersion = None
    if not msg:
        isLastestVersion, lastest_version, msg = update.Check_Revision() #检查是否为新版本
        app_package_name = update.config_dict['AppName']+lastest_version+' '+update.bit+'.zip'
    else:
        win32api.MessageBox(0, msg, "提示", win32con.MB_OK)
    if isLastestVersion !=None:  #如果检测到了有最新版本
        if os.name == 'nt':
            cmd = 'taskkill /IM AllPart.exe /f'
        try:
            os.system(cmd)
            print('Allpart进程已关闭')
        except Exception as e:
            print(e)
        isDownload, msg =update.download(app_package_name, save_path, save_path)
    win32api.MessageBox(0, msg, "提示", win32con.MB_OK)

