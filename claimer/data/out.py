import pandas as pd
from xlsxwriter import *


def get_df_estadistica(df, list):
    """
    Construye el data frame todos con los datos estadisticos
    relevantes
    Toma como parametro el dat frame de los datos y la lista de tuplas con
    la informacion de los productos
    """
    # Toma los datos necesarios de df_datos
    df_e = df[['indice', 'Prima neta', 'Com. prima neta', 'Com. correduría', 'Com. prima neta %', 
        'Com. correduría %', 'Sobrecomisión %']]

    # Crea un data frame con la información de los productos
    dfp = pd.DataFrame(list, columns= ['ind', 'Compañía', 'Producto', 'Com. año 1', 
        'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5'])
    df1 = dfp[['ind', 'Compañía', 'Producto']]

    # Crea otro data frame con los datos estadisticos y elimina los campos innecesarios
    df2 = df_e.groupby('indice').describe()
    df2.drop(('Prima neta', 'std') , axis=1, inplace=True)
    df2.drop(('Prima neta', '25%') , axis=1, inplace=True)
    df2.drop(('Prima neta', '50%') , axis=1, inplace=True)
    df2.drop(('Prima neta', '75%') , axis=1, inplace=True)
    df2.drop(('Com. prima neta', 'count') , axis=1, inplace=True)
    df2.drop(('Com. prima neta', 'std') , axis=1, inplace=True)
    df2.drop(('Com. prima neta', '25%') , axis=1, inplace=True)
    df2.drop(('Com. prima neta', '50%') , axis=1, inplace=True)
    df2.drop(('Com. prima neta', '75%') , axis=1, inplace=True)
    df2.drop(('Com. correduría', 'count') , axis=1, inplace=True)
    df2.drop(('Com. correduría', 'std') , axis=1, inplace=True)
    df2.drop(('Com. correduría', '25%') , axis=1, inplace=True)
    df2.drop(('Com. correduría', '50%') , axis=1, inplace=True)
    df2.drop(('Com. correduría', '75%') , axis=1, inplace=True)
    df2.drop(('Com. prima neta %', 'count') , axis=1, inplace=True)
    df2.drop(('Com. correduría %', 'count') , axis=1, inplace=True)
    df2.drop(('Sobrecomisión %', 'count') , axis=1, inplace=True)
    df2.drop(('Sobrecomisión %', 'std') , axis=1, inplace=True)
    df2.drop(('Sobrecomisión %', '25%') , axis=1, inplace=True)
    df2.drop(('Sobrecomisión %', '50%') , axis=1, inplace=True)
    df2.drop(('Sobrecomisión %', '75%') , axis=1, inplace=True)

    # Crea otro data frame con la información de las comisiones de producto
    df3 = dfp[['Com. año 1', 'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']]
    # Calcula un parametro que determina si hay discrepancia entre la información
    # de la BBDD y los datos registrados en los recibos
    df3['Discrepancy'] = "NO"
    for i in range(len(df3)):
        mean = (df3['Com. año 1'][i] + df3['Com. año 2'][i] + df3['Com. año 3'][i]
                 + df3['Com. año 4'][i] + df3['Com. año 5'][i]) / 5
        if (df3['Com. año 1'][i] < 0.001 and  df3['Com. año 2'][i] < 0.001 and df3['Com. año 3'][i] < 0.001 
        and df3['Com. año 4'][i] < 0.001 and df3['Com. año 5'][i] < 0.001):
            df3['Discrepancy'][i] = "YES"
        elif abs(df2['Com. prima neta %', 'mean'][i] - mean) > 0.06:
            df3['Discrepancy'][i] = "YES"
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
