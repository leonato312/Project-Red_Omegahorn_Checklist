# Plantilla de checklist — Project Red

Cómo levantar la checklist de una serie nueva de Project Red.

**El punto de partida es Omegahorn, no Myth.** La primera versión de esta
plantilla salía de Kamen Rider Myth, y al montar Omegahorn quedó claro que
Kamen Rider y Project Red se parecen menos de lo que parecía: Myth tenía **una**
colección repartida y las demás checklists eran categorías donde un producto era
una pieza; Omegahorn tiene **tres** colecciones repartidas y ninguna encaja en
ese molde. El motor de Omegahorn generaliza eso, así que copiarlo ahorra la
reescritura entera.

Del sistema de Myth sobrevive todo lo que era acierto de fondo —el mes como
categoría raíz, la checklist derivada, la cobertura transitiva, el trato de las
imágenes— y está recogido aquí. Lo que no sobrevive es su estructura de datos.

Este documento se copia al repositorio de cada serie nueva y se adapta.

Los otros tres que acompañan a una serie:

| Documento | Qué contiene | Cuándo se lee |
|---|---|---|
| **`PROJECT-RED.md`** | las reglas | al arrancar *(este)* |
| **`BITACORA.md`** | el proceso y los errores que costaron tiempo | **antes de arrancar** |
| **`ADAPTACION.md`** | cómo está construido el motor y por qué | cuando haya que tocarlo |
| **`REGISTRO.md`** | los datos y decisiones de esa serie | al cargar cada wave |

La bitácora no repite las reglas: cuenta en qué orden se hizo Omegahorn y qué
salió mal. Media docena de las correcciones que recoge se evitan solo con
saber que existen.

---

## 0. Antes de nada: un repositorio por serie

**No meter dos series en el mismo catálogo.** Cada una tiene sus coleccionables,
sus líneas de producto y su calendario, y sobre todo: **una serie sigue sacando
producto después de que acabe su emisión**. Si compartieran repositorio, el
catálogo de la vieja seguiría creciendo dentro del de la nueva y el calendario
dejaría de responder a la pregunta que lo justifica.

Consecuencia práctica: cada serie tiene su repositorio, su `index.html` y su
URL. Y **su propia clave de `localStorage`** — si dos catálogos comparten
dominio y clave, se pisan lo que el usuario tenga marcado. Omegahorn usa
`omegahorn-catalog-v1`; el patrón es `<serie>-catalog-v1`.

---

## 1. Para qué existe una checklist así

Dos preguntas, en este orden:

1. **¿Cuándo llega la próxima wave?** Por eso el mes es la categoría raíz y todo
   cuelga de la fecha de salida.
2. **¿Qué me falta de los coleccionables?** Toda serie reparte sus piezas entre
   sets, cajas sorpresa y exclusivas — decenas, imposibles de rastrear a ojo.

Vocabulario, porque significan cosas distintas y se confunden solas: una **wave**
es el ciclo de lanzamientos de un mes, y las **tandas** son los días concretos de
salida dentro de ese mes. Septiembre de Omegahorn es una wave con dos tandas.

---

## 2. El motor: lo que no cambia entre series

### Un archivo, dos listas

`index.html` es HTML5 + CSS3 + Vanilla JS. Sin frameworks, sin build, sin
dependencias. Todo el catálogo se genera desde dos arrays:

- `PIEZAS_CATALOG` — un objeto por pieza coleccionable
- `PRODUCTS` — un objeto por producto

De ahí salen las tarjetas, los contadores, las barras y las checklists.
Mantener el catálogo es editar dos listas.

**Por qué así:** la checklist necesita saber qué piezas trae cada producto. Si
las tarjetas fueran HTML a mano, esa relación viviría en la cabeza de quien las
escribió y se rompería a la tercera wave. Declarada como dato, marcar un
producto actualiza la checklist sola y nunca se desincroniza.

**El coste:** un error de sintaxis deja la página en blanco, porque todo se
genera en tiempo de ejecución. De ahí que el repositorio sea Git **desde antes
de escribir la primera entrada**.

### La regla de oro

Solo se persiste `{products:{id:estado}, ui:{...}}`. **Las checklists nunca se
guardan: se derivan de los productos en cada render.** Todo lo demás —progreso,
cobertura, qué pieza falta— es cálculo. Esa es la razón de que no puedan
desincronizarse.

`loadState()` además descarta ids que ya no existen, para que renombrar un
producto no deje basura invisible engordando el guardado.

### Varias colecciones, un solo mecanismo

Esta es la diferencia grande con Myth y la razón de partir de Omegahorn.

Cada pieza declara a qué **colección** pertenece:

