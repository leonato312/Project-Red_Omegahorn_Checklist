# Cómo funciona el motor · y de dónde viene

Documento de dos caras:

- **Referencia del motor de Omegahorn.** Los §§1–3 describen una arquitectura
  que Omegahorn hereda casi intacta, así que valen igual para leer su
  `index.html`. Solo hay que traducir dos nombres: donde dice `EGGS_CATALOG`,
  aquí es `PIEZAS_CATALOG`, y donde dice `EGGS_LINES`, es `LINES`.
- **Registro histórico.** Nació como el análisis de Kamen Rider Myth y el plan
  para adaptarlo. Se conserva porque explica **por qué** Omegahorn se separó de
  Myth, y ese razonamiento es lo que hace falta la próxima vez que haya que
  decidir si algo se generaliza o se copia.

**Para arrancar una serie nueva no se lee esto, se lee `PROJECT-RED.md`**, que
ya parte de Omegahorn. Esto es el porqué; aquello es el cómo.

Base del análisis: `D:\DG\Kamen Rider_Myth` — `index.html` (2.261 líneas),
`tools/` (3 scripts, 498 líneas), `.gitignore` y la estructura en disco.

---

## 1. Cómo está montado el `index.html`

Un solo archivo, cuatro capas, con numeración de bloques en los comentarios:

| Líneas | Bloque | Qué hay |
|---|---|---|
| 32–625 | CSS, 8 secciones | tokens → base → cabecera → acordeón → tarjetas → sub-acordeón → visor → panel → responsive |
| 627–725 | **Bloque 1 · Configuración** | todas las constantes que se tocan al cambiar de serie |
| 726–810 | **Bloque 2 · `EGGS_CATALOG`** | catálogo maestro del coleccionable |
| 811–1350 | **Bloque 3 · `PRODUCTS`** | los productos, agrupados por mes en comentarios |
| 1352–1394 | **Bloque 4 · Estado** | `localStorage`, carga y guardado |
| 1395–1503 | **Bloque 5 · Índices** | derivados: cobertura, variantes, progreso |
| 1504–1567 | **Bloque 6 · Utilidades** | escape, precio, fechas, meses |
| 1568–1788 | **Bloque 7 · Render catálogo** | mes → subcategoría → tarjeta |
| 1789–1964 | **Bloque 8 · Render checklist** | panel lateral y pestañas |
| 1965–2239 | **Bloque 9 · Eventos** | acordeón, estados, visor, panel |
| 2240–2261 | **Bloque 10 · Arranque** | `init()` |

El `<body>` es mínimo: cabecera, `<main id="catalog">` vacío, el visor, el
backdrop y el `<aside id="panel">`. **Todo el contenido se genera desde JS.**

---

## 2. El flujo de datos — lo que de verdad hay que entender

```
PRODUCTS[].date  ──> p.month = date.slice(0,7)  ──> acordeón de meses
                     (línea 1349, una sola línea)

PRODUCTS[].contains ─┐
                     ├─> ownedVariantSet() ─> eggsStatus() ─> checklist + barras
EGGS_CATALOG ────────┘

PRODUCTS[].reemplaza ──> coveredMap() ──> isResolved() ──> "cubierto" + contadores

PRODUCTS[].contains ──> SOURCES ──> salto desde la checklist al producto
```

**La regla de oro, y está escrita en el propio archivo:** solo se persiste
`{products:{id:estado}, ui:{...}}`. *La checklist nunca se guarda: se deriva de
los productos en cada render.* Por eso marcar un set actualiza sola la lista de
piezas y nunca se desincroniza.

`loadState()` además **descarta ids que ya no existen**, para que renombrar un
producto no deje basura invisible en el guardado.

---

## 3. Los tres mecanismos de checklist que ya existen

**a) Coleccionable repartido** — `EGGS_CATALOG` + `contains`. La pieza no tiene
producto propio; el progreso se deriva. Soporta `variants` (una línea del panel,
cualquier versión la marca) y `line` (DX/SG con contadores separados).

**b) Checklist de producto** — `PRODUCT_CHECKLISTS` + `catProgress(cat)`. Cada
producto de una categoría **es** la pieza. Se usa para TAF, SO-DO, Buckles y
Vinyl.

**c) Cobertura** — `reemplaza` + `coveredMap()`. Recursivo con corte de ciclos
(`vistos`), así que la cadena se resuelve sola declarando solo lo directo. Un
producto cubierto cuenta como conseguido en la checklist, pero en la tarjeta se
atenúa con «Ya lo tienes: viene en X».

---

## 4. El problema estructural de Omegahorn — y por qué cambia la plantilla

