class MemoryAgent:
    def __init__(self):
        self.memory = []  # 存储会话记忆
        self.system_prompt = "你是一个有记忆功能的智能体，会记住用户的信息"

    def handle_input(self, user_input):
        # 核心逻辑：判断是否为重置记忆指令
        if user_input.strip() == "重置记忆":
            self.memory.clear()
            return "记忆已重置，请重新介绍自己"

        # 记忆存储逻辑
        self.memory.append(user_input)
        # 模拟LLM回复（实际场景可对接真实LLM）
        if "我叫" in user_input:
            name = user_input.replace("我叫", "").strip()
            return f"我记住啦，你是{name}！"
        elif "我喜欢" in user_input:
            return f"我记住你的爱好啦~ 当前记忆内容：{self.memory}"
        else:
            return f"当前记忆内容：{self.memory}"


# 测试对话流程
if __name__ == "__main__":
    agent = MemoryAgent()
    # 一轮完整对话测试
    print(agent.handle_input("我叫小红"))
    print(agent.handle_input("我喜欢什么？"))
    print(agent.handle_input("重置记忆"))
    print(agent.handle_input("我喜欢什么？"))