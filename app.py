from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ADYoKNjXZh/5+P3eCwaJoArENIESc/sXDY44VqLNjObkjNQTPcawT4zKsXnsii3CvoxeCVREMGQDoBauQIon+Z3Bo+T/mF6Hv+VZSTtRl6hhF2nWiGJgolCHbaXBrU93PITFx1VnGWtCjukEOjQY8wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('06996e3be3a91c8ee81fd83ef5acc051')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'
state_mapping = {
    'main_page':'0',
    'find_member':'1'
}
state = state_mapping['main_page']
#關鍵字回覆
def keyword_rely(receive_text):
    reply_text = '請重新輸入'
    global state
    if state == state_mapping['main_page']:
        if receive_text == '查詢選手':
            state = state_mapping['find_member']
            reply_text = '請輸入欲查詢選手名稱'
        else:
            reply_text = '請輸入所需功能'
    if state == state_mapping['find_member']:
        #reply_text = crawl_player_data(receive_text)
        state = state_mapping['main_page']
    return reply_text





#爬取姓名欄位
#def crawl_player_data():



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=keyword_rely(event.message.text))
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
