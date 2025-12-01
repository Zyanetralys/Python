#Con esto puedes:

#Poner Libro.xlsx en la misma carpeta que el script.

#Instalar dependencias si hace falta:

#pip install pandas numpy openpyxl


#Ejecutar el script y te generará el fichero:

#KPI_2024-12_a_2025-12_COMPLETO.xlsx

import pandas as pd
import numpy as np

# ---------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------

RUTA_LIBRO = "Libro.xlsx"  # fichero original que tú tienes
HOJA_EMPLEADOS = "empleados"
HOJA_KPI_HIST = "KPIS"
SALIDA_KPI = "KPI_2024-12_a_2025-12_COMPLETO.xlsx"

FECHA_INICIO = pd.Timestamp("2024-12-01")
FECHA_FIN = pd.Timestamp("2025-12-01")  # corte 01/12/2025

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------

def parse_date(s):
    """Convierte string/Excel date a datetime con día primero (formato español)."""
    return pd.to_datetime(s, errors="coerce", dayfirst=True)

def map_dpto(d):
    """Mapea la columna DPT al nombre de departamento del KPI."""
    if pd.isna(d):
        return None
    t = str(d).upper().strip()
    mapping = {
        "ADMINISTRACION": "ADMINISTRACION Y FINANZAS",
        "ADMINISTRACIÓN": "ADMINISTRACION Y FINANZAS",
        "ASISTENCIA Y SOPORTE": "ASISTENCIA Y SOPORTE",
        "CENTRALITA": "CENTRALITA",
        "COMERCIAL": "COMERCIAL",
        "CONSULTORIA": "CONSULTORIA ECONOMICA",
        "CONSULTORÍA": "CONSULTORIA ECONOMICA",
        "CONTABILIDAD": "CONTABILIDAD",
        "GESTIÓN DE PROYECTOS": "COORDINACION DE PROYECTOS",
        "GESTION DE PROYECTOS": "COORDINACION DE PROYECTOS",
        "GERENTE DE PROYECTO": "COORDINACION DE PROYECTOS",
        "DESARROLLO": "DESARROLLO Y TECNOLOGIA",
        "TECNOLOGIA": "DESARROLLO Y TECNOLOGIA",
        "TECNOLOGÍA": "DESARROLLO Y TECNOLOGIA",
        "COO": "DIR. TECNOLOGIA, SISTEMAS E INNOVACION",
        "OPERACIONES": "DIR. TECNOLOGIA, SISTEMAS E INNOVACION",
        "DIRECCIÓN GENERAL": "DIRECCIÓN GENERAL",
        "DIRECCION GENERAL": "DIRECCIÓN GENERAL",
        "FORMACIÓN": "FORMACIÓN",
        "FORMACION": "FORMACIÓN",
        "IMPLANTACIÓN": "IMPLANTACIONES Y MIGRACIONES",
        "IMPLANTACION": "IMPLANTACIONES Y MIGRACIONES",
        "MIGRACIONES": "IMPLANTACIONES Y MIGRACIONES",
        "IMPRENTA": "IMPRENTA",
        "INSPECCION": "INSPECCIÓN E INVENTARIOS",
        "INSPECCIÓN": "INSPECCIÓN E INVENTARIOS",
        "INVENTARIOS": "INSPECCIÓN E INVENTARIOS",
        "LIMPIEZA": "LIMPIEZA",
        "RRHH": "RRHH",
        "RECAUDACION": "SERVICIOS TRIBUTARIOS",
        "RECAUDACIÓN": "SERVICIOS TRIBUTARIOS",
        "SISTEMAS": "SISTEMAS",
        "SISTEMAS DE GESTIÓN": "SISTEMAS DE GESTIÓN",
        "SISTEMAS DE GESTION": "SISTEMAS DE GESTIÓN",
        "NOMINAS": "Sº NOMINAS Y PORTAL DEL EMPLEADO",
        "NÓMINAS": "Sº NOMINAS Y PORTAL DEL EMPLEADO",
        "PORTAL DEL EMPLEADO": "Sº NOMINAS Y PORTAL DEL EMPLEADO",
    }
    for k, v in mapping.items():
        if k in t:
            return v
    return None

