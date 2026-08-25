# Actualización — Kakusei Hunter Omegahorn

> **Esto es una guía, no un parche.** No lo apliques al pie de la letra: las
> cifras y los nombres son de Gavan Infinity, y algunas cosas aquí **no te
> tocan**. Lee el §3 antes de tocar nada.
>
> **Y no es el destino final.** El encargo de verdad está en el §5: fundir toda
> tu documentación en **un solo md**, que es lo que heredará el próximo
> repositorio.

Sustituye a la versión anterior de este archivo, que ya está aplicada.

---

## 1. Lo que ha cambiado en Gavan Infinity

| Qué | En una línea |
|---|---|
| **Un solo md por repositorio** | los cinco documentos se fundieron en `Gavan-Infinity.md` |
| **La checklist se pliega por línea** | 129 piezas en un scroll eran 152 elementos |
| **Las reediciones son versiones, no piezas** | y la referencia lleva `@` siempre |
| **Colección contra familia** | la familia solo ordena dentro de una línea |
| **El límite de barras de la cabecera hay que medirlo** | el que estaba escrito era falso |

---

## 2. Lo que sí te toca, con tus propios números

Tu catálogo son **44 piezas** en tres colecciones —`egolgear` 33, `kakuzyu` 7,
`omegahorn` 4— sobre dos líneas, DX y SG. Eso cambia qué te sirve de esta lista.

### 2.1 Colección contra familia — la regla que te confirma

**Si dos grupos se compran por separado y no comparten línea, son colecciones
distintas.** La familia solo ordena dentro de una misma línea.

Tú ya lo hiciste bien: `kakuzyu` y `omegahorn` son colecciones propias, no
familias de `egolgear`. Gavan tuvo que aprenderlo tarde — los Gavarion Blade
empezaron como familia y hubo que sacarlos, porque agrupando primero por línea
quedaban repartidos entre tres y no había forma de verlos juntos.

**Lo que sí conviene comprobar:** una colección con una sola familia dibuja un
encabezado que repite su propio nombre y no organiza nada. Con `kakuzyu` a 7
piezas y `omegahorn` a 4, míralo: si cada una tiene una sola familia, ese
encabezado sobra.

### 2.2 Las reediciones, si las tienes

**Ninguna de tus 44 piezas declara `variants` hoy.** Merece una revisión: si una
pieza salió reeditada por otro canal —un premio, un furoku, un color exclusivo—
y está como entrada aparte, está compitiendo en el contador con su original.
Infla el denominador y deja la línea clavada para siempre por algo que no se
compra.

Va como `variants` de la pieza base, y **basta con tener una versión para que
cuente**. En Gavan eso bajó la línea DX de 98 a 94.

Si lo haces, dos avisos:

- **La referencia lleva `@` siempre** cuando la pieza tiene versiones, también
  `@std`. Desnuda parece declarar la pieza y declara una versión.
- **Tu `audit.py` sí parsea el catálogo de piezas**, como el de Gavan. Su lector
  corta en la primera llave de cierre, que en una pieza con `variants` es la de
  `{id:"std", …}`, y la sub-variante casa como si fuera una pieza. **Arréglalo
  antes**, exigiendo `name` detrás de `id` con un **lookahead** —consumirlo deja
  el cuerpo sin el campo y revienta igual—. Y al comprobarlo, mira que salgan
  los mismos ids **y los mismos campos**, no solo los ids.

### 2.3 Plegar la checklist por línea

Con 33 piezas en la principal sobre dos líneas estás por debajo del umbral donde
esto se vuelve urgente. **Anótalo para la próxima wave:** si una colección pasa
de unas 40 piezas, pliégala por línea desde el principio, con la misma máquina
del acordeón de meses. Cerrada debe seguir mostrando nombre, contador y barra.

### 2.4 La comprobación que le falta a la auditoría

Avisa de un tipo usado sin etiqueta, pero no del caso contrario: **una familia
declarada que ya ninguna pieza usa**. Como no dibuja nada, se queda en el mapa
para siempre sin que nada la delate. Aviso en BAJO.

### 2.5 El límite de la cabecera

La tabla que decía que la séptima barra envuelve casi siempre **era falsa**:
medido, siete caben a 1280 px. Lo que sí fallaba era la banda entre el
breakpoint del responsive y 1280, donde quedaba una barra huérfana en segunda
fila.

Tú tienes cuatro barras y margen de sobra, así que no te corre prisa. La lección
que sí te llevas: **ese número describe el ancho de *tus* rótulos, no los de
otra serie. Mídelo.**

