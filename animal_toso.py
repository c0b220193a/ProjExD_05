import math
import os
import random
import sys
import time
from typing import Any
import pygame as pg
from pygame.sprite import AbstractGroup


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

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

class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラス
    """
    imgs = [pg.image.load(f"{MAIN_DIR}/fig/enemy{i}.png") for i in range(1, 6)]
    

    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.tmr =random.randint(1, 100)

        self.rect = self.image.get_rect()
        self.rect.center = 200, 590  # 敵の初期位置
        self.xy = 2  # 敵キャラの横方向の移動速度
        self.state = "normal"  # 状態
        self.hp = 100
        self.attack = 20

    def update(self,screen:pg.Surface):
        """
        敵を右から左へ移動
        """
        if self.state == "normal":  # 
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":
            screen.blit(self.image, self.rect)   
            
        else:
            self.state == "normal"
             


def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    emys = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()

    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        
        if tmr%200 == 0:  # 100フレームに1回敵出現
            emys.add(Enemy())

        for emy in emys:  # 敵が城前で止まり攻撃
            if len(pg.sprite.spritecollide(siro, [emy], False)) != 0:
                emy.state = "stop"
                if tmr%100 == emy.tmr:
                    siro.hp -= emy.attack
                print(siro.hp)
   
        
        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen)
        emys.update(screen)

        pg.display.update()

        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()