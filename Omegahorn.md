# Kakusei Hunter Omegahorn — catálogo y manual

Punto de entrada único de este repositorio. Toda actualización, mejora o
investigación empieza aquí. Sustituye a `PROJECT-RED.md`, `ADAPTACION.md`,
`BITACORA.md`, `REGISTRO.md` y `ACTUALIZAR.md`, que quedaron volcados dentro.

**Si queda otro `.md` suelto en la raíz, no es un segundo documento: es algo
pendiente de bajar aquí y borrar.**

---

## 0. Cómo se hereda este documento

La serie siguiente copia este archivo, lo renombra a su nombre y **sustituye
solo el §7**, que es lo único específico de Omegahorn. Todo lo demás sirve tal
cual.

| Sección | Al heredar |
|---|---|
| §1 Qué es y cómo se mantiene | tal cual |
| §2 El motor | tal cual |
| §3 Carpetas e imágenes | tal cual |
| §4 De dónde salen los datos | tal cual — **es lo más caro de reconstruir** |
| §5 Herramientas | tal cual, cambiando los mapas de `plan.py` |
| §6 Nomenclatura | tal cual |
| **§7 Esta serie** | **se reescribe entero** |
| §8 Lo aprendido | tal cual, añadiendo lo nuevo |
| §9 Publicación | tal cual |
| §10 Qué decidir al arrancar | tal cual |

Cada decisión de aquí lleva su **porqué**. No es adorno: es lo que impide que
alguien la deshaga dentro de seis meses creyendo que era una errata. Si tomas
una decisión nueva, escríbela con su motivo o se perderá igual.

### Un apunte sobre el linaje

La plantilla ha cambiado de base dos veces, siempre por lo mismo: la serie nueva
no cabía en el molde de la anterior.

| Base | Por qué se abandonó |
|---|---|
| Kamen Rider Myth | tenía **una** colección repartida; las demás checklists eran categorías donde un producto era una pieza |
| **Omegahorn** | generalizó a **varias** colecciones repartidas — es la base actual |

De Myth sobrevive lo que era acierto de fondo: el mes como categoría raíz, la
checklist derivada, la cobertura transitiva y el trato de las imágenes. Lo que
no sobrevivió fue su estructura de datos.

**La pregunta que decide si hay que tocar el motor** está en el §10: *¿cada
coleccionable está repartido entre productos, o cada producto es una pieza?* Si
todo cabe en los dos mecanismos que ya existen, el motor no se toca.

---

## 1. Qué es esto y cómo se mantiene

### Para qué existe

Dos preguntas, en este orden:

1. **¿Cuándo llega la próxima wave?** Por eso el mes es la categoría raíz y todo
   cuelga de la fecha de salida.
2. **¿Qué me falta de los coleccionables?** Toda serie reparte sus piezas entre
   sets, cajas sorpresa y exclusivas — decenas, imposibles de rastrear a ojo.

Vocabulario, porque son cosas distintas y se confunden solas: una **wave** es el
ciclo de lanzamientos de un mes; las **tandas** son los días concretos de salida
dentro de ese mes. Septiembre es una wave con dos tandas.

### Un repositorio por serie

**No meter dos series en el mismo catálogo.** Cada una tiene sus coleccionables,
sus líneas y su calendario, y sobre todo: **una serie sigue sacando producto
después de que acabe su emisión**. Si compartieran repositorio, el catálogo de
la vieja seguiría creciendo dentro del de la nueva y el calendario dejaría de
responder a la pregunta que lo justifica.

Cada serie tiene su repositorio, su `index.html`, su URL y **su propia clave de
`localStorage`** — si dos catálogos comparten dominio y clave, se pisan lo que
el usuario tenga marcado. Aquí es `omegahorn-catalog-v1`; el patrón es
`<serie>-catalog-v1`.

### El ciclo de una wave

```
ficha  →  carpetas con fotos  →  audit.py  →  entradas en PIEZAS_CATALOG
   y PRODUCTS  →  registrar la carpeta en CARPETA de plan.py  →  build_all.py
   →  audit.py otra vez  →  check_urls.py  →  push  →  verificar contra el
   servidor publicado
```

**Los dos primeros pasos no se saltan.** Cada vez que se adelantó una decisión
sin tener los datos delante, hubo que deshacerla.

---

## 2. El motor

### Un archivo, dos listas

`index.html` es HTML5 + CSS3 + Vanilla JS. Sin frameworks, sin build, sin
dependencias. Todo el catálogo se genera desde dos arrays:

- `PIEZAS_CATALOG` — un objeto por pieza coleccionable
- `PRODUCTS` — un objeto por producto

De ahí salen las tarjetas, los contadores, las barras y las checklists.
Mantenerlo es editar dos listas.

**Por qué así:** la checklist necesita saber qué piezas trae cada producto. Si
las tarjetas fueran HTML a mano, esa relación viviría en la cabeza de quien las
escribió y se rompería a la tercera wave. Declarada como dato, marcar un
producto actualiza la checklist sola y no puede desincronizarse.

**El coste:** un error de sintaxis deja la página en blanco, porque todo se
genera en tiempo de ejecución. De ahí que el repositorio sea Git **desde antes
de escribir la primera entrada**.

### Estructura del archivo

| Bloque | Qué hay |
|---|---|
| CSS, 9 secciones | tokens → base → cabecera → acordeón → tarjetas → contenidos → visor → panel → responsive |
| **1 · Configuración** | todas las constantes que se tocan al cambiar de serie |
| **2 · `PIEZAS_CATALOG`** | catálogo maestro de coleccionables |
| **3 · `PRODUCTS`** | los productos, agrupados por mes en comentarios |
| **4 · Estado** | `localStorage`, carga y guardado |
| **5 · Índices** | derivados: cobertura, variantes, progreso |
| **6 · Utilidades** | escape, precio, fechas, meses |
| **7 · Render catálogo** | mes → subcategoría → tarjeta |
| **8 · Render checklists** | panel lateral y pestañas |
| **9 · Eventos** | acordeón, estados, visor, panel |
| **10 · Arranque** | `init()` |

El `<body>` es un esqueleto: cabecera, `<main id="catalog">` vacío, el visor, el
backdrop y el `<aside id="panel">`. Todo el contenido se genera desde JS.