Esta sección es la razón de que `PROJECT-RED.md` ya no parta de Myth.

**Los coleccionables secundarios de Omegahorn no encajan en el mecanismo (b).**

En Myth funcionaba porque TAF, SO-DO, Buckles y Vinyl son categorías donde
un producto = una pieza. En Omegahorn no:

| Pieza secundaria | Aparece en |
|---|---|
| Kakuzyu Enkaku | `DX MEGA FLAME HORN ENKAKU` · `ENKAKU ＆ OMEGAHORN SET` · `EGOLGEAR SET` |
| Omega Horn | `DX OMEGAHORN` · `ENKAKU ＆ OMEGAHORN SET` · `EGOLGEAR SET` |
| Kakuzyu Enkaku (SG) | `YU-DO … ENKAKU` · `MINIPLA … SET` |

Son piezas repartidas entre productos, exactamente como los EgolGear. Necesitan
el mecanismo **(a)**, no el **(b)**.

### La adaptación mínima

Generalizar `EGGS_CATALOG` a un `PIEZAS_CATALOG` con un campo `collection`:

```js
const COLECCIONES = {
  "egolgear":     { label:"EgolGear",      principal:true },
  "kakuzyu": { label:"Kakuzyu" },
  "omegahorn":    { label:"Omegahorn" }
};
```

Cada pieza declara `collection`, `type`, `line` y opcionalmente `variants`.
Los productos siguen declarando **un solo `contains`** con piezas de las tres
colecciones mezcladas — el motor no necesita distinguirlas al marcar.

Qué hay que tocar, y no es mucho:

| Función | Cambio |
|---|---|
| `lineProgress(line, owned)` | añadir parámetro `collection` y filtrar por él |
| rama `if(activa.id === "eggs")` del panel | parametrizar por colección en vez de hardcodear |
| `miniStats` | recorrer `COLECCIONES` × `EGGS_LINES` |
| `CHECKLIST_TABS` | una pestaña por colección |

**Todo lo demás sigue igual**: `contains`, `coveredMap`, `SOURCES`, `variants`,
`normalizeRef`, el visor, el acordeón y los eventos no se enteran del cambio,
porque para ellos una pieza es una pieza.

**Cuidado con la cabecera.** Tres colecciones × dos líneas son seis barras, y el
§3 de la plantilla avisa de que con seis barras gritando igual se pierde cuál
importa. Propuesta: EgolGear DX y SG con los colores fuertes y barra propia;
Kakuzyu y Omegahorn en una sola barra cada una, sin partir por línea, en
tonos suaves.

---

## 5. Mapa de configuración · Myth → Omegahorn

Todo esto vive en el Bloque 1 y es lo único que se reescribe.

| Constante | Myth | Omegahorn |
|---|---|---|
| `STORAGE_KEY` | `"krmyth-catalog-v1"` | **`"omegahorn-catalog-v1"`** |
| `CATEGORY_ORDER` | 12 categorías | `TAF · SOFTVINYL · SG MINIPLA · SG YU-DO · SG RANDOM BOX · DX SETS · DX MECHAS · DX EGOLGEAR SETS · EGOLGEAR PROMOCIONALES` |
| `RANDOM_BOX_CATEGORIES` | SG y DX RANDOM BOX | **solo `SG RANDOM BOX`** — ver §6 |
| `MONTHS` | jul–nov 2026 | jul · ago · sep · oct 2026 |
| `EGGS_TYPES` | 5 tipos de Eggs | `egolgear` · `egolgear-kakuju` · `zetsu-egolgear` |
| `EGGS_LINES` | `{DX, SG}` | igual |
| `COMPONENTES` | Drivers y Buckles | **probablemente vacío** — ver §6 |
| `CHECKLIST_TABS` | Eggs + 4 categorías | EgolGear · Kakuzyu · Omegahorn |
| `PRODUCT_CHECKLISTS` | TAF, SO-DO, Buckles, Vinyl | **ninguna de momento** — TAF y SOFTVINYL tienen 1 producto cada una |
| `STATES` | pending/reserved/owned | igual |
| `CURRENCY` | ¥ / ja-JP | igual |

### Tokens de color

```css
--dx:  #f0b429;   /* oro  -> pasa a ROJO     */
--sg:  #35d0d8;   /* cian -> pasa a TURQUESA */
--taf --sodo --buckles --vinyl   /* se reemplazan por los de las colecciones
                                    secundarias, en tonos suaves */
```

El resto de tokens (superficies, texto, estados, métricas) se hereda tal cual:
son neutros y no tienen nada de Myth.

---

