"""
Data es un paquete que crea dataframes y otros objetos necesario para el cálculo de algunos datos estadísticos tomando como muestra 
los datos registrados en los recibos de la BBDD, expone los datos y sus desviaciones, resalta discrepancias llamativas y los exporta 
en formato excel.
Consta de tres modulos:
- build: conjunto de funciones necesarias para la creacion de los data frame y los campos que aportan información y permiten parametrizar 
- estadística: contiene la función que estructura  la creación de esos data frame y sus campos
- out: conjunto de funciones necesarias para exportar los data frame a formato excel y darle formato para una visualización mas clara
"""