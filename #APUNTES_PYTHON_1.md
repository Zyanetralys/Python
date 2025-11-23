# ===============================
# Python Junior — Chuleta Completa
# ===============================

# 1. Imprimir en pantalla
print("Hola Mundo")

# 2. Comentarios
# Esto es un comentario
"""
Esto es un comentario
de varias líneas
"""

# 3. Variables y tipos
x = 10                 # int
y = 3.5                # float
nombre = "Zyanetralys" # str
activo = True          # bool

# 4. Operadores
# Aritméticos
# +, -, *, /, //, %, **
print(5 + 3)
print(10 // 3)    # división entera
print(5 ** 2)     # potencia

# Comparación
# ==, !=, >, <, >=, <=
print(5 == 5)     # True
print(3 != 4)     # True

# Lógicos
# and, or, not
print(True and False)  # False
print(not True)        # False

# 5. Condicionales
edad = 18
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")

# 6. Bucles
# For
for i in range(5):
    print("For loop:", i)

# While
i = 0
while i < 5:
    print("While loop:", i)
    i += 1

# 7. Listas
armas = ["Nmap", "Gobuster", "SQLmap"]

# Métodos clave
armas.append("Metasploit")  # añadir al final
armas.remove("Gobuster")    # eliminar por valor
armas.pop(0)                # eliminar por posición
print(len(armas))           # longitud de la lista
print(armas[0])             # acceder al primer elemento
print(armas[-1])            # acceder al último elemento

# 8. Diccionarios
usuario = {
    "nombre": "Zyanetralys",
    "nivel": 1
}
print(usuario["nombre"])  # acceder
usuario["rango"] = "Recluta"  # añadir campo
print(usuario)

# 9. Strings (cadenas)
texto = "Hola Mundo"
print(texto.upper())  # MAYÚSCULAS
print(texto.lower())  # minúsculas
print(texto.split())  # separar por espacios en lista

# 10. Funciones
def saludar(nombre):
    print("Hola", nombre)

saludar("Zyanetralys")

def sumar(a, b):
    return a + b

resultado = sumar(3, 5)
print(resultado)

# 11. Errores y excepciones
try:
    x = 1 / 0
except ZeroDivisionError:
    print("No puedes dividir entre cero")

# 12. Módulos
import math
import random

print(math.sqrt(16))        # 4.0
print(random.randint(1, 10)) # aleatorio entre 1 y 10

# 13. Ejemplo práctico completo
objetivos = ["ssh", "http", "ftp", "rdp"]

for obj in objetivos:
    if obj == "ftp":
        print("Alerta: servicio vulnerable detectado →", obj)
    else:
        print("Servicio estándar:", obj)
