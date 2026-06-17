# 这行是导入tkinter库，用来做窗口界面的，给它起个小名叫tk
import tkinter as tk

# 从tkinter里面拿出两个工具：文件选择窗口和消息提示窗口
from tkinter import filedialog, messagebox

# 导入OpenCV，这是专门处理图片的库，我们叫它cv2
import cv2

# 导入numpy，这是处理数组和矩阵的库，我们叫它np
import numpy as np

# 导入操作系统相关的功能，暂时没用到，但先留着
import os


# ===================== 下面是通用的工具函数 =====================

# 定义一个专门读图片的函数，因为OpenCV默认不支持中文路径
def cv_imread(file_path):
    """
    读取图片，支持中文路径
    先读成二进制数据，再转成图片格式
    """
    # 把文件路径转成二进制数据流
    # 再从二进制数据流解码成图片
    return cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)


# 检查图片是否真的读成功了
def check_img_read(img, img_name):
    """
    如果图片是空的，就弹窗报错
    """
    # 如果img是None（就是空的意思）
    if img is None:
        # 弹出一个错误窗口，告诉用户哪个图片没读出来
        messagebox.showerror("错误", f"无法读取图像：\n{img_name}")
        # 返回False表示没成功
        return False
    # 返回True表示成功了
    return True


# 同时显示多张图片的函数
def show_imgs(win_names, imgs, wait_time=0):
    """
    开多个窗口显示多张图片
    win_names是窗口名字列表
    imgs是对应的图片列表
    """
    # 用zip把窗口名和图片配对，一对一对处理
    for win_name, img in zip(win_names, imgs):
        # 用cv2显示图片，窗口名是win_name
        cv2.imshow(win_name, img)

    # 等待按键，如果不按键就一直显示
    cv2.waitKey(wait_time)

    # 关掉所有OpenCV开的窗口
    cv2.destroyAllWindows()


