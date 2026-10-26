#!/bin/bash
set -e
cd "$(dirname "$0")"
gcc -c SOIL2/SOIL2.c -o SOIL2/SOIL2.o -O2 -I SOIL2
gcc -c SOIL2/image_DXT.c -o SOIL2/image_DXT.o -O2 -I SOIL2
gcc -c SOIL2/image_helper.c -o SOIL2/image_helper.o -O2 -I SOIL2
g++ -std=c++11 -O2 "main.cpp" \
    SOIL2/SOIL2.o SOIL2/image_DXT.o SOIL2/image_helper.o \
    -o "estadio" \
    $(pkg-config --cflags --libs glfw3 glew glm assimp)
echo "Compilado OK -> ./estadio"