### La regla de oro

Solo se persiste `{products:{id:estado}, ui:{...}}`. **Las checklists nunca se
guardan: se derivan de los productos en cada render.** Progreso, cobertura y qué
pieza falta son cálculo, no dato. Esa es la razón de que no puedan
desincronizarse.

`loadState()` además **descarta ids que ya no existen**, para que renombrar un
producto no deje basura invisible engordando el guardado.

### El flujo de datos

```
PRODUCTS[].date  ──> p.month = date.slice(0,7)  ──> acordeón de meses

PRODUCTS[].contains ─┐
                     ├─> ownedVariantSet() ─> piezaStatus() ─> checklists y barras
PIEZAS_CATALOG ──────┘

PRODUCTS[].reemplaza ──> coveredMap() ──> isResolved() ──> "cubierto" y contadores

PRODUCTS[].contains ──> SOURCES ──> salto desde la checklist al producto
```

### Varias colecciones, un solo mecanismo

Es la diferencia grande con Myth y la razón de que esta sea la base.

Cada pieza declara a qué **colección** pertenece:

```js
const COLECCIONES = {
  "egolgear":  { label:"EgolGear", principal:true, slug:"egolgear", hint:"…" },
  "kakuzyu":   { label:"Kakuzyu",   slug:"kakuzyu",   hint:"…" },
  "omegahorn": { label:"Omegahorn", slug:"omegahorn", hint:"…" }
};
```

`principal:true` marca el gimmick de la temporada: se lleva los dos colores
fuertes y se parte por línea en la cabecera. Las secundarias van en tonos suaves
y con una barra sola.

Los productos declaran **un único `contains`** mezclando piezas de todas las
colecciones. El motor no las distingue al marcar: para él una pieza es una
pieza. El panel se genera recorriendo `COLECCIONES`, así que añadir o quitar una
colección no toca la lógica.

**Colección contra familia, que es lo que más se confunde.** Si dos grupos se
compran por separado y no comparten línea, son **colecciones distintas**. La
familia solo ordena dentro de una misma línea. Agrupar como familia algo que
debería ser colección lo deja repartido entre líneas y sin forma de verlo junto.

**Una colección con una sola familia no dibuja encabezado de grupo.** Repetiría
el nombre de la colección y su contador ya está en la barra de la línea. Está
resuelto en el render con `familiasDe(col).size > 1`, mirando la colección
entera y no una línea suelta: si dentro de SG hay una sola familia pero la
colección tiene cuatro, el encabezado sigue diciendo algo.

### Modelo de pieza

```js
{ id:"eg-denkaku",
  name:"Denkaku EgolGear",
  collection:"egolgear",   // clave de COLECCIONES
  type:"egolgear",         // clave de FAMILIAS; agrupa dentro del panel
  line:"DX",               // contadores separados por línea
  meaning:"Electric Horn", // opcional, pista bajo el nombre
  variants:[ {id:"std", label:"Estandar"}, {id:"promo", label:"Promo ver."} ] }
```

`variants` es para **la misma pieza reeditada** por otro canal. La pieza cuenta
una vez y basta tener una versión para marcarla. Si una reedición se mete como
entrada aparte, compite con su original en el contador: infla el denominador y
deja la línea clavada para siempre por algo que no se compra.

**Cuando una pieza tiene versiones, la referencia lleva `@` siempre**, también
`@std`. Desnuda parece que declara la pieza y en realidad declara una versión.

### Modelo de producto

```js
{ id:"dx-enkaku-set",         // <línea>-<producto>, minúsculas
  title:"NOMBRE DE LA CAJA",
  category:"CATEGORÍA",       // una de CATEGORY_ORDER
  date:"2026-07-25",          // el mes del acordeón sale de aquí
  dateType:"release",         // "release" | "preorder"
  dateExact:false,            // opcional: mes anunciado, día no → muestra N/D
  price:8580,                 // con impuestos, o null
  priceLabel:"3 cajas x 418", // opcional: matiza o sustituye el precio
  alsoIn:["OTRA CATEGORÍA"],  // opcional: producto que pertenece a dos
  reemplaza:["id"],           // opcional: productos que trae dentro
  componentes:["no-coleccionable"],  // opcional, solo para la auditoría
  img:"...-thumb.webp",
  gallery:["....webp"],
  contains:["pieza-id","pieza-id@variante"] }
```

`date` es **la única fuente de verdad temporal**; el mes se deriva de ella al
cargar. Guardar mes y fecha por separado los deja desincronizarse.

**`dateExact:false` para cuando hay mes pero no día.** La fecha sigue haciendo
falta para colocar el producto en su acordeón, pero la tarjeta muestra **N/D** y
ese día no cuenta como tanda ni alimenta la cuenta atrás. Sin esto, la cabecera
publica como cierto un día que nos inventamos: septiembre llegó a anunciar «2
tandas: días 1 · 5» con un día 1 que no existía. **Un dato inventado para que el
motor funcione tiene que estar marcado como inventado.**

**Convención para el ancla: el día 15**, que es la fecha habitual cuando Bandai
anuncia solo el mes. Deja el producto a mitad de mes en vez de empujarlo al día
1, que lo colocaba por delante de lanzamientos ya confirmados. Sigue siendo un
marcador —la tarjeta muestra N/D igual—, pero es un marcador que no desordena.

### `CATEGORY_BADGE` — el distintivo se declara, no se deduce

```js
const CATEGORY_BADGE = {
  "DX SETS":"DX", "DX MECHAS":"DX", "DX EGOLGEAR SETS":"DX",
  "SG MINIPLA":"SG", "SG YU-DO":"SG", "SG RANDOM BOX":"SG"
};
```

El motor sacaba el distintivo de `p.category.startsWith("SG")` y todo lo demás
recibía «DX». Con dos líneas de juguete parecía funcionar, pero **TAF y
SOFTVINYL no son ninguna de las dos** y salían etiquetadas como DX: la tarjeta
mentía. **Una categoría sin entrada no lleva distintivo**, que es mejor que
llevar uno equivocado. El promocional tampoco lleva: ya se distingue con su
chapa de «Premio».

### Las cuatro reglas del modelo que más se prestan a error

