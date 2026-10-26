# BOCETO DEL PROYECTO FINAL — Laboratorio de Computación Gráfica

**Tema:** Deportes
**Espacio recreado:** Estadio de fútbol (fachada exterior + interior / cancha)
**Equipo:** 2 integrantes
**Base de código:** la proporcionada por el profesor (obligatoria)
**Entrega:** ver §9 (⚠️ verificar fecha con el profesor)

---

## 1. Idea en una frase

Recreación 3D en **OpenGL** de un estadio de fútbol: su **fachada** (cúpula obround con
letrero) y su **espacio interior** (césped demarcado, gradas, cubierta con luminarias,
marcador LED y ambientación de partido), con **10 objetos modelados** y **5 animaciones**
(3 sencillas + 2 complejas) generadas por código, sobre el código base del profesor.

---

## 2. Imágenes de referencia

Guardadas en `referencia/`. Son las que se presentan en la portada del manual.

| Archivo | Qué muestra | Fuente | Licencia |
|---|---|---|---|
| `referencia/fachada.jpg` | **Fachada**: cúpula/obround, letrero, accesos, estacionamiento | Wikimedia Commons – *EstadioAkronGDL.jpg* (HugoGN12) | CC BY-SA 4.0 (exige atribución) |
| `referencia/espacio.jpg` | **Espacio**: cancha, gradas, cubierta, luminarias, marcador, ambientación | Wikimedia Commons – *Estadio Akron 02-07-2022 cabecera sur lado derecho.jpg* (Alejan98) | CC0 (dominio público) |

**Nota sobre marcas:** en el modelo se usará un nombre genérico (`ESTADIO NORTE` o similar)
en marcador/fachada, para no reproducir logotipos de terceros.

---

## 3. Objetos evaluables (mín. 7 → vamos por 10)

> Regla del reglamento: *los objetos repetidos cuentan como uno* y *puertas, ventanas,
> chimeneas, escaleras y detalles de ambientación NO cuentan*.

| # | Objeto | ¿Dónde está en la referencia? | Origen | Estado |
|---|---|---|---|---|
| 1 | **Cancha de fútbol** (césped con franjas + demarcaciones: círculo central, áreas, penales) | centro de `espacio.jpg` | ya modelada | ✅ `stadium_model.py` / `estadio.blend` |
| 2 | **Gradas con butacas** (anillo inferior + superior, color rojo) | alrededor de la cancha | parcial | ⚠️ `estadio.blend` tiene escalones; **faltan las butacas individuales** |
| 3 | **Cubierta / techo** con ribos y perfilería (la gran losa superior) | parte alta de ambas fotos | ya modelada | ✅ `stadium_model.py` → colección `STADIUM_ROOF` |
| 4 | **Fachada exterior** (envolvente obround + banda de acento, columnas, accesos) | `fachada.jpg` | ya modelada | ✅ `stadium_model.py` → `STADIUM_FACADE/COLUMNS/ENTRANCES/EXTERIOR` |
| 5 | **Marcador LED** sobre el anillo + pantallas laterales | fondo de `espacio.jpg` | ya modelado | ✅ `scoreboard_model.py` / `scoreboard.blend` |
| 6 | **Arco con red** (2 en la cancha, cuentan como 1) | ambos fondos de la cancha | **falta** | ❌ por modelar |
| 7 | **Carrito de emergencias** (golf médico, cruce roja y baliza) | borde de cancha en `espacio.jpg` | ya modelado | ✅ `carrito_model.py` / `carrito_emergencias.blend` |
| 8 | **Márquitas publicitarias perimetrales** (banners LED alrededor del pasto) | perímetro de la cancha | **falta** | ❌ por modelar |
| 9 | **Luminarias / focos** bajo la cubierta | borde de la cubierta | **falta** | ❌ por modelar (además da pie a la animación de luces) |
| 10 | **Bandera de córner** (2, cuentan como 1) | esquinas de la cancha | **falta** | ❌ por modelar |
| 11 | **Balón de fútbol** | sobre el pasto | reutilizable | ✅ hay `ball.obj` en las prácticas (p9/p10) |
| 12 | **Podio y trofeo** (ambientación de ceremonia de premiación) | no está en la foto; es ambientación extra | ya modelado | ✅ `podio-y-trofeo.blend` |

**Cómodo:** con los 10 primeros ya pasamos el mínimo de 7 con holgura, y dos de ellos
(cancha, gradas) ya están hechos.

### Detalles que NO cuentan como objetos (pero sí se modelan para el realismo)
Túnel de acceso, puertas de gradas, escaleras/vómitos, barandas, línea de fondo,
tecnología de transmisión (plataforma/cámara), césped perimetral, bancos de suplentes.

---

## 4. Animaciones (5 obligatorias: 3 sencillas + 2 complejas)

