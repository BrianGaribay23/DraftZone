import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import *
sys.argv=sys.argv_saved
NM={'BUF':'Buffalo','NE':'N. Inglaterra','NYJ':'NY Jets','MIA':'Miami','PIT':'Pittsburgh','CIN':'Cincinnati','CLE':'Cleveland','BAL':'Baltimore',
'JAX':'Jacksonville','HOU':'Houston','IND':'Indianápolis','TEN':'Tennessee','DEN':'Denver','KC':'Kansas City','LV':'Las Vegas','LAC':'LA Chargers',
'NYG':'NY Giants','DAL':'Dallas','WAS':'Washington','PHI':'Filadelfia','MIN':'Minnesota','CHI':'Chicago','DET':'Detroit','GB':'Green Bay',
'CAR':'Carolina','TB':'Tampa Bay','ATL':'Atlanta','NO':'Nueva Orleans','SF':'San Francisco','SEA':'Seattle','LAR':'LA Rams','ARI':'Arizona'}
WK=8
D={'AFC':[('ESTE',[('BUF','6-1'),('NE','5-3'),('NYJ','2-6'),('MIA','1-6')]),('NORTE',[('PIT','6-2'),('CIN','5-2'),('CLE','5-3'),('BAL','4-4')]),
          ('SUR',[('JAX','5-2'),('HOU','2-5'),('IND','2-6'),('TEN','1-7')]),('OESTE',[('DEN','6-2'),('KC','5-2'),('LV','4-4'),('LAC','0-7')])],
   'NFC':[('ESTE',[('NYG','4-2-1'),('DAL','3-5'),('WAS','2-4-1'),('PHI','2-6')]),('NORTE',[('MIN','6-1'),('CHI','6-2'),('DET','5-2'),('GB','5-3')]),
          ('SUR',[('CAR','3-4'),('TB','3-5'),('ATL','3-5'),('NO','2-5')]),('OESTE',[('SF','6-1'),('SEA','4-4'),('LAR','4-4'),('ARI','3-5')])]}
for k,(conf,divs) in enumerate(D.items()):
    s,c=bg(); top(c,k+1,2)
    text(c,'ASÍ VAN',380,225,104,WHITE,'blacki','c'); text(c,conf,800,225,104,LIME,'blacki','c')
    text(c,f'Posiciones por división · después de la semana {WK}',540,320,30,MUTED,'semi','c')
    for i,(dn,teams) in enumerate(divs):
        x0=60 if i%2==0 else 555; y0=385+(i//2)*445; w=465
        text(c,f'{conf} {dn}',x0+8,y0,30,LIME,'black','l')
        for j,(ab,rec) in enumerate(teams):
            y=y0+62+j*88
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0,y-38,x0+w,y+38),16,16),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.95 if j==0 else 0.7)))
            if j==0: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0,y-38,x0+w,y+38),16,16),skia.Paint(AntiAlias=True,Color=col(LIME,0.6),Style=skia.Paint.kStroke_Style,StrokeWidth=3))
            thex(c,ab,x0+48,y,28)
            text(c,NM[ab],x0+92,y,27,WHITE,'black','l')
            text(c,rec,x0+w-22,y,32,LIME if j==0 else WHITE,'blacki','r')
    text(c,'¿Quién gana tu división? Comenta 👇'.replace(' 👇',''),540,1270,34,WHITE,'black','c')
    save(s,f'asivan_{conf.lower()}_semana{WK}')
