import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
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
        self.hp = 1000


    def update(self, screen: pg.Surface):
        """
        城の描画判定
        """
        screen.blit(self.image, self.rect)

class Tomo(pg.sprite.Sprite):
    """
    味方に関するクラス
    """
    def __init__(self, name):
        super().__init__()
        self.tmr = random.randint(1, 100)
        self.zahyo = random.randint(1, 15)

        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{name}.png"), 0, 0.5)
        self.image = img  #猫の画像を読み込む
        self.rect = self.image.get_rect()  #れくとを生成
        self.rect.center = 1400, 627-self.zahyo
        self.speed = 2
        self.state = "normal"  #猫の状態を定義
        self.hp = 500
        self.attack = 20
    
    def update(self, screen:pg.Surface):
        """
        猫を自陣から左に移動させる。
        """
        if self.state == "normal":
            self.rect.move_ip(-self.speed, 0)
            screen.blit(self.image, self.rect)
            if check_bound(self.rect) != (True, True):
                self.kill()
        elif self.state == "atk":
            screen.blit(self.image, self.rect)
        elif self.state == "death":
            screen.blit(self.image, self.rect)
            self.kill()

        

def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")
    cats = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()

    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    while True:      
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    cats.add(Tomo("cat"))  #ねこを追加
        
        for cat in cats:
            if len(pg.sprite.spritecollide(enemy_siro, [cat], False)) != 0:  # ねこと敵城がぶつかったときに止まり攻撃
                cat.state = "atk"
                if tmr%100 == cat.tmr:
                    enemy_siro.hp -= cat.attack
                    cat.rect.move_ip(8, 0)
                pg.display.update()
            else:
                cat.state = "normal"

        if enemy_siro.hp <= 0:
            return
            


        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen)
        cats.update(screen)
        pg.display.update()

        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