## 6. Cosas que encontré y hay que resolver

**El precio de los yu-dō está mal en el registro.** Anoté 418 para cada uno de
los tres productos, pero `YU-DO … ENKAKU` son las cajas ① ② ③, o sea **3 × 418 =
1.254**. Igual `… OMEGAHORN` son 2 × 418 = **836**, y solo `… CAPTAIN OMEGAHORN`
cuesta 418 de verdad. Hay que corregirlo antes de escribir `PRODUCTS`.

**Los yu-dō no son caja sorpresa.** La foto de la caja lleva
`この箱の中には ① が入っています` — el número va impreso fuera, así que se elige.
Por eso `SG YU-DO` **no** entra en `RANDOM_BOX_CATEGORIES`: si entrara, la
tarjeta diría «Ver posibles contenidos» y trataría un contenido garantizado como
una lotería.

**`COMPONENTES` se queda casi vacío, y es una mejora.** En Myth existía porque
Drivers y Buckles no eran Eggs y la auditoría no podía deducir la cobertura sin
ellos. En Omegahorn los Kakuzyu y el Omega Horn **sí** son coleccionables,
así que van en `contains` y la auditoría 3b deduce la cadena de Enkaku sola:

```
DX MEGA FLAME HORN ENKAKU  {kakuzyu-enkaku}
DX OMEGAHORN               {omegahorn, egolgear-enkaku}
  ⊂ ENKAKU ＆ OMEGAHORN SET  {kakuzyu-enkaku, omegahorn, egolgear-enkaku}
    ⊂ EGOLGEAR SET           {… + 5 gears}
```

**El promocional no tiene fecha exacta y el motor la exige.** `p.month` sale de
`date.slice(0,7)` y no hay rama para fechas parciales. Opciones: darle un día
convencional de septiembre, o dejarlo fuera del catálogo hasta que se concrete.

**Los productos de imagen suelta no los cubren las herramientas.** `plan.py`
mapea `id → carpeta`, así que los productos sin carpeta —como será el
promocional— **no pasan por `build_all.py`**. En Myth hay 4 así y sus `.webp`
están generados a mano. Si el promocional se queda como imagen suelta, o se
convierte a mano o hay que extender `plan.py`.

**El espejo de `alsoIn` no se declara en `plan.py`.** El comentario del propio
script lo dice: el Ridewatter sale solo por su categoría primaria, aunque tenga
carpeta espejo. Para Omegahorn eso significa listar `Zetsu-Enkaku` únicamente
bajo `DX SETS`; la copia de `DX MECHAS` se queda sin `.webp`, igual que la de
`TAF` en Myth.

---

## 7. Las herramientas

| Script | Lee | Escribe | Qué hace |
|---|---|---|---|
| `audit.py` | `index.html` + disco | nada | 4 secciones + una 3b |
| `plan.py` | disco | nada | portada y galería que saldrían |
| `build_all.py` | `plan.py` | `.webp` + `index.html` | convierte y repunta rutas |

`audit.py` comprueba, en este orden: (1) rutas referenciadas que no existen,
`.webp` huérfanos y carpetas que el HTML ignora; (2) portada y numeración;
(3) el árbol de `reemplaza` con detección de ciclos e ids inexistentes;
(3b) cobertura **deducida** comparando conjuntos de contenido; (4) nomenclatura
y duplicados entre categorías. Salida ordenada por severidad ALTO/MEDIO/BAJO.

`build_all.py` genera `<nombre>.webp` a 1600 px calidad 80 y
`<nombre>-thumb.webp` a 700 px calidad 82, salta `FICHA/`, **no renombra ni
borra nada**, y luego reescribe `img:` y `gallery:` en el HTML con expresiones
regulares ancladas al `id` del producto. Al final verifica rutas rotas y calcula
el peso de despliegue.

**Nota sobre el escalado:** `escala = min(1.0, lado/max(w,h))` — nunca amplía.
Nuestros originales son de 1500 px (Bandai juguetes) y 1200 px (Bandai Candy),
así que las galerías se quedarán por debajo de los 1600 nominales. No es un
fallo; es que no hay más resolución publicada.

---

## 8. Detalles de implementación que conviene no perder

- **Sin `loading="lazy"` en las portadas.** Las tarjetas viven dentro de un
  acordeón con `max-height:0` y el navegador no las pediría hasta hacer scroll.
- **La galería sí se difiere de verdad**: el visor solo pide la foto al abrirse.
- **`updateCardUI` + `refreshCoverage` en vez de re-render completo**, para no
  cerrar los `<details>` abiertos ni perder el scroll.
