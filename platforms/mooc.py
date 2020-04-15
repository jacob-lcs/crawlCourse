"""
@author Jacob
@describe 获取慕课所有课程信息
"""

import requests
import json
from utils.mysql import execute

# 所有课程类别id
front_category_id = []


# 获取类别id
def get_category_id():
    querystring = {"csrfKey": "22ce62ac935b4cf99c75e5ba0cdd4524"}

    url = "https://www.icourse163.org/web/j/mocCourseCategoryBean.getCategByType.rpc?csrfKey=22ce62ac935b4cf99c75e5ba0cdd4524"

    payload = "type=4"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-length": "6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "NTESSTUDYSI=22ce62ac935b4cf99c75e5ba0cdd4524; EDUWEBDEVICE=6d0627a3651f4c3c84e0173433aff802; utm=\"eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly93d3cuYmFpZHUuY29tL2xpbms/dXJsPV83X1NFWnBZeUN4M3RvemdqZ2h2NjA5LUJhRDZNblZEamJudVlfU2NvWDYyeGtYVEpWUm5WTHh6QmJiZElSZzAmY2s9MzI1My4xLjUyLjI4Ny4xNTguMjg4LjE1OC40NDMmc2hoPXd3dy5iYWlkdS5jb20mc2h0PTgwMDM1MTYxXzJfZGcmd2Q9JmVxaWQ9OTRhNmIxMzIwMDEyYzdiZTAwMDAwMDA1NWU5NjcwZDg=\"; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1586917597; hb_MA-A976-948FFA05E931_source=www.baidu.com; __yadk_uid=B4J22jcAcdoc2oQ0KNgpZ8298xHZAxVG; WM_NI=bYBYcbYGjQ%2F5wYoBHRGvpS%2F4HF6W4vuezsBOux%2F9Sw73W7GzB%2BNaTDYmkKPMw7MhnxNhWWz9mjrtQ87NuwMd1dIk7%2FtATbPmRaoK%2Bo6FLWIdGRAMGzc0y5NXEtcwXdCsTHg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee83f25485b3a69adc79818a8ab7d85b838f8e85b55eaeaa818fd95dfc93bfb7f82af0fea7c3b92aa2878ebae26a9b99a6b2ae3fb587a1a3cb5a85aac0b4ae408c9afab8b77eb7bbb694c145b7a8e1dad27df5ed99d8c67282f58282d7509bb3a5acd347b5e98389ed748eb899b8f933afb6be95d434f592bb98d070f3bc878cb625b89f9c83d36792bfa1acaa65f69a84b8cc70858e8faec672a1f0b7d6cd5487acad98db7081ad9ca9e637e2a3; WM_TID=UeA6r%2B53QUpFFRVFVQZ6Ey%2Be3MG8MrAv; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1586919276",
        "edu-script-token": "22ce62ac935b4cf99c75e5ba0cdd4524",
        "origin": "https://www.icourse163.org",
        "referer": "https://www.icourse163.org/category/guojiajingpin",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    json_list = json.loads(response.text)["result"]
    return json_list


# 解析json数据
def parsing_json(data, category):
    for item in data:
        if item["children"]:
            parsing_json(item["children"], category + item["name"] + ";")
        else:
            category_content = {
                "id": item["id"],
                "category": category + item["name"] + ";"
            }
            front_category_id.append(category_content)


# 获取课程数据
def get_course_data(page, category, category_name):
    querystring = {"csrfKey": "22ce62ac935b4cf99c75e5ba0cdd4524"};

    url = "https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=22ce62ac935b4cf99c75e5ba0cdd4524"

    payload = "categoryId=" + str(category) + "&type=30&orderBy=0&pageIndex=" + str(page) + "&pageSize=20"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-length": "63",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "NTESSTUDYSI=22ce62ac935b4cf99c75e5ba0cdd4524; EDUWEBDEVICE=6d0627a3651f4c3c84e0173433aff802; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1586917597; hb_MA-A976-948FFA05E931_source=www.baidu.com; __yadk_uid=B4J22jcAcdoc2oQ0KNgpZ8298xHZAxVG; WM_NI=bYBYcbYGjQ%2F5wYoBHRGvpS%2F4HF6W4vuezsBOux%2F9Sw73W7GzB%2BNaTDYmkKPMw7MhnxNhWWz9mjrtQ87NuwMd1dIk7%2FtATbPmRaoK%2Bo6FLWIdGRAMGzc0y5NXEtcwXdCsTHg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee83f25485b3a69adc79818a8ab7d85b838f8e85b55eaeaa818fd95dfc93bfb7f82af0fea7c3b92aa2878ebae26a9b99a6b2ae3fb587a1a3cb5a85aac0b4ae408c9afab8b77eb7bbb694c145b7a8e1dad27df5ed99d8c67282f58282d7509bb3a5acd347b5e98389ed748eb899b8f933afb6be95d434f592bb98d070f3bc878cb625b89f9c83d36792bfa1acaa65f69a84b8cc70858e8faec672a1f0b7d6cd5487acad98db7081ad9ca9e637e2a3; WM_TID=UeA6r%2B53QUpFFRVFVQZ6Ey%2Be3MG8MrAv; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1586920876;",
        "edu-script-token": "22ce62ac935b4cf99c75e5ba0cdd4524",
        "origin": "https://www.icourse163.org",
        "referer": "https://www.icourse163.org/category/computer",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53",
        "Eo-Token": "37339b26-6882-42e9-82a5-8ff37545b177"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    res_json = json.loads(response.text)["result"]
    if res_json["result"]:
        for course in res_json["result"]:
            save_to_mysql(course, category_name)
        pagination = res_json["pagination"]
        return pagination["pageIndex"] < pagination["totlePageCount"]
    else:
        return False


# 存储到数据库
def save_to_mysql(data, category_name):
    sql = "insert into webCourses (category, name, site, imgUrl, resource) values ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
        category_name, data["name"],
        'https://www.icourse163.org/course/' + str(data["schoolPanel"]["shortName"]) + "-" + str(data["id"]),
        data["imgUrl"], "慕课")
    print(sql)
    execute(sql)


def mooc():
    res = get_category_id()
    parsing_json(res, "")
    print(front_category_id)
    for item in front_category_id:
        index = 1
        while True:
            more = get_course_data(index, item["id"], item["category"])
            if not more:
                break
            index += 1
