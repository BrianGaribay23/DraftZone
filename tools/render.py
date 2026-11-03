import skia, math, random, subprocess, sys, os
W,H,FPS=1080,1920,30
FD='/usr/share/fonts/opentype/inter/'
TF={k:skia.Typeface.MakeFromFile(FD+v) for k,v in dict(black='InterDisplay-Black.otf',blacki='InterDisplay-BlackItalic.otf',xb='InterDisplay-ExtraBold.otf',bold='InterDisplay-Bold.otf',semi='InterDisplay-SemiBold.otf').items()}
NAVY=(11,27,58);NAVY2=(20,40,78);LIME=(198,255,26);WHITE=(255,255,255);MUTED=(150,172,205)
def col(c,a=1.0): return skia.ColorSetARGB(int(max(0,min(1,a))*255),*c)
def cl(x): return max(0.0,min(1.0,x))
def seg(t,a,b): return cl((t-a)/(b-a))
def eo(x): return 1-(1-x)**3
def eback(x):
    c1=1.70158;c3=c1+1; return 1+c3*(x-1)**3+c1*(x-1)**2
def eio(x): return 4*x**3 if x<.5 else 1-(-2*x+2)**3/2
def lerp(a,b,x): return a+(b-a)*x

# background
def make_bg():
    s=skia.Surface(W,H);c=s.getCanvas()
    p=skia.Paint(Shader=skia.GradientShader.MakeLinear([(0,0),(0,H)],[col((15,35,72)),col((6,15,33))]))
    c.drawRect(skia.Rect(0,0,W,H),p)
    lp=skia.Paint(AntiAlias=True,Color=col(WHITE,.05),StrokeWidth=3,Style=skia.Paint.kStroke_Style)
    for y in range(120,H,150):
        c.drawLine(0,y,W,y,lp)
        for x in (300,780):
            c.drawLine(x,y-18,x,y+18,lp)
    g=skia.Paint(Shader=skia.GradientShader.MakeRadial((W/2,H*0.45),900,[col(LIME,.07),col(LIME,0)]))
    c.drawRect(skia.Rect(0,0,W,H),g)
    return s.makeImageSnapshot()
BG=make_bg()

def text(c,s,x,y,size,color,tf='black',align='c',alpha=1,scale=1,ls=0):
    if alpha<=0: return
    f=skia.Font(TF[tf],size)
    w=f.measureText(s)
    p=skia.Paint(AntiAlias=True,Color=col(color,alpha))
    c.save();c.translate(x,y);c.scale(scale,scale)
    dx={'c':-w/2,'l':0,'r':-w}[align]
    c.drawString(s,dx,size*0.36,f,p)
    c.restore()
    return w

def hexpath(cx,cy,r):
    p=skia.Path()
    for i in range(6):
        a=math.radians(60*i-90)
        x,y=cx+r*math.cos(a),cy+r*math.sin(a)
        (p.moveTo if i==0 else p.lineTo)(x,y)
    p.close();return p
def hexdraw(c,cx,cy,r,fill=None,stroke=None,a=1,lw=5,fa=1):
    if r<=0 or a<=0: return
    hp=hexpath(cx,cy,r)
    if fill: c.drawPath(hp,skia.Paint(AntiAlias=True,Color=col(fill,a*fa)))
    if stroke: c.drawPath(hp,skia.Paint(AntiAlias=True,Color=col(stroke,a),Style=skia.Paint.kStroke_Style,StrokeWidth=lw,StrokeJoin=skia.Paint.kRound_Join))
def glow(c,cx,cy,r,color,a):
    p=skia.Paint(AntiAlias=True,Color=col(color,a),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,r*0.35))
    c.drawPath(hexpath(cx,cy,r*1.15),p)

import os; LD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logos')+'/'
IMG={k:skia.Image.open(LD+k+'.png').withDefaultMipmaps() for k in ('sym','hor','ver')}
SAMP=skia.SamplingOptions(skia.FilterMode.kLinear,skia.MipmapMode.kLinear)
def drawimg(c,k,cx,cy,w,a=1):
    im=IMG[k];h=w*im.height()/im.width()
    c.drawImageRect(im,skia.Rect(cx-w/2,cy-h/2,cx+w/2,cy+h/2),SAMP,skia.Paint(AntiAlias=True,Color=col(WHITE,a)))
def logo_old(c,cx,cy,r,a=1):
    hexdraw(c,cx,cy,r,fill=NAVY2,stroke=LIME,a=a,lw=max(3,r*0.09))
    text(c,'DZ',cx,cy,r*0.95,WHITE,'blacki',alpha=a)

def header(c,a=1):
    drawimg(c,'hor',60+190,250,380,a)

