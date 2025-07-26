import pandas as pd
from xlsxwriter import *


def get_df_estadistica(df, list_prod):
    """
    Construye los data frames con los datos estadísticos relevantes.
    Recibe:
        - df: el DataFrame con los datos ya procesados (con columna 'indice')
        - list_prod: lista de tuplas con la información de los productos
    Devuelve:
        - df1: DataFrame con índice, compañía y producto
        - df2: Estadísticas agrupadas por índice, con columnas seleccionadas
        - df3: Información de comisiones por año y detección de discrepancias
    """

    # Subconjunto con las columnas relevantes
    df_e = df[['indice', 'Prima neta', 'Com. prima neta', 'Com. correduría',
               'Com. prima neta %', 'Com. correduría %', 'Sobrecomisión %']]

    # Crear DataFrame de productos
    dfp = pd.DataFrame(list_prod, columns=[
        'ind', 'Compañía', 'Producto', 'Com. año 1', 'Com. año 2',
        'Com. año 3', 'Com. año 4', 'Com. año 5'
    ])
    df1 = dfp[['ind', 'Compañía', 'Producto']].copy()

    # Agrupamos y seleccionamos solo estadísticas relevantes
    df2 = df_e.groupby('indice').agg({
        'Prima neta': ['mean', 'min', 'max'],
        'Com. prima neta': ['mean', 'min', 'max'],
        'Com. correduría': ['mean', 'min', 'max'],
        'Com. prima neta %': ['mean'],
        'Com. correduría %': ['mean'],
        'Sobrecomisión %': ['mean', 'min', 'max']
    })

    # Preparar df3 con las comisiones por año
    df3 = dfp[['Com. año 1', 'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']].copy()

    # Calculamos la media de las comisiones esperadas por fila
    df3['mean_product'] = df3.mean(axis=1)

    # Detectar discrepancias
    all_zeros = (df3[['Com. año 1', 'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']] < 0.001).all(axis=1)

    # Alineamos los valores de la media real por índice del producto
    com_real_mean = df2[('Com. prima neta %', 'mean')].reset_index(drop=True)

    # Creamos la columna 'Discrepancy'
    df3['Discrepancy'] = 'NO'
    df3.loc[all_zeros | (abs(com_real_mean - df3['mean_product']) > 0.06), 'Discrepancy'] = 'YES'

    # Eliminamos la columna auxiliar
    df3.drop(columns='mean_product', inplace=True)

    return df1, df2, df3



def exportar_datos(df, writer, hoja):
    """
    Exporta el data frame que contiene la información de los recibos a procesar
    a un archivo excel y le da un formato adecuado para su correcta visualización
    Toma como parametros:
        - df: data frame a exportar
        - writer: el objeto del módulo xlsxwriter creado para dar formato a un excel 
        desde Python
        - hoja: una cadena que da nombre a la hoja creada en el archivo excel
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
    format3 = workbook.add_format({'border': 1, 'align': 'center'})
    worksheet1.set_row(0, 20)
    worksheet1.set_column(2, 3, None, format3)
    worksheet1.set_column(4, 6, None, format1)
    worksheet1.set_column(10, 14, None, format2)
    worksheet1.set_column(4, 6, None, format1)
    worksheet1.autofit()
    worksheet1.set_column(0, 1, 0)
    worksheet1.set_column(7, 9, 16, format2)


def exportar_estadistica(df1, df2, df3, writer, hoja):
    """
    Exporta el data frame que contiene los datos estadísticos calculados
    a un archivo excel y le da un formato adecuado para su correcta visualización
    Toma como parametros:
        - df1, df2, df3: data frames a exportar que conforman la hoja excel obtenida
        - writer: el objeto del módulo xlsxwriter creado para dar formato a un excel 
        desde Python
        - hoja: una cadena que da nombre a la hoja creada en el archivo excel
    """
    df1.to_excel(writer, sheet_name=hoja, startrow=3, header=False, index=0)
    df2.to_excel(writer, sheet_name=hoja, startrow=0, startcol=3)
    df3.to_excel(writer, sheet_name=hoja, startrow=3, startcol=31, header=False, index=0)
    workbook = writer.book
    worksheet1 = writer.sheets[hoja]
    header_format = workbook.add_format({
        'bold' : True,
        'valign': 'vcenter',
        'align': 'center',
        'border': 1})
    for col, value in enumerate(df1.columns.values):
        worksheet1.write(1, col, value, header_format)
    for col, value in enumerate(df3.columns.values):
        worksheet1.write(1, col + 31, value, header_format)
    format1 = workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'right'})
    format2 = workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'right', 'bg_color': 'yellow'})
    format3 = workbook.add_format({'num_format': '#,##0.00%', 'border': 1, 'align': 'right'})
    format4 = workbook.add_format({'num_format': '#,##0.00%', 'border': 1, 'align': 'right', 'bg_color': 'yellow'})
    format5 = workbook.add_format({'border': 1, 'align': 'center'})
    format6 = workbook.add_format({'border': 1, 'align': 'center', 'bg_color': 'yellow'})
    worksheet1.conditional_format(3, 1, len(df3) + 2, 2, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format6})
    worksheet1.conditional_format(3, 1, len(df3) + 2, 2, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format5})
    worksheet1.conditional_format(3, 36, len(df3) + 2, 36, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format6})
    worksheet1.conditional_format(3, 36, len(df3) + 2, 36, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format5})
    worksheet1.conditional_format(3, 4, len(df3) + 2, 13, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format2})
    worksheet1.conditional_format(3, 4, len(df3) + 2, 13, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format1})
    worksheet1.conditional_format(3, 14, len(df3) + 2, 14, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format4})
    worksheet1.conditional_format(3, 14, len(df3) + 2, 14, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format3})
    worksheet1.conditional_format(3, 15, len(df3) + 2, 15, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format2})
    worksheet1.conditional_format(3, 15, len(df3) + 2, 15, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format1})
    worksheet1.conditional_format(3, 16, len(df3) + 2, 21, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format4})
    worksheet1.conditional_format(3, 16, len(df3) + 2, 21, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format3})
    worksheet1.conditional_format(3, 22, len(df3) + 2, 22, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format2})
    worksheet1.conditional_format(3, 22, len(df3) + 2, 22, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format1})
    worksheet1.conditional_format(3, 23, len(df3) + 2, 35, {'type': 'formula', 'criteria': '=$AK4="YES"', 'format': format4})
    worksheet1.conditional_format(3, 23, len(df3) + 2, 35, {'type': 'formula', 'criteria': '=$AK4="NO"', 'format': format3})
    worksheet1.set_row(0, 20)
    worksheet1.set_row(1, 20)
    worksheet1.autofit()
    worksheet1.set_column(0, 0, 0)
    worksheet1.set_column(3, 3, 0)
    worksheet1.set_column(4, 13, None)
    worksheet1.set_column(14, 14, None)
    worksheet1.set_column(15, 15, None)
    worksheet1.set_column(16, 21, None)
    worksheet1.set_column(22, 22, None)
    worksheet1.set_column(23, 30, None)
    worksheet1.set_column(31, 35, 10)