```js
const COLECCIONES = {
  "egolgear":  { label:"EgolGear", principal:true, slug:"egolgear", hint:"..." },
  "kakuzyu":   { label:"Kakuzyu",  slug:"kakuzyu",   hint:"..." },
  "omegahorn": { label:"Omegahorn", slug:"omegahorn", hint:"..." }
};
```

`principal:true` marca el gimmick de la temporada: se lleva los dos colores
fuertes y se parte por línea en la cabecera. Las secundarias van en tonos
suaves y con una barra sola.

Los productos declaran **un único `contains`** mezclando piezas de todas las
colecciones. El motor no necesita distinguirlas al marcar: para él una pieza es
una pieza. El panel se genera recorriendo `COLECCIONES`, así que añadir o quitar
una colección no toca la lógica.

### Modelo de pieza

```js
{ id:"eg-denkaku",
  name:"Denkaku EgolGear",
  collection:"egolgear",   // clave de COLECCIONES
  type:"egolgear",         // clave de FAMILIAS; agrupa dentro del panel
  line:"DX",               // contadores separados por línea
  meaning:"Electric Horn", // opcional, pista bajo el nombre
  variants:[ {id:"std", label:"Estandar"}, {id:"special", label:"Special ver."} ] }
```

### Modelo de producto

```js
{ id:"dx-enkaku-set",         // <línea>-<producto>, minúsculas
  title:"NOMBRE DE LA CAJA",
  category:"CATEGORÍA",       // una de CATEGORY_ORDER
  date:"2026-07-25",          // el mes del acordeón sale de aquí
  dateType:"release",         // "release" | "preorder"
  dateExact:false,            // opcional: mes anunciado, día no. Muestra N/D
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

### Las cuatro reglas del modelo que más se prestan a error

**Líneas separadas.** Si la serie tiene dos líneas que sacan piezas exclusivas
cada una, van con contadores independientes. Fundirlas hace que «me faltan 3» no
signifique nada.

**Variantes contra piezas propias:**

| Situación | Cómo va |
|---|---|
| Misma pieza reeditada, otro acabado | `variants` — una línea, cualquier versión cuenta |
| Piezas que aluden a criaturas o personajes distintos | entradas separadas |
| Piezas distintas de una caja sorpresa | **entradas separadas, siempre** |

Esa tercera fila la aprendimos en Omegahorn con los `Hen'ishu`. En una caja
sorpresa cada pieza es un SKU: si fueran variantes, sacar la normal marcaría la
línea completa mientras te sigue faltando algo que solo se consigue con otra
compra. El contador mentiría.

**Una familia se define por un criterio, no por una lista.** En Omegahorn
`egolgear-kakuju` no es «los que vienen con un mecha» sino «los que pertenecen a
un Kakuzyu del que existe figura». Con un criterio, una pieza migra sola de
familia cuando sale su figura; con una lista, hay que acordarse de moverla.

**Qué alimenta cada checklist.** Solo el coleccionable de verdad. Los accesorios
a escala de una figura no son la pieza: el TAF de Omegahorn trae un «Omega Horn»
que es parte de la figura, no el juguete, y contarlo inflaría el progreso.

---

## 3. Las checklists

**Cada colección en su pestaña, nunca apiladas.** Hay quien sigue una sola, y a
ese pasar por las demás para llegar a la suya no le sirve. Cada pestaña lleva su
contador, su texto de ayuda y su color; el panel recuerda en cuál estabas.

**Iguala el largo de los textos de ayuda.** Si uno ocupa tres líneas y los
demás dos, la cabecera del panel salta de alto al cambiar de pestaña. Ponles
`min-height` y déjalos todos en el mismo número de líneas.

**El color orienta.** Los dos tonos más fuertes son del coleccionable principal;
el resto usa tonos suaves. **No atenúes las secundarias con `opacity`**: lo que
hace que la principal mande es que su color sea el más fuerte y que ocupe más
ancho, no apagar las demás — apagadas se leen como deshabilitadas.

**Sigue existiendo la checklist de producto**, para categorías donde cada
producto **es** la pieza (`PRODUCT_CHECKLISTS` + `catProgress`). Omegahorn la
tiene vacía porque no le hace falta, pero el mecanismo está y funciona.

**Cuidado con «cubierto»:** en la tarjeta significa *no necesitas comprarlo* y
se atenúa; en la checklist significa *lo tienes* y se marca en verde. Misma
información, dos preguntas distintas.

---

## 4. Estructura de carpetas

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
tienen que corresponderse con nada**: una hoja puede cubrir una colección entera.

Aun así conviene nombrarlas `PRODUCTO-Contenido 1, Contenido 2…`: no lo exige
nada, pero al cargar una wave se sabe qué trae cada caja sin abrir la imagen.

**Portada = `PACKAGE` si existe, si no `01`.**

