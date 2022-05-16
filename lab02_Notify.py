from bs4 import BeautifulSoup
import requests

# --- 爬蟲 ---
# response = requests.get("https://www.udemy.com/course/codegym-python/")
# soup = BeautifulSoup(response.text, "html.parser")
# price = soup.find("span", {"class": "udlite-sr-only"}).getText()[7:]  # 取得文字中的價格部分

price = '3'
print(f'price： {price}')

if int(price) < 5000:  # 將爬取的價格字串轉型為整數
    headers = {
        # "Authorization": "Bearer " + "你的權杖(token)",

        "Content-Type": "application/x-www-form-urlencoded"
    }

    # params = {"message": "\n黃x的雞雞已漲價至" + price + "元"}
    params = {"message": '\n請多多指教😊'}

    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  # 200
