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
        self.vy = random.randint(575, 605)  # 敵出現の縦座標

        self.rect = self.image.get_rect()  # 敵のレクト
        self.rect.center = 200, self.vy  # 敵の初期位置
        self.xy = 1  # 敵キャラの横方向の移動速度
        self.state = "normal"  # 状態
        self.hp_enemy = 100
        self.attack_enemy = 20

    def update(self,screen:pg.Surface):
        """
        敵を右から左へ移動
        """
        if self.state == "normal":  # 
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":
            screen.blit(self.image, self.rect) 
            

        elif self.hp_enemy < 0:
            self.kill()
            
        else:
            self.state == "normal"

class Attack_effect(pg.sprite.Sprite):
    """
    攻撃エフェクトに関するクラス
    """
    def __init__(self, obj: "Siro", life: int):
        """
        攻撃するエフェクトを生成する
        引数1 obj：攻撃するSiroまたは
        引数2 life：発生時間
        """
        super().__init__()
        self.image = pg.image.load(f"{MAIN_DIR}/fig/attack_effect.png")
        self.rect = self.image.get_rect(center=(obj.rect.centerx+70, obj.rect.centery))
        self.life = life

    def update(self):
        """
        攻撃時間を1減算した攻撃経過時間_lifeに応じて
        爆発エフェクトを表現する
        """
        self.life -= 1
        if self.life < 0:
            self.kill()
             


def main():
    pg.display.set_caption("アニマル闘争")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/fig/haikei.jpg")

    emys = pg.sprite.Group()
    attack_e = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()

    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    while True:
        frame_enemy = random.randint(300, 500)
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        
        if tmr%frame_enemy == 0:  # randomフレームに1回敵出現
            emys.add(Enemy())

        for emy in emys:  # 敵が城前で止まり攻撃
            if len(pg.sprite.spritecollide(siro, [emy], False)) != 0:
                emy.state = "stop"
                if tmr%100 == emy.tmr:
                    emy.rect.move_ip(-10,0)  # 攻撃モーション
                    attack_e.add(Attack_effect(emy, 3)) # 攻撃エフェクト発生
                    siro.hp -= emy.attack_enemy  # 城にダメージ
                    print(siro.hp)
            else:
                emy.state ="normal"
   
        
        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen)
        emys.update(screen)
        attack_e.update()
        attack_e.draw(screen)

        pg.display.update()

        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()