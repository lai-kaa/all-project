import os
import requests
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = os.getenv('DEEPSEEK_BASE_URL') or os.getenv('API_BASE_URL')
QWEATHER_KEY = os.getenv('QWEATHER_KEY')


def get_weather(location):
    """
    获取指定位置的实时天气信息（使用和风天气API）
    :param location: 位置名称（城市名）
    :return: 天气信息字典
    """
    try:
        # 1. 先获取城市ID
        location_url = "https://geoapi.qweather.com/v2/city/lookup"
        location_params = {
            "location": location,
            "key": QWEATHER_KEY
        }

        location_response = requests.get(location_url, params=location_params)
        location_response.raise_for_status()
        location_data = location_response.json()

        if location_data["code"] != "200" or not location_data["location"]:
            raise Exception(f"未找到城市: {location}")

        city_id = location_data["location"][0]["id"]

        # 2. 获取实时天气
        weather_url = "https://devapi.qweather.com/v7/weather/now"
        weather_params = {
            "location": city_id,
            "key": QWEATHER_KEY,
            "unit": "m"
        }

        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if weather_data["code"] != "200":
            raise Exception("获取天气信息失败")

        # 格式化返回数据
        now = weather_data["now"]
        return {
            "location": location,
            "update_time": weather_data["updateTime"],
            "obs_time": now["obsTime"],
            "temp": now["temp"],
            "feels_like": now["feelsLike"],
            "text": now["text"],
            "wind_dir": now["windDir"],
            "wind_scale": now["windScale"],
            "humidity": now["humidity"]
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"获取天气信息失败: {str(e)}")
    except KeyError as e:
        raise Exception(f"解析天气数据失败: {str(e)}")


def call_deepseek_function(function_name, parameters):
    """
    调用DeepSeek API中的函数
    :param function_name: 函数名称
    :param parameters: 函数参数
    :return: 函数调用结果
    """
    if not DEEPSEEK_API_URL or not DEEPSEEK_API_KEY:
        raise ValueError("API配置未设置，请检查环境变量")

    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'function_name': function_name,
        'parameters': parameters
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")


if __name__ == "__main__":
    try:
        cities = ["南京", "北京", "上海"]
        for city in cities:
            weather = get_weather(city)
            print(f"\n{city}的实时天气信息：")
            print(f"温度: {weather['temp']}°C")
            print(f"体感温度: {weather['feels_like']}°C")
            print(f"天气状况: {weather['text']}")
            print(f"风向: {weather['wind_dir']}")
            print(f"风力等级: {weather['wind_scale']}级")
            print(f"相对湿度: {weather['humidity']}%")
    except Exception as e:
        print("函数调用失败：", str(e))