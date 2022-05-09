# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudioMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage
)
# handle msg
import os
import speech_recognition as sr

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi(
    'GCd4/NMhrvJ7sSwntRSVNM5v7wD5qUAl1m+Sa0NNV4/5ovSX8V5p9CBXvm2JgevdjAIMjEBaGNJyb1ED99AfQb9MWY+dBmp5dDtZCdFdRwLyglGR7/32At5Xdt1kX6Jae0mfTEBhfZPPh4Oxif/IpAdB04t89/1O/w1cDnyilFU=')

# your linebot message API - Channel secret
handler = WebhookHandler('7a5930f965c6055bbbd755d74f1aeac9')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''

    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    name_mp3 = 'recording.mp3'
    name_wav = 'recording.wav'
    message_content = line_bot_api.get_message_content(event.message.id)

    with open(name_mp3, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    os.system('ffmpeg -y -i ' + name_mp3 + ' ' + name_wav + ' -loglevel quiet')
    text = transcribe(name_wav)
    print('Transcribe:', text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))


# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345)