**Líneas separadas.** Si la serie tiene dos líneas que sacan piezas exclusivas
cada una, van con contadores independientes. Fundirlas hace que «me faltan 3» no
signifique nada.

**Variantes contra piezas propias:**

| Situación | Cómo va |
|---|---|
| Misma pieza reeditada, otro acabado o canal | `variants` |
| Piezas que aluden a criaturas o personajes distintos | entradas separadas |
| Piezas distintas de una caja sorpresa | **entradas separadas, siempre** |

La tercera fila es aportación de Omegahorn y sigue vigente. En una caja sorpresa
cada pieza es un SKU: si fueran variantes, sacar la normal marcaría la línea
completa mientras te sigue faltando un gear físico que solo se consigue con otra
compra. **El contador mentiría.** Es lo contrario del caso de la reedición, y lo
que los separa es si hay que comprar dos veces o no.

**Una familia se define por un criterio, no por una lista.** Aquí
`egolgear-kakuju` no es «los que vienen con un mecha» sino «los que pertenecen a
un Kakuzyu del que existe figura». Con un criterio, una pieza migra sola de
familia cuando salga la suya; con una lista, hay que acordarse de moverla.

**Qué alimenta cada checklist.** Solo el coleccionable de verdad. Los accesorios
a escala de una figura no son la pieza: el TAF trae un «Omega Horn» que es parte
de la figura, no el juguete, y contarlo inflaría el progreso.

### Las checklists en pantalla

**Cada colección en su pestaña, nunca apiladas.** Hay quien sigue una sola, y a
ese pasar por las demás para llegar a la suya no le sirve. Cada pestaña lleva su
contador, su texto de ayuda y su color; el panel recuerda en cuál estabas.

**Iguala el largo de los textos de ayuda** y ponles `min-height`. Si uno ocupa
tres líneas y los demás dos, la cabecera del panel salta de alto al cambiar de
pestaña.

**El color orienta, la opacidad no.** Los dos tonos más fuertes son del
coleccionable principal; el resto usa tonos suaves. **No atenúes las secundarias
con `opacity`**: se leen como deshabilitadas. La jerarquía la dan el color y el
ancho.

**Filas sin caja.** Con más de veinte piezas en pantalla, una tarjeta por fila
convierte la lista en un muro. Fondo solo al pasar por encima y el estado en el
punto.

**El límite de barras de la cabecera hay que medirlo, no heredarlo.** Ese número
describe el ancho de *tus* rótulos. Medido aquí a 1280 px con rótulos del largo
de los nuestros: **siete caben, la octava envuelve**. Con cuatro hay margen de
sobra. Comprueba también la banda entre el breakpoint del responsive (1080 px) y
1280, donde puede quedar una barra huérfana en segunda fila; a 1100 px con
cuatro barras no ocurre.

**Si una colección pasa de unas 40 piezas, pliégala por línea** desde el
principio, con la misma máquina del acordeón de meses. Cerrada debe seguir
mostrando nombre, contador y barra. Aquí la mayor tiene 33 y no hace falta.

**Cuidado con «cubierto»:** en la tarjeta significa *no necesitas comprarlo* y
se atenúa; en la checklist significa *lo tienes* y se marca en verde. Misma
información, dos preguntas distintas.

### Cobertura entre productos

Cuando un set trae dentro otro producto se declara con `reemplaza` **en el que
absorbe**, y la cobertura es **transitiva**: basta declarar lo que se absorbe
directamente. `coveredMap()` recorre la cadena con corte de ciclos.

Se declara solo hacia abajo, nunca al revés: así sacar un set nuevo es tocar un
solo sitio en vez de editar todo lo que deja obsoleto.

### Detalles de implementación que conviene no perder

- **`updateCardUI` + `refreshCoverage`** en vez de re-render completo, para no
  cerrar los `<details>` abiertos ni perder el scroll.
- **`querySelectorAll("[data-pid]")`, nunca `getElementById`**: un producto con
  `alsoIn` tiene varias tarjetas y todas deben reflejar el mismo estado.
- **Volver a pulsar el estado activo lo devuelve a `pending`.**
- **`esc()` en todo lo que venga de datos** antes de inyectarlo.
- **Aviso por consola** si un producto referencia una pieza inexistente. En Myth
  eso se ignoraba en silencio y la checklist quedaba corta sin decirlo.
- El texto del desplegable cambia según sea caja sorpresa («posibles
  contenidos») o set («piezas incluidas»): llamarlos igual daría a entender que
  un set es una lotería.

---

## 3. Carpetas e imágenes

```
SERIE/
├── index.html
├── .gitignore
├── tools/
├── CATEGORÍA EN MAYÚSCULAS/
│   ├── FICHA/                    ← consulta, NO se publica
│   ├── NOMBRE DEL PRODUCTO/
│   │   ├── PACKAGE.jpg           ← original, NO se publica
│   │   ├── PACKAGE.webp          ← galería, 1600 px
│   │   ├── PACKAGE-thumb.webp    ← portada, 700 px
│   │   └── 01.jpg  01.webp
│   └── PRODUCTO DE UNA IMAGEN-Contenidos.jpg   ← sin carpeta
```

**`FICHA/` es material de consulta de formato libre.** Capturas de las páginas
oficiales de donde salen fecha, precio y contenidos, a resolución original y sin
convertir, precisamente para poder leerlas. No se publican y **sus nombres no
tienen que corresponderse con nada**: una hoja puede cubrir una colección
entera. Exigirles un nombre por producto fue una regla inventada que hizo gritar
a la auditoría de Myth durante días.

Aun así conviene nombrarlas `PRODUCTO-Contenido 1, Contenido 2…`: no lo exige
nada, pero al cargar una wave se sabe qué trae cada caja sin abrir la imagen.

**Portada = `PACKAGE` si existe, si no `01`.**

**Un producto cruzado tiene carpeta espejo.** Si pertenece de verdad a dos
categorías, la carpeta y la ficha se duplican **con el mismo nombre** en ambas y
el catálogo apunta solo a la primaria con `alsoIn`. La copia espejo se queda sin
`.webp` a propósito, porque `build_all` solo convierte lo que el catálogo
referencia. **No sobra: es espejo deliberado.**

