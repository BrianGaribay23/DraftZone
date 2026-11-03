import sys, os, math, random, subprocess, json
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0]]
from render import *          # shared helpers, colors, BG, header, teams...
sys.argv = sys.argv_saved

YEL = (255, 210, 0)
BLUE = (80, 150, 255)

def chip(c, s, x, y, size, bg, fg, a=1, scale=1, pad=26):
    if a <= 0: return
    f = skia.Font(TF['black'], size); w = f.measureText(s) + pad * 2; h = size * 1.5
    c.save(); c.translate(x, y); c.scale(scale, scale)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w/2, -h/2, w/2, h/2), h/2, h/2), skia.Paint(AntiAlias=True, Color=col(bg, a)))
    c.restore()
    text(c, s, x, y, size, fg, 'black', 'c', a, scale=scale)

def pop(t, a, b): return 0.8 + 0.2 * eback(seg(t, a, b))

def outro(c, t, t0, line='Síguenos para más NFL en español'):
    o = seg(t, t0, t0 + 0.6)
    if o > 0:
        glow(c, 540, 800, 170, LIME, 0.25 * o)
        drawimg(c, 'ver', 540, 920, 820 * (0.7 + 0.3 * eback(o)), o)
        text(c, line, 540, 1360, 42, WHITE, 'bold', 'c', seg(t, t0 + 0.7, t0 + 1.2))

# ---------------------------------------------------------------- flags
def flag(c, x, y, s=1.0, rot=0, a=1):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(-34, -26); p.cubicTo(-10, -34, 10, -18, 34, -26); p.lineTo(30, 24); p.cubicTo(8, 30, -12, 16, -30, 26); p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=col(YEL, a)))
    c.drawCircle(0, 30, 8, skia.Paint(AntiAlias=True, Color=col((230, 230, 230), a)))
    c.restore()

def falling_flag(c, t, t0, x0, y0, x1, y1, s=1.0, a=1):
    """flag thrown at t0 lands at (x1,y1) after 0.6s; returns landed alpha"""
    if t < t0: return
    p = seg(t, t0, t0 + 0.6); e = eo(p)
    x = lerp(x0, x1, e); y = lerp(y0, y1, e) - 160 * math.sin(math.pi * p)
    flag(c, x, y, s, rot=(1 - p) * 540, a=a)

# ---------------------------------------------------------------- field (top-down, offense goes right)
FX0, FX1, FY0, FY1 = 40, 1040, 760, 1250
PPY = 30.0          # pixels per yard
LOSX = 400          # screen x of line of scrimmage (camera follows)
def field(c, view_los, a=1, fd=10, show_fd=True):
    """view_los: absolute yard of the LOS (camera keeps LOS at LOSX)."""
    if a <= 0: return
    c.save(); c.clipRect(skia.Rect(FX0, FY0, FX1, FY1))
    c.drawRect(skia.Rect(FX0, FY0, FX1, FY1), skia.Paint(Color=col((16, 52, 40), a)))
    stripe = skia.Paint(Color=col((20, 62, 48), a))
    y0 = math.floor((view_los - (LOSX - FX0) / PPY) / 5) * 5
    yd = y0
    while True:
        x = LOSX + (yd - view_los) * PPY
        if x > FX1: break
        if (yd // 5) % 2 == 0: c.drawRect(skia.Rect(x, FY0, x + 5 * PPY, FY1), stripe)
        lw = 4 if yd % 10 == 0 else 2
        c.drawLine(x, FY0, x, FY1, skia.Paint(AntiAlias=True, Color=col(WHITE, 0.55 * a), StrokeWidth=lw))
        for k in range(1, 5):
            xh = x + k * PPY
            for yy in (FY0 + 40, FY1 - 40):
                c.drawLine(xh, yy - 8, xh, yy + 8, skia.Paint(AntiAlias=True, Color=col(WHITE, 0.35 * a), StrokeWidth=2))
        if yd % 10 == 0:
            n = yd if yd <= 50 else 100 - yd
            text(c, str(n), x, FY1 - 80, 34, WHITE, 'black', 'c', 0.35 * a)
        yd += 5
    c.drawLine(LOSX, FY0, LOSX, FY1, skia.Paint(AntiAlias=True, Color=col(BLUE, 0.9 * a), StrokeWidth=6))
    if show_fd:
        xf = LOSX + fd * PPY
        c.drawLine(xf, FY0, xf, FY1, skia.Paint(AntiAlias=True, Color=col(LIME, 0.9 * a), StrokeWidth=6))
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(FX0, FY0, FX1, FY1), 18, 18), skia.Paint(AntiAlias=True, Color=col(WHITE, 0.25 * a), Style=skia.Paint.kStroke_Style, StrokeWidth=3))

def player(c, x, y, off=True, a=1, lab=None, hl=0):
    if a <= 0: return
    if hl > 0: c.drawCircle(x, y, 34, skia.Paint(AntiAlias=True, Color=col(YEL, 0.35 * hl * a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)))
    if off:
        c.drawCircle(x, y, 20, skia.Paint(AntiAlias=True, Color=col(LIME, a)))
    else:
        c.drawCircle(x, y, 20, skia.Paint(AntiAlias=True, Color=col(NAVY, a)))
        c.drawCircle(x, y, 20, skia.Paint(AntiAlias=True, Color=col(WHITE, a), Style=skia.Paint.kStroke_Style, StrokeWidth=5))
    if lab: text(c, lab, x, y, 18, NAVY if off else WHITE, 'black', 'c', a)