---

## 3. Lo que NO te toca

- **`CATEGORY_BADGE`, `reservas`.** Ya venían en la actualización anterior.
- **`LINE_LABEL`.** Tus claves de línea son `DX` y `SG`, de una palabra.
- **Las cinco líneas y las siete familias de Gavan.** Son suyas.

---

## 4. Verificar

```bash
python tools/audit.py
python tools/check_urls.py
```

Y **ejecuta la lógica, no la leas**: marca una caja en el navegador, recarga, y
comprueba que la checklist dice lo mismo.

Aviso ganado por las malas: **las transiciones CSS no avanzan en una pestaña en
segundo plano.** Si un acordeón parece no abrirse, descarta eso antes de buscar
el fallo en tu CSS.

---

## 5. El encargo de verdad: un solo md

Hoy tienes `ADAPTACION.md`, `BITACORA.md`, `REGISTRO.md`, `PROJECT-RED.md` y
este archivo. Se solapan, y mantener varios es cómo se desincronizan.

**Fúndelos en un único documento llamado `Omegahorn.md`** (o como quieras
referirte a esa conversación), que sea el punto de entrada para cualquier
actualización, mejora o investigación. Lo que debe llevar dentro:

1. Qué es esto y cómo se mantiene.
2. El motor: estructura, la regla de oro del estado, el modelo de datos.
3. De dónde salen los datos y las imágenes, con sus trampas.
4. Qué se decidió en Omegahorn **y por qué** — que las piezas de una caja
   sorpresa van como entradas separadas y nunca como variantes, que es tu
   aportación y sigue vigente en Gavan.
5. Lo aprendido: los errores y lo que se probó y no funcionó.

**Escríbelo para heredarse.** La serie siguiente copia ese archivo, lo renombra
y sustituye la parte que es solo tuya. Todo lo demás debe servirle tal cual.

### ANTES de borrar `PROJECT-RED.md`, rescata su §5

**Este es el aviso más importante de todo el documento.** El §5 de
`PROJECT-RED.md` —«de dónde salen las imágenes»— es **la única copia que hay en
este repositorio** de las nueve páginas de las que se saca todo: los dos hosts de
Bandai, el CDN por número de modelo, Bandai Candy, Tamashii, el geobloqueo de
P-Bandai, las fotos de caja de HobbySearch, las APIs de Tokullectibles, la wiki
para los premios y el repositorio hermano para los crossover.

Ni `ADAPTACION.md` ni `BITACORA.md` ni `REGISTRO.md` lo tienen. Si borras
`PROJECT-RED.md` sin volcarlo, **eso desaparece** y la próxima wave se recopila a
ciegas.

Ya pasó: Myth consolidó siguiendo la versión anterior de esta guía y perdió la
sección; hubo que restituirla desde el historial de git. **Vuélcalo tú antes**, o
copia el anexo del final de este archivo, que es la versión completa y más al
día.

Y borra al terminar: `PROJECT-RED.md`, `ACTUALIZAR.md`, y `ADAPTACION.md`,
`BITACORA.md` y `REGISTRO.md` una vez volcados. **Si queda un `.md` suelto en la
raíz, no es un segundo documento: es algo pendiente de bajar y borrar.**

---

## 6. Un dato que sigue en pie

El premio de la **PROJECT R.E.D. Choco Campaign** es **la misma pieza física**
en las dos series: una cara Gavan Infinity y otra Captain Omegahorn. Tu copia es
la buena —`1798x1012`— frente a los `300x564` de la wiki. Gavan la tomó prestada
de aquí. Que quede escrito en tu md final: no es una foto duplicada por error,
es el mismo objeto.

---

## Anexo · De dónde salen las imágenes y los datos

Ninguna serie tiene todas sus fotos en un sitio. Este es el orden de búsqueda.

| Fuente | Para qué |
|---|---|
| `toy.bandai.co.jp` | ficha: fotos, fecha, precio, contenidos |
| **CDN de Akamai** | fotos de cualquier producto, aunque su página no abra |
| `bandai.co.jp/candy` | la raíz de SG |
| `tamashiiweb.com` | S.H.Figuarts: datos buenos, fotos pequeñas |
| `p-bandai.jp` | **geobloqueado** |
| `1999.co.jp` | **las fotos de caja** |
| `tokullectibles.com` | números de modelo, contenidos y banners |
| la wiki de la serie | premios, que ninguna tienda vende |
| el repositorio hermano | piezas de crossover |

