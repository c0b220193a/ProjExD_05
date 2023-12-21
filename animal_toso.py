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


class Explosion(pg.sprite.Sprite):
    """
    爆発エフェクトに関するクラス
    """
    def __init__(self, zahyo):
        """
        城が爆発するエフェクトを生成する
        引数1 zahyo:hpが0になった城のX座標
        """
        super().__init__()
        self.bakuhatu1_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/bakuhatu1.png"), 0, 0.6) # 小爆発の画像を0.6倍にして読み込む
        self.bakuhatu2_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/bakuhatu2.png"), 0, 0.8) # 中爆発の画像を0.8倍にして読み込む
        self.bakuhatu3_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/bakuhatu3.png"), 0, 1.0) # 大爆発の画像を1.0倍にして読み込む
        self.rect1 = self.bakuhatu1_img.get_rect()
        self.rect2 = self.bakuhatu2_img.get_rect()
        self.rect3 = self.bakuhatu3_img.get_rect()
        self.rect1.center = zahyo, 550 # xが引数(zahyo),yが550の位置に設定
        self.rect2.center = zahyo, 550 # xが引数(zahyo),yが550の位置に設定
        self.rect3.center = zahyo, 550 # xが引数(zahyo),yが550の位置に設定
    
    def update(self, num, screen):
        """
        爆発エフェクトを表現する
        引数1 num:どの画像を使うか
        引数2 screen:画面Surface
        """
        if num == 1:
            screen.blit(self.bakuhatu1_img, self.rect1) # 小爆発を貼り付け
        elif num == 2:
            screen.blit(self.bakuhatu2_img, self.rect2) # 中爆発を貼り付け
        elif num == 3:
            screen.blit(self.bakuhatu3_img, self.rect3) # 大爆発を貼り付け


class Collapse(pg.sprite.Sprite):
    """
    城崩壊に関するクラス
    """
    def __init__(self, zahyo):
        """
        城が崩壊する画像を生成する
        引数1 zahyo:hpが0になった城の座標
        """
        super().__init__()
        self.siro_houkai1_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/siro_houkai1.png"), 0, 4.75) # 味方の城の画像を4.75倍にして読み込む
        self.siro_houkai2_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/siro_houkai2.png"), 0, 4.2) # 敵の城の画像を4.2倍にして読み込む
        self.rect1 = self.siro_houkai1_img.get_rect()
        self.rect2 = self.siro_houkai2_img.get_rect()
        self.rect1.center = zahyo, 550 # xが引数(zahyo),yが550の位置に設定
        self.rect2.center = zahyo, 550 # xが引数(zahyo),yが550の位置に設定
    
    def update(self, num, screen):
        """
        城が崩壊した画像に切り替える
        引数1 num:どの画像を使うか
        引数2 screen:画面Surface
        """
        if num == 1:
            screen.blit(self.siro_houkai1_img, self.rect1) # 味方の城の崩壊後の画像
        elif num == 2:
            screen.blit(self.siro_houkai2_img, self.rect2) # 敵の城の崩壊後の画像


class Game(pg.sprite.Sprite):
    """
    ゲームクリア・ゲームオーバー判定に関するクラス
    """
    def __init__(self):
        """
        ゲームクリア・ゲームオーバーの画像を生成する
        """
        super().__init__()
        self.gameclear_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/gameclear.png"), 0, 1.0) # gameclearの画像を読み込む
        self.gameover_img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/gameover.png"), 0, 1.5) # gameoverの画像を1.5倍にして読み込む
        self.rect1 = self.gameclear_img.get_rect()
        self.rect2 = self.gameover_img.get_rect()
        self.rect1.center = 800, 250 # xが800,yが250の位置に設定
        self.rect2.center = 800, 250 # xが800,yが250の位置に設定
    
    def update(self, num, screen):
        """
        ゲームクリア・ゲームオーバーを表示する
        引数1 num:どの画像を使うか
        引数2 screen:画面Surface
        """
        if num == 1: # 引数が1の場合
            screen.blit(self.gameclear_img, self.rect1) # gameclearの画像を貼り付ける
        elif num == 2: # 引数が2の場合
            screen.blit(self.gameover_img, self.rect2) # gameoverの画像を貼り付ける



def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    tmr = 0
    tmr5 = 450
    gamemode = 0 # 初期状態
    clock = pg.time.Clock()

    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0                 
        screen.blit(bg_img, [0, 0])

        if gamemode == 0: # 初期状態
            enemy_siro.update(screen)
            siro.update(screen)
        elif gamemode == 1: # 味方の城のhpが0で中爆発が起きた時、味方の城の表示をなくす
            enemy_siro.update(screen)
        elif gamemode == 2: # 敵の城のhpが0で中爆発が起きた時　敵の城の表示をなくす
            siro.update(screen)

        if siro.hp <= 0: # 味方の城のHPが0の時
            explosion = Explosion(1400) # 爆発エフェクトを表示するクラスを呼び出す(引数：表示したい座標)
            collapse = Collapse(1400) # 崩壊した城に変えるクラスを呼び出す(引数：表示したい座標)
            gameover = Game()
            if not tmr5 <= 450: # 一回も爆発エフェクトが発生していない場合
                tmr5 = 0
            elif tmr5 <= 450:
                if tmr5 <= 25:
                    explosion.update(1, screen) # 小爆発
                elif tmr5 <= 50:
                    explosion.update(2, screen) # 中爆発
                elif tmr5 <= 75:
                    explosion.update(3, screen) # 大爆発
                    gamemode =1 
                elif tmr5 <= 200:
                    collapse.update(1,screen) # 崩壊した城の表示
                    gameover.update(2, screen) # gameoverの表示
                elif tmr5 < 210: # ゲームの終了
                    return
                    
        elif enemy_siro.hp <= 0: # 敵の城のHPが0の時
            explosion = Explosion(200) # 爆発エフェクトを表示するクラスを呼び出す(引数：表示したい座標)
            collapse = Collapse(200) # 崩壊した城に変えるクラスを呼び出す(引数：表示したい座標)
            gameclear = Game()
            if not tmr5 <= 450: # 一回も爆発エフェクトが発生していない場合
                tmr5 = 0
            elif tmr5 <= 450:
                if tmr5 <= 25:
                    explosion.update(1, screen) # 小爆発
                elif tmr5 <= 50:
                    explosion.update(2, screen) # 中爆発
                elif tmr5 <= 75:
                    explosion.update(3, screen) # 大爆発
                    gamemode =2
                elif tmr5 <= 200:
                    collapse.update(2,screen) # 崩壊した城の表示
                    gameclear.update(1,screen) # gameclearの表示
                elif tmr5 < 210: # 終了
                    return
                

            
        pg.display.update()

        tmr += 1
        tmr5 += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
