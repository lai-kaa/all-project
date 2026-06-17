def check_user(user: dict) -> tuple[bool, str]:
    """校验用户信息，返回 (是否通过, 提示信息)"""
    # 校验姓名
    if not isinstance(user.get("name"), str) or len(user.get("name", "").strip()) == 0:
        return False, "姓名必须是非空字符串"

    # 校验年龄
    age = user.get("age")
    if not isinstance(age, int) or not (0 <= age <= 150):
        return False, "年龄必须是0-150之间的整数"

    # 校验邮箱
    email = user.get("email")
    if not isinstance(email, str) or "@" not in email:
        return False, "邮箱必须包含@符号"

    return True, "用户信息校验通过"


if __name__ == "__main__":
    # 测试示例
    user1 = {"name": "张三", "age": 25, "email": "zhangsan@example.com"}
    user2 = {"name": "", "age": 200, "email": "lisi.example.com"}
    user3 = {"name": "李四", "age": "30", "email": "lisi@example.com"}

    print(check_user(user1))
    print(check_user(user2))
    print(check_user(user3))


def get_mock_weather(city: str) -> str:
    """根据内置字典返回城市天气描述，不需要真实接口"""
    weather_dict = {
        "北京": "晴，温度15-25℃",
        "上海": "多云，温度18-28℃",
        "广州": "雷阵雨，温度22-30℃"
    }
    return weather_dict.get(city, "暂未查询到该城市天气信息")


def format_weather(city: str, weather: str) -> str:
    """把城市名和天气信息拼成一句好读的话"""
    return f"城市{city}的天气情况为：{weather}"


if __name__ == "__main__":
    # 读取用户输入并查询天气
    city = input("请输入要查询的城市：")
    weather_info = get_mock_weather(city)
    result = format_weather(city, weather_info)
    print(result)

    # 可再次测试其他城市
    city2 = input("请输入另一个要查询的城市：")
    weather_info2 = get_mock_weather(city2)
    result2 = format_weather(city2, weather_info2)
    print(result2)


class SimpleMCPServer:
    """只管理一个简单工具的极简服务器"""

    def __init__(self, name: str):
        self.name = name
        self.tools = {}

    def register_tool(self, tool_name: str, tool_func):
        """注册工具：只保存名称到函数的映射"""
        self.tools[tool_name] = tool_func

    def call_tool(self, tool_name: str, **kwargs):
        """根据名称找到函数并调用"""
        if tool_name not in self.tools:
            return f"工具 {tool_name} 未注册"
        return self.tools[tool_name](**kwargs)


def read_file_tool(filename: str) -> str:
    """尝试读取文件内容；如果文件不存在，返回友好提示"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"文件 {filename} 不存在"


# 可选扩展：列出当前目录文件
import os


def list_files_tool() -> str:
    """列出当前目录的文件名"""
    files = os.listdir(".")
    return "当前目录文件列表：" + ", ".join(files)


def main():
    # 创建服务器并注册工具
    server = SimpleMCPServer("file_manager")
    server.register_tool("read_file", read_file_tool)
    server.register_tool("list_files", list_files_tool)  # 可选扩展

    # 调用工具
    print(server.call_tool("read_file", filename="test_mcp.txt"))
    print(server.call_tool("list_files"))  # 可选扩展


if __name__ == "__main__":
    main()