def ball(c, x, y, a=1, rot=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawOval(skia.Rect(-14, -9, 14, 9), skia.Paint(AntiAlias=True, Color=col((150, 85, 40), a)))
    c.drawLine(-5, 0, 5, 0, skia.Paint(AntiAlias=True, Color=col(WHITE, a), StrokeWidth=2))
    c.restore()

YROWS = [905, 955, 1005, 1055, 1105]
def X(dy): return LOSX + dy * PPY      # dy yards relative to LOS
BASE_O = {'OL0': (-1, 905), 'OL1': (-1, 955), 'OL2': (-1, 1005), 'OL3': (-1, 1055), 'OL4': (-1, 1105),
          'QB': (-4.5, 1005), 'WR1': (-1, 815), 'WR2': (-1, 1195)}
BASE_D = {'DL0': (1, 930), 'DL1': (1, 980), 'DL2': (1, 1030), 'DL3': (1, 1080),
          'LB0': (5, 955), 'LB1': (5, 1055), 'CB1': (2.5, 815), 'CB2': (2.5, 1195)}

def draw_formation(c, pos, a=1, hl=()):
    for k, (dy, y) in pos.items():
        off = k in BASE_O
        player(c, X(dy), y, off, a, lab='QB' if k == 'QB' else None, hl=1 if k in hl else 0)

def foul_title(c, t, n, name, eng, a=1):
    p = seg(t, 0.0, 0.4)
    chip(c, f'{n}/5', 540, 395, 32, LIME, NAVY, p * a, scale=pop(t, 0, 0.4))
    f = skia.Font(TF['blacki'], 76); w = f.measureText(name); sz = 76 * min(1, 960 / w)
    text(c, name, 540, 480, sz, WHITE, 'blacki', 'c', p * a, scale=pop(t, 0.05, 0.45))
    text(c, eng, 540, 545, 32, MUTED, 'semi', 'c', seg(t, 0.2, 0.6) * a)

def pen_chip(c, t, t0, s, sub=None, clr=YEL):
    q = seg(t, t0, t0 + 0.35)
    chip(c, s, 540, 650, 44, clr, NAVY, q, scale=pop(t, t0, t0 + 0.35))
    if sub: text(c, sub, 540, 1330, 38, WHITE, 'bold', 'c', seg(t, t0 + 0.3, t0 + 0.7))

def lerp_pos(a, b, e): return (lerp(a[0], b[0], e), lerp(a[1], b[1], e))

# ================================================================ VIDEO 1: FALTAS
def fa_hook(c, t, D):
    header(c)
    rnd = random.Random(5)
    for i in range(12):
        x = rnd.choice([rnd.uniform(60, 300), rnd.uniform(780, 1020)]); sp = rnd.uniform(500, 900); t0 = rnd.uniform(0, 1.5); rot = rnd.uniform(0, 360)
        dt = t - t0
        if dt < 0: continue
        y = -60 + sp * dt
        if y > 2000: continue
        flag(c, x, y, 1.0, rot + dt * 200, 0.75 * (1 - seg(t, D - 0.3, D)))
    out = 1 - seg(t, D - 0.25, D)
    for k, (s, clr, sz, y) in enumerate([('¿POR QUÉ TIRAN', WHITE, 92, 820), ('PAÑUELOS', YEL, 128, 945), ('AMARILLOS?', YEL, 128, 1070)]):
        p = seg(t, 0.15 + k * 0.2, 0.55 + k * 0.2)
        text(c, s, 540, y, sz, clr, 'blacki', 'c', min(1, p * 2) * out, scale=0.6 + 0.4 * eback(p))
    text(c, 'Las 5 faltas más comunes de la NFL', 540, 1210, 40, WHITE, 'bold', 'c', seg(t, 1.2, 1.6) * out)

def fa_intro(c, t, D):
    header(c)
    falling_flag(c, t, 0.2, 900, 300, 540, 820, 3.0)
    q = seg(t, 0.8, 1.1)
    text(c, '¡FALTA!', 540, 1050, 120, YEL, 'blacki', 'c', q, scale=pop(t, 0.8, 1.1))
    text(c, 'Rompes una regla = te castigan con yardas', 540, 1190, 38, WHITE, 'bold', 'c', seg(t, 1.6, 2.0))
    # yard arrow
    a = seg(t, 2.4, 2.8)
    if a > 0:
        x0, x1 = 300, 300 + 480 * eo(seg(t, 2.4, 3.4)); y = 1330
        c.drawLine(x0, y, x1, y, skia.Paint(AntiAlias=True, Color=col(LIME, a), StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap))
        text(c, '5 · 10 · 15 yardas', 540, 1410, 36, LIME, 'xb', 'c', seg(t, 3.0, 3.4))
    # transition: field fades in at end
    field(c, 30, seg(t, D - 0.6, D) * 0.0)

def foul_scene_factory(n, name, eng, kind):
    def sc(c, t, D):
        header(c)
        foul_title(c, t, n, name, eng)
        fa = seg(t, 0.0, 0.3) * (1 - seg(t, D - 0.3, D))
        los0 = 30.0
        # penalty movement
        if kind == 'false_start':   mv, tf, tp = -5, 1.8, 2.9
        elif kind == 'offside':     mv, tf, tp = 5, 1.8, 2.9
        elif kind == 'holding':     mv, tf, tp = -10, 2.3, 3.3
        elif kind == 'dpi':         mv, tf, tp = 12, 2.5, 3.5
        else:                       mv, tf, tp = 15, 2.6, 3.6
        m = eio(seg(t, tp, tp + 1.0))
        los = los0 + mv * m
        fd_rel = 10 if kind in ('dpi', 'roughing') else 10 - mv * m * 0 + (0 if kind != 'holding' else 0)
        if kind in ('false_start', 'offside', 'holding'):
            fd_rel = 10 - mv * m       # first-down marker stays at its absolute spot
        field(c, los, fa, fd=fd_rel)
        # players: positions relative to original LOS, drawn in camera coords
        shift = -(mv * m) * PPY   # world moves opposite to camera
        po = {k: v for k, v in BASE_O.items()}; pd = {k: v for k, v in BASE_D.items()}
        hl = ()
        bx, by, ba = X(-0.5), 1005, 0
        if kind == 'false_start':
            e = eo(seg(t, 0.8, 1.1)); po['OL2'] = (-1 + 0.8 * e, 1005); hl = ('OL2',) if t > 0.8 else ()
        elif kind == 'offside':
            e = eo(seg(t, 0.8, 1.1)); pd['DL1'] = (1 - 2.0 * e, 980); hl = ('DL1',) if t > 0.8 else ()
        elif kind == 'holding':
            s_ = eo(seg(t, 0.8, 1.8))
            po['QB'] = (-4.5 - 2.5 * s_, 1005)
            for k in ('DL0', 'DL2', 'DL3'): pd[k] = (1 - 1.2 * s_, pd[k][1])
            pd['DL1'] = (1 - 0.5 * s_, 980); po['OL1'] = (-1 + 0.9 * s_, 965)
            hl = ('OL1',) if t > 1.4 else ()
        elif kind == 'dpi':
            r = eo(seg(t, 0.8, 2.3))
            po['WR1'] = (-1 + 13 * r, 815 + 60 * r); pd['CB1'] = (2.5 + 10 * r, 820 + 70 * r)
            po['QB'] = (-4.5 - 2 * eo(seg(t, 0.8, 1.4)), 1005)
            hl = ('CB1',) if t > 2.0 else ()
        else:
            s_ = eo(seg(t, 0.8, 1.6)); po['QB'] = (-4.5 - 2.5 * s_, 1005)
            r = eo(seg(t, 0.8, 2.6)); po['WR1'] = (-1 + 11 * r, 815 + 40 * r)
            h = eo(seg(t, 1.4, 2.3)); pd['DL1'] = (1 - 9.0 * h, 980 + 25 * h)
            hl = ('DL1',) if t > 2.2 else ()
        # draw players shifted by world offset
        c.save(); c.clipRect(skia.Rect(FX0, FY0, FX1, FY1)); c.translate(shift, 0)
        pa = fa * (1 - seg(t, tp, tp + 0.5))
        draw_formation(c, {**po, **pd}, pa, hl)
        # holding: grab line
        if kind == 'holding' and t > 1.3:
            g = seg(t, 1.3, 1.6)
            a_ = (X(po['OL1'][0]), po['OL1'][1]); b_ = (X(pd['DL1'][0]), pd['DL1'][1])
            c.drawLine(a_[0], a_[1], b_[0], b_[1], skia.Paint(AntiAlias=True, Color=col(YEL, g * pa), StrokeWidth=8, StrokeCap=skia.Paint.kRound_Cap))
        # ball
        if kind == 'dpi':
            p = seg(t, 1.6, 2.5)
            if 0 < p < 1:
                sx, sy = X(-6.5), 1005; ex, ey = X(13), 900
                ball(c, lerp(sx, ex, p), lerp(sy, ey, p) - 140 * math.sin(math.pi * p), pa, rot=p * 360)
            if t > 2.0:
                bump = seg(t, 2.0, 2.3)
                cx = (X(po['WR1'][0]) + X(pd['CB1'][0])) / 2; cy = (po['WR1'][1] + pd['CB1'][1]) / 2
                c.drawCircle(cx, cy, 30 + 40 * bump, skia.Paint(AntiAlias=True, Color=col(YEL, (1 - bump) * pa), Style=skia.Paint.kStroke_Style, StrokeWidth=5))
        if kind == 'roughing':
            p = seg(t, 1.5, 2.6)
            if 0 < p < 1:
                sx, sy = X(-7), 1005; ex, ey = X(10), 855
                ball(c, lerp(sx, ex, p), lerp(sy, ey, p) - 120 * math.sin(math.pi * p), pa, rot=p * 360)
            if t > 2.25:
                hit = seg(t, 2.25, 2.6); qx, qy = X(po['QB'][0]), po['QB'][1]
                c.drawCircle(qx, qy, 30 + 50 * hit, skia.Paint(AntiAlias=True, Color=col((255, 80, 80), (1 - hit) * pa), Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        c.restore()
        # fresh formation at the new spot
        na = fa * seg(t, tp + 1.0, tp + 1.5)
        if na > 0:
            c.save(); c.clipRect(skia.Rect(FX0, FY0, FX1, FY1)); draw_formation(c, {**BASE_O, **BASE_D}, na); c.restore()
        # flag thrown toward foul spot (world coords -> screen)
        spot = {'false_start': (X(-0.2), 1005), 'offside': (X(0.0), 980), 'holding': (X(-0.2), 975),
                'dpi': (X(12.5), 860), 'roughing': (X(-6.5), 1000)}[kind]
        if t >= tf:
            fx, fy = spot[0] + shift, spot[1]
            falling_flag(c, t, tf, 1000, 700, fx, fy, 1.0, a=fa)
        # penalty chips / captions
        if kind == 'false_start':
            text(c, 'La ofensiva se mueve antes de tiempo', 540, 1330, 38, WHITE, 'bold', 'c', seg(t, 0.9, 1.3) * (1 - seg(t, tp, tp + 0.3)))
            pen_chip(c, t, tp, '−5 YARDAS', 'Castigo para la ofensiva')
        elif kind == 'offside':
            text(c, 'Un defensivo cruza la línea antes', 540, 1330, 38, WHITE, 'bold', 'c', seg(t, 0.9, 1.3) * (1 - seg(t, tp, tp + 0.3)))
            pen_chip(c, t, tp, '+5 YARDAS', 'para la ofensiva')
        elif kind == 'holding':
            text(c, 'Agarrar al rival para frenarlo', 540, 1330, 38, WHITE, 'bold', 'c', seg(t, 1.3, 1.7) * (1 - seg(t, tp, tp + 0.3)))
            pen_chip(c, t, tp, '−10 YARDAS', 'Si lo hace la ofensiva')
            q = seg(t, tp + 1.6, tp + 2.0)
            text(c, 'Si lo hace la defensa: 5 yardas + 1ª y 10', 540, 1400, 34, LIME, 'xb', 'c', q)
        elif kind == 'dpi':
            text(c, 'Estorbar al receptor antes del balón', 540, 1330, 38, WHITE, 'bold', 'c', seg(t, 1.9, 2.3) * (1 - seg(t, tp, tp + 0.3)))
            pen_chip(c, t, tp, 'BALÓN EN EL LUGAR DE LA FALTA', '+ primero y diez automático')
        else:
            text(c, 'Golpear al QB después de lanzar', 540, 1330, 38, WHITE, 'bold', 'c', seg(t, 2.3, 2.7) * (1 - seg(t, tp, tp + 0.3)))
            pen_chip(c, t, tp, '+15 YARDAS', '+ primero y diez automático')
    return sc

FOULS = [(1, 'SALIDA EN FALSO', 'False start', 'false_start'), (2, 'FUERA DE LUGAR', 'Offside', 'offside'),
         (3, 'HOLDING', 'Sujetar al rival', 'holding'), (4, 'INTERFERENCIA DE PASE', 'Pass interference', 'dpi'),
         (5, 'RUDEZA AL QUARTERBACK', 'Roughing the passer', 'roughing')]

def fa_outro(c, t, D):
    header(c, 1 - seg(t, 3.0, 3.3))
    a1 = 1 - seg(t, 3.0, 3.3)
    p = seg(t, 0, 0.4)
    text(c, '¿CUÁL TE', 540, 470, 90, WHITE, 'blacki', 'c', p * a1, scale=pop(t, 0, 0.4))
    text(c, 'DESESPERA MÁS?', 540, 570, 90, YEL, 'blacki', 'c', p * a1, scale=pop(t, 0.1, 0.5))
    for i, (n, name, eng, k) in enumerate(FOULS):
        q = seg(t, 0.5 + i * 0.15, 0.8 + i * 0.15) * a1
        y = 720 + i * 115
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(150 + 40 * (1 - eo(q)), y - 45, 930, y + 45), 24, 24), skia.Paint(AntiAlias=True, Color=col(NAVY2, q)))
        flag(c, 215 + 40 * (1 - eo(q)), y, 0.7, -15, q)
        text(c, name, 280 + 40 * (1 - eo(q)), y, 40, WHITE, 'black', 'l', q)
    text(c, 'Comenta 👇'.replace(' 👇', ''), 540, 1330, 44, LIME, 'black', 'c', seg(t, 1.5, 1.9) * a1)
    outro(c, t, 3.3)

FALTAS = [(fa_hook, 3.6), (fa_intro, 5.0)] + [(foul_scene_factory(*f), d) for f, d in zip(FOULS, [6.0, 6.0, 7.6, 7.0, 7.0])] + [(fa_outro, 6.5)]

# ================================================================ VIDEO 2: DRAFT
def dr_hook(c, t, D):
    header(c)
    out = 1 - seg(t, D - 0.25, D)
    for k, (s, clr, sz, y) in enumerate([('¿CÓMO ELIGEN', WHITE, 96, 800), ('A SUS NUEVOS', WHITE, 96, 910), ('JUGADORES?', LIME, 128, 1035)]):
        p = seg(t, 0.15 + k * 0.2, 0.55 + k * 0.2)
        text(c, s, 540, y, sz, clr, 'blacki', 'c', min(1, p * 2) * out, scale=0.6 + 0.4 * eback(p))
    q = seg(t, 1.3, 1.7)
    chip(c, 'EL DRAFT', 540, 1200, 54, LIME, NAVY, q * out, scale=pop(t, 1.3, 1.7))

def card(c, x, y, w, h, a, fill=NAVY2, stroke=LIME):
    if a <= 0: return
    r = skia.RRect.MakeRectXY(skia.Rect(x - w/2, y - h/2, x + w/2, y + h/2), 22, 22)
    c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(fill, a)))
    c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(stroke, a), Style=skia.Paint.kStroke_Style, StrokeWidth=4))

