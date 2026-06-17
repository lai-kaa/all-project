# 模拟基础Agent的核心逻辑
class BasicAgent:
    def __init__(self):
        # 修改点1：调整系统提示词，设置为学习助手口吻（添加注释标记）
        self.system_prompt = "你是一个贴心的学习助手，说话温和亲切，会耐心解答用户的各种问题"

    # 模拟天气查询工具
    def get_weather(self, city):
        # 模拟获取天气数据（实际场景可对接天气API）
        weather_dict = {
            "北京": "晴，气温28℃",
            "上海": "小雨，气温22℃",
            "广州": "多云，气温30℃"
        }
        weather_info = weather_dict.get(city, "暂未查询到该城市天气")

        # 修改点2：根据天气添加建议（添加注释标记）
        if "晴" in weather_info:
            weather_info += "，建议做好防晒措施哦~"
        elif "雨" in weather_info:
            weather_info += "，出门记得带伞呀~"
        return weather_info

    # 对话交互函数
    def chat(self, user_input):
        if "天气" in user_input:
            city = user_input.replace("天气", "").strip()
            return self.get_weather(city)
        else:
            return f"[学习助手] {user_input} 这个问题我会努力学习解答哒~"


# 测试运行
if __name__ == "__main__":
    agent = BasicAgent()
    # 提问两个不同城市的天气
    print(agent.chat("北京天气"))
    print(agent.chat("上海天气"))