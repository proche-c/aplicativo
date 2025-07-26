"""
El modulo regular contiene la funcion necesaria para la creación del dataframe
que trata las pólizas sin anomalías.
"""


def get_comision_a(df_recibos):
    """Calcula la comisión que se debe aplicar según la antigüedad de la póliza"""

    # Calcula diferencias de años y meses
    y1 = df_recibos['Fecha efecto'].dt.year
    m1 = df_recibos['Fecha efecto'].dt.month
    y2 = df_recibos['Poliza.FechaPrimerEfecto'].dt.year
    m2 = df_recibos['Poliza.FechaPrimerEfecto'].dt.month

    df_recibos['com_aplicada'] = df_recibos['Poliza.Producto.Com6']  # valor por defecto

    # Condiciones por año/mes
    mask1 = (y1 == y2) | ((y1 == y2 + 1) & (m1 < m2))
    mask2 = ((y1 == y2 + 1) & (m1 >= m2)) | ((y1 == y2 + 2) & (m1 < m2))
    mask3 = ((y1 == y2 + 2) & (m1 >= m2)) | ((y1 == y2 + 3) & (m1 < m2))
    mask4 = ((y1 == y2 + 3) & (m1 >= m2)) | ((y1 == y2 + 4) & (m1 < m2))
    mask5 = ((y1 == y2 + 4) & (m1 >= m2)) | ((y1 == y2 + 5) & (m1 < m2))

    df_recibos.loc[mask5, 'com_aplicada'] = df_recibos['Poliza.Producto.Com5']
    df_recibos.loc[mask4, 'com_aplicada'] = df_recibos['Poliza.Producto.Com4']
    df_recibos.loc[mask3, 'com_aplicada'] = df_recibos['Poliza.Producto.Com3']
    df_recibos.loc[mask2, 'com_aplicada'] = df_recibos['Poliza.Producto.Com2']
    df_recibos.loc[mask1, 'com_aplicada'] = df_recibos['Poliza.Producto.Com1']



def add_Com6(df_recibos):
    """Añade la comisión del 6º año para Zurich Motor Pack"""
    df_recibos['Poliza.Producto.Com6'] = df_recibos['Poliza.Producto.Com5']

    mask_motor_pack = df_recibos['Producto'].isin([
        'ZURICH MOTOR PACK(1ª CAT)',
        'ZURICH MOTOR PACK(2ª CAT)',
        'ZURICH MOTOR PACK(3ª CAT)'
    ])

    df_recibos.loc[mask_motor_pack, 'Poliza.Producto.Com6'] += 0.01


    
def get_comision_t(df_recibos):
    """Calcula la comisión teórica: com_aplicada * Prima neta"""
    df_recibos['com_teorica'] = 0.0
    mask = df_recibos['Prima neta'] != 0
    df_recibos.loc[mask, 'com_teorica'] = (
        df_recibos.loc[mask, 'com_aplicada'] * df_recibos.loc[mask, 'Prima neta']
    )