def dr_what(c, t, D):
    header(c)
    p = seg(t, 0.1, 0.5)
    text(c, '¿QUÉ ES EL DRAFT?', 540, 440, 80, WHITE, 'blacki', 'c', p, scale=pop(t, 0.1, 0.5))
    # college -> NFL arrow
    q = seg(t, 0.6, 1.0)
    card(c, 270, 820, 340, 260, q, stroke=WHITE)
    text(c, 'UNIVERSIDAD', 270, 780, 40, WHITE, 'black', 'c', q)
    for i in range(3):
        player(c, 200 + i * 70, 870, True, q * seg(t, 0.9 + i * 0.12, 1.1 + i * 0.12))
    q2 = seg(t, 1.6, 2.0)
    card(c, 810, 820, 340, 260, q2)
    text(c, 'NFL', 810, 780, 56, LIME, 'blacki', 'c', q2)
    text(c, '32 equipos', 810, 860, 34, WHITE, 'semi', 'c', q2)
    a = seg(t, 1.2, 1.7)
    if a > 0:
        x1 = 460 + 160 * eo(a)
        c.drawLine(460, 820, x1, 820, skia.Paint(AntiAlias=True, Color=col(LIME, a), StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap))
        pth = skia.Path(); pth.moveTo(x1 + 18, 820); pth.lineTo(x1 - 8, 800); pth.lineTo(x1 - 8, 840); pth.close()
        c.drawPath(pth, skia.Paint(AntiAlias=True, Color=col(LIME, a)))
    q3 = seg(t, 2.6, 3.0)
    chip(c, 'CADA AÑO · EN ABRIL', 540, 1100, 46, LIME, NAVY, q3, scale=pop(t, 2.6, 3.0))
    text(c, 'Los equipos eligen jugadores que vienen de la universidad', 540, 1230, 32, WHITE, 'bold', 'c', seg(t, 3.0, 3.4))

