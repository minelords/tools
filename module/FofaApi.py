from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import base64

def browser(login_url,username,password,info,page):  #返回html信息
    # 配置代理
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = "http://localhost:2080"
    # 创建 Chrome WebDriver 实例，并添加代理选项
    opt = webdriver.ChromeOptions()
    opt.add_argument("--proxy-server=http://localhost:2080")
    #eager加载策略加速
    opt.page_load_strategy = 'eager'

    driver=webdriver.Chrome(options=opt)
    driver.get(login_url)
    driver.find_element(By.ID,"username").send_keys(username)
    driver.find_element(By.ID,"password").send_keys(password)
    yzm=input("请输入验证码:")
    driver.find_element(By.XPATH,"//*[@id='login-form']/table/tbody/tr[3]/td/input[@class='mod_input dl_n']").send_keys(yzm)
    time.sleep(random.random())
    driver.find_element(By.ID,"rememberMe").click()
    driver.find_element(By.ID,"fofa_service").click()
    time.sleep(random.random())
    driver.find_element(By.CLASS_NAME,"mod_but").submit()
    time.sleep(2)

    """需要新建标签页时使用
    js =  "window.open('http://www.baidu.com','_blank');"  #新建标签页
    driver.execute_script(js)     #执行js命令
    driver.switch_to.window(driver.window_handles[1]) #切换到新标签页
    # 在新的标签页打开新的地址
    """

    html_list=[]
    for i in range(1,page+1):
        #关键词
        word=base64.b64encode(bytes(info,'utf-8')).decode('utf-8') #word='fid="4OeA79EXS7Z+DdzkAvrBag==" && country="CN"'
        url="https://fofa.info/result?qbase64={}&page={}&page_size=10".format(word,i)
        driver.get(url)
        html_list.append(driver.page_source) #获取网页源码
    return html_list

#保存url信息
def save(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    body= soup.find_all("span",{"class":"hsxa-host"})
    with open("url.txt","a",newline="") as f: #保存网址
        for b in body:
            tag=b.find_all('a',{"target":"_blank"})
            f.write(str(tag[0].get('href'))+"\n")
            


if __name__=='__main__':
    #登陆信息
    login_url='https://fofa.info/f_login'
    username='2xxxxxx@qq.com' #账号
    password='Zxxxxxxxxxx4' #密码
    info=input("请输入关键词：")
    page=int(input("需要几页？"))
    #进行登陆操作，以便保存cookie
    html_list=[]
    html_list=browser(login_url,username,password,info,page)
    for html_text in html_list:
        save(html_text)
    