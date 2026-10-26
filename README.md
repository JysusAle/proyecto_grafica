# Estadio Norte — Proyecto Final de Computación Gráfica

Recreación 3D en **OpenGL** de un estadio de fútbol (fachada + espacio interior),
con 10 objetos modelados y 5 animaciones (3 sencillas + 2 complejas) generadas
por código.

**Base de código:** proporcionada por el profesor (prácticas 5–10), sin modificar
los headers `Camera.h`, `Shader.h`, `Mesh.h`, `Model.h` ni las librerías `SOIL2/`
y `stb_image.h`.

## Requisitos

- g++, pkg-config
- `libglfw3-dev`, `libglew-dev`, `libglm-dev`, `libassimp-dev`

## Compilar y ejecutar

```bash
./build.sh      # genera ./estadio
./estadio
```

El ejecutable no depende de ninguna carpeta `Debug/`: todo se genera con `build.sh`.

## Controles

| Tecla | Acción |
|---|---|
| `W A S D` / flechas | mover la cámara |
| ratón | rotar la cámara |
| `ESC` | salir |
| `ESPACIO` | color de la luz puntual (base del profesor) |
| `1` | S3 — encendido de luminarias |
| `2` | S1 — marcador LED *(pendiente)* |
| `3` | S2 — banderas de córner *(pendiente)* |
| `4` | C1 — recorrido del carrito *(pendiente)* |
| `5` | C2 — ceremonia / confeti *(pendiente)* |

## Estructura

```
main.cpp        escena, iluminación y animaciones (base: p8/fuentesDeLuz.cpp + p10)
Camera.h        navegación en primera persona        [del profesor]
Shader.h        carga de shaders                     [del profesor]
Mesh.h          malla + VAO/VBO                      [del profesor]
Model.h          carga de modelos con Assimp          [del profesor]
Shader/         lighting.*, lamp.*
SOIL2/          carga de texturas
Models/         .obj + .mtl + texturas (< 100 MB c/u)
referencia/     imágenes de referencia del proyecto
doc/            manuales, diagramas de flujo y Gantt
BOCETO.md       plan del proyecto
```

## Modelo de trabajo

1. Se modela en **Blender** (scripts en la raíz del repo de prácticas:
   `stadium_model.py`, `scoreboard_model.py`, `carrito_model.py`).
2. Se exporta a `.obj + .mtl` dentro de `Models/`.
3. Se carga en `main.cpp` con `Model` (Assimp) y se dibuja con `lightingShader`.
# proyecto_grafica
# proyecto_grafica