def wrap_center(c,lines,y,size,color,tf='black',alpha=1,gap=1.15,scale=1):
    for i,(s,clr) in enumerate(lines):
        text(c,s,W/2,y+i*size*gap,size,clr if clr else color,tf,'c',alpha,scale)

# teams
random.seed(7)
TEAMS=[]
TD=[('BUF',(0,51,141),(198,12,48)),('MIA',(0,142,151),(252,76,2)),('NE',(0,34,68),(198,12,48)),('NYJ',(18,87,64),(255,255,255)),
('BAL',(36,23,115),(158,124,12)),('CIN',(251,79,20),(0,0,0)),('CLE',(49,29,0),(255,60,0)),('PIT',(255,182,18),(16,24,32)),
('HOU',(3,32,47),(167,25,48)),('IND',(0,44,95),(162,170,173)),('JAX',(0,103,120),(215,162,42)),('TEN',(75,146,219),(12,35,64)),
('DEN',(251,79,20),(0,34,68)),('KC',(227,24,55),(255,184,28)),('LV',(0,0,0),(165,172,175)),('LAC',(0,128,198),(255,194,14)),
('DAL',(0,53,148),(134,147,151)),('NYG',(1,35,82),(163,13,45)),('PHI',(0,76,84),(165,172,175)),('WAS',(90,20,20),(255,182,18)),
('CHI',(11,22,42),(200,56,3)),('DET',(0,118,182),(176,183,188)),('GB',(32,55,49),(255,184,28)),('MIN',(79,38,131),(255,198,47)),
('ATL',(167,25,48),(0,0,0)),('CAR',(0,133,202),(16,24,32)),('NO',(211,188,141),(16,24,32)),('TB',(213,10,10),(52,48,43)),
('ARI',(151,35,63),(255,182,18)),('LAR',(0,53,148),(255,209,0)),('SF',(170,0,0),(173,153,93)),('SEA',(0,34,68),(105,190,40))]
for i in range(32):
    cc=i//16;k=i%16;d=k//4;j=k%4
    ab,p1,p2=TD[i]
    lum=0.299*p1[0]+0.587*p1[1]+0.114*p1[2]
    TEAMS.append(dict(c=cc,d=d,j=j,ab=ab,p1=p1,p2=p2,tc=(16,24,32) if lum>150 else WHITE))
pop_order=list(range(32));random.shuffle(pop_order)
POP={t:n for n,t in enumerate(pop_order)}
WIN={(cc,d):random.randrange(4) for cc in range(2) for d in range(4)}
WC={}
for cc in range(2):
    pool=[i for i,t in enumerate(TEAMS) if t['c']==cc and t['j']!=WIN[(cc,t['d'])]]
    random.shuffle(pool)
    for i in pool[:3]: WC[i]=1
def pos_grid(t): return 540+((t['c']*4+t['j'])-3.5)*112, 960+(t['d']-1.5)*112, 46
BX=(250,830)
def pos_split(t): return BX[t['c']]+(t['j']-1.5)*92, 960+(t['d']-1.5)*112, 40
def pos_div(t): return BX[t['c']]+(t['j']-1.5)*92, 770+t['d']*165, 40
CONFC=(LIME,WHITE)
DIVN=['ESTE','NORTE','SUR','OESTE']

def draw_teams(c,posf,a=1,colorize=1,dim=lambda i:1,extra=None):
    for i,t in enumerate(TEAMS):
        x,y,r=posf(i,t)
        if r<=0: continue
        sc=CONFC[t['c']] if colorize>0.5 else WHITE
        if 0<colorize<1:
            base=CONFC[t['c']];sc=tuple(int(lerp(255,base[k],colorize)) for k in range(3))
        aa=a*dim(i)
        hexdraw(c,x,y,r,fill=t['p1'],stroke=t['p2'],a=aa,lw=4)
        text(c,t['ab'],x,y,r*(0.62 if len(t['ab'])<3 else 0.52),t['tc'],'black','c',aa)
        if extra: extra(c,i,t,x,y,r)

def conf_headers(c,a,y=640):
    for cc,name,sub in ((0,'AFC','Conferencia Americana'),(1,'NFC','Conferencia Nacional')):
        text(c,name,BX[cc],y,70,CONFC[cc],'black','c',a)
        text(c,sub,BX[cc],y+58,27,MUTED,'semi','c',a)

def div_labels(c,a):
    for d in range(4):
        text(c,DIVN[d],540,770+d*165,30,WHITE,'xb','c',a)

