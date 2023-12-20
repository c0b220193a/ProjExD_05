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
        self.hp = 0


    def update(self, screen: pg.Surface):
        """
        城の描画判定
        """
        screen.blit(self.image, self.rect)


class Exploaion(pg.sprite.Sprite):
    """
    爆発エフェクトに関するクラス
    """
    def __init__(self, zahyo):
        """
        城が爆発するエフェクトを生成する
        引数1 zahyo:hpが0になった城のX座標
        """
        super().__init__()
        self.bakuhatu1_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/bakuhatu1.png"), 0, 0.6)
        self.bakuhatu2_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/bakuhatu2.png"), 0, 0.8)
        self.bakuhatu3_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/bakuhatu3.png"), 0, 1.0)
        self.rect1 = self.bakuhatu1_img.get_rect()
        self.rect2 = self.bakuhatu2_img.get_rect()
        self.rect3 = self.bakuhatu3_img.get_rect()
        self.rect1.center = zahyo, 550
        self.rect2.center = zahyo, 550
        self.rect3.center = zahyo, 550
    
    def update(self, num, screen):
        """
        爆発エフェクトを表現する
        引数1 num:どの画像を使うか
        引数2 screen:画面Surface
        """
        if num == 1:
            screen.blit(self.bakuhatu1_img, self.rect1)
        elif num == 2:
            screen.blit(self.bakuhatu2_img, self.rect2)
        elif num == 3:
            screen.blit(self.bakuhatu3_img, self.rect3)


def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    tmr = 0
    tmr5 = 450
    clock = pg.time.Clock()

    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0                 
        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen)
        if siro.hp <= 0: # 味方の城のHPが0の時
            exploaion = Exploaion(200)
            tmr5 = 0
            if tmr5 <= 100:
                exploaion.update(1, screen)
            elif tmr5 <= 200:
                exploaion.update(2, screen)
            elif tmr5 < 300:
                exploaion.update(3, screen)
        

        elif enemy_siro.hp <= 0: # 敵の城のHPが0の時
            exploaion = Exploaion(1400)
            tmr5 = 0
            if tmr5 <= 100:
                exploaion.update(1, screen)
            elif tmr5 <= 200:
                exploaion.update(2, screen)
            elif tmr5 < 300:
                exploaion.update(3, screen)
            
        pg.display.update()

        tmr += 1
        tmr5 += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
