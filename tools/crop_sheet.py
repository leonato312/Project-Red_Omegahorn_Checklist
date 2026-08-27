# -*- coding: utf-8 -*-
"""Recorta una hoja de despiece en paneles individuales.

Bandai suele publicar el listado de una caja sorpresa o de un model kit como
UNA sola imagen con los N contenidos en rejilla (los "①②③..." de las cajas
SG, o el cuadro de セット内容 de un EGOLGEAR SET). Este script la parte en
archivos numerados para usarlos como portada o galería de cada producto.

Se usó a mano, con este mismo procedimiento, para:
  - SG YU-DO: la hoja de 6 cajas (480589.jpg) partida en 6 paneles de 2x3.
  - SG YU-DO: la hoja de 4 fotos (480309.jpg) partida en 3, descartando el
    cuadrante de la caja.
  - SG MINIPLA: idem.

DOS MODOS:

  detect   Solo lectura. Imprime las bandas de fila/columna que son "gutter"
           (pasillo limpio, sin tinta) y las que son "borde" (línea oscura de
           rejilla). Sirve para decidir a ojo por dónde cortar: no hay que
           adivinar coordenadas a mano en un editor de imagenes.

  crop     Corta de verdad. Recibe las coordenadas X e Y donde va cada corte
           (los límites internos, no los bordes de la imagen) y genera un
           panel por cada celda de la rejilla resultante, en orden de
           lectura (izquierda a derecha, arriba a abajo). Con --skip se
           descartan celdas (por índice, 0-based) — para cuando la hoja
           mezcla el producto con una foto de la caja que no se quiere.

Nunca escribe sobre el origen ni sobre `FICHA/`.

Ejemplos:

  python tools/crop_sheet.py detect "SG YU-DO/FICHA/hoja.jpg"

  python tools/crop_sheet.py crop "SG YU-DO/FICHA/hoja.jpg" \\
      --x 602 --y 707 \\
      --out "SG YU-DO/YU-DO KAKUSEIHUNTER OMEGAHORN 01 ENKAKU" \\
      --start 2

  python tools/crop_sheet.py crop "SG YU-DO/FICHA/hoja2.jpg" \\
      --x 699 --y 707 --skip 3 \\
      --out "SG YU-DO/YU-DO KAKUSEIHUNTER OMEGAHORN 01 ENKAKU" --start 1
"""
import argparse
import os
from PIL import Image


def bandas_limpias(valores, umbral, minimo_ancho=3):
    """Agrupa índices consecutivos por debajo de `umbral` en (inicio, fin)."""
    grupos, actual = [], []
    for i, v in enumerate(valores):
        if v < umbral:
            actual.append(i)
        else:
            if len(actual) >= minimo_ancho:
                grupos.append((actual[0], actual[-1]))
            actual = []
    if len(actual) >= minimo_ancho:
        grupos.append((actual[0], actual[-1]))
    return grupos


def perfil(im_gris, eje, paso=2):
    """Media de luminosidad por fila (eje='y') o columna (eje='x')."""
    w, h = im_gris.size
    px = im_gris.load()
    if eje == 'y':
        return [sum(px[x, y] for x in range(0, w, paso)) / len(range(0, w, paso))
                for y in range(h)]
    return [sum(px[x, y] for y in range(0, h, paso)) / len(range(0, h, paso))
            for x in range(w)]


def cmd_detect(args):
    im = Image.open(args.imagen).convert('L')
    w, h = im.size
    print('tamaño: %d x %d' % (w, h))

    filas = perfil(im, 'y')
    cols = perfil(im, 'x')

    print('\n-- posibles GUTTERS (pasillo en blanco, umbral %d) --' % args.gutter)
    print('  filas :', bandas_limpias([255 - v for v in filas], 255 - args.gutter))
    print('  cols  :', bandas_limpias([255 - v for v in cols], 255 - args.gutter))

    print('\n-- posibles BORDES (línea oscura de rejilla, umbral %d) --' % args.borde)
    print('  filas :', bandas_limpias(filas, args.borde))
    print('  cols  :', bandas_limpias(cols, args.borde))

    print('\nElige el punto medio de la banda que separa las celdas que buscas')
    print('y pásalo a `crop` con --x / --y. Puedes dar varios: --x 400 800.')


