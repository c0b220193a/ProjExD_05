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
        # 城のHP表示に関わる
        self.iro = iro
        self.zahyo = zahyo


    def update(self, screen: pg.Surface):
        """
        城の描画判定
        """
        if self.hp <= 0:
            self.hp = 0
        self.change_HP = self.font.render(f"{self.hp}/5000", 0, self.iro)
        self.rect_HP = self.change_HP.get_rect()
        self.rect_HP.center = self.zahyo, 420
        screen.blit(self.image, self.rect)
        screen.blit(self.change_HP,self.rect_HP)

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

class Inf(pg.sprite.Sprite):
    def __init__(self, name, zahyo: int, size: float):
        """
        猫とキリンの情報の画像を出力
        """
        super().__init__()
        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{name}.png"), 0, size)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = zahyo, 780

    def update(self, screen: pg.Surface):
        """
        ネコとキリンの情報の画像を描画
        """
        screen.blit(self.image, self.rect)

class Shoten(pg.sprite.Sprite):
    """
    友達や敵のHPが0になったときに昇天の画像を作る。
    引数として座標が送られる。
    """
    def __init__(self, zahyo):
        super().__init__()
        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/shoten.png"), 0, 2.5)
        self.image = img  #昇天の画像を作成
        self.rect = self.image.get_rect()  #れくとを生成
        self.rect.center = zahyo
        self.speed = 3.5  #上に上がるスピードを定義

    def update(self, screen:pg.Surface):
        """
        昇天画像を上に上昇させる。
        """
        self.rect.move_ip(0, -self.speed)
        screen.blit(self.image, self.rect)
        if check_bound(self.rect) != (True, True):
            self.kill()
    
class Tomo(pg.sprite.Sprite):
    """
    味方に関するクラス
    """
    def __init__(self, name):
        super().__init__()
        self.tmr = random.randint(1, 100)
        self.zahyo = random.randint(1, 15)

        # ノックバックに関する変数
        self.hp_thresholds = 0  #ノックバックする体力
        self.knockback_distance = 40  #ノックバックする距離
        self.knockback_count = 0  #ノックバックの回数
        self.knockback_limit = 1  #ノックバックの限界
        self.knockhp = 1000

        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{name}.png"), 0, 0.5)
        self.image = img  #猫の画像を読み込む
        self.rect = self.image.get_rect()  #れくとを生成
        self.rect.center = 1400, 627-self.zahyo
        self.speed = 2
        self.state = "normal"  #猫の状態を定義
        self.hp = 90
        self.attack = 20

    def motion(self, enemy, tmr):
        """
        攻撃のモーションを定義
        """
        if tmr%100 == self.tmr:
            enemy.hp -= self.attack
            self.rect.move_ip(8, 0)

    def update(self, screen:pg.Surface):
        """
        猫を自陣から左に移動させる。
        状態を更新する。体力が一定以下になったときにノックバックする。
        """
        if self.hp <= self.hp_thresholds and self.knockback_count == 0:
            self.knockback()
            self.knockback_count += 1

        if self.knockback_count >= self.knockback_limit and self.knockhp >= 900:
            self.knockhp = 0  # ノックバックの限界に達したらknockhpを0にする。

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
        self.knockhp += 1

    def knockback(self):
        """
        キャラクターを後退させる（ノックバックする）。
        """
        self.rect.move_ip(self.knockback_distance, 0)