# ---------- scenes ----------
def s1(c,t,D):
    # hook
    for k in range(3):
        rr=320+k*90; a=0.10-0.03*k
        c.save();c.translate(540,960);c.rotate(t*12*(1 if k%2 else -1))
        hexdraw(c,0,0,rr*(0.6+0.4*eo(seg(t,0,0.6))),stroke=LIME,a=a+0.05,lw=4)
        c.restore()
    lines=[('¿CÓMO FUNCIONAN',WHITE,92,800),('LAS DIVISIONES',LIME,118,925),('DE LA NFL?',WHITE,92,1050)]
    for k,(s,clr,sz,y) in enumerate(lines):
        p=seg(t,0.15+k*0.22,0.55+k*0.22)
        out=1-seg(t,D-0.25,D)
        text(c,s,540,y,sz,clr,'blacki','c',min(p*2,1)*out,scale=0.6+0.4*eback(p))
    p=seg(t,1.3,1.7)
    text(c,'Te lo explico rápido',540,1180,40,MUTED,'semi','c',p*(1-seg(t,D-0.25,D)))
    header(c)

def s2(c,t,D):
    header(c)
    n=int(round(32*eo(seg(t,0.2,2.0))))
    p=seg(t,0.0,0.4)
    text(c,str(n),540,520,190,LIME,'blacki','c',p,scale=0.8+0.2*eback(p))
    text(c,'EQUIPOS',540,660,64,WHITE,'black','c',seg(t,0.3,0.7))
    def pf(i,tm):
        x,y,r=pos_grid(tm); q=seg(t,0.2+POP[i]*0.05,0.55+POP[i]*0.05)
        return x,y,r*eback(q) if q>0 else 0
    draw_teams(c,pf,colorize=0)
    text(c,'Y así se organiza toda la liga:',540,1300,44,WHITE,'bold','c',seg(t,2.4,2.9))

def s3(c,t,D):
    header(c)
    m=eio(seg(t,0.1,1.1))
    def pf(i,tm):
        a=pos_grid(tm);b=pos_split(tm)
        return lerp(a[0],b[0],m),lerp(a[1],b[1],m),lerp(a[2],b[2],m)
    p=seg(t,0.6,1.1)
    text(c,'2 CONFERENCIAS',540,470,84,WHITE,'blacki','c',p,scale=0.85+0.15*eback(p))
    conf_headers(c,seg(t,1.0,1.5),y=650)
    draw_teams(c,pf,colorize=m)
    text(c,'16 equipos en cada una',540,1290,46,WHITE,'bold','c',seg(t,1.8,2.3))

def s4(c,t,D):
    header(c)
    m=eio(seg(t,0.1,1.1))
    def pf(i,tm):
        a=pos_split(tm);b=pos_div(tm)
        return lerp(a[0],b[0],m),lerp(a[1],b[1],m),40
    p=seg(t,0.4,0.9)
    text(c,'4 DIVISIONES',540,440,84,WHITE,'blacki','c',p,scale=0.85+0.15*eback(p))
    text(c,'en cada conferencia',540,515,40,MUTED,'semi','c',p)
    conf_headers(c,1,y=620)
    for d in range(4):
        text(c,DIVN[d],540,770+d*165,30,WHITE,'xb','c',seg(t,1.0+d*0.2,1.3+d*0.2))
    # division brackets
    for cc in range(2):
        for d in range(4):
            a=seg(t,1.0+d*0.2,1.3+d*0.2)*0.18
            y=770+d*165
            r=skia.RRect.MakeRectXY(skia.Rect(BX[cc]-190,y-58,BX[cc]+190,y+58),24,24)
            c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(CONFC[cc],a),Style=skia.Paint.kStroke_Style,StrokeWidth=3))
    draw_teams(c,pf)
    text(c,'4 equipos por división',540,1450,48,WHITE,'bold','c',seg(t,2.2,2.7))
    text(c,'8 divisiones en total',540,1520,40,LIME,'xb','c',seg(t,3.4,3.9))

