import csv
from io import open


parametros = [0, "", "", 0, 0]

def generate_parameters(parametros):
    with open('../installfiles/parametros.csv', 'w', newline = '\n') as csvfile:
        campos = ['instalado', 'path', 'path_cosesa', 'desviacion', 'referencia']
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        writer.writerow({
            'instalado':parametros[0], 'path':parametros[1], 'path_cosesa':parametros[2], 'desviacion':parametros[3], 'referencia':parametros[4]
        })
        
if __name__ == '__main__':
    generate_parameters(parametros)