# 让用户选择图片的函数
def select_image(title="选择图片"):
    """
    弹出一个文件选择窗口
    用户选完就自动读取图片
    """
    # 弹出文件选择对话框
    path = filedialog.askopenfilename(
        title=title,  # 窗口标题
        filetypes=[("图像文件", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]  # 只能选图片格式
    )

    # 如果用户没选文件（点了取消）
    if not path:
        # 返回None，表示什么都没有
        return None

    # 调用我们写的支持中文的读图函数
    img = cv_imread(path)

    # 检查图片是不是真读出来了
    if not check_img_read(img, path):
        return None

    # 把读出来的图片返回给调用者
    return img


# 让用户在图片上画矩形的函数
def select_roi(img, win_name="画矩形：左键按下拖动，松开确认"):
    """
    用户用鼠标画个矩形框
    返回框的坐标和大小
    """
    # 准备一个字典记录画框的状态
    # drawing表示是否正在画
    # x0,y0是起点，x1,y1是终点
    roi = {"drawing": False, "x0": 0, "y0": 0, "x1": 0, "y1": 0}

    # 定义鼠标回调函数（就是鼠标操作时自动调用的函数）
    def mouse_cb(event, x, y, flags, param):
        # 如果鼠标左键按下去了
        if event == cv2.EVENT_LBUTTONDOWN:
            # 标记开始画框
            roi["drawing"] = True
            # 记录起点坐标
            roi["x0"], roi["y0"] = x, y

        # 如果鼠标在移动而且正在画框
        elif event == cv2.EVENT_MOUSEMOVE and roi["drawing"]:
            # 复制一份原图（避免在原始图片上直接画）
            tmp = img.copy()
            # 从起点到当前鼠标位置画一个绿色矩形
            cv2.rectangle(tmp, (roi["x0"], roi["y0"]), (x, y), (0, 255, 0), 2)
            # 显示这个临时图片
            cv2.imshow(win_name, tmp)

        # 如果鼠标左键松开了
        elif event == cv2.EVENT_LBUTTONUP:
            # 标记停止画框
            roi["drawing"] = False
            # 记录终点坐标
            roi["x1"], roi["y1"] = x, y
            # 在原始图片上画最终的框
            cv2.rectangle(img, (roi["x0"], roi["y0"]), (x, y), (0, 255, 0), 2)
            # 显示带框的图片
            cv2.imshow(win_name, img)

    # 创建一个窗口
    cv2.namedWindow(win_name)
    # 设置鼠标回调函数（就是告诉电脑：鼠标在这个窗口操作时，调用mouse_cb函数）
    cv2.setMouseCallback(win_name, mouse_cb)

    # 显示图片
    cv2.imshow(win_name, img)

    # 等待用户操作（按键或画框）
    cv2.waitKey(0)

    # 关掉这个窗口
    cv2.destroyWindow(win_name)

    # 如果终点坐标还是(0,0)（就是用户没画框）
    if roi["x1"] == 0 and roi["y1"] == 0:
        # 返回None表示没画
        return None

    # 计算矩形左上角坐标（因为用户可能从右下往左上画）
    x, y = min(roi["x0"], roi["x1"]), min(roi["y0"], roi["y1"])

    # 计算矩形的宽和高
    w, h = abs(roi["x1"] - roi["x0"]), abs(roi["y1"] - roi["y0"])

    # 返回矩形的位置和大小
    return (x, y, w, h)


# ===================== 下面是8个具体的图片处理功能 =====================

# 功能1：两张图片叠加
def img_add():
    """
    选两张图片，把它们加在一起
    """
    # 选第一张图片
    img1 = select_image("选择第一张图片")
    # 选第二张图片
    img2 = select_image("选择第二张图片")

    # 如果有一张没选成功，就不继续了
    if img1 is None or img2 is None:
        return

    # 统一两张图片的尺寸（取最小的那个尺寸）
    h = min(img1.shape[0], img2.shape[0])  # 高度取最小值
    w = min(img1.shape[1], img2.shape[1])  # 宽度取最小值

    # 把两张图片都缩放到这个尺寸
    img1 = cv2.resize(img1, (w, h))
    img2 = cv2.resize(img2, (w, h))

    # 把两张图片叠加（就是对应像素值相加）
    result = cv2.add(img1, img2)

    # 显示叠加后的结果
    cv2.imshow("叠加结果", result)
    # 等待按键
    cv2.waitKey(0)
    # 关掉窗口
    cv2.destroyAllWindows()


# 功能2：提取图片中的某个区域
def img_mask_bitwise():
    """
    让用户画个框，只保留框里的内容
    """
    # 选一张图片
    img = select_image("选择要提取区域的图片")
    if img is None:
        return

    # 让用户画矩形框（用图片的拷贝，避免在原图上画）
    roi = select_roi(img.copy(), "画要提取的矩形区域")

    # 如果用户没画框
    if roi is None:
        # 弹窗提示
        messagebox.showinfo("提示", "未选择区域，操作取消")
        return

    # 拆开矩形的信息：x,y是左上角坐标，w,h是宽高
    x, y, w, h = roi

    # 创建一个全黑的掩膜（和图片一样大）
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    # 把矩形区域涂成白色
    mask[y:y + h, x:x + w] = 255

    # 用"按位与"操作，只保留掩膜白色区域的内容
    result = cv2.bitwise_and(img, img, mask=mask)

    # 显示原图和提取结果
    cv2.imshow("原图", img)
    cv2.imshow("提取结果", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 功能3：给图片打马赛克
def img_mosaic():
    """
    在图片的某个区域打马赛克
    """
    # 选一张图片
    img = select_image("选择要打马赛克的图片")
    if img is None:
        return

    # 让用户画要打码的区域
    roi = select_roi(img.copy(), "画要打码的矩形区域")
    if roi is None:
        messagebox.showinfo("提示", "未选择区域，操作取消")
        return

    # 拆开矩形信息
    x, y, w, h = roi

    # 马赛克块的大小
    size = 20

    # 复制原图（避免修改原图）
    mosaic = img.copy()

    # 在矩形区域内打马赛克
    for i in range(y, y + h, size):  # 从上到下，每次跳一个马赛克块
        for j in range(x, x + w, size):  # 从左到右，每次跳一个马赛克块
            # 取当前块的左上角颜色
            color = img[i, j]
            # 把这个颜色填满整个马赛克块
            mosaic[i:i + size, j:j + size] = color

    # 在原图上用绿框标出马赛克区域
    cv2.rectangle(mosaic, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示原图和马赛克效果
    show_imgs(["原图", "马赛克效果"], [img, mosaic])


# 功能4：调整图片大小
def img_resize():
    """
    让用户输入宽高，调整图片尺寸
    """
    # 选一张图片
    img = select_image("选择要调整大小的图片")
    if img is None:
        return

    # 创建一个新的输入窗口
    input_win = tk.Toplevel()  # Toplevel就是子窗口
    input_win.title("输入目标尺寸")  # 窗口标题
    input_win.geometry("250x150")  # 窗口大小
    input_win.resizable(False, False)  # 不允许用户调整窗口大小

    # 创建"宽度："标签
    tk.Label(input_win, text="宽度：").grid(row=0, column=0, padx=10, pady=10)
    # 创建"高度："标签
    tk.Label(input_win, text="高度：").grid(row=1, column=0, padx=10, pady=10)

    # 创建宽度输入框
    width_entry = tk.Entry(input_win, width=10)
    # 创建高度输入框
    height_entry = tk.Entry(input_win, width=10)

    # 把输入框放到窗口里
    width_entry.grid(row=0, column=1)
    height_entry.grid(row=1, column=1)

    # 定义"确定"按钮按下的操作
    def apply_resize():
        try:
            # 从输入框获取宽度和高度，转成整数
            w = int(width_entry.get())
            h = int(height_entry.get())

            # 检查宽高是不是正数
            if w <= 0 or h <= 0:
                raise ValueError  # 如果不是，就报错
        except ValueError:
            # 如果输入的不是数字或者是负数，就弹窗报错
            messagebox.showerror("输入错误", "请输入正整数宽高！")
            return

        # 调整图片大小
        resized = cv2.resize(img, (w, h))

        # 显示原图和调整后的图片
        cv2.imshow("原图", img)
        cv2.imshow(f"调整后 ({w}×{h})", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 关掉输入窗口
        input_win.destroy()

    # 创建"确定"按钮
    tk.Button(input_win, text="确定", command=apply_resize).grid(row=2, column=0, columnspan=2, pady=10)


# 功能5：检测图片边缘
def img_edge_detect():
    """
    用三种方法检测图片的边缘
    """
    # 选一张图片
    an = select_image("选择要做边缘检测的图片")
    if an is None:
        return

    # 把彩色图转成灰度图（因为边缘检测一般用灰度图）
    an = cv2.cvtColor(an, cv2.COLOR_BGR2GRAY)

    # 用Sobel算子检测x方向的边缘
    anX = cv2.Sobel(an, -1, dx=1, dy=0)
    # 用Sobel算子检测y方向的边缘
    anY = cv2.Sobel(an, -1, dx=0, dy=1)
    # 把x和y方向的结果合并
    anSobel = cv2.addWeighted(anX, 0.5, anY, 0.5, 0)

    # 用Scharr算子检测x方向边缘（比Sobel更敏感）
    anX_scharr = cv2.Scharr(an, -1, dx=1, dy=0)
    # 用Scharr算子检测y方向边缘
    anY_scharr = cv2.Scharr(an, -1, dx=0, dy=1)
    # 合并Scharr的结果
    anScharr = cv2.addWeighted(anX_scharr, 0.5, anY_scharr, 0.5, 0)

    # 用Laplacian算子检测边缘
    anLaplacian = cv2.Laplacian(an, -1, ksize=3)

    # 同时显示四种结果
    show_imgs(["原图(灰度)", "Sobel", "Scharr", "Laplacian"],
              [an, anSobel, anScharr, anLaplacian])


# 功能6：给图片补洞/填充
def img_morphology():
    """
    用形态学操作填充图片中的空洞
    """
    # 选一张图片
    img = select_image("选择要补洞的图片")
    if img is None:
        return

    # 转成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 创建一个10x10的白色方块（这就是结构元素）
    kernel = np.ones((10, 10), np.uint8)

    # 做闭运算（先膨胀后腐蚀），可以填充小洞
    filled = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=3)

    # 显示填充结果
    cv2.imshow("补洞结果", filled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 功能7：对图片进行各种变换
def img_transform():
    """
    平移、旋转、缩放、透视变换
    """

    # 定义一个通用的输入对话框函数
    def _input_dialog(title, fields, callback):
        """
        创建一个输入参数的窗口
        title: 窗口标题
        fields: 要输入的字段列表，比如[("角度", "30"), ("缩放", "1.0")]
        callback: 用户输完后要调用的函数
        """
        # 创建输入窗口
        win = tk.Toplevel()
        win.title(title)
        win.resizable(False, False)  # 不能调整大小

        # 用来存输入框的字典
        entries = {}

        # 为每个字段创建标签和输入框
        for idx, (label, default) in enumerate(fields):
            # 创建标签（比如"角度："）
            tk.Label(win, text=label).grid(row=idx, column=0, padx=8, pady=4)

            # 创建输入框
            e = tk.Entry(win, width=8)
            e.insert(0, str(default))  # 设置默认值
            e.grid(row=idx, column=1, padx=8, pady=4)

            # 把输入框存起来
            entries[label] = e

        # 定义"确定"按钮的点击事件
        def on_ok():
            try:
                # 从所有输入框获取值，转成浮点数
                values = {k: float(v.get()) for k, v in entries.items()}
            except ValueError:
                # 如果输入的不是数字，就报错
                messagebox.showerror("输入错误", "请填写数字！")
                return

            # 关掉输入窗口
            win.destroy()
            # 调用回调函数，把用户输入的值传过去
            callback(values)

        # 创建"确定"按钮
        tk.Button(win, text="确定", command=on_ok).grid(
            row=len(fields), column=0, columnspan=2, pady=8)

        # 等待用户输入（这个窗口不关，程序就停在这里）
        win.wait_window()

    # ---------- 主流程开始 ----------

    # 选一张图片
    img = select_image("选择要变换的图片")
    if img is None:
        return

    # 获取图片的高度和宽度
    h, w = img.shape[:2]

    # 创建一个变量来存用户选择的变换类型
    choice = tk.StringVar(value="translate")

    # 创建选择变换类型的窗口
    top = tk.Toplevel()
    top.title("选择变换类型")
    top.resizable(False, False)

    # 创建四个单选按钮
    for txt, val in [("平移", "translate"),
                     ("旋转", "rotate"),
                     ("缩放", "scale"),
                     ("透视", "perspective")]:
        tk.Radiobutton(top, text=txt, variable=choice, value=val,
                       anchor="w").pack(fill="x", padx=10, pady=2)

    # 创建"下一步"按钮
    tk.Button(top, text="下一步", command=top.destroy).pack(pady=5)

    # 等待用户选择
    top.wait_window()

    # ---------- 下面是四种变换的具体实现 ----------

    def do_translate(v):
        """平移图片"""
        dx, dy = int(v["dx"]), int(v["dy"])  # 获取x和y方向的移动距离

        # 创建平移矩阵：[[1, 0, dx], [0, 1, dy]]
        M = np.float32([[1, 0, dx], [0, 1, dy]])

        # 应用平移变换
        out = cv2.warpAffine(img, M, (w, h), borderValue=(0, 255, 0))

        # 显示结果
        cv2.imshow(f"平移 dx={dx} dy={dy}", out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def do_rotate(v):
        """旋转图片"""
        angle, scale = v["angle"], v["scale"]  # 获取旋转角度和缩放比例

        # 创建旋转矩阵（绕图片中心旋转）
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)

        # 应用旋转变换
        out = cv2.warpAffine(img, M, (w, h))

        # 显示结果
        cv2.imshow(f"旋转 angle={angle} scale={scale}", out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def do_scale(v):
        """缩放图片"""
        sx, sy = v["sx"], v["sy"]  # 获取x和y方向的缩放比例

        # 创建缩放矩阵：[[sx, 0, 0], [0, sy, 0]]
        M = np.float32([[sx, 0, 0], [0, sy, 0]])

        # 应用缩放变换
        out = cv2.warpAffine(img, M, (w, h))

        # 显示结果
        cv2.imshow(f"缩放 sx={sx} sy={sy}", out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def do_perspective(v):
        """透视变换（让图片看起来有立体感）"""
        # 定义原图的四个角点
        src = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

        # 定义变换后的四个角点（根据用户输入）
        dst = np.float32([[v["x1"], v["y1"]],
                          [w - v["x2"], v["y2"]],
                          [v["x3"], h - v["y3"]],
                          [w - v["x4"], h - v["y4"]]])

        # 计算透视变换矩阵
        M = cv2.getPerspectiveTransform(src, dst)

        # 应用透视变换
        out = cv2.warpPerspective(img, M, (w, h), borderValue=(255, 255, 255))

        # 显示结果
        cv2.imshow("透视变换", out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # ---------- 根据用户的选择调用对应的函数 ----------

    # 获取用户选择的变换类型
    c = choice.get()

    # 如果是平移
    if c == "translate":
        _input_dialog("平移参数", [("dx", 100), ("dy", 50)], do_translate)

    # 如果是旋转
    elif c == "rotate":
        _input_dialog("旋转参数", [("angle", 75), ("scale", 0.6)], do_rotate)

    # 如果是缩放
    elif c == "scale":
        _input_dialog("缩放参数", [("sx", 0.6), ("sy", 0.5)], do_scale)

    # 如果是透视变换
    elif c == "perspective":
        _input_dialog("透视偏移",
                      [("x1", 100), ("y1", 120),
                       ("x2", 100), ("y2", 120),
                       ("x3", 0), ("y3", 0),
                       ("x4", 0), ("y4", 0)],
                      do_perspective)


# 功能8：提高图片亮度/增强对比度
def img_hist_equalize():
    """
    让图片变得更亮，对比度更强
    """
    # 选一张图片
    img = select_image("选择要做直方图均衡的图片")
    if img is None:
        return

    # 把BGR颜色空间转成HSV颜色空间
    # HSV：H色相，S饱和度，V明度（亮度）
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 把HSV三个通道分开
    h, s, v = cv2.split(hsv)

    # 只对V通道（亮度通道）做直方图均衡
    v_eq = cv2.equalizeHist(v)

    # 把三个通道重新合并
    hsv_eq = cv2.merge([h, s, v_eq])

    # 转回BGR颜色空间
    result = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)

    # 显示原图和提亮后的结果
    cv2.imshow("原图", img)
    cv2.imshow("提亮结果", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ===================== 创建主界面 =====================

# 定义一个App类，继承自tk.Tk（tk.Tk是tkinter的主窗口类）
class App(tk.Tk):
    """
    主程序窗口
    """

    def __init__(self):
        # 调用父类的初始化方法
        super().__init__()

        # 设置窗口标题
        self.title("OpenCV 图像处理小工具")

        # 设置窗口大小：宽400像素，高480像素
        self.geometry("400x480")

        # 按钮列表：每个按钮的文字和对应的函数
        btn_list = [
            ("1 图片叠加", img_add),
            ("2 区域提取", img_mask_bitwise),
            ("3 打马赛克", img_mosaic),
            ("4 调整大小", img_resize),
            ("5 轮廓检测", img_edge_detect),
            ("6 补洞/填充", img_morphology),
            ("7 平移/旋转/变形", img_transform),
            ("8 提亮/增强对比", img_hist_equalize),
        ]

        # 循环创建每个按钮
        for txt, cmd in btn_list:
            # 创建按钮：文字是txt，宽度28，点击时执行cmd函数
            tk.Button(self, text=txt, width=28, command=cmd).pack(pady=4)

        # 创建退出按钮（红色文字）
        tk.Button(self, text="0 退出", width=28, fg="red",
                  command=self.destroy).pack(pady=12)


# 程序入口
if __name__ == "__main__":
    # 创建App对象
    App().mainloop()  # 启动事件循环，让窗口显示出来