CITIES=[('Denver','Broncos'),('Kansas City','Chiefs'),('Las Vegas','Raiders'),('Los Ángeles','Chargers')]
def s5(c,t,D):
    header(c)
    m=eio(seg(t,0.3,1.3))
    fade=1-seg(t,0,0.5)
    conf_headers(c,fade,y=620)
    for d in range(4): text(c,DIVN[d],540,770+d*165,30,WHITE,'xb','c',fade)
    out0=eio(seg(t,5.3,6.6))
    def pf(i,tm):
        x,y,r=pos_div(tm)
        if tm['c']==0 and tm['d']==3:
            tx,ty,tr=210,650+tm['j']*165,62
            x,y,r=lerp(x,tx,m),lerp(y,ty,m),lerp(r,tr,m)
            if i!=13 and out0>0: r=r*(1-0.5*out0)
            return x,y,r
        return x,y,r
    def dim(i):
        tm=TEAMS[i]
        if i==13: return 0 if out0>0 else 1
        return (1-out0) if (tm['c']==0 and tm['d']==3) else fade
    draw_teams(c,pf,dim=dim)
    if out0>0:
        x=lerp(210,270,out0);y=lerp(815,880,out0);r=lerp(62,135,out0)
        team_hex(c,'KC',x,y,r,1,ga=out0)
        la=seg(t,6.4,6.9)
        text(c,'Kansas City',270,1060,40,WHITE,'black','c',la)
        text(c,'Chiefs',270,1108,30,MUTED,'semi','c',la)
    p=seg(t,0.8,1.3); out=eio(seg(t,5.3,6.6)); ka=1-out
    text(c,'EJEMPLO',540,420,40,LIME,'xb','c',p*ka)
    text(c,'AFC OESTE',540,495,92,WHITE,'blacki','c',p*ka,scale=0.85+0.15*eback(p))
    for j,s_ in enumerate(CITIES):
        q=seg(t,1.3+j*0.18,1.7+j*0.18)
        xx=310+40*(1-eo(q))-60*out
        text(c,s_[0],xx,632+j*165,54,WHITE,'black','l',q*ka)
        text(c,s_[1],xx,682+j*165,32,MUTED,'semi','l',q*ka)
    # x2 badges
    for j in range(4):
        q=seg(t,2.9+j*0.12,3.2+j*0.12)*ka
        if q>0 and j!=1:
            bx,by=800,650+j*165
            c.drawCircle(bx,by,36*eback(min(1,q*1.2)),skia.Paint(AntiAlias=True,Color=col(LIME,q)))
            text(c,'x2',bx,by,32,NAVY,'black','c',q)
    q=seg(t,2.6,3.0)
    text(c,'Juegan 2 veces entre ellos',540,1330,46,WHITE,'bold','c',q*ka)
    text(c,'ida y vuelta',540,1395,34,MUTED,'semi','c',seg(t,3.0,3.4)*ka)

def s6(c,t,D):
    header(c)
    fin=seg(t,0,0.5)
    p=seg(t,0.2,0.7)
    text(c,'¿QUIÉN VA A',540,420,68,WHITE,'blacki','c',p)
    text(c,'PLAYOFFS?',540,500,96,LIME,'blacki','c',p,scale=0.85+0.15*eback(p))
    conf_headers(c,fin,y=620)
    for d in range(4): text(c,DIVN[d],540,770+d*165,30,WHITE,'xb','c',fin)
    w1=seg(t,1.0,1.5); w2=seg(t,3.6,4.1)
    def iswin(i): tm=TEAMS[i]; return WIN[(tm['c'],tm['d'])]==tm['j']
    def dim(i):
        if iswin(i): return 1
        if i in WC: return lerp(1,0.35,w1)*(1-w2)+w2
        return lerp(1,0.25,w1)
    text(c,'* Ejemplo ilustrativo, no es la tabla real',540,1580,26,MUTED,'semi','c',seg(t,1.0,1.5))
    def extra(c,i,tm,x,y,r):
        cc=CONFC[tm['c']]
        bx,by=x+r*0.72,y-r*0.62
        if iswin(i) and w1>0:
            hexdraw(c,x,y,r+5,stroke=LIME,a=w1,lw=5)
            br=17*eback(w1)
            c.drawCircle(bx,by,br,skia.Paint(AntiAlias=True,Color=col(LIME,w1)))
            pth=skia.Path();pth.moveTo(bx-7,by);pth.lineTo(bx-2,by+6);pth.lineTo(bx+8,by-6)
            c.drawPath(pth,skia.Paint(AntiAlias=True,Color=col(NAVY,w1),Style=skia.Paint.kStroke_Style,StrokeWidth=4.5,StrokeCap=skia.Paint.kRound_Cap,StrokeJoin=skia.Paint.kRound_Join))
        if i in WC and w2>0:
            hexdraw(c,x,y,r+5,stroke=WHITE,a=w2,lw=4)
            rr=skia.RRect.MakeRectXY(skia.Rect(bx-22,by-14,bx+22,by+14),14,14)
            c.drawRRect(rr,skia.Paint(AntiAlias=True,Color=col(WHITE,w2)))
            text(c,'WC',bx,by,18,NAVY,'black','c',w2)
    draw_teams(c,lambda i,tm:(pos_div(tm)),a=fin,dim=dim,extra=extra)
    q1=seg(t,1.3,1.8);q1o=seg(t,3.4,3.7)
    text(c,'Ganas tu división = estás dentro',540,1450,44,WHITE,'bold','c',q1*(1-q1o))
    q2=seg(t,3.8,4.3);q2o=seg(t,5.8,6.1)
    text(c,'+3 comodines por conferencia',540,1450,44,WHITE,'bold','c',q2*(1-q2o))
    text(c,'(los mejores récords que no ganaron)',540,1515,32,MUTED,'semi','c',q2*(1-q2o))
    q3=seg(t,6.2,6.6)
    text(c,'7 por conferencia',540,1440,52,WHITE,'black','c',q3,scale=0.85+0.15*eback(q3))
    text(c,'14 equipos en total',540,1515,40,LIME,'xb','c',seg(t,6.6,7.0))

