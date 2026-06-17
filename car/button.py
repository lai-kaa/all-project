import pygame.font
import os

class Button():
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 100, 50
        self.button_color = (0, 120, 215)
        self.text_color = (255, 255, 255)

        FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
        if os.path.exists(FONT_PATH):
            self.font = pygame.font.Font(FONT_PATH, 25)
        else:
            try:
                self.font = pygame.font.SysFont("Microsoft YaHei", 25)
            except:
                self.font = pygame.font.Font(None, 25)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = 640 - self.width / 2 + 2
        self.rect.centery = 480 - self.height / 2 + 2
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)