**Las mayúsculas importan.** Windows es case-insensitive y GitHub Pages no: una
mayúscula mal puesta funciona en tu equipo y da 404 publicada. `audit.py` usa
`os.path.exists` y **no puede verlo**; para eso está `check_urls.py`, que
compara cada tramo contra el nombre real del directorio letra a letra.

### Tamaños

| Archivo | Lado máx. | Calidad | Para qué |
|---|---|---|---|
| `<nombre>.webp` | 1600 px | 80 | galería, se abre en el visor |
| `<nombre>-thumb.webp` | 700 px | 82 | portada de la tarjeta |

`build_all` nunca amplía: `escala = min(1, lado/max(w,h))`. Si el origen es de
1200 px, la galería se queda en 1200 y no pasa nada.

**Comprueba la resolución de origen antes de recortar.** Un panel recortado de
una hoja de despiece puede quedar por debajo de los 700 px del thumb y salir
borroso de portada. Si la galería del producto trae la pieza montada a tamaño
completo, esa es la portada.

### Cinco trampas de imagen que costaron horas

**No pongas `loading="lazy"` en las portadas.** Las tarjetas viven dentro de un
acordeón que arranca con `max-height: 0`; el navegador las da por fuera de
pantalla y no las pide hasta que hay scroll, así que aparecen vacías.

**Las fotos de galería sí se difieren, pero de verdad:** el visor pide la foto
al abrirse. Con `lazy` a secas el navegador tira de las cercanas y el ahorro se
evapora.

**Nada de servir imágenes desde Drive.** Van junto al HTML, con **rutas
relativas** — así funciona igual bajo `/repo/` que en un dominio propio.

**Cuidado con las miniaturas que cargan la imagen grande.** Una tira de
miniaturas de 62 px apuntando al archivo de 1600 px son megas para pintar
cuadraditos.

**`flex:1` en una tarjeta de la cabecera la estira.** El ancho lo fija
`min-width`; el `flex:1` solo va dentro de la media query, donde las barras
bajan a su propia fila y sí deben repartirse el espacio.

---

## 4. De dónde salen los datos y las imágenes

**Esta sección es la más cara de reconstruir. No la borres al heredar.** Ninguna
serie tiene todas sus fotos en un sitio; este es el orden de búsqueda.

| Fuente | Para qué sirve |
|---|---|
| `toy.bandai.co.jp` | la ficha: fotos, fecha, precio y contenidos |
| **el CDN de Akamai** | fotos de cualquier producto, aunque su página no abra |
| `bandai.co.jp/candy` | la raíz de SG: shokugan, minipla, yu-dō |
| `tamashiiweb.com` | S.H.Figuarts: datos buenos, fotos pequeñas |
| `p-bandai.jp` | **geobloqueado** |
| `1999.co.jp` | **las fotos de caja**, que Bandai no publica aparte |
| `tokullectibles.com` | números de modelo, contenidos y banners |
| la wiki de la serie | premios de campaña, que ninguna tienda vende |
| el repositorio hermano | piezas de crossover |

**1 · La ficha de Bandai.** Conviven dos hosts de imagen y hay que mirar los dos:

```
bandai-a.akamaihd.net/bc/img/model/xl/<nº modelo>_<n>.jpg          fichas antiguas
assets-toy.bandai.co.jp/toy/ja/product/AAAA/MM/<hash>/<nombre>.jpg  nuevas
```

Con solo el primero se quedó fuera **la mitad** de los productos. Se enumera
`_1`, `_2`… hasta el primer 404 y **se conserva el orden del documento**: es el
de la galería oficial.

**2 · El CDN de Akamai, por número de modelo. Es la llave maestra.** No está
geobloqueado y responde aunque la página del producto no se pueda abrir:

```
bandai-a.akamaihd.net/bc/img/model/xl/1000247747_1.jpg
```

> **La trampa más cara de la franquicia: devuelve 200 a cualquier número válido,
> sea de la serie que sea.** Diez fotos de Omegahorn acabaron en el catálogo de
> Gavan Infinity porque una tienda daba un número equivocado y la descarga
> «funcionó». **Abre una imagen y mírala** antes de dar por buena una carpeta.

**3 · Bandai Candy** es la raíz de SG. El buscador que funciona:

```
bandai.co.jp/candy/search/result.html?q=<término en japonés>
```

En la ficha, la galería propia son las imágenes con pareja `-product-mobile`;
las que solo aparecen como `-product-main` son miniaturas de otros productos.
**Sirve los mismos archivos que el CDN**, así que aporta datos y no imágenes
mejores — pero hay que ir igual: destapó un producto que ninguna otra fuente
listaba.

**4 · Tamashii Web** para S.H.Figuarts, `tamashiiweb.com/item/<n>`. Datos
completos —precio, ventana de reservas, `セット内容`— pero **las fotos más
pequeñas** (857×1200), y las fichas nuevas solo en `.webp`.

**5 · Premium Bandai está geobloqueado.** `p-bandai.jp` devuelve 302 desde fuera
de Japón y `p-bandai.com/us` no distribuye las exclusivas japonesas. **La salida
es el CDN:** el número de item de la URL de P-Bandai *es* el número de modelo.

**6 · HobbySearch (`1999.co.jp`) es de donde salen las cajas.** Bandai no publica
la foto del paquete por separado:

```
www.1999.co.jp/itbig<NN>/<id>.jpg     miniatura de 224 px
www.1999.co.jp/itbig<NN>/<id>b*.jpg   galería a 1200 px
www.1999.co.jp/itbig<NN>/<id>p*.jpg   PAQUETE a 1200 px   ← esto
```

Son JPEG de verdad aunque el navegador reciba `.webp` por negociación de
contenido. **Su buscador tiene truco:** el parámetro que funciona es
`searchkey=`, no `sw=`; con `sw=` devuelve el catálogo entero sin filtrar. Lo
más simple es enviar el formulario y quedarse con la URL resultante. No stockea
exclusivas de P-Bandai ni premios.

**7 · Tokullectibles**, tienda Shopify. Su API sirve para tres cosas:

```
tokullectibles.com/products/<handle>.json
tokullectibles.com/collections/<slug>/products.json?limit=250
```

