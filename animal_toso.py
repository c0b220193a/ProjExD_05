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
        self.hp = 500
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
    

    tmr = 0
    clock = pg.time.Clock()
    money = Money(0,1500,1)


    cannon = Cannon() #キャノンクラスを呼び出す
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 32) #フォントをhgp創英角ﾎﾟｯﾌﾟ体でサイズを32にして表示
    text = font.render('大砲完了', True, (0, 0, 0)) #文字色(0,0,0)で大砲完了と表示させる


    enemy_siro = Siro(0, 200, 0.4)
    siro = Siro(1, 1400, 0.3)

    catinf = Inf("catinf", 600, 0.8)
    giraffeinf = Inf("giraffeinf", 900, 0.8)
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
            p = 3800

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    cats.add(Tomo("cat"))  #ねこを追加
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_2:
                    giraffes.add(LongTomo("giraffe"))  #キリンを追加
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and tmr>=5: #tmrが5以上でスペースキーが押されたとき
                cannon.fired = True #大砲を発射する
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

        if enemy_siro.hp <= 0:
            return

        screen.blit(bg_img, [0, 0])

        if tmr >=5 and not cannon.fired: #tmrが5以上で大砲が発射されていない時
            screen.blit(text, (1340, 700)) #文字を（1340, 700）のところに表示する
            
        cannon.update(screen) #大砲を更新する

        enemy_siro.update(screen)

        siro.update(screen)
        giraffeinf.update(screen)
        catinf.update(screen)

        cats.update(screen)
        giraffes.update(screen, tmr)
        shotens.update(screen)
        money.update(screen)

        pg.display.update()

        tmr += 1
        clock.tick(50)

            
                


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
