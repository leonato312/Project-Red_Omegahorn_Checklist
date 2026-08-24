# Bitácora — cómo se construyó Omegahorn

Los otros tres documentos dicen **qué** hacer. Este dice **qué salió mal por el
camino**, que es lo que no se aprende leyendo el resultado terminado.

Se escribe para la serie siguiente. Casi todo lo de aquí son errores míos que el
usuario tuvo que corregir, y errores que encontré yo al verificar. Cuando montes
la próxima, léelo antes de empezar: la mitad de estas correcciones se evitan
sabiendo que existen.

- `PROJECT-RED.md` — las reglas
- `ADAPTACION.md` — el motor
- `REGISTRO.md` — los datos de esta serie
- **`BITACORA.md`** — el proceso *(este)*

---

## 1. El orden en que se hizo

Diez commits, de la recopilación a la publicación. El orden importa: cada fase
depende de que la anterior esté cerrada.

| Fase | Qué pasó |
|---|---|
| Recopilación | Leer las 20 fichas, cotejar contra las páginas oficiales, montar `REGISTRO.md` |
| Nomenclatura | Fijar grafías **antes** de tocar código |
| Estructura | Carpetas, fotos, auditoría manual |
| Análisis | Leer Myth entero: `index.html`, `tools/`, `.gitignore` |
| Motor | Escribir `index.html` desde cero heredando el sistema |
| Herramientas | `plan.py`, `build_all.py`, `audit.py` |
| Conversión | WebP y repunte de rutas |
| Publicación | Git, GitHub, Pages, verificación contra el servidor |
| Pulido | Vocabulario, estética, documentación |

**Lo que hizo que esto funcionara:** no escribir una línea de código hasta tener
el `REGISTRO.md` cerrado. Cada vez que se adelantó una decisión sin datos, hubo
que deshacerla.

---

## 2. Correcciones de criterio

Las que más costaron. Ninguna se veía en los datos: eran interpretaciones mías
que estaban mal.

### Confundí el documento de contexto con un encargo

Se dejó `PROJECT-RED.md` en la carpeta para que heredara lo aprendido en Myth.
Lo leí como un brief: pedí las respuestas del cuestionario y ofrecí montar el
árbol de carpetas.

**Regla:** un `.md` que aparece en el proyecto es contexto para cargar, no una
petición de ejecutar lo que describe. Leer, confirmar en corto, esperar.

### Di por muerta una copia que debía quedarse

El Zetsu-Enkaku SET tenía carpeta y ficha duplicadas en `DX MECHAS` y `DX SETS`,
idénticas bit a bit. Lo marqué como «sobra una copia».

Estaba mal. Myth ya tenía el caso resuelto con `DX RIDEWATTER EGGS`: **las dos
copias se quedan, con el mismo nombre**, y el catálogo apunta solo a la
primaria con `alsoIn`. Lo que sí estaba mal era que las dos copias **no
coincidían** — a la de MECHAS le faltaba el guion y media lista de contenidos.

**Regla:** antes de declarar que algo sobra, buscar si el sistema anterior ya
resolvió ese caso.

### Dije que una ficha estaba mal colocada cuando no lo estaba

La ficha de la caja individual de Minipla estaba en `SG YU-DO` y la señalé como
error, porque ambas fichas eran de productos ミニプラ. Resulta que a las cajas
individuales se las llama yu-dō precisamente porque a veces salen solo en ese
formato, sin SET que las agrupe. La categorización era correcta y la mía no.

**Regla:** una categoría que no entiendo no es una categoría equivocada.

### Traté las secundarias como categorías, no como colecciones

Este fue el error de arquitectura, y el más caro de haber pasado por alto.

Myth tenía **una** colección repartida (los Eggs) y sus otras checklists eran
categorías donde un producto era una pieza. Copiar eso a Omegahorn no funciona:
el Kakuzyu Enkaku sale en tres productos DX distintos y el Omega Horn en otros
tres. Son piezas repartidas, igual que los EgolGear.

Se detectó al analizar Myth a fondo, antes de escribir nada. Si se hubiera
copiado el `index.html` y adaptado sobre la marcha, se habría descubierto con el
catálogo ya escrito.

