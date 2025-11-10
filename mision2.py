agente = "Zyanetralys"
nivel = 1
energia = 100.0
activo = True

#Pierdes 30 de energia
energia = energia - 30

# Sube tu nivel en 1
{nivel + 1}

# Verifica energia y cambia estado si es necesario
if energia < 50:
    activo = False

# Mostrar estado
print("Agente", agente)
print("Nivel", nivel)
print("Energua", energia)
print("Activo", activo)

#Entrada de usuario para clave de acceso
clave = input("Introduce clave de acceso: ")
print("Clave registrada:", clave)