**Las mayúsculas importan.** Windows es case-insensitive y GitHub Pages no: una
mayúscula mal puesta es una imagen que funciona en tu equipo y da 404 publicada.
La auditoría **no** puede detectarlo, porque en tu disco resuelve igual. La
comprobación real es pedirle las rutas al servidor ya publicado.

**Un producto cruzado tiene carpeta espejo.** Si pertenece de verdad a dos
categorías, la carpeta y la ficha se duplican **con el mismo nombre** en ambas, y
el catálogo apunta solo a la primaria con `alsoIn`. La copia espejo se queda sin
`.webp` a propósito.

---

## 5. Imágenes

| Archivo | Lado máx. | Calidad | Para qué |
|---|---|---|---|
| `<nombre>.webp` | 1600 px | 80 | galería, se abre en el visor |
| `<nombre>-thumb.webp` | 700 px | 82 | portada de la tarjeta |

En Omegahorn: 101 fotos de 94,8 MB a 16,7 MB, un 82 % menos. Los originales no
se tocan ni se suben; su respaldo va aparte.

**Comprueba la resolución de origen antes de recortar.** Un panel recortado de
una hoja de despiece puede quedar por debajo de los 700 px del thumb y salir
borroso de portada. Si la galería del producto trae la pieza montada a tamaño
completo, esa es la portada.

### Cinco trampas que costaron horas

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

## 6. Herramientas

Tres scripts de Python con Pillow como única dependencia:

| Script | Qué hace | Escribe |
|---|---|---|
| `audit.py` | Cruza `index.html` con el disco | nada |
| `plan.py` | Muestra qué portada y galería saldrían | nada |
| `build_all.py` | Genera los `.webp` y repunta el HTML | sí |

Los dos primeros son de solo lectura: **correrlos siempre antes**. `audit.py`
sale con código 1 si hay algo en ALTO, así que se puede encadenar.

`plan.py` mapea `id → carpeta` en `CARPETA` y `id → archivo` en `SUELTO`. Los
productos de una sola imagen van en el segundo: en Myth no pasaban por las
herramientas y sus `.webp` había que generarlos a mano.

**Una auditoría con falsos positivos es peor que ninguna.** La de Myth contaba
los `.webp` derivados como fotos y avisaba de huecos inexistentes; con 74 avisos
de los que 70 eran ruido, nadie los lee. La de Omegahorn además reconoce las
copias espejo de `alsoIn` y los productos de una imagen, que la de Myth marcaba
en falso.

### Verificar la cobertura comparando contenidos

Cuando un set trae dentro otro producto se declara con `reemplaza` **en el que
absorbe**, y la cobertura es **transitiva**: basta declarar lo que se absorbe
directamente. Deducir eso a ojo falló dos veces seguidas en Myth, así que la
auditoría lo **deduce** comparando conjuntos de contenido y avisa en los dos
sentidos: cobertura que falta declarar y cobertura declarada que el contenido no
respalda.

En Myth hacía falta el campo `componentes` para eso, porque Drivers y Buckles no
eran Eggs. **Cuantas más cosas sean coleccionables, menos falta hace:** en
Omegahorn los Kakuzyu y el Omega Horn están en `contains`, así que la cadena se
deduce sola y `componentes` quedó casi vacío.

---

## 7. Qué se publica

```
se sube          index.html + los .webp + tools/ + los .md
se queda local   originales + FICHA/ + hojas de cálculo de apoyo
```

El `.gitignore` filtra por patrón, así vale para lo que añadas dentro de meses.
**Git no es la copia de seguridad** de los originales: están ignorados a
propósito y necesitan respaldo aparte.

GitHub Pages desde `main` / root. Tras un push que renombra rutas tarda uno o
dos minutos: **un 404 justo después de subir no es un fallo**.

**Renombrar el repositorio rompe la URL de Pages.** GitHub deja una redirección
para `github.com/...`, pero **no** para `usuario.github.io/repo/`: la dirección
vieja de la web pasa a dar 404. Decide el nombre antes de compartirla.

---

## 8. Nomenclatura

**La romanización sale de la caja, no de la transcripción.** Las páginas en
inglés de Bandai vienen de traductor automático: al Ikaku EgolGear lo llamaron
«Squid Quest Gorgia» y a Saikaku «Horned beast Rhino». Sirven para fechas y
precios; para nombres, manda la caja.

**Dentro de la propia web, la lista de contenidos es más fiable que la
descripción**: conserva las vocales largas que la descripción recorta —Goukaku,
Kyoukaku, Youkaku— aunque falla alguna vez, así que conviene cruzar las dos.

**La wiki de la serie sirve para aclarar dudas, no para alimentar el catálogo.**
Lista personajes que aún no tienen producto, y una pieza que ningún producto
trae no se puede marcar nunca. Vale para confirmar que dos bichos parecidos son
distintos y para resolver grafías.

