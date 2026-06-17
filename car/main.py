import pygame
import cv2
import os
import pandas as pd

from settings import Settings
from button import Button
import textboard
import procedure_functions as pf

cdir = os.getcwd()
path = cdir + '/file/'

if not os.path.exists(path):
    os.makedirs(path)

owner_file = path + '住户车辆表.xlsx'
if not os.path.exists(owner_file):
    df = pd.DataFrame(columns=["车牌号", "姓名", "车位号"])
    df.to_excel(owner_file, sheet_name="data", index=False)

car_file = path + '停车场车辆表.xlsx'
if not os.path.exists(car_file):
    carfile = pd.DataFrame(columns=['carnumber', 'inDate', 'outData', 'price', 'isOwner', 'validityDate'])
    carfile.to_excel(car_file, sheet_name='data', index=False)

history_file = path + '停车场历史表.xlsx'
if not os.path.exists(history_file):
    history_df = pd.DataFrame(columns=['carnumber', 'inDate', 'outData', 'price', 'isOwner', 'validityDate'])
    history_df.to_excel(history_file, sheet_name='data', index=False)

def run_procedure():
    settings = Settings()
    pygame.init()
    pygame.display.set_caption('小区智能车牌识别系统')

    try:
        ic_launcher = pygame.image.load('images/icon_launcher.png')
        pygame.display.set_icon(ic_launcher)
    except:
        print("图标文件不存在，已跳过")

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    try:
        cam = cv2.VideoCapture(0)
    except:
        print("请连接摄像头")

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(settings.bg_color)

        sucess, img = cam.read()
        if sucess:
            if not os.path.exists('images'):
                os.makedirs('images')
            cv2.imencode('.jpg', img)[1].tofile('images/test.jpg')

            image = pygame.image.load('images/test.jpg')
            image = pygame.transform.scale(image, (640, 480))
            screen.blit(image, (2, 2))
        else:
            screen.fill((100, 100, 100), (2, 2, 640, 480))

        recognition_button = Button(screen, '识别')
        recognition_button.draw_button()

        ownerInfo_table = pd.read_excel(path + '住户车辆表.xlsx', sheet_name='data')
        carInfo_table = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data')
        history_table = pd.read_excel(path + '停车场历史表.xlsx', sheet_name='data')

        # 清空空数据，只保留有车牌的行（安全写法，不报错）
        carInfo_table = carInfo_table.dropna(subset=['carnumber'])

        inNumber = len(carInfo_table)

        textboard.draw_bg(screen)
        textboard.draw_text(screen, '共有车位: ' + str(settings.total) + ' 剩余车位: ' + str(settings.total - inNumber), 680, 0, 20)
        textboard.draw_text(screen, '车牌号    进入时间', 700, 40, 15)

        carInfos = carInfo_table.sort_values(by='inDate', ascending=False)
        i = 0
        # 固定行高，绝对不重叠！
        for index, carInfo in carInfos.iterrows():
            if i >= 10:
                break
            # 每行固定间隔 20 像素，绝对整齐
            y = 60 + i * 22
            cn = str(carInfo['carnumber'])
            dt = str(carInfo['inDate'])
            textboard.draw_text(screen, cn + '    ' + dt, 700, y, 15)
            i += 1

        textboard.draw_text(screen, settings.carnumber, 660, 400, 15, settings.ocr_color)
        textboard.draw_text(screen, settings.comeInTime, 660, 422, 15, settings.ocr_color)
        textboard.draw_text(screen, settings.message, 660, 442, 15, settings.ocr_color)

        pf.check_events(settings, recognition_button, ownerInfo_table, carInfo_table, history_table, path)

        pygame.display.flip()
        clock.tick(60)

    cam.release()

if __name__ == '__main__':
    run_procedure()