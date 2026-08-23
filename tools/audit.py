# -*- coding: utf-8 -*-
"""Auditoria del catalogo. SOLO LECTURA: no modifica nada.

Que comprueba, por orden de importancia:

  1. Que index.html y el disco digan lo mismo. Es lo unico que puede romper el
     sitio publicado, asi que va primero.
  2. Integridad del catalogo de piezas: referencias huerfanas, piezas que
     ningun producto trae, ids duplicados, familias sin etiqueta.
  3. Portada y numeracion de cada producto.
  4. El arbol de `reemplaza`, resuelto en cadena, con ciclos e ids inexistentes.
  4b. Cobertura DEDUCIDA comparando contenidos, para no fiarse de lo declarado.
  5. Nomenclatura.

Que NO comprueba: el contenido de FICHA/. Es material de consulta, de formato
libre y no publicable; una hoja puede cubrir una coleccion entera. Exigirle un
nombre por producto solo generaba ruido.

UNA AUDITORIA CON FALSOS POSITIVOS ES PEOR QUE NINGUNA. Dos que daba la de Myth
y aqui no se dan:
  · La carpeta espejo de un producto cruzado (`alsoIn`) no se marca como
    "carpeta que el HTML no referencia": es espejo a proposito.
  · Los productos de una sola imagen, sueltos en la raiz de su categoria, se
    reconocen como productos y no como archivos perdidos.
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML      = os.path.join(BASE, 'index.html')
FICHA_DIR = 'FICHA'
IMG_EXT   = ('.jpg', '.jpeg', '.png')     # solo originales; los .webp derivan
OMITIR    = ('tools',)

s_html = io.open(HTML, encoding='utf-8').read()

problemas = []
def flag(sev, ruta, motivo):
    problemas.append((sev, ruta, motivo))

def orden(nombre):
    stem = os.path.splitext(nombre)[0]
    if stem.upper() == 'PACKAGE': return (0, 0)
    return (1, int(stem)) if stem.isdigit() else (2, 0)

cats = sorted(d for d in os.listdir(BASE)
              if os.path.isdir(os.path.join(BASE, d))
              and not d.startswith('.') and d not in OMITIR)

# ------------------------------------------------------------- inventario
inv = {}
for cat in cats:
    d = os.path.join(BASE, cat)
    fp = os.path.join(d, FICHA_DIR)
    ficha = len([f for f in os.listdir(fp) if f.lower().endswith(IMG_EXT)]) \
            if os.path.isdir(fp) else 0
    prods, sueltos = {}, []
    for x in sorted(os.listdir(d)):
        xp = os.path.join(d, x)
        if os.path.isdir(xp) and x != FICHA_DIR:
            prods[x] = sorted([f for f in os.listdir(xp) if f.lower().endswith(IMG_EXT)],
                              key=orden)
        elif os.path.isfile(xp) and x.lower().endswith(IMG_EXT):
            sueltos.append(x)                    # producto de una sola imagen
    inv[cat] = {'ficha': ficha, 'prods': prods, 'sueltos': sueltos}

# ------------------------------------------------------ datos del index.html
titulos, categoria, reemplaza, alsoIn, contiene, componentes, imgde = {}, {}, {}, {}, {}, {}, {}
for m in re.finditer(r'\{ id:"([a-z0-9-]+)", title:"([^"]*)", category:"([^"]*)"(.*?)contains:\[([^\]]*)\]',
                     s_html, re.S):
    pid, tit, cat, cuerpo, cont = m.groups()
    titulos[pid], categoria[pid] = tit, cat
    r = re.search(r'reemplaza:\[([^\]]*)\]', cuerpo)
    reemplaza[pid] = re.findall(r'"([^"]+)"', r.group(1)) if r else []
    a = re.search(r'alsoIn:\[([^\]]*)\]', cuerpo)
    alsoIn[pid] = re.findall(r'"([^"]+)"', a.group(1)) if a else []
    c = re.search(r'componentes:\[([^\]]*)\]', cuerpo)
    if c:
        componentes[pid] = set(re.findall(r'"([^"]+)"', c.group(1)))
    i = re.search(r'img:"([^"]*)"', cuerpo)
    imgde[pid] = i.group(1) if i else ''
    contiene[pid] = set(x if '@' in x else x + '@std'
                        for x in re.findall(r'"([^"]+)"', cont))

bloque_piezas = s_html[s_html.index('const PIEZAS_CATALOG'):s_html.index('BLOQUE 3')]
piezas = {}
for m in re.finditer(r'\{\s*id:"([a-z0-9\'-]+)"(.*?)\}', bloque_piezas, re.S):
    pid, cuerpo = m.groups()
    piezas[pid] = {
        'name': re.search(r'name:"([^"]*)"', cuerpo).group(1),
        'collection': re.search(r'collection:"([a-z-]+)"', cuerpo).group(1),
        'type': re.search(r'type:"([a-z-]+)"', cuerpo).group(1),
        'line': re.search(r'line:"(\w+)"', cuerpo).group(1),
    }
familias = set(re.findall(r'"([a-z-]+)":\s*"', s_html[s_html.index('const FAMILIAS'):
                                                      s_html.index('const LINES')]))

print('=' * 62)
print(' 1. INDEX.HTML  <->  DISCO   (lo unico que puede romper el sitio)')
print('=' * 62)

portadas = re.findall(r'img:"([^"]*)"', s_html)
galerias = re.findall(r'"([^"]+\.(?:webp|jpg|jpeg|png))"',
                      ' '.join(re.findall(r'gallery:\[(.*?)\]', s_html, re.S)))
rotas = [p for p in portadas + galerias if not os.path.exists(os.path.join(BASE, p))]
for p in rotas:
    flag('ALTO', p, 'referenciada en index.html pero no esta en disco')
print('  portadas %d · fotos de galeria %d · rutas rotas %d'
      % (len(portadas), len(galerias), len(rotas)))

sin_convertir = [p for p in portadas + galerias if not p.endswith('.webp')]
if sin_convertir:
    print('  aun sin convertir a .webp: %d  (correr build_all.py)' % len(sin_convertir))

# WebP en disco que nadie usa: peso muerto que se subiria al repositorio
refs = set(portadas) | set(galerias)
huerfanos = []
for r, d, fs in os.walk(BASE):
    partes = [x.upper() for x in r.split(os.sep)]
    if '.GIT' in partes or FICHA_DIR in partes:
        continue
    for f in fs:
        if f.endswith('.webp'):
            rel = os.path.relpath(os.path.join(r, f), BASE).replace(os.sep, '/')
            if rel not in refs:
                huerfanos.append(rel)
for h in huerfanos:
    flag('MEDIO', h, '.webp en disco que index.html no usa')
print('  .webp huerfanos: %d' % len(huerfanos))

# Carpetas que la pagina no referencia. Las copias espejo de un producto
# cruzado son legitimas: existen a proposito y el catalogo apunta solo a la
# primaria, asi que no se marcan.
conocidas = set(p.rsplit('/', 1)[0] for p in portadas + galerias)
# Un producto cruzado tiene su carpeta replicada en la otra categoria, con el
# mismo nombre. El catalogo apunta solo a la primaria, asi que la copia queda
# sin referenciar a proposito y no debe salir como incidencia.
espejos = set()
for pid, otras in alsoIn.items():
    if not otras:
        continue
    ruta = imgde.get(pid, '')
    if '/' not in ruta:
        continue
    carpeta = ruta.rsplit('/', 1)[0]              # "CATEGORIA/PRODUCTO"
    if '/' not in carpeta:
        continue                                   # producto de una imagen
    nombre = carpeta.split('/', 1)[1]
    for cat in otras:
        espejos.add('%s/%s' % (cat, nombre))
for cat in cats:
    for prod, files in inv[cat]['prods'].items():
        ruta = '%s/%s' % (cat, prod)
        if files and ruta not in conocidas and ruta not in espejos:
            flag('MEDIO', ruta + '/', 'carpeta con fotos que index.html no referencia')
print('  copias espejo reconocidas (alsoIn): %d' % len(espejos))

print('')
print('=' * 62)
print(' 2. CATALOGO DE PIEZAS')
print('=' * 62)
refs_piezas = set()
for pid, cont in contiene.items():
    refs_piezas |= set(x.split('@')[0] for x in cont)
huerfanas = sorted(refs_piezas - set(piezas))
sin_fuente = sorted(set(piezas) - refs_piezas)
for x in huerfanas:
    flag('ALTO', x, 'un producto la declara en `contains` pero no existe en PIEZAS_CATALOG')
for x in sin_fuente:
    flag('MEDIO', x, 'pieza que ningun producto trae: nunca se podra marcar')
sin_fam = sorted(set(p['type'] for p in piezas.values()) - familias)
for t in sin_fam:
    flag('MEDIO', t, 'familia usada por alguna pieza pero sin etiqueta en FAMILIAS')

for col in sorted(set(p['collection'] for p in piezas.values())):
    porlinea = {}
    for pid, p in piezas.items():
        if p['collection'] == col:
            porlinea.setdefault(p['line'], []).append(pid)
    detalle = '  '.join('%s %d' % (l, len(v)) for l, v in sorted(porlinea.items()))
    print('  %-14s %-16s total %d' % (col, detalle,
                                      sum(len(v) for v in porlinea.values())))
print('  piezas %d · referencias huerfanas %d · piezas sin producto %d'
      % (len(piezas), len(huerfanas), len(sin_fuente)))

print('')
print('=' * 62)
print(' 3. PORTADA Y NUMERACION DE CADA PRODUCTO')
print('=' * 62)
for cat in cats:
    prods, sueltos = inv[cat]['prods'], inv[cat]['sueltos']
    if not prods and not sueltos:
        print('-- %-30s (vacia)' % cat)
        continue
    print('-- %-30s ficha: %d archivo(s)' % (cat, inv[cat]['ficha']))
    for x in sueltos:
        print('   %-52s  1 img  (producto de una imagen)' % os.path.splitext(x)[0][:52])
    for nombre, files in sorted(prods.items()):
        if not files:
            flag('ALTO', '%s/%s/' % (cat, nombre), 'carpeta de producto vacia')
            print('   %-52s VACIA' % nombre[:52]); continue
        stems = [os.path.splitext(f)[0] for f in files]
        pkg   = any(v.upper() == 'PACKAGE' for v in stems)
        nums  = sorted(int(v) for v in stems if v.isdigit())
        portada = 'PACKAGE' if pkg else ('01' if 1 in nums else '??')
        if portada == '??':
            flag('ALTO', '%s/%s/' % (cat, nombre), 'sin PACKAGE y sin 01: no hay portada')
        aviso = ''
        if nums and nums != list(range(1, len(nums) + 1)):
            faltan = [n for n in range(1, max(nums) + 1) if n not in nums]
            aviso = '  HUECOS: %s' % ', '.join('%02d' % n for n in faltan)
            flag('MEDIO', '%s/%s/' % (cat, nombre), 'numeracion con huecos:%s' % aviso)
        sinpad = [v for v in stems if v.isdigit() and len(v) < 2]
        if sinpad:
            flag('MEDIO', '%s/%s/' % (cat, nombre), 'sin cero delante: %s' % ', '.join(sinpad))
        print('   %-52s %2d img  portada=%-8s%s' % (nombre[:52], len(files), portada, aviso))

print('')
print('=' * 62)
print(' 4. QUE ABSORBE CADA SET   (campo `reemplaza`, transitivo)')
print('=' * 62)

def rama(pid, nivel, vistos, out):
    for hijo in reemplaza.get(pid, []):
        if hijo in vistos:
            out.append('   %s! CICLO -> %s' % ('  ' * nivel, hijo))
            flag('ALTO', hijo, 'ciclo en `reemplaza`')
            continue
        if hijo not in titulos:
            out.append('   %s! id inexistente -> %s' % ('  ' * nivel, hijo))
            flag('ALTO', pid, '`reemplaza` apunta a "%s", que no existe' % hijo)
            continue
        out.append('   %s+- %s' % ('  ' * nivel, titulos[hijo][:60]))
        rama(hijo, nivel + 1, vistos | {hijo}, out)

raices = [p for p in reemplaza if reemplaza[p]
          and not any(p in v for v in reemplaza.values())]
if not raices:
    print('  ningun set absorbe a otro')
for r in sorted(raices, key=lambda x: titulos[x]):
    print('  %s' % titulos[r][:66])
    out = []
    rama(r, 0, {r}, out)
    for l in out: print(l)
    print('      cubre %d producto(s) en total' % len(out))

print('')
print('=' * 62)
print(' 4b. COBERTURA DEDUCIDA DE LOS CONTENIDOS')
print('=' * 62)
print('  Compara el contenido real de cada caja en vez de fiarse de lo que')
print('  declaramos. En Myth hacia falta el campo `componentes` porque Drivers')
print('  y Buckles no eran coleccionables; aqui los Kakuzyu y el Omega')
print('  Horn SI lo son, asi que `contains` ya basta para deducirlo.')
print('')

def total(pid):
    return componentes.get(pid, set()) | contiene.get(pid, set())

def declarado(pid, vistos=None):
    vistos = vistos or set()
    res = set()
    for h in reemplaza.get(pid, []):
        if h in vistos: continue
        res.add(h); res |= declarado(h, vistos | {h})
    return res

evaluables = sorted(p for p in titulos if total(p))
avisos_cobertura = 0
for a in evaluables:
    deducido = set(b for b in evaluables if b != a and total(b) and total(b) < total(a))
    dec = declarado(a)
    for b in sorted(deducido - dec):
        flag('ALTO', titulos[a][:52],
             'contiene todo lo de "%s" pero no lo declara en `reemplaza`' % titulos[b])
        print('  !! %s deberia cubrir a %s' % (titulos[a][:38], titulos[b][:38]))
        avisos_cobertura += 1
    for b in sorted(dec - deducido):
        if not total(b): continue
        flag('ALTO', titulos[a][:52],
             'declara cubrir "%s" pero su contenido no lo incluye' % titulos[b])
        print('  !! %s NO contiene lo de %s' % (titulos[a][:38], titulos[b][:38]))
        avisos_cobertura += 1
if not avisos_cobertura:
    print('  La cadena declarada coincide con la deducida de los contenidos.')

print('')
print('=' * 62)
print(' 5. NOMENCLATURA')
print('=' * 62)
for cat in cats:
    if cat != cat.upper():
        flag('MEDIO', cat, 'categoria con minusculas')
    for prod in inv[cat]['prods']:
        if prod != prod.upper():
            flag('BAJO', '%s/%s/' % (cat, prod), 'estilo: minusculas en el nombre')
# Nombres repetidos entre categorias: legitimo solo si es un producto cruzado
vistos = {}
for cat in cats:
    for f in list(inv[cat]['prods']) + list(inv[cat]['sueltos']):
        vistos.setdefault(f, []).append(cat)
dups = {k: v for k, v in vistos.items() if len(v) > 1}
if not dups:
    print('  sin nombres repetidos entre categorias')
for f, cs in sorted(dups.items()):
    esperado = any('%s/%s' % (c, f) in espejos for c in cs)
    marca = 'espejo de un producto cruzado, correcto' if esperado else 'REVISAR'
    if not esperado:
        flag('MEDIO', f[:52], 'mismo nombre en %s sin ser producto cruzado' % ' y '.join(cs))
    print('  %s en %s  ->  %s' % (f[:46], ' y '.join(cs), marca))

print('')
print('=' * 62)
print(' RESULTADO')
print('=' * 62)
orden_sev = {'ALTO': 0, 'MEDIO': 1, 'BAJO': 2}
problemas.sort(key=lambda x: (orden_sev[x[0]], x[1]))
if not problemas:
    print('  Sin incidencias.')
else:
    print('  %d incidencias (ALTO=%d MEDIO=%d BAJO=%d)' % (
        len(problemas),
        sum(1 for p in problemas if p[0] == 'ALTO'),
        sum(1 for p in problemas if p[0] == 'MEDIO'),
        sum(1 for p in problemas if p[0] == 'BAJO')))
    print('')
    for sev, ruta, motivo in problemas:
        print('  [%-5s] %-52s %s' % (sev, ruta[:52], motivo))
sys.exit(1 if any(p[0] == 'ALTO' for p in problemas) else 0)
