import re
import datetime
import requests
import pandas
import json
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from account import ACCOUNT


def Checking_Tickets(data):
    # 购票
    # 准备发送url，数据和请求头
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'
    data = {
        'leftTicketDTO.train_date': data['train_date'],
        'leftTicketDTO.from_station': data['from_station_code'],
        'leftTicketDTO.to_station': data['to_station_code'],
        'purpose_codes': 'ADULT',
    }
    headers = {
        'Cookie': '_uab_collina=168224976379483748225314; JSESSIONID=B319717F46133A844870C7EC7BFF3008; BIGipServerotn=2547450122.24610.0000; BIGipServerpassport=988283146.50215.0000; RAIL_EXPIRATION=1682580025509; RAIL_DEVICEID=h43v5lhic0x_HKaTqGVAFPQYyvVSGy1bIGPS_zTgd_aoNS7X72ZYlemi4Dvw82B9k6hPpTPukHRWhpgsGwreeQEt8wfpZXDd_O3bzOjFQwHR1W958lgWNmqYm404WrhTrAqNg7D2y6lFkrwN4C4k19oU-XEieqBY; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; fo=vy7nxh7ym0v4hiq9DgB3chm9Ju4nBwdM3-ODM_qkUoZHPDacNtrKYuEwpqsPLi9MkN8dCWUHAFj39Ax77MbL4tZyd5VcEWCZpmUZDAcvc1oKhF62DxivEstIMAGAolIsLgxyRuaGUvFU981fiVaJltXqbgWRhp0zQVFzjJuGPmwTChHMJGQiw-3YCoU; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5E7F%u5DDE%2CGZQ; _jc_save_fromDate=2023-04-23; _jc_save_toDate=2023-04-23; _jc_save_wfdc_flag=dc',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, params=data, headers=headers)  # 以get方式发送请求
    response.encoding = response.apparent_encoding  # 自动识别编码
    result = response.json()['data']['result']  # 获取返回数据
    # page = 0
    list = []
    for index in result:
        index_list = index.split('|')
        Num = index_list[3]  # 车次
        Start = index_list[8]  # 出发时间
        End = index_list[9]  # 到达时间
        Use_Time = index_list[10]  # 耗时
        Top = index_list[32]  # 特等座
        First = index_list[31]  # 一等座
        Second = index_list[30]  # 二等座
        Advanced_Soft_Sleeper = index_list[21]  # 高级软卧
        Soft_Sleeper = index_list[23]  # 软卧
        Mobile_Sleeper = index_list[33]  # 动卧
        Hard_Sleeper = index_list[28]  # 硬卧
        Soft_Seat = index_list[27]  # 软座
        Hard_Seat = index_list[29]  # 硬座
        No_Seat = index_list[26]  # 无座
        data = {
            'Num': Num,
            'Start': Start,
            'End': End,
            'Time': Use_Time,
            'Top': Top,
            'First': First,
            'Second': Second,
            'GRW': Advanced_Soft_Sleeper,
            'RW': Soft_Sleeper,
            'DW': Mobile_Sleeper,
            'YW': Hard_Sleeper,
            'RZ': Soft_Seat,
            'YZ': Hard_Seat,
            'WZ': No_Seat
        }
        # 将没有数据的值转化为NaN
        for key in data:
            val = data[key]
            if val == '':
                data[key] = 'NaN'
        # for i in index_list:
        #     print(i)
        #     print('-----', page)
        #     page += 1
        # print(data)
        list.append(data)

    # 展示所有行和列
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    # 保存数据
    content = pandas.DataFrame(list)
    # content.to_csv('data.csv', sep="|")
    print(content)


