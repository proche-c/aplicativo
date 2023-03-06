from tkinter import *
import io
from install.generate_p import *
from install.read_p import *
from interfaces.configurar import *

# Evaluo si ya se ha configurado (parametros['instalado] = 0)
parametros = {}
read_parameters(parametros, 'installfiles/parametros.csv')
if parametros['instalado'] == '0':
    configurar(parametros)
else:
    comprobar()

