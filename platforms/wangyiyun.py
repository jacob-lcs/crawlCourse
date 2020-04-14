"""
@author Jacob
@describe 获取网易云课堂所有课程信息
"""

import requests
import json
from utils.mysql import execute

front_category_id = []


# 获取类别id
def get_category_id():
    headers = {"Accept": "application/json",
               "Host": "study.163.com",
               "Origin": "https://study.163.com",
               "Content-Type": "application/json",
               "Referer": "https://study.163.com/courses",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/62.0.3202.62 Safari/537.36 "
               }
    req = requests.get("https://home.study.163.com/home/j/web/getFrontCategory.json", headers=headers)
    json_list = json.loads(req.text)["result"]
    return json_list


# 获取课程数据
def get_course_data(page, category, category_name):
    print("正在抓取%s页数据" % page)
    payload = {"pageIndex": page,
               "pageSize": 50,
               "relativeOffset": 0,
               "frontCategoryId": category,
               "searchTimeType": -1,
               "orderType": 50,
               "priceType": -1,
               "activityId": 0,
               "keyword": ""}
    payload = json.dumps(payload)
    headers = {"Accept": "application/json",
               "Host": "study.163.com",
               "Origin": "https://study.163.com",
               "Content-Type": "application/json",
               "Referer": "https://study.163.com/courses",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/62.0.3202.62 Safari/537.36 "
               }
    req = requests.post("https://study.163.com/p/search/studycourse.json", data=payload, headers=headers)
    res_json = json.loads(req.text)["result"]
    if res_json["list"]:
        for course in res_json["list"]:
            save_to_mysql(course, category_name)
        query = res_json["query"]
        return query["pageIndex"] * query["pageSize"] < query["totleCount"]
    else:
        return False


# 存储到数据库
def save_to_mysql(data, category_name):
    sql = "insert into webCourses (category, name, site, imgUrl, resource) values ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
        category_name, data["productName"], 'https://study.163.com/course/introduction/' + str(data["courseId"]) + '.htm',
        data["imgUrl"], "网易云课堂")
    print(sql)
    execute(sql)


# 解析json数据
def parsing_json(data, category):
    for item in data:
        if len(item["children"]) != 0:
            parsing_json(item["children"], category + item["name"] + ";")
        else:
            category_content = {
                "id": item["id"],
                "category": category + item["name"] + ";"
            }
            front_category_id.append(category_content)


def wang_yi_yun():
    category_id = get_category_id()
    parsing_json(category_id, "")
    print(front_category_id)
    for item in front_category_id:
        index = 1
        while True:
            print(index)
            more = get_course_data(index, item["id"], item["category"])
            if not more:
                break
            index += 1
