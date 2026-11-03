import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import bg, top, chip, save, thex, PW, PH
from render import *
sys.argv=sys.argv_saved
R=[(1,'NE','Patriots',6),(2,'DEN','Broncos',5),(3,'BUF','Bills',4),(3,'MIN','Vikings',4),
   (5,'SF','49ers',3),(5,'CIN','Bengals',3),(5,'PHI','Eagles',3),(5,'LAR','Rams',3),(5,'MIA','Dolphins',3),(5,'DAL','Cowboys',3),(5,'KC','Chiefs',3)]
s,c=bg(); top(c)
text(c,'LOS QUE MÁS',540,215,80,WHITE,'blacki','c')
text(c,'HAN PERDIDO',540,305,104,LIME,'blacki','c')
text(c,'Equipos con más Super Bowls perdidos en la historia',540,385,32,MUTED,'semi','c')
for i,(rk,ab,nm,n) in enumerate(R):
    y=460+i*68
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60,y-29,1020,y+29),16,16),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.9 if i%2==0 else 0.6)))
    text(c,str(rk),110,y,34,LIME if rk==1 else WHITE,'blacki','c')
    thex(c,ab,180,y,24); text(c,nm,225,y,31,WHITE,'black','l')
    for k in range(n): trophy(c,560+k*58,y+4,0.155,0.38)
    text(c,str(n),995,y,40,LIME,'blacki','r')
text(c,'Actualizado después del Super Bowl LX (feb. 2026)',540,1240,26,MUTED,'semi','c')
text(c,'¿A quién le duele más? Comenta',540,1292,34,WHITE,'black','c')
save(s,'top_sb_perdidos')
