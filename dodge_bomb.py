import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = { #移動量辞書
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}

def check_bound(rct:pg.Rect)-> tuple[bool,bool]:
    """
    引数：こうかとんrectまたは爆弾rect
    戻り値：横縦の画面外判定結果
    画面内True,画面外False    
    """
    yoko,tate=True,True
    if rct.left<0 or WIDTH< rct.right:
        yoko=False
    if rct.top<0 or HEIGHT<rct.bottom:
        tate=False
    return yoko,tate

def create_bb_assets() -> tuple[list[pg.Surface], list[int]]:
    """
    10段階の爆弾Surfaceと加速度リスト(1〜10)を返す。
    """
    bb_imgs: list[pg.Surface] = []  #大きくなる爆弾を更新するためのリスト
    bb_accs: list[int] = [a for a in range(1, 11)]  #加速度具合

    for r in range(1, 11):
        size = 20 * r #爆弾のサイズ調整
        img = pg.Surface((size, size))  #新たな爆弾を生成
        pg.draw.circle(img, (255, 0, 0), (size / 2, size / 2), size / 2)  #爆弾のサイズと色
        img.set_colorkey((0, 0, 0))  #黒いところを透明化
        bb_imgs.append(img)  #新しい爆弾を追加する

    return bb_imgs, bb_accs

def show_game_over(screen: pg.Surface, kk_rct: pg.Rect):
    """
    ゲームオーバー時の画面演出を行う関数
    ブラックアウト＋泣いているこうかとん＋Game Over文字を表示して5秒停止
    """

    blackout = pg.Surface((WIDTH, HEIGHT))  
    blackout.set_alpha(210)  #半透明の黒で画面を覆う
    pg.draw.rect(blackout, (0, 0, 0), (0, 0, WIDTH, HEIGHT))  # 四角を描画
    screen.blit(blackout, (0, 0))  # 画面に貼り付け

    sad_img = pg.image.load("fig/8.png")  #泣いているこうかとん画像を表示
    sad_img = pg.transform.rotozoom(sad_img, 0, 0.9)

    font = pg.font.SysFont(None, 100)  #Game Overテキストを表示
    text = font.render("Game Over", True, (255, 255, 255))  #色
    text_rct = text.get_rect(center=(WIDTH / 2, HEIGHT /2))  #画面中央に配置
    screen.blit(text, text_rct)
    
    left_rct = sad_img.get_rect(center=(text_rct.left - 50, text_rct.centery))  #ゲームオーバーの左に配置
    right_rct = sad_img.get_rect(center=(text_rct.right + 50, text_rct.centery))  #ゲームオーバーの右に配置
    screen.blit(sad_img, left_rct)
    screen.blit(sad_img, right_rct)

    pg.display.update() #画面切り替え
    time.sleep(5) #５秒間表示

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img=pg.Surface((20,20))  #爆弾の縦横のサイズ
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  #爆弾の色
    bb_rct = bb_img.get_rect()
    bb_rct.centerx =random.randint(0,WIDTH)  #爆弾ランダム座標横
    bb_rct.centery =random.randint(0,HEIGHT)  #爆弾ランダム座標縦
    bb_img.set_colorkey((0,0,0))  #余白部分を透明化
    vx,vy=+5,+5  #爆弾の移動速度
    
    bb_imgs, bb_accs = create_bb_assets()
    bb_img = bb_imgs[0]
        
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
         
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):  # 衝突時
            show_game_over(screen, kk_rct)
            return

        key_lst = pg.key.get_pressed()  #キーを取得
        sum_mv = [0, 0]
        for key, mv in DELTA.items():  # こうかとん移動
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外なら戻す
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        stage = min(tmr // 200, 9)  #tmrから爆弾の拡大加速を決める
        prev_center = bb_rct.center  #爆弾の中心位置を記録

        bb_img = bb_imgs[stage]  #時間に応じた大きさの爆弾画像
        bb_rct = bb_img.get_rect(center=prev_center)  #新しい爆弾をさっきの中心に合わせる

        avx = vx * bb_accs[stage]  #爆弾の速度
        avy = vy * bb_accs[stage]
        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:  #爆弾を反射
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bg_img, (0, 0))
        screen.blit(bb_img, bb_rct)
        screen.blit(kk_img, kk_rct)
        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
