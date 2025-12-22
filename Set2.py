def hola():
    nombre = "Juan"
    print("hola", nombre)
    
hola()

def contador():
    contar = 0    
    for i in range(3):
        contar += 1
        print("saludo", contar)

contador()



def imprimir():
    print("he aprendido a hacer funciones")

imprimir()



def saludo_inteligente():
    nombre_usuario = input("Escribe tu nombre: ")

    if nombre_usuario == "":
        print("No escribiste ningún nombre")
        return

    longitud_nombre = len(nombre_usuario)
    es_nombre_largo = longitud_nombre > 5

    print("Hola", nombre_usuario)
    print("Tu nombre tiene", longitud_nombre, "letras")

    if es_nombre_largo:
        print("Tu nombre es largo")
    else:
        print("Tu nombre es corto")

    print("Saludando varias veces:")

    for i in range(3):
        print("Saludo", i + 3, "para", nombre_usuario)

saludo_inteligente()



variable_edad = 26

if variable_edad >= 18:
    print("Eres mayor de edad y tu edad es:", variable_edad)
else:
    print("No eres mayor de edad y tu edad es:", variable_edad)


def saludo():
	nombre_usuario = input("Introduce tu usuario:" )
	print ("Hola", nombre_usuario)

saludo()
