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

import requests
from bs4 import BeautifulSoup

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
    reply_text = '回到初始頁面，請重新選取功能'
    global state
    if state == state_mapping['main_page']:
        if receive_text == '查詢會員':
            state = state_mapping['find_member']
            reply_text = '請輸入欲查詢會員名稱'
        else:
            print("錯誤的輸入")
            reply_text = '請輸入所需功能'
    elif state == state_mapping['find_member']:
        reply_text = player_state(crawl_player_data(receive_text))
        state = state_mapping['main_page']
        #print("功能尚未完成")
    return reply_text





#爬取姓名欄位
def crawl_player_data(player_name):
    url = 'http://www.twlttf.org/lttfproject/playerprofiles/search?utf8=✓&keyword='
    res = requests.get(url+player_name)
    soup = BeautifulSoup(res.text,'html.parser')
    data_tr = soup.select(".datatable tbody tr")
    players = list()
    for column in data_tr:
        tds = column.find_all('td')
        col = list()
        col.append(tds[0].find('img')['src'])
        col.append(tds[1].getText())
        col.append(tds[2].find('a').find('font').getText())
        col.append(tds[3].find('font').getText())
        col.append(tds[4].getText())
        col.append(tds[5].getText())
        col.append(tds[6].getText())
        col_ = list(col)
        players.append(col_)
        #player[len(player):len(player)+1] = col
        #print(col, end  = '')
        #print('\n')
        col.clear()
    return players

#def player_photo(players):
def player_state(players):
    player_data = ''
    for player in players:
        player_data += '會員編號： '+player[1]+'\n會員姓名： '+ player[2] + \
        '\n目前積分： ' + player[3] + '\n初始積分： ' + player[4] + '\n總勝場數： ' \
        + player[5] + '\n總敗場數： ' + player[6]+'\n\n'
    print(player_data)
    return player_data


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(keyword_rely(event.message.text))
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