def map_deleg(p):
    """Mapea Provincia a fila de delegación del KPI."""
    if pd.isna(p):
        return None
    t = str(p).upper().strip()
    deleg = {
        "BURGOS": "DELEGACIÓN BURGOS",
        "CIUDAD REAL": "DELEGACIÓN CIUDAD REAL",
        "CUENCA": "DELEGACIÓN CUENCA",
        "MURCIA": "DELEGACIÓN DE MURCIA",
        "GUADALAJARA": "DELEGACIÓN GUADALAJARA",
        "SALAMANCA": "DELEGACIÓN SALAMANCA",
        "TOLEDO": "DELEGACIÓN TOLEDO",
    }
    return deleg.get(t, None)

def active_mask(base, date_point):
    """Quién está activo (plantilla o becario) en una fecha concreta."""
    return (base['fecha_ini'] <= date_point) & (
        base['fecha_fin'].isna() | (base['fecha_fin'] >= date_point)
    )

def between_period(start_date, series, cutoff):
    """
    Fechas entre inicio de mes y min(fin de mes, FECHA_FIN).
    Sirve para contar altas/bajas dentro del mes.
    """
    end_of_month = start_date + pd.offsets.MonthEnd(0)
    end = min(end_of_month, cutoff)
    return (series >= start_date) & (series <= end)

# ---------------------------
# CARGA DE DATOS
# ---------------------------

xls = pd.ExcelFile(RUTA_LIBRO)
emp = pd.read_excel(xls, HOJA_EMPLEADOS)
kpi_hist = pd.read_excel(xls, HOJA_KPI_HIST)

# Índice del KPI histórico = primera columna (nombres filas)
kpi_hist = kpi_hist.set_index(kpi_hist.columns[0])

# ---------------------------
# PREPARACIÓN DE EMPLEADOS
# ---------------------------

emp['fecha_ini'] = parse_date(emp['Fecha Antigüedad reconocida'])
emp['fecha_baja_col'] = parse_date(emp['Fecha Baja en la empresa'])
emp['fin_contrato_col'] = parse_date(emp['Fin de contrato'])
emp['fecha_fin'] = emp[['fecha_baja_col', 'fin_contrato_col']].max(axis=1)

filtro = emp['Filtro'].astype(str)
mask_exclude = filtro.str.contains("Inc|Prof|Colombia",
                                   case=False, regex=True)
base = emp[~mask_exclude].copy()

# Flags becarios / plantilla
f_base = base['Filtro'].astype(str).str.lower()
base['es_becario'] = f_base.str.contains("becario")
base['es_plantilla'] = ~base['es_becario']

# Fijos vs eventuales según Contrato legal
cl = base['Contrato legal'].astype(str).str.upper()
base['es_fijo'] = base['es_plantilla'] & cl.str.contains("INDEFINIDO|CONVERSION", regex=True)
base['es_eventual'] = base['es_plantilla'] & ~base['es_fijo']

# Sexo
sexo = base['Sexo'].astype(str).str.upper()
base['es_hombre'] = sexo.str.startswith("H")
base['es_mujer'] = sexo.str.startswith("M")

# Fecha nacimiento
base['fecha_nac'] = parse_date(base['Fecha nacimiento'])

# Costes 2025
for colname in ['TOTAL RETRIBUCIÓN 2025', 'Seguridad Social empresa 2025', 'COSTE TOTAL 2025']:
    if colname in base.columns:
        base[colname] = pd.to_numeric(base[colname], errors="coerce").fillna(0.0)
    else:
        base[colname] = 0.0

# Departamentos y delegaciones
base['DEP_KPI'] = base['DPT'].apply(map_dpto)
base['DELEG_KPI'] = base['Provincia'].apply(map_deleg)

# ---------------------------
# COLUMNAS (MESES) A CALCULAR
# ---------------------------

