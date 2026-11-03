import sys
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
from posts import *
sys.argv=sys.argv_saved
from PIL import Image, ImageFilter
src=Image.open('/mnt/user-data/attachments/076d352e-6e33-5981-bbd2-d7b232361ec5/269acdf3-image.png').convert('RGB')
src=src.crop((0,90,1086,1448)).resize((1080,1350),Image.LANCZOS)
# suavizar texto ilegible del mural
from PIL import ImageDraw
m=Image.new('L',src.size,0); ImageDraw.Draw(m).ellipse((170,10,410,230),fill=255); m=m.filter(ImageFilter.GaussianBlur(35))
src=Image.composite(src.filter(ImageFilter.GaussianBlur(10)),src,m)
src.save('/tmp/claude-0/sched/_base.png')
s=skia.Surface(PW,PH); c=s.getCanvas()
c.drawImage(skia.Image.open('/tmp/claude-0/sched/_base.png'),0,0)
c.drawRect(skia.Rect(0,0,PW,330),skia.Paint(Shader=skia.GradientShader.MakeLinear([(0,0),(0,330)],[col(NAVY,0.85),col(NAVY,0)])))
c.drawRect(skia.Rect(0,PH-430,PW,PH),skia.Paint(Shader=skia.GradientShader.MakeLinear([(0,PH-430),(0,PH)],[col(NAVY,0),col(NAVY,0.95)])))
top(c)
text(c,'LLEVA TU EQUIPO',540,PH-215,74,WHITE,'blacki','c')
text(c,'A LA CALLE',540,PH-140,92,LIME,'blacki','c')
text(c,'Jersey Buffalo · Allen #17  ·  Link en bio',540,PH-65,30,WHITE,'xb','c')
save(s,'post_jersey_allen')
