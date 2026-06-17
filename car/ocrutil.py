from aip import AipOcr
import json
import os
import re


def get_key():
    key_path = "key.txt"
    # 🔥 修复：os.path.exists
    if not os.path.exists(key_path):
        print("请先创建 key.txt 文件！")
        return {
            "APP_ID": "",
            "API_KEY": "",
            "SECRET_KEY": ""
        }
    with open(key_path, 'r', encoding='utf-8') as f:
        content = f.read()
        key_dict = json.loads(content)
        return key_dict


key_info = get_key()
APP_ID = key_info.get('APP_ID', '')
API_KEY = key_info.get('API_KEY', '')
SECRET_KEY = key_info.get('SECRET_KEY', '')

client = None
if APP_ID and API_KEY and SECRET_KEY:
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def getcn():
    try:
        image_path = 'images/test.jpg'
        if not os.path.exists(image_path):
            return "未识别"

        with open(image_path, 'rb') as f:
            img = f.read()

        if not client:
            return "未配置KEY"

        res = client.basicGeneral(img)
        car_number = ""

        for words in res.get('words_result', []):
            tmp = words['words']
            tmp = re.sub(
                r'[^京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼ABCDEFGHJKLMNPQRSTUVWXYZ0-9]', '',
                tmp)
            if 6 <= len(tmp) <= 8:
                car_number = tmp
                break

        return car_number if car_number else "未识别"

    except:
        return "未识别"