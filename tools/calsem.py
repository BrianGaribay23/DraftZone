import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import *
sys.argv=sys.argv_saved
CITY={'JAX':'Jacksonville','BAL':'Baltimore','CIN':'Cincinnati','ATL':'Atlanta','CLE':'Cleveland','NO':'Nueva Orleans','DAL':'Dallas','IND':'Indianápolis',
 'DEN':'Denver','CAR':'Carolina','DET':'Detroit','MIA':'Miami','LAR':'LA Rams','WAS':'Washington','NYG':'NY Giants','PHI':'Filadelfia',
 'NYJ':'NY Jets','KC':'Kansas City','HOU':'Houston','LAC':'LA Chargers','ARI':'Arizona','SEA':'Seattle','GB':'Green Bay','NE':'N. Inglaterra',
 'LV':'Las Vegas','SF':'San Francisco','TB':'Tampa Bay','CHI':'Chicago','BUF':'Buffalo','MIN':'Minnesota','PIT':'Pittsburgh','TEN':'Tennessee'}
M='12:00 PM'
W={
10:([('JUEVES 12 NOV',[('WAS','NYG','7:15 PM','')]),
     ('DOMINGO 15 NOV',[('NE','DET','8:30 AM','MÚNICH'),('CAR','NO',M,''),('BUF','NYJ',M,''),('HOU','CLE',M,''),('JAX','TEN',M,''),('KC','ATL',M,''),('MIA','IND',M,''),('MIN','GB',M,''),
                        ('LAR','ARI','3:05 PM',''),('SEA','LV','3:05 PM',''),('SF','DAL','3:25 PM',''),('PIT','CIN','7:20 PM','')]),
     ('LUNES 16 NOV',[('LAC','BAL','7:15 PM','')])],'Descansan: Chicago, Denver, Filadelfia y Tampa Bay','¿Ya tienes tu jersey para el domingo? · Link en bio'),
11:([('JUEVES 19 NOV',[('IND','HOU','7:15 PM','')]),
     ('DOMINGO 22 NOV',[('BAL','CAR',M,''),('ARI','KC',M,''),('JAX','NYG',M,''),('MIA','BUF',M,''),('NO','CHI',M,''),('TB','DET',M,''),('TEN','DAL',M,''),
                        ('NYJ','LAC','3:05 PM',''),('LV','DEN','3:25 PM',''),('PIT','PHI','3:25 PM',''),('MIN','SF','7:20 PM','EN CDMX')]),
     ('LUNES 23 NOV',[('CIN','WAS','7:15 PM','')])],'Descansan: Atlanta, Cleveland, Green Bay, LA Rams, N. Inglaterra y Seattle','¿Vas al Estadio Banorte? Llega con tu jersey · Link en bio'),
12:([('MIÉRCOLES 25 NOV',[('GB','LAR','7:00 PM','')]),
     ('JUEVES 26 NOV · ACCIÓN DE GRACIAS',[('CHI','DET',M,''),('PHI','DAL','3:30 PM',''),('KC','BUF','7:20 PM','')]),
     ('VIERNES 27 NOV',[('DEN','PIT','2:00 PM','')]),
     ('DOMINGO 29 NOV',[('BAL','HOU',M,''),('ATL','MIN',M,''),('LV','CLE',M,''),('NO','CIN',M,''),('NYG','IND',M,''),('NYJ','MIA',M,''),
                        ('TEN','JAX','3:05 PM',''),('SEA','SF','3:25 PM',''),('WAS','ARI','3:25 PM',''),('NE','LAC','7:20 PM','')]),
     ('LUNES 30 NOV',[('CAR','TB','7:15 PM','')])],'Esta semana juegan los 32 equipos','¿Ya tienes tu jersey para Acción de Gracias? · Link en bio'),
}
for wk,(days,foot,cta) in W.items():
    s,c=bg(); top(c)
    text(c,f'SEMANA {wk}',540,200,96,WHITE,'blacki','c')
    chip(c,'HORARIOS CDMX',540,280,32,LIME,NAVY)
    ng=sum(len(g) for _,g in days); nd=len(days)
    HD,GAP=40,10
    rh=min(50,(1215-340-nd*(HD+GAP))/ng); k=rh/50
    y=340
    for day,games in days:
        text(c,day,90,y,28*min(1,k*1.05),LIME,'black','l'); y+=HD*min(1,k*1.05)+4
        for a,h,hr,tag in games:
            hh=rh*0.46
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(70,y-hh,1010,y+hh),12,12),skia.Paint(AntiAlias=True,Color=col(NAVY2,0.85)))
            r=19*k; fs=25*k
            thex(c,a,105,y,r); text(c,CITY[a],135,y,fs,WHITE,'black','l')
            text(c,'@',400,y,fs,MUTED,'black','c')
            thex(c,h,440,y,r); text(c,CITY[h],470,y,fs,WHITE,'black','l')
            if tag: chip(c,tag,790,y,20*k,LIME if 'CDMX' in tag else WHITE,NAVY)
            text(c,hr,990,y,27*k,WHITE,'black','r')
            y+=rh
        y+=GAP
    text(c,foot,540,y+6,25,MUTED,'semi','c')
    text(c,cta,540,PH-55,30,LIME,'xb','c')
    save(s,f'calendario_semana{wk}')
    print(wk,ng,round(rh,1),round(y))
