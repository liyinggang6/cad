# -*- coding: utf-8 -*-
import requests,sys
import os,shutil
import win32api, win32con

class Update:

    def __init__(self):
        self.config_file_path = "settings.ini"
        self.root = None
        self.config_dict = {}


    def Parse_Config(self):
        '''
        function:解析settings.ini文件，从文件中读取配置，放在self.config_fict中
        '''

        msg = ''
        try:
            # 导入解析ini文件的包
            import configparser
            config = configparser.ConfigParser()    #类实例化
            config.read(self.config_file_path)
            # 读取软件版本号
            current_version = config['AppInfos']['CurrentVersion']
            self.config_dict.update({'current_version': current_version})

            # 读取软件名称
            app_name = config['AppInfos']['AppName']
            self.config_dict.update({'app_name': app_name})

            # 读取服务器地址
            server_ip = config['ServerInfos']['ServerIP']
            self.config_dict.update({'server_ip': server_ip})

            # 读取服务器端口号信息
            server_port = config['ServerInfos']['port']
            self.config_dict.update({'server_port': server_port})

            # 拼接url地址
            root_url = "http://" + server_ip + ":" + server_port + "/"
            self.config_dict.update({'root_url': root_url})
        except FileNotFoundError:
            msg = "配置文件未找到!"
        except:
            msg = "配置文件解析出现异常!异常原因为：" + str(sys.exc_info()[1])

        # 正式发布版请注销以下两行代码
        print("配置文件内容如下：")
        print(self.config_dict)
        return msg


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
        print('download_path: ', download_path)
        print('unpack_path: ', unpack_path)
        msg = ''
        try:

            # 下载链接，根据根链接及工具名称拼接
            download_url = self.config_dict['root_url'] + "download/" + app_package_name
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
        except:
            msg = '下载最新版安装包失败，失败原因：' + str(sys.exc_info()[1])
        return isDownload, msg



    def Check_Revision(self):
        '''
        function:检查更新
        :return:
        isLastestVersion：标记当前软件版本是否为最新版本
        msg：提示信息
        '''

        msg = str() #存放软件运行提示，报错或运行结果等
        isLastestVersion = True    #标志本地安装的软件是否为最新版本，默认值为True
        lastest_version = ''
        try:
            msg = self.Parse_Config()
            # 判断是否从配置文件中读取到内容
            if bool(self.config_dict):
                app_name = self.config_dict['app_name']
                current_version = self.config_dict['current_version']  # 获取当前软件的版本

                # 拼接查询软件版本的url
                check_version_url = self.config_dict['root_url'] + "version/" + app_name
                print(check_version_url)
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


    def Auto_Update(self):
        '''
        比较软件版本是否是最新，不是最新的自动下载安装包
        :return:
        msg：提示信息
        '''
        isDown = False
        try:
            isLastestVersion, lastest_version, msg = self.Check_Revision()

            # 若软件不是最新版，主要下载安装包
            if not isLastestVersion:
                isUpdate = win32api.MessageBox(0, msg + '\n 是否更新？', "选择", win32con.MB_YESNO)
                print(isUpdate)
                if isUpdate == 6:
                    # 为6代表用户选择更新
                    # 下载的安装包存储在当前exe的上一级目录下
                    unpack_path = os.path.dirname(os.path.realpath(sys.argv[0]))
                    download_path = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
                    # download_path = r'C:\Users\ytw2879\Desktop\temp\laji'
                    print('压缩包将下载至目录：' + download_path)
                    # 安装包名称，需得是zip格式
                    # 谢工2022.10.12日需求：
                    # 压缩包名称规则如下："ALLPart 32-bit"+".zip"中的空格替换成新版本号加空格=压缩包文件名
                    # !-----------以下是规划的压缩包文件名
                    #
                    # ALLPart3.0 32-bit
                    # ALLPart3.0 64-bit
                    #
                    # ALLPart3.2 32-bit
                    # ALLPart3.2 64-bit
                    #
                    # ALLPart3.6 32-bit
                    # ALLPart3.6 64-bit
                    app_package_name = self.config_dict['app_name'].replace(' ', lastest_version+' ')+'.zip'
                    print(app_package_name)
                    isDownload, msg =self.download(app_package_name, download_path, unpack_path)
                    isDown = isDownload
                    if isDownload:
                        msg = "更新完成！"
                if isUpdate == 7:
                    # 为7代表用户取消更新
                    msg = ''

        except:
            msg = "自动更新出现异常，异常原因为：" + str(sys.exc_info()[1])
        return  isDown, msg

if __name__ == "__main__":
    # 主程序中调用方法如下：
    update_service = Update()
    isDown, msg = update_service.Auto_Update()
    # 弹出提示框
    import win32api, win32con
    if(len(msg)!=0):
        win32api.MessageBox(0, msg, "提示", win32con.MB_OK)

    # root_url = "http://127.0.0.1:80/"

