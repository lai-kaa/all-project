import pygame.font
import os

line_color = (0, 0, 0)
text_color = (0, 0, 0)
# 强制使用系统微软雅黑，中文完美显示
try:
    font_path = "C:/Windows/Fonts/msyh.ttc"
    font_ok = True
except:
    font_ok = False

def draw_bg(screen):
    if font_ok:
        bgfont = pygame.font.Font(font_path, 15)
    else:
        bgfont = pygame.font.SysFont("SimHei", 15)
    pygame.draw.aaline(screen, line_color, (662, 30), (980, 30))
    text_image = bgfont.render('识别信息：', True, text_color)
    screen.blit(text_image, (660, 370))

def draw_text(screen, text, x, y, size, color=(0, 0, 0)):
    if font_ok:
        font = pygame.font.Font(font_path, size)
    else:
        font = pygame.font.SysFont("SimHei", size)
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))