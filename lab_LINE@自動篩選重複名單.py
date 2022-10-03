from selenium import webdriver
import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# --- main program ---
def main():
    pass


# --- 抓取LINE@ 相關data ---
class LINE官方開發:
    def __init__(self, lineId, ChannelId, userChannelId):
        # --- 使用一般 LINE Account Login ---
        self.loginUrl = 'https://access.line.me/oauth2/v2.1/login?loginState=mk5NtzsIlxOIHFR981IBcb&loginChannelId=1576775644&returnUri=%2Foauth2%2Fv2.1%2Fauthorize%2Fconsent%3Fscope%3Dprofile%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Faccount.line.biz%252Flogin%252Fline-callback%26state%3DBybOk7sQn6vMGJfB%26client_id%3D1576775644#/'
        # --- 帳號頁面 ---
        self.accountPage = 'https://manager.line.biz/account/'+lineId           # 輸入您LINE官方帳號專屬ID
        # --- 聊天頁面 ---
        self.messagePage = 'https://chat.line.biz/'+ChannelId                    # 輸入您LINE官方帳號 ChannelId
        # --- 聯絡人葉面 ---
        self.contactPersonPage = 'https://chat.line.biz/'+ChannelId+'/contact'   # 輸入您LINE官方帳號 ChannelId
        # --- 私訊頁面 ---
        self.sendMessagePage = 'https://chat.line.biz/U12900499ce18e43e7ef96ecfe631ff6e/chat/' + userChannelId

    # --- selenium 初始化 ---
    def 初始化(self):
        # ------- selenium webdriver 初始化 -------
        print('初始化作業...')
        opts = Options()  # 使用開發人員模式
        try:
            path = 'C:/Users/user/python/crawler/chromedriver_v103/chromedriver.exe'  # FilePath_chromedriver.
            # ------- 開發人員選項 -------
            opts.add_argument("--incognito")  # 使用無痕模式開啟 browser.
            # opts.add_argument("--headless")  # 不開啟實體瀏覽器, 背景執行.
            # opts.add_argument("--disable-plugins")  # 禁止載入外掛, 增加速度。可以透過about: plugins 頁面檢視效果.
            opts.add_argument("--incognito")  # 隱身模式啟動.
            # ------- 偽造user-agent -------
            ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
            opts.add_argument(f'user-agent={ua}')  # 偽造 user-agent
            # ------- 啟動/定義 driver -------
            self.driver = webdriver.Chrome(executable_path=path,
                                           chrome_options=opts)
            # self.driver.set_window_size(570, 812)  # set window size.
        except:
            print('請更換 chromedriver')

    # --- goto page ---
    def get(self, url):
        print('前往頁面...')
        self.driver.get(url)

    def login(self, email, password):
        print('登入頁面作業...')
        # --- 頁面加載緩衝, 定義尋找元素 ---
        # --- email input label ---
        tid = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'tid')))
        # --- password input label ---
        tpasswd = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'tpasswd')))

        # --- input email and password ---
        tid.send_keys(email)
        tpasswd.send_keys(password)
        print('登陸成功!\n')

    def cookieLogin(self):
        pass

    # --- share message to all user ---
    def sendMessage(self, userChannelId):
        print('自動私訊息廣播作業...')
        print(f'共計抓取: {len(userChannelId)}筆 user data')

    def outputData(self, data, fileName):
        print('匯出檔案作業...')
        print(f'共計讀取: {len(data)}筆 data, 準備匯出檔案')

        select = str(input('請先確認檔案名稱正確(y/n): '))

        if select == 'y':
            try:
                with open(fileName+'.txt', mode='wb', encoding='utf-8') as f:
                    f.write(data)
                    f.close()
            except:
                print('程式出現未知錯誤, 檔案匯出失敗')
        elif select == 'n':
            print('取消檔案匯出作業.')
        else:
            print(f'您輸入了: {select}, 並沒有此選項')

    # --- get user channel ID ---
    def getUserChannelId(self):
        print('抓取 User Channel ID 作業...')

        userChannelId = []

        print(f'共計取得: {len(userChannelId)}筆 User Channel ID')
        return userChannelId


class UI:
    def __init__(self):
        pass

    def control(self):
        pass


if __name__ == '__main__':
    main()


