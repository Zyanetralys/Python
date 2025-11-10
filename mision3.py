energia = 100
nivel = 2
activo = True

# Estado de alerta
virus_detectado = True
sistema_secundario_dañado = False

if energia < 50:
    activo = False
    print("Energía crítica, suspendiendo operaciones.")
elif virus_detectado and not sistema_secundario_dañado:
    energia -= 20
    print("Defendiendo sistema primario, energía restante:", energia)
else:
    energia += 10
    print("Recuperando recursos, energía:", energia)

if energia > 50:
    activo = True
    print("Sistemas funcionales, energía:", energia)

# Entrada de usuario
codigo = input("Introduce código de autorización: ")

if codigo == "ALFA":
    energia += 20
else:
    energia -= 10

print("Nivel de energía:", energia)
print("Nivel:", nivel)
print("Nivel de actividad:", activo)
