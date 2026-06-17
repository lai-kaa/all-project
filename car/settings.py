class Settings():
    def __init__(self):
        """初始化设置"""
        # 屏幕设置（宽、高、背景色、线颜色）
        self.screen_width = 1000
        self.screen_height = 484
        self.bg_color = (255, 255, 255)

        # 停车位总数
        self.total = 100

        # 识别颜色、车牌号、进来时间、出入场信息
        self.ocr_color = (212, 35, 122)
        self.carnumber = ''
        self.comeInTime = ''
        self.message = ''