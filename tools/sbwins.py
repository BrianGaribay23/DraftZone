import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import bg, top, chip, save, thex, PW, PH
from render import *
sys.argv=sys.argv_saved
R=[(1,'NE','Patriots',6),(1,'PIT','Steelers',6),(3,'SF','49ers',5),(3,'DAL','Cowboys',5),(5,'GB','Packers',4),(5,'NYG','Giants',4),(5,'KC','Chiefs',4),
   (8,'DEN','Broncos',3),(8,'LV','Raiders',3),(8,'WAS','Commanders',3)]
s,c=bg(); top(c)
text(c,'LOS MÁS',540,215,84,WHITE,'blacki','c')
text(c,'GANADORES',540,305,110,LIME,'blacki','c')
text(c,'Equipos con más Super Bowls en la historia',540,385,34,MUTED,'semi','c')
for i,(rk,ab,nm,n) in enumerate(R):
    y=470+i*76
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60,y-32,1020,y+32),18,18),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.9 if i%2==0 else 0.6)))
    text(c,str(rk),110,y,38,LIME if rk==1 else WHITE,'blacki','c')
    thex(c,ab,180,y,26); text(c,nm,225,y,34,WHITE,'black','l')
    for k in range(n): trophy(c,560+k*58,y+4,0.17,1)
    text(c,str(n),995,y,44,LIME,'blacki','r')
text(c,'Actualizado después del Super Bowl LX (feb. 2026)',540,1255,26,MUTED,'semi','c')
text(c,'¿Tu equipo está en la lista? Comenta 👇'.replace(' 👇',''),540,1305,34,WHITE,'black','c')
save(s,'top_superbowls')
