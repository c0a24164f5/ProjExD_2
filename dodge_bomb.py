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

def show_game_over(screen: pg.Surface, kk_rct: pg.Rect):
    """
    ゲームオーバー時の画面演出を行う関数
    ブラックアウト＋泣いているこうかとん＋Game Over文字を表示して5秒停止
    """
    
    blackout = pg.Surface((WIDTH, HEIGHT))  
    blackout.set_alpha(210)  #半透明の黒で画面を覆う
    pg.draw.rect(blackout, (0, 0, 0,220), (0, 0, WIDTH, HEIGHT))  # 四角を描画
    screen.blit(blackout, (0, 0))  # 画面に貼り付け

    sad_img = pg.image.load("fig/8.png")  #泣いているこうかとん画像を表示
    sad_img = pg.transform.rotozoom(sad_img, 0, 0.9)

    font = pg.font.SysFont(None, 100)  #Game Overを表示
    text = font.render("Game Over", True, (255, 255, 255))  #色
    text_rct = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  #画面中央に配置
    screen.blit(text, text_rct)
    
    left_rct = sad_img.get_rect(center=(text_rct.left - 50, text_rct.centery))  #左に配置
    right_rct = sad_img.get_rect(center=(text_rct.right + 50, text_rct.centery))  #右に配置
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
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  #衝突時
            show_game_over(screen, kk_rct)
            return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for key, mv in DELTA.items():  #こうかとん移動
            if key_lst[key]:
                sum_mv[0] +=mv[0]
                sum_mv[1] +=mv[1]
                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):  #こうかとんが画面外に行かないように移動量を相殺
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        bb_rct.move_ip(vx,vy)
        yoko,tate=check_bound(bb_rct)  #爆弾が画面端で反射
        if not yoko:
            vx*=-1
        if not tate :
            vy*=-1
            
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