**1 · La ficha de Bandai.** Conviven dos hosts y hay que mirar los dos:

```
bandai-a.akamaihd.net/bc/img/model/xl/<nº modelo>_<n>.jpg      fichas antiguas
assets-toy.bandai.co.jp/toy/ja/product/AAAA/MM/<hash>/<n>.jpg  nuevas
```

Con solo el primero se quedó fuera **la mitad** de los productos. Se enumera
`_1`, `_2`… hasta el primer 404 y **se conserva el orden del documento**: es el
de la galería oficial.

**2 · El CDN por número de modelo es la llave maestra.** No está geobloqueado y
responde aunque la página no se pueda abrir.

> **La trampa más cara de esta serie: devuelve 200 a cualquier número válido,
> sea de la serie que sea.** Diez fotos de Omegahorn entraron en este catálogo
> porque una tienda daba un número equivocado y la descarga «funcionó». **Abre
> una imagen y mírala** antes de dar por buena una carpeta.

**3 · Bandai Candy**, la raíz de SG:
`bandai.co.jp/candy/search/result.html?q=<término en japonés>`. En la ficha, la
galería propia son las imágenes con pareja `-product-mobile`; las que solo
aparecen como `-product-main` son de otros productos. **Sirve los mismos
archivos que el CDN**, así que aporta datos y no imágenes mejores — pero hay que
ir: destapó un producto que ninguna otra fuente listaba.

**4 · Tamashii Web** para S.H.Figuarts. Datos completos —precio, reservas,
`セット内容`— pero **las fotos más pequeñas** (857×1200) y las fichas nuevas solo
en `.webp`.

**5 · Premium Bandai está geobloqueado.** `p-bandai.jp` devuelve 302 desde fuera
de Japón y `p-bandai.com/us` no distribuye las exclusivas japonesas. **La salida
es el CDN:** el número de item de la URL *es* el número de modelo.

**6 · HobbySearch (`1999.co.jp`) es de donde salen las cajas.** Bandai no
publica la foto del paquete por separado:

```
www.1999.co.jp/itbig<NN>/<id>.jpg     miniatura 224 px
www.1999.co.jp/itbig<NN>/<id>b*.jpg   galería 1200 px
www.1999.co.jp/itbig<NN>/<id>p*.jpg   PAQUETE 1200 px   <- esto
```

Son JPEG de verdad aunque el navegador reciba `.webp`. **Su buscador tiene
truco:** el parámetro que funciona es `searchkey=`, no `sw=`; con `sw=` devuelve
el catálogo entero sin filtrar. No stockea exclusivas de P-Bandai ni premios.

**7 · Tokullectibles**, Shopify, sirve para tres cosas:

```
tokullectibles.com/products/<handle>.json
tokullectibles.com/collections/<slug>/products.json?limit=250
```

- **Números de modelo de todo**, incluidos SG, GP, minipla y yu-dō. Con eso, el
  CDN da las fotos: es la vía más rápida para levantar una línea entera.
- **Contenidos** que a veces Bandai no lista.
- **Banners** que Bandai no publica: se detectan porque su nombre **no** sigue
  el patrón `<nº modelo>_<n>.jpg`.

Dos avisos: **sus copias de Bandai están recomprimidas** —ni un byte coincidía
con las del CDN— y **reutiliza una imagen genérica** en los productos sin foto,
que se detecta porque el mismo nombre aparece en varios. Sus precios son de
importación en dólares.

**8 · La wiki es la única fuente de los premios**: campañas, máquina de garra,
bonos de ropa y regalos de revista. En Fandom los nombres están en
`data-image-name`. Ojo: a veces el original subido es pequeño.

**9 · El repositorio hermano.** Si una pieza es un crossover, puede estar mejor
al otro lado. El premio de la Choco Campaign está en Omegahorn a 1798×1012 y en
la wiki a 300×564.

### Después de descargar, comprueba

**Abre y decodifica todas las imágenes.** Un `PACKAGE.jpg` llegó truncado
—107.826 bytes en vez de 164.106— **con código 200**, y abría como imagen válida
hasta que `build_all` intentó leer el último bloque. Ni el código ni el tamaño
bastan.

**Adáptalo al volcarlo.** Lo de la línea SG y los premios de campaña te aplica
igual; lo del repositorio hermano, aquí es literal: el premio de la Choco
Campaign es el mismo objeto que en Gavan Infinity.
