import time
from time import sleep
from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import sys

import random
import requests
from newsapi import NewsApiClient


import pyautogui  # 控制滑鼠與鍵盤的套件.


def main():
    run = LineBot()                   # import class
    run.initialize()                  # initialize selenium

    mail = 'h9y0c7hw81tn@gmail.com'
    password = '1qaz12345'

    run.get()                         # 取得頁面
    run.login(mail=mail,              # 登入帳號
              password=password)

    runLen = run.getACCTfansNumber()  # 抓取帳號粉絲數

    # data = run.getUserID(runLen)      # get user id, 前往"元宵大代幣大放送"頁面
    # run.outputFile(ACCTiD=data)       # 名單數據匯出作業

    data = run.getUserData(runLen)
    run.outputFile(data)

    # message = '晚上好'
    # run.sendMessage(data,
    #                 message)          # 自動化廣播私訊

    input('輸入任意按鍵結束程式:\t')


# LINE@ 廣播程式
class LineBot:
    def __init__(self):
        self.driver = None
        # self.baseUrl = 'https://account.line.biz/login?redirectUri=https%3A%2F%2Fmanager.line.biz%2F'  # LINE 官方登入頁面
        self.baseUrl = 'https://manager.line.biz/'  # LINE 官方登入頁面

        # --- 無人使用帳號 ---
        # 1. input LINE@ 專屬編碼
        # 2. input LINE@ 專屬ID
        # self.LineChannelCode = 'Ub67b2090a321206cc7bbb33769de6302'  # 測試帳號
        # self.LineChannelID = '@201vivlj'                            # 測試帳號
        #
        self.LineChannelCode = 'Ufff9d93c88ec397800331d041fbdb507'  # 正式帳號
        self.LineChannelID = '@395pdxuu'                            # 正式帳號

    def note(self):
        # --- 圖形驗證碼輸入 ---
        # 帳密打錯
        # IP臭掉
        pass

    # initialize selenium
    def initialize(self):
        opts = Options()  # developer vision
        path = "C:/Users/user/python/crawler/chromedriver_v110/chromedriver.exe"  # FilePath_chromedriver.
        # 開發人員選項
        opts.add_argument("--incognito")        # 使用無痕模式開啟 browser.
        # opts.add_argument("--headless")         # 不開啟實體瀏覽器, 背景執行.
        opts.add_argument("--disable-plugins")  # 禁止載入外掛, 增加速度。可以透過about: plugins 頁面檢視效果.
        opts.add_argument("--incognito")        # 隱身模式啟動.
        # create user-agent (模擬手機 user-agent)
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        opts.add_argument(f'user-agent={ua}')  # fake user-agent
        # opts.add_experimental_option('mobileEmulation', {'deviceName': 'Responsive'})  # 模拟iPad Air
        # start driver
        try:
            self.driver = webdriver.Chrome(executable_path=path,
                                           chrome_options=opts)
            self.driver.set_window_size(1920, 1080)
        except:
            print('請更換chromedriver')

    # 取得頁面
    def get(self):
        self.driver.get(self.baseUrl)  # 前往登入頁面

    # 登入帳號
    def login(self, mail, password):
        self.driver.get(self.baseUrl)  # 前往登入帳號頁面

        # 使用LINE商用帳號登入
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[3]/div[2]/a'))).click()     # click "使用商用帳號登入"
        sleep(3)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(str(mail))                       # input 註冊信箱
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(str(password))                # input 註冊密碼
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[5]/button'))).click()  # click "登入"
        sleep(3)

    # 測試登入方法
    def adminLogin(self, mail, password):
        print(f'註冊信箱: {mail}')
        print(f'註冊密碼: {password}')

        # use  private LINE account login url
        url = 'https://access.line.me/oauth2/v2.1/login?returnUri=%2Foauth2%2Fv2.1%2Fauthorize%2Fconsent%3Fresponse_type%3Dcode%26client_id%3D1576775644%26redirect_uri%3Dhttps%253A%252F%252Faccount.line.biz%252Flogin%252Fline-callback%26scope%3Dprofile%26state%3DrTrdS6vY9dI75aZj&loginChannelId=1576775644&loginState=DRxVSnITNBN7xD25BFEf7C#/'
        self.driver.get(self.baseUrl)  # 使用私人LINE帳號登入
        sleep(3)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div/form/div/input'))).click()
        sleep(3)
        # 輸入註冊信箱
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/form/fieldset/div[1]/input'))).send_keys(str(mail))
        # 輸入註冊密碼
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/form/fieldset/div[2]/input'))).send_keys(str(password))

        # 使用一般LINE帳號登入
        print(f'緩存休息10秒, 請在這時間內輸入圖形驗證碼')
        sleep(10)
        # 點擊 登入按紐
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/form/fieldset/div[4]/button'))).click()

        print(f'緩存休息 10 秒, 請在這時間內輸入手機驗證碼')
        for i in range(10):
            print(f'休息第: {int(i)}秒')
            sleep(1)

        print(f'抓取token...')
        token = self.driver.execute_script('return window.localStorage.getItem("token");')
        print(token)

        # 以下為 使用 requests 抓取 token的方法
        # 抓取登入後的token
        # 設定 HTTP headers
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        # }
        #
        # response = requests.get(url, headers=headers)  # send requests
        # token = response.headers.get("Authorization")  # 從 HTTP headers 中取得 JWT token

        # 如果該網站的 JWT token 是放在 response body 裡，則可以透過下面的方式取得
        # token = response.json().get("token")

        # print(token)  # output token

        # # 设置请求头中的 token
        # token = 'your_token'
        # headers = {'Authorization': 'Bearer ' + token}
        #
        # # 向指定 URL 发送 GET 请求，并在请求头中添加 token
        # response = requests.get(url, headers=headers)
        #
        # print(response.text)  # output response txt

    # 抓取帳號粉絲數
    def getACCTfansNumber(self):
        url = 'https://manager.line.biz/account/'+self.LineChannelID
        self.driver.get(url)
        sleep(3)

        bs = BeautifulSoup(self.driver.page_source, 'html.parser')
        for i in bs.find_all('span', {'class': 'mr-3 cursor-pointer'}):  # target_element
            fansNumber = i.text

        fansNumber = fansNumber.replace(',', '')

        print(f'抓取得到的粉絲數量: {int(fansNumber)}')
        print(f'推估需要加載次數: {int(int(fansNumber)/10)}')

        return int(int(fansNumber)/10)

    # Get User ID, Name
    def getUserData(self, runLen):
        print(f'抓取官方名單數據作業...')
        datasetUserInformation = {"ID": [],
                                  "Name": []}

        url = 'https://chat.line.biz/'+self.LineChannelCode+'/contact'  # url_聯絡人頁面
        self.driver.get(url)
        sleep(3)
        try:  # 例外處裡, if 出現惱人的對話框
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="page"]/div[2]/div[2]/div/div/div[2]/button'))).click()
        except:
            pass
        sleep(5)

        # 頁面加載作業, 模擬滑鼠滾輪作業, 加載所有的名單數據
        targetXpath = '//*[@id="content"]/div/div[3]/table/tbody/tr[1]'
        self.driver.find_element_by_xpath(targetXpath).click()  # 點擊第一個聊天對象

        print(f'共計加載頁面: {runLen}.')
        for i in range(int(runLen)):  # 實際執行次數+5
            print(f'加載第:{i}頁')
            pyautogui.keyDown('pagedown')
            sleep(1)

        # 抓取 User ID
        try:
            bs = BeautifulSoup(self.driver.page_source, 'html.parser')
            for i in bs.find_all('a', {'class': 'btn btn-sm btn-outline-primary'}):
                userID = i.attrs['href']
                datasetUserInformation["ID"].append(userID+'\n')

            print(f'共計抓取: {len(datasetUserInformation["ID"])}筆 User ID')
        # 抓取 User Name
        # 其次根據抓取得到的 User ID 筆數, 進行抓取對應數量的 User Name
            try:
                for i in range(len(datasetUserInformation["ID"])):
                    i += 1
                    target = "//*[@id='content']/div/div[3]/table/tbody/tr["+str(i)+"]/td[1]/div/div[2]/div[1]/h6/span"
                    UserName = self.driver.find_element_by_xpath(target).text
                    datasetUserInformation["Name"].append(UserName)

                print(f'共計抓取: {len(datasetUserInformation["Name"])}筆 User Name')
                return datasetUserInformation

            except:
                print(f'ERROR: Get User Name')

        except:
            print(f'ERROR: Get User ID')

    # 判斷名單檔案存在與否
    def Check_whetherTheFileExists(self, fileName):
        print(fileName)
        print(os.listdir)           # output folder
        list_localFIle = os.listdir

        if fileName not in list_localFIle:
            print(f'判斷 目標名單數據 尚未存在 目標資料夾內')
        else:                                                           # if 沒有看到目標名單數據,
            print(f'判斷 目標名單數據 存在 目標資料夾內')

    # 匯出官方內名單數據
    def outputFile(self, ACCTinfo):
        print(f'\n名單數據匯出作業...')
        print(f'共計讀取: {len(ACCTinfo["ID"])}筆 User ID')
        print(f'共計讀取: {len(ACCTinfo["Name"])}筆 User Name')
        print(f'匯出檔案名稱: {self.LineChannelID+"_名單數據"}')  # 根據官方ID 命名匯出的名單檔案

        print('\n')
        f = open(str(self.LineChannelID+'_名單數據.txt'), 'w', encoding='utf-8')  # 匯出檔案
        for ID, Name in zip(ACCTinfo['ID'], ACCTinfo['Name']):
            ID = ID.replace(f'{"/"+self.LineChannelCode+"/chat/"}', "").replace('\n', '')  # 篩選值：官方編碼, 多餘的URL
            f.write(f'{ID},{Name}\n')
        f.close()

        print(f'匯出完成_名單數據檔案')

    def 自動化篩選重複名單(self):
        pass

    # 讀取抓取得到的名單檔案
    def readData_UserInfo(self):
        print(f'\n讀取名單作業...')

        # 根據user input LINE Channel Code, 讀取對應的名單數據檔案

        # 若在資料夾內沒有發現對應數據檔案, 就進行抓取名單數據

    def sendMessage(self, data, message):
        print(f'自動化私訊廣播作業...')
        print(f'共計讀取: {len(data)}筆 user ID')

        # 自動化廣播私訊作業
        for i in data:
            成功筆數 = []                             # container_成功私訊
            失敗筆數 = []                             # container_失敗私訊

            url = 'https://chat.line.biz'+str(i)    # 聊天視窗頁面url組成作業
            print(f'前往私訊: {url}')                # output 聊天室視窗頁面
            self.driver.get(url)                    # 前往目標聊天室視窗
            sleep(1)

            try:
                sleep(1)
                print(f'嘗試第一種方式')
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="editor"]/textarea'))).send_keys(str(message)+'\n')
                成功筆數.append(i)
                sleep(1)
            except:
                失敗筆數.append(i)

        # output information
        print(f'共計成功私訊筆數: {len(成功筆數)}')
        print(成功筆數)
        print(成功筆數)
        print('-'*77)

        print(f'共計失敗私訊筆數: {len(失敗筆數)}')
        print(失敗筆數)


if __name__ == '__main__':
    main()
    # run = LineBot()                   # import class
    # run.initialize()
    # mail = 'ian2000xz@gmail.com'
    # password = '2GLLZ6pqZg57Bp0h'
    # run.adminLogin(mail, password)

