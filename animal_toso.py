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
    def __init__(self, num: int, zahyo: int, size: float):
        """
        城を置く
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/siro{num}.png"), 0, size)
        self.img = pg.transform.flip(img0, True, False)  # デフォルトの城

        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.center = zahyo, 550
        self.hp = 5000


    def update(self, screen: pg.Surface):
        """
        城の描画判定
        """
        screen.blit(self.image, self.rect)
class Money:
    """
    左上のお金を表示させるクラス
    Qキーを押すとレベルがあがる
    """
    def __init__(self,amount,bunbo,level):
        self.amount = amount
        self.bunbo = bunbo
        self.level = level
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.color = (255, 220, 0)
        self.image = self.font.render(f"{self.amount}/{self.bunbo}円", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 1450, 50

        self.text = self.font.render(f"お金LEVEL：{self.level}",0,self.color)
        self.rect_text = self.text.get_rect()
        self.rect_text.center = 200,HEIGHT-50

        
        

    def increase(self, amount): # お金が増える関数、3000で止まる
        if self.amount >= self.bunbo:
            self.amount = self.bunbo
        else:
            self.amount += amount
    
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"{self.amount}/{self.bunbo}円", 0, self.color)
        screen.blit(self.image, self.rect)
        self.text = self.font.render(f"お金LEVEL：{self.level}",0,self.color)
        screen.blit(self.text, self.rect_text)

def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    ###後から修正する部分
    """
    white = (255,255,255)
    ell = pg.Surface((100, 100))
    pg.draw.ellipse(ell,white,[800,450,50,100])
    pg.display.flip()
    """

    tmr = 0
    clock = pg.time.Clock()
    money = Money(0,1500,1)


    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)

    while True:
        if money.color == (255,220,0):
            p = 0
            money.increase(1)
        elif money.color == (255,0,0):
            p = 800
            money.level = 2
            money.increase(2)
        elif money.color == (0,0,0):
            money.increase(3)
            money.level = 3     

        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0  
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_2:
                    if money.amount >= 701 + p:
                        money.bunbo += 1500
                        money.amount -= 700
                        if money.color ==(255,220,0):
                            money.color =(255,0,0)
                            money.increase(2)
                        elif money.color == (255,0,0):
                            money.color = (0,0,0)
                            money.increase(3)
                            money.amount -=800
                        else:
                            money.color = (0,0,0)
                            money.bunbo -= 1500
                            money.increase(3)
                            money.amount +=700

        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen) 

        money.update(screen)
        pg.display.update()

        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()