- **Números de modelo de todo**, incluidos SG, GP, minipla y yu-dō. Con eso el
  CDN da las fotos: es la vía más rápida para levantar una línea entera.
- **Contenidos** que a veces Bandai no lista.
- **Banners** que Bandai no publica: se detectan porque su nombre **no** sigue
  el patrón `<nº modelo>_<n>.jpg`.

Dos avisos: **sus copias de Bandai están recomprimidas** —ni un byte coincidía
con las del CDN— y **reutiliza una imagen genérica** en los productos sin foto,
que se detecta porque el mismo nombre aparece en varios. Sus precios son de
importación en dólares, no el PVP en yenes.

**8 · La wiki de la serie es la única fuente de los premios**: campañas, máquina
de garra, bonos de ropa y regalos de revista. En Fandom los nombres de archivo
están en `data-image-name`. Ojo: a veces el original subido es pequeño.

**9 · El repositorio hermano.** Si una pieza es un crossover, puede estar mejor
al otro lado.

### Y una regla sobre la wiki que no es de imágenes

**La wiki aclara dudas; no alimenta el catálogo.** Lista personajes del
bestiario que todavía no tienen producto, y una pieza que ningún producto trae
no se puede marcar nunca: infla el denominador y la auditoría la señalaría con
razón. Sirve para confirmar que dos bichos parecidos son distintos y para
resolver grafías.

### Después de descargar, comprueba

**Abre y decodifica todas las imágenes.** Un `PACKAGE.jpg` llegó truncado
—107.826 bytes en vez de 164.106— **con código 200**, y abría como imagen válida
hasta que `build_all` intentó leer el último bloque. Ni el código de respuesta
ni el tamaño bastan.

---

## 5. Herramientas

Tres scripts con Pillow como única dependencia, más uno de solo red.

| Script | Qué hace | Escribe |
|---|---|---|
| `audit.py` | cruza `index.html` con el disco | nada |
| `check_urls.py` | comprueba las rutas distinguiendo mayúsculas | nada |
| `plan.py` | muestra qué portada y galería saldrían | nada |
| `build_all.py` | genera los `.webp` y repunta el HTML | sí |

Los de lectura van siempre antes. `audit.py` sale con código 1 si hay algo en
ALTO, así que se puede encadenar.

`plan.py` mapea `id → carpeta` en `CARPETA` y `id → archivo` en `SUELTO`. **Los
productos de una sola imagen van en el segundo:** en Myth no pasaban por las
herramientas y sus `.webp` había que generarlos a mano.

`build_all.py` reescribe `img:` y `gallery:` con expresiones ancladas al `id` del
producto, y al final verifica rutas rotas y calcula el peso de despliegue.

### Lo que comprueba la auditoría

1. Que `index.html` y el disco digan lo mismo — lo único que puede romper el
   sitio publicado, así que va primero.
2. Integridad del catálogo de piezas: referencias huérfanas, piezas que ningún
   producto trae, ids duplicados, familias sin etiqueta **y familias declaradas
   que ya no usa nadie** (esta última en BAJO: como no dibuja nada, no hay nada
   que la delate).
3. Portada y numeración de cada producto.
4. El árbol de `reemplaza`, con ciclos e ids inexistentes.
5. Cobertura **deducida** comparando contenidos, para no fiarse de lo declarado.
6. Nomenclatura.

**Una auditoría con falsos positivos es peor que ninguna.** La de Myth contaba
los `.webp` derivados como fotos y avisaba de huecos inexistentes: con 74 avisos
de los que 70 eran ruido, nadie los lee. Aquí se corrigieron dos que daba de
más: la copia espejo de un producto cruzado y los productos de una imagen.

**El lector del catálogo de piezas lleva un lookahead de `name:`, y es
necesario.** Una pieza con `variants` contiene objetos `{id:"std", label:"…"}`;
el cuerpo no-avaro corta en la primera llave de cierre, que es la de la
variante, y sin el filtro la siguiente casaba como si fuera una pieza más. Tiene
que ser lookahead y **no** consumo: si se consume `name:`, el cuerpo se queda
sin ese campo y el `re.search` revienta. Al tocarlo, comprueba que salgan los
mismos ids **y los mismos campos**, no solo los ids.

### Cobertura deducida de los contenidos

La auditoría compara conjuntos de contenido y avisa en los dos sentidos:
cobertura que falta declarar y cobertura declarada que el contenido no respalda.
Deducir eso a ojo falló dos veces seguidas en Myth.

En Myth hacía falta el campo `componentes` porque Drivers y Buckles no eran
coleccionables. **Cuantas más cosas sean coleccionables, menos falta hace:** aquí
los Kakuzyu y el Omega Horn están en `contains`, así que la cadena se deduce
sola y `componentes` quedó casi vacío.

---

## 6. Nomenclatura

**La romanización sale de la caja, no de la transcripción.** Las páginas en
inglés de Bandai vienen de traductor automático: al Ikaku EgolGear lo llamaron
«Squid Quest Gorgia» y a Saikaku «Horned beast Rhino». Sirven para fechas y
precios; para nombres, manda la caja.

**Dentro de la propia web, la lista de contenidos gana a la descripción.**
Conserva las vocales largas que la descripción recorta —Goukaku, Kyoukaku,
Youkaku— aunque falla alguna vez: dijo «Pikakuegorgia» donde la descripción daba
«Bikaku (Beautiful)», y ahí ganó la descripción porque *beautiful* es 美 (bi).
**Cruzar las dos siempre.**

**La tabla de セット内容 de la caja es la fuente buena.** Fue la que cerró si dos
piezas parecidas eran la misma: nombra en katakana y marca las exclusivas con
セット品限定.

**Guion en los compuestos cuando la costura no se ve.** `Zetsu-Enkaku`, no
`Zetsuenkaku`. Bandai suele ponerlo en el título de producto y perderlo en los
contenidos.

**Prima que se entienda sobre la fidelidad literal.** El gimmick de Myth se
romaniza «EGZ» y se eligió **Eggs**. Cuando tomes una decisión así, **escríbela
con su porqué**, o alguien la «corregirá» meses después creyendo que es una
errata.

