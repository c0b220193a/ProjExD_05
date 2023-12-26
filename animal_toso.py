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
        self.speed = random.randint(1, 2)  # 敵のスピード変数

        self.rect = self.image.get_rect()  # 敵のレクト
        self.rect.center = 200, self.vy  # 敵の初期位置
        self.xy = self.speed  # 敵キャラの移動速度
        self.state = "normal"  # 状態
        self.hp_enemy = 100  # 敵のHP
        self.attack_enemy = 20  # 敵の攻撃力

    def update(self,screen:pg.Surface):
        """
        敵を右から左へ移動
        """
        if self.state == "normal":  # 通常状態
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":  # 停止状態
            screen.blit(self.image, self.rect) 
            
        elif self.hp_enemy < 0:
            self.kill()
            
        else:
            self.state == "normal"

class Attack_effect(pg.sprite.Sprite):
    """
    モブキャラ攻撃エフェクトに関するクラス
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
        攻撃エフェクトを表現する
        """
        self.life -= 1
        if self.life < 0:
            self.kill()

class Boss(pg.sprite.Sprite):
    """
    ボスに関するクラス
    """

    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/boss.png"), 0, 6.0)
        

        self.tmr =random.randint(1, 100)

        self.rect = self.image.get_rect()  # ボスのレクト
        self.rect.center = 200, 460  # ボスの初期位置
        self.xy = 1 # ボスの移動速度
        self.state = "normal"  # 状態
        self.hp_enemy = 1000  # ボスのHP
        self.attack_enemy = 200  # ボスの攻撃力

    def update(self,screen:pg.Surface):
        """
        ボスを右から左へ移動
        """
        if self.state == "normal":  # 通常状態
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":  # 停止状態
            screen.blit(self.image, self.rect) 
            
        elif self.hp_enemy < 0:
            self.kill()
            
        else:
            self.state == "normal"


class Attack_effect_boss(pg.sprite.Sprite):
    """
    ボス攻撃エフェクトに関するクラス
    """
    def __init__(self, obj: "Siro", life: int):
        """
        攻撃するエフェクトを生成する
        引数1 obj：攻撃するSiroまたは
        引数2 life：発生時間
        """
        super().__init__()
        self.image = pg.image.load(f"{MAIN_DIR}/fig/attack_effect2.png")
        self.rect = self.image.get_rect(center=(obj.rect.centerx+250, obj.rect.centery))

        self.life = life

    def update(self):
        """
        攻撃時間を1減算した攻撃経過時間_lifeに応じて
        攻撃エフェクトを表現する
        """
        self.life -= 1
        if self.life < 0:
            self.kill()


class Kanban(pg.sprite.Sprite):
    def __init__(self, x:int):
        """
        看板を置く
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/kanban.png"), 0, 1)
        self.img = pg.transform.flip(img0, True, False)  # デフォルトの看板
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.center = x, 620

    def update(self, screen: pg.Surface):
        """
        看板の描画判定
        """
        screen.blit(self.image, self.rect)


class Dragon(pg.sprite.Sprite):
    """
    ドラゴンに関するクラス
    """
    imgs = [pg.image.load(f"{MAIN_DIR}/fig/dragon{i}.png") for i in range(1, 3)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.tmr =random.randint(1, 100)
        self.vy = random.randint(575, 605)  # 敵出現の縦座標

        self.rect = self.image.get_rect()  # 敵のレクト
        self.rect.center = 200, self.vy  # 敵の初期位置
        self.xy = 1  # 敵キャラの移動速度
        self.state = "normal"  # 状態
        self.hp_enemy = 300  # 敵のHP
        self.attack_enemy = 40  # 敵の攻撃力

    def update(self,screen:pg.Surface):
        """
        敵を右から左へ移動
        """
        if self.state == "normal":  # 通常状態
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":  # 停止状態
            screen.blit(self.image, self.rect) 
            
        elif self.hp_enemy < 0:
            self.kill()
            
        else:
            self.state == "normal"


class Attack_effect_dragon(pg.sprite.Sprite):
    """
    ドラゴン攻撃に関するクラス
    """
    def __init__(self, obj: "Siro", life: int):
        """
        攻撃するエフェクトを生成する
        引数1 obj：攻撃するSiroまたは
        引数2 life：発生時間
        """
        super().__init__()
        self.image = pg.image.load(f"{MAIN_DIR}/fig/attack_effect_dragon1.png")
        self.rect = self.image.get_rect(center=(obj.rect.centerx+150, obj.rect.centery))
        self.life = life

    def update(self):
        """
        攻撃時間を1減算した攻撃経過時間_lifeに応じて
        攻撃エフェクトを表現する
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
    boss = pg.sprite.Group()
    dragon = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()

    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)
    kanban = Kanban(1290)
    bossnum = False

    while True:
        frame_enemy = random.randint(300, 500)  # 敵出現頻度ランダム
        frame_dragon = random.randint(600, 800)
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        
        if tmr%600 == frame_enemy:  # randomフレームに1回敵出現
            emys.add(Enemy())

        for emy in emys:  # 敵が城前で止まり攻撃
            if len(pg.sprite.spritecollide(siro, [emy], False)) != 0:
                emy.state = "stop"
                if tmr%100 == emy.tmr:
                    emy.rect.move_ip(-10,0)  # 攻撃モーション
                    attack_e.add(Attack_effect(emy, 3)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                    siro.hp -= emy.attack_enemy  # 城にダメージ
                    print(siro.hp)
            else:
                emy.state ="normal"

        if siro.hp <= 2000 and bossnum is not True:
            boss.add(Boss())
            bossnum = True

        for bos in boss:  # bossが城前で止まり攻撃
            if len(pg.sprite.spritecollide(siro, [bos], False)) != 0:
                bos.state = "stop"
                if tmr%500 == 0:
                    bos.rect.move_ip(-15,0)  # 攻撃モーション
                    attack_e.add(Attack_effect_boss(bos, 7)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                    siro.hp -= emy.attack_enemy  # 城にダメージ
            else:
                bos.state = "normal"

        if tmr%1200 == frame_dragon:
            dragon.add(Dragon())

        for dra in dragon:  # ドラゴンが城前で止まり攻撃
            if len(pg.sprite.spritecollide(siro, [dra], False)) != 0:
                dra.state = "stop"
                if tmr%200 == dra.tmr:
                    dra.rect.move_ip(-10,0)  # 攻撃モーション
                    attack_e.add(Attack_effect_dragon(dra, 6)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                    siro.hp -= dra.attack_enemy  # 城にダメージ
                    print(siro.hp)
            else:
                dra.state ="normal"


        screen.blit(bg_img, [0, 0])

        enemy_siro.update(screen)
        siro.update(screen)
        kanban.update(screen)
        boss.update(screen)
        dragon.update(screen)
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