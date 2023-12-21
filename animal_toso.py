import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Siro(pg.sprite.Sprite):
    def __init__(self, num: int, zahyo: int, size: float, iro):
        """
        城を置く
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/siro{num}.png"), 0, size)
        self.img = pg.transform.flip(img0, True, False)  # デフォルトの城
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.center = zahyo, 550
        self.hp = 5000

        self.change_HP = self.font.render(f"{self.hp}/5000", 0, iro)
        self.rect_HP = self.change_HP.get_rect()
        self.rect_HP.center = zahyo, 420


    def update(self, screen: pg.Surface):
        """
        城の描画判定
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.change_HP,self.rect_HP)

class Money:
    def __init__(self,amount):
        self.amount=amount
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.color = (255, 220, 0)
        self.image = self.font.render(f"{self.amount}/3000円", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 1450, 50
    def increase(self, amount): # お金が増える関数、3000で止まる
        if self.amount >= 3000:
            self.amount = 3000
        else:
            self.amount += amount
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"{self.amount}/3000円", 0, self.color)
        screen.blit(self.image, self.rect)

def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    tmr = 0
    clock = pg.time.Clock()
    money = Money(0)


    enemy_siro = Siro(0, 200, 0.4,(0,0,0))
    siro = Siro(1, 1400, 0.3,(255,255,255))
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0  
        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen)
        money.increase(1) # Increase the money
        money.update(screen)
        pg.display.update()

        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()