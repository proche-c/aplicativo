
from getter.output import *
from errores.errores import *
from inter.interfaz_1 import *
from inter.interfaz_2 import *
from reclamacion.reclamar import *
from reclamacion.reclamar_all import *
from data.estadistica import *
from time import *
import os
import subprocess
try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
        raise ImportError("Se requiere el modulo tkinter")
from tkinter import messagebox
    
dfs = []
df_data = []
path = ""
path_cosesa = ""
desv = 0.01
ref = 1

def save_result():
    global dfs
    your_file = save_r_1(dfs)
    comando = f'open "{your_file}"'
    subprocess.call(comando, shell=True)


def save_correctos():
    global dfs
    your_file = save_r_2(dfs)
    comando = f'open "{your_file}"'
    subprocess.call(comando, shell=True)

def save_estadistica():
    global path
    global df_data
    your_file_e = save_est(df_data)
    comando = f'open "{your_file_e}"'
    subprocess.call(comando, shell=True)


def comprobar():
    global path
    global path_cosesa
    global ref
    global desv
    global dfs
    global df_data

    claim = 0
    cos = 0
    caja2 = 0

    path = ""
    path_cosesa = ""

    try:
        path = os.path.relpath(app.path_file, start=os.curdir)
    except Exception as e:
        tipo = type(e).__name__
        print("Error 00: " + tipo)
        e_00 = Error(tipo, "00")
        msg = "Error 00: " + tipo + ": " + e_00.msg_1 + e_00.msg_2
        messagebox.showinfo(message=msg, title="Warning", parent=root)
    else:
        claim = 1
    if claim == 1:
        try:
            path_cosesa = os.path.relpath(app.path_cosesa, start=os.curdir)
        except Exception as e:
            caja2 = 1
            tipo = type(e).__name__
            print("Error 01: " + tipo)
            e_01 = Error(tipo, "01")
            if tipo == "TypeError":
                msg = e_01.msg_1 + e_01.msg_2
            else:
                msg = "Error 01: " + tipo + ": " + e_01.msg_1 + e_01.msg_2
            r_msg = messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            cos = 1
    desv = float(app.get_apdesv())
    ref = app.get_reference()
    l = []
    s = []
    if caja2 == 1:
        while(1):
            if r_msg == "ok":
                break
    resultado = 0
    if claim == 1 and cos == 1:
        df_data = estadistica(path, root)
        l, s, dfs, resultado = reclamar_all(path, path_cosesa, desv, ref, root)
    elif claim == 1 and cos == 0:
        df_data = estadistica(path, root)
        l, s, dfs, resultado = reclamar(path, desv, ref, root)
    
    if resultado == 1:
        root_2 = Tk()
        y = round((root.winfo_screenheight() - 500) / 2)
        x = round((root.winfo_screenwidth() - 1000) / 2)
        w = 1000
        h = 500
        root_2.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        root_2.resizable(0,0)
        root_2.title("RESUMEN DE RESULTADOS")
        app_2 = Aplication_2(l, s, master=root_2)
        Fr1 = Frame(root_2, width=980, height=130)
        Fr1.pack()
        Fr1.config(bg='blue', bd=5, relief="ridge")
        Fr11 = Frame(Fr1, width=240, height=120)
        Fr11.grid(row=0, column=0)
        Fr11.config(padx=3, pady=5, bg="#C2C2C2")
        Fr12 = Frame(Fr1, width=240, height=120)
        Fr12.grid(row=0, column=1)
        Fr12.config(padx=3, pady=5, bg="#C2C2C2")
        Fr13 = Frame(Fr1, width=240, height=120)
        Fr13.grid(row=0, column=2)
        Fr13.config(padx=3, pady=5, bg="#C2C2C2")
        Fr14 = Frame(Fr1, width=240, height=120)
        Fr14.grid(row=0, column=3)
        Fr14.config(padx=3, pady=5, bg="#C2C2C2")
        B1 = Button(Fr11, text= "Recibos a regularizar", fg ='blue', bg="#C2C2C2", width=18, padx=2, pady=5, font=("Verdana", 14, 'bold'), command=save_result)
        B1.pack()
        B2 = Button(Fr12, text= "Recibos correctos", fg ='blue', bg="#C2C2C2", width=18, padx=2, pady=5, font=("Verdana", 14, 'bold'), command=save_correctos)
        B2.pack()
        B3 = Button(Fr13, text= "Datos estadísticos", fg ='green', bg="#C2C2C2", width=18, padx=2, pady=5, font=("Verdana", 14, 'bold'), command=save_estadistica)
        B3.pack()
        B4 = Button(Fr14, text= "SALIR", fg ='red', bg="#C2C2C2", width=18, padx=2, pady=5, font=("Verdana", 14, 'bold'), command=root_2.destroy)
        B4.pack()
        app_2.mainloop()

root = Tk()
y = round((root.winfo_screenheight() - 450) / 2)
x = round((root.winfo_screenwidth() - 700) / 2)
w = 700
h = 450
root.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
root.resizable(0,0)
root.title("¡BIENVENIDO!")
app = Aplication_1(master=root)
path = app.path_file
path_cosesa = app.path_cosesa
Frame1 = Frame(root, width=700, height=90)
Frame1.pack(fill='x')
Frame1.config(bg="blue", bd=5, relief="ridge")
Frame2 = Frame(Frame1, width=360)
Frame2.pack(side='left', fill='y')
Frame2.config(bg='blue', padx=20, pady=10)
Frame3 = Frame(Frame1, width=360)
Frame3.pack(side='right', fill='y')
Frame3.config(bg='blue', padx=20, pady=10)
result = Button(Frame2, text="COMPROBAR RECIBOS", command=comprobar)
result.pack()
result.config(padx=10, pady=10, font=("Verdana", 14, "bold"), fg='darkblue')
quit = Button(Frame3, text="CERRAR APLICACION", command=root.destroy)
quit.pack()
quit.config(padx=10, pady=10, font=("Verdana", 14, "bold"), fg='red')
app.mainloop()

