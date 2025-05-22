

class Error():
    """
    La clase Error contiene la información de los posibles errores que puedan producirse 
    durante la ejecución del programa. Toma como parámetros:
        - tipo: tipo de error generado
        - n: indica donde se produce el error. El primer dígito indica en qué módulo se 
        ha producido el error y los siguientes dígitos indican la función
    """
    file = ""
    funct = ""
    msg_1 = ""
    msg_2 = ""
    tipo = ""
    def __init__(self, tipo, n):
        """Método constructor de la clase"""
        
        # Errores al establecer el path de los ficheros de entrada en claim empiezan por 0
        if n[0] == "0":
            self.file = "claim.py"
            self.tipo = tipo
            if n[1] == "0":
                self.funct = "Comprobar"
                self.msg_1 = f'Se ha producido un {self.tipo} en {self.file} al importar el archivo de datos. '
                self.msg_2 = "Compruebe que la ruta indicada es válida."
            elif n[1] == "1":
                self.funct = "Comprobar"
                if tipo == "TypeError":
                    self.msg_1 = "No ha seleccionado ningún archivo para procesar los recibos ya reclamados de Cosesa. "
                    self.msg_2 = "Los recibos se procesarán como si no se hubieran reclamado."
                else:
                    self.msg_1 = f'Se ha producido un {self.tipo} en {self.file} al importar el archivo de recibos cosesa. '
                    self.msg_2 = "Compruebe que la ruta indicada es válida."
        
        # Errores generados en reclamar empiezan por 1        
        elif n[0] == "1":
            self.file = "reclamacion.reclamar.py"
            self.tipo = tipo
            if len(n) == 2 and n[1] == "0":
                self.funct = "create_df. "
            elif len(n) == 2 and n[1] == "1":
                self.funct = "eliminar_columnas. "
            elif n[1] == "2":
                self.funct = "el análisis de los valores de Prima neta y comisión proporcionados. "
            elif n[1] == "3":
                self.funct = "get_prima_fraccionada. "    
            elif n[1] == "4":
                self.funct = "get_com. "
            elif n[1] == "5":
                self.funct = "la separación de las pólizas con comisión reducida. "
            elif n[1] == "6":
                self.funct = "la separación de las pólizas con pago fraccionado. "
            elif n[1] == "7":
                self.funct = "get_comision_r. "
            elif n[1] == "8":
                self.funct = "get_desv. "
            elif n[1] == "9":
                self.funct = "el calculo y separación de los recibos sin comision reducida mal pagados. Debt1. "
            elif n[1] == "1" and n[2] == "0":
                self.funct = "el calculo y separación de los recibos con comisión reducida mal pagados. Debt2. "
            elif n[1] == "1" and n[2] == "1":
                self.funct = "el calculo de las cantidades a regularizar. "
            elif n[1] == "1" and n[2] == "2":
                self.funct = "la concatenación de los df de recibos pagados correctamente. "
            elif n[1] == "1" and n[2] == "3":
                self.funct = "la conversión de las fechas de los dfs. "
            elif n[1] == "1" and n[2] == "4":
                self.funct = "el cambio de nombre de las columnas de los dfs. "
            elif n[1] == "1" and n[2] == "5":
                self.funct = "la creación de la lista de dfs resultante. "
            elif n[1] == "1" and n[2] == "6":
                self.funct = "exportar_resultado. "
            self.msg_1 = f'Se ha producido un {self.tipo} en el archivo {self.file} en {self.funct}'
            if self.tipo == "PermissionError":
                self.msg_2 = "Compruebe que tiene permiso para leer o modificar ese archivo."
            elif tipo == "FileNotFoundError":
                self.msg_2 = "No se ha encontrado el archivo. Asegúrese de que el archivo no ha sido borrado."
            elif tipo == "KeyError":
                self.msg_2 = "Asegúrese de que el archivo cargado es correcto. Recuerde que el archivo debe tener el formato y los campos que el listado CAZ de Elevia genera. Asegúrese de que el listado no ha sido modificado. FIJESE EN LAS PRIMERAS FILAS DEL ARCHIVO EXCEL, no debe haber líeas en blanco al inicio del archivo. EL ALIAS DE LA COMPAÑIA ZURICH DEBE SER 'ZURICH'."
            elif tipo == "AttributeError":
                self.msg_2 = "Revise bien el formato de los datos de su archivo, es decir, los datos numéricos son números, las fechas tienen formato de fecha..."
            else:
                self.msg_2 = "Revise la ruta de los ficheros proporcionados y el formato de éstos. Vuelva a intentarlo y si el problema continua, póngase en contacto con el desarrollador"
        
        # Errores generados en reclamar_all empiezan por 2
        elif n[0] == "2":
            self.file = "reclamacion.reclamar_all.py"
            self.tipo = tipo
            if len(n) == 2 and n[1] == "0":
                self.funct = "create_df. "
            elif len(n) == 2 and n[1] == "1":
                self.funct = "eliminar_columnas. "
            elif len(n) and n[1] == "2":
                self.funct = "create_df(cosesa). "
            elif n[1] == "3":
                self.funct = "build_cosesa. "
            elif n[1] == "4":
                self.funct = "add_is_cosesa. "
            elif n[1] == "5":
                self.funct = "el análisis de los valores de Prima neta y comisión proporcionados. "
            elif n[1] == "6":
                self.funct = "get_prima_fraccionada. "    
            elif n[1] == "7":
                self.funct = "get_com. "
            elif n[1] == "8":
                self.funct = "la separación de los recibos de pólizas emitidas en clave cosesa ya reclamadas. "
            elif n[1] == "9":
                self.funct = "la separación de las pólizas con comisión reducida. "
            elif n[1] == "1" and n[2] == "0":
                self.funct = "la separación de las pólizas con pago fraccionado. "
            elif n[1] == "1" and n[2] == "1":
                self.funct = "get_comision_r. "
            elif n[1] == "1" and n[2] == "2":
                self.funct = "get_desv. "
            elif n[1] == "1" and n[2] == "3":
                self.funct = "el calculo y separación de los recibos sin comision reducida mal pagados. Debt1. "
            elif n[1] == "1" and n[2] == "4":
                self.funct = "el calculo y separación de los recibos ya reclamados de cosesa mal pagados. Debt2. "
            elif n[1] == "1" and n[2] == "5":
                self.funct = "el calculo y separación de los recibos con comisión reducida mal pagados. Debt3. "
            elif n[1] == "1" and n[2] == "6":
                self.funct = "el calculo de las cantidades a regularizar. "
            elif n[1] == "1" and n[2] == "7":
                self.funct = "la concatenación de los df de recibos pagados correctamente. "
            elif n[1] == "1" and n[2] == "8":
                self.funct = "la conversión de las fechas de los dfs. "
            elif n[1] == "1" and n[2] == "9":
                self.funct = "el cambio de nombre de las columnas de los dfs. "
            elif n[1] == "2" and n[2] == "0":
                self.funct = "la creación de la lista de dfs resultante. "
            elif n[1] == "2" and n[2] == "1":
                self.funct = "exportar_resultado. "
            self.msg_1 = f'Se ha producido un {self.tipo} en el archivo {self.file} en {self.funct}'
            if self.tipo == "PermissionError":
                self.msg_2 = "Compruebe que tiene permiso para leer o modificar ese archivo."
            elif tipo == "FileNotFoundError":
                self.msg_2 = "No se ha encontrado el archivo. Asegúrese de que el archivo no ha sido borrado."
            elif tipo == "KeyError":
                self.msg_2 = "Asegúrese de que el archivo cargado es correcto. Recuerde que el archivo debe tener el formato y los campos que el listado CAZ de Elevia genera. Asegúrese de que el listado no ha sido modificado. FIJESE EN LAS PRIMERAS FILAS DEL ARCHIVO EXCEL, no debe haber líeas en blanco al inicio del archivo. EL ALIAS DE LA COMPAÑIA ZURICH DEBE SER 'ZURICH'."
            elif tipo == "AttributeError":
                self.msg_2 = "Revise bien el formato de los datos de su archivo, es decir, los datos numéricos son números, las fechas tienen formato de fecha..."
            else:
                self.msg_2 = "Revise la ruta de los ficheros proporcionados y el formato de éstos. Vuelva a intentarlo y si el problema continua, póngase en contacto con el desarrollador"

        # Errores generados en output empiezan por 3
        elif n[0] == "3":
            self.file = "getter.output.py"
            if n[1] == "0":
                self.funct = "save_r_1. "
            elif n[1] == "1":
                self.funct = "save_r_2. "
            elif n[1] == "2":
                self.funct = "save_est. "
            self.msg_1 = f'Se ha producido un {self.tipo} en el archivo {self.file} en {self.funct}'
            self.msg_2 = "Revise la ruta proporcionada y el formato de los archivos. Si el problema continúa, póngase en contacto con el desarrollador."
       
        # Errores generados en estadistica empiezan por 4
        elif n[0] == "4":
            self.file = "data.estadistica.py"
            if n[1] == "0":
                self.funct = "estadistica(create_df). "
            elif n[1] == "1":
                self.funct = "estadistica(create_list_prod). "
            elif n[1] == "2":
                self.funct = "estadistica(complete_df). "
            elif n[1] == "3":
                self.funct = "estadistica(get_df_estadistica). "
            elif n[1] == "4":
                self.funct = "estadistica(pd.ExcelWriter, exportar_datos o exportar_estadistica). "
            self.msg_1 = f'Se ha producido un {self.tipo} en el archivo {self.file} en {self.funct}'
            self.msg_2 = "Revise la ruta proporcionada y el formato de los archivos. Si el problema continúa, póngase en contacto con el desarrollador."
    
