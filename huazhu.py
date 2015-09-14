import http.cookiejar,urllib.request
import re
import urllib.parse
import json
import time

txtkey=re.compile(r'id="txtkey" value="(.*?)"')
txtActivityType=re.compile(r'id="txtActivityType" value="(.*?)"')
hdActivityCode=re.compile(r'id="hdActivityCode" value="(.*?)"')

the_code={
	'99':'太棒了！恭喜！您已成功兑换免房券,快去您的账户查看吧！',
	'2.1':'不在开抢日期！',
	'3':'不要着急哦，马上登场！',
	'4':'IP错误',
	'12':'系统错误',
	'97':'啊呀，手慢了...免房兑换已满',
	'5':'每个会员至多抢一张免房哟！把机会留给其他人吧！',
	'103':'啊呀，手慢了...免房兑换已满',
	'104':'啊呀，手慢了...免房兑换已满'
}

headers={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/web',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
	'Accept-Encoding': 'sdch'
}
phone_num='18616760526'
def init():
	global opener
	global sign
	global ActivityType
	global activityCode
	global memberID
	cj=http.cookiejar.CookieJar()
	opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

	main_url='http://activity.h-world.com/PointExchangeRoom/Secondkill/skill09'
	main=urllib.request.Request(url=main_url,headers=headers,method='GET')
	get=opener.open(main)
	content=get.read().decode('utf-8')
	sign=txtkey.findall(content)[0]
	ActivityType=txtActivityType.findall(content)[0]
	activityCode=hdActivityCode.findall(content)[0]
	print(activityCode)
	js_url=re.findall(r'"(http://ws-www.hantinghotels.com/Content_activty/js/SecondKill\.js.*?)"',content)[0]
	js=urllib.request.urlopen(js_url)
	js_con=js.read().decode()
	memberID=re.findall(r"memberID: '(.*?)'",js_con)[0]
	print(memberID)

def isanom():
	url_isanom='http://activity.h-world.com/PointExchangeRoom/IsAnom'
	anom=urllib.request.Request(url=url_isanom,headers=headers,data=urllib.parse.urlencode('').encode(),method='POST')
	post=opener.open(anom)
	result=json.loads(post.read().decode('utf-8'))
	return result['code']
def ismobile():
	data={
	'mobile':phone_num
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
	'Mobile':phone_num,
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
def login():
	img_data={
	'mobile':phone_num,
	'time':str(int(time.time()))
	}
	url_img='https://loginactivity.h-world.com/authservice/GetValidateCode?'+urllib.parse.urlencode(img_data)
	get=urllib.request.Request(url=url_img,headers=headers,method='GET')
	img=opener.open(get)
	with open('test.jpg','wb') as f:
		f.write(img.read())
	print(ismobile())
	verify_code=input('图片验证码：')
	mobile_code=input('手机验证码：')
	login_data={
	'callback':'handleRegisterResult',
	'Mobile':phone_num,
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
	count=1
	hotel=['汉庭酒店苏州新观前店','汉庭酒店苏州大学葑门店','汉庭酒店苏州园区金鸡湖店']
	while True:
		print(isanom())
		url='http://activity.h-world.com/PointExchangeRoom/Exchange'
		data={
		'activityCode':activityCode,
		'storeName':hotel[0],
		'memberID':memberID,
		'strDate':'2015/9/14'
		}
		post=urllib.request.Request(url=url,headers=headers,data=urllib.parse.urlencode(data).encode(),method='POST')
		exchange=opener.open(post)
		result=json.loads(exchange.read().decode())
		code=str(result['code'])
		try:
			sign=the_code[code]
			print(sign)
		except Exception:
			print(result)
		if code!='3':
			data['storeName']=hotel[count]
			count+=1
		time.sleep(0.6)

if __name__=='__main__':
	init()
	send_message()
	login()
	get_room()