class LongTomo(pg.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.tmr = random.randint(1, 200)  #300に一回の攻撃のタイミングを決定する。
        self.range = 280  # 攻撃の射程を定義
        self.zahyo = random.randint(1, 15)

        img = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/{name}.png"), 0, 0.2)
        self.image = img  #キリンの画像を読み込む
        self.rect = self.image.get_rect()  #れくとを生成
        self.rect.center = 1400, 580-self.zahyo
        self.speed = 1.8
        self.attack = 80  #キリンの攻撃力を定義
        self.hp = 800  #キリンのhpを定義
        self.state = "normal"  #キリンの状態を定義
        
        # ノックバックに関する変数
        self.hp_thresholds = [0, self.hp/2]  #ノックバックする体力
        self.knockback_distance = 60  #ノックバックする距離
        self.knockback_count = 0  #ノックバックの回数
        self.knockback_limit = 2  #ノックバックの限界
        self.knockhp = 1000
        
        
    def motion(self, enemy, tmr, screen):
        """
        攻撃モーションを起動する処理
        """
        if tmr%200 == self.tmr:
            enemy.hp -= self.attack
        if self.tmr-7 <= tmr%200 <= self.tmr+7:
            self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/giraffe2.png"), 0, 0.2)
            screen.blit(self.image, self.rect)
        else:
            self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/giraffe.png"), 0, 0.2)
            screen.blit(self.image, self.rect)


    def update(self, screen:pg.Surface, tmr):
        """
        猫を自陣から左に移動させる。
        """

        if self.hp <= self.hp_thresholds[1] and self.knockback_count == 0:
            self.knockback()
            self.knockback_count += 1
        if self.hp <= self.hp_thresholds[0] and self.knockback_count == 1:
            self.knockback()
            self.knockback_count += 1

        if self.knockback_count >= self.knockback_limit and self.knockhp >= 900:
            self.knockhp = 0  # ノックバックの限界に達したらknockhpを0にする。

        if self.state == "normal":
            if 0 <= tmr % 100 <= 50:
                self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/giraffe.png"), 0, 0.2)
            if 51 <= tmr % 100 <= 100:
                self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/giraffewalk.png"), 0, 0.2)

            self.rect.move_ip(-self.speed, 0)
            screen.blit(self.image, self.rect)
            if check_bound(self.rect) != (True, True):
                self.kill()
        elif self.state == "atk":
            screen.blit(self.image, self.rect)
        elif self.state == "death":
            screen.blit(self.image, self.rect)
            self.kill()
        self.knockhp += 1

    def knockback(self):
        """
        キャラクターを後退させる（ノックバックする）。
        """
        self.rect.move_ip(self.knockback_distance, 0)

class Cannon(pg.sprite.Sprite): #大砲について
    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"{MAIN_DIR}/fig/beam.png"), 0, 3.0) #ビームの画像を倍率3倍で挿入している
        self.image = pg.transform.flip(self.image, True, False) #ビームを左右反転させる
        self.rect = self.image.get_rect()
        self.rect.center = (1350, 550) #ビームの座標
        self.speed = 10 #ビームのスピード
        self.fired = False #大砲が発射されていない
        
    def update(self, screen):
        """"
        ビームの表示するための処理
        """
        if self.fired: #大砲が発射されたとき
            screen.blit(self.image, self.rect) #ビームの描画
            self.rect.move_ip(-self.speed, 0) #ビームの動き

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
        self.attack_enemy = 25  # 敵の攻撃力
        self.attacktime = 100

    def update(self,screen:pg.Surface):
        """
        敵を右から左へ移動
        """
        if self.state == "normal":  # 通常状態
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":  # 停止状態
            screen.blit(self.image, self.rect) 
            
        else:
            self.state == "normal"

        if self.hp_enemy < 0:
            self.kill()

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
        self.attacktime = 500

    def update(self,screen:pg.Surface):
        """
        ボスを右から左へ移動
        """
        if self.state == "normal":  # 通常状態
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":  # 停止状態
            screen.blit(self.image, self.rect) 
        
            
        else:
            self.state == "normal"

        if self.hp_enemy < 0:
            self.kill()

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
        self.attacktime = 200

    def update(self,screen:pg.Surface):
        """
        敵を右から左へ移動
        """
        if self.state == "normal":  # 通常状態
            self.rect.move_ip(self.xy,0)
            screen.blit(self.image, self.rect)

        elif self.state == "stop":  # 停止状態
            screen.blit(self.image, self.rect) 
            
        else:
            self.state == "normal"

        if self.hp_enemy < 0:
            self.kill()

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
    cats = pg.sprite.Group()
    giraffes = pg.sprite.Group()
    shotens = pg.sprite.Group()

    ###後から修正する部分
    """
    white = (255,255,255)
    ell = pg.Surface((50, 100))
    pg.draw.ellipse(ell,white,[800,450,50,100])
    pg.display.flip()"""
    

    emys = pg.sprite.Group()
    attack_e = pg.sprite.Group()
    boss = pg.sprite.Group()
    dragon = pg.sprite.Group()

    tmr = 0
    tmr5 = 450
    gamemode = 0 # 初期状態
    clock = pg.time.Clock()
    money = Money(0,1500,1)

    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 32) #フォントをhgp創英角ﾎﾟｯﾌﾟ体でサイズを32にして表示
    text = font.render('大砲完了', True, (0, 0, 0)) #文字色(0,0,0)で大砲完了と表示させる

    catinf = Inf("catinf", 600, 0.8)
    giraffeinf = Inf("giraffeinf", 900, 0.8)
    enemy_siro = Siro(0, 200, 0.4,(0,0,0))
    siro = Siro(1, 1400, 0.3,(255,255,255))
    kanban = Kanban(1290)
    bossnum = False
    cannon_fire = False


    while True:
        frame_enemy = random.randint(300, 500)  # 敵出現頻度ランダム
        frame_dragon = random.randint(600, 800)
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
            p = 3800

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1 and money.amount >= 150:
                    cats.add(Tomo("cat"))  #ねこを追加
                    money.amount -= 150
            if event.type == pg.KEYDOWN and money.amount >= 1200:
                if event.key == pg.K_2:
                    money.amount -= 1200
                    giraffes.add(LongTomo("giraffe"))  #キリンを追加
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and tmr >= 1500: #tmrが5以上でスペースキーが押されたとき
                cannon = Cannon()
                cannon.fired = True #大砲を発射する
                cannon_fire = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
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
            

        # 猫に対する捜査の実行
        for cat in cats:
            cat.state = "normal"
            # 猫が敵の城と当たったときの操作
            if len(pg.sprite.spritecollide(enemy_siro, [cat], False)) != 0:  # ねこと敵城がぶつかったときに止まり攻撃
                cat.state = "atk"
                cat.motion(enemy_siro, tmr)
            elif cat.knockhp <= 999:
                cat.state = "atk"
            else:
                cat.state = "normal"
            if 10 <= cat.knockhp <= 100:
                cat.state = "death"
                shotens.add(Shoten(cat.rect.center))
        
        #射程の長いキリンに対する処理
        for giraffe in giraffes:
            if giraffe.rect.center[0] - enemy_siro.rect.center[0] <= giraffe.range:  # 射程内に敵城がある場合
                giraffe.state = "atk"
                giraffe.motion(enemy_siro, tmr, screen)
            elif giraffe.knockhp <= 999:
                giraffe.state = "atk"
            else:
                giraffe.state = "normal"
            if 10 <= giraffe.knockhp <= 100:
                giraffe.state = "death"
                shotens.add(Shoten(giraffe.rect.center))

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

        if tmr >= 1500 and not cannon_fire == True: #tmrが5以上で大砲が発射されていない時
            screen.blit(text, (1340, 700)) #文字を（1340, 700）のところに表示する

        
        # ここから敵のコード
        if tmr%600 == frame_enemy:  # randomフレームに1回敵出現
            emys.add(Enemy())

        for emy in emys:  # 敵が城前で止まり攻撃
            if len(pg.sprite.spritecollide(siro, [emy], False)) != 0:
                emy.state = "stop"
                if tmr%100 == emy.tmr:
                    emy.rect.move_ip(-10,0)  # 攻撃モーション
                    attack_e.add(Attack_effect(emy, 3)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                    siro.hp -= emy.attack_enemy  # 城にダメージ
            else:
                emy.state ="normal"

        if enemy_siro.hp <= 2000 and bossnum is not True:
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
            else:
                dra.state ="normal"

        for enemy in [emys, dragon, boss]:
            for ene in enemy:
                if cannon_fire == True:
                    if len(pg.sprite.spritecollide(cannon, [ene], False)) != 0:
                        ene.hp_enemy -= 7
        
        #  敵の昇天エフェクトを追加
        eneint = 0
        for enemy in [emys, dragon, boss]:
            eneint += 1
            for ene in enemy:
                if ene.hp_enemy <= 0:
                    shotens.add(Shoten(ene.rect.center))
                    ene.kill()
                    money.amount += 50
                #ネコと敵の衝突判定を追加
                for cat in pg.sprite.groupcollide(cats, [ene], False, False).keys():
                    ene.state = "stop"
                    if tmr%ene.attacktime == ene.tmr:
                        if eneint == 1:
                            attack_e.add(Attack_effect(ene, 6)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                        elif eneint == 2:
                            attack_e.add(Attack_effect_dragon(ene, 6)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                        else:
                            attack_e.add(Attack_effect_boss(ene, 6)) # 攻撃エフェクト発生:数字はエフェクトフレーム
                        cat.hp -= ene.attack_enemy  # 敵に攻撃


                    cat.state = "atk"
                    if tmr%100 == cat.tmr:
                        ene.hp_enemy -= cat.attack
                        cat.rect.move_ip(8, 0)
                    if cat.knockhp <= 999:
                        cat.state = "atk"
        for cat in cats:
            if 10 <= cat.knockhp <= 100:
                cat.state = "death"
                shotens.add(Shoten(cat.rect.center))

        


        if cannon_fire == True:
            cannon.update(screen) #大砲を更新する

        giraffeinf.update(screen)
        catinf.update(screen)

        cats.update(screen)
        giraffes.update(screen, tmr)
        shotens.update(screen)
        money.update(screen)      
        kanban.update(screen)
        boss.update(screen)
        dragon.update(screen)
        emys.update(screen)
        attack_e.update()
        attack_e.draw(screen)      


        pg.display.update()

        tmr += 1
        tmr5 += 1
        clock.tick(50)

            
                
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
