import sys
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0]]
from render import *
sys.argv = sys.argv_saved
import os
PW, PH = 1080, 1350
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'posts'); os.makedirs(OUT, exist_ok=True)
YEL = (255, 210, 0)

def bg():
    s = skia.Surface(PW, PH); c = s.getCanvas()
    c.drawRect(skia.Rect(0, 0, PW, PH), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, PH)], [col((15, 35, 72)), col((6, 15, 33))])))
    lp = skia.Paint(AntiAlias=True, Color=col(WHITE, .05), StrokeWidth=3, Style=skia.Paint.kStroke_Style)
    for y in range(100, PH, 140):
        c.drawLine(0, y, PW, y, lp)
        for x in (300, 780): c.drawLine(x, y - 16, x, y + 16, lp)
    c.drawRect(skia.Rect(0, 0, PW, PH), skia.Paint(Shader=skia.GradientShader.MakeRadial((PW / 2, PH * 0.45), 800, [col(LIME, .07), col(LIME, 0)])))
    return s, c

def top(c, page=None, total=None):
    drawimg(c, 'hor', 60 + 160, 90, 320)
    if page:
        f = skia.Font(TF['xb'], 28); s = f'{page}/{total}'; w = f.measureText(s)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(PW - 70 - w - 40, 66, PW - 70, 114), 24, 24), skia.Paint(AntiAlias=True, Color=col(LIME)))
        text(c, s, PW - 70 - 20, 90, 28, NAVY, 'xb', 'r')

def swipe(c, s='Desliza'):
    text(c, s + '  →', PW - 70, PH - 70, 32, LIME, 'xb', 'r')

def chip(c, s, x, y, size, bgc, fg):
    f = skia.Font(TF['black'], size); w = f.measureText(s) + 52; h = size * 1.5
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), h / 2, h / 2), skia.Paint(AntiAlias=True, Color=col(bgc)))
    text(c, s, x, y, size, fg, 'black', 'c')

def save(s, name):
    s.makeImageSnapshot().save(f'{OUT}/{name}.png', skia.kPNG)

def thex(c, ab, x, y, r):
    tm = AB[ab]
    hexdraw(c, x, y, r, fill=tm['p1'], stroke=tm['p2'], lw=max(3, r * 0.08))
    text(c, ab, x, y, r * (0.62 if len(ab) < 3 else 0.5), tm['tc'], 'black', 'c')

# ------------------------------------------------ CARRUSEL DIVISIONES
DIVS = {'AFC': [('ESTE', ['BUF', 'MIA', 'NE', 'NYJ']), ('NORTE', ['BAL', 'CIN', 'CLE', 'PIT']), ('SUR', ['HOU', 'IND', 'JAX', 'TEN']), ('OESTE', ['DEN', 'KC', 'LV', 'LAC'])],
        'NFC': [('ESTE', ['DAL', 'NYG', 'PHI', 'WAS']), ('NORTE', ['CHI', 'DET', 'GB', 'MIN']), ('SUR', ['ATL', 'CAR', 'NO', 'TB']), ('OESTE', ['ARI', 'LAR', 'SF', 'SEA'])]}
