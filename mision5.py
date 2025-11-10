# mision5.py
import random
import time
import logging

# ---- Configuración de logging ----
logging.basicConfig(
    filename="mision5_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ---- Estado inicial ----
energia = 100
nivel = 3
activo = True

# ---- Funciones ----
def status():
    """Devuelve una tupla con el estado actual."""
    return energia, nivel, activo

def aplicar_perdida(e):
    """Resta energía de forma segura y actualiza estado activo."""
    global energia, activo
    energia -= e
    if energia < 0:
        energia = 0
    if energia < 50:
        activo = False
    logging.info(f"Pérdida aplicada: {e}. Energía ahora: {energia}. Activo: {activo}")
    return energia

def aplicar_refuerzo(v):
    """Aumenta energía y registra evento."""
    global energia
    energia += v
    logging.info(f"Refuerzo aplicado: {v}. Energía ahora: {energia}")
    return energia

def intentar_contraataque(nivel_intento):
    """
    Simula un intento de contraataque:
    - éxito depende de nivel_intento y un factor aleatorio.
    - devuelve (exito: bool, impacto: int)
    """
    global nivel
    base_chance = 40 + (nivel * 5) + (nivel_intento * 5)  # porcentaje base
    roll = random.randint(1, 100)
    exito = roll <= base_chance
    impacto = random.randint(5, 25) if not exito else random.randint(10, 5 + nivel_intento * 10)
    logging.info(f"Contraataque intento {nivel_intento}: roll={roll}, base_chance={base_chance}, exito={exito}, impacto={impacto}")
    return exito, impacto

# ---- Simulación principal ----
def simulacion_contraataque():
    global energia, nivel, activo
    print("INICIANDO CONTRAATAQUE AUTOMATIZADO - MISION 5")
    logging.info("Misión 5 iniciada")
    objetivos = ["Nodo de filtrado", "C2 hostil", "Proxy reverse", "Exfiltración abierta"]
    for idx, objetivo in enumerate(objetivos, start=1):
        if not activo:
            print("\nOperaciones suspendidas: energía crítica.")
            logging.warning("Operaciones suspendidas por energía crítica.")
            break

        print(f"\nObjetivo {idx}: {objetivo}")
        perdida = random.randint(5, 15)
        aplicar_perdida(perdida)
        print(f"Energía tras incursión defensiva: {energia}")

        # opción de contraataque: elegir nivel de riesgo
        try:
            nivel_op = int(input("Selecciona nivel de contraataque (1=bajo, 2=medio, 3=alto): ").strip())
            if nivel_op not in (1,2,3):
                raise ValueError("Nivel inválido")
        except Exception as e:
            print("Entrada inválida. Se selecciona nivel 1 por defecto.")
            logging.error(f"Entrada inválida para nivel_op: {e}")
            nivel_op = 1

        # intentar contraataque
        exito, impacto = intentar_contraataque(nivel_op)
        if exito:
            energia = aplicar_refuerzo(impacto)
            nivel += 1
            print(f"✅ Contraataque exitoso. Energía reforzada +{impacto}. Nivel operativo: {nivel}")
        else:
            energia = aplicar_perdida(impacto)
            print(f"Contraataque fallido. Pérdida extra {impacto}. Energía ahora: {energia}")
            # Si la energía baja demasiado, pedir confirmación para seguir
            if energia < 40:
                resp = input("Energía baja. ¿Continuar? (S/N): ").strip().upper()
                if resp != "S":
                    print("Retirada ordenada. Terminando misión.")
                    logging.info("Retirada ordenada por decisión del usuario.")
                    break

        time.sleep(0.5)  # sensación de tiempo entre acciones

    # Ataque final: evaluación y registro
    print("\nEVALUACIÓN FINAL DE LA MISION 5")
    logging.info("Evaluación final iniciada")
    print(f"Energía final: {energia}")
    print(f"Nivel final: {nivel}")
    print(f"Activo: {activo}")
    logging.info(f"Resultado final - Energia: {energia}, Nivel: {nivel}, Activo: {activo}")

if __name__ == "__main__":
    try:
        simulacion_contraataque()
    except Exception as exc:
        print("ERROR CRÍTICO EN LA SIMULACIÓN:", exc)
        logging.exception("Excepción no manejada en simulación")
