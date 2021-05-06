import requests

#変数定義
token='K3FaMwAR400CwqfOrHN3UJG9ysG0PAT3RJMVdn7ri53'

class LineNotify:
 API_URL = "https://notify-api.line.me/api/notify"
 def __init__(self,access_token):
     self.__headers = {'Authorization': 'Bearer ' + access_token}

 def send(
          self,message,
          image=None,sticker_package_id=None,sticker_id=None,
         ):

     payload = {
     'message':message,
     'stickerPackageId':sticker_package_id,
     'stickerId':sticker_id,
     }
     files = {} 
     if image != None:
        files = {'imageFile': open(image,'rb')}
     r = requests.post(
         LineNotify.API_URL,
         headers = self.__headers,
         data = payload,
         files=files,
         )

#bot = LineNotify(access_token=token)
#bot.send(
#    message='Your Message',
#    ) 

