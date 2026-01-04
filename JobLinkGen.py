#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZYANETRALYS – Job Link Generator

"""

import webbrowser
import urllib.parse
import csv
import os
from datetime import datetime
from typing import List, Optional, Dict

# Soporte por país
COUNTRY_DOMAINS = {
    'es': {'indeed': 'es', 'linkedin': 'es', 'glassdoor': 'es'},
    'uk': {'indeed': 'co.uk', 'linkedin': 'uk', 'glassdoor': 'co.uk'},
    'us': {'indeed': 'com', 'linkedin': 'com', 'glassdoor': 'com'},
    'de': {'indeed': 'de', 'linkedin': 'de', 'glassdoor': 'de'},
    'fr': {'indeed': 'fr', 'linkedin': 'fr', 'glassdoor': 'fr'},
}

BACK_KEYWORDS = {"«", "back", "atrás", "volver"}

def safe_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value in BACK_KEYWORDS:
            raise KeyboardInterrupt
        return value

def ask_optional(prompt: str) -> Optional[str]:
    try:
        val = safe_input(prompt)
        return val if val else None
    except KeyboardInterrupt:
        return "BACK"

def ask_list(prompt: str) -> List[str]:
    try:
        raw = safe_input(prompt)
        return [x.strip().lower() for x in raw.split(',') if x.strip()]
    except KeyboardInterrupt:
        return ["BACK"]

def normalize_modality(mod: str) -> str:
    mod = mod.lower()
    if mod in ("remoto", "teletrabajo", "remote"):
        return "remoto"
    elif mod in ("hibrido", "híbrido", "hybrid"):
        return "híbrido"
    elif mod in ("presencial", "presencia", "on-site"):
        return "presencial"
    return "cualquiera"

def normalize_shift(shift: str) -> str:
    s = shift.lower()
    if "mañana" in s:
        return "mañana"
    elif "tarde" in s:
        return "tarde"
    elif "noche" in s:
        return "noche"
    return "todas"

def get_user_input():
    while True:
        try:
            print("\n[ZYANETRALYS] Protocolo de búsqueda – v3")
            print("→ En cualquier momento, escribe « para retroceder.\n")

            country = ask_optional("País (código ISO: es, uk, us...): ")
            if country == "BACK": continue
            city = ask_optional("Ciudad (o 'remoto' si solo buscas remoto): ")
            if city == "BACK": continue
            technologies = ask_list("Tecnologías (separadas por coma): ")
            if "BACK" in technologies: continue
            position = ask_optional("Puesto / Rol: ")
            if position == "BACK": continue
            area = ask_optional("Área (IT, Ciber, Data, Redes...): ")
            if area == "BACK": continue
            experience_years = ask_optional("Años de experiencia (opcional): ")
            if experience_years == "BACK": continue
            company = ask_optional("Empresa concreta (opcional): ")
            if company == "BACK": continue
            modality = normalize_modality(safe_input("Modalidad (remoto/hibrido/presencial): "))
            contract_type = ask_optional("Tipo de contrato (fijo, freelance, etc.): ")
            if contract_type == "BACK": continue
            seniority = ask_optional("Seniority (junior/mid/senior/lead): ")
            if seniority == "BACK": continue
            shift = normalize_shift(safe_input("Turno: mañana / tarde / noche / todas: "))
            salary_min = ask_optional("Salario mínimo anual (ej: 30000, opcional): ")
            if salary_min == "BACK": continue

            return {
                "country": country,
                "city": city,
                "technologies": technologies,
                "position": position,
                "area": area,
                "experience_years": experience_years,
                "company": company,
                "modality": modality,
                "contract_type": contract_type,
                "seniority": seniority,
                "shift": shift,
                "salary_min": salary_min,
            }

        except KeyboardInterrupt:
            print("\n[INFO] Retrocediendo al inicio...")
            continue

def build_full_query(data: dict) -> str:
    parts = [data["position"]]
    if data["area"]:
        parts.append(data["area"])
    if data["technologies"]:
        parts.extend(data["technologies"])
    if data["seniority"]:
        parts.append(data["seniority"])
    if data["company"]:
        parts.append(data["company"])
    return " ".join(parts)

def build_urls(data: dict) -> List[str]:
    country = data["country"]
    city = data["city"]
    modality = data["modality"]
    shift = data["shift"]
    salary = data["salary_min"]
    full_query = build_full_query(data)
    q = urllib.parse.quote_plus(full_query)
    city_enc = urllib.parse.quote_plus(city) if city and city.lower() != "remoto" else ""

    dom = COUNTRY_DOMAINS.get(country, COUNTRY_DOMAINS["es"])
    urls = []

    # LinkedIn
    if dom.get("linkedin"):
        loc = ""
        if country == "es" and city and city.lower() != "remoto":
            loc = "&location=España"
        elif city and city.lower() != "remoto":
            loc = f"&location={urllib.parse.quote(city)}"
        remote_f = "&f_WT=2" if modality == "remoto" else ("&f_WT=1" if modality == "presencial" else "")
        urls.append(f"https://www.linkedin.com/jobs/search/?keywords={q}{loc}{remote_f}")

    # Indeed
    if dom.get("indeed"):
        domain = dom["indeed"]
        base_domain = f"{'es' if domain == 'es' else domain}.indeed.com"
        loc_param = f"&l={city_enc}" if city_enc else ""
        remote_f = "&sc=0kf%3Aattr%28DSQF7%29" if modality == "remoto" else ("&sc=0kf%3Aattr%28DSQF6%29" if modality == "presencial" else "")
        salary_f = f"&salary={salary}" if salary and salary.isdigit() else ""
        urls.append(f"https://{base_domain}/jobs?q={q}{loc_param}{remote_f}{salary_f}")

    # InfoJobs
    if country == "es":
        params = []
        if data["experience_years"] and data["experience_years"].isdigit():
            params.append(f"exr={min(5, int(data['experience_years']))}")
        if modality == "remoto":
            params.append("wl=1")
        if shift == "mañana":
            params.append("jth=1")
        elif shift == "tarde":
            params.append("jth=2")
        elif shift == "noche":
            params.append("jth=3")
        param_str = "&".join(params)
        sep = "?" if param_str else ""
        urls.append(f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={q}{sep}{param_str}")

    # Tecnoempleo
    if country == "es":
        exp = data["experience_years"] if data["experience_years"] and data["experience_years"].isdigit() else "0"
        base = f"https://www.tecnoempleo.com/busqueda-empleo/{urllib.parse.quote(data['position'])}/,/{exp}/"
        query_params = []
        if data["technologies"]:
            techs = ",".join(data["technologies"])
            query_params.append(f"tecnologias={urllib.parse.quote(techs)}")
        if modality == "remoto":
            query_params.append("teletrabajo=1")
        elif modality == "presencial":
            query_params.append("teletrabajo=0")
        if shift == "mañana":
            query_params.append("turno=1")
        elif shift == "tarde":
            query_params.append("turno=2")
        elif shift == "noche":
            query_params.append("turno=3")
        if query_params:
            base += "?" + "&".join(query_params)
        urls.append(base)

    # Joppy
    joppy_q = full_query + (" españa" if country == "es" else "")
    urls.append(f"https://joppy.com/jobs?query={urllib.parse.quote_plus(joppy_q)}")

    # Glassdoor
    if dom.get("glassdoor"):
        loc = f"&location={city_enc}" if city_enc else ""
        remote_gd = "&remote_work_allowed=1" if modality == "remoto" else ""
        salary_gd = f"&salary={salary}" if salary and salary.isdigit() else ""
        urls.append(f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={q}{loc}{remote_gd}{salary_gd}")

    return urls

def export_results(urls: List[str], data: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_file = f"zyanetralys_jobs_{timestamp}.txt"
    csv_file = f"zyanetralys_jobs_{timestamp}.csv"

    metadata = {
        "Fecha": datetime.now().isoformat(),
        "País": data["country"],
        "Ciudad": data["city"],
        "Puesto": data["position"],
        "Área": data["area"],
        "Tecnologías": ", ".join(data["technologies"]) if data["technologies"] else "N/A",
        "Experiencia": data["experience_years"] or "N/A",
        "Modalidad": data["modality"],
        "Turno": data["shift"],
        "Seniority": data["seniority"] or "N/A",
        "Empresa": data["company"] or "N/A",
        "Contrato": data["contract_type"] or "N/A",
        "Salario_min": data["salary_min"] or "N/A",
    }

    # TXT
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("=== ZYANETRALYS – Búsqueda de empleo ===\n\n")
        for k, v in metadata.items():
            f.write(f"{k}: {v}\n")
        f.write("\n--- Enlaces ---\n")
        for u in urls:
            f.write(u + "\n")

    # CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metadato", "Valor"])
        for k, v in metadata.items():
            writer.writerow([k, v])
        writer.writerow(["", ""])
        writer.writerow(["Enlace", "URL"])
        for u in urls:
            writer.writerow(["Oferta", u])

    print(f"\n✅ Exportado:\n - TXT: {txt_file}\n - CSV: {csv_file}")
    return txt_file, csv_file

def handle_results(urls: List[str], data: dict):
    print(f"\n[RESULTADOS] Se generaron {len(urls)} enlaces:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")

    while True:
        print("\n¿Qué deseas hacer?")
        print("  1. Abrir TODOS los enlaces en el navegador")
        print("  2. Seleccionar enlaces específicos para abrir")
        print("  3. Solo exportar (TXT + CSV)")
        print("  4. Exportar y abrir TODOS")
        print("  5. Retroceder (nueva búsqueda)")

        choice = input("Elige opción (1-5): ").strip()
        if choice == "5":
            return "RETRY"
        elif choice == "3":
            export_results(urls, data)
            return "DONE"
        elif choice in ("1", "4"):
            for url in urls:
                webbrowser.open_new_tab(url)
            if choice == "4":
                export_results(urls, data)
            return "DONE"
        elif choice == "2":
            try:
                selected = input("Introduce los números de los enlaces a abrir (ej: 1,3,5): ").strip()
                indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
                for i in indices:
                    if 0 <= i < len(urls):
                        webbrowser.open_new_tab(urls[i])
                if input("¿Exportar también? (s/n): ").strip().lower() == "s":
                    export_results(urls, data)
                return "DONE"
            except:
                print("[!] Selección inválida.")
        else:
            print("[!] Opción no válida.")

def confirm_exit() -> bool:
    return input("\n¿Confirmar salida? (s/n): ").strip().lower() == "s"

def main():
    while True:
        data = get_user_input()
        urls = build_urls(data)
        if not urls:
            print("[!] No se generaron enlaces. Intenta de nuevo.")
            continue

        action = handle_results(urls, data)
        if action == "RETRY":
            continue

        while True:
            next_step = input("\n¿Nueva búsqueda o salir? (n/s): ").strip().lower()
            if next_step == "n":
                break
            elif next_step == "s":
                if confirm_exit():
                    print("\n[ZYANETRALYS] Protocolo terminado.")
                    return
                else:
                    break
            else:
                print("[!] Usa 'n' para nueva búsqueda o 's' para salir.")

if __name__ == "__main__":
    main()
