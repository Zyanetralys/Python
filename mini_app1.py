import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Crear la ventana principal
# -----------------------------
ventana = tk.Tk()
ventana.title("Mi primera app")
ventana.geometry("400x250")  # tamaño de la ventana

# -----------------------------
# Etiquetas y entradas
# -----------------------------
# Etiqueta para nombre
etiqueta_nombre = tk.Label(ventana, text="Escribe tu nombre:")
etiqueta_nombre.pack(pady=5)

# Entrada para nombre
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack(pady=5)

# Etiqueta para edad
etiqueta_edad = tk.Label(ventana, text="Escribe tu edad:")
etiqueta_edad.pack(pady=5)

# Entrada para edad
entrada_edad = tk.Entry(ventana)
entrada_edad.pack(pady=5)

# -----------------------------
# Función del botón
# -----------------------------
def saludar():
    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    if nombre and edad:
        try:
            edad_int = int(edad)
            messagebox.showinfo("Saludo", f"Hola {nombre}, tienes {edad_int} años. ¡Bienvenida!")
        except ValueError:
            messagebox.showwarning("Error", "La edad debe ser un número")
    else:
        messagebox.showwarning("Error", "Escribe tu nombre y tu edad primero")

# -----------------------------
# Botón para saludar
# -----------------------------
boton_saludo = tk.Button(ventana, text="Saludar", command=saludar)
boton_saludo.pack(pady=10)

# -----------------------------
# Ejecutar la app
# -----------------------------
ventana.mainloop()
