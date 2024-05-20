import requests
import webbrowser
from flowlauncher import FlowLauncher
import sys
import os
import urllib.parse
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))


def login():
    account = 'B21090519@njxy'
    password = 'Xwj20021114.'

    url = 'https://p.njupt.edu.cn:802/eportal/portal/login'
    params = {
        'callback': 'dr1003',
        'login_method': '1',
        # 'user_account': ',0,B21090519@njxy',
        'user_account': account,
        'user_password': password,
        'wlan_user_ip': '10.136.160.206',
        'wlan_user_ipv6': '',
        'wlan_user_mac': '000000000000',
        'wlan_ac_ip': '',
        'wlan_ac_name': '',
        'jsVersion': '4.1.3',
        'terminal_type': '1',
        'lang': 'zh-cn',
        'v': '4028',
        'lang': 'zh'
    }

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    response = requests.get(url, params=params, headers=headers)

    print(response.status_code)
    print(response.text)  # 如果需要查看返回的内容


def logout():
    url = 'https://p.njupt.edu.cn:802/eportal/portal/logout'
    params = {
        'callback': 'dr1003',
        'login_method': '1',
        'user_account': 'drcom',
        'user_password': '123',
        'ac_logout': '1',
        'register_mode': '1',
        'wlan_user_ip': '10.136.160.206',
        'wlan_user_ipv6': '',
        'wlan_vlan_id': '0',
        'wlan_user_mac': '000000000000',
        'wlan_ac_ip': '',
        'wlan_ac_name': '',
        'jsVersion': '4.1.3',
        'v': '7267',
        'lang': 'zh'
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,en-IE;q=0.4',
        'Cookie': '_ga=GA1.1.148507178.1701333449; _ga_J6LT8812GZ=GS1.1.1701333448.1.1.1701334038.0.0.0',
        'Referer': 'https://p.njupt.edu.cn/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        # 其他可能需要的 header
    }

    response = requests.get(url, params=params, headers=headers)

    print(response.status_code)
    print(response.text)  # 如果需要查看返回的内容


def debug_json_rpc(str):
    return [{
        "Title": "title",
        "SubTitle": str,
        "IcoPath": "image/app.png",
        # "jsonRPCAction": {
        #     "method": "cmd_command",
        #     "parameters": [self.cmd]
        # }
    }]


class MessageDTO:
    def __init__(self, operation) -> None:
        self.title = operation["Title"]
        self.subtitle = "Please enter"
        self.image = operation["Image"]
        # todo:无法获得flow launcher客户端的配置设置，只能被调用
        # 无法从配置中获取账号密码,先将就用着吧
        self.cmd = operation["cmd"]

    def asFlowMessage(self) -> dict:
        return {
            "Title": urllib.parse.unquote(self.title),
            "SubTitle": self.subtitle,
            "IcoPath": self.image,
            "jsonRPCAction": {
                "method": "cmd_command",  # 自定义插件的方法
                "parameters": [self.cmd]  # 自定义插件类的参数
            }
        }


class HelloWorld(FlowLauncher):

    messages = []

    def addMessage(self, message: MessageDTO):
        self.messages.append(message.asFlowMessage())

    def query(self,  params: str) -> list:
        operation_list = [
            {
                "Title": "login",
                "SubTitle": "login",
                "Image": "images/app.png",
                "cmd": "login"
            },
            {
                "Title": "logout",
                "SubTitle": "logout",
                "IcoPath": "image/app.png",
                "Image": "images/app.png",
                "cmd": "logout"
            }
        ]
        for operation in operation_list:
            self.addMessage(MessageDTO(operation))
        return self.messages

    def open_url(self, url):
        webbrowser.open(url)

    def cmd_command(self, command):
        if command == "login":
            login()
        elif command == "logout":
            logout()


if __name__ == "__main__":
    HelloWorld()