from io import open
import csv

parametros = {}
def read_parameters(parametros, ruta):
    with open(ruta, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for parametro in reader:
            parametros['instalado'] = parametro['instalado']
            parametros['path'] = parametro['path']
            parametros['path_cosesa'] = parametro['path_cosesa']
            parametros['desviacion'] = parametro['desviacion']
            parametros['referencia'] = parametro['referencia']
    return parametros

if __name__ == '__main__':
    read_parameters(parametros)

