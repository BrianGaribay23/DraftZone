import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import bg, top, chip, save, thex, PW, PH
from render import *
sys.argv=sys.argv_saved
R=[('NYJ','Jets',57,'SB III','1969'),('MIA','Dolphins',52,'SB VIII','1974'),('LV','Raiders',42,'SB XVIII','1984'),
   ('CHI','Bears',40,'SB XX','1986'),('WAS','Commanders',34,'SB XXVI','1992'),('SF','49ers',31,'SB XXIX','1995'),
   ('DAL','Cowboys',30,'SB XXX','1996'),('IND','Colts',19,'SB XLI','2007'),('PIT','Steelers',17,'SB XLIII','2009'),('NO','Saints',16,'SB XLIV','2010')]
s,c=bg(); top(c)
text(c,'LAS SEQUÍAS',540,215,84,WHITE,'blacki','c')
text(c,'MÁS LARGAS',540,305,110,LIME,'blacki','c')
text(c,'Años desde su último Super Bowl ganado',540,385,32,MUTED,'semi','c')
BX0,BX1=470,850
for i,(ab,nm,n,sb,yr) in enumerate(R):
    y=465+i*74
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60,y-31,1020,y+31),16,16),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.9 if i%2==0 else 0.6)))
    text(c,str(i+1),105,y,34,LIME if i==0 else WHITE,'blacki','c')
    thex(c,ab,170,y,24)
    text(c,nm,212,y-11,30,WHITE,'black','l')
    text(c,f'Último: {sb} ({yr})',212,y+17,19,MUTED,'semi','l')
    w=(BX1-BX0)*n/57
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(BX0,y-9,BX1,y+9),9,9),skia.Paint(AntiAlias=True,Color=col(WHITE,0.08)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(BX0,y-9,BX0+w,y+9),9,9),skia.Paint(AntiAlias=True,Color=col(LIME,1.0 if i==0 else 0.75)))
    text(c,str(n),960,y-6,40,LIME,'blacki','r'); text(c,'años',1003,y+4,20,MUTED,'semi','r')
text(c,'Y 12 equipos nunca lo han ganado. Datos hasta el Super Bowl LX (feb. 2026)',540,1245,23,MUTED,'semi','c')
text(c,'¿Qué sequía termina primero? Comenta',540,1295,34,WHITE,'black','c')
save(s,'top_sequias')
