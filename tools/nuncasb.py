import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import *
sys.argv=sys.argv_saved
R=[('BUF','Bills',4),('MIN','Vikings',4),('CIN','Bengals',3),('ATL','Falcons',2),('CAR','Panthers',2),('ARI','Cardinals',1),('LAC','Chargers',1),('TEN','Titans',1),
   ('CLE','Browns',0),('DET','Lions',0),('HOU','Texans',0),('JAX','Jaguars',0)]
s,c=bg(); top(c)
text(c,'LOS QUE NUNCA',540,215,80,WHITE,'blacki','c')
text(c,'LO HAN GANADO',540,305,104,LIME,'blacki','c')
text(c,'12 equipos sin Super Bowl · cuántas finales han perdido',540,385,31,MUTED,'semi','c')
for i,(ab,nm,n) in enumerate(R):
    y=455+i*64
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60,y-27,1020,y+27),15,15),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.9 if i%2==0 else 0.6)))
    thex(c,ab,115,y,23); text(c,nm,160,y,30,WHITE,'black','l')
    if n:
        for k in range(n): trophy(c,520+k*56,y+4,0.145,0.38)
        text(c,str(n),945,y-4,38,LIME,'blacki','r'); text(c,'finales' if n>1 else 'final',1000,y+2,18,MUTED,'semi','r')
    else:
        chip(c,'NUNCA HA LLEGADO',820,y,20,WHITE,NAVY)
text(c,'Datos hasta el Super Bowl LX (feb. 2026)',540,1245,24,MUTED,'semi','c')
text(c,'¿Quién lo gana primero? Comenta',540,1295,34,WHITE,'black','c')
save(s,'top_nunca_ganado')