def car_div():
    T = 5
    s, c = bg(); top(c, 1, T)
    for k, (t_, clr, sz, y) in enumerate([('¿CÓMO', WHITE, 110, 470), ('FUNCIONAN LAS', WHITE, 90, 580), ('DIVISIONES', LIME, 130, 710), ('DE LA NFL?', WHITE, 110, 840)]):
        text(c, t_, 540, y, sz, clr, 'blacki', 'c')
    text(c, 'Explicado fácil, en 5 slides', 540, 960, 40, MUTED, 'semi', 'c')
    for i, ab in enumerate(['KC', 'DAL', 'GB', 'SF', 'BUF']):
        thex(c, ab, 220 + i * 160, 1110, 58)
    swipe(c); save(s, 'divisiones_1')

    s, c = bg(); top(c, 2, T)
    text(c, '32 EQUIPOS', 540, 260, 100, WHITE, 'blacki', 'c')
    text(c, 'divididos en 2 conferencias de 16', 540, 340, 40, MUTED, 'semi', 'c')
    for ci, (cf, clr) in enumerate((('AFC', LIME), ('NFC', WHITE))):
        bx = 270 + ci * 540
        text(c, cf, bx, 450, 72, clr, 'blacki', 'c')
        text(c, 'Conferencia ' + ('Americana' if ci == 0 else 'Nacional'), bx, 510, 28, MUTED, 'semi', 'c')
        teams = [ab for _, l in DIVS[cf] for ab in l]
        for k, ab in enumerate(teams):
            thex(c, ab, bx - 150 + (k % 4) * 100, 620 + (k // 4) * 115, 44)
    text(c, 'AFC y NFC son como dos “ligas” dentro de la NFL', 540, 1160, 34, WHITE, 'bold', 'c')
    swipe(c); save(s, 'divisiones_2')

    s, c = bg(); top(c, 3, T)
    text(c, '4 DIVISIONES', 540, 230, 96, WHITE, 'blacki', 'c')
    text(c, 'por conferencia · 4 equipos cada una', 540, 305, 36, MUTED, 'semi', 'c')
    for ci, (cf, clr) in enumerate((('AFC', LIME), ('NFC', WHITE))):
        bx = 260 + ci * 560
        text(c, cf, bx, 395, 56, clr, 'blacki', 'c')
        for d, (dn, l) in enumerate(DIVS[cf]):
            y = 520 + d * 175
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(bx - 220, y - 75, bx + 220, y + 75), 24, 24), skia.Paint(AntiAlias=True, Color=col(clr, 0.12)))
            text(c, dn, bx - 200, y - 50, 24, clr, 'black', 'l')
            for k, ab in enumerate(l): thex(c, ab, bx - 150 + k * 100, y + 10, 42)
    text(c, '★ Guárdalo para tenerlo a la mano', 540, 1245, 32, LIME, 'xb', 'c')
    swipe(c); save(s, 'divisiones_3')

    s, c = bg(); top(c, 4, T)
    text(c, '¿QUIÉN VA A', 540, 300, 90, WHITE, 'blacki', 'c')
    text(c, 'PLAYOFFS?', 540, 410, 120, LIME, 'blacki', 'c')
    rows = [('4', 'campeones de división', LIME), ('+3', 'comodines (mejores récords que no ganaron)', WHITE), ('= 7', 'equipos por conferencia', LIME)]
    for i, (n, lab, clr) in enumerate(rows):
        y = 610 + i * 170
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, y - 70, 990, y + 70), 30, 30), skia.Paint(AntiAlias=True, Color=col(NAVY2)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, y - 70, 990, y + 70), 30, 30), skia.Paint(AntiAlias=True, Color=col(clr), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        text(c, n, 210, y, 80, clr, 'blacki', 'c')
        f = skia.Font(TF['bold'], 36)
        text(c, lab, 320, y, 36 if f.measureText(lab) < 640 else 30, WHITE, 'bold', 'l')
    text(c, '14 equipos en total buscan el Super Bowl', 540, 1150, 38, WHITE, 'black', 'c')
    swipe(c); save(s, 'divisiones_4')

    s, c = bg(); top(c, 5, T)
    text(c, '¿EN QUÉ DIVISIÓN', 540, 330, 86, WHITE, 'blacki', 'c')
    text(c, 'ESTÁ TU EQUIPO?', 540, 435, 86, LIME, 'blacki', 'c')
    text(c, 'Dínoslo en los comentarios', 540, 530, 40, WHITE, 'bold', 'c')
    glow(c, 540, 760, 130, LIME, 0.3)
    drawimg(c, 'sym', 540, 770, 230)
    text(c, 'Y si vas a ver el partido,', 540, 980, 40, WHITE, 'bold', 'c')
    text(c, 've con la playera bien puesta 😉'.replace(' 😉', ''), 540, 1035, 40, WHITE, 'bold', 'c')
    chip(c, 'JERSEYS · LINK EN BIO', 540, 1150, 40, LIME, NAVY)
    save(s, 'divisiones_5')

# ------------------------------------------------ CALENDARIO SEMANA 9
WEEK9 = [('JUEVES 5 NOV', [('JAX', 'BAL', '7:15 PM', '')]),
         ('DOMINGO 8 NOV', [('CIN', 'ATL', '8:30 AM', 'MADRID'), ('CLE', 'NO', '12:00 PM', ''), ('DAL', 'IND', '12:00 PM', ''), ('DEN', 'CAR', '12:00 PM', ''),
                            ('DET', 'MIA', '12:00 PM', ''), ('LAR', 'WAS', '12:00 PM', ''), ('NYG', 'PHI', '12:00 PM', ''), ('NYJ', 'KC', '12:00 PM', ''),
                            ('HOU', 'LAC', '3:05 PM', ''), ('ARI', 'SEA', '3:25 PM', ''), ('GB', 'NE', '3:25 PM', ''), ('LV', 'SF', '3:25 PM', ''),
                            ('TB', 'CHI', '7:20 PM', '')]),
         ('LUNES 9 NOV', [('BUF', 'MIN', '7:15 PM', '')])]
def calendario():
    s, c = bg(); top(c)
    text(c, 'SEMANA 9', 540, 200, 96, WHITE, 'blacki', 'c')
    chip(c, 'HORARIOS CDMX', 540, 280, 32, LIME, NAVY)
    CITY = {'JAX':'Jacksonville','BAL':'Baltimore','CIN':'Cincinnati','ATL':'Atlanta','CLE':'Cleveland','NO':'Nueva Orleans','DAL':'Dallas','IND':'Indianápolis',
            'DEN':'Denver','CAR':'Carolina','DET':'Detroit','MIA':'Miami','LAR':'LA Rams','WAS':'Washington','NYG':'NY Giants','PHI':'Filadelfia',
            'NYJ':'NY Jets','KC':'Kansas City','HOU':'Houston','LAC':'LA Chargers','ARI':'Arizona','SEA':'Seattle','GB':'Green Bay','NE':'N. Inglaterra',
            'LV':'Las Vegas','SF':'San Francisco','TB':'Tampa Bay','CHI':'Chicago','BUF':'Buffalo','MIN':'Minnesota'}
    y = 340
    for day, games in WEEK9:
        text(c, day, 90, y, 28, LIME, 'black', 'l'); y += 44
        for a, h, hr, tag in games:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(70, y - 23, 1010, y + 23), 12, 12), skia.Paint(AntiAlias=True, Color=col(NAVY2, 0.85)))
            thex(c, a, 105, y, 19); text(c, CITY[a], 135, y, 25, WHITE, 'black', 'l')
            text(c, '@', 400, y, 25, MUTED, 'black', 'c')
            thex(c, h, 440, y, 19); text(c, CITY[h], 470, y, 25, WHITE, 'black', 'l')
            if tag: chip(c, tag, 790, y, 20, WHITE, NAVY)
            text(c, hr, 990, y, 27, WHITE, 'black', 'r')
            y += 50
        y += 12
    text(c, 'Descansan: Pittsburgh y Tennessee', 540, y + 4, 26, MUTED, 'semi', 'c')
    text(c, '¿Ya tienes tu jersey para el domingo? · Link en bio', 540, PH - 55, 30, LIME, 'xb', 'c')
    save(s, 'calendario_semana9')