- **`querySelectorAll("[data-pid]")`, nunca `getElementById`**: un producto con
  `alsoIn` tiene varias tarjetas y todas deben reflejar el mismo estado.
- **Volver a pulsar el estado activo lo devuelve a `pending`.**
- **`esc()` en todo lo que venga de datos** antes de inyectarlo.
- El texto del desplegable cambia según sea caja sorpresa («posibles
  contenidos») o set («Eggs incluidos»): llamarlos igual daría a entender que un
  set es una lotería.

---

## 9. Orden de trabajo — estado

| # | Paso | Estado |
|---|---|---|
| 1 | `git init` y primer commit | hecho |
| 2 | Motor escrito desde cero heredando el sistema | hecho |
| 3 | Bloque 1 reescrito con la tabla del §5 | hecho |
| 4 | `PIEZAS_CATALOG` con `collection` | hecho |
| 5 | Catálogo de piezas: 44 en tres colecciones | hecho |
| 6 | `PRODUCTS`: 25 productos, precios de yu-dō corregidos | hecho |
| 7 | `tools/` con las 25 carpetas y el suelto | hecho |
| 8 | `audit.py` → `plan.py` → `build_all.py` → `audit.py` | hecho, sin incidencias |
| 9 | Repositorio público y GitHub Pages desde `main` / root | hecho |

Publicado en **https://leonato312.github.io/Project-Red_Omegahorn_Checklist/**. Las 126
rutas de imagen verificadas contra el servidor: todas 200, ninguna mayúscula
mal puesta.

### Los dos huecos de las herramientas de Myth, arreglados

- **Productos de una sola imagen.** En Myth no pasaban por `plan.py` y sus
  `.webp` se generaban a mano. Aquí `plan.py` tiene un diccionario `SUELTO`
  aparte de `CARPETA` y `build_all.py` los convierte igual que a los demás.
- **Falsos positivos de la auditoría.** La copia espejo de un producto cruzado
  ya no sale como «carpeta que el HTML no referencia»: `audit.py` deduce los
  espejos desde `alsoIn` y los reconoce. Tampoco marca los productos de una
  imagen como archivos perdidos.

`audit.py` además comprueba ahora la integridad del catálogo de piezas
—referencias huérfanas, piezas que ningún producto trae, familias sin
etiqueta— y devuelve código de salida 1 si hay algo en ALTO, para poder
encadenarlo.

### Resultado de la conversión

101 fotos: **94,8 MB de originales → 16,7 MB en WebP**, un 82 % menos. Más
1,23 MB de portadas. Despliegue total, sin `FICHA/` ni originales: **18,1 MB**.

---

## 10. Qué hereda la próxima serie

Lo que sigue es el resumen de este documento en forma de decisión, para no
tener que releerlo entero.

**Se copia tal cual de Omegahorn:**

| Qué | Por qué |
|---|---|
| El motor entero, Bloques 4 a 10 | estado, cobertura, render, eventos y visor no saben de qué serie son |
| Las tres herramientas | ya cubren carpetas, archivos sueltos y copias espejo |
| Los tokens neutros del CSS | superficies, texto, estados y métricas no tienen nada de Omegahorn |
| `.gitignore` | filtra por patrón |

**Se reescribe:**

| Qué | Cuánto |
|---|---|
| `COLECCIONES`, `FAMILIAS`, `LINES` | una entrada por coleccionable de la serie |
| El resto del Bloque 1 | categorías, meses, clave de `localStorage`, colores |
| `PIEZAS_CATALOG` y `PRODUCTS` | los datos, que es el trabajo de verdad |
| `CARPETA` y `SUELTO` en `plan.py` | una línea por producto |
| Cabecera, `<title>` y los tres textos de ayuda | |

**Lo que no hay que volver a decidir**, porque ya está decidido y razonado en
`PROJECT-RED.md`: que la checklist se deriva y no se guarda, que el mes es la
categoría raíz, que la cobertura es transitiva y se declara solo hacia abajo,
que las piezas de una caja sorpresa son entradas separadas, que las familias se
definen por criterio y no por lista, y que la jerarquía visual la dan el color y
el ancho, nunca la opacidad.

**La pregunta que decide si hay que tocar el motor** es la del §9.2 de la
plantilla: *¿cada coleccionable está repartido entre productos, o cada producto
es una pieza?* Si todos los coleccionables de la serie nueva caben en alguno de
los dos mecanismos que ya existen, el motor no se toca. Solo si aparece un
tercer tipo de coleccionable que no encaje en ninguno habría que generalizar
otra vez — y entonces conviene escribir aquí por qué, como se hizo con esto.