def Ticketing(data, num):
    # 购票
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=option)
    driver.get(r'https://kyfw.12306.cn/otn/resources/login.html')

    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    driver.execute_script(script)

    driver.find_element(By.XPATH, '//*[@id="J-userName"]').send_keys(ACCOUNT.account_12306)  # 输入账号
    driver.find_element(By.XPATH, '//*[@id="J-password"]').send_keys(ACCOUNT.password_12306)  # 输入密码
    # time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="J-login"]').click()  # 点击登录

    driver.implicitly_wait(10)  # 设置隐式等待
    # 通过滑块验证
    action = ActionChains(driver)
    span = driver.find_element(By.XPATH, '//*[@class="nc_iconfont btn_slide"]')
    action.click_and_hold(span)
    for i in range(5):
        # perform()立即执行动作链
        # move-by-offset（x，y）：水平方向竖直方向
        action.move_by_offset(65, 0).perform()
    # 释放动作链
    action.release()

    # 点击购票
    driver.find_element(By.XPATH, '//*[@id="link_for_ticket"]').click()

    # 输入出发地
    driver.find_element(By.XPATH, '//*[@id="fromStationText"]').click()
    driver.find_element(By.XPATH, '//*[@id="fromStationText"]').clear()
    driver.find_element(By.XPATH, '//*[@id="fromStationText"]').send_keys(data['from_station'])
    driver.find_element(By.XPATH, '//*[@id="fromStationText"]').send_keys(Keys.ENTER)

    # 输入目的地
    driver.find_element(By.XPATH, '//*[@id="toStationText"]').click()
    driver.find_element(By.XPATH, '//*[@id="toStationText"]').clear()
    driver.find_element(By.XPATH, '//*[@id="toStationText"]').send_keys(data['to_station'])
    driver.find_element(By.XPATH, '//*[@id="toStationText"]').send_keys(Keys.ENTER)

    # 输入出发时间
    driver.find_element(By.XPATH, '//*[@id="train_date"]').click()
    driver.find_element(By.XPATH, '//*[@id="train_date"]').clear()
    driver.find_element(By.XPATH, '//*[@id="train_date"]').send_keys(data['train_date'])

    # 点击查询
    driver.find_element(By.XPATH, '//*[@id="query_ticket"]').click()

    # num = 1  # 购买第几列的车票，num=((n-1)*2)+1
    num = (num*2)+1
    # 点击预定
    try:
        driver.find_element(By.XPATH, f'//*[@id="queryLeftTable"]/tr[{num}]/td[13]/a').click()
    except selenium.common.exceptions.NoSuchElementException:
        return '该列车车票以售空'

    # 选择乘车人
    driver.find_element(By.XPATH, '//*[@id="normal_passenger_id"]/li/label').click()
    # 点击提交
    driver.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()
    time.sleep(5)  # 等待确认按钮加载
    # 点击确认
    # 把下面这行的代码注释去掉就能点击确定提交订单
    # try:
    #     driver.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
    # except selenium.common.exceptions.NoSuchElementException:
    #     return '该列车车票以售空'
    return '下单成功，请尽快前往支付'


def run():
    # 读取城市文件
    with open(r'D:\Spiders\12306py\city.json', 'r', encoding='utf-8') as f:
        data = f.read()
    city = json.loads(data)

    while True:
        try:
            from_station = input('输入出发城市：')
            from_station_code = city[from_station]
            break
        except KeyError:
            print('请输入正确的城市名')
    while True:
        try:
            to_station = input('输入到达城市：')
            to_station_code = city[to_station]
            break
        except KeyError:
            print('请输入正确的城市名')
    while True:
        train_date = input('出发时间(格式：xxxx-xx-xx)：')
        if not re.match('\d{4}-\d{2}-\d{2}', train_date):
            print('请输入正确格式的出发时间(xxxx-xx-xx)')
            continue
        date_time = datetime.datetime.strptime(train_date, "%Y-%m-%d")
        now = datetime.datetime.today()
        time = now + datetime.timedelta(days=14)
        if date_time > time or date_time < now:
            print('该时间暂无售票信息，请重新输入出发时间')
        else:
            break

    data = {
        'from_station': from_station,
        'to_station': to_station,
        'train_date': train_date,
        'from_station_code': from_station_code,
        'to_station_code': to_station_code
    }

    Checking_Tickets(data)
    while True:
        try:
            num = int(input('选择要购票的序号或输入-1退出：'))
            break
        except ValueError:
            print('请输入正确的序号')
    if num == -1:
        return
    result = Ticketing(data, num)
    print(result)


if __name__ == '__main__':
    run()