def dr_order(c, t, D):
    header(c)
    p = seg(t, 0.1, 0.5)
    text(c, 'EL ORDEN ES AL REVÉS', 540, 430, 72, WHITE, 'blacki', 'c', p, scale=pop(t, 0.1, 0.5))
    text(c, 'de la tabla de posiciones', 540, 500, 38, MUTED, 'semi', 'c', seg(t, 0.4, 0.8))
    # list of picks
    rows = [('1', 'Peor récord', (255, 90, 90)), ('2', '2º peor récord', (255, 140, 90)), ('3', '3º peor récord', (255, 180, 90)),
            ('…', '', MUTED), ('31', 'Subcampeón', WHITE), ('32', 'Campeón del Super Bowl', LIME)]
    for i, (n, lab, clr) in enumerate(rows):
        q = seg(t, 0.9 + i * 0.35 + (1.2 if i >= 4 else 0), 1.2 + i * 0.35 + (1.2 if i >= 4 else 0))
        y = 640 + i * 120
        if n == '…':
            text(c, '⋮'.replace('⋮', '· · ·'), 540, y, 48, MUTED, 'black', 'c', q); continue
        card(c, 540 + 40 * (1 - eo(q)), y, 800, 96, q, stroke=clr)
        text(c, f'PICK {n}', 220 + 40 * (1 - eo(q)), y, 40, clr, 'black', 'l', q)
        text(c, lab, 470 + 40 * (1 - eo(q)), y, 36, WHITE, 'bold', 'l', q)
        if n == '32' and q > 0:
            trophy(c, 990, y + 6, 0.22, q)
    text(c, 'Así los equipos débiles reciben a los mejores jóvenes', 540, 1400, 34, LIME, 'xb', 'c', seg(t, 4.8, 5.3))

