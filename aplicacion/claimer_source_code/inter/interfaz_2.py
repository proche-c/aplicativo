from tkinter import *

class Aplication_2(Frame):
    """Esta clase hereda de frame y sus instancias generan el frame que expone el resumen de resultados"""
    def __init__(self, l, s, master=NONE):
        """
        El método constructor de la clase. Toma como parámetros:
            - l: lista que contiene numero de registros procesados, número de registros emitidos en clave 
            cosesa que ya se habían regularizado, número de registros que tienen comisión reducida, número 
            de registros de pólizas sin anomalías, número de registros de pólizas fraccionadas de Zurich, 
            número de registros a regularizar de pólizas sin anomalías, número de registros a regularizar 
            de pólizas fraccionadas de Zurich, número de registros a regularizar de pólizas en clave cosesa 
            y que ya se regularizaron y número de registros a regularizar de pólizas con comisión reducida.
            - s: lista que contiene la cantidad a deber por la compañía y se correcponden respectivamente 
             con los recibos sin anomalías, los recibos de pólizas fraccionadas de Zurich, los recibos con 
             comisión reducida y los recibos de clave cosesa que ya fueron reclamados
        """
        super().__init__(master, width=1000, height=600)   #constructor de la clase madre, master (esto seria root)
        self.master = master
        self.pack(anchor='n')
        self.config(cursor="arrow", bg='blue', bd=5, relief="ridge")
        self.s = s
        self.r_cosesa = l[1]
        self.r_cr = l[2]
        self.r_f = l[4]
        self.r_n = l[3]
        self.r_e_cosesa = l[7]
        self.r_ok_cosesa = l[1] - l[7]
        self.r_e_cr = l[8]
        self.r_ok_cr = l[2] - l[8]
        self.r_e_f = l[6]
        self.r_ok_f = l[4] - l[6]
        self.r_e_n = l[5]
        self.r_ok_n = l[3] - l[5]
        self.r_total = l[0]
        self.r_e = l[7] + l[8] + l[6] + l[5]
        self.r_ok = l[0] - self.r_e
        self.s_total = s[0] + s[1] + s[2] + s[3]
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets contenidos en el frame"""
        self.F1 = Frame(self, width=1000, height=80)
        self.F1.pack(fill='x')
        self.F1.config(padx=5, pady=5, bd=2, relief="ridge")
        self.L11 = Label(self.F1, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "")
        self.L11.grid(row=0, column=0)
        self.L11.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L12 = Label(self.F1, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Recibos procesados")
        self.L12.grid(row=0, column=1)
        self.L12.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L13 = Label(self.F1, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Recibos correctos")
        self.L13.grid(row=0, column=2)
        self.L13.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L14 = Label(self.F1, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Recibos a regularizar")
        self.L14.grid(row=0, column=3)
        self.L14.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L15 = Label(self.F1, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Cuantía a regularizar")
        self.L15.grid(row=0, column=4)
        self.L15.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.F2 = Frame(self, width=1000, height=80)
        self.F2.pack(fill='x')
        self.F2.config(padx=5, pady=5, bd=2, relief="ridge")
        self.L21 = Label(self.F2, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Reclamados de Cosesa")
        self.L21.grid(row=0, column=0)
        self.L21.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L22 = Label(self.F2, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_cosesa, 2)))
        self.L22.grid(row=0, column=1)
        self.L22.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L23 = Label(self.F2, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_ok_cosesa, 2)))
        self.L23.grid(row=0, column=2)
        self.L23.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L24 = Label(self.F2, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_e_cosesa, 2)))
        self.L24.grid(row=0, column=3)
        self.L24.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L25 = Label(self.F2, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.s[3], 2)))
        self.L25.grid(row=0, column=4)
        self.L25.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.F3 = Frame(self, width=1000, height=80)
        self.F3.pack(fill='x')
        self.F3.config(padx=5, pady=5, bd=2, relief="ridge")
        self.L31 = Label(self.F3, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Comisión reducida")
        self.L31.grid(row=0, column=0)
        self.L31.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L32 = Label(self.F3, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_cr, 2)))
        self.L32.grid(row=0, column=1)
        self.L32.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L33 = Label(self.F3, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_ok_cr, 2)))
        self.L33.grid(row=0, column=2)
        self.L33.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L34 = Label(self.F3, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_e_cr, 2)))
        self.L34.grid(row=0, column=3)
        self.L34.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L35 = Label(self.F3, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.s[2], 2)) + " €")
        self.L35.grid(row=0, column=4)
        self.L35.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.F4 = Frame(self, width=1000, height=80)
        self.F4.pack(fill='x')
        self.F4.config(padx=5, pady=5, bd=2, relief="ridge")
        self.L41 = Label(self.F4, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Pólizas fraccionadas")
        self.L41.grid(row=0, column=0)
        self.L41.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L42 = Label(self.F4, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_f, 2)))
        self.L42.grid(row=0, column=1)
        self.L42.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L43 = Label(self.F4, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_ok_f, 2)))
        self.L43.grid(row=0, column=2)
        self.L43.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L44 = Label(self.F4, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_e_f, 2)))
        self.L44.grid(row=0, column=3)
        self.L44.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L45 = Label(self.F4, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.s[1], 2)) + " €")
        self.L45.grid(row=0, column=4)
        self.L45.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.F5 = Frame(self, width=1000, height=80)
        self.F5.pack(fill='x')
        self.F5.config(padx=5, pady=5, bd=2, relief="ridge")
        self.L51 = Label(self.F5, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "Resto de pólizas")
        self.L51.grid(row=0, column=0)
        self.L51.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L52 = Label(self.F5, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_n, 2)))
        self.L52.grid(row=0, column=1)
        self.L52.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L53 = Label(self.F5, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_ok_n, 2)))
        self.L53.grid(row=0, column=2)
        self.L53.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L54 = Label(self.F5, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.r_e_n, 2)))
        self.L54.grid(row=0, column=3)
        self.L54.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L55 = Label(self.F5, bg="#C2C2C2", fg="#2E2929", font=("Verdana", 16),
        text= str(round(self.s[0], 2)) + " €")
        self.L55.grid(row=0, column=4)
        self.L55.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.F6 = Frame(self, width=1000, height=80)
        self.F6.pack(fill='x')
        self.F6.config(padx=5, pady=5, bd=2, relief="ridge")
        self.L61 = Label(self.F6, bg="#A5A1A1", fg="#2E2929", font=("Verdana", 14, "bold"),
        text= "TOTAL")
        self.L61.grid(row=0, column=0)
        self.L61.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L62 = Label(self.F6, bg="#A5A1A1", fg="#2E2929", font=("Verdana", 16, "bold"),
        text= str(round(self.r_total, 2)))
        self.L62.grid(row=0, column=1)
        self.L62.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L63 = Label(self.F6, bg="#A5A1A1", fg="#2E2929", font=("Verdana", 16, "bold"),
        text= str(round(self.r_ok, 2)))
        self.L63.grid(row=0, column=2)
        self.L63.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L64 = Label(self.F6, bg="#A5A1A1", fg="#2E2929", font=("Verdana", 16, "bold"),
        text= str(round(self.r_e, 2)))
        self.L64.grid(row=0, column=3)
        self.L64.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)
        self.L65 = Label(self.F6, bg="#A5A1A1", fg="#2E2929", font=("Verdana", 16, "bold"),
        text= str(round(self.s_total, 2)) + " €")
        self.L65.grid(row=0, column=4)
        self.L65.config(width=16, height=1, relief="ridge", bd=2, padx=5, pady=3)




