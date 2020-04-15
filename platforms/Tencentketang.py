"""
@author Jacob
@describe 获取腾讯课堂所有课程信息
"""

import requests
import json

from bs4 import BeautifulSoup

from utils.mysql import execute

# 所有课程类别id
front_category_id = []


# 获取类别id
def get_category_id():
    querystring = {"bkn": "", "r": "0.33490091914754694"}

    url = "https://ke.qq.com/cgi-bin/get_cat_info"

    payload = ""

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "cookie": "pgv_pvi=2479348736; tvfe_boss_uuid=2eca41104712882b; pgv_pvid=8072841810; _ga=GA1.2.864479556.1573722435; RK=evZMBujSdu; ptcz=525c5325fa6ca7a129a5002629810da03a3d05923545a9ab76f8f433583c3f63; ts_refer=www.baidu.com/link; ts_uid=8639569252; iswebp=1; pgv_info=ssid=s3565391882; ts_last=ke.qq.com/; Hm_lvt_0c196c536f609d373a16d246a117fd44=1585272384,1586922732; tdw_data_new_2={\"auin\":\"-\",\"sourcetype\":\"\",\"sourcefrom\":\"\",\"ver9\":\"\",\"uin\":\"\",\"visitor_id\":\"6477293613128756\",\"ver10\":\"\",\"url_page\":\"\",\"url_module\":\"\",\"url_position\":\"\"}; _pathcode=0.7334630695802486; tdw_auin_data=-; tdw_data={\"ver4\":\"www.baidu.com\",\"ver5\":\"\",\"ver6\":\"\",\"refer\":\"www.baidu.com\",\"from_channel\":\"\",\"path\":\"a-0.7334630695802486\",\"auin\":\"-\",\"uin\":\"\",\"real_uin\":\"\"}; tdw_data_testid=; tdw_data_flowid=; tdw_first_visited=1; Hm_lpvt_0c196c536f609d373a16d246a117fd44=1586922984",
        "referer": "https://ke.qq.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53",
        "x-requested-with": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    json_list = json.loads(response.text)["result"]["catInfo"]
    return json_list


# 解析json数据
def parsing_json(data):
    for key1 in data:
        for key2 in data[key1]["s"]:
            for key3 in data[key1]["s"][key2]["t"]:
                front_category_id.append({
                    "mt": key1,
                    "st": key2,
                    "tt": key3,
                    "category": data[key1]["n"] + ";" + data[key1]["s"][key2]["n"] + ";" +
                                data[key1]["s"][key2]["t"][key3]["n"]
                })
    print(front_category_id)


# 获取课程数据
def get_course_data(mt, st, tt, page, category):
    url = "https://ke.qq.com/course/list?mt=" + str(mt) + "&st=" + str(st) + "&tt=" + str(tt) + "&page=" + str(page)
    response = requests.request("GET", url).text
    bs = BeautifulSoup(response)
    course_blocks = bs.find_all(name='li', attrs={"class": "course-card-item--v3 js-course-card-item"})
    # print(course_blocks)
    if len(course_blocks) != 0:
        for i in range(len(course_blocks)):
            bs = course_blocks[i]
            img = bs.find(name="img", attrs={"class", "item-img"})
            a = bs.find(name="a", attrs={"class", "item-img-link"})
            save_to_mysql(img.attrs["alt"], a.attrs["href"], img.attrs["src"], category)
        return True
    else:
        return False


# 存储到数据库
def save_to_mysql(name, url, imgUrl, category_name):
    sql = "insert into webCourses (category, name, site, imgUrl, resource) values ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
        category_name, name, url, imgUrl, "腾讯课堂")
    print(sql)
    execute(sql)


def tencent_ketang():
    res = get_category_id()
    parsing_json(res)
    mid = {'mt': '1005', 'st': '2042', 'tt': '3237', 'category': '升学·考研;大学;自考'}

    m = front_category_id.index(mid)
    for item in front_category_id[m:]:
        index = 1
        while True:
            more = get_course_data(item["mt"], item["st"], item["tt"], index, item["category"])
            if more:
                index += 1
            else:
                break