def trophy(c,cx,cy,sc,a):
    if a<=0: return
    c.save();c.translate(cx,cy);c.scale(sc,sc)
    sil=skia.GradientShader.MakeLinear([(-120,0),(120,0)],[col((150,160,175),a),col((255,255,255),a),col((190,200,215),a),col((120,130,150),a)])
    pm=skia.Paint(AntiAlias=True,Shader=sil)
    # bowl
    p=skia.Path();p.moveTo(-120,-170);p.lineTo(120,-170);p.cubicTo(120,-40,70,20,22,40);p.lineTo(-22,40);p.cubicTo(-70,20,-120,-40,-120,-170);p.close()
    c.drawPath(p,pm)
    # rim
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-132,-186,132,-166),8,8),pm)
    # handles
    hp=skia.Paint(AntiAlias=True,Shader=sil,Style=skia.Paint.kStroke_Style,StrokeWidth=16)
    h=skia.Path();h.moveTo(-118,-150);h.cubicTo(-200,-150,-200,-50,-90,-40);c.drawPath(h,hp)
    h=skia.Path();h.moveTo(118,-150);h.cubicTo(200,-150,200,-50,90,-40);c.drawPath(h,hp)
    # stem + base
    c.drawRect(skia.Rect(-18,40,18,110),pm)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-60,105,60,125),6,6),pm)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-95,125,95,175),10,10),skia.Paint(AntiAlias=True,Color=col(NAVY2,a)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-95,125,95,175),10,10),skia.Paint(AntiAlias=True,Color=col(LIME,a),Style=skia.Paint.kStroke_Style,StrokeWidth=5))
    # shine
    c.drawPath(skia.Path.Rect(skia.Rect(-80,-160,-62,-40)),skia.Paint(AntiAlias=True,Color=col(WHITE,0.55*a)))
    c.restore()
_rng=random.Random(11)
CONF=[(_rng.uniform(-1,1),_rng.uniform(-1.6,-0.6),_rng.uniform(0,6.28),_rng.uniform(-8,8),_rng.choice([LIME,WHITE,(110,170,235),LIME]),_rng.uniform(8,16)) for _ in range(120)]
def confetti(c,t0,t,cx,cy):
    dt=t-t0
    if dt<0 or dt>3.2: return
    fa=1-seg(dt,2.4,3.2)
    for vx,vy,rot,vr,clr,sz in CONF:
        x=cx+vx*900*dt; y=cy+vy*1100*dt+900*dt*dt
        if y>1900: continue
        c.save();c.translate(x,y);c.rotate((rot+vr*dt)*57.3)
        c.drawRect(skia.Rect(-sz/2,-sz/4,sz/2,sz/4),skia.Paint(AntiAlias=True,Color=col(clr,fa)))
        c.restore()
def s7(c,t,D):
    hx=1-seg(t,4.3,4.6)
    header(c,hx)
    up=eio(seg(t,1.7,2.3)); a1=1-up
    p=seg(t,0.0,0.4)
    text(c,'AFC',300,760,110,LIME,'blacki','c',p*a1,scale=0.7+0.3*eback(p))
    text(c,'NFC',780,760,110,WHITE,'blacki','c',p*a1,scale=0.7+0.3*eback(p))
    text(c,'vs',540,760,56,MUTED,'xb','c',seg(t,0.3,0.6)*a1)
    text(c,'Los campeones de cada conferencia',540,900,40,WHITE,'bold','c',seg(t,0.5,0.9)*a1)
    text(c,'se juegan el',540,955,40,WHITE,'bold','c',seg(t,0.5,0.9)*a1)
    q=seg(t,0.9,1.3); sbo=1-seg(t,4.2,4.5)
    text(c,'SUPER BOWL',540,lerp(1090,470,up),124,LIME,'blacki','c',q*sbo,scale=0.7+0.3*eback(q))
    # trophy moment
    tr=seg(t,1.9,2.5); ta=tr*sbo
    if ta>0:
        # rays
        c.save();c.translate(540,940);c.rotate(t*12)
        for k in range(14):
            ang=k*360/14
            c.save();c.rotate(ang)
            pth=skia.Path();pth.moveTo(0,0);pth.lineTo(-60,-900);pth.lineTo(60,-900);pth.close()
            c.drawPath(pth,skia.Paint(AntiAlias=True,Color=col(LIME,0.07*ta)))
            c.restore()
        c.restore()
        glow(c,540,900,230,LIME,0.35*ta)
        trophy(c,540,940+260*(1-eback(tr)),1.25,ta)
        text(c,'¡CAMPEÓN!',540,1250,64,WHITE,'blacki','c',seg(t,2.4,2.8)*sbo,scale=0.8+0.2*eback(seg(t,2.4,2.8)))
    confetti(c,2.1,t,540,820)
    # outro
    o=seg(t,4.6,5.2)
    if o>0:
        glow(c,540,800,170,LIME,0.25*o)
        drawimg(c,'ver',540,920,820*(0.7+0.3*eback(o)),o)
        text(c,'Síguenos para más NFL en español',540,1360,42,WHITE,'bold','c',seg(t,5.3,5.8))

