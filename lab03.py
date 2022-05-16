# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
# from linebot.models import (MessageEvent, TextMessage, TextSendMessage, LocationSendMessage, ImageSendMessage, StickerSendMessage, FlexSendMessage)
import json
from linebot.models import *
import requests

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi(
    'your channel access token ')

# your linebot message API - Channel secret
handler = WebhookHandler('your Channel secret ')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


# 抓取中央氣象局資料
def get_weather(city):  # 使用該function, user 需要帶入要查詢的城市.
    apiKey = 'CWB-30D6DD6E-CCCB-4BB8-85BD-510C22B37B52'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + apiKey + '&format=JSON&locationName=' + str(city)
    data = requests.get(url)
    # data = (json.loads(data.text,encoding='utf-8'))['records']['location'][0]['weatherElement']
    data = json.loads(data.text)['records']['location'][0]['weatherElement']

    res = [[], [], []]
    for j in range(3):
        for i in data:
            res[j].append(i['time'][j])

    return res


# handle msg
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info & message
    user_id = event.source.user_id
    msg = event.message.text
    user_name = line_bot_api.get_profile(user_id).display_name

    # get msg details
    try:
        print('msg from [', user_name, '](', user_id, ') : ', msg)
    except:
        print('對方沒有加入好友')

    # 查詢天氣Function
    def searchWeather():
        # 天氣狀況 = data[0]['parameter']['parameterName']
        # 降雨機率 = data[1]['parameter']['parameterName']
        # 最高溫度 = data[4]['parameter']['parameterName']
        # 最低溫度 = data[2]['parameter']['parameterName']
        # 舒適度 = data[3]['parameter']['parameterName']

        cities = ['基隆市', '嘉義市', '臺北市', '嘉義縣', '新北市', '臺南市', '桃園縣', '高雄市', '新竹市', '屏東縣', '新竹縣', '臺東縣', '苗栗縣', '花蓮縣',
                  '臺中市', '宜蘭縣', '彰化縣', '澎湖縣', '南投縣', '金門縣', '雲林縣', '連江縣']

        city = msg[3:]
        city = city.replace('台', '臺')
        res = get_weather(city)  # input 要抓取資料的縣市, 再將該function 抓取到的data return.

        if city not in cities:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="天氣查詢格式為: \"天氣 縣市\""))
        else:
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text=city + '未來36小時天氣預測',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://static01.nyt.com/images/2014/05/25/magazine/25wmt/mag-25WMT-t_CA0-master1050.jpg',
                            title='{} ~ {}'.format(data[0]['startTime'][5:-3], data[0]['endTime'][5:-3]),


                            # data[0] = 天氣狀況
                            # data[1] = 降雨機率
                            # data[2] = 最低溫度
                            # data[3] = 舒適度
                            # data[4] = 最高溫度

                            text='天氣狀況 {} \n舒適度 {}\n溫度 {} ~ {} °C\n降雨機率 {}'.format(data[0]['parameter']['parameterName'],
                                                                                 data[3]['parameter']['parameterName'],
                                                                                 data[2]['parameter']['parameterName'],
                                                                                 data[4]['parameter']['parameterName'],
                                                                                 data[1]['parameter']['parameterName'],),
                            actions=[
                                URIAction(
                                    label='詳細內容',
                                    uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                )
                            ]
                        )for data in res
                    ]
                )
            ))

    # --- 辨識關鍵字 ---
    # --- 常用功能關鍵字 ---
    def keyword_疾管署():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(
                                        text='提供給您台灣最新疫情資訊：\n\n--- 衛福部簡訊實聯制民眾資料調閱紀錄查詢服務網站 ---\nhttps://sms.1922.gov.tw/\n\n--- 衛生福利部疾管署官網 ---\nhttps://www.cdc.gov.tw/\n\n--- 最新統計資訊 ---\nhttps://sites.google.com/cdc.gov.tw/2019ncov/taiwan\n'),
                                    # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://images.chinatimes.com/newsphoto/2020-12-10/656/20201210001896.png',
                                        preview_image_url='https://cc.tvbs.com.tw/img/upload/2021/11/11/20211111162332-ea2b7e10.jpg'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='衛生福利部疾病管制署',
                                        latitude=25.04358,
                                        longitude=121.52269)
                                    ])

    def keyword_help():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='10'),  # 貼圖
                                    TextSendMessage(text='為您提供命令列選單：\nhttps://docs.google.com/spreadsheets/d/1KJH3VVdFcO_OkA8LYz2yiHMQJmNJXtuSrZ2qqRP-x0o/edit?usp=sharing'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://tomorrowsci.com/wp-content/uploads/2020/06/hacker-8k-8p-1440x900-1.jpg',
                                        preview_image_url='https://tomorrowsci.com/wp-content/uploads/2020/06/hacker-8k-8p-1440x900-1.jpg'),
                                    ])  # 文字訊息

    def keyword_google搜尋趨勢():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='為您提供最新 google 搜尋趨勢：\nhttps://trends.google.com.tw/trends/trendingsearches/daily?geo=TW'),

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://tomorrowsci.com/wp-content/uploads/2020/06/hacker-8k-8p-1440x900-1.jpg',
                                        preview_image_url='https://cdn2.ettoday.net/images/4927/4927668.jpg'),
                                    ])  # 文字訊息

    def keyword_股票線上資源():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(
                                        text='提供給您股票線上參考資源：\n\n--- GOODINFO ---\nhttps://goodinfo.tw/tw/index.asp/\n\n--- CMONEY ---\nhttps://www.cmoney.tw/forum/popular/buzz\n'),
                                    # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://en.pimg.jp/042/508/329/1/42508329.jpg',
                                        preview_image_url='https://en.pimg.jp/042/508/329/1/42508329.jpg'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='台灣證卷交易所',
                                        latitude=25.03390754249655,
                                        longitude=121.56480999747941)
                                    ])

    # --- 地點關鍵字 ---
    def 淡水捷運站():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您淡水捷運站資訊：'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://live.staticflickr.com/2410/3530634417_6bc39559a3.jpg',
                                        preview_image_url='https://foncc.com/wp-content/uploads/2018/12/20181215121.jpg'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='淡水捷運站',
                                        latitude=25.167947367891387,
                                        longitude=121.44566314974743)
                                    ])

    def keyword_101():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您101資訊'),  # 文字訊息
                                    # ImageSendMessage(original_content_url='https://www.iii.org.tw/assets/images/nav-all/logo.png',
                                    # preview_image_url='https://www.iii.org.tw/assets/images/nav-all/logo.png'),

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://res.klook.com/image/upload/q_85/c_fill,w_750/fl_lossy.progressive/q_auto/blogtw/2018/06/%E5%8F%B0%E5%8C%97101%E8%A7%80%E6%99%AF%E5%8F%B0%E9%96%80%E7%A5%A8.jpg',
                                        preview_image_url='https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/%E5%9C%96%E7%89%872-1638173874.jpg?crop=1.00xw:1.00xh;0,0&resize=640:*'),

                                    LocationSendMessage(
                                        title='Store Location',
                                        address='Taipei 101',
                                        latitude=25.033981,
                                        longitude=121.564506)
                                    ])

        # push text_msg
        # 為主動式訊息, 每月有限額的訊息則數, 超過要付費(免費用戶目前每月僅可傳送500則推播訊息)
        # line_bot_api.push_message(user_id,
        #                           TextSendMessage(text=user_name + ' 您好^^'))

    def keyword_頂溪捷運站():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您頂溪捷運站資訊：'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://yukiblog.tw/wp-content/uploads/img/1VSVS_924C/-6.jpg',
                                        preview_image_url='https://img.ltn.com.tw/Upload/house/page/2015/11/06/151106-30-1-WYh2N.jpg'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='頂溪捷運站',
                                        latitude=25.013904618518488,
                                        longitude=121.5154861836169)
                                    ])

    def keyword_遠東世紀廣場():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您遠東世紀廣場資訊：'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://pic.pimg.tw/leezozo/1457755888-422370469_n.jpg?v=1457755898',
                                        preview_image_url='https://fangmei1688.com.tw/wp-content/uploads/s0015.jpg'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='遠東世紀廣場',
                                        latitude=25.997962517043725,
                                        longitude=121.48565273980469)
                                    ])

    def keyword_南港捷運站():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您南港捷運站資訊：'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://carollin.tw/wp-content/uploads/7b0bc3dff4505193722403b7976a2258.jpg',
                                        preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6IlIGbqLCwkLLhoXb49K8Unj5pwAo4Vk52Q&usqp=CAU'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='南港捷運站',
                                        latitude=25.052177088420695,
                                        longitude=121.60707681360628)
                                    ])

    def keyword_台北捷運路線圖():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您台北捷運路線圖資訊：'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://web.metro.taipei/pages/assets/images/routemap2020.png',
                                        preview_image_url='https://web.metro.taipei/pages/assets/images/routemap2020.png'),
                                    ])

    def keyword_超速冷凍():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您超速冷凍工業股份有限公司資訊：\n\n統一編號:66376718\n代表人：許榮郇(1,351,'
                                                         '500 股)\n董事：許麗珠(158,000 股)\n董事：蔡春稻(990,'
                                                         '500 股)\n監察人：林瑞雄\n資本總額:25,000,000'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIKvfXD6QkOAyl579is4ClnrpNBc0H7IPdBA&usqp=CAU',
                                        preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIKvfXD6QkOAyl579is4ClnrpNBc0H7IPdBA&usqp=CAU'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='超速冷凍工業股份有限公司',
                                        latitude=25.524044977496153,
                                        longitude=121.43382120954556)
                                    ])

    def keyword_公司登記查詢():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供您：\n--- 經濟部公司登記查詢網址 '
                                                         '---\nhttps://findbiz.nat.gov.tw/fts/query/QueryBar'
                                                         '/queryInit.do\n\nP.S. 經濟部長：王美花'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://upload.wikimedia.org/wikipedia/commons/6/6e/Wang_Mei-hua.jpg',
                                        preview_image_url='https://im01.itaiwantrade.com/035b5a9d-d13b-4d7c-b40f-924aa5d8a00e/%E7%B6%93%E6%BF%9F%E9%83%A8logo-%E5%BC%B7%E5%8C%96%E6%95%B8%E4%BD%8D%E8%B2%BF%E6%98%93%E5%8F%8A%E9%9B%BB%E5%AD%90%E5%95%86%E5%8B%99%E6%8E%AA%E6%96%BD.png'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='中華民國經濟部',
                                        latitude=25.028144151403495,
                                        longitude=121.5168678974794)
                                    ])

    def keyword_sean():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='10'),  # 貼圖
                                    TextSendMessage(text='今晚要出發了嗎？\n\n--- 香閣_禮服店 ---\n台北市大安區106號忠孝東路4段270號\n\n--- '
                                                         '冥想_公主店 ---\n106台北市大安區忠孝東路三段303號\n\n--- Come Here Bar, '
                                                         'Angel&Annie 飛鏢酒吧 ---\n106台北市信義區基隆路三段2號\n\n--- 雙喜酒吧 '
                                                         '---\n110台北市信義區松壽路22號3樓\n\n--- Sing! go! 忠孝永春店 '
                                                         '---\n台北市信義區忠孝東路五段297號\n\n--- wave '
                                                         '夜店---\n110台北市信義區松壽路12號7樓\n\n--- 隱士餐酒館 ---\n台北市信義區忠孝東路五段297號'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://pic.pimg.tw/inotanymore/1575305492-2857491791.jpg',
                                        preview_image_url='https://pic.pimg.tw/inotanymore/1575305492-2857491791.jpg')])

    # --- PMC 事業關鍵字 ---
    def keyword_軍用格鬥士林點():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='2'),  # 貼圖
                                    TextSendMessage(text='提供給您軍用格鬥士林上課點資訊：'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    # ImageSendMessage(
                                    #     original_content_url='https://carollin.tw/wp-content/uploads/7b0bc3dff4505193722403b7976a2258.jpg',
                                    #     preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6IlIGbqLCwkLLhoXb49K8Unj5pwAo4Vk52Q&usqp=CAU'),

                                    LocationSendMessage(
                                        title='地理資訊',
                                        address='軍用格鬥_士林上課點',
                                        latitude=25.09199383561895,
                                        longitude=121.5191252970376)
                                    ])

    # --- 幹話關鍵字 ---
    def keyword_幹():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='3'),  # 貼圖
                                    TextSendMessage(text='靠北'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://cdn2.ettoday.net/images/2497/2497309.jpg',
                                        preview_image_url='https://www.moedict.tw/%E5%B9%B9.png')])

    def keyword_靠北():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='3'),  # 貼圖
                                    TextSendMessage(text='幹'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://truth.bahamut.com.tw/s01/201804/470376d973997b34c9ace54a8769de6c.JPG',
                                        preview_image_url='https://www.moedict.tw/%E9%9D%A0%E5%8C%97.png')])

    def keyword_哭喔():
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text='你是在哭喔😂😂')])  # 文字訊息

    def keyword_哭喔v2():
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text='還在哭喔😂😂😂')])  # 文字訊息

    def keyword_欸():
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text='幹嘛')])  # 文字訊息

    def keyword_欸欸():
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text='安安')])

    def keyword_女朋友():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='3'),  # 貼圖
                                    TextSendMessage(text='別做夢了, 你只有左手 右手'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://cdn.hk01.com/di/media/images/dw/20211019/527148419811250176517034.jpeg/47T0cd68_PR44o_DQ1Br3ylSWw1UHGFgQcHP2UHBz9k?v=w1920',
                                        preview_image_url='https://assets.juksy.com/files/articles/85528/800x_100_w-5c0cd63834618.jpg')])

    # --- administrator ---
    def keyword_administrator():
        line_bot_api.reply_message(event.reply_token,
                                   [StickerSendMessage(package_id='1', sticker_id='3'),  # 貼圖
                                    TextSendMessage(text='主人早安~~❤\n\n--- 日常卡路里 Table '
                                                         '---\nhttps://docs.google.com/spreadsheets/d'
                                                         '/1oW0N_f8ga730XSO5LHMkwdlkwr9adycA7ypdAaH9Jjc/edit#gid=0\n\n--- 今日待辦事項 ---\nhttps://docs.google.com/spreadsheets/d/1UHRG-7vodyhD8iLRSrwXYmg256MT1AqF4Rw9yowyi1g/edit?usp=sharing'),  # 文字訊息

                                    # original_content_ur ﹕ 點開圖片後顯示出來的圖片
                                    # preview_image_url ： 傳送訊息的預覽圖
                                    ImageSendMessage(
                                        original_content_url='https://img1.dowebok.com/484.jpg',
                                        preview_image_url='https://tomorrowsci.com/wp-content/uploads/2020/06/hacker-8k-8p-1440x900-1.jpg')])

    def 紅包():
        FlexMessage = json.load(open('Line Pay.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('LINE發送給您母親節紅包, 趕快來領取', FlexMessage))

    # Template Message
    def IanQuinn():
        carousel_template_message = TemplateSendMessage(
            alt_text='Private Menu',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i3.jueshifan.com/7b077d83/790e7f8b/2a5d3fd74ca1fb1c982a.jpg',
                        image_background_color='#FFFFFF',
                        title='Menu1.',
                        text='日常',
                        actions=[
                            URIAction(
                                label='卡路里',
                                uri='https://docs.google.com/spreadsheets/d/1oW0N_f8ga730XSO5LHMkwdlkwr9adycA7ypdAaH9Jjc/edit?usp=sharing'
                            ),
                            URIAction(
                                label='待辦事項',
                                uri='https://docs.google.com/spreadsheets/d/1UHRG-7vodyhD8iLRSrwXYmg256MT1AqF4Rw9yowyi1g/edit?usp=sharing'
                            ),
                            URIAction(
                                label='搜尋趨勢',
                                uri='https://trends.google.com.tw/trends/?geo=TW'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i3.jueshifan.com/7b077d83/790e7f8b/2a5d3fd74ca1fb1c982a.jpg',
                        image_background_color='#000000',
                        title='Menu2.',
                        text='功能',
                        actions=[
                            MessageAction(
                                label='疫情資訊',
                                text='疫情'
                            ),
                            URIAction(
                                label='台股資訊',
                                uri='https://goodinfo.tw/tw/index.asp'
                            ),
                            URIAction(
                                label='公司登記查詢',
                                uri='https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i3.jueshifan.com/7b077d83/790e7f8b/2a5d3fd74ca1fb1c982a.jpg',
                        image_background_color='#000000',
                        title='Menu3.',
                        text='Location',
                        actions=[
                            MessageAction(
                                label='淡水捷運站',
                                text='淡水捷運站'
                            ),
                            MessageAction(
                                label='遠東世紀廣場',
                                text='遠東世紀廣場'
                            ),
                            MessageAction(
                                label='101',
                                text='101'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i3.jueshifan.com/7b077d83/790e7f8b/2a5d3fd74ca1fb1c982a.jpg',
                        image_background_color='#000000',
                        title='Menu4.',
                        text='閱讀',
                        actions=[
                            URIAction(
                                label='LINE Bot',
                                uri='https://ithelp.ithome.com.tw/users/20122649/ironman/3122?page=1'
                            ),
                            URIAction(
                                label='Line Bot 人臉辨識',
                                uri='https://ithelp.ithome.com.tw/articles/10266638?sc=iThelpR'
                            ),
                            URIAction(
                                label='30天學演算法和資料結構',
                                uri='https://ithelp.ithome.com.tw/users/20111557/ironman/2110'
                            )
                        ]
                    )
                ],
                image_aspect_ratio='rectangle', image_size='cover'
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    def google():
        keyword = msg[6:]
        baseUrl = 'https://letmegooglethat.com/?q=' + str(keyword)
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text=f'讓您提供給不會Google的人...\n{baseUrl}\n\n但有句話是這麼說的：\n工程師就是比一般人更會google')])  # 文字訊息

    def 翻譯():
        pass

    def 欸欸做做():
        carousel_template_message = TemplateSendMessage(
            alt_text='出發 欸欸做做瞜！',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/inotanymore/1575305492-2857491791.jpg',
                        image_background_color='#FFFFFF',
                        title='酒店',
                        text='私人招待所',
                        actions=[
                            MessageAction(
                                label='香閣_禮服店',
                                text='香閣_禮服店'
                            ),
                            MessageAction(
                                label='冥想_公主店',
                                text='冥想_公主店'
                            ),
                            URIAction(
                                label='等待開發',
                                uri='https://www.google.com/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://media.vogue.com.tw/photos/607ebcb61f9a7e047be933aa/master/w_1600%2Cc_limit/128143310_170605801415139_976993578358591326_n.jpg',
                        image_background_color='#000000',
                        title='酒吧',
                        text='飲酒作樂',
                        actions=[
                            MessageAction(
                                label='飛鏢酒吧',
                                text='飛鏢酒吧'
                            ),
                            MessageAction(
                                label='雙喜酒吧',
                                text='雙喜酒吧'
                            ),
                            MessageAction(
                                label='隱士餐酒館',
                                text='隱士餐酒館'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/mdrt913/1456762728-1743065239_n.jpg',
                        image_background_color='#000000',
                        title='KTV 夜店',
                        text='飲酒作樂',
                        actions=[
                            MessageAction(
                                label='Sing! go! 忠孝永春店',
                                text='Sing! go! 忠孝永春店'
                            ),
                            MessageAction(
                                label='Wave_夜店',
                                text='Wave_夜店'
                            ),
                            URIAction(
                                label='等待開發',
                                uri='https://www.google.com/'
                            )
                        ]
                    )
                ],
                image_aspect_ratio='rectangle', image_size='cover'
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    def 人臉辨識():
        carousel_template_message = TemplateSendMessage(
            alt_text='人臉辨識 Facial Recognition System',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://face8.ai/static/images/knowledge/20200824-01.png',
                        image_background_color='#000000',
                        title='人臉辨識',
                        text='Facial Recognition System',
                        actions=[
                            CameraAction(
                                label='開啟鏡頭'
                            ),
                            CameraRollAction(
                                label='選擇相片'
                            )
                        ]
                    )
                ],
                image_aspect_ratio='rectangle', image_size='cover'
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    def 洗版():
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text='沒救搂~~~')])

    # --- 判斷式 ---
    def 判斷式_常用功能():
        if msg == '疫情':
            keyword_疾管署()
        elif msg[:2] == '天氣':
            searchWeather()
        elif msg[:6] == 'google':
            google()
        elif msg == 'Ian Quinn':
            IanQuinn()
        elif msg == 'Ian Quinn PC':
            keyword_administrator()
        elif msg == '公司登記查詢':
            keyword_公司登記查詢()
        elif msg == '搜尋排行':
            keyword_google搜尋趨勢()
        elif msg == 'sean':
            keyword_sean()
        elif msg == '欸欸做做':
            欸欸做做()
        elif msg == '台北捷運路線圖':
            keyword_台北捷運路線圖()
        elif msg == '超速資訊':
            keyword_超速冷凍()
        elif msg == '台股線上資源':
            keyword_股票線上資源()
        elif msg == 'Quinn':
            keyword_help()
        elif msg == '人臉辨識':
            人臉辨識()
        elif msg == '我要紅包':
            紅包()
        else:
            判斷式_地點()

    def 判斷式_地點():
        if msg == '101':
            keyword_101()
        elif msg == '淡水捷運站':
            淡水捷運站()
        elif msg == '頂溪捷運站':
            keyword_頂溪捷運站()
        elif msg == '遠東世紀廣場':
            keyword_遠東世紀廣場()
        elif msg == '南港捷運站':
            keyword_南港捷運站()
        else:
            判斷式_PMC()

    def 判斷式_PMC():
        if msg == '士林上課點':
            keyword_軍用格鬥士林點()
        else:
            判斷式_幹話()

    def 判斷式_幹話():
        if msg == '幹':
            keyword_幹()
        elif msg == '靠北':
            keyword_靠北()
        elif msg == '😂😂':
            keyword_哭喔()
        elif msg == '😂😂😂':
            keyword_哭喔v2()
        elif msg == '女朋友':
            keyword_女朋友()
        elif msg == '欸':
            keyword_欸()
        elif msg == '欸欸':
            keyword_欸欸()
        else:
            pass

    # 判斷式Function寫法, 使用漸進式
    # 判斷沒有符合第一種判斷式關鍵字以後, 再判斷有無符合第二種關鍵字、再判斷有無符合第三種關鍵字, etc.
    判斷式_常用功能()


# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345)