def cmd_crop(args):
    im = Image.open(args.imagen).convert('RGB')
    w, h = im.size

    # --x/--y son la lista COMPLETA de límites, no puntos de corte internos.
    # Si quieres que la rejilla llegue al borde de la imagen, inclúyelo tú
    # mismo (0 y w, o 0 y h). El caso real que motivó esto: la hoja de 480589
    # tenía margen sobrante fuera de x=199..1004 e y=39..1150, y ese margen
    # había que descartarlo, no convertirlo en una fila/columna más.
    if len(args.x) < 2 or len(args.y) < 2:
        raise SystemExit('--x y --y necesitan al menos 2 valores cada uno '
                         '(los límites exterior e interior de la rejilla). '
                         'Si quieres llegar al borde de la imagen, añade 0 '
                         'y/o %d (ancho) / %d (alto) explícitamente.' % (w, h))
    xs = sorted(args.x)
    ys = sorted(args.y)

    os.makedirs(args.out, exist_ok=True)
    existentes = [f for f in os.listdir(args.out)
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if existentes and not args.force:
        raise SystemExit(
            'Ya hay %d imagen(es) en "%s". Usa --force si quieres seguir '
            'numerando a partir de ahí, o vacía la carpeta primero.'
            % (len(existentes), args.out))

    n = args.start
    guardados = []
    idx = 0
    for yi in range(len(ys) - 1):
        for xi in range(len(xs) - 1):
            celda = (xs[xi], ys[yi], xs[xi + 1], ys[yi + 1])
            if idx in args.skip:
                print('  [%d] %-22s SALTADA (--skip)' % (idx, str(celda)))
                idx += 1
                continue
            recorte = im.crop(celda)
            nombre = '%02d.jpg' % n
            destino = os.path.join(args.out, nombre)
            recorte.save(destino, quality=95, subsampling=0)
            print('  [%d] %-22s -> %s  (%dx%d)'
                  % (idx, str(celda), destino, recorte.width, recorte.height))
            guardados.append(destino)
            n += 1
            idx += 1

    print('\n%d paneles guardados en "%s".' % (len(guardados), args.out))
    print('Revísalos: build_all.py no comprueba que el recorte tenga sentido,')
    print('solo que exista.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_det = sub.add_parser('detect', help='solo lectura: sugiere dónde cortar')
    p_det.add_argument('imagen')
    p_det.add_argument('--gutter', type=int, default=245,
                       help='luminosidad mínima para considerar "blanco" (0-255, default 245)')
    p_det.add_argument('--borde', type=int, default=140,
                       help='luminosidad máxima para considerar "línea oscura" (0-255, default 140)')
    p_det.set_defaults(func=cmd_detect)

    p_crop = sub.add_parser('crop', help='corta de verdad')
    p_crop.add_argument('imagen')
    p_crop.add_argument('--x', type=int, nargs='*', default=[],
                        help='cortes verticales (columna en px); 0 y el ancho van implícitos')
    p_crop.add_argument('--y', type=int, nargs='*', default=[],
                        help='cortes horizontales (fila en px); 0 y el alto van implícitos')
    p_crop.add_argument('--skip', type=int, nargs='*', default=[],
                        help='índices de celda a descartar, 0-based, en orden de lectura')
    p_crop.add_argument('--out', required=True,
                        help='carpeta de producto donde guardar los paneles')
    p_crop.add_argument('--start', type=int, default=1,
                        help='número del primer panel guardado (default 1)')
    p_crop.add_argument('--force', action='store_true',
                        help='permite guardar aunque la carpeta ya tenga imágenes')
    p_crop.set_defaults(func=cmd_crop)

    args = ap.parse_args()
    args.func(args)