SKY=(110,170,235)
GROUPS=[(6,LIME,'fill','contra su división',2.5),(4,WHITE,'fill','otra división de su conferencia',5.0),(4,SKY,'fill','una división de la otra conferencia',7.5),(3,LIME,'line','equipos que quedaron en su misma posición',10.0)]
def s5b(c,t,D):
    header(c)
    p=seg(t,0.1,0.6)
    text(c,'NO SOLO ENTRE ELLOS',540,430,78,WHITE,'blacki','c',p,scale=0.85+0.15*eback(p))
    text(c,'Cada equipo juega 17 partidos',540,505,40,MUTED,'semi','c',seg(t,0.5,1.0))
    # example team
    q=seg(t,0.8,1.3); kc=TEAMS[13]
    if q>0:
        hexdraw(c,540,640,52*eback(q),fill=kc['p1'],stroke=kc['p2'],lw=5)
        text(c,'KC',540,640,32,WHITE,'black','c',q)
    # slots
    bw,gap=48,8; x0=540-(17*bw+16*gap)/2; y0,y1=760,830
    k=0
    for n,clr,sty,lab,t0 in GROUPS:
        for i in range(n):
            a=seg(t,t0+i*0.09,t0+0.25+i*0.09)
            x=x0+k*(bw+gap)
            r=skia.RRect.MakeRectXY(skia.Rect(x,y0,x+bw,y1),10,10)
            c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(MUTED,0.35),Style=skia.Paint.kStroke_Style,StrokeWidth=2))
            if a>0:
                c.save();c.translate(x+bw/2,(y0+y1)/2);s_=0.4+0.6*eback(a);c.scale(s_,s_);c.translate(-(x+bw/2),-(y0+y1)/2)
                if sty=='fill': c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(clr,a)))
                else: c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(clr,a),Style=skia.Paint.kStroke_Style,StrokeWidth=5))
                c.restore()
            k+=1
    # counter
    tot=0
    for n,clr,sty,lab,t0 in GROUPS:
        if t>=t0: tot+=int(round(n*eo(seg(t,t0,t0+0.6))))
    fin=seg(t,12.3,12.8)
    if tot>0:
        text(c,str(tot),540,950,150,LIME if fin>0 else WHITE,'blacki','c',1,scale=1+0.12*eback(fin)*(1-seg(t,12.8,13.4)))
        text(c,'PARTIDOS',540,1045,40,WHITE,'black','c',seg(t,2.6,3.0))
    # legend
    for j,(n,clr,sty,lab,t0) in enumerate(GROUPS):
        a=seg(t,t0,t0+0.4); y=1150+j*78
        if a<=0: continue
        x=90+30*(1-eo(a))
        r=skia.RRect.MakeRectXY(skia.Rect(x,y-20,x+40,y+20),8,8)
        if sty=='fill': c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(clr,a)))
        else: c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(clr,a),Style=skia.Paint.kStroke_Style,StrokeWidth=4))
        text(c,str(n),x+70,y,40,clr if clr!=WHITE else WHITE,'black','l',a)
        text(c,lab,x+115,y,32,WHITE,'semi','l',a)

AB={t['ab']:t for t in TEAMS}
CITY={'DEN':'Denver','LV':'Las Vegas','LAC':'Los Ángeles','NYJ':'NY Jets','NE':'Nueva Inglaterra','BUF':'Buffalo','MIA':'Miami',
 'ARI':'Arizona','SF':'San Francisco','LAR':'Los Ángeles','SEA':'Seattle','IND':'Indianápolis','CIN':'Cincinnati','ATL':'Atlanta','KC':'Kansas City'}