def dr_rounds(c, t, D):
    header(c)
    p = seg(t, 0.1, 0.5)
    text(c, '7 RONDAS', 540, 440, 100, WHITE, 'blacki', 'c', p, scale=pop(t, 0.1, 0.5))
    text(c, 'En cada una, los 32 equipos eligen', 540, 520, 38, MUTED, 'semi', 'c', seg(t, 0.4, 0.8))
    cw, gap = 24, 4; x0 = 540 - (32 * cw + 31 * gap) / 2
    for r in range(7):
        y = 650 + r * 82
        q = seg(t, 0.8 + r * 0.3, 1.1 + r * 0.3)
        text(c, f'R{r+1}', x0 - 10, y, 30, LIME, 'black', 'r', q)
        for k in range(32):
            a = seg(t, 0.8 + r * 0.3 + k * 0.012, 1.0 + r * 0.3 + k * 0.012)
            if a <= 0: continue
            x = x0 + k * (cw + gap)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y - 26, x + cw, y + 26), 6, 6),
                        skia.Paint(AntiAlias=True, Color=col(LIME if r == 0 else (WHITE if r < 3 else SKY), a * (1 - 0.1 * r))))
    text(c, '32 equipos × 7 rondas', 540, 1290, 44, WHITE, 'black', 'c', seg(t, 3.4, 3.8))

def dr_trade(c, t, D):
    header(c)
    p = seg(t, 0.1, 0.5)
    text(c, 'LOS PICKS SE CAMBIAN', 540, 440, 72, WHITE, 'blacki', 'c', p, scale=pop(t, 0.1, 0.5))
    text(c, 'como si fueran fichas de intercambio', 540, 515, 36, MUTED, 'semi', 'c', seg(t, 0.4, 0.8))
    qa = seg(t, 0.6, 1.0)
    # two generic teams
    for x, lab, clr in ((240, 'EQUIPO A', LIME), (840, 'EQUIPO B', WHITE)):
        hexdraw(c, x, 860, 120 * eback(qa) if qa > 0 else 0, fill=NAVY2, stroke=clr, lw=8)
        text(c, lab, x, 860, 36, clr, 'black', 'c', qa)
    sw = eio(seg(t, 1.8, 3.0))
    # pick card goes A->B, player card B->A
    for (x0, x1, y, lab, clr) in ((240, 840, 700, 'PICK 5', LIME), (840, 240, 1020, 'JUGADOR', WHITE)):
        x = lerp(x0, x1, sw); yy = y - 80 * math.sin(math.pi * sw) * (1 if y < 860 else -1)
        a = seg(t, 1.2, 1.6)
        card(c, x, yy, 220, 80, a, stroke=clr)
        text(c, lab, x, yy, 32, clr, 'black', 'c', a)
    text(c, 'Un pick se puede cambiar por jugadores o por otros picks', 540, 1250, 32, WHITE, 'bold', 'c', seg(t, 3.2, 3.6))

def dr_outro(c, t, D):
    header(c, 1 - seg(t, 2.6, 2.9))
    a1 = 1 - seg(t, 2.6, 2.9)
    p = seg(t, 0, 0.4)
    text(c, 'SI TU EQUIPO', 540, 700, 90, WHITE, 'blacki', 'c', p * a1, scale=pop(t, 0, 0.4))
    text(c, 'ESCOGIERA PRIMERO…', 540, 810, 80, LIME, 'blacki', 'c', p * a1, scale=pop(t, 0.1, 0.5))
    text(c, '¿qué posición pedirías? Comenta', 540, 950, 42, WHITE, 'bold', 'c', seg(t, 0.8, 1.2) * a1)
    outro(c, t, 2.9)

DRAFT = [(dr_hook, 3.6), (dr_what, 5.5), (dr_order, 7.0), (dr_rounds, 5.5), (dr_trade, 5.5), (dr_outro, 6.0)]

# ================================================================ VIDEO 3: PICKS SEMANA 9
GAMES = [('JAX', 'BAL', 'JUEVES 5 NOV', '7:15 PM', None),
         ('CIN', 'ATL', 'DOMINGO 8 NOV', '8:30 AM', 'EN MADRID'),
         ('GB', 'NE', 'DOMINGO 8 NOV', '3:25 PM', None),
         ('TB', 'CHI', 'DOMINGO 8 NOV', '7:20 PM', 'DOMINGO NOCHE'),
         ('BUF', 'MIN', 'LUNES 9 NOV', '7:15 PM', 'LUNES NOCHE')]
