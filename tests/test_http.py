import pytest
import requests
from plugin.main import extract_ip


def login(account: str, password: str):
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
    return response.text


def logout():
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
    return response.text


def test_login():
    assert login('B21090519@njxy',
                 'Xwj20021114.') == 'dr1003({"result":1,"msg":"Portal协议认证成功！"});'


def test_logout():
    assert logout() == 'dr1003({"result":1,"msg":"Radius注销成功！"});'
