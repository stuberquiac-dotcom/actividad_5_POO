import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass
import os

@dataclass
class Empleado:
    nombre: str
    apellidos: str
    cargo: str
    genero: str
    salario_dia: float
    dias_trabajados: int
    otros_ingresos: float
    salud: float
    pension: float

    @property
    def salario_mensual(self):
        return self.dias_trabajados*self.salario_dia + self.otros_ingresos - self.salud - self.pension

class AplicacionNomina:
    def __init__(self, root):
        self.root=root; self.root.title("Sistema de nómina"); self.root.geometry("760x430")
        self.empleados=[]
        barra=tk.Menu(root); menu=tk.Menu(barra,tearoff=0)
        menu.add_command(label="Agregar empleado",command=self.agregar)
        menu.add_command(label="Calcular nómina",command=self.calcular)
        menu.add_command(label="Guardar archivo",command=self.guardar)
        barra.add_cascade(label="Opciones",menu=menu); root.config(menu=barra)
        ttk.Label(root,text="GESTIÓN DE NÓMINA",font=("Arial",20,"bold")).pack(pady=35)
        ttk.Label(root,text="Agregue empleados, consulte el cálculo de nómina o guarde el reporte.").pack(pady=10)
        self.estado=ttk.Label(root,text="Empleados registrados: 0"); self.estado.pack(pady=20)

    def agregar(self):
        w=tk.Toplevel(self.root); w.title("Agregar empleado"); w.geometry("440x510")
        specs=[("Nombre",None),("Apellidos",None),("Cargo",["Directivo","Estratégico","Operativo"]),
               ("Género",["Masculino","Femenino"]),("Salario por día",None),("Días trabajados (1-31)",None),
               ("Otros ingresos",None),("Pagos por salud",None),("Aporte pensiones",None)]
        widgets={}
        for i,(label,values) in enumerate(specs):
            ttk.Label(w,text=label).grid(row=i,column=0,sticky="w",padx=12,pady=7)
            x=ttk.Combobox(w,values=values,state="readonly",width=25) if values else ttk.Entry(w,width=28)
            if values: x.current(0)
            x.grid(row=i,column=1,padx=10,pady=7); widgets[label]=x
        def registrar():
            nombre=widgets["Nombre"].get().strip(); apellidos=widgets["Apellidos"].get().strip()
            if not nombre or not apellidos:
                messagebox.showerror("Datos incompletos","Nombre y apellidos son obligatorios.",parent=w); return
            try:
                salario=float(widgets["Salario por día"].get()); dias=int(widgets["Días trabajados (1-31)"].get())
                otros=float(widgets["Otros ingresos"].get() or 0); salud=float(widgets["Pagos por salud"].get() or 0)
                pension=float(widgets["Aporte pensiones"].get() or 0)
                if salario<0 or min(otros,salud,pension)<0 or not 1<=dias<=31: raise ValueError
            except ValueError:
                messagebox.showerror("Dato inválido","Use valores numéricos no negativos y días entre 1 y 31.",parent=w); return
            self.empleados.append(Empleado(nombre,apellidos,widgets["Cargo"].get(),widgets["Género"].get(),salario,dias,otros,salud,pension))
            self.estado.config(text=f"Empleados registrados: {len(self.empleados)}")
            messagebox.showinfo("Éxito","Empleado agregado correctamente.",parent=w); w.destroy()
        ttk.Button(w,text="Registrar empleado",command=registrar).grid(row=9,column=0,columnspan=2,pady=18)

    def calcular(self):
        if not self.empleados:
            messagebox.showwarning("Sin empleados","Primero agregue empleados."); return
        w=tk.Toplevel(self.root); w.title("Cálculo de nómina"); w.geometry("700x380")
        cols=("nombre","apellidos","sueldo"); t=ttk.Treeview(w,columns=cols,show="headings")
        for c,txt in zip(cols,("Nombres","Apellidos","Sueldo mensual")): t.heading(c,text=txt)
        t.column("nombre",width=180); t.column("apellidos",width=220); t.column("sueldo",width=180,anchor="e")
        t.pack(fill="both",expand=True,padx=12,pady=12)
        total=0
        for e in self.empleados:
            t.insert("","end",values=(e.nombre,e.apellidos,f"$ {e.salario_mensual:,.2f}")); total+=e.salario_mensual
        ttk.Label(w,text=f"TOTAL DE LA NÓMINA: $ {total:,.2f}",font=("Arial",13,"bold")).pack(pady=12)

    def guardar(self):
        if not self.empleados:
            messagebox.showwarning("Sin empleados","No hay datos para guardar."); return
        carpeta=filedialog.askdirectory(title="Seleccione la carpeta para Nómina.txt")
        if not carpeta: return
        total=sum(e.salario_mensual for e in self.empleados); ruta=os.path.join(carpeta,"Nómina.txt")
        try:
            with open(ruta,"w",encoding="utf-8") as f:
                f.write("REPORTE DE NÓMINA\\n"+"="*50+"\\n")
                for e in self.empleados:
                    f.write(f"Nombre: {e.nombre} {e.apellidos}\\nCargo: {e.cargo}\\nGénero: {e.genero}\\n"
                            f"Salario por día: {e.salario_dia:.2f}\\nDías trabajados: {e.dias_trabajados}\\n"
                            f"Otros ingresos: {e.otros_ingresos:.2f}\\nPagos por salud: {e.salud:.2f}\\n"
                            f"Aporte pensiones: {e.pension:.2f}\\nSalario mensual: {e.salario_mensual:.2f}\\n"+"-"*50+"\\n")
                f.write(f"TOTAL DE LA NÓMINA: {total:.2f}\\n")
            messagebox.showinfo("Guardado",f"Archivo creado en:\\n{ruta}")
        except OSError as err: messagebox.showerror("Error",str(err))

if __name__=="__main__":
    root=tk.Tk(); app=AplicacionNomina(root); root.mainloop()
