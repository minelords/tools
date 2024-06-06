import time
import requests
import json
import random
import string
import re

def get_code(email):
    url="http://142.171.234.219:5000/api/v1?email={}".format(email)

    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()

        # 假设你想要获取的参数名是'param_name'
        # 你可以通过键值对的方式来获取这个参数的值
        param_value = data.get('title')
        code=re.search(r'([0-9]{6})',param_value)
        # 打印参数值
        return code.group(1)
    else:
        # 请求失败，打印错误信息
        print(f'请求失败，状态码：{response.status_code}')

def get_random_mail():
    email="".join(random.choices(string.ascii_lowercase, k=random.randint(2,9)))
    return email


if __name__=="__main__":
    print(get_code("ytw@llllll.love"))