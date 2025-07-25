"""
El modulo reducida contiene la funcion necesaria para la creación del dataframe
que trata las pólizas emitidas en las que se ha pactado de manera particular
una comisión diferente de la que consta en la tabla de condiciones.
"""

def get_comision_r(df):
    """Parsea los valores de com. reducida y los transforma todos a flotantes"""
    df['com. red'] = 1.00
    for i in range(len(df)):
        if df['Comision reducida'][i].count('%') == 1:
            c = df['Comision reducida'][i]
            c1 = c.split(' ')
            if len(c1) == 1:
                c2 = str(c1[0])
                c3 = c2.strip('%')
                c4 = c3.replace(',','.')
                c5 = float(c4)
                df['com. red'][i] = c5 / 100
            elif len(c1) == 3 and c1[0] == "Fija" and c1[1] == "a":
                c2 = str(c1[2])
                c3 = c2.strip('%')
                c4 = c3.replace(',','.')
                c5 = float(c4)
                df['com. red'][i] = c5 / (100 * df['com_aplicada'][i])
