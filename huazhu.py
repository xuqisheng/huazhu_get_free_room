import http.cookiejar,urllib.request
import re
import urllib.parse
import json
import time

txtkey=re.compile(r'id="txtkey" value="(.*?)"')
txtActivityType=re.compile(r'id="txtActivityType" value="(.*?)"')
headers={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/web',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
	'Accept-Encoding': 'sdch'
}
def init():
	global opener
	global sign
	global ActivityType
	cj=http.cookiejar.CookieJar()
	opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

	main_url='http://activity.h-world.com/PointExchangeRoom/Secondkill/skill09'
	main=urllib.request.Request(url=main_url,headers=headers,method='GET')
	get=opener.open(main)
	content=get.read().decode('utf-8')
	sign=txtkey.findall(content)[0]
	ActivityType=txtActivityType.findall(content)[0]

def isanom():
	url_isanom='http://activity.h-world.com/PointExchangeRoom/IsAnom'
	anom=urllib.request.Request(url=url_isanom,headers=headers,data=urllib.parse.urlencode('').encode(),method='POST')
	post=opener.open(anom)
	result=json.loads(post.read().decode('utf-8'))
	return result['code']
def ismobile():
	data={
	'mobile':'18616760526'
	}
	url='http://activity.h-world.com/WechatFLS/ISMobile'
	mobile=urllib.request.Request(url=url,headers=headers,data=urllib.parse.urlencode(data).encode(),method='POST')
	post=opener.open(mobile)
	result=json.loads(post.read().decode())
	return result['code']

def send_message():
	print(isanom())
	data={
	'callback':'SmsGetMemberSms',
	'Mobile':'18616760526',
	'ShortMessageType':'5',
	'Sign':sign,
	'ActivityType':ActivityType,
	}
	url='https://loginactivity.h-world.com/AuthService/SendShortMessage?'+urllib.parse.urlencode(data)
	get=urllib.request.Request(url=url,headers=headers,method='GET')
	con=opener.open(get)
	#con=urllib.request.urlopen(url)
	result=con.read().decode('utf-8')
	print(result)
def test():
	img_data={
	'mobile':'18616760526',
	'time':str(int(time.time()))
	}
	url_img='https://loginactivity.h-world.com/authservice/GetValidateCode?'+urllib.parse.urlencode(img_data)
	get=urllib.request.Request(url=url_img,headers=headers,method='GET')
	img=opener.open(get)
	with open('test.jpg','wb') as f:
		f.write(img.read())
	print(ismobile())
	verify_code=input('verify code:')
	mobile_code=input('mobile code:')
	login_data={
	'callback':'handleRegisterResult',
	'Mobile':'18616760526',
	'ShortMessageType':'5',
	'SendCode':mobile_code,
	'ImgVerificationCode':verify_code,
	'VNoHead':'',
	'Sign':sign,
	'ActivityType':ActivityType
	}
	url_login='https://loginactivity.h-world.com/AuthService/LoginOnlyMobile?'+urllib.parse.urlencode(login_data)
	get=urllib.request.Request(url=url_login,headers=headers,method='GET')
	login=opener.open(get)
	result=login.read().decode()
	print(result)

def get_room():
	while True:
		url='http://activity.h-world.com/PointExchangeRoom/Exchange'
		data={
		'activityCode':'skill09',
		'storeName':'汉庭酒店苏州新观前店',
		'memberID':'031006407',
		'strDate':'2015/9/14'
		}
		post=urllib.request.Request(url=url,headers=headers,data=urllib.request.urlencode(data).encode(),method='POST')
		exchange=opener.open(post)
		result=json.loads(exchange.read().decode())
		print(result['code'])
		time.sleep(5)

if __name__=='__main__':
	init()
	send_message()
	test()
	get_room()