**Decide la nomenclatura antes de publicar, y hazlo completo.** Nombres
visibles, nombres de archivo **e identificadores internos**, más las clases CSS
y los tokens de color. Dejar un slug antiguo por dentro mostrando el nombre
nuevo por fuera es deuda que se paga sola. Renombrar es barato en local y caro
cuando ya hay enlaces fuera.

---

## 7. Esta serie · SE REESCRIBE ENTERO AL HEREDAR

Todo lo de este apartado es específico de Kakusei Hunter Omegahorn.

### 7.1 Configuración

| Constante | Valor |
|---|---|
| `STORAGE_KEY` | `omegahorn-catalog-v1` |
| Líneas | `DX` y `SG` |
| Colecciones | `egolgear` *(principal)* · `kakuzyu` · `omegahorn` |
| Familias | `egolgear` · `egolgear-kakuju` · `egolgear-henishu` · `zetsu-egolgear` · `kakuzyu` · `device` |
| Colores | **rojo** EgolGear DX · **turquesa** EgolGear SG · dorado Kakuzyu · azul Omegahorn |
| `RANDOM_BOX_CATEGORIES` | solo `SG RANDOM BOX` |
| Categorías | TAF · SOFTVINYL · SG MINIPLA · SG YU-DO · SG RANDOM BOX · DX SETS · DX MECHAS · DX EGOLGEAR SETS · EGOLGEAR PROMOCIONALES |

Rojo y turquesa son la identidad de la serie: el rojo de Enkaku y el Capitán, el
turquesa del Omega Horn.

### 7.2 Los coleccionables

**44 piezas**: 33 EgolGear (25 DX + 8 SG), 7 Kakuzyu (6 DX + 1 SG) y 4 Omegahorn
(3 DX + 1 SG). **25 productos** en 9 categorías, hasta 2026/10/03.

> **Aquí no se repite el catálogo.** La lista de productos con sus fechas,
> precios y contenidos vive en `PIEZAS_CATALOG` y `PRODUCTS`, dentro de
> `index.html`, y **esa es la única fuente de verdad**. Copiarla aquí crearía un
> segundo sitio que actualizar, que es exactamente cómo se desincronizaron los
> cinco documentos que este sustituye. Para consultar datos, mira el catálogo;
> para saber **por qué** un dato es como es, sigue leyendo.

**EgolGear DX (25).** Doce se venden en pares en los `DX EGOLGEAR SETS`;
los demás solo existen dentro de otro producto, que es lo que justifica derivar
el progreso desde `contains`.

| Familia | Piezas |
|---|---|
| `egolgear` | 17 — los doce de los sets, Enkaku no, los cuatro del REPLICA SET y el promocional |
| `egolgear-kakuju` | 6 — Enkaku, Zetsu-Enkaku, Zankaku, Saikaku, Hikaku, Goukaku |
| `zetsu-egolgear` | 2 — Zetsu-Soukaku y Zetsu-Gokaku |

**EgolGear SG (8).** Los del `SG EGOLGEAR RANDOM BOX 01`: Enkaku, Denkaku,
Ninkaku, Roukaku, Soukaku, Hokaku y los dos `Hen'ishu`. Cuatro repiten nombre de
bicho con DX pero son moldes y canales distintos: cuentan aparte.

**Kakuzyu (7).** Enkaku, Zankaku, Saikaku, Hikaku, Goukaku y Zetsu-Enkaku en DX,
más el Enkaku de Minipla en SG. El Enkaku de soft vinyl **no** entra: es una
figura de vinilo de otra escala y otra línea.

**Omegahorn (4).** Omega Horn, Omega Horn Absolute y Omega Horn Replica en DX,
más el de Minipla en SG. El `Omega Analyzer` **no** entra: es el aparato de
transformación, otro producto.

### 7.3 Las decisiones cerradas, con su porqué

**角獣 se escribe Kakuzyu, nunca «Horned Beast».** Decisión de nomenclatura de la
serie. Se aplicó a nombres visibles, nombres de archivo e identificadores
internos a la vez.

**Los tres `Zetsu-` no van juntos.** La familia `egolgear-kakuju` la decide el
bicho, no la caja: entra un gear si pertenece a un Kakuzyu **del que existe
figura**. Zetsu-Enkaku tiene figura, así que se va con los de Kakuzyu;
Zetsu-Soukaku y Zetsu-Gokaku no la tienen y se quedan solos. Si Bandai saca el
mecha de Soukaku, esa pieza migra sola de familia — que es la ventaja de definir
por criterio.

**Zetsu-Soukaku y Zetsu-Gokaku son piezas distintas.** Aguantó tres rondas de
comprobación: la tabla oficial de セット内容 del EGOLGEAR SET nombra
**ゼツソウカク** y le pone el sello セット品限定; el arte interior de las dos
piezas blancas no se parece —cresta dorada y dos colmillos curvos frente a un
tocado en abanico sobre cara acorazada, y 双角 son «dos cuernos»—; y la wiki
oficial las lista separadas, Class A y Class S. **Consecuencia práctica:** quien
compre el REPLICA SET no se queda cubierto el Zetsu-Soukaku.

**Los dos `Hen'ishu` son entradas propias y con familia propia.** Vienen de una
caja sorpresa de ocho SKU: si fueran variantes, sacar el Denkaku normal marcaría
la línea completa mientras te falta un gear físico. La wiki lo respalda: los
trata como bichos distintos, no como una versión.

**El premio de la Choco Campaign se cataloga como EgolGear.** En la fuente
japonesa la pieza es un **エモルギア (Emolgear)**, el coleccionable de Gavan
Infinity, no un エゴルギア: la página de la campaña dice
*«限定スペシャルカラー エモルギアが合計2,000名様にあたる»* y la ficha del
`DX OMEGAANALYZER` lo confirma al explicar que el Analyzer lee Emolgear además
de EgolGear. Se cataloga como EgolGear por practicidad —encaja en el formato y
se usa en el mismo juguete— y con `line:"DX"`. **Que quede escrito: no es una
errata.**

**Y es el mismo objeto físico que en Gavan Infinity**, no una foto duplicada por
error: una cara Gavan y otra Captain Omegahorn. Nuestra copia es la buena,
**1798×1012** frente a los 300×564 de la wiki; Gavan la tomó de aquí.