**Regla, y es la pregunta del §9.2 de la plantilla:** antes de tocar el motor,
preguntar por cada coleccionable si está repartido entre productos o si cada
producto es una pieza.

### Atenué con opacidad lo que debía distinguirse por color

Puse `opacity:.65` a las barras de las colecciones secundarias para que la
principal mandara. Se leen como deshabilitadas.

Myth no atenúa nada: lo que hace que su coleccionable principal mande es que
oro y cian son los tonos más fuertes y que sus barras ocupan más ancho.

---

## 3. Correcciones de datos

### El precio de los yu-dō

Anoté 418 en los tres productos. 418 es lo que cuesta **una caja**, y cada
producto yu-dō agrupa varias: `… ENKAKU` son tres cajas (1.254), `… OMEGAHORN`
dos (836) y solo `… CAPTAIN OMEGAHORN` una.

Las tres juntas suman 2.508, exactamente lo que cuesta el SET de Minipla. Ese
cuadre es lo que confirma que la cuenta está bien: **si un SET no descuenta
respecto a comprar las partes, sospecha del precio de las partes.**

### Di por buena una línea de producto que no existía

Escribí que Omegahorn tenía «una sola línea de producto (DX)» porque no aparecía
SG en las fichas que había. Existía, y el usuario ya lo había dicho.

### Un día de salida inventado

Cinco productos tenían mes anunciado pero no día. Les puse `2026-09-01` como
ancla para el acordeón, y esa fecha se coló en la cabecera: septiembre anunciaba
«2 tandas: días 1 · 5», con un día que no existe.

Se arregló con `dateExact:false`: la fecha sigue anclando el mes, la tarjeta
muestra **N/D**, y ese día no cuenta como tanda ni alimenta la cuenta atrás.

**Regla:** un dato inventado para que el motor funcione tiene que estar marcado
como inventado, o el motor lo publicará como si fuera cierto.

---

## 4. Nomenclatura: lo que enseñó esta serie

**La web oficial en inglés viene de traductor automático.** Al Ikaku EgolGear lo
llama «Squid Quest Gorgia» y a Saikaku «Horned beast Rhino». Vale para fechas y
precios; para nombres, no.

**Dentro de la propia web, la lista de contenidos gana a la descripción.**
Conserva las vocales largas que la descripción recorta —Goukaku, Kyoukaku,
Youkaku— aunque falló una vez: dijo «Pikakuegorgia» donde la descripción daba
«Bikaku (Beautiful)», y ahí ganó la descripción porque *beautiful* es 美 (bi).
Cruzar las dos siempre.

**La tabla de セット内容 de la caja es la fuente buena.** Fue la que cerró
definitivamente si Zetsu-Soukaku y Zetsu-Goukaku eran la misma pieza: nombra
**ゼツソウカク** en katakana y le pone el sello セット品限定.

**La wiki de la serie aclara dudas, no alimenta el catálogo.** Lista personajes
sin producto, y una pieza que ningún producto trae no se puede marcar nunca.

**Renombrar a medias es peor que no renombrar.** Al cambiar «Horned Beast» por
«Kakuzyu» hubo que tocar los nombres visibles, los de archivo **y** los
identificadores internos, más las clases CSS y el token de color. Dejar
`horned-beast` por dentro mostrando «Kakuzyu» por fuera es deuda que se paga
sola.

**Una decisión deliberada hay que escribirla.** El premio de campaña es
técnicamente un Emolgear de otra serie y se cataloga como EgolGear por
practicidad. Si eso no queda razonado en el `REGISTRO.md`, alguien lo «corrige»
meses después creyendo que es una errata.

---

## 5. Errores de implementación que encontré verificando

Ninguno se vio leyendo el código. Todos salieron al medir.

**Una palabra desaparecida.** Escribí un bloque de comentarios con un heredoc de
shell sin comillas, y las comillas invertidas de `` `contains` `` se ejecutaron
como comando. La palabra quedó borrada del archivo. **Usar siempre `<<'EOF'`.**

**«Los angeju en si».** Palabra inventada en un texto de ayuda, presente desde
el primer commit. Sobrevivió a varias lecturas del archivo y salió al listar los
tres textos juntos para compararlos.