# ------------------------------------------------ GUIA DE TALLAS
def tallas():
    T = 3
    s, c = bg(); top(c, 1, T)
    text(c, '¿QUÉ TALLA', 540, 470, 120, WHITE, 'blacki', 'c')
    text(c, 'DE JERSEY', 540, 600, 120, WHITE, 'blacki', 'c')
    text(c, 'ME COMPRO?', 540, 730, 120, LIME, 'blacki', 'c')
    text(c, 'El truco para no fallar en 3 pasos', 540, 860, 40, MUTED, 'semi', 'c')
    swipe(c); save(s, 'tallas_1')

    s, c = bg(); top(c, 2, T)
    text(c, 'MIDE ASÍ', 540, 230, 100, WHITE, 'blacki', 'c')
    steps = [('1', 'Toma una playera que te', 'quede como te gusta'), ('2', 'Extiéndela y mide de', 'axila a axila'),
             ('3', 'Compara esa medida con la', 'tabla de medidas del jersey')]
    for i, (n, l1, l2) in enumerate(steps):
        y = 430 + i * 230
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, y - 90, 990, y + 90), 30, 30), skia.Paint(AntiAlias=True, Color=col(NAVY2)))
        c.drawCircle(190, y, 56, skia.Paint(AntiAlias=True, Color=col(LIME)))
        text(c, n, 190, y, 64, NAVY, 'blacki', 'c')
        text(c, l1, 280, y - 24, 38, WHITE, 'bold', 'l'); text(c, l2, 280, y + 26, 38, LIME, 'black', 'l')
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(90, 1110, 990, 1230), 30, 30), skia.Paint(AntiAlias=True, Color=col(LIME, 0.15)))
    text(c, 'Tip: si te gusta holgado, estilo street, sube una talla', 540, 1170, 32, LIME, 'xb', 'c')
    swipe(c); save(s, 'tallas_2')

    s, c = bg(); top(c, 3, T)
    text(c, '¿TODAVÍA CON', 540, 380, 96, WHITE, 'blacki', 'c')
    text(c, 'DUDAS?', 540, 500, 130, LIME, 'blacki', 'c')
    text(c, 'Mándanos DM con tu medida', 540, 640, 44, WHITE, 'bold', 'c')
    text(c, 'y te decimos qué talla te queda', 540, 700, 44, WHITE, 'bold', 'c')
    glow(c, 540, 900, 120, LIME, 0.3); drawimg(c, 'sym', 540, 910, 200)
    chip(c, 'JERSEYS · LINK EN BIO', 540, 1130, 40, LIME, NAVY)
    text(c, 'Guárdalo para tu próxima compra', 540, 1240, 32, MUTED, 'semi', 'c')
    save(s, 'tallas_3')

car_div(); calendario(); tallas()
print(sorted(os.listdir(OUT)))
