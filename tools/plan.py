# -*- coding: utf-8 -*-
"""Construye el plan de imagenes: portada + galeria de cada producto.

SOLO LECTURA. Correr esto antes de build_all para ver que saldria.

Portada = PACKAGE si existe, si no 01.

Dos clases de producto:
  · CARPETA  -> producto con subcarpeta propia y varias fotos numeradas.
  · SUELTO   -> producto de una sola imagen, en la raiz de su categoria.
                (En Myth estos NO pasaban por las herramientas y sus .webp se
                generaban a mano. Aqui van incluidos.)

Un producto cruzado (`alsoIn`) tiene carpeta espejo en la otra categoria, pero
se lista SOLO por su categoria primaria: la copia espejo no recibe .webp, igual
que en Myth con el Ridewatter.
"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, 'index.html')

# id de PRODUCTS -> carpeta relativa
CARPETA = {
 'dx-omegahorn':            'DX SETS/DX OMEGAHORN',
 'dx-omegaanalyzer':        'DX SETS/DX OMEGAANALYZER',
 'dx-enkaku-set':           'DX SETS/DX MEGA FLAME HORN ENKAKU＆OMEGAHORN SET',
 'dx-enkaku-egolgear-set':  'DX SETS/DX MEGA FLAME HORN ENKAKU＆OMEGAHORN EGOLGEAR SET',
 # Cruzado: tambien tiene carpeta en DX MECHAS, pero sale por DX SETS.
 'dx-zetsu-enkaku-set':     'DX SETS/DX MEGA FLAME HORN ZETSU-ENKAKU ＆ OMEGAHORN ZETSU SET',
 'dx-replica-set':          'DX SETS/OMEGAHORN REPLICA ＆ EGOLGEAR SET',

 'dx-mecha-enkaku':         'DX MECHAS/DX MEGA FLAME HORN ENKAKU',
 'dx-mecha-zankaku':        'DX MECHAS/DX MEGA SLASH HORN ZANKAKU',
 'dx-mecha-goukaku':        'DX MECHAS/DX MEGA BRAVE HORN GOKAKU',
 'dx-mecha-saikaku':        'DX MECHAS/DX MEGA CRUSH HORN SAIKAKU',
 'dx-mecha-hikaku':         'DX MECHAS/DX MEGA WING HORN HIKAKU',

 'dx-egolgear-set-01':      'DX EGOLGEAR SETS/DX EGOLGEAR SET 01',
 'dx-egolgear-set-02':      'DX EGOLGEAR SETS/DX EGOLGEAR SET 02',
 'dx-egolgear-set-03':      'DX EGOLGEAR SETS/DX EGOLGEAR SET 03',
 'dx-egolgear-set-04':      'DX EGOLGEAR SETS/DX EGOLGEAR SET 04',
 'dx-egolgear-set-05':      'DX EGOLGEAR SETS/DX EGOLGEAR SET 05',
 'dx-egolgear-set-06':      'DX EGOLGEAR SETS/DX EGOLGEAR SET 06',

 'sg-random-box-01':        'SG RANDOM BOX/SG EGOLGEAR RANDOM BOX 01',
 'sg-minipla-set':          'SG MINIPLA/MINIPLA KAKUSEIHUNTER OMEGAHORN 01 SET',
 'sg-yudo-enkaku':          'SG YU-DO/YU-DO KAKUSEIHUNTER OMEGAHORN 01 ENKAKU',
 'sg-yudo-omegahorn':       'SG YU-DO/YU-DO KAKUSEIHUNTER OMEGAHORN 01 OMEGAHORN',
 'sg-yudo-captain':         'SG YU-DO/YU-DO KAKUSEIHUNTER OMEGAHORN 01 CAPTAIN OMEGAHORN',

 'sv-enkaku':               'SOFTVINYL/SOFT VINYL KAKUZYU ENKAKU',
 'taf-captain':             'TAF/TAF CAPTAIN OMEGAHORN',
}

# id -> archivo suelto (producto de una sola imagen, sin subcarpeta)
SUELTO = {
 'promo-special-color':
   'EGOLGEAR PROMOCIONALES/PROJECT RED CHOCO CAMPAIGN-EgolGear Limited Special Color.png',
}

IMG_EXT = ('.jpg', '.jpeg', '.png')


def orden(nombre):
    """PACKAGE primero, luego 01, 02, 03..."""
    stem = os.path.splitext(nombre)[0]
    if stem.upper() == 'PACKAGE':
        return (0, 0)
    return (1, int(stem)) if stem.isdigit() else (2, 0)


def plan():
    """[(pid, ruta, portada, [archivos], es_suelto, error)]

    Para un producto suelto, `ruta` es el archivo y `portada` su nombre.
    """
    filas = []
    for pid, carpeta in sorted(CARPETA.items()):
        full = os.path.join(BASE, carpeta)
        if not os.path.isdir(full):
            filas.append((pid, carpeta, None, [], False, 'CARPETA NO EXISTE'))
            continue
        # Solo originales: los .webp son derivados y contarlos duplicaria cada
        # numero, ademas de arrastrar el -thumb de la portada.
        files = [f for f in os.listdir(full) if f.lower().endswith(IMG_EXT)]
        if not files:
            filas.append((pid, carpeta, None, [], False, 'VACIA'))
            continue
        files.sort(key=orden)
        filas.append((pid, carpeta, files[0], files, False, ''))

    for pid, ruta in sorted(SUELTO.items()):
        full = os.path.join(BASE, ruta)
        if not os.path.isfile(full):
            filas.append((pid, ruta, None, [], True, 'ARCHIVO NO EXISTE'))
            continue
        filas.append((pid, ruta, os.path.basename(ruta), [os.path.basename(ruta)], True, ''))

    return filas


if __name__ == '__main__':
    filas = plan()
    print('%-24s %-50s %-11s %s' % ('PRODUCTO', 'RUTA', 'PORTADA', 'GALERIA'))
    print('-' * 108)
    pkg = uno = total = 0
    peso = 0
    for pid, ruta, portada, files, suelto, err in filas:
        if err:
            print('%-24s %-50s  !! %s' % (pid, ruta[:50], err))
            continue
        if portada.upper().startswith('PACKAGE'):
            pkg += 1
        else:
            uno += 1
        total += len(files)
        base = os.path.dirname(ruta) if suelto else ruta
        peso += os.path.getsize(os.path.join(BASE, base, portada))
        etiqueta = ' (suelto)' if suelto else ''
        print('%-24s %-50s %-11s %d img%s'
              % (pid, ruta[:50], portada[:11], len(files), etiqueta))
    print('-' * 108)
    print('%d productos   portada PACKAGE: %d   portada 01/suelto: %d   imagenes: %d'
          % (len(filas), pkg, uno, total))
    print('Peso de las %d portadas hoy: %.1f MB  ->  se convertiran a WebP'
          % (len(filas), peso / 1048576.0))