# Intentamos interpretar las columnas del KPI histórico como fechas
parsed_cols = {}
for c in kpi_hist.columns:
    try:
        parsed_cols[c] = pd.to_datetime(c)
    except Exception:
        parsed_cols[c] = pd.NaT

# Seleccionamos columnas entre FECHA_INICIO y FECHA_FIN
selected_cols = [
    c for c, d in parsed_cols.items()
    if pd.notna(d) and (d >= FECHA_INICIO) and (d <= FECHA_FIN)
]

# Sub-KPI sólo con esos meses, manteniendo resto de filas (incluidas LGD, etc.)
kpi = kpi_hist[selected_cols].copy()

# ---------------------------
# LISTAS DE FILAS A RELLENAR
# ---------------------------

# Filas globales
main_rows = [
    "Trabajadores en alta inicio mes total",
    "Fijos",
    "Eventuales",
    "Altas fijos",
    "Altas eventuales",
    "Bajas fijos",
    "Bajas eventuales",
    "Trabajadores al final de mes",
    "Estudiantes en prácticas",
    "Trabajadores en alta inicio mes (hombre)",
    "Fijos (hombre)",
    "Eventuales (hombre)",
    "Altas fijos (hombre)",
    "Altas eventuales (hombre)",
    "Bajas fijos (hombre)",
    "Bajas eventuales (hombre)",
    "Trabajadores al final de mes (hombre)",
    "Trabajadores en alta inicio mes (mujer)",
    "Fijos (mujer)",
    "Eventuales (mujer)",
    "Altas fijos (mujer)",
    "Altas eventuales (mujer)",
    "Bajas fijos (mujer)",
    "Bajas eventuales (mujer)",
    "Trabajadores al final de mes (mujer)",
    "Coste salarial",
    "Coste seguridad social empresa",
    "Coste Total",
    "Coste medio personal",
    "Edad média",
    "Antiguedad média",
]

dept_rows = [
    "ADMINISTRACION Y FINANZAS",
    "ASISTENCIA Y SOPORTE",
    "CENTRALITA",
    "COMERCIAL",
    "CONSULTORIA ECONOMICA",
    "CONTABILIDAD",
    "COORDINACION DE PROYECTOS",
    "DESARROLLO Y TECNOLOGIA",
    "DIR. TECNOLOGIA, SISTEMAS E INNOVACION",
    "DIRECCIÓN GENERAL",
    "FORMACIÓN",
    "IMPLANTACIONES Y MIGRACIONES",
    "IMPRENTA",
    "INSPECCIÓN E INVENTARIOS",
    "LIMPIEZA",
    "RRHH",
    "SERVICIOS TRIBUTARIOS",
    "SISTEMAS",
    "SISTEMAS DE GESTIÓN",
    "Sº NOMINAS Y PORTAL DEL EMPLEADO",
]

deleg_rows = [
    "DELEGACIÓN BURGOS",
    "DELEGACIÓN CIUDAD REAL",
    "DELEGACIÓN CUENCA",
    "DELEGACIÓN DE MURCIA",
    "DELEGACIÓN GUADALAJARA",
    "DELEGACIÓN SALAMANCA",
    "DELEGACIÓN TOLEDO",
]

# ---------------------------
# CÁLCULO MES A MES
# ---------------------------

