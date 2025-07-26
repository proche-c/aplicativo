#!/bin/bash

# Verificamos si python3.11 está disponible en el PATH
if ! command -v python3.11 &> /dev/null
then
    echo "❌ Python 3.11 no está instalado o no está en el PATH."
    echo "Por favor instálalo antes de continuar."
    echo "Instala Python 3.11 así:"
    echo "macOS: https://www.python.org/downloads/mac-osx/"
    echo "Linux (Debian/Ubuntu): sudo apt install python3.11"
    echo "Windows: usa el instalador oficial de https://python.org"
    exit 1
fi

# Usamos el python3.11 del sistema
python3.11 -m pip install --user --upgrade pipenv

# Creamos entorno virtual con ese Python
pipenv --python python3.11 install