**Los yu-dō no son caja sorpresa.** La caja lleva impreso
`この箱の中には ① が入っています`: el número va por fuera y se elige. Por eso
`SG YU-DO` no entra en `RANDOM_BOX_CATEGORIES` — si entrara, la tarjeta trataría
un contenido garantizado como una lotería.

**El precio de los yu-dō es por caja, y cada producto agrupa varias.**
`… ENKAKU` son tres cajas (1.254), `… OMEGAHORN` dos (836) y
`… CAPTAIN OMEGAHORN` una (418). Las tres suman 2.508, exactamente lo que cuesta
el SET de Minipla: **el SET no descuenta, solo ahorra la búsqueda.** Ese cuadre
es lo que confirma que la cuenta está bien.

**`Zetsu-Gokaku`, sin vocal larga.** Es la única pieza donde la wiki oficial
gana a la lista de contenidos de Bandai, que escribe `Zetsugoukaku`. Decisión
tomada a la vista de las dos fuentes.

**Ojo con la inconsistencia que deja, y es deliberada:** el bicho base sigue
siendo **`Goukaku`** —con u—, porque ahí Bandai lo escribe así en la descripción
**y** en la lista de contenidos, y solo lo recorta en el título en mayúsculas
`DX MEGA BRAVE HORN GOKAKU`. La evidencia es distinta para cada pieza, así que
las grafías son distintas. No es una errata a medio corregir.

**El accesorio «Omega Horn» del TAF no cuenta.** Es pieza de figura a escala, no
el juguete.

**El `DX MEGA FLAME HORN ENKAKU` suelto es el único mecha sin EgolGear.** Está
confirmado en la web; no es un hueco de la ficha.

### 7.4 Cobertura

Dos cadenas, ninguna cruza entre líneas.

```
DX MEGA FLAME HORN ENKAKU ＆ OMEGAHORN EGOLGEAR SET
 └─ ENKAKU ＆ OMEGAHORN SET
     ├─ DX MEGA FLAME HORN ENKAKU
     └─ DX OMEGAHORN

MINIPLA KAKUSEIHUNTER OMEGAHORN 01 SET
 ├─ YU-DO … 01 ENKAKU
 ├─ YU-DO … 01 OMEGAHORN
 └─ YU-DO … 01 CAPTAIN OMEGAHORN
```

El EGOLGEAR SET **no** absorbe los SET 01–04 aunque comparta un gear con cada
uno: cada set trae dos y solo coincide uno. Ahí va `contains`, nunca
`reemplaza`.

Un solo producto cruzado: el `ZETSU-ENKAKU ＆ OMEGAHORN ZETSU SET`, en `DX SETS`
con `alsoIn:["DX MECHAS"]`.

### 7.5 Fechas sin día

Cinco productos de septiembre llevan `dateExact:false`: los tres yu-dō, el SET
de Minipla y el promocional. Su ancla es **2026-09-15** por la convención de
arriba; la tarjeta muestra **N/D** y septiembre se rotula «Día 5 · 5 sin fecha».
La campaña del premio cierra el **2027/03/31**.

### 7.6 Fuentes de esta serie

| path en `toy.bandai.co.jp/en/article/detail/?cate=item&path=` | Producto |
|---|---|
| `01_20719` … `01_20737` | los 19 productos DX, en orden de path |
| `bandai.co.jp/candy/products/2026/4570117934254000.html` | SG EGOLGEAR RANDOM BOX 01 |
| `4570117934278000.html` | MINIPLA … 01 (caja yu-dō suelta) |
| `4570117934261000.html` | MINIPLA … 01 SET |
| `bandai.co.jp/candy/camp/2026RED/` | Choco Campaign (premio) |
| `projectred.miraheze.org/wiki/Kakuseihunter_Omegahorn` | wiki — solo dudas |

---

## 8. Lo aprendido

Errores reales de este repositorio. Media docena se evitan solo con saber que
existen.

### Correcciones de criterio

**Confundir el documento de contexto con un encargo.** Un `.md` que aparece en
el proyecto es contexto para cargar, no una petición de ejecutar lo que
describe. Leer, confirmar en corto, esperar.

**Dar por sobrante una copia que debía quedarse.** El Zetsu-Enkaku tenía carpeta
y ficha duplicadas y se marcó como error. Myth ya tenía el caso resuelto con
`alsoIn`: las dos copias se quedan. Lo que sí estaba mal era que **no
coincidían**. → *Antes de declarar que algo sobra, buscar si el sistema anterior
ya resolvió ese caso.*

**Llamar mal colocada una ficha que estaba bien.** La caja individual de Minipla
estaba en `SG YU-DO` y se señaló como error; la categorización era correcta. →
*Una categoría que no entiendo no es una categoría equivocada.*

**Tratar las colecciones secundarias como categorías.** El error de arquitectura,
y el que obligó a cambiar la base de la plantilla. Se detectó **antes** de
escribir nada, al analizar Myth a fondo; con el catálogo ya escrito habría
costado el triple.

**Atenuar con opacidad lo que debía distinguirse por color.** Ver §2.

### Correcciones de datos

**El precio de los yu-dō** (§7.3) y **una línea de producto que se dio por
inexistente**: se escribió que la serie solo tenía DX porque SG no aparecía en
las fichas que había delante.

**Un día de salida inventado** que se coló en la cabecera como si fuera cierto.
De ahí salió `dateExact`.

### Errores de implementación que solo salieron al medir

Ninguno se vio leyendo el código.

**Una palabra desaparecida.** Un bloque de comentarios escrito con un heredoc de
shell **sin comillas**: las comillas invertidas de `` `contains` `` se ejecutaron
como comando y la palabra se borró del archivo. **Usar siempre `<<'EOF'`.**

**Una errata que sobrevivió varias lecturas.** «Los angeju en si» en un texto de
ayuda, desde el primer commit. Salió al listar los tres textos juntos para
compararlos, no al leer el archivo.

**Portadas por debajo del thumb.** Recortes de una hoja de despiece a ~403 px
para un thumbnail de 700.

**El panel saltaba de alto** al cambiar de pestaña, porque un texto de ayuda
ocupaba tres líneas y los otros dos.

**`flex:1` en la cabecera** estirando las dos barras principales.

**Una regla CSS duplicada** al reescribir un bloque, con la segunda pisando a la
primera.