NAMES = {'JAX': ('Jacksonville', 'Jaguars'), 'BAL': ('Baltimore', 'Ravens'), 'CIN': ('Cincinnati', 'Bengals'), 'ATL': ('Atlanta', 'Falcons'),
         'GB': ('Green Bay', 'Packers'), 'NE': ('Nueva Inglaterra', 'Patriots'), 'TB': ('Tampa Bay', 'Buccaneers'), 'CHI': ('Chicago', 'Bears'),
         'BUF': ('Buffalo', 'Bills'), 'MIN': ('Minnesota', 'Vikings')}

def pk_hook(c, t, D):
    header(c)
    out = 1 - seg(t, D - 0.25, D)
    p = seg(t, 0.1, 0.5)
    chip(c, 'SEMANA 9', 540, 700, 60, LIME, NAVY, p * out, scale=pop(t, 0.1, 0.5))
    for k, (s, clr, sz, y) in enumerate([('LOS PARTIDOS QUE', WHITE, 84, 860), ('NO TE PUEDES', WHITE, 84, 960), ('PERDER', LIME, 140, 1090)]):
        q = seg(t, 0.4 + k * 0.2, 0.8 + k * 0.2)
        text(c, s, 540, y, sz, clr, 'blacki', 'c', min(1, q * 2) * out, scale=0.6 + 0.4 * eback(q))
    text(c, 'Horarios del centro de México', 540, 1230, 36, MUTED, 'semi', 'c', seg(t, 1.4, 1.8) * out)

def pk_game_factory(i):
    away, home, day, hour, badge = GAMES[i]
    def sc(c, t, D):
        header(c)
        out = 1 - seg(t, D - 0.35, D)
        chip(c, f'{i+1}/5', 540, 400, 32, LIME, NAVY, seg(t, 0, 0.3) * out)
        text(c, day, 540, 480, 64, WHITE, 'blacki', 'c', seg(t, 0.05, 0.4) * out, scale=pop(t, 0.05, 0.4))
        text(c, hour + ' (CDMX)', 540, 550, 40, LIME, 'black', 'c', seg(t, 0.25, 0.6) * out)
        # teams slide in from sides
        ia = eback(seg(t, 0.3, 0.75)); ih = eback(seg(t, 0.45, 0.9))
        ax = 270 - 420 * (1 - ia) - 380 * eio(seg(t, D - 0.35, D)); hx = 810 + 420 * (1 - ih) + 380 * eio(seg(t, D - 0.35, D))
        a1 = min(1, seg(t, 0.3, 0.6) * 2) * out; a2 = min(1, seg(t, 0.45, 0.75) * 2) * out
        team_hex(c, away, ax, 880, 135, a1); team_hex(c, home, hx, 880, 135, a2)
        text(c, NAMES[away][0], ax, 1060, 40, WHITE, 'black', 'c', a1); text(c, NAMES[away][1], ax, 1108, 30, MUTED, 'semi', 'c', a1)
        text(c, NAMES[home][0], hx, 1060, 40, WHITE, 'black', 'c', a2); text(c, NAMES[home][1], hx, 1108, 30, MUTED, 'semi', 'c', a2)
        text(c, 'VISITA', ax, 720, 28, MUTED, 'xb', 'c', a1); text(c, 'LOCAL', hx, 720, 28, MUTED, 'xb', 'c', a2)
        bq = seg(t, 0.85, 1.25)
        if 0 < bq < 1: hexdraw(c, 540, 880, 60 + 110 * eo(bq), stroke=LIME, a=(1 - bq) * 0.9, lw=6)
        text(c, '@', 540, 880, 96, LIME, 'blacki', 'c', seg(t, 0.8, 1.1) * out, scale=1 + 0.2 * (1 - seg(t, 0.85, 1.2)))
        if badge:
            chip(c, badge, 540, 1230, 40, WHITE, NAVY, seg(t, 1.2, 1.6) * out, scale=pop(t, 1.2, 1.6))
        # poll
        pq = seg(t, 1.8, 2.2) * out
        if pq > 0:
            for x, ab in ((300, away), (780, home)):
                tm = AB[ab]
                r = skia.RRect.MakeRectXY(skia.Rect(x - 200, 1320, x + 200, 1410), 45, 45)
                c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(tm['p1'], pq)))
                c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(tm['p2'], pq), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                text(c, NAMES[ab][1].upper(), x, 1365, 34, tm['tc'], 'black', 'c', pq)
            text(c, '¿Quién gana? Comenta tu pick', 540, 1470, 34, WHITE, 'bold', 'c', seg(t, 2.1, 2.5) * out)
    return sc

def pk_outro(c, t, D):
    header(c, 1 - seg(t, 2.6, 2.9))
    a1 = 1 - seg(t, 2.6, 2.9)
    p = seg(t, 0, 0.4)
    text(c, 'DEJA TUS PICKS', 540, 760, 92, WHITE, 'blacki', 'c', p * a1, scale=pop(t, 0, 0.4))
    text(c, 'en los comentarios', 540, 850, 44, LIME, 'black', 'c', seg(t, 0.3, 0.7) * a1)
    text(c, 'y al final de la semana vemos quién le atinó', 540, 930, 40, WHITE, 'bold', 'c', seg(t, 0.8, 1.2) * a1)
    outro(c, t, 2.9)

PICKS = [(pk_hook, 3.6)] + [(pk_game_factory(i), 5.0) for i in range(5)] + [(pk_outro, 6.0)]

# ================================================================ VIDEO 4: CAMINO AL SUPER BOWL
SEEDY = [640 + i * 108 for i in range(7)]
def seed_col(c, x, a, label, clr, hl=None, dim=None, t=0, t0=0):
    text(c, label, x, 560, 60, clr, 'blacki', 'c', a)
    for i in range(7):
        q = seg(t, t0 + i * 0.12, t0 + 0.3 + i * 0.12) * a
        y = SEEDY[i]; wc = i >= 4
        d = 1 if dim is None else dim(i)
        fillc = NAVY2
        r = skia.RRect.MakeRectXY(skia.Rect(x - 170, y - 42, x + 170, y + 42), 20, 20)
        c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(fillc, q * d)))
        c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(WHITE if wc else clr, q * d), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        text(c, f'#{i+1}', x - 110, y, 40, clr, 'black', 'c', q * d)
        text(c, 'Comodín' if wc else 'Campeón div.', x + 40, y, 30, WHITE, 'semi', 'c', q * d)
        if hl and hl(i) > 0:
            c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(LIME, hl(i) * q), Style=skia.Paint.kStroke_Style, StrokeWidth=8))

