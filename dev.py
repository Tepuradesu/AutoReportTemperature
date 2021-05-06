from line_notify import LineNotify


#変数定義
token=''


bot = LineNotify(access_token=token)
bot.send(
    message='Your Message',
    ) 
