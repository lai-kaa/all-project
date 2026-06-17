import pandas as pd

# 新增统计工具函数：统计MonthlyCharges大于阈值的用户数
def count_high_charges(threshold: float, data_path: str = "telco_data.csv"):
    try:
        df = pd.read_csv(data_path)
        count = len(df[df["MonthlyCharges"] > threshold])
        print(f"高于阈值的用户数：{count}")
        return count
    except FileNotFoundError:
        print("错误：未找到telco_data.csv文件")
        return 0

# 智能体工具列表
agent_tools = [
    {
        "name": "count_high_charges",
        "func": count_high_charges,
        "description": "统计telco_data.csv中MonthlyCharges大于指定阈值的用户数量"
    }
]

# 测试运行
if __name__ == "__main__":
    # 输入阈值（示例：100）
    threshold = float(input("请输入阈值："))
    # 调用工具
    for tool in agent_tools:
        if tool["name"] == "count_high_charges":
            tool["func"](threshold)