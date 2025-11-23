#Variables

a = 10
b = 10.5
c = "Hola"
d = True

print(a,type(a))
print(b,type(b))
print(c,type(c))
print(d,type(d))

#Control de acceso

edad = int(input("Tu edad: "))

if edad >= 18:
    print("Puedes entrar")
else:
    print("No puedes entrar")

#Suma de 5 numeros

def es_par(n):
    if n % 2 == 0:
        return True
    else:
        return False

n = int(input("Dime un numero:"))
if es_par(n):
    print("Es par")
else:
    print("Es impar")
