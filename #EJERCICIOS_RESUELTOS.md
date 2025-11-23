# =====================================================
# Python Junior — Chuleta + Ejercicios + Preguntas
# =====================================================

# -----------------------------
# 1. Imprimir en pantalla
# -----------------------------
print("Hola Mundo")  # mostrar texto en pantalla

# Mini-ejercicio resuelto:
nombre = "Zyanetralys"
edad = 33
print("Nombre:", nombre, "| Edad:", edad)

# Pregunta típica de entrevista:
# Q: ¿Cuál es la diferencia entre print() y return en Python?
# A: print() muestra en pantalla; return devuelve un valor dentro de una función.

# -----------------------------
# 2. Comentarios
# -----------------------------
# Comentario de una línea

"""
Comentario
de varias líneas
"""

# Mini-ejercicio resuelto:
# Añade un comentario explicando el propósito de tu variable 'edad'
edad = 33  # Edad de Zyanetralys

# Pregunta de entrevista:
# Q: ¿Para qué sirven los comentarios?
# A: Explicar código para humanos, no afecta la ejecución.

# -----------------------------
# 3. Variables y tipos
# -----------------------------
x = 10             # int
y = 3.5            # float
activo = True      # bool
nombre = "Zyanetralys"  # str

# Mini-ejercicio resuelto:
ciudad = "Madrid"
pais = "España"
poblacion = 3200000
print(ciudad, pais, poblacion)

# Pregunta:
# Q: ¿Qué tipos básicos de datos conoces en Python?
# A: int, float, str, bool

# -----------------------------
# 4. Operadores
# -----------------------------
# Aritméticos
a = 5
b = 2
print(a + b)  # 7
print(a - b)  # 3
print(a * b)  # 10
print(a / b)  # 2.5
print(a // b) # 2 (división entera)
print(a % b)  # 1 (resto)
print(a ** b) # 25 (potencia)

# Comparación
print(a == b)  # False
print(a != b)  # True
print(a > b)   # True

# Lógicos
print(a > 3 and b < 5)  # True
print(not (a > 3))      # False

# Mini-ejercicio:
x = 7
y = 10
print(x < y or x == 7)  # True

# -----------------------------
# 5. Condicionales
# -----------------------------
edad = 18
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")

nota = 8
if nota >= 9:
    print("Sobresaliente")
elif nota >= 7:
    print("Notable")
else:
    print("Aprobado o Suspenso")

# Mini-ejercicio resuelto:
numero = -5
if numero > 0:
    print("Positivo")
elif numero < 0:
    print("Negativo")
else:
    print("Cero")

# Pregunta:
# Q: ¿Qué es elif y por qué se usa?
# A: Es “else if”, permite evaluar múltiples condiciones en orden.

# -----------------------------
# 6. Bucles
# -----------------------------
# For
for i in range(5):
    print("For loop:", i)

# While
i = 5
while i > 0:
    print("While loop:", i)
    i -= 1

# Mini-ejercicio resuelto:
for num in range(2, 11, 2):
    print("Número par:", num)

# Pregunta:
# Q: Diferencia entre for y while
# A: For recorre una secuencia; while repite mientras la condición sea True

# -----------------------------
# 7. Listas
# -----------------------------
armas = ["Nmap", "Gobuster", "SQLmap"]
armas.append("Metasploit")
armas.remove("Gobuster")
armas.pop(0)
print("Lista armas:", armas)
print("Longitud:", len(armas))

# Recorrer lista
for arma in armas:
    print("Revisando arma:", arma)

# Mini-ejercicio resuelto:
herramientas = ["Wireshark", "Burp Suite", "Hydra"]
for h in herramientas:
    print("Herramienta:", h)

# Pregunta:
# Q: Diferencia entre append() y extend()
# A: append() añade un elemento, extend() añade múltiples elementos de otra lista

# -----------------------------
# 8. Diccionarios
# -----------------------------
usuario = {"nombre": "Zyanetralys", "nivel": 1}
usuario["rango"] = "Recluta"
print(usuario)

for clave, valor in usuario.items():
    print(clave, ":", valor)

# Mini-ejercicio resuelto:
info = {"ciudad": "Madrid", "pais": "España", "edad": 33}
for k, v in info.items():
    print(k, "->", v)

# Pregunta:
# Q: Cómo acceder a un valor y cómo añadir un nuevo campo
# A: valor = diccionario["clave"], diccionario["nueva_clave"] = valor

# -----------------------------
# 9. Strings
# -----------------------------
texto = "Hola Mundo"
print(texto.upper())
print(texto.lower())
print(texto.split())
print(" ".join(["Python", "es", "genial"]))

# Mini-ejercicio resuelto:
nombre_completo = "Zya Netralys"
print(nombre_completo.upper())
print(nombre_completo.lower())
print(nombre_completo.split())

# Pregunta:
# Q: Qué hace split() y join()
# A: split() divide un string en lista; join() une lista en string

# -----------------------------
# 10. Funciones
# -----------------------------
def saludar(nombre):
    print("Hola", nombre)

saludar("Zyanetralys")

def multiplicar(a, b):
    return a * b

print(multiplicar(4, 5))

# Mini-ejercicio resuelto:
def bienvenida(nombre):
    return "Bienvenido " + nombre

print(bienvenida("Zyanetralys"))

# Pregunta:
# Q: Diferencia entre print() y return
# A: print() muestra; return devuelve un valor usable dentro de código

# -----------------------------
# 11. Manejo de errores
# -----------------------------
try:
    x = int("abc")
except ValueError:
    print("Error: no se puede convertir a int")
finally:
    print("Bloque finalizado")

# Mini-ejercicio resuelto:
try:
    y = 1 / 0
except ZeroDivisionError:
    print("División por cero detectada")

# Pregunta:
# Q: Para qué sirve finally
# A: Se ejecuta siempre, haya o no excepción

# -----------------------------
# 12. Módulos
# -----------------------------
import math
import random

print(math.sqrt(25))
print(math.pow(2, 4))
print(random.randint(1, 100))

# Mini-ejercicio resuelto:
numeros = [random.randint(1, 100) for _ in range(5)]
print("Números aleatorios:", numeros)

# Pregunta:
# Q: Cómo importas solo una función de un módulo
# A: from math import sqrt

# -----------------------------
# 13. Ejemplo práctico completo
# -----------------------------
objetivos = ["ssh", "http", "ftp", "rdp"]
vulnerables = 0

for obj in objetivos:
    if "h" in obj:
        print("Atención, contiene h:", obj)
        vulnerables += 1
    else:
        print("Servicio seguro:", obj)

print("Total servicios con 'h':", vulnerables)

# Mini-ejercicio resuelto:
# Crea un programa que recorra la lista ["a", "b", "c", "d"] y cuente letras 'a'
letras = ["a", "b", "a", "c", "a"]
count_a = 0
for letra in letras:
    if letra == "a":
        count_a += 1
print("Número de 'a':", count_a)
