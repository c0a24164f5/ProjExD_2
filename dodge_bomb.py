import os
import sys
import random
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


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img=pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx =random.randint(0,WIDTH)
    bb_rct.centery =random.randint(0,HEIGHT)
    bb_img.set_colorkey((0,0,0))
    vx,vy=+50,+55
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            print("お前の負け")
            return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] +=mv[0]
                sum_mv[1] +=mv[1]
                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        bb_rct.move_ip(vx,vy)
        yoko,tate=check_bound(bb_rct)
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