for col_label in selected_cols:
    # Fecha de inicio de mes según KPI histórico
    dt = parsed_cols[col_label]
    if pd.isna(dt):
        # Por si acaso alguna columna rara
        continue

    start_m = dt
    # fin de periodo: fin de mes o fecha de corte (01/12/2025), lo que ocurra antes
    end_m = min(start_m + pd.offsets.MonthEnd(0), FECHA_FIN)

    # Máscaras
    mask_start = active_mask(base, start_m)
    mask_end = active_mask(base, end_m)

    plantilla_start = base['es_plantilla'] & mask_start
    plantilla_end = base['es_plantilla'] & mask_end

    fijos_start = base['es_fijo'] & mask_start
    eventuales_start = base['es_eventual'] & mask_start

    # --- Globales ---
    if "Trabajadores en alta inicio mes total" in kpi.index:
        kpi.loc["Trabajadores en alta inicio mes total", col_label] = int(plantilla_start.sum())
    if "Fijos" in kpi.index:
        kpi.loc["Fijos", col_label] = int(fijos_start.sum())
    if "Eventuales" in kpi.index:
        kpi.loc["Eventuales", col_label] = int(eventuales_start.sum())

    altas_fijos = (base['es_fijo'] & between_period(start_m, base['fecha_ini'], FECHA_FIN)).sum()
    altas_eventuales = (base['es_eventual'] & between_period(start_m, base['fecha_ini'], FECHA_FIN)).sum()
    bajas_fijos = (base['es_fijo'] & between_period(start_m, base['fecha_fin'], FECHA_FIN)).sum()
    bajas_eventuales = (base['es_eventual'] & between_period(start_m, base['fecha_fin'], FECHA_FIN)).sum()

    if "Altas fijos" in kpi.index:
        kpi.loc["Altas fijos", col_label] = int(altas_fijos)
    if "Altas eventuales" in kpi.index:
        kpi.loc["Altas eventuales", col_label] = int(altas_eventuales)
    if "Bajas fijos" in kpi.index:
        kpi.loc["Bajas fijos", col_label] = int(bajas_fijos)
    if "Bajas eventuales" in kpi.index:
        kpi.loc["Bajas eventuales", col_label] = int(bajas_eventuales)

    if "Trabajadores al final de mes" in kpi.index:
        kpi.loc["Trabajadores al final de mes", col_label] = int(plantilla_end.sum())

    # Estudiantes en prácticas (becarios) al inicio de mes
    becarios_start = base['es_becario'] & mask_start
    if "Estudiantes en prácticas" in kpi.index:
        kpi.loc["Estudiantes en prácticas", col_label] = int(becarios_start.sum())

    # --- Hombres / Mujeres ---
    plantilla_h_start = plantilla_start & base['es_hombre']
    plantilla_m_start = plantilla_start & base['es_mujer']
    plantilla_h_end = plantilla_end & base['es_hombre']
    plantilla_m_end = plantilla_end & base['es_mujer']

    if "Trabajadores en alta inicio mes (hombre)" in kpi.index:
        kpi.loc["Trabajadores en alta inicio mes (hombre)", col_label] = int(plantilla_h_start.sum())
    if "Fijos (hombre)" in kpi.index:
        kpi.loc["Fijos (hombre)", col_label] = int((fijos_start & base['es_hombre']).sum())
    if "Eventuales (hombre)" in kpi.index:
        kpi.loc["Eventuales (hombre)", col_label] = int((eventuales_start & base['es_hombre']).sum())
    if "Trabajadores al final de mes (hombre)" in kpi.index:
        kpi.loc["Trabajadores al final de mes (hombre)", col_label] = int(plantilla_h_end.sum())

    if "Altas fijos (hombre)" in kpi.index:
        kpi.loc["Altas fijos (hombre)", col_label] = int(
            (base['es_fijo'] & base['es_hombre'] &
             between_period(start_m, base['fecha_ini'], FECHA_FIN)).sum()
        )
    if "Altas eventuales (hombre)" in kpi.index:
        kpi.loc["Altas eventuales (hombre)", col_label] = int(
            (base['es_eventual'] & base['es_hombre'] &
             between_period(start_m, base['fecha_ini'], FECHA_FIN)).sum()
        )
    if "Bajas fijos (hombre)" in kpi.index:
        kpi.loc["Bajas fijos (hombre)", col_label] = int(
            (base['es_fijo'] & base['es_hombre'] &
             between_period(start_m, base['fecha_fin'], FECHA_FIN)).sum()
        )
    if "Bajas eventuales (hombre)" in kpi.index:
        kpi.loc["Bajas eventuales (hombre)", col_label] = int(
            (base['es_eventual'] & base['es_hombre'] &
             between_period(start_m, base['fecha_fin'], FECHA_FIN)).sum()
        )

    if "Trabajadores en alta inicio mes (mujer)" in kpi.index:
        kpi.loc["Trabajadores en alta inicio mes (mujer)", col_label] = int(plantilla_m_start.sum())
    if "Fijos (mujer)" in kpi.index:
        kpi.loc["Fijos (mujer)", col_label] = int((fijos_start & base['es_mujer']).sum())
    if "Eventuales (mujer)" in kpi.index:
        kpi.loc["Eventuales (mujer)", col_label] = int((eventuales_start & base['es_mujer']).sum())
    if "Trabajadores al final de mes (mujer)" in kpi.index:
        kpi.loc["Trabajadores al final de mes (mujer)", col_label] = int(plantilla_m_end.sum())

    if "Altas fijos (mujer)" in kpi.index:
        kpi.loc["Altas fijos (mujer)", col_label] = int(
            (base['es_fijo'] & base['es_mujer'] &
             between_period(start_m, base['fecha_ini'], FECHA_FIN)).sum()
        )
    if "Altas eventuales (mujer)" in kpi.index:
        kpi.loc["Altas eventuales (mujer)", col_label] = int(
            (base['es_eventual'] & base['es_mujer'] &
             between_period(start_m, base['fecha_ini'], FECHA_FIN)).sum()
        )
    if "Bajas fijos (mujer)" in kpi.index:
        kpi.loc["Bajas fijos (mujer)", col_label] = int(
            (base['es_fijo'] & base['es_mujer'] &
             between_period(start_m, base['fecha_fin'], FECHA_FIN)).sum()
        )
    if "Bajas eventuales (mujer)" in kpi.index:
        kpi.loc["Bajas eventuales (mujer)", col_label] = int(
            (base['es_eventual'] & base['es_mujer'] &
             between_period(start_m, base['fecha_fin'], FECHA_FIN)).sum()
        )

    # --- Costes, edad, antigüedad (sobre plantilla activa a final de periodo) ---
    plantilla_cost = plantilla_end
    headcount_end = plantilla_cost.sum()

    total_retrib = base.loc[plantilla_cost, 'TOTAL RETRIBUCIÓN 2025'].sum()
    total_ss = base.loc[plantilla_cost, 'Seguridad Social empresa 2025'].sum()
    total_coste = base.loc[plantilla_cost, 'COSTE TOTAL 2025'].sum()

    if "Coste salarial" in kpi.index:
        kpi.loc["Coste salarial", col_label] = float(total_retrib)
    if "Coste seguridad social empresa" in kpi.index:
        kpi.loc["Coste seguridad social empresa", col_label] = float(total_ss)
    if "Coste Total" in kpi.index:
        kpi.loc["Coste Total", col_label] = float(total_coste)
    if "Coste medio personal" in kpi.index:
        kpi.loc["Coste medio personal", col_label] = (
            float(total_coste / headcount_end) if headcount_end > 0 else np.nan
        )

    subset = base.loc[plantilla_end].copy()
    subset['edad_anios'] = (end_m - subset['fecha_nac']).dt.days / 365.25
    subset['antig_anios'] = (end_m - subset['fecha_ini']).dt.days / 365.25

    if "Edad média" in kpi.index:
        kpi.loc["Edad média", col_label] = float(subset['edad_anios'].mean())
    if "Antiguedad média" in kpi.index:
        kpi.loc["Antiguedad média", col_label] = float(subset['antig_anios'].mean())

    # --- Departamentos y delegaciones ---
    for row in dept_rows:
        if row in kpi.index:
            kpi.loc[row, col_label] = int((plantilla_end & (base['DEP_KPI'] == row)).sum())

    for row in deleg_rows:
        if row in kpi.index:
            kpi.loc[row, col_label] = int((plantilla_end & (base['DELEG_KPI'] == row)).sum())

    # Fila TOTAL = suma de departamentos
    if "TOTAL" in kpi.index:
        kpi.loc["TOTAL", col_label] = float(kpi.loc[dept_rows, col_label].sum())

# ---------------------------
# GUARDAR RESULTADO
# ---------------------------

kpi.to_excel(SALIDA_KPI)
print(f"KPI recalculado guardado en: {SALIDA_KPI}")
