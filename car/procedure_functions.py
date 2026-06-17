import sys
import pygame
import time
import pandas as pd
import ocrutil
import timeutil

def check_events(settings, recognition_button, ownerInfo_table, carInfo_table, history_table, path):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = recognition_button.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked:
                try:
                    carnumber = ocrutil.getcn()
                    localtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                    settings.carnumber = '车牌号码: ' + carnumber

                    owner_carnumbers = ownerInfo_table[['车牌号']]
                    carnumbers = ownerInfo_table['车牌号'].values

                    carInfo_carnumbers = carInfo_table[['carnumber', 'inDate', 'isOwner', 'validityDate']].values
                    cars = carInfo_table['carnumber'].values

                    append_carInfo = {'carnumber': carnumber}
                    append_history = {'carnumber': carnumber}
                    carInfo_length = len(carInfo_carnumbers)

                    if carInfo_length == 0:
                        in_park(owner_carnumbers, carnumbers, carInfo_table, append_carInfo, carnumber, localtime, settings, path)
                    else:
                        if carnumber in cars:
                            i = 0
                            for carInfo_carnumber in carInfo_carnumbers:
                                if carnumber == carInfo_carnumber[0]:
                                    if carInfo_carnumber[2] == 1:
                                        msgMessage = '业主车，可出停车场'
                                        parkPrice = '业主免费'
                                    else:
                                        price = timeutil.priceCalc(carInfo_carnumber[1], localtime)
                                        msgMessage = '停车费用: ' + str(5 * price)
                                        parkPrice = 5 * int(price)

                                    carInfo_table = carInfo_table.drop([i])
                                    append_history['outData'] = localtime
                                    append_history['price'] = parkPrice
                                    append_history['isOwner'] = carInfo_carnumber[2]
                                    append_history['validityDate'] = carInfo_carnumber[3]
                                    history_table = pd.concat([history_table, pd.DataFrame([append_history])], ignore_index=True)

                                    settings.comeInTime = '出场时间: ' + localtime
                                    settings.message = msgMessage

                                    carInfo_table.to_excel(path + '停车场车辆表.xlsx', sheet_name='data', index=False)
                                    history_table.to_excel(path + '停车场历史表.xlsx', sheet_name='data', index=False)
                                    break
                                i += 1
                        else:
                            if carInfo_length < settings.total:
                                in_park(owner_carnumbers, carnumbers, carInfo_table, append_carInfo, carnumber, localtime, settings, path)
                            else:
                                settings.comeInTime = '进场时间: ' + localtime
                                settings.message = '停车场已满，无法进入'
                except Exception as e:
                    print("错误原因: ", e)
                    continue

def in_park(owner_carnumbers, carnumbers, carInfo_table, append_carInfo, carnumber, localtime, settings, path):
    if carnumber in carnumbers:
        msgMessage = '提示信息: 业主车，可入停车场'
        append_carInfo['isOwner'] = 1
        append_carInfo['validityDate'] = ''
    else:
        msgMessage = '提示信息: 外来车，可入停车场'
        append_carInfo['isOwner'] = 0
        append_carInfo['validityDate'] = ''

    append_carInfo['inDate'] = localtime
    append_carInfo['outData'] = ''
    append_carInfo['price'] = 0
    settings.comeInTime = '进场时间: ' + localtime
    settings.message = msgMessage

    carInfo_table = pd.concat([carInfo_table, pd.DataFrame([append_carInfo])], ignore_index=True)
    carInfo_table.to_excel(path + '停车场车辆表.xlsx', sheet_name='data', index=False)