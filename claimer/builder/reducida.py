"""
El modulo reducida contiene la funcion necesaria para la creación del dataframe
que trata las pólizas emitidas en las que se ha pactado de manera particular
una comisión diferente de la que consta en la tabla de condiciones.
"""

def get_comision_r(df):
    """Parsea los valores de com. reducida y los transforma todos a flotantes"""
    df['com. red'] = 1.00

    # Aseguramos tipo string
    comision_str = df['Comision reducida'].astype(str)

    # Filtramos los que contienen un único '%'
    mask_porcentaje = comision_str.str.count('%') == 1
    subset = df[mask_porcentaje].copy()
    com_texts = comision_str[mask_porcentaje]

    # Caso 1: Formato directo, e.g. "10%"
    mask_directo = com_texts.str.match(r"^\d{1,3},?\d*%$")

    # Procesamos directo
    direct_vals = com_texts[mask_directo].str.replace('%', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    df.loc[mask_porcentaje[mask_porcentaje].index[mask_directo], 'com. red'] = direct_vals / 100

    # Caso 2: Formato "Fija a 10%"
    mask_fija = com_texts.str.startswith("Fija a")
    fija_vals = com_texts[mask_fija].str.extract(r"Fija a (\d{1,3},?\d*)%")[0]
    fija_vals = fija_vals.str.replace(',', '.', regex=False).astype(float)

    idx_fija = mask_porcentaje[mask_porcentaje].index[mask_fija]

    # Evitamos división por cero con clip
    divisor = df.loc[idx_fija, 'com_aplicada'].clip(lower=1e-6)
    df.loc[idx_fija, 'com. red'] = fija_vals.values / (100 * divisor.values)

    
