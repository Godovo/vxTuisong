import random
from time import localtime
from requests import get,post
import requests
import json
from json import loads
from datetime import datetime, date
from zhdate import ZhDate
from datetime import datetime
import sys
import os

config = {
# 公众号配置
# 公众号appId
"app_id": "wxd44db1122cfb05ff",
# 公众号appSecret
"app_secret": "d3e9909a7e3d21a977ae66e3b7c9970f",
# 模板消息id
"template_id": "F-xQmyGKROzDLoJIBrN7GUrUaOQPXoZu64uP5HCcC1w",
# 接收公众号消息的微信号，如果有多个，需要在[]里用英文逗号间隔，例如["wx1", "wx2"]
"user": ["otDUI6ql70CemmO_zlOj1Pl7ntlc"],
# 信息配置
# 所在地区，可为省，城市，区，县，同时支持国外城市，例如伦敦
"region": "青岛",
# 和风天气apikey
# 金句中文，如果设置了，则会显示这里的，如果为空，默认会读取金山的每日金句
"note_ch": "",
# 金句英文
"note_en": ""
}


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)
print(get_color())

def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    # print(access_token)
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    return access_token
print(get_access_token())

def get_weather():
    region = '青岛'
    key = '5b330d89c1ba4bc4aa81d8d71aaeea47'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    if response["code"] == "404":
        print("推送消息失败，请检查地区名是否有误！")
        os.system("pause")
        sys.exit(1)
    elif response["code"] == "401":
        print("推送消息失败，请检查和风天气key是否正确！")
        os.system("pause")
        sys.exit(1)
    else:
        # 获取地区的location--id
        location_id = response["location"][0]["id"]
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 时间
    date = response["now"]["obsTime"][:10]
    # 天气
    weather = response["now"]["text"]
    # 当前温度
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    # 风向
    wind_dir = response["now"]["windDir"]
    return date,weather,temp,wind_dir
print(get_weather())

def get_birthday():
    wen = datetime.strptime('2023-08-03 08:00:00','%Y-%m-%d %H:%M:%S')
    yu = datetime.strptime('2023-08-04 08:00:00','%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    wen_birthday = wen-now
    yu_birthday = yu-now
    birthday = f"小文的生日：2002年08月03日，距离生日还有{wen_birthday.days}天\n小鱼的生日：1998年08月04日，距离生日还有{yu_birthday.days}天"
    return birthday
print(get_birthday())

def get_love():
    object = datetime.strptime('2021-04-16 08:00:00','%Y-%m-%d %H:%M:%S')
    #当前时间
    now=datetime.now()
    #时间差
    delta = now-object
    hour = delta.seconds/60/60
    minute = (delta.seconds -hour*60*60)/60
    love_time = f"恋爱纪念日：2021年4月17日，小文和小鱼的爱情故事已经写到第{delta.days}天啦！"
    return love_time
print(get_love())

def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch,note_en
print(get_ciba())

def send_message(to_user, access_token, region_name, weather, temp, wind_dir,birthday,loveday,note_ch, note_en):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    # love_year = int(config["love_date"].split("-")[0])
    # love_month = int(config["love_date"].split("-")[1])
    # love_day = int(config["love_date"].split("-")[2])
    # love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    # love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    # birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "region": {
                "value": region_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "temp": {
                "value": temp,
                "color": get_color()
            },
            "wind_dir": {
                "value": wind_dir,
                "color": get_color()
            },
            "birthday": {
                "value": birthday,
                "color": get_color()
            },
            "loveday": {
                "value": loveday,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
        }
    }
    return data

if __name__ == "__main__":
    access_token = get_access_token()
    # 接收的用户
    region = "青岛"
    users = config["user"]
    # 传入地区获取天气信息
    date,weather,temp,wind_dir = get_weather()
    note_ch,note_en = get_ciba()
    birthday = get_birthday()
    loveday = get_love()

    # # 公众号推送消息
    for user in users:
        send_message(user,access_token,region,weather,temp,wind_dir,birthday,loveday,note_ch,note_en)
    os.system("pause")