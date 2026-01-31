#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rrhh_candidatos.py
Pequeña utilidad para llevar registro de candidatos sin depender de mil herramientas
"""

import csv
import os
from datetime import datetime
from pathlib import Path

RUTA_DATOS = Path.home() / "Documentos" / "rrhh_alvatross"
RUTA_CSV = RUTA_DATOS / "candidatos.csv"
CAMPOS = ["id", "nombre", "email", "telefono", "puesto", "stack", "salario_esperado", "estado", "notas", "fecha_registro"]


def _inicializar_directorio():
    """Crea la carpeta de datos si no existe."""
    RUTA_DATOS.mkdir(parents=True, exist_ok=True)


def _leer_csv():
    """Devuelve lista de candidatos o lista vacía si el archivo no existe."""
    if not RUTA_CSV.exists():
        return []
    
    with open(RUTA_CSV, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _escribir_csv(candidatos):
    """Sobreescribe el CSV con la lista actual. Simple y sin dramas."""
    with open(RUTA_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(candidatos)


def nuevo_candidato():
    print("\n--- Nuevo candidato ---")
    print("(Deja en blanco y pulsa Enter para saltar un campo)")

    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("⚠️  Sin nombre no hay candidato. Volviendo al menú.")
        return

    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    puesto = input("Puesto al que aplica: ").strip() or "Sin especificar"
    stack = input("Stack (ej: Java/Spring, AWS, TMForum): ").strip() or "Por evaluar"
    salario = input("Expectativa salarial (k€): ").strip() or "?"
    notas = input("Notas rápidas: ").strip() or "-"

    candidato = {
        "id": datetime.now().strftime("%y%m%d%H%M"),
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "puesto": puesto,
        "stack": stack,
        "salario_esperado": salario,
        "estado": "screening",
        "notas": notas,
        "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    candidatos = _leer_csv()
    candidatos.append(candidato)
    _escribir_csv(candidatos)

    print(f"\n✅ Guardado: {nombre} | ID: {candidato['id']}")
    # ese momento en que el script funciona a la primera y el café sigue caliente
    # ...bueno, casi siempre quemado, pero funciona


def listar_candidatos(filtro_estado=None):
    candidatos = _leer_csv()
    if not candidatos:
        print("\n📭 Bandeja vacía. Ni un CV a la vista.")
        return

    # Filtrar si aplica
    if filtro_estado:
        candidatos = [c for c in candidatos if c["estado"] == filtro_estado]
        if not candidatos:
            print(f"\n📭 Sin candidatos en estado '{filtro_estado}'")
            return

    print("\n--- Candidatos registrados ---")
    for c in candidatos:
        print(f"\n[{c['id']}] {c['nombre']}")
        print(f"   Puesto: {c['puesto']}")
        print(f"   Stack:  {c['stack']}")
        print(f"   €:      {c['salario_esperado']}k | Estado: {c['estado']}")
        if c["notas"] != "-":
            print(f"   Notas:  {c['notas']}")
        print(f"   Reg:    {c['fecha_registro']}")


def cambiar_estado():
    cid = input("\nID del candidato: ").strip()
    candidatos = _leer_csv()
    
    for c in candidatos:
        if c["id"] == cid:
            print(f"\nCandidato: {c['nombre']}")
            print(f"Estado actual: {c['estado']}")
            print("\nEstados válidos: screening | entrevista-tech | entrevista-hm | offer | descartado")
            nuevo = input("Nuevo estado: ").strip().lower()
            if nuevo:
                c["estado"] = nuevo
                _escribir_csv(candidatos)
                print(f"✅ Estado actualizado a '{nuevo}'")
            return
    
    print("❌ ID no encontrado. Revisa la lista.")


def busqueda_rapida():
    termino = input("\nBuscar en nombre/stack/puesto: ").strip().lower()
    if not termino:
        return

    candidatos = _leer_csv()
    resultados = [
        c for c in candidatos
        if termino in c["nombre"].lower() 
        or termino in c["stack"].lower()
        or termino in c["puesto"].lower()
    ]

    if not resultados:
        print(f"\n📭 Nada encontrado con '{termino}'")
        return

    print(f"\n--- Resultados ({len(resultados)}) ---")
    for c in resultados:
        print(f"[{c['id']}] {c['nombre']} | {c['puesto']} | {c['stack']}")


def menu_principal():
    _inicializar_directorio()

    while True:
        print("\n" + "="*50)
        print(" RRHH Alvatross - Gestor rápido de candidatos")
        print("="*50)
        print(" 1. Nuevo candidato")
        print(" 2. Listar todos")
        print(" 3. Listar por estado (screening/entrevista/offer/...)")
        print(" 4. Buscar rápido")
        print(" 5. Cambiar estado")
        print(" 0. Salir")
        print("-"*50)

        opcion = input(" > ").strip()

        if opcion == "1":
            nuevo_candidato()
        elif opcion == "2":
            listar_candidatos()
        elif opcion == "3":
            estado = input("Estado (screening/entrevista-tech/entrevista-hm/offer/descartado): ").strip()
            listar_candidatos(filtro_estado=estado)
        elif opcion == "4":
            busqueda_rapida()
        elif opcion == "5":
            cambiar_estado()
        elif opcion == "0":
            print("\n👋 Hasta luego. Que el stack te acompañe.")
            break
        else:
            print("\n⚠️  Opción no válida. Prueba otra.")


if __name__ == "__main__":
    menu_principal()