**Falsos positivos en mis propias herramientas.** El primer script de auditoría
partía los nombres por el primer guion seguido de mayúscula, y `ZETSU-ENKAKU` lo
partía por el sitio equivocado — el error del que la propia plantilla avisa. Y
una comprobación comparó la lista de Git con la del disco sin tener en cuenta
que Git escapa los caracteres no ASCII como `\357\274\206`: 20 archivos parecían
sin rastrear y estaban perfectamente.

### Afirmaciones que resultaron falsas

**«GitHub deja una redirección al renombrar el repositorio».** Cierto para
`github.com/usuario/repo`, que devuelve 301. **Falso para Pages**:
`usuario.github.io/repo-viejo/` pasa a dar 404. Si has compartido la dirección
de la web, renombrar la rompe.

**«El límite son N barras en la cabecera».** Ese número describe el ancho de los
rótulos de *una* serie. Mídelo con los tuyos.

### Lo que se probó y no funcionó

- **Checklists apiladas en un panel.** Quien colecciona una sola no debería
  recorrer las demás.
- **Una rama especial para el gimmick y otra para las categorías.** Funcionaba
  con una colección repartida y se rompió con tres.
- **Atenuar con `opacity` las colecciones secundarias.**
- **Una caja por fila en el panel.** Con veintitantas piezas es un muro.
- **Inventarse un día cuando solo se conoce el mes.**
- **Un encabezado de grupo en una colección de una sola familia.** Repite el
  nombre de la colección y no organiza nada.
- **Desplegable de galería en la tarjeta.** Una tira de miniaturas por tarjeta
  metía una fila de ruido en todas. Se sustituyó por pulsar la portada.
- **Una página por producto.** Es una checklist, no una tienda.
- **Entradas separadas enlazadas con un campo `related`.** Ocupaban tres líneas
  del panel repitiendo enlaces cruzados.
- **Etiqueta «Estimado»** para datos sin confirmar. O se omite, o se pone sin
  anunciarlo.
- **Enlaces de Drive** como origen de las imágenes.
- **Fiarse de una hoja de cálculo de apoyo para los nombres.** Sirve para fechas
  y precios; para nomenclatura transcribe mal la mitad.
- **Exigir que cada ficha se llamara igual que un producto.**

### Lo que sí funcionó del método

**Verificar contra la fuente, no contra la memoria.** Cruzar cada producto con
el número de imágenes que publica su página oficial. Coincidieron todas, y de
paso quedó descartado que los productos con una sola foto estuvieran
incompletos: la web solo publica una.

**Verificar contra el servidor, no contra el disco.** Pedir las 126 rutas a
GitHub Pages tal y como las escribe el `index.html`. Es la única forma de
detectar una mayúscula mal puesta.

**Ejecutar la lógica, no leerla.** Marcar productos en el navegador y mirar qué
se cubre, en vez de razonar sobre el código.

> Aviso ganado por las malas: **las transiciones CSS no avanzan en una pestaña
> en segundo plano.** Si un acordeón parece no abrirse, descarta eso antes de
> buscar el fallo en tu CSS.

**Generar las rutas con un script en vez de escribirlas.** Las 101 rutas de
imagen salieron de leer el disco. Cero erratas.

**Cerrar las dudas con evidencia, no con probabilidad.** Lo de Zetsu-Soukaku
aguantó tres rondas independientes.

---

## 9. Publicación

```
se sube          index.html + los .webp + tools/ + este .md
se queda local   originales + FICHA/ + hojas de cálculo de apoyo
```

El `.gitignore` filtra por patrón, así vale para lo que añadas dentro de meses.
**Git no es la copia de seguridad** de los originales: están ignorados a
propósito y necesitan respaldo aparte.

Publicado en **https://leonato312.github.io/Project-Red_Omegahorn_Checklist/**,
repo `leonato312/Project-Red_Omegahorn_Checklist`, Pages desde `main` / root.
101 fotos: 94,8 MB de originales → 16,7 MB en WebP, un 82 % menos. Despliegue
total sin `FICHA/` ni originales: 18,1 MB.

Tras un push que renombra rutas, Pages tarda uno o dos minutos: **un 404 justo
después de subir no es un fallo**.

**Renombrar el repositorio rompe la URL de Pages** (§8). Decide el nombre antes
de compartirla.

---

## 10. Qué decidir al arrancar una serie nueva

1. **¿Cuáles son los coleccionables, y cuál es el principal?**
2. **¿Cada coleccionable está repartido entre productos, o cada producto es una
   pieza?** Lo primero va en `PIEZAS_CATALOG` con su `collection`; lo segundo en
   `PRODUCT_CHECKLISTS`. **Es la pregunta que decide si hay que tocar el motor.**
3. **¿Qué familias tiene cada colección, y bajo qué criterio?**
4. **¿Hay líneas que saquen piezas exclusivas?** Contadores separados.
5. **¿Qué categorías, y en qué orden dentro del mes?** Y cuál lleva distintivo
   en `CATEGORY_BADGE` — las que no sean de una línea, ninguno.
6. **¿Cuáles son caja sorpresa de verdad?** Solo si el contenido es azar.
7. **¿Hay sets que traigan dentro otros productos?**
8. **¿Hay reediciones?** Van como `variants`, no como entradas.
9. **¿Qué colores?** Los dos más fuertes para el principal.
10. **Clave de `localStorage`.**

### Pasos

1. **`git init` y primer commit antes de nada.**
2. Copiar de aquí: `index.html`, `tools/`, `.gitignore` y este documento
   renombrado.
3. Vaciar `PIEZAS_CATALOG` y `PRODUCTS`; reescribir el Bloque 1 con las
   respuestas de arriba.
4. Ajustar `COLECCIONES`, `FAMILIAS`, `LINES`, `CATEGORY_BADGE` y los tokens de
   color. Cambiar `STORAGE_KEY`, el `<title>` y la cabecera.
5. Crear las categorías en mayúsculas, cada una con su `FICHA/`.
6. Cargar la primera wave siguiendo el ciclo del §1.
7. Repositorio público y Pages desde `main` / root. Verificar contra el
   servidor.
8. **Sustituir el §7 por el de la serie nueva** y borrar lo que no aplique.
