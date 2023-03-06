from tkinter import *
import os
from tkinter import filedialog

# def desviacion(parametros):
#     root = Tk()
#     root.geometry()
#     root.resizable(0,0)
#     root.title("RECLAMATOR")
#     root.config(cursor="arrow", bg="#3BCBF1", bd=15, relief="ridge")

#     label_1 = Label(root, bg="#3BCBF1", fg="#2E2929", pady=20, font=("Verdana", 20), text="¡BIENVENIDO A RECLAMATOR!")
#     label_1.pack()
#     label_2 = Label(root, justify='left', bg="#3BCBF1", fg="#2E2929", pady=1, padx=10, font=("Verdana", 18),
#     text="Por favor, introduzca la desviacion")
#     label_2.pack()
#     label_3 = Label(root, justify='left', bg="#3BCBF1", fg="#2E2929", pady=1, padx=10, font=("Verdana", 18),
#     text="")
#     label_3.pack()
#     label_n = Label(root, bg="#3BCBF1", fg="#2E2929", pady=1)
#     label_n.pack()
#     # boton = Button(root, justify="right", height=1, font=("Verdana", 18), pady=5, padx=20, text="Siguiente", command=next1(root, parametros))
#     # boton.pack()

# def next1(old_root):
#     old_root.quit
#     desviacion(parametros)


def configurar(parametros):
    def next1(old_root):
        old_root.quit
    root = Tk()
    root.geometry()
    root.resizable(0,0)
    root.title("RECLAMATOR")
    root.config(cursor="arrow", bg="#3BCBF1", bd=15, relief="ridge")

    label_1 = Label(root, bg="#3BCBF1", fg="#2E2929", pady=20, font=("Verdana", 20), text="¡BIENVENIDO A RECLAMATOR!")
    label_1.pack()
    label_2 = Label(root, justify='left', bg="#3BCBF1", fg="#2E2929", pady=1, padx=10, font=("Verdana", 18),
    text="Es la primera vez que usted utiliza este programa y necesitaré\nalgunos ajustes de configuracón muy sencillos")
    label_2.pack()
    label_3 = Label(root, justify='left', bg="#3BCBF1", fg="#2E2929", pady=1, padx=10, font=("Verdana", 18),
    text="Por favor, siga paso a paso mis instrucciones")
    label_3.pack()
    label_n = Label(root, bg="#3BCBF1", fg="#2E2929", pady=1)
    label_n.pack()
    boton = Button(root, justify="right", height=1, font=("Verdana", 18), pady=5, padx=20, text="Siguiente", command=root.quit)
    boton.pack()

    root.mainloop()

def comprobar():
    root = Tk()
    root.geometry("1000x500")
    root.resizable(1,1)
    root.title("RECLAMATOR")
    root.config(cursor="arrow", bg="#3BCBF1", bd=15, relief="ridge")

    label_1 = Label(root, bg="#3BCBF1", fg="#2E2929", pady=20, font=("Verdana", 20), text="¡BIENVENIDO A RECLAMATOR!")
    label_1.pack()
    label_2 = Label(root, bg="#3BCBF1", fg="#2E2929", pady=15, font=("Verdana", 18), text="Seleccione el archivo que desea comprobar:")
    label_2.pack()

    root.mainloop()