import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Huesped:
    nombre: str
    apellidos: str
    documento: str
    fecha_ingreso: datetime

@dataclass
class Habitacion:
    numero: int
    precio_dia: int
    huesped: Huesped|None=None
    @property
    def disponible(self): return self.huesped is None

class AplicacionHotel:
    FORMATO="%d/%m/%Y"
    def __init__(self,root):
        self.root=root; root.title("Gestión de huéspedes - Hotel"); root.geometry("650x420")
        self.habitaciones=[Habitacion(i,120000 if i<=5 else 160000) for i in range(1,11)]
        barra=tk.Menu(root); menu=tk.Menu(barra,tearoff=0)
        menu.add_command(label="Consultar habitaciones",command=self.consultar)
        menu.add_command(label="Salida de huéspedes",command=self.salida)
        barra.add_cascade(label="Opciones",menu=menu); root.config(menu=barra)
        ttk.Label(root,text="HOTEL",font=("Arial",22,"bold")).pack(pady=30)
        ttk.Label(root,text="Sistema de ingreso y salida de huéspedes").pack()
        ttk.Label(root,text="Habitaciones 1–5: $120.000 por día\\nHabitaciones 6–10: $160.000 por día",justify="center").pack(pady=25)

    def buscar(self,valor):
        if not valor.isdigit() or not 1<=int(valor)<=10: return None
        return self.habitaciones[int(valor)-1]

    def consultar(self):
        w=tk.Toplevel(self.root); w.title("Consultar habitaciones"); w.geometry("500x430")
        ttk.Label(w,text="Estado de las habitaciones",font=("Arial",14,"bold")).pack(pady=10)
        cols=("numero","precio","estado"); t=ttk.Treeview(w,columns=cols,show="headings",height=10)
        for c,txt in zip(cols,("Habitación","Precio por día","Estado")): t.heading(c,text=txt)
        t.pack(fill="x",padx=12,pady=8)
        for h in self.habitaciones:
            t.insert("","end",values=(h.numero,f"$ {h.precio_dia:,.0f}","Disponible" if h.disponible else "No disponible"))
        ttk.Label(w,text="Número de habitación que desea ocupar:").pack(pady=(10,3))
        num=ttk.Entry(w,width=15); num.pack()
        def continuar():
            h=self.buscar(num.get().strip())
            if h is None: messagebox.showerror("Inválida","Ingrese un número entre 1 y 10.",parent=w)
            elif not h.disponible: messagebox.showerror("Ocupada","La habitación no está disponible.",parent=w)
            else: self.ingreso(h); w.destroy()
        ttk.Button(w,text="Continuar con ingreso",command=continuar).pack(pady=12)

    def ingreso(self,h):
        w=tk.Toplevel(self.root); w.title(f"Ingreso - Habitación {h.numero}"); w.geometry("430x330")
        ttk.Label(w,text=f"Registro de huésped | Habitación {h.numero}",font=("Arial",12,"bold")).pack(pady=12)
        labels=("Nombre","Apellidos","Documento","Fecha de ingreso (DD/MM/AAAA)"); entries={}
        for lab in labels:
            row=ttk.Frame(w); row.pack(fill="x",padx=15,pady=6)
            ttk.Label(row,text=lab,width=29).pack(side="left")
            e=ttk.Entry(row,width=20); e.pack(side="right"); entries[lab]=e
        def registrar():
            vals={k:v.get().strip() for k,v in entries.items()}
            if not all(vals.values()): messagebox.showerror("Obligatorio","Complete todos los campos.",parent=w); return
            try: fecha=datetime.strptime(vals[labels[3]],self.FORMATO)
            except ValueError: messagebox.showerror("Fecha inválida","Use DD/MM/AAAA.",parent=w); return
            h.huesped=Huesped(vals["Nombre"],vals["Apellidos"],vals["Documento"],fecha)
            messagebox.showinfo("Éxito",f"Huésped registrado en habitación {h.numero}.",parent=w); w.destroy()
        ttk.Button(w,text="Registrar ingreso",command=registrar).pack(pady=14)

    def salida(self):
        w=tk.Toplevel(self.root); w.title("Salida de huéspedes"); w.geometry("440x360")
        ttk.Label(w,text="Registrar salida",font=("Arial",14,"bold")).pack(pady=12)
        ttk.Label(w,text="Número de habitación (1-10):").pack()
        num=ttk.Entry(w,width=16); num.pack(pady=4)
        ttk.Label(w,text="Fecha de salida (DD/MM/AAAA):").pack(pady=(10,3))
        fecha=ttk.Entry(w,width=16); fecha.pack()
        resultado=ttk.Label(w,text="",justify="center"); resultado.pack(pady=14)
        confirmar=ttk.Button(w,text="Registrar salida",state="disabled"); confirmar.pack(pady=5)
        seleccion={}
        def calcular():
            h=self.buscar(num.get().strip())
            if h is None: messagebox.showerror("Dato incorrecto","Ingrese habitación entre 1 y 10.",parent=w); return
            if h.disponible: messagebox.showerror("No ocupada","La habitación no está ocupada.",parent=w); return
            try: fs=datetime.strptime(fecha.get().strip(),self.FORMATO)
            except ValueError: messagebox.showerror("Fecha inválida","Use DD/MM/AAAA.",parent=w); return
            fi=h.huesped.fecha_ingreso
            if fs<=fi: messagebox.showerror("Fecha incorrecta","La salida debe ser posterior al ingreso.",parent=w); return
            dias=(fs.date()-fi.date()).days; total=dias*h.precio_dia; seleccion["h"]=h
            resultado.config(text=f"Huésped: {h.huesped.nombre} {h.huesped.apellidos}\\nDías: {dias}\\nTotal a pagar: $ {total:,.0f}")
            confirmar.config(state="normal")
        def registrar():
            h=seleccion.get("h")
            if h:
                h.huesped=None; messagebox.showinfo("Salida registrada",f"Habitación {h.numero} disponible.",parent=w); w.destroy()
        ttk.Button(w,text="Calcular total",command=calcular).pack(pady=7)
        confirmar.config(command=registrar)

if __name__=="__main__":
    root=tk.Tk(); app=AplicacionHotel(root); root.mainloop()
