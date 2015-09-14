"""华住积分抢免房活动，自动抢房脚本
需要设置登录手机号，想要抢的门店列表，以及对应的日期
原理即模拟正常操作，首先登录，然后循环发送请求
因为很多参数需要依赖HTML或JS中的设定，所以参数不能正常获取则需要结合具体情况修改代码
注意：登录需要手机验证码，但每天验证码发送次数是有限的
"""
import http.cookiejar
import urllib.request
import urllib.parse
import re
import json
import time

phone_num = '18616760526'  # 登录手机号，是注册过的
hotel = ['汉庭酒店苏州新观前店', '汉庭酒店苏州大学葑门店', '汉庭酒店苏州园区金鸡湖店']  # 门店列表，按优先级排列
date = '2015/9/14'  # 对应抢免房的日期

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/web',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Accept-Encoding': 'sdch'
}  # 伪造为iPhone访问


class Get_free():

    def __init__(self):
        """初始化
        主要是创建带coockie的opener
        以及用正则表达式获取几乎所有需要的，POST需要的值
        """
        cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj))

        self.const = {}
        main_url = 'http://activity.h-world.com/PointExchangeRoom/Secondkill/skill09'
        main = urllib.request.Request(
            url=main_url, headers=headers, method='GET')
        get = self.opener.open(main)
        content = get.read().decode('utf-8')

        self.const['sign'] = re.findall(
            r'id="txtkey" value="(.*?)"', content)[0]
        self.const['ActivityType'] = re.findall(
            r'id="txtActivityType" value="(.*?)"', content)[0]
        self.const['activityCode'] = re.findall(
            r'id="hdActivityCode" value="(.*?)"', content)[0]

        js_url = re.findall(
            r'"(http://ws-www\.hantinghotels\.com/Content_activty/js/SecondKill\.js.*?)"', content)[0]
        js = urllib.request.urlopen(js_url)
        js_con = js.read().decode()
        self.const['memberID'] = re.findall(r"memberID: '(.*?)'", js_con)[0]

        js_url = re.findall(
            r'"(http://ws-www\.hantinghotels\.com/Content_activty/js/ActivityPublic\.js.*?)"', content)[0]
        js = urllib.request.urlopen(js_url)
        js_con = js.read().decode()
        self.const['ShortMessageType'] = re.findall(
            r'"ShortMessageType": (\d+?),', js_con)[0]
        print(self.const['ShortMessageType'])

    def isanom(self):
        """发送isanom请求
        这个请求在正常访问时会经常发送
        """
        url = 'http://activity.h-world.com/PointExchangeRoom/IsAnom'
        anom = urllib.request.Request(
            url=url, headers=headers, data=urllib.parse.urlencode('').encode(), method='POST')
        post = self.opener.open(anom)
        result = json.loads(post.read().decode('utf-8'))
        return result['code']

    def ismobile(self):
        """发送ismobile请求
        这个请求在登录前需要发送
        """
        data = {
            'mobile': phone_num
        }
        url = 'http://activity.h-world.com/WechatFLS/ISMobile'
        mobile = urllib.request.Request(
            url=url, headers=headers, data=urllib.parse.urlencode(data).encode(), method='POST')
        post = self.opener.open(mobile)
        result = json.loads(post.read().decode())
        return result['code']

    def send_message(self):
        """发送短信
        触发发送短信，并显示请求返回结果
        是否成功发送短信会在结果中显示
        """
        print(self.isanom())
        data = {
            'callback': 'SmsGetMemberSms',
            'Mobile': phone_num,
            'ShortMessageType': self.const['ShortMessageType'],
            'Sign': self.const['sign'],
            'ActivityType': self.const['ActivityType'],
        }
        url = 'https://loginactivity.h-world.com/AuthService/SendShortMessage?' + \
            urllib.parse.urlencode(data)
        get = urllib.request.Request(url=url, headers=headers, method='GET')
        con = self.opener.open(get)
        result = con.read().decode('utf-8')
        print(result)

    def login(self):
        """登录
        首先下载验证码
        然后输入图片验证码和手机验证码
        最后显示请求返回结果
        若登录正常会得到用户信息
        """
        img_data = {
            'mobile': phone_num,
            'time': str(int(time.time()))
        }
        url_img = 'https://loginactivity.h-world.com/authservice/GetValidateCode?' + \
            urllib.parse.urlencode(img_data)
        get = urllib.request.Request(
            url=url_img, headers=headers, method='GET')
        img = self.opener.open(get)
        with open('test.jpg', 'wb') as f:
            f.write(img.read())
        print(self.ismobile())
        verify_code = input('图片验证码：')
        mobile_code = input('手机验证码：')
        login_data = {
            'callback': 'handleRegisterResult',
            'Mobile': phone_num,
            'ShortMessageType': self.const['ShortMessageType'],
            'SendCode': mobile_code,
            'ImgVerificationCode': verify_code,
            'VNoHead': '',
            'Sign': self.const['sign'],
            'ActivityType': self.const['ActivityType']
        }
        url_login = 'https://loginactivity.h-world.com/AuthService/LoginOnlyMobile?' + \
            urllib.parse.urlencode(login_data)
        get = urllib.request.Request(
            url=url_login, headers=headers, method='GET')
        login = self.opener.open(get)
        result = login.read().decode()
        print(result)

    def get_room(self):
        """循环抢免房券
        就是循环发送请求了
        需要设置抢哪几家门店的房
        若活动还未开始，则一直循环请求第一家
        当开始时会循环请求list中的门店
        """
        the_code = {
            '99': '太棒了！恭喜！您已成功兑换免房券,快去您的账户查看吧！',
            '2.1': '不在开抢日期！',
            '3': '不要着急哦，马上登场！',
            '4': 'IP错误',
            '12': '系统错误',
            '97': '啊呀，手慢了...免房兑换已满',
            '5': '每个会员至多抢一张免房哟！把机会留给其他人吧！',
            '103': '啊呀，手慢了...免房兑换已满',
            '104': '啊呀，手慢了...免房兑换已满'
        }
        count = 1
        data = {
            'activityCode': self.const['activityCode'],
            'storeName': hotel[0],
            'memberID': self.const['memberID'],
            'strDate': date
        }
        url = 'http://activity.h-world.com/PointExchangeRoom/Exchange'
        while True:
            print(self.isanom())
            post = urllib.request.Request(
                url=url, headers=headers, data=urllib.parse.urlencode(data).encode(), method='POST')
            con = self.opener.open(post)
            result = json.loads(con.read().decode())
            code = str(result['code'])
            try:
                sign = the_code[code]
                print(sign)
            except Exception:
                print(result)
            if code != '3':  # 如果尚未开始，则循环请求，不改变门店
                data['storeName'] = hotel[count]
                count += 1
                count = count % 3
            time.sleep(0.6)  # 请求时间间隔

if __name__ == '__main__':
    free = Get_free()