NICK={'DEN':'Broncos','LV':'Raiders','LAC':'Chargers','NYJ':'Jets','NE':'Patriots','BUF':'Bills','MIA':'Dolphins','ARI':'Cardinals','SF':'49ers',
 'LAR':'Rams','SEA':'Seahawks','IND':'Colts','CIN':'Bengals','ATL':'Falcons','KC':'Chiefs'}
# groups: label, sub, opponents, games each, nominal start, per-card duration
MGROUPS=[('SU DIVISIÓN','AFC Oeste · 2 veces c/u',['DEN','LV','LAC'],2),
         ('OTRA DIVISIÓN DE SU CONFERENCIA','AFC Este · 1 vez c/u',['NYJ','NE','BUF','MIA'],1),
         ('UNA DIVISIÓN DE LA OTRA CONFERENCIA','NFC Oeste · 1 vez c/u',['ARI','SF','LAR','SEA'],1),
         ('MISMA POSICIÓN QUE EL AÑO PASADO','3er lugar de otras divisiones',['IND','CIN','ATL'],1)]
MG_T=[1.6,4.6,7.8,11.0]; MG_END=14.0
def mg_cards():
    out=[]
    for gi,(lab,sub,ops,g) in enumerate(MGROUPS):
        t0=MG_T[gi]; t1=MG_T[gi+1] if gi<3 else MG_END
        step=(t1-t0-0.2)/len(ops)
        for i,o in enumerate(ops): out.append((gi,o,g,t0+0.2+i*step,step))
    return out
CARDS=mg_cards()
def team_hex(c,ab,x,y,r,a=1,ga=1):
    tm=AB[ab]
    if ga>0: glow(c,x,y,r,tm['p1'],0.45*a*ga)
    hexdraw(c,x,y,r,fill=tm['p1'],stroke=tm['p2'],a=a,lw=r*0.07)
    text(c,ab,x,y,r*(0.62 if len(ab)<3 else 0.5),tm['tc'],'black','c',a)