**Portadas por debajo del thumb.** Recorté las portadas de yu-dō de una hoja de
despiece de 1200 px: cada panel salía a ~403 px, por debajo de los 700 px del
thumbnail. La galería del producto tenía las mismas piezas montadas a tamaño
completo. **Comprobar la resolución de origen antes de recortar.**

**El panel saltaba de alto.** Un texto de ayuda ocupaba tres líneas y los otros
dos: la cabecera pasaba de 205 a 222 px al cambiar de pestaña.

**`flex:1` en la cabecera.** Las dos barras de EgolGear se estiraban y rompían
la fila. Myth solo pone `flex:1` dentro de la media query, donde las barras
bajan a su propia fila. En escritorio el ancho lo fija `min-width`.

**Una regla CSS duplicada** al reescribir un bloque, con la segunda pisando a la
primera.

**Mi propia auditoría con un falso positivo.** El primer script partía los
nombres por el primer guion seguido de mayúscula, y `ZETSU-ENKAKU` lo partía por
el sitio equivocado. Irónico, porque el §6 de la plantilla avisa justo de eso.

**Mi propia verificación equivocada.** Comparé la lista de archivos de Git con
la del disco y salieron 20 sin rastrear. Git escapa los caracteres no ASCII como
`\357\274\206`, así que la comparación de cadenas fallaba. Los archivos estaban
perfectamente.

---

## 6. Afirmaciones mías que resultaron falsas

**«GitHub deja una redirección al renombrar el repositorio».** Cierto para
`github.com/usuario/repo`, que devuelve un 301. **Falso para Pages**:
`usuario.github.io/repo-viejo/` pasa a dar 404. Lo comprobé después de que el
usuario ya hubiera renombrado.

**«Una sola línea de producto».** Ver §3.

**«Sobra una de las dos copias».** Ver §2.

---

## 7. Lo que sí funcionó del método

**Verificar contra la fuente, no contra la memoria.** Crucé los 19 productos DX
con el número de imágenes que publica cada página oficial. Coincidieron todos, y
de paso quedó descartado que los dos productos con una sola foto estuvieran
incompletos: la web solo publica una.

**Verificar contra el servidor, no contra el disco.** Pedí las 126 rutas de
imagen a GitHub Pages tal y como las escribe el `index.html`. Las 126 dieron
200. Es la única forma de detectar una mayúscula mal puesta: en Windows resuelve
igual y la auditoría no puede verlo.

**Ejecutar la lógica, no leerla.** Comprobé la cobertura transitiva marcando
productos en el navegador y mirando qué se cubría, en vez de razonar sobre el
código. Ahí se confirmó que el REPLICA SET no cubre el Zetsu-Soukaku.

**Generar las rutas con un script en vez de escribirlas.** Las 101 rutas de
imagen salieron de leer el disco. Cero erratas.

**Git antes de escribir la primera línea.** Todo se genera en tiempo de
ejecución: un error de sintaxis deja la página en blanco.

**Cerrar las dudas con evidencia, no con probabilidad.** Lo de
Zetsu-Soukaku contra Zetsu-Goukaku aguantó tres rondas: la tabla oficial de la
caja, la comparación del arte de las dos piezas lado a lado, y la wiki. Las tres
apuntaban a lo mismo.

---

## 8. Antes de empezar la siguiente

1. `git init` y primer commit vacío.
2. Copiar de Omegahorn: `index.html`, `tools/`, `.gitignore` y los cuatro `.md`.
3. **Responder el §9 de `PROJECT-RED.md` entero antes de tocar código.** Sobre
   todo la 2: ¿cada coleccionable está repartido o cada producto es una pieza?
4. Fijar la nomenclatura y **escribir en el `REGISTRO.md` cada decisión con su
   porqué**, incluidas las que se apartan de la fuente a propósito.
5. Cargar los datos, y solo entonces escribir los arrays.
6. `audit.py` → `plan.py` → `build_all.py` → `audit.py`.
7. Publicar y **verificar las rutas contra el servidor**.

Y una que no es técnica: cuando algo no cuadre, decirlo antes de construir
encima. Casi todo lo de esta bitácora se detectó porque alguien preguntó «¿por
qué esto es así?» en vez de darlo por bueno.
