# DraftZone — Guía de estilo de posts

Referencia para que todas las imágenes de Instagram/Facebook se vean iguales. Antes de hacer un post nuevo, seguir esto.

## 1. Formato
- **Tamaño:** 1080 × 1350 px (4:5, feed). Historias aparte: 1080 × 1920 (9:16). Nunca subir 9:16 al feed (Instagram recorta logo y CTA).
- **Archivo:** PNG. Nombre: `tipo_semanaN.png` o `top_tema.png` (ej. `calendario_semana10.png`, `top3_semana11.png`, `top_sequias.png`).
- **Ubicación:** carpeta `posts/` del repo DraftZone (GitHub) → link público `https://raw.githubusercontent.com/BrianGaribay23/DraftZone/main/posts/<archivo>` → Metricool.

## 2. Colores
| Uso | Color | HEX |
|---|---|---|
| Fondo (degradado vertical) | Azul marino | #0F2348 → #060F21 |
| Marca / fondo base | Navy DraftZone | #0B1B3A |
| Tarjetas / filas | Navy claro | #14284E (90% / 60% alternado) |
| Acento, números, CTA | Lima DraftZone | #C6FF1A |
| Texto principal | Blanco | #FFFFFF |
| Texto secundario, notas | Azul gris | #96ACCD |

- Fondo: degradado + líneas horizontales tenues (blanco 5%) + halo lima muy suave al centro.
- Chips (etiquetas tipo "EN MÚNICH"): píldora blanca con texto navy. La única chip lima es **"EN CDMX"** (para destacar México).

## 3. Tipografía (Inter Display)
- **Títulos:** Black Italic, MAYÚSCULAS. Línea 1 en blanco, línea 2 en lima y más grande (ej. "LOS MÁS" / "GANADORES").
- **Nombres de equipo y horarios:** Black.
- **Subtítulos y notas:** SemiBold en azul gris.
- **CTA:** ExtraBold en lima.

## 4. Estructura fija
1. Logo horizontal DraftZone arriba a la izquierda (sin escudo de la NFL mientras la licencia esté pendiente).
2. Título en 2 líneas (blanco + lima) o título de semana ("SEMANA 10" + chip "HORARIOS CDMX").
3. Subtítulo en azul gris que explique el dato.
4. Contenido en filas/tarjetas redondeadas.
5. Nota de fuente/fecha en azul gris ("Datos hasta el Super Bowl LX (feb. 2026)").
6. Pregunta para comentar en blanco + CTA en lima.

## 5. Tipos de post y calendario semanal
| Día | Hora CDMX | Post | Detalle |
|---|---|---|---|
| Martes | 7:00 PM | Calendario de la semana | Todos los partidos, agrupados por día, horario CDMX, descansos abajo |
| Jueves | 12:00 PM | Top 3 partidos | Tarjetas #1–#3, chip con contexto, fecha y hora CDMX, motivo corto |
| Sábado | 1:00 PM | Top histórico | Ranking de 10–12 equipos con iconos y número grande a la derecha |

### Reglas por tipo
- **Calendario:** formato "Visitante @ Local". Nombres de ciudad en español (Nueva Orleans, Filadelfia, Indianápolis, N. Inglaterra, NY Giants/Jets, LA Rams/Chargers). Chip blanca para sede internacional ("MÚNICH", "MADRID"); chip lima "EN CDMX".
- **Top 3:** sin récords en la imagen (cambian cada semana). Motivos atemporales: rivalidad divisional, horario estelar, sede, festivo.
- **Tops históricos:** ganadores → trofeos de pie; perdidos / nunca han ganado → **trofeos tirados**. El número de trofeos tiene que coincidir con el número. "NUNCA HA LLEGADO" como chip blanca.

## 6. Textos
- Español de México, informal.
- Horarios siempre en **CDMX** (EE.UU. horario de invierno: ET − 1 h; horario de verano: ET − 2 h).
- CTA estándar: **"¿Ya tienes tu jersey para el partido? · Link en bio"**. Variantes de temporada: "para Acción de Gracias", "¿Vas al Estadio Banorte? Llega con tu jersey".
- Pregunta para comentar: "¿Cuál vas a ver? Comenta 1, 2 o 3", "¿Tu equipo está en la lista? Comenta", etc.
- Caption: 1–2 frases + pregunta + máximo **5 hashtags** (#NFL #NFLenEspañol #FutbolAmericano #NFLMexico #DraftZone o variantes).

## 7. Validación (obligatorio)
- Cada dato de una imagen se valida contra **al menos 2 fuentes**. Si no coinciden, se busca una tercera y se avisa.
- Calendarios: revalidar el lunes antes de publicar (la NFL puede mover horarios por "flex").
- Si una imagen editada con otra herramienta (logos) cambia números, se compara contra los datos validados antes de usarla.
- Cuando todo está bien, la respuesta es solo: **"validado"**.

## 8. Logos
- Claude genera la versión con siglas en hexágono con colores de cada equipo.
- Brian agrega logos de equipos con su herramienta y revisa que no cambien datos.
- Escudo de la NFL: evitar mientras la licencia esté pendiente.

## 9. Herramientas
- Scripts en `tools/` del repo (Python + skia-python, fuente Inter Display):
  - `posts.py` (fondo, header, chips, hexágonos de equipo) y `render.py` (colores, textos, trofeos).
  - `calsem.py` calendarios · `top3gen.py` Top 3 · `sbwins.py`, `sblosses.py`, `sequias.py`, `nuncasb.py` tops históricos.
- Flujo: imagen → `posts/` → commit + push → Metricool (Instagram + Facebook, publicación automática).
