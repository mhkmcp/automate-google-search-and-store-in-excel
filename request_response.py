import requests
from datetime import datetime


def hit_url(url):
    r = requests.get(url)
    return r.status_code


tm = datetime.now().strftime("%H:%M:%S")
txt = 'ada reach system'
r_s = hit_url('https://api.mobireach.com.bd/SendTextMessage?Username=shagor&Password=Sh@g0R21AdmiN&From=adareach&To=8801837967588&Message='+tm+' '+txt+' OK')
print(r_s)

tmb = datetime.now().strftime("%H:%M:%S")
txt_boomcast = 'boomcast system'
rs = hit_url('http://45.249.101.2/boomcast/WebFramework/boomCastWebService/externalApiSendSMSMobiReach?masking=EBL.&userName=robimobireach&password=ec9fdbc5aa84840418b1a5c315655835&MsgType=UNICODE&receiver=8801748242482&message='+tmb+' '+txt_boomcast+' OK')
print(rs)
