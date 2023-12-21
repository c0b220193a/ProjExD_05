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


class Cannon(pg.sprite.Sprite): #大砲について
    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/beam.png"), 0, 3.0) #ビームの画像を倍率3倍で挿入している
        self.image = pg.transform.flip(self.image, True, False) #ビームを左右反転させている
        self.rect = self.image.get_rect()
        self.rect.center = (1350, 550) #ビームの座標
        self.speed = 10 #ビームのスピード
        self.fired = False
        
    def update(self, screen):
        """"
        ビームの表示
        """
        if self.fired: #大砲が発射されたとき
            screen.blit(self.image, self.rect) #ビームの描画
            self.rect.move_ip(-self.speed, 0) #ビームの動き


def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    tmr = 0
    clock = pg.time.Clock()

    cannon = Cannon()
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 32) #フォントのサイズを32にする
    text = font.render('大砲完了', True, (0, 0, 0)) #大砲完了と表示させる


    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    while True:  
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0         
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and tmr>=5: #タイマーが5以上でスペースキーが押されたとき
                cannon.fired = True #大砲を発射する
                
        
        screen.blit(bg_img, [0, 0])

        if tmr >=5 and not cannon.fired: #タイマーが5以上で大砲が発射されていない時
            screen.blit(text, (1340, 700)) #文字を（1340, 700）のところに表示する
            
        cannon.update(screen) #大砲を更新する

        enemy_siro.update(screen)
        siro.update(screen)
        pg.display.update()

        tmr += 1
        clock.tick(50)

            
                



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
