# 南邮校园网认证原理

portal原理

<https://support.huawei.com/enterprise/zh/doc/EDOC1100126895/609549d8>

1. 向学校的接入设备发送HTTP连接请求。接入设备将我重定向至"<http://10.10.244.11/"，即定位到"https://p.njupt.edu.cn/"。>
2. 所以p.njupt.edu.cn就是Portal服务器域名，向p.njupt.edu.cn发送GET请求，返回认证页面。依据JavaScript脚本运行page.run
3. 发送认证请求，通知客户端向接入设备发送认证请求，发送认证请求

具体过程看上面的链接

## 接口

portal服务器：p.njupt.edu.cn:80

接入设备：p.njupt.edu.cn:802

1. loadConfig

/eportal/portal/page/loadConfig?callback=dr1001&program_index=&wlan_vlan_id=0&wlan_user_ip=MTAuMTM2LjE2MC4yMDY%3D&wlan_user_ipv6=&wlan_user_ssid=&wlan_user_areaid=&wlan_ac_ip=&wlan_ap_mac=000000000000&gw_id=000000000000&jsVersion=4.X&v=10414&lang=zh

1. online_list

/eportal/portal/online_list?callback=dr1002&user_account=&user_password=&wlan_user_mac=000000000000&wlan_user_ip=176726222&curr_user_ip=176726222&jsVersion=4.X&v=4182&lang=zh

1. login

/eportal/portal/login?callback=dr1003&login_method=1&user_account=账户&user_password=密码&wlan_user_ip=10.136.160.206&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=zh-cn&v=4028&lang=zh

1. logout

/eportal/portal/logout?callback=dr1003&login_method=1&user_account=drcom&user_password=123&ac_logout=1&register_mode=1&wlan_user_ip=10.136.160.206&wlan_user_ipv6=&wlan_vlan_id=0&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&v=7267&lang=zh

```python
import requests


def login():
    account = 密码
    password = 账户

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


if __name__ == "__main__":

    # logout()
    login()
```
