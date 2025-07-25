"""
El módulo exexcel contiene las funciones que exportan los data frame 
resultantes del procesamiento de recibos a un archivo excel y le dan formato
"""

from xlsxwriter import *

def fix_columns(df, col):
    """
    Elimina las columnas que no se van a exportar al archivo excel
    y renombra
    Toma como parámetros:
        - df: el data frame en el que se eliminan columnas
        - col: lista que contiene los nuevos nombres de las columnas
    """   
    df.drop('is_fraccionada', axis=1, inplace=True)
    df.drop('is_fraccionada_zurich', axis=1, inplace=True)
    df.drop('Comision reducida', axis=1, inplace=True)
    df.columns = col


def fix_columns_all(df, col, n):
    """
    Elimina las columnas que no se van a exportar al archivo excel
    y renombra
    Toma como parámetros:
        - df: el data frame en el que se eliminan columnas
        - col: lista que contiene los nuevos nombres de las columnas
        - n: su valor es 0 para el data frame de recibos incorrectos y
        1 para el de recibos incorrectos
    """   
    df.drop('is_fraccionada', axis=1, inplace=True)
    df.drop('is_fraccionada_zurich', axis=1, inplace=True)
    df.drop('Comision reducida', axis=1, inplace=True)
    df.drop('is cosesa', axis=1, inplace=True)
    if n == 0:
        df.drop('com. cosesa', axis=1, inplace=True)
    df.columns = col


def exportar_resultado(df, writer, hoja, n):
    """
    Exporta el data frame que contiene la información de los recibos procesados
    a un archivo excel y le da un formato adecuado para su correcta visualización
    Toma como parametros:
        - df: data frame a exportar
        - writer: el objeto del módulo xlsxwriter creado para dar formato a un excel 
        desde Python
        - hoja: una cadena que da nombre a la hoja creada en el archivo excel
        - n: toma diferentes valores según la hoja exportada. 0 para la hoja de resultados
        de 'normales' y 'fraccionadas'; 1 para 'comision reducida'; 2 para recibos 'correctos' 
        si no se procesan recibos reclamados de cosesa; 3 para 'cosesa'; y 4 para recibos 
        'correctos' si se han procesado recibos de cosesa
    """
    df.to_excel(writer, sheet_name=hoja, startrow=1, header=False)
    workbook = writer.book
    worksheet1 = writer.sheets[hoja]
    header_format = workbook.add_format({
        'bold' : True,
        'valign': 'vcenter',
        'align': 'center',
        'border': 1})
    for col, value in enumerate(df.columns.values):
        worksheet1.write(0, col + 1, value, header_format)
    format1 = workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'right'})
    format2 = workbook.add_format({'num_format': '#,##0.00%', 'border': 1, 'align': 'right'})
    format3 = workbook.add_format({'border': 1, 'align': 'right'})
    worksheet1.set_row(0, 20)
    worksheet1.set_column(1, 5, None, format3)
    worksheet1.set_column(6, 8, None, format1)
    worksheet1.set_column(9, 11, None, format3)
    worksheet1.set_column(12, 16, None, format2)
    worksheet1.set_column(17, 17, None, format3)
    if n == 0 or n == 1 or n ==2:
        worksheet1.set_column(18, 19, None, format2)
        if n == 0:
            worksheet1.set_column(20, 21, None, format1)
        elif n == 1:
            worksheet1.set_column(20, 20, None, format1)
            worksheet1.set_column(21, 21, None, format2)
            worksheet1.set_column(22, 22, None, format1)
        elif n == 2:
            worksheet1.set_column(20, 21, None, format1)
            worksheet1.set_column(22, 22, None, format2)
    elif n == 3 or n == 4:
        worksheet1.set_column(18, 20, None, format2)
        worksheet1.set_column(21, 22, None, format1)
        if n == 4:
            worksheet1.set_column(23, 23, None, format2)
    worksheet1.autofit()
