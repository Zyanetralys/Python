import random

energia = 100
nivel = 2
activo = True

# Lista de ataques simulados
ataques = ["Firewall", "Base de datos", "Servidor web", "Módulo de control", "Red interna"]

for ataque in ataques:
    print("\nAlerta de ataque en:", ataque)
    
    perdida = random.randint(5, 20)
    energia -= perdida
    print("Energía perdida:", perdida, "Energía restante:", energia)
    
    if energia < 50:
        activo = False
        print("Energía crítica, suspendiendo operaciones.")
        break
    
    # Entrada de código de autorización
    codigo = input("Introduce código de autorización para reforzar energía: ")
    if codigo == "ALFA":
        energia += 20
        print("✅ Energía reforzada, nueva energía:", energia)
    else:
        print("Código inválido, energía sin cambios.")
    
    nivel += 1
    print("Nivel operativo actualizado:", nivel)

force_final = True

if force_final:
    print("\n--- ATAQUE FINAL: Red interna (ejecución forzada) ---")
    perdida_final = random.randint(5, 20)
    energia -= perdida_final
    print("Energía perdida en ataque final:", perdida_final, "Energía restante:", energia)

    if energia < 50:
        activo = False
        print("Energía crítica tras ataque final, operaciones suspendidas.")
    else:
        # permitir una última entrada para intentar reforzar si es posible
        codigo = input("Introduce código final de autorización (ALFA para reforzar): ")
        if codigo == "ALFA":
            energia += 20
            print("Energía reforzada tras ataque final, nueva energía:", energia)
        else:
            print("Código inválido o no introducido, energía sin cambios.")

    nivel += 1
    print("Nivel operativo actualizado (post-final):", nivel)

print("\n--- Misión finalizada ---")
print("Energía final:", energia)
print("Nivel final:", nivel)
print("Estado activo:", activo)
