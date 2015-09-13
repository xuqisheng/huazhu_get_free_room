import http.cookiejar,urllib.request

cj=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers={
	'Host': 'activity.h-world.com',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/web',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
	'Accept-Encoding': 'sdch'
}
main_url='http://activity.h-world.com/PointExchangeRoom/Secondkill/skill09'
main=urllib.request.Request(url=main_url,headers=headers,method='GET')
get=opener.open(main)
print(get.read().decode('utf-8'))