**Guion en los compuestos cuando la costura no se ve.** `Zetsu-Enkaku`, no
`Zetsuenkaku`. Bandai suele ponerlo en el título de producto y perderlo en los
contenidos.

**Prima que se entienda sobre la fidelidad literal.** El gimmick de Myth se
romaniza «EGZ» y se eligió **Eggs**; el premio de campaña de Omegahorn es
técnicamente un Emolgear de otra serie y se cataloga como **EgolGear**. Cuando
tomes una decisión así, **escríbela en el registro**, o alguien la «corregirá»
meses después creyendo que es una errata.

**Decide la nomenclatura antes de publicar.** Renombrar es barato en local y
caro cuando ya hay enlaces fuera. Y hazlo completo: nombres visibles, nombres de
archivo e identificadores internos. Dejar `horned-beast` por dentro mostrando
«Kakuzyu» por fuera es deuda que se paga sola.

---

## 9. Lo que hay que decidir en cada serie

Esto es lo que **no** se hereda. Responder antes de escribir una línea:

1. **¿Cuáles son los coleccionables, y cuál es el principal?** El principal es el
   gimmick de la temporada. Los demás van como colecciones secundarias.
2. **¿Cada coleccionable está repartido entre productos, o cada producto es una
   pieza?** Lo primero va en `PIEZAS_CATALOG` con su `collection`; lo segundo en
   `PRODUCT_CHECKLISTS`. Myth tenía de los dos tipos; Omegahorn solo del primero.
3. **¿Qué familias tiene cada colección, y bajo qué criterio?**
4. **¿Hay líneas de producto que saquen piezas exclusivas?** DX y SG en las dos
   series hasta ahora. Si las hay, contadores separados.
5. **¿Qué categorías de producto tiene?** En el orden en que quieras verlas
   dentro de cada mes.
6. **¿Cuáles son caja sorpresa de verdad?** Solo si el contenido es azar. Si el
   número va impreso fuera, no lo es.
7. **¿Hay sets que traigan dentro otros productos?**
8. **¿Qué colores?** Los dos más fuertes para el coleccionable principal.
9. **Clave de `localStorage`** propia de la serie.

---

## 10. Arrancar una serie nueva

1. **`git init` y primer commit antes de nada.** Un error de sintaxis deja la
   página en blanco; sin Git no hay a qué volver.
2. Copiar de Omegahorn: `index.html`, `tools/`, `.gitignore` y este documento.
3. Vaciar `PIEZAS_CATALOG` y `PRODUCTS`; reescribir el Bloque 1 con las
   respuestas del §9.
4. Ajustar `COLECCIONES`, `FAMILIAS`, `LINES` y los tokens de color.
5. Cambiar `STORAGE_KEY`, el `<title>` y la cabecera.
6. Crear las categorías en mayúsculas, cada una con su `FICHA/`.
7. Cargar waves: ficha → carpetas con fotos → `audit.py` → entradas en los dos
   arrays → registrar la carpeta en `CARPETA` de `plan.py` → `build_all.py` →
   `audit.py` otra vez.
8. Repositorio público y Pages desde `main` / root. Comprobar las rutas contra
   el servidor, no contra el disco.

**Lo que hace falta de ti para empezar:** las respuestas del §9 y la primera
tanda de fichas.

**Lleva un `REGISTRO.md` desde el primer día.** Los datos recopilados, las
decisiones de nomenclatura ya cerradas y las que siguen abiertas. Es lo que
evita volver a mirar las mismas fichas dos veces y lo que impide que una
decisión deliberada se deshaga por parecer un error.

---

## 11. Lo que se probó y no funcionó

Vale más que la lista de aciertos.

- **Checklists apiladas en un panel.** Quien colecciona una sola no debería
  recorrer las demás para llegar a la suya.
- **Una rama especial para el gimmick y otra para las categorías.** Funcionaba
  en Myth y se rompió en Omegahorn en cuanto hubo tres coleccionables
  repartidos. Generalizar por `collection` es lo que debía haber sido desde el
  principio.
- **Atenuar con `opacity` las colecciones secundarias.** Se leen como
  deshabilitadas. La jerarquía la dan el color y el ancho.
- **Una caja por fila en el panel.** Con 25 piezas en pantalla es un muro. Fondo
  solo al pasar por encima y el estado en el punto.
- **Inventarse un día cuando solo se conoce el mes.** La cabecera anunciaba
  «2 tandas: días 1 y 5» con un día que no existía. Para eso está `dateExact`.
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
- **Exigir que cada ficha se llamara igual que un producto.** Regla inventada
  que hizo gritar a la auditoría durante días.
