"""
Getter es un paquete que se encarga de procesar los datos de entrada y construior los datos datos de salida
 y otros objetos necesario para el cálculo de las desviacionesa partir de ficheros excel.
Contiene las funciones que calculan los campos que se muestran en los data frame de salida
Consta de tres modulos:
- input: conjunto de funciones que modifican el data frame inicial y la función que gestiona la creación de los 
    campos necesarios para el procesamiento de los recibos.
- output: conjunto de funciones necesarias que obtienen los datos necesarios para clasificar los registros y 
    las funciones que guardan una copia temporal de los resultados obtenidos
- exexcel: conjunto de funciones que exportan el data frame a un archivo excel y le dan formato
"""