def cs_hook(c, t, D):
    header(c)
    out = 1 - seg(t, D - 0.25, D)
    for k, (s, clr, sz, y) in enumerate([('¿CÓMO SE LLEGA', WHITE, 92, 820), ('AL SUPER BOWL?', LIME, 110, 940)]):
        p = seg(t, 0.15 + k * 0.25, 0.55 + k * 0.25)
        text(c, s, 540, y, sz, clr, 'blacki', 'c', min(1, p * 2) * out, scale=0.6 + 0.4 * eback(p))
    text(c, 'Así funcionan los playoffs', 540, 1080, 42, WHITE, 'bold', 'c', seg(t, 1.0, 1.4) * out)
    tq = seg(t, 1.3, 1.9) * out
    if tq > 0:
        glow(c, 540, 1330, 140, LIME, 0.3 * tq); trophy(c, 540, 1360 + 80 * (1 - eback(seg(t, 1.3, 1.9))), 0.7, tq)

def cs_seven(c, t, D):
    header(c)
    p = seg(t, 0.1, 0.5)
    text(c, '7 EQUIPOS POR CONFERENCIA', 540, 440, 62, WHITE, 'blacki', 'c', p, scale=pop(t, 0.1, 0.5))
    seed_col(c, 270, seg(t, 0.4, 0.8), 'AFC', LIME, t=t, t0=0.6)
    seed_col(c, 810, seg(t, 0.4, 0.8), 'NFC', WHITE, t=t, t0=0.9)
    text(c, '4 campeones de división + 3 comodines', 540, 1430, 36, LIME, 'xb', 'c', seg(t, 2.2, 2.6))

def cs_seeds(c, t, D):
    header(c)
    text(c, 'DEL #1 AL #7', 540, 440, 80, WHITE, 'blacki', 'c', 1)
    text(c, 'según su récord', 540, 505, 36, MUTED, 'semi', 'c', seg(t, 0.2, 0.6))
    h = lambda i: seg(t, 0.8, 1.2) if i < 4 else seg(t, 2.4, 2.8)
    seed_col(c, 270, 1, 'AFC', LIME, hl=h, t=9, t0=0)
    seed_col(c, 810, 1, 'NFC', WHITE, hl=h, t=9, t0=0)
    text(c, 'Los campeones de división siempre van del #1 al #4', 540, 1430, 32, LIME, 'xb', 'c', seg(t, 1.0, 1.4))

def cs_bye(c, t, D):
    header(c)
    text(c, 'EL #1 DESCANSA', 540, 440, 80, WHITE, 'blacki', 'c', seg(t, 0.1, 0.5), scale=pop(t, 0.1, 0.5))
    text(c, 'y pasa directo a la siguiente ronda', 540, 505, 36, MUTED, 'semi', 'c', seg(t, 0.4, 0.8))
    dim = lambda i: 1 if i == 0 else 1 - 0.6 * seg(t, 0.6, 1.0)
    seed_col(c, 270, 1, 'AFC', LIME, dim=dim, t=9, t0=0)
    seed_col(c, 810, 1, 'NFC', WHITE, dim=dim, t=9, t0=0)
    for x in (270, 810):
        q = seg(t, 1.0, 1.4)
        chip(c, 'DESCANSA', x + 40, SEEDY[0], 28, LIME, NAVY, q, scale=pop(t, 1.0, 1.4))

# bracket (single conference) layout
BX_ = [150, 460, 760, 960]
def bracket(c, t, stage, a=1):
    """stage: 0 wildcard pairs drawn; animations controlled by t inside each scene."""
    pass

def seed_box(c, x, y, s, a, clr=LIME, w=200, h=70, alive=1):
    if a <= 0: return
    r = skia.RRect.MakeRectXY(skia.Rect(x - w/2, y - h/2, x + w/2, y + h/2), 18, 18)
    c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(NAVY2, a * alive)))
    c.drawRRect(r, skia.Paint(AntiAlias=True, Color=col(clr, a * alive), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    text(c, s, x, y, 36, clr if alive > 0.5 else MUTED, 'black', 'c', a * max(alive, 0.35))

def cs_wildcard(c, t, D):
    header(c)
    text(c, 'RONDA DE COMODINES', 540, 440, 66, WHITE, 'blacki', 'c', seg(t, 0.1, 0.5), scale=pop(t, 0.1, 0.5))
    text(c, 'Juega en casa el mejor sembrado', 540, 505, 36, MUTED, 'semi', 'c', seg(t, 0.4, 0.8))
    pairs = [(2, 7), (3, 6), (4, 5)]
    for i, (hi, lo) in enumerate(pairs):
        q = seg(t, 0.8 + i * 0.9, 1.2 + i * 0.9)
        y = 700 + i * 220
        seed_box(c, 300 - 60 * (1 - eo(q)), y, f'#{hi}', q, LIME)
        seed_box(c, 780 + 60 * (1 - eo(q)), y, f'#{lo}', q, WHITE)
        text(c, 'VS', 540, y, 54, LIME, 'blacki', 'c', q)
        text(c, 'LOCAL', 300, y - 58, 24, MUTED, 'xb', 'c', q)
    q = seg(t, 3.8, 4.2)
    chip(c, 'EL QUE PIERDE, SE VA A CASA', 540, 1380, 40, YEL, NAVY, q, scale=pop(t, 3.8, 4.2))

def cs_divisional(c, t, D):
    header(c)
    text(c, 'RONDA DIVISIONAL', 540, 440, 72, WHITE, 'blacki', 'c', seg(t, 0.1, 0.5), scale=pop(t, 0.1, 0.5))
    text(c, 'Ejemplo: ganan el #2, el #3 y el #5', 540, 505, 36, MUTED, 'semi', 'c', seg(t, 0.4, 0.8))
    # survivors
    alive = [1, 2, 3, 5]
    q = seg(t, 0.6, 1.0)
    xs = [180, 400, 680, 900]
    # pairing #1 vs lowest (#5), #2 vs #3
    m = eio(seg(t, 1.6, 2.6))
    def pos(s):
        tgt = {1: (300, 950), 5: (780, 950), 2: (300, 1180), 3: (780, 1180)}[s]
        return lerp(xs[alive.index(s)], tgt[0], m), lerp(700, tgt[1], m)
    for s in alive:
        x, y = pos(s); seed_box(c, x, y, f'#{s}', q, LIME if s != 5 else WHITE, w=170)
    a = seg(t, 2.6, 3.0)
    text(c, 'VS', 540, 950, 54, LIME, 'blacki', 'c', a); text(c, 'VS', 540, 1180, 54, LIME, 'blacki', 'c', a)
    text(c, 'El #1 recibe al peor sembrado que siga vivo', 540, 1360, 34, LIME, 'xb', 'c', seg(t, 3.0, 3.4))

def cs_conf(c, t, D):
    header(c)
    text(c, 'FINAL DE CONFERENCIA', 540, 440, 64, WHITE, 'blacki', 'c', seg(t, 0.1, 0.5), scale=pop(t, 0.1, 0.5))
    q = seg(t, 0.5, 0.9)
    for x, lab, clr in ((300, 'AFC', LIME), (780, 'NFC', WHITE)):
        text(c, lab, x, 620, 56, clr, 'blacki', 'c', q)
        seed_box(c, x, 760, 'GANADOR', q, clr, w=260)
        seed_box(c, x, 900, 'GANADOR', q, clr, w=260)
        text(c, 'VS', x, 830, 40, clr, 'blacki', 'c', q)
        m = eio(seg(t, 1.8, 2.6))
        if m > 0:
            c.drawLine(x, 950, x, 950 + 150 * m, skia.Paint(AntiAlias=True, Color=col(clr, q), StrokeWidth=6))
            seed_box(c, x, 1150, 'CAMPEÓN ' + lab, seg(t, 2.4, 2.8), clr, w=320)
    text(c, 'Los dos que sobreviven se juegan el pase', 540, 1330, 34, WHITE, 'bold', 'c', seg(t, 1.0, 1.4))

def cs_sb(c, t, D):
    hx = 1 - seg(t, 4.3, 4.6)
    header(c, hx)
    up = eio(seg(t, 1.4, 2.0)); a1 = 1 - up
    p = seg(t, 0.0, 0.4)
    text(c, 'AFC', 300, 760, 110, LIME, 'blacki', 'c', p * a1, scale=0.7 + 0.3 * eback(p))
    text(c, 'NFC', 780, 760, 110, WHITE, 'blacki', 'c', p * a1, scale=0.7 + 0.3 * eback(p))
    text(c, 'vs', 540, 760, 56, MUTED, 'xb', 'c', seg(t, 0.3, 0.6) * a1)
    q = seg(t, 0.6, 1.0); sbo = 1 - seg(t, 4.2, 4.5)
    text(c, 'SUPER BOWL', 540, lerp(1000, 470, up), 124, LIME, 'blacki', 'c', q * sbo, scale=0.7 + 0.3 * eback(q))
    tr = seg(t, 1.6, 2.2); ta = tr * sbo
    if ta > 0:
        c.save(); c.translate(540, 940); c.rotate(t * 12)
        for k in range(14):
            c.save(); c.rotate(k * 360 / 14)
            pth = skia.Path(); pth.moveTo(0, 0); pth.lineTo(-60, -900); pth.lineTo(60, -900); pth.close()
            c.drawPath(pth, skia.Paint(AntiAlias=True, Color=col(LIME, 0.07 * ta))); c.restore()
        c.restore()
        glow(c, 540, 900, 230, LIME, 0.35 * ta)
        trophy(c, 540, 940 + 260 * (1 - eback(tr)), 1.25, ta)
        text(c, '¡CAMPEÓN!', 540, 1250, 64, WHITE, 'blacki', 'c', seg(t, 2.1, 2.5) * sbo, scale=0.8 + 0.2 * eback(seg(t, 2.1, 2.5)))
    confetti(c, 1.8, t, 540, 820)
    outro(c, t, 4.6)

CAMINO = [(cs_hook, 3.6), (cs_seven, 6.0), (cs_seeds, 5.5), (cs_bye, 4.5), (cs_wildcard, 7.0), (cs_divisional, 7.0), (cs_conf, 5.5), (cs_sb, 8.0)]

VIDEOS = {'faltas': FALTAS, 'draft': DRAFT, 'picks': PICKS, 'camino': CAMINO}

def render_scene(vid, k, out, D=None, warp=None):
    fn, D0 = VIDEOS[vid][k]; D = D or D0; n = int(round(D * FPS)); sc = D0 / D
    tmp = out[:-4] + '.part.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    import numpy as np
    for f in range(n):
        tn = float(np.interp(f / FPS, [a for a, b in warp], [b for a, b in warp])) if warp else f / FPS * sc
        img = frame(fn, tn, D0)
        p.stdin.write(img.toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, out)

if __name__ == '__main__':
    vid, mode = sys.argv[1], sys.argv[2]
    if mode == 'still':
        k = int(sys.argv[3]); tt = float(sys.argv[4]); fn, D = VIDEOS[vid][k]
        frame(fn, tt, D).save(sys.argv[5], skia.kPNG)
    else:
        k = int(mode); out = sys.argv[3]
        D = float(sys.argv[4]) if len(sys.argv) > 4 else None
        w = json.loads(os.environ['WARP']) if os.environ.get('WARP') else None
        render_scene(vid, k, out, D, w)
