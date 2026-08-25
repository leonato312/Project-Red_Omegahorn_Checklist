# Actualización pendiente — Kakusei Hunter Omegahorn

**Este documento es una tarea, no documentación.** Se aplica, se verifica y
**se borra**, junto con los archivos que deja obsoletos.

Viene de lo aprendido montando **Gavan Infinity**, la serie siguiente. Nada de
lo que hay aquí es de Gavan: son cosas de uso general que se descubrieron allí y
que este repositorio necesita.

> **Adáptalo a Omegahorn.** Las tablas llevan los valores de esta serie ya
> calculados, pero **revísalos** antes de pegarlos: son mi lectura de tu
> `CATEGORY_ORDER`, no una verdad comprobada contra las cajas.

---

## 1. Lo que ya está copiado en el repositorio

| Archivo | Estado | Qué hacer |
|---|---|---|
| `tools/check_urls.py` | **copiado y probado aquí** | nada, ya funciona |
| `PROJECT-RED.md` | **sustituido** por la versión nueva | leer los §§2, 5, 6 y 10 |

`check_urls.py` se corrió en seco en este repositorio: **126 rutas, 0
discrepancias de mayúsculas.** Confirma lo que ya sabías por haber pedido las
rutas al servidor, pero ahora se comprueba en segundos y sin publicar.

### Por qué hacía falta

`audit.py` usa `os.path.exists`, que **en Windows no distingue mayúsculas**: una
ruta mal capitalizada pasa la auditoría en local y da 404 publicada. Tu propio
`PROJECT-RED.md` §4 dice que la auditoría no puede detectarlo. Ahora sí.

```bash
python tools/check_urls.py
python tools/check_urls.py --servidor https://leonato312.github.io/Project-Red_Omegahorn_Checklist
```

**No lo canalices**: `| tail` se come el código de salida y un fallo pasa por
bueno. Usa `${PIPESTATUS[0]}`.

---

## 2. Lo que hay que aplicar a mano en `index.html`

### 2.1 El distintivo de línea está mal en tres categorías

En la línea 1366:

```js
const isSG = p.category.startsWith("SG");
```

y en la 1375:

```js
isSG ? '<span class="badge badge--sg">SG</span>' : '<span class="badge badge--dx">DX</span>',
```

Todo lo que no empiece por `SG` recibe **DX**. De tus nueve categorías,
**tres no son DX**: el `TOKUSATSU ACTION FIGURE` no es DX, el soft vinyl tampoco,
y el promocional es un premio de campaña.

**Sustituye** las dos líneas y añade el mapa al Bloque 1:

```js
/* Distintivo de linea que lleva la tarjeta, declarado por categoria.
   Sin entrada, sin distintivo: mejor nada que una linea equivocada. */
const CATEGORY_BADGE = {
  "DX SETS":"DX", "DX MECHAS":"DX", "DX EGOLGEAR SETS":"DX",
  "SG MINIPLA":"SG", "SG YU-DO":"SG", "SG RANDOM BOX":"SG"
};
```

```js
const linea   = CATEGORY_BADGE[p.category] || "";
const isPromo = p.category === "EGOLGEAR PROMOCIONALES";
```

```js
linea ? `<span class="badge badge--${esc(linea.toLowerCase())}">${esc(linea)}</span>` : "",
```

**Quedan sin distintivo a propósito:** `TAF`, `SOFTVINYL` y
`EGOLGEAR PROMOCIONALES`.

### 2.2 `reservas`: aquí sí tienes dónde usarlo

Un campo opcional del producto que pinta una línea bajo el precio:

```js
reservas:"cierre de solicitudes: 31 mar 2027",
```

**Tu promocional lo necesita.** El `REGISTRO.md` §6.3 dice que la campaña de la
Choco cierra el **2027/03/31**, y ese dato hoy solo vive en el registro: la
tarjeta no lo dice. Es información accionable —si se te pasa, no lo consigues— y
ahora tiene dónde ir.

El CSS y el punto exacto donde se pinta están en `PROJECT-RED.md` §2. El campo
`exclusiva` que lo acompaña solo hace falta si aparecen exclusivas de P-Bandai;
hoy no tienes.

### 2.3 `LINE_LABEL`: no lo necesitas

Solo hace falta si una clave de `LINES` es compuesta. Las tuyas son `DX` y `SG`.
**Ignóralo.**

---

## 3. Lo que la plantilla nueva trae y te conviene leer

`PROJECT-RED.md` ha crecido de 452 a 665 líneas. Lo nuevo:

| § | Qué |
|---|---|
| Cabecera | el punto de partida pasa a ser **Gavan Infinity**, con el porqué de cada cambio de base |
| **§2** | los tres enganches nuevos y **cuántas líneas caben en la cabecera** |
| **§5** | **de dónde salen las imágenes**: nueve fuentes, qué aporta cada una y sus trampas |
| §6 | cuatro herramientas en vez de tres, con `check_urls.py` |
| §10 | el paso 7 apunta al §5, y recuerda repetir `build_all.py` tras regenerar el catálogo |

El §5 es el que más te va a servir en la próxima wave: el CDN de Akamai por
número de modelo, las cajas de HobbySearch con el sufijo `p`, el geobloqueo de
P-Bandai y cómo rodearlo, y la advertencia de que **el CDN devuelve 200 a
cualquier número de modelo, sea de la serie que sea**.

---

## 4. Verificar antes de dar por bueno

```bash
python tools/audit.py          # debe seguir sin incidencias
python tools/check_urls.py     # 126 rutas, 0 discrepancias
```

Y en el navegador: **una tarjeta de TAF ya no debe decir «DX»**, y las de
`DX MECHAS` y `SG YU-DO` deben seguir bien.

---

## 5. Qué borrar al terminar

### La `PROJECT-RED.md` vieja

**Ya está sustituida**, no hay nada que borrar a mano. Pero si guardaste copia
en algún sitio, tírala: mantener dos plantillas es cómo se desincronizan.

### Este archivo

`ACTUALIZAR.md` se borra cuando los puntos 1 a 4 estén hechos y verificados.

### Lo que NO se borra

- **`ADAPTACION.md`** y **`BITACORA.md`**: son la historia de Omegahorn, no una
  copia de nada. Gavan Infinity tiene los suyos, distintos.
- **`REGISTRO.md`**: tus datos.

---

## 6. Una corrección que le debo a este repositorio

Al leerlo para arrancar Gavan Infinity encontré dos cosas desfasadas en
`REGISTRO.md`, y no las toqué porque no era mi repositorio:

- El **§11 «Lo que falta traer de Myth»** dice que faltan `index.html`, `tools/`
  y `.gitignore`. Los tres están desde hace tiempo.
- El **§9, fila 8** da la clave de `localStorage` por pendiente, y la tabla de
  decisiones cerradas justo debajo ya la fija en `omegahorn-catalog-v1`.

Son dos párrafos. Si alguien lee ese registro dentro de seis meses, van a
confundirle.

---

## 7. Un dato que Gavan Infinity le devuelve a Omegahorn

El premio de la **PROJECT R.E.D. Choco Campaign** es **la misma pieza física** en
las dos series: una cara Gavan Infinity y otra Captain Omegahorn.

Tu copia es la buena —`1798x1012`— y la de la wiki está a `300x564`. Gavan
Infinity la tomó prestada de aquí, no al revés. Queda anotado por si alguna vez
te preguntas por qué esa foto aparece en dos repositorios: **es el mismo objeto**.
