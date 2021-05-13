from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import requests
from line_notify import LineNotify

#変数定義
chrome_path = '/usr/bin/chromium-browser'
chromedriver_path = '/usr/lib/chromium/chromedriver'
sekomu_login_url = ''
renraku_hokoku_url=''
kigyo_code = 'Your kigyo code'
user_id = 'Your id'
password = 'Your password'
token=''
#開発環境:True 本番環境:False
dev_or_pro = True

#オプション設定
o = Options()
o.binary_location = '/usr/bin/chromium-browser'
o.add_argument('--headless')
o.add_argument('--disable-gpu')
o.add_argument('--no-sandbox')
o.add_argument('--window-size=1200x600')

"""
#Sample test
"""
#d = webdriver.Chrome(chromedriver_path, options=o)
#d.get('https://www.google.com')
#print(d.title)
#d.quit()

"""
Use the Chrome DriverService.
https://chromedriver.chromium.org/getting-started
"""
s = Service(executable_path=chromedriver_path)
s.start()
d = webdriver.Remote(
    s.service_url,
    desired_capabilities=o.to_capabilities()
)
#ログイン画面に遷移
d.get(sekomu_login_url)
#企業コード入力要素取得
customer_code_elm=d.find_element_by_id("customer-code")
#ユーザID入力要素取得
user_code_elm=d.find_element_by_id("user-code")
#パスワード入力要素取得
pass_code_elm=d.find_element_by_id("keyboard-output")
#ログインボタン要素取得
btn_login_elm=d.find_element_by_id("btn-login")

#ログイン処理を実施する。
customer_code_elm.send_keys(kigyo_code)
time.sleep(1)
user_code_elm.send_keys(user_id)
time.sleep(1)
pass_code_elm.send_keys(password)
time.sleep(1)
btn_login_elm.click()
time.sleep(3)
print('------Complete Page Transition!--------')

#連絡報告画面に遷移する。
d.get(renraku_hokoku_url)
time.sleep(3)
try: 
 saigaijokyo_checkbox_elm=d.find_element_by_xpath("//*[@id=\"saigaiJykyKndCd001\"]")
 saigaijokyo_paneltext_elm=d.find_element_by_xpath("//*[@id=\"l-main\"]/div/div[1]/div[2]/table[2]/tbody/tr[1]/td/div/div[1]/label/span/span[2]")
 #checkbox 選択状態を確認。未選択の場合のみチェックする。
 if not saigaijokyo_checkbox_elm.is_selected():
   print("検温項目がチェックされていません。\n新しく検温項目をチェックします。")
   saigaijokyo_paneltext_elm.click()
 else:
  print("既に37.0未満をチェック済みです。")
  
 #連絡報告をする。
 btn_exec_elm=d.find_element_by_id("btn-exec")
 btn_exec_elm.click()
 time.sleep(2)
 #Pro
 if dev_or_pro:
   #Confirmation--------->OKボタン押下
   btn_primary_elm=d.find_element_by_xpath("/html/body/div[3]/div/div/div/button[1]")
   btn_primary_elm.click()
   print("OKボタンを押下しました。")
   #終了処理
   #Line通知処理実施
   bot = LineNotify(access_token=token)
   bot.send(
       message='検温報告が完了しました。',
       )
 #Dev
 else:
   #Confirmation--------->Cancelボタン押下
   btn_secondary_elm=d.find_element_by_xpath("/html/body/div[3]/div/div/div/button[2]")
   btn_secondary_elm.click()
   print("Cancelボタンを押下しました。")
   #Line通知処理実施
   bot = LineNotify(access_token=token)
   bot.send(
       message='検温報告が完了しました。',
       ) 
except Exception as e:
   print(e)
   print('------Error------')
finally:
 #終了処理
 print('-------Complete Reporting!-------')
 d.close()
 d.quit()
