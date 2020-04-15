"""
@author Jacob
@describe 获取学堂在线所有课程信息
"""

import requests
import json
from utils.mysql import execute


# 获取类别id
def get_course(page):
    querystring = {"page": str(page)}

    url = "https://next.xuetangx.com/api/v1/lms/get_product_list/"

    payload = "{\"query\":\"\",\"chief_org\":[],\"classify\":[],\"selling_type\":[],\"status\":[],\"appid\":10000}"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh",
        "content-length": "85",
        "content-type": "application/json",
        "cookie": "django_language=zh",
        "django-language": "zh",
        "origin": "https://next.xuetangx.com",
        "referer": "https://next.xuetangx.com/search?query=&org=&classify=&type=&status=&page=6",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53",
        "x-client": "web",
        "xtbz": "xt"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    json_list = json.loads(response.text)["data"]["product_list"]
    return json_list


# 存储到数据库
def save_to_mysql(name, url, imgUrl, category_name):
    sql = 'insert into webCourses (category, name, site, imgUrl, resource) values ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(
        category_name, name, url, imgUrl, "学堂在线")
    print(sql)
    execute(sql)


def xuetang_online():
    index = 1
    while True:
        course_list = get_course(index)
        if len(course_list) > 0:
            for course in course_list:
                save_to_mysql(course["name"], "https://next.xuetangx.com/course/" + course["course_sign"],
                              course["cover"], ";".join(course["classify_name"]))
            index += 1
        else:
            break