def s_match(c,t,D):
    header(c)
    p=seg(t,0.1,0.6)
    text(c,'17 PARTIDOS',540,420,96,WHITE,'blacki','c',p,scale=0.85+0.15*eback(p))
    text(c,'por temporada · ejemplo: Kansas City',540,500,36,MUTED,'semi','c',seg(t,0.4,0.9))
    # category pill
    gi=max([i for i in range(4) if t>=MG_T[i]],default=-1)
    for g0 in MG_T:
        w_=seg(t,g0-0.05,g0+0.4)
        if 0<w_<1:
            bx=-500+2100*eio(w_)
            pth=skia.Path();pth.moveTo(bx,540);pth.lineTo(bx+320,540);pth.lineTo(bx+240,700);pth.lineTo(bx-80,700);pth.close()
            c.drawPath(pth,skia.Paint(AntiAlias=True,Color=col(LIME,0.9*(1-abs(2*w_-1)**3))))
    if gi>=0:
        lab,sub,ops,g=MGROUPS[gi]; q=seg(t,MG_T[gi]+0.12,MG_T[gi]+0.45)
        f=skia.Font(TF['black'],34);w=f.measureText(lab)+60
        y=600; rr=skia.RRect.MakeRectXY(skia.Rect(540-w/2,y-32,540+w/2,y+32),32,32)
        c.save();c.translate(540,y);s_=0.8+0.2*eback(q);c.scale(s_,s_);c.translate(-540,-y)
        c.drawRRect(rr,skia.Paint(AntiAlias=True,Color=col(LIME,q)))
        c.restore()
        text(c,lab,540,600,34,NAVY,'black','c',q)
        text(c,sub,540,665,32,WHITE,'semi','c',q)
    # left: KC
    kx=270; ka=1
    team_hex(c,'KC',kx,880,135,ka)
    text(c,'Kansas City',kx,1060,40,WHITE,'black','c',ka)
    text(c,'Chiefs',kx,1108,30,MUTED,'semi','c',ka)
    # VS
    va=seg(t,0.8,1.2)
    pulse=0
    for (gi2,o,g,ts,st) in CARDS:
        if ts<=t<ts+0.3: pulse=1-seg(t,ts,ts+0.3)
    for (gi2,o,g,ts,st) in CARDS:
        bq=seg(t,ts+0.15,ts+0.55)
        if 0<bq<1:
            hexdraw(c,540,880,60+110*eo(bq),stroke=LIME,a=(1-bq)*0.9,lw=6)
    text(c,'VS',540,880,96,LIME,'blacki','c',va,scale=1+0.18*pulse)
    # right: opponent card sliding
    for (gi2,o,g,ts,st) in CARDS:
        te=ts+st if o!=CARDS[-1][1] else 1e9
        if t<ts or t>te+0.25: continue
        ir=seg(t,ts,ts+0.32); inn=eback(ir); out=eio(seg(t,te-0.05,te+0.2))
        x=810+330*(1-inn)-330*out; a=min(min(1,ir*2.5),1-out)
        if 0<ir<1 or 0<out<1:
            sp=(1-ir) if ir<1 else out
            for k,dy in enumerate((-90,-35,30,85)):
                ln=180*sp*(0.6+0.4*((k*37)%5)/4); x1=x+150+ (0 if ir<1 else -480)
                c.drawLine(x1,880+dy,x1+ln,880+dy,skia.Paint(AntiAlias=True,Color=col(AB[o]['p2'],0.7*sp),StrokeWidth=6,StrokeCap=skia.Paint.kRound_Cap))
        team_hex(c,o,x,880,135,a)
        text(c,CITY[o],x,1060,40,WHITE,'black','c',a)
        text(c,NICK[o],x,1108,30,MUTED,'semi','c',a)
        if g==2:
            bx,by=x+105,880-115
            c.drawCircle(bx,by,34*a,skia.Paint(AntiAlias=True,Color=col(LIME,a)))
            text(c,'x2',bx,by,30,NAVY,'black','c',a)
    # 17-slot bar
    bw,gap=46,8; x0=540-(17*bw+16*gap)/2; y0,y1=1210,1268
    filled=[]
    for (gi2,o,g,ts,st) in CARDS:
        for k in range(g): filled.append((ts+0.15+k*0.12,gi2))
    GC=[LIME,WHITE,SKY,LIME]
    for k in range(17):
        x=x0+k*(bw+gap); r=skia.RRect.MakeRectXY(skia.Rect(x,y0,x+bw,y1),10,10)
        c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(MUTED,0.35*seg(t,0.8,1.3)),Style=skia.Paint.kStroke_Style,StrokeWidth=2))
        tf,gi2=filled[k]; a=seg(t,tf,tf+0.2)
        if a>0:
            sc_=0.5+0.5*eback(seg(t,tf,tf+0.3)); cx_=x+bw/2; cy_=(y0+y1)/2
            r=skia.RRect.MakeRectXY(skia.Rect(cx_-bw/2*sc_,cy_-(y1-y0)/2*sc_,cx_+bw/2*sc_,cy_+(y1-y0)/2*sc_),10,10)
            if gi2==3: c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(GC[gi2],a),Style=skia.Paint.kStroke_Style,StrokeWidth=5))
            else: c.drawRRect(r,skia.Paint(AntiAlias=True,Color=col(GC[gi2],a)))
    n=sum(1 for tf,_ in filled if t>=tf)
    tl=max([tf for tf,_ in filled if t>=tf],default=-9)
    bump=1-seg(t,tl,tl+0.25)
    fin=seg(t,MG_END,MG_END+0.4)
    text(c,f'{n} / 17',540,1345,52,LIME if n==17 else WHITE,'black','c',seg(t,0.8,1.3),scale=1+0.18*bump+0.15*eback(fin)*(1-seg(t,MG_END+0.4,MG_END+0.9)))
    text(c,'Las divisiones rivales rotan cada año',540,1420,32,MUTED,'semi','c',seg(t,MG_END,MG_END+0.5))

SCENES=[(s1,3.4),(s2,4.4),(s3,4.2),(s4,5.4),(s5,7.2),(s6,8.4),(s7,8.0),(s5b,14.0),(s_match,16.0)]

def frame(fn,t,D):
    s=skia.Surface(W,H);c=s.getCanvas();c.drawImage(BG,0,0);fn(c,t,D)
    return s.makeImageSnapshot()

if __name__=='__main__':
    mode=sys.argv[1]
    out=sys.argv[2]
    if mode=='still':
        k=int(sys.argv[3]);tt=float(sys.argv[4]);fn,D=SCENES[k]
        frame(fn,tt,D).save(out,skia.kPNG)
    else:
        k=int(mode);fn,D0=SCENES[k];D=float(sys.argv[3]) if len(sys.argv)>3 else D0;n=int(round(D*FPS));sc=D0/D
        tmp=out[:-4]+'.part.mp4'
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),tmp],stdin=subprocess.PIPE)
        for f in range(n):
            WP=os.environ.get('WARP')
            if WP:
                import json as _j, numpy as _np; kn=_j.loads(WP); tn=float(_np.interp(f/FPS,[k[0] for k in kn],[k[1] for k in kn]))
            else: tn=f/FPS*sc
            img=frame(fn,tn,D0)
            p.stdin.write(img.toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        p.stdin.close()
        if p.wait()==0: os.rename(tmp,out)
