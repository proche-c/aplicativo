from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Aplication_1(Frame):
    """
    Esta clase hereda de frame y su instancia generan el frame con los widgets 
    necesarios para que el usuario introduzca los parámetros de entrada
    """
    def __init__(self, master=NONE):
        """
        El método constructor de la clase. Toma como parámetro el 
        widget madre que lo contiene
        """
        super().__init__(master, width=700, height=500) 
        self.master = master
        self.pack(anchor='n')
        self.config(cursor="arrow", bg="blue", bd=5, relief="ridge")
        self.path_file = StringVar()
        self.path_cosesa = StringVar()
        self.create_widgets()

    def get_apdesv(self):
        """Obtiene el valor de desviación intrducido por el usuario y que se 
        establecerá el valor de desviación a partir del cual se considera que 
        se ha de regularizar el recibo
        """
        self.desv = float(self.desv_value.get())
        return self.desv
    

    def get_reference(self):
        """
        Obtiene un parámetro introducido por el usuario y que indica cómo se han 
        de consideran las pólizas por las que se percibe una comisión por debajo 
        de la comisión por tabla pero no se tiene la certeza de que s ehaya pactado 
        una comisión reducida.
        - Si su valor es 1, se considerará que la póliza tiene la comisión que se 
        indica en la tabla de comisiones
        - Si su valor es 0, se considerará que las pólizas tienen pactada una comisión 
        reducida y por lo tanto, el recibo es correcto 
        """
        return self.r.get()


    def open_file(self):
        """
        Otiene la ruta indicada por el usuario en la que se encuentra ubicado el 
        archivo a procesar
        """
        self.path_file = filedialog.askopenfilename(title="Abrir",
            filetypes=(("Archivos Excel", "*.xls"), ("Libros Excel", "*.xlsx")))
        return self.path_file    

    def open_cosesa(self):
        """
        Obtiene la ruta indicada por el usuario en la que se encuentra ubicado el 
        archivo con los recibos reclamados cosesa
        """
        self.path_cosesa = filedialog.askopenfilename(title="Abrir",
                        filetypes=(("Archivos Excel", "*.xls"), ("Libros Excel", "*.xlsx")))
        return self.path_cosesa
    

    def create_widgets(self):
        """Crea los widgets contenidos en el frame"""
        self.welcome = Label(self, text="INTRODUZCA LOS PARAMETROS DE ENTRADA")
        self.welcome.pack(fill='x')
        self.welcome.config(padx=15, bg="#C2C2C2", fg="#2E2929", bd=3, font=("Verdana", 18), relief="ridge", width=60, pady=15)
        self.Frame1 = Frame(self, width=700, height=120)
        self.Frame1.pack(fill='x')
        self.Frame1.config(bg="#C2C2C2", pady=10, padx=10)
        self.Frame2 = Frame(self.Frame1, width=500, height=100)
        self.Frame2.pack(side='left', fill='y')
        self.Frame2.config(bg="#C2C2C2", pady=10, padx=5)
        self.Frame3 = Frame(self.Frame1, width=200, height=100)
        self.Frame3.pack(side='right', fill='y')
        self.Frame3.config(bg="#C2C2C2", pady=10, padx=5)
        
        self.desv = Label(self.Frame2, text="Introduzca la desviación en euros:")
        self.desv.pack(fill='both')
        self.desv.config(justify='left', bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16), padx=3)

        self.desv_value = ttk.Combobox(self.Frame3, font=("Verdana", 16), state='readonly', justify='left', width=12)
        self.desv_value.pack(fill='both')
        self.desv_value.set("0.01")
        self.option = ["0.01", "0.05", "0.10", "0.50", "1.00", "5.00"]
        self.desv_value['values'] = self.option

        self.Frame4 = Frame(self, width=700, height=150)
        self.Frame4.pack(fill='x')
        self.Frame4.config(bg="#C2C2C2", pady=10, padx=10)
        self.Frame5 = Frame(self.Frame4, width=500, height=150)
        self.Frame5.pack(side='left', fill='y')
        self.Frame5.config(bg="#C2C2C2", pady=10, padx=5)
        self.Frame6 = Frame(self.Frame4, width=200, height=150)
        self.Frame6.pack(side='right', fill='y')
        self.Frame6.config(bg="#C2C2C2", pady=10, padx=5)

        self.r = IntVar()
        self.ref = Label(self.Frame5, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16), justify='left',
        text="Calcular 'referencia' o 'por determinar' como:")
        self.ref.pack(anchor='n', fill='both')

        self.ref_1 = Radiobutton(self.Frame6, bg="#C2C2C2", text="Por tabla", font=("Verdana", 15), justify='left',
                variable=self.r, value=1, command=self.get_reference, width=9, height=1)
        self.ref_1.pack(fill='x')
        self.ref_2 = Radiobutton(self.Frame6,  bg="#C2C2C2", text="Comisión reducida", font=("Verdana", 15), justify='left',
                variable=self.r, value=0, command=self.get_reference, width=15, height=1)
        self.ref_2.pack(fill='x')

        self.Frame7 = Frame(self, width=700, height=150)
        self.Frame7.pack(fill='x')
        self.Frame7.config(bg="#C2C2C2", pady=10, padx=10)
        self.Frame8 = Frame(self.Frame7, width=500, height=150)
        self.Frame8.pack(side='left', fill='y')
        self.Frame8.config(bg="#C2C2C2", pady=10, padx=5)
        self.Frame9 = Frame(self.Frame7, width=200, height=150)
        self.Frame9.pack(side='right', fill='y')
        self.Frame9.config(bg="#C2C2C2", pady=10, padx=5)

        self.file = Label(self.Frame8, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16), justify='left',
        text="Abra el archivo excel que desea evaluar:        ")
        self.file.pack(fill='both')
        self.open = Button(self.Frame9, text="Abrir", command=self.open_file)
        self.open.pack(fill='both')
        self.open.config(bg="#3300FF", font=("Verdana", 16), padx=12, justify='left', width=9, pady=2)

        self.Frame10 = Frame(self, width=700, height=150)
        self.Frame10.pack(fill='x')
        self.Frame10.config(bg="#C2C2C2", pady=10, padx=10)
        self.Frame11 = Frame(self.Frame10, width=500, height=150)
        self.Frame11.pack(side='left', fill='y')
        self.Frame11.config(bg="#C2C2C2", pady=10, padx=5)
        self.Frame12 = Frame(self.Frame10, width=200, height=150)
        self.Frame12.pack(side='right', fill='y')
        self.Frame12.config(bg="#C2C2C2", pady=10, padx=5)

        self.cosesa = Label(self.Frame11, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16), justify='left',
        text="Cargue el archivo de los recibos reclamados de Cosesa:")
        self.cosesa.pack(fill='both')
        self.open_c = Button(self.Frame12, text="Abrir", command=self.open_cosesa)
        self.open_c.pack(fill='both')
        self.open_c.config(bg="#3300FF", font=("Verdana", 16), padx=12, justify='left', width=9, pady=2)

