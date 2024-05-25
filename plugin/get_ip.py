import socket
import requests

# # 公网ip
# res = requests.get('http://myip.ipip.net', timeout=5).text
# print(res)  # 当前 IP：121.229.106.244  来自于：中国 江苏 南京  电信

# # 非公网ip
# # 函数 gethostname() 返回当前正在执行 Python 的系统主机名
# res = socket.gethostbyname(socket.gethostname())
# print(res)  # 192.168.56.2


# 它还适用于所有公共、私有、外部 IP。这种方法在 Linux、Windows 和 OSX 上很有效。
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


print(extract_ip())