Todas **generadas por código**, con coherencia con el contexto (nada de "rotación sin
sentido"), siguiendo el patrón de `p9/p10 KeyFrames.cpp` y `Maquina de estados.cpp`.

### Sencillas
| ID | Animación | Técnica |
|---|---|---|
| **S1** | **Marcador LED**: marcador 0-0 → gol, y cronómetro corriendo | cambio de "dígitos" (UV/segmentos) + parpadeo del segundero; temporización por `deltaTime` |
| **S2** | **Banderas de córner ondeando** | oscilación senoidal con amplitud decreciente hacia el asta (deformación por vértices o rotación por tramos) |
| **S3** | **Encendido de luminarias** | rampa de intensidad (`fade-in`) + flicker aleatorio sincronizado entre torres |

### Complejas (más allá de transformaciones básicas o trayectorias lineales)
| ID | Animación | Por qué es compleja |
|---|---|---|
| **C1** | **Recorrido del carrito de emergencias** por la vía perimetral | trayectoria **curva paramétrica** (Catmull-Rom/Bézier) con orientación tangente + balanceo por suspensión + máquina de estados (espera → acelera → dobla → frena) + estrobo parpadeando |
| **C2** | **Ceremonia de premiación**: el trofeo asciende al podio con **confeti** | easing no lineal (subida con rebote) + **sistema de partículas** (≈200 confetis con gravedad, rotación, deriva y "desvanecimiento"), todo por código |

> Alternativa a C2 si no se quiere el podio: **tiro libre del balón** (balística + efecto
> Magnus + rebote en el travesaño + red vibrando). Decidir en la Fase 2.

---

## 5. Stack técnico y código base

- **Lenguaje/graphics:** C++11, OpenGL 3.3 core, GLFW, GLEW, GLM, Assimp (carga `.obj`),
  SOIL2/stb_image (texturas).
- **Código base del profesor (obligatorio, no se reescribe desde cero):**
  `Camera.h`, `Shader.h`, `Mesh.h`, `Model.h`, `SOIL2/`, `stb_image.h`, `Shader/`
  (lighting.vs/frag, lamp.vs/frag, modelLoading) y el esqueleto de
  `p8/fuentesDeLuz.cpp` + `p9-p10/KeyFrames.cpp` + `Maquina de estados.cpp`.
  → Origen: `p8/` (iluminación+modelos) y `p10/` (animación).
- **Build:** `build.sh` igual al de `p8/` → genera **un ejecutable** (`./estadio`),
  sin depender de carpeta `Debug/` de Visual Studio.
- **Modelado:** Blender con los scripts Python ya escritos (`stadium_model.py`,
  `scoreboard_model.py`, `carrito_model.py`) → export a `.obj + .mtl` para Assimp.
- **Assets externos:** Poly Haven (texturas/HDRI CC0), Poly Pizza / Sketchfab (modelos
  con licencia CC0/CC-BY). **Cada objeto < 100 MB.**

---

## 6. Estructura propuesta del repositorio (GitHub)

```
proyecto-final-grafica/
├── README.md                  ← liga para Classroom
├── build.sh                   ← compila → ./estadio
├── main.cpp                   ← base del profesor adaptada
├── Camera.h  Shader.h  Mesh.h  Model.h
├── Shader/                    ← lighting, lamp, modelLoading (.vs/.frag)
├── SOIL2/  stb_image.h
├── Models/                    ← .obj/.mtl/texturas  (<100 MB c/u)
│   ├── cancha.obj  gradas.obj  cubierta.obj  fachada.obj
│   ├── arco.obj  marcador.obj  carrito.obj  butaca.obj
│   ├── marquesina.obj  luminaria.obj  bandera.obj  balon.obj  podio.obj
├── doc/
│   ├── manual-usuario.pdf
│   ├── manual-tecnico.pdf     ← objetivos, flujo, Gantt, alcance, límites,
│   │                             metodología, documentación del código, conclusiones
│   ├── referencia/            ← fotos de referencia + créditos
│   └── diagramas/             ← flujo.png, gantt.png
├── capturas/                  ← imágenes para el video/manual
└── .gitignore                 ← NO subir .zip, Debug/, .blend1, builds
```

---

## 7. Reparto del equipo (2)

| Fase | Integrante A | Integrante B |
|---|---|---|
| 1. Alcance | selección de referencia | checklist del reglamento |
| 2. Modelado | butacas + arco + banderas | márquitas + luminarias + balón |
| 3. Texturizado/UV | pasto, gradas, fachada | accesorios, marcador, carrito |
| 4. Puesta en escena (GL) | carga de modelos, iluminación | cámara, controles, HUD/estado |
| 5. Animaciones | C1 carrito (compleja) | S1/S2/S3 + C2 confeti |
| 6. Documentación | manual técnico (diagramas, Gantt, código) | manual de usuario + README |
| 7. Video / oral | guion + grabación | edición + exponer (5 min) |

---

## 8. Cronograma (diagrama de Gantt)

> ⚠️ **Fecha:** el PDF dice entrega **11 de mayo de 2026**, pero ese día ya pasó
> (el PDF fue impreso el 25/10/2026). Muy probablemente sea **11 de mayo de 2027**:
> **confirmar con el profesor**. El plan de abajo asume ~6 meses de desarrollo.

| Fase | Tarea | Sem 1-2 | Sem 3-4 | Sem 5-6 | Sem 7-8 | Sem 9-10 | Sem 11-12 | Sem 13+ |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| F1 | Referencia + alcance + repo | ██ | | | | | | |
| F2 | Modelado: butacas + accesorios (arco, banderas, marquitas, luminarias) | ██ | ██ | ██ | | | | |
| F3 | Texturizado de toda la escena (césped, asientos, concreto, metal) | | ██ | ██ | ██ | | | |
| F4 | Export .obj + carga en OpenGL + cámara/controles | | ██ | ██ | ██ | | | |
| F5 | Iluminación y materiales (Phong + texturas) | | | | ██ | ██ | | |
| F6 | Animaciones sencillas S1-S3 | | | | | ██ | ██ | |
| F7 | Animaciones complejas C1-C2 | | | | | ██ | ██ | ██ |
| F8 | Pulido, rendimiento, ejecutable | | | | | | ██ | ██ |
| F9 | Manual técnico + manual de usuario | | | | ██ | ██ | ██ | ██ |
| F10 | Video explicativo (30 pts) | | | | | | ██ | ██ |
| F11 | Presentación oral 5 min (40 pts) | | | | | | | ██ |

---

## 9. Checklist de entrega (200 puntos)

**Software funcional (100)**
- [ ] Repo GitHub con commits progresivos (sin .zip, sin carpeta `Debug/`)
- [ ] Ejecutable `./estadio` funcional
- [ ] ≥ 7 objetos distintos con texturizado y geometría adecuada
- [ ] Realismo frente a la imagen de referencia
- [ ] Liga subida a Classroom antes de las 23:59

**Documentación (30)**
- [ ] Manual de usuario (interacción: WASD, mouse, teclas de animación)
- [ ] Manual técnico: objetivos, diagrama de flujo, Gantt, alcance, limitantes,
      metodología aplicada, documentación del código, conclusiones

**Video (30)**
- [ ] Explicación del funcionamiento y las animaciones

**Oral (40)**
- [ ] 5 animaciones (3 sencillas + 2 complejas)
- [ ] Exposición ≤ 5 minutos

**Restricciones a vigilar**
- [ ] Nada de espacios UNAM / gubernamentales
- [ ] Nada de estética retro de videojuego (PS1/N64…)
- [ ] Animaciones coherentes y hechas por código
- [ ] Cada objeto < 100 MB

---

## 10. Inventario de assets que ya existen

| Archivo | Contenido | Ruta |
|---|---|---|
| `stadium_model.py` (789 líneas) | cancha con demarcaciones, 2 niveles de gradas, fachada, columnas, estructura, **cubierta**, accesos y exterior (obround 240×190 m, campo 105×68) | raíz de `grafica/` |
| `scoreboard_model.py` | marcador 13×6 m sobre 2 patas, pantalla LED, parciales y cronómetro | raíz de `grafica/` |
| `carrito_model.py` | golf médico por fases: chasis, carrocería, cabina, detalles médicos | raíz de `grafica/` |
| `estadio.blend`, `scoreboard.blend`, `carrito_emergencias.blend`, `podio-y-trofeo.blend` | escenas ya ejecutadas de los scripts anteriores + podio/trofeo | `teoria/proyectoGrafica/` (repo git propio) |
| `ball.obj` + `grass.jpg` | balón y textura de pasto de las prácticas | `p9`/`p10` |
| Código base | `Camera.h`, `Shader.h`, `Mesh.h`, `Model.h`, `SOIL2/`, `Shader/`, `build.sh`, `fuentesDeLuz.cpp`, `KeyFrames.cpp`, `Maquina de estados.cpp` | `p8/` y `p10/` |

> Pendiente confirmar: ¿`estadio.blend` corresponde a la última versión de
> `stadium_model.py`? Verificar con Blender y reexportar si hace falta.

---

## 11. Próximos pasos (en orden)

1. **Confirmar la fecha de entrega** con el profesor (el PDF dice 11/05/2026 y ya pasó).
2. Crear el repo en GitHub con esta estructura (sin `.zip`, sin `Debug/`).
3. Abrir `estadio.blend` en Blender, verificar que coincide con el script y
   modelar las **butacas** + accesorios (arco, banderas, márquitas, luminarias).
4. Crear el esqueleto del ejecutable copiando la base del profesor (`p8` + `p10`)
   y compilar con `build.sh`.
5. Exportar la cancha a `.obj` y cargarla en OpenGL con textura de césped.
6. Definir la 2ª animación compleja (confeti del podio vs. tiro libre del balón).
