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
