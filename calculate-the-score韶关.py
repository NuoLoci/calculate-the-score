import re
import time

import requests
from bs4 import BeautifulSoup

from selenium import webdriver


def geturl():
    initurl = input("请输入你学校的网址(例如http://jwc.sgu.edu.cn)")
    initurl = initurl +'/jsxsd'

    username = input("请输入你的学号")
    userpassword = input("请输入你的密码")

    browser = webdriver.Edge(executable_path='msedgedriver.exe')
    #定义webdriver所在的位置
    browser.get(initurl)
    time.sleep(1)

    browser.find_element_by_id('userAccount').send_keys(username)
    #定位到输入选框，输入账号
    browser.find_element_by_id('userPassword').send_keys(userpassword)
    #定位到输入选框，输入密码
    browser.find_element_by_id('btnSubmit').click()
    #定位到确认选框，模拟点击操作
    time.sleep(1)
    #需要给电脑1秒钟的反应时间

    browser.get(initurl + "/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ")
    #跳转到对应的成绩查询界面
    time.sleep(1)

    choose_button = webdriver.support.ui.Select(browser.find_element_by_id('kksj'))
    choose_button.select_by_index(0)
    #选择到成绩查询对应选框
    browser.find_element_by_id('btn_query').click()
    #找到对应的按钮点击
    time.sleep(1)

    windows = browser.window_handles
    #窗口定位到当前窗口
    browser.switch_to.window(windows[-1])
    #选择最新打开的一个窗口
    browser.current_window_handle 
    #定位到当前浏览器窗口
    url = browser.current_url
    #定位到当前浏览器url
    time.sleep(1)

    f = open('成绩数据网页.html','wb')
    f.write(browser.page_source.encode("gbk", "ignore"))
    f.close()
    browser.quit()

def seeurl():
    f = open('成绩数据网页.html','rb')
    soupstr = str(BeautifulSoup(f,'lxml'))
    f.close()

    sign = re.compile(r'align="left">(.+)?<',re.M)
    #根据正则表达式查找所有的课程名
    classcall = sign.findall(soupstr)
    classcall = classcall[1::2]

    sign = re.compile(r'<td>(.+)?</td>')
    #根据正则表达式查找所有td子串
    classall = sign.findall(soupstr)

    #学分列表
    credit = []
    #绩点列表
    GPA = []
    #课程属性
    classtype = []
    #课程字典
    classdict = {}
    #挂科列表
    linkeddepartments = []

    #整理学分，绩点,课程属性列表
    for index in range(len(classall)):
        if (index+7)%9 == 0:
            credit.append(classall[index])
        if (index+4)%9 == 0:
            GPA.append(classall[index])
        if (index+1)%9 == 0:
            classtype.append(classall[index])

    #将所有的列表打包
    classname = list(zip(classtype,credit,GPA,classcall))
    print(classname)

    #将字典赋值0
    for index in range(len(classname)):
        classdict[classname[index][0]] = 0

    #整理字典
    for index in range(len(classname)):
        if eval(classname[index][2]) > 0:
            if classdict[classname[index][0]] != 0:
                classdict[classname[index][0]] = classdict[classname[index][0]] + eval(classname[index][1])
            else:
                classdict[classname[index][0]] = eval(classname[index][1])
        else:
            linkeddepartments.append(classname[index][3])

    #最终输出结果
    print("学分情况如下\n",classdict)
    
    #挂科结果
    if linkeddepartments:
        print("挂科科目如下\n",linkeddepartments)
    else:
        print("非常棒，目前暂无挂科记录")

def __init__():
    print("该软件是Maplelove写的，不做盈利，只方便大家查学分情况")
    print("仅适用于强智科技构筑的学校教务系统，不适用于其他学校")
    geturl()
    seeurl()
    input("目前的结果已经查询完毕啦")

__init__()
