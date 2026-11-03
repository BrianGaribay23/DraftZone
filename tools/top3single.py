import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import bg, top, chip, save, thex, PW, PH
from render import *
sys.argv=sys.argv_saved
NM={'BUF':'Buffalo','MIN':'Minnesota','CIN':'Cincinnati','ATL':'Atlanta','GB':'Green Bay','NE':'N. Inglaterra'}
G=[('BUF','MIN',('LUNES 9 NOV','7:15 PM CDMX'),'LUNES POR LA NOCHE','Dos de los mejores récords'),
   ('CIN','ATL',('DOMINGO 8 NOV','8:30 AM CDMX'),'EN MADRID','En el Santiago Bernabéu'),
   ('GB','NE',('DOMINGO 8 NOV','3:25 PM CDMX'),'DUELO DE LA TARDE','Dos récords ganadores')]
s,c=bg(); top(c)
text(c,'TOP 3',300,250,130,LIME,'blacki','c')
text(c,'PARTIDOS',700,215,62,WHITE,'blacki','c'); text(c,'SEMANA 9',700,285,62,WHITE,'blacki','c')
text(c,'Horarios de la Ciudad de México (CDMX)',540,365,32,MUTED,'semi','c')
for i,(a,h,when,tag,why) in enumerate(G):
    y0=420+i*255; y1=y0+225
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60,y0,1020,y1),32,32),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.9)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60,y0,1020,y1),32,32),skia.Paint(AntiAlias=True,Color=col(LIME,0.5),Style=skia.Paint.kStroke_Style,StrokeWidth=3))
    cy=y0+95
    text(c,f'#{i+1}',125,cy,64,LIME,'blacki','c')
    thex(c,a,265,cy,60); text(c,'@',395,cy,50,LIME,'blacki','c'); thex(c,h,525,cy,60)
    text(c,NM[a],265,cy+90,26,WHITE,'black','c'); text(c,NM[h],525,cy+90,26,WHITE,'black','c')
    chip(c,tag,815,y0+50,24,WHITE,NAVY)
    text(c,when[0],815,y0+100,28,WHITE,'black','c')
    text(c,when[1],815,y0+145,36,LIME,'black','c')
    text(c,why,815,y0+190,24,MUTED,'semi','c')
text(c,'¿Cuál vas a ver? Comenta 1, 2 o 3',540,1215,40,WHITE,'black','c')
text(c,'¿Ya tienes tu jersey? · Link en bio',540,1280,32,LIME,'xb','c')
save(s,'top3_semana9')
