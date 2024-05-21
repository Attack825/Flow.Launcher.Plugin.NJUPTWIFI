import os
import sys
import json
import socket
import requests
import webbrowser
import urllib.parse
from flowlauncher import FlowLauncher
from typing import Any, Mapping, Dict

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict


parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))


class JsonRPCRequest(TypedDict):
    method: str
    parameters: list
    settings: NotRequired[dict[Any, Any]]


class JsonRPCClient:

    def send(self, data: Mapping) -> None:
        json.dump(data, sys.stdout)

    def recieve(self):
        try:
            return json.loads(sys.argv[1])
        except (IndexError, json.JSONDecodeError):
            return {'method': 'query', 'parameters': ['']}


def settings() -> Dict[str, Any]:
    """Retrieve the settings from Flow Launcher."""
    return JsonRPCClient().recieve().get('settings', {})

# 它还适用于所有公共、私有、外部 IP。这种方法在 Linux、Windows 和 OSX 上很有效。


def extract_ip():
    url = 'https://p.njupt.edu.cn'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get(url, headers=headers)
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


def debug_str(str):
    return [
        {
            "Title": "Hello World Python's Context menu",
            "SubTitle": str,
            "IcoPath": "Images/app.png",
            "JsonRPCAction": {
                "method": "is_online",
                "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
            }
        }
    ]


class MessageDTO:
    def __init__(self, operation) -> None:
        self.title = operation["Title"]
        self.subtitle = "Please enter"
        self.image = operation["Image"]
        # todo:无法获得flow launcher客户端的配置设置，只能被调用
        # 无法从配置中获取账号密码,先将就用着吧
        self.funcname = operation["FuncName"]
        self.parameters = operation["Parameters"]

    def asFlowMessage(self) -> dict:
        return {
            "Title": urllib.parse.unquote(self.title),
            "SubTitle": self.subtitle,
            "IcoPath": self.image,
            "jsonRPCAction": {
                "method": self.funcname,  # 自定义插件的方法
                "parameters": self.parameters  # 自定义插件类的参数
            }
        }


class HelloWorld(FlowLauncher):

    messages = []

    def addMessage(self, message: MessageDTO):
        self.messages.append(message.asFlowMessage())

    def query(self,  params: str) -> list:
        settings = JsonRPCClient().recieve().get("settings", {})
        account = settings.get("account", None) or None
        password = settings.get("password", None) or None
        operation_list = [
            {
                "Title": "login",
                "SubTitle": "login",
                "Image": "images/app.png",
                "FuncName": "login",
                "Parameters": [account, password]
            },
            {
                "Title": "logout",
                "SubTitle": "logout",
                "Image": "images/app.png",
                "FuncName": "logout",
                "Parameters": []
            },
            {
                "Title": "is_online",
                "SubTitle": "is_online",
                "Image": "images/app.png",
                "FuncName": "is_online",
                "Parameters": ["https://p.njupt.edu.cn:802/eportal/portal/online_list?callback=dr1002"]}
        ]

        for operation in operation_list:
            self.addMessage(MessageDTO(operation))

        return self.messages
        # local_network_ip = extract_ip()
        # return debug_str(local_network_ip)

    def open_url(self, url):
        webbrowser.open(url)

    def context_menu(self, data):
        """
        用于点击->后，显示的菜单选项
        """
        pass
        # return [
        #     {
        #         "Title": "Hello World Python's Context menu",
        #         "SubTitle": "Press enter to open Flow the plugin's repo in GitHub",
        #         "IcoPath": "Images/app.png",
        #         "JsonRPCAction": {
        #             "method": "open_url",
        #             "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
        #         }
        #     }
        # ]

    def login(self, account: str, password: str):
        account = account
        password = password
        local_network_ip = extract_ip()
        url = 'https://p.njupt.edu.cn:802/eportal/portal/login'
        params = {
            'callback': 'dr1003',
            'login_method': '1',
            # 'user_account': ',0,B21090519@njxy',
            'user_account': account,
            'user_password': password,
            'wlan_user_ip': local_network_ip,
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

        # print(response.status_code)
        # print(response.text)  # 如果需要查看返回的内容

    def logout(self):
        url = 'https://p.njupt.edu.cn:802/eportal/portal/logout'
        local_network_ip = extract_ip()
        params = {
            'callback': 'dr1003',
            'login_method': '1',
            'user_account': 'drcom',
            'user_password': '123',
            'ac_logout': '1',
            'register_mode': '1',
            'wlan_user_ip': local_network_ip,
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

        # print(response.status_code)
        # print(response.text)  # 如果需要查看返回的内容
    def is_online(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    HelloWorld()
