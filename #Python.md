# PYTHON COMPLETO

---

## ÍNDICE
### FUNDAMENTOS
- [1. Arquitectura, Ejecución](#1-arquitectura-ejecución)
  - [CPython](#1-arquitectura-ejecución)
  - [PyPy](#1-arquitectura-ejecución)
  - [Bytecode (.pyc)](#1-arquitectura-ejecución)
  - [GIL (Global Interpreter Lock)](#1-arquitectura-ejecución)
  - [Virtual Environments](#1-arquitectura-ejecución)
  - [Packaging (Wheel/SDist)](#1-arquitectura-ejecución)
- [2. Sintaxis, Tipos, Variables](#2-sintaxis-tipos-variables)
  - [Tipado Dinámico Fuerte](#2-sintaxis-tipos-variables)
  - [Mutabilidad](#2-sintaxis-tipos-variables)
  - [Type Hints](#2-sintaxis-tipos-variables)
  - [Walrus Operator `:=`](#2-sintaxis-tipos-variables)
  - [F-Strings](#2-sintaxis-tipos-variables)
- [3. Control de Flujo, Patrones](#3-control-de-flujo-patrones)
  - [Match-Case (3.10+)](#3-control-de-flujo-patrones)
  - [Comprensiones](#3-control-de-flujo-patrones)
  - [Generadores (yield)](#3-control-de-flujo-patrones)

### ESTRUCTURAS & FUNCIONAL
- [4. POO, Modelado de Dominio](#4-poo-modelado-de-dominio)
  - [Encapsulamiento](#4-poo-modelado-de-dominio)
  - [Herencia vs Composición](#4-poo-modelado-de-dominio)
  - [MRO](#4-poo-modelado-de-dominio)
  - [Dataclasses](#4-poo-modelado-de-dominio)
  - [`__slots__`](#4-poo-modelado-de-dominio)
  - [Protocolos](#4-poo-modelado-de-dominio)
- [5. Excepciones, Manejo de Errores](#5-excepciones-manejo-de-errores)
  - [EAFP vs LBYL](#5-excepciones-manejo-de-errores)
  - [`raise` from](#5-excepciones-manejo-de-errores)
  - [Custom Exceptions](#5-excepciones-manejo-de-errores)
- [6. Colecciones, Tipos Genéricos](#6-colecciones-tipos-genéricos)
  - [list/tuple/dict/set](#6-colecciones-tipos-genéricos)
  - [collections Module](#6-colecciones-tipos-genéricos)
  - [Typing Genéricos](#6-colecciones-tipos-genéricos)
  - [TypedDict / NamedTuple](#6-colecciones-tipos-genéricos)
- [7. Funcional, Iteradores, Generadores](#7-funcional-iteradores-generadores)
  - [`*args`/`**kwargs`](#7-funcional-iteradores-generadores)
  - [Iteradores / Generadores](#7-funcional-iteradores-generadores)
  - [itertools / functools](#7-funcional-iteradores-generadores)

### RENDIMIENTO & CONCURRENCIA
- [8. Concurrencia, Paralelismo](#8-concurrencia-paralelismo)
  - [Threading](#8-concurrencia-paralelismo)
  - [Multiprocessing](#8-concurrencia-paralelismo)
  - [AsyncIO / async/await](#8-concurrencia-paralelismo)
  - [GIL Implications](#8-concurrencia-paralelismo)
- [9. I/O, Archivos, Serialización](#9-io-archivos-serialización)
  - [`open()` / pathlib](#9-io-archivos-serialización)
  - [JSON / Pickle](#9-io-archivos-serialización)
  - [Compression](#9-io-archivos-serialización)
- [10. Gestión de Memoria, GC](#10-gestión-de-memoria-gc)
  - [Reference Counting](#10-gestión-de-memoria-gc)
  - [Generational GC](#10-gestión-de-memoria-gc)
  - [Memory Leaks](#10-gestión-de-memoria-gc)
  - [`weakref`](#10-gestión-de-memoria-gc)

### METAPROGRAMACIÓN & HERRAMIENTAS
- [11. Metaprogramación, Decoradores, Reflexión](#11-metaprogramación-decoradores-reflexión)
  - [Decoradores](#11-metaprogramación-decoradores-reflexión)
  - [Metaclasses](#11-metaprogramación-decoradores-reflexión)
  - [`inspect` / `eval`/`exec`](#11-metaprogramación-decoradores-reflexión)
  - [Descriptors](#11-metaprogramación-decoradores-reflexión)
- [12. Testing](#12-testing)
  - [unittest / pytest](#12-testing)
  - [Fixtures / Mocking](#12-testing)
  - [Type Checking / Linting](#12-testing)
  - [Coverage / Property-Based](#12-testing)
- [13. Ecosistema, Build, Dependencias](#13-ecosistema-build-dependencias)
  - [pip / pyproject.toml](#13-ecosistema-build-dependencias)
  - [poetry / pdm / uv](#13-ecosistema-build-dependencias)
  - [Virtual Environments](#13-ecosistema-build-dependencias)
  - [Build Backends / Publishing](#13-ecosistema-build-dependencias)

### PRODUCCIÓN & SEGURIDAD
- [14. Web, APIs](#14-web-apis)
  - [requests / httpx](#14-web-apis)
  - [FastAPI / Flask / Django](#14-web-apis)
  - [WebSockets / Background Tasks](#14-web-apis)
- [15. Seguridad](#15-seguridad)
  - [OWASP Python Top 10](#15-seguridad)
  - [SQL / Command Injection](#15-seguridad)
  - [Secrets / Cryptography](#15-seguridad)
  - [Pickle Security / Dependency Scanning](#15-seguridad)
- [16. Python Moderno (3.10-3.13+)](#16-python-moderno-310-313)
  - [Structural Pattern Matching](#16-python-moderno-310-313)
  - [Type Hints Avanzados](#16-python-moderno-310-313)
  - [ExceptionGroup / tomllib](#16-python-moderno-310-313)
  - [Performance Improvements](#16-python-moderno-310-313)

### OPERACIONES & COMUNICACIÓN
- [17. Comunicación](#17-comunicación)
  - [Trade-off Framework](#17-comunicación)
  - [Preguntas Trampa](#17-comunicación)
  - [System Design / Debugging](#17-comunicación)
  - [Behavioral (STAR) / Code Review](#17-comunicación)
- [18. Checklist](#18-checklist)
  - [Preparación Técnica](#18-checklist)
  - [Despliegue](#18-checklist)

---

## 1. ARQUITECTURA, EJECUCIÓN
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **CPython** | Implementación de referencia en C. Interpreta bytecode + GC. Tiene GIL (Global Interpreter Lock). | Default en la mayoría de entornos. Limita paralelismo CPU-bound en threads. |
| **PyPy** | Implementación con JIT. 3-10x más rápido en código puro Python. Compatible con CPython (casi). | Ideal para scripts largos/CPU-bound. Cuidado con extensiones C. |
| **Bytecode (.pyc)** | Código intermedio compilado desde `.py`. Ejecutado por la VM de Python. | Se cachea en `__pycache__/`. No es portable entre versiones mayores. |
| **GIL (Global Interpreter Lock)** | Mutex que protege acceso a objetos Python, impidiendo ejecución paralela de bytecode en múltiples threads. | No afecta I/O-bound (libera GIL en syscalls). Para CPU-bound: usa `multiprocessing` o C extensions. |
| **Interpretado vs Compilado** | Python compila a bytecode automáticamente, luego interpreta. No hay paso de compilación explícito (usualmente). | `python -m compileall .` precompila para despliegue. |
| **Virtual Environments** | Aislamiento de dependencias por proyecto. Evita conflictos de versiones. | `python -m venv .venv` → `source .venv/bin/activate` |
| **Entry Point** | Ejecución directa de script o módulo. `if __name__ == "__main__":` protege ejecución como módulo. | `python main.py` vs `python -m package.module` |
| **Packaging (Wheel/SDist)** | Wheel (`.whl`): binario precompilado, instalación rápida. SDist (`.tar.gz`): fuente, requiere build. | `pip wheel .` para distribuir. `pyproject.toml` estándar moderno. |

---

## 2. SINTAXIS, TIPOS, VARIABLES
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Tipado Dinámico Fuerte** | Tipo se asigna en runtime, pero no hay coerción implícita peligrosa. | `"5" + 2` → `TypeError`. No como JS. |
| **Mutabilidad** | Inmutables: `int`, `float`, `str`, `tuple`, `frozenset`. Mutables: `list`, `dict`, `set`, `bytearray`. | Cuidado con defaults mutables: `def f(x=[]):` → usa `None` y crea dentro. |
| **None** | Único valor nulo. No es `False` ni `0`. Comparar con `is None`. | `if value is None:` (no `== None`). |
| **Asignación Múltiple & Unpacking** | Asignar/desempaquetar en una línea. Soporta `*` para resto. | `a, b = b, a` (swap). `first, *rest, last = seq` |
| **Type Hints (3.5+)** | Anotaciones estáticas opcionales. Mejoran legibilidad y permiten `mypy`/`pyright`. | `def process(user: User) -> list[str]: ...` |
| **`final`, `Literal`, `TypeAlias` (3.8-3.10+)** | `@final` evita herencia. `Literal` restringe valores. `TypeAlias` define alias tipados. | `Status = Literal["active", "inactive"]` `def set_status(s: Status): ...` |
| **Walrus Operator `:=` (3.8+)** | Asignación en expresión. Útil en condiciones/bucles. | `while (line := f.readline()): process(line)` |
| **F-Strings (3.6+)** | Interpolación eficiente y legible. Soporta expresiones, formato, debug (`=`). | `f"User: {user.name!r} (id={user.id:04d})"` `f"{value=}"` → `value=42` |

---

## 3. CONTROL DE FLUJO, PATRONES
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Condicional** | `if`/`elif`/`else`. Evaluación perezosa de `and`/`or`. Truthiness: vacíos = `False`. | `if users and users[0].active:` (corto-circuito seguro). |
| **Match-Case (3.10+)** | Pattern matching estructural. Soporta tipos, valores, guards, desestructuración. | `match event: case {"type": "login", "user": str(name)} if name: log(name) case _: handle_unknown()` |
| **Bucles** | `for` sobre iterables (preferido). `while` por condición. `else` en bucles (ejecuta si no hay `break`). | `for item in collection: ... else: print("Completado sin breaks")` |
| **Comprensiones** | Sintaxis concisa para crear listas/dicts/sets. Más rápido que bucles + append. | `[x*2 for x in nums if x > 0]` `{k: v.upper() for k,v in data.items()}` |
| **Generadores (yield)** | Función que retorna iterador perezoso. Ahorra memoria en datasets grandes. | `def chunks(seq, n): for i in range(0, len(seq), n): yield seq[i:i+n]` |
| **Break/Continue/Return/Else** | `break` sale, `continue` salta. `else` en bucles: ejecuta si no hubo `break`. | `for item in items: if found(item): break else: raise NotFoundError()` |

---

## 4. POO, MODELADO DE DOMINIO
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Clase/Objeto** | Todo es objeto. Clases definidas con `class`. Constructor: `__init__`. | `class Agent: def __init__(self, id: str): self.id = id` |
| **Atributos de Instancia vs Clase** | Instancia: `self.x`. Clase: compartido entre instancias. Cuidado con mutables en clase. | `class Cache: store = {}` → compartido. Mejor: `self.store = {}` en `__init__`. |
| **Encapsulamiento (Convención)** | No hay `private` real. Convención: `_protegido`, `__name_mangled`. `@property` para getters/setters. | `@property def status(self) -> str: return self._status` |
| **Herencia vs Composición** | Herencia múltiple permitida (MRO C3). Composición preferida para flexibilidad. | Preferir `Agent` tiene `Weapon` sobre `Agent extends Weapon`. |
| **MRO (Method Resolution Order)** | Orden de búsqueda de métodos en herencia múltiple. Algoritmo C3 linearization. | `ClassName.__mro__` para inspeccionar. `super()` sigue MRO. |
| **`@abstractmethod` (ABC)** | Define métodos obligatorios en subclases. `ABC` como base para clases abstractas. | `from abc import ABC, abstractmethod` `class Op(ABC): @abstractmethod def run(self): ...` |
| **Dataclasses (3.7+)** | Decorador para clases de datos. Genera `__init__`, `__repr__`, `__eq__`, etc. Soporta `frozen`, `slots`. | `@dataclass(frozen=True) class User: name: str; age: int` |
| **`__slots__`** | Declara atributos permitidos. Ahorra memoria, evita `__dict__`. Útil en miles de instancias. | `class Point: __slots__ = ("x", "y")` |
| **Protocolos (Structural Subtyping, 3.8+)** | Tipado estructural (duck typing estático). `Protocol` define interfaz sin herencia. | `class SupportsClose(Protocol): def close(self) -> None: ...` |
| **`__enter__`/`__exit__` (Context Managers)** | Protocolo para `with`. Garantiza cleanup. | `class DBConn: def __enter__(self): return self; def __exit__(self, *e): self.close()` |

---

## 5. EXCEPCIONES, MANEJO DE ERRORES
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Jerarquía** | `BaseException` → `Exception` → específicas. `KeyboardInterrupt`/`SystemExit` no capturar salvo necesidad. | `try: risky() except ValueError as e: log(e)` |
| **EAFP vs LBYL** | "Easier to Ask Forgiveness than Permission" (try/except) vs "Look Before You Leap" (if checks). Python prefiere EAFP. | `try: value = data[key] except KeyError: handle_missing()` |
| **`raise` from** | Encadenamiento de excepciones. Preserva traceback original. | `raise NewError("context") from original_error` |
| **`else`/`finally` en try** | `else`: ejecuta si no hubo excepción. `finally`: siempre ejecuta (cleanup). | `try: f=open(x) except: ... else: process(f) finally: f and f.close()` |
| **Custom Exceptions** | Heredar de `Exception`. Incluir contexto. Usar jerarquía propia para granularidad. | `class OpsError(Exception): pass` `class TimeoutError(OpsError): ...` |
| **Warning System** | `warnings.warn()` para deprecaciones/no-críticos. Configurables con filtros. | `warnings.warn("Legacy API", DeprecationWarning, stacklevel=2)` |

---

## 6. COLECCIONES, TIPOS GENÉRICOS
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **list** | Ordenada, mutable, permite duplicados. Indexación O(1), búsqueda O(n). | `items = [1,2,3]` `items.append(4)` `items[0]` |
| **tuple** | Ordenada, inmutable. Usar para datos heterogéneos/retornos múltiples. | `coords: tuple[float, float] = (10.5, 20.3)` |
| **dict** | Pares clave-valor. Claves deben ser hashables. O(1) promedio acceso. Orden preservado (3.7+). | `user = {"name": "Ana", "age": 30}` `user.get("email", "unknown")` |
| **set/frozenset** | Único, no ordenado. `set` mutable, `frozenset` inmutable (hashable). Operaciones de conjunto. | `valid = {"active", "pending"}` `if status in valid: ...` |
| **collections Module** | Estructuras especializadas: `deque` (colas eficientes), `defaultdict`, `Counter`, `OrderedDict`, `ChainMap`. | `from collections import deque` `q = deque(maxlen=100)` |
| **Typing Genéricos** | `list[str]`, `dict[str, int]`, `Optional[T]`, `Union[A,B]`, `Callable[[int], str]`, `TypeVar`. | `def process(items: list[str]) -> dict[str, int]: ...` |
| **`TypedDict` (3.8+)** | Diccionarios con esquema de tipos estático. Útil para APIs/JSON. | `class User(TypedDict): name: str; age: int` |
| **`NamedTuple`** | Tupla con nombres de campos. Inmutable, ligera, tipable. | `from typing import NamedTuple` `class Point(NamedTuple): x: float; y: float` |

---

## 7. FUNCIONAL, ITERADORES, GENERADORES
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Funciones de Primera Clase** | Funciones son objetos: asignables, pasables, retornables. | `ops = {"add": lambda a,b: a+b}` `result = ops["add"](2,3)` |
| **`*args`/`**kwargs`** | Argumentos posicionales/keyword variables. Útil para wrappers/decoradores. | `def wrapper(*args, **kwargs): return target(*args, **kwargs)` |
| **`lambda`** | Función anónima de una expresión. Limitada, usar con moderación. | `sorted(users, key=lambda u: u.name)` |
| **`map`/`filter`/`reduce`** | Funcionales clásicas. Preferir comprensiones/generadores por legibilidad. | `from functools import reduce` `total = reduce(lambda a,b: a+b, nums, 0)` |
| **Iteradores** | Objetos con `__iter__` y `__next__`. Consumen elementos uno a uno. | `it = iter([1,2,3])` `next(it)` → `1` |
| **Generadores (`yield`)** | Función que pausa/resume estado. Iterador perezoso, eficiente en memoria. | `def read_large(file): for line in file: yield line.strip()` |
| **`itertools`** | Herramientas para iteradores: `chain`, `groupby`, `islice`, `product`, `cycle`. | `from itertools import islice` `first_10 = islice(data, 10)` |
| **`functools`** | Decoradores/utilidades: `lru_cache`, `partial`, `singledispatch`, `wraps`. | `@lru_cache(maxsize=128) def expensive(n): ...` |

---

## 8. CONCURRENCIA, PARALELISMO
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Threading (`threading`)** | Hilos OS. GIL limita paralelismo CPU-bound. Ideal para I/O-bound. | `from threading import Thread` `Thread(target=task).start()` |
| **`concurrent.futures`** | API unificada para threads/processes. `ThreadPoolExecutor`, `ProcessPoolExecutor`. | `with ThreadPoolExecutor() as pool: results = pool.map(fetch, urls)` |
| **Multiprocessing (`multiprocessing`)** | Procesos separados (sin GIL). Para CPU-bound. Comunicación vía `Queue`, `Pipe`, `Manager`. | `from multiprocessing import Pool` `with Pool() as p: p.map(cpu_task, data)` |
| **AsyncIO (3.4+)** | Concurrencia basada en event loop + `async`/`await`. Ideal para I/O masivo (red, DB). | `async def fetch(url): async with httpx.AsyncClient() as c: return await c.get(url)` |
| **`async`/`await`** | Define corrutinas. `await` pausa hasta que awaitable se resuelve. No bloquea event loop. | `results = await asyncio.gather(fetch(u) for u in urls)` |
| **GIL Implications** | GIL libera en I/O syscalls y extensiones C. CPU-bound en threads: sin paralelismo real. | Para CPU-bound: `multiprocessing` o mover lógica a C/Rust (via `pyo3`, `cffi`). |
| **`asyncio` Utilities** | `gather`, `wait`, `as_completed`, `Timeout`, `Semaphore`, `Lock`, `Queue`. | `async with asyncio.Timeout(5): await slow_op()` |
| **Thread/Process Safety** | `queue.Queue` (thread-safe), `multiprocessing.Queue` (process-safe). Evitar estado compartido sin locks. | `from threading import Lock` `lock = Lock(); with lock: shared += 1` |

---

## 9. I/O, ARCHIVOS, SERIALIZACIÓN
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **`open()` & Context Managers** | Apertura de archivos. Siempre usar `with` para cierre automático. Modos: `r`, `w`, `a`, `b`, `x`. | `with open("data.txt", "r", encoding="utf-8") as f: content = f.read()` |
| **`pathlib` (3.4+)** | API orientada a objetos para rutas. Más legible que `os.path`. | `from pathlib import Path` `files = Path("/data").glob("*.json")` |
| **JSON** | Serialización estándar. `json.load(s)`, `json.dump(obj, f)`. Cuidado con tipos no nativos. | `json.dumps(obj, default=str, ensure_ascii=False)` para fechas/Unicode. |
| **Pickle** | Serialización binaria de objetos Python. **Inseguro**: no deserializar datos no confiables. | Solo para cache interno/confiable. Alternativas: `msgpack`, `protobuf`, `orjson`. |
| **CSV/Excel** | `csv` module nativo. `pandas` para Excel/CSV avanzado. | `import csv` `with open("data.csv") as f: reader = csv.DictReader(f)` |
| **Compression** | `gzip`, `bz2`, `lzma`, `zipfile`. Integración con `open` vía `gzip.open()`. | `import gzip` `with gzip.open("data.json.gz", "rt") as f: data = json.load(f)` |
| **`io` Module** | Streams en memoria (`BytesIO`, `StringIO`). Útil para testing/transformaciones. | `from io import StringIO` `buf = StringIO(); buf.write("data"); buf.getvalue()` |

---

## 10. GESTIÓN DE MEMORIA, GC
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Reference Counting** | Contador de referencias por objeto. Liberación inmediata al llegar a 0. | Principal mecanismo. Ciclos de referencia requieren GC adicional. |
| **Generational GC** | Recolector cíclico para objetos con referencias circulares. Tres generaciones (0,1,2). | `import gc; gc.collect()` forzado (raro). `gc.disable()` en hot paths críticos. |
| **Memory Leaks Comunes** | Caches sin límite, referencias circulares con `__del__`, globals mutables, callbacks no removidos. | Usar `weakref` para caches. Perfil con `tracemalloc`, `memory_profiler`. |
| **`__slots__` & Memoria** | Evita `__dict__` por instancia. Ahorra ~40-50% memoria en clases con muchos atributos. | `class Point: __slots__ = ("x", "y")` |
| **`sys.getsizeof()`** | Tamaño en bytes de objeto (shallow). No incluye referencias internas. | `import sys; sys.getsizeof([1]*1000)` → tamaño de lista, no de elementos. |
| **Profiling Memoria** | `tracemalloc` (nativo), `memory_profiler` (decorador), `objgraph` (referencias). | `import tracemalloc; tracemalloc.start(); ...; tracemalloc.get_traced_memory()` |
| **`weakref`** | Referencias débiles: no incrementan contador. Útil para caches, observers, evitar ciclos. | `import weakref` `cache = weakref.WeakValueDictionary()` |

---

## 11. METAPROGRAMACIÓN, DECORADORES, REFLEXIÓN
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Decoradores** | Funciones que modifican/envuelven otras. Sintaxis `@decorator`. Usar `functools.wraps`. | `def log(func): @wraps(func) def wrapper(*a,**k): log(a,k); return func(*a,**k); return wrapper` |
| **Decoradores con Parámetros** | Decorador que retorna decorador. Tres niveles de anidación. | `def retry(max_attempts=3): def decorator(func): ...; return decorator` |
| **Clases como Decoradores** | Implementar `__call__`. Útil para estado mutable entre llamadas. | `class Timer: def __call__(self, func): ...` |
| **`__getattr__`/`__setattr__`** | Interceptan acceso a atributos. Poderoso pero peligroso (rendimiento, recursión). | Usar para proxies, lazy loading. Siempre llamar `super()` o manipular `__dict__` con cuidado. |
| **Metaclasses** | Clases de clases. Controlan creación de clases. Avanzado, raro. | `class Meta(type): ...` `class Base(metaclass=Meta): ...` |
| **`inspect` Module** | Introspección: firmas, fuentes, jerarquía, atributos. | `import inspect; sig = inspect.signature(func); params = sig.parameters` |
| **`eval`/`exec`/`compile`** | Ejecución dinámica de código. **Peligroso** con input externo. | Solo con código confiable. Preferir `ast.literal_eval` para datos. |
| **Descriptors** | Objetos con `__get__`/`__set__`/`__delete__`. Base de `@property`, `@classmethod`. | `class Validated: def __set__(self, obj, value): if not self.validate(value): raise ...` |

---

## 12. TESTING
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **`unittest` (stdlib)** | Framework xUnit nativo. Clases, asserts, fixtures. Verboso pero estándar. | `class TestOps(unittest.TestCase): def test_valid(self): self.assertEqual(op(), expected)` |
| **`pytest` (recomendado)** | Sintaxis simple, fixtures potentes, plugins, reporting. Compatible con `unittest`. | `def test_process(mock_db): assert process(user) == expected` |
| **Fixtures & Parametrización** | Setup/teardown reutilizable. Ejecutar tests con múltiples inputs. | `@pytest.fixture def db(): ...` `@pytest.mark.parametrize("inp,out", [(1,2), (3,4)])` |
| **Mocking (`unittest.mock`)** | Simular dependencias: `Mock`, `MagicMock`, `patch`. | `@patch("module.api_call") def test(mock_api): mock_api.return_value = 200; ...` |
| **Type Checking (`mypy`/`pyright`)** | Verificación estática de tipos. Configuración en `pyproject.toml`. | `mypy --strict src/` Integrar en CI. |
| **Linting & Formatting** | `ruff` (rápido, unifica flake8/isort), `black` (formato), `pylint` (análisis profundo). | `ruff check . && black .` en pre-commit/CI. |
| **Coverage (`coverage.py`)** | Métrica de líneas/ramas ejecutadas. Integración con `pytest-cov`. | `pytest --cov=src --cov-report=html` → `htmlcov/index.html` |
| **Property-Based Testing (`hypothesis`)** | Generar casos aleatorios para invariantes. Encuentra edge cases automáticamente. | `from hypothesis import given, strategies as st` `@given(st.integers()) def test_inverse(x): assert f(f(x)) == x` |

---

## 13. ECOSISTEMA, BUILD, DEPENDENCIAS
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **`pip`** | Gestor de paquetes oficial. Instala desde PyPI, VCS, archivos locales. | `pip install -r requirements.txt` `pip install -e .` (editable) |
| **`pyproject.toml` (PEP 517/518)** | Estándar moderno para configuración de build, dependencias, herramientas. | `[project] dependencies = ["httpx>=0.24"]` `[tool.pytest.ini_options] addopts = "-v"` |
| **`poetry`/`pdm`/`uv`** | Gestores modernos: lockfiles, entornos virtuales, publishing. `uv` (Rust) es ultra-rápido. | `poetry add httpx` `poetry install` `poetry publish` |
| **Virtual Environments** | Aislamiento por proyecto. `venv` (stdlib), `virtualenv` (avanzado). | `python -m venv .venv` → `source .venv/bin/activate` |
| **Requirements Files** | `requirements.txt` (pip), `pyproject.toml` (poetry/pdm). Pinning: `==`, `>=`, `~=`. | `httpx==0.24.1` (exacto) vs `httpx~=0.24` (compatible) |
| **Editable Installs** | `pip install -e .` vincula código fuente. Ideal para desarrollo. | Cambios en código se reflejan sin reinstalar. |
| **Build Backends** | `setuptools` (tradicional), `flit`, `hatchling`, `poetry-core`. Definidos en `pyproject.toml`. | `[build-system] requires = ["hatchling"] build-backend = "hatchling.build"` |
| **Packaging & Publishing** | `build` module para crear wheel/sdist. `twine` para subir a PyPI/TestPyPI. | `python -m build` `twine upload dist/*` |

---

## 14. WEB, APIs
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **`requests`** | Cliente HTTP sincrónico. Simple, robusto. No async. | `import requests` `r = requests.get(url, timeout=5); r.json()` |
| **`httpx`** | Cliente HTTP sincrónico + asincrónico. API compatible con `requests`. | `async with httpx.AsyncClient() as c: r = await c.get(url)` |
| **FastAPI (3.8+)** | Framework moderno para APIs. Type hints → validación automática + docs OpenAPI. | `@app.get("/users/{id}") async def get_user(id: int) -> User: ...` |
| **Flask** | Microframework minimalista. Flexible, gran ecosistema. | `@app.route("/health") def health(): return {"status": "ok"}` |
| **Django** | Framework "baterías incluidas". ORM, admin, auth, forms. Monolítico pero robusto. | `class User(models.Model): name = models.CharField(max_length=100)` |
| **WebSockets** | Comunicación bidireccional en tiempo real. `websockets` lib, o integrado en FastAPI/Starlette. | `@app.websocket("/ws") async def ws(websocket: WebSocket): await websocket.accept(); ...` |
| **Background Tasks** | `Celery` (Redis/RabbitMQ), `RQ`, `Dramatiq`, o `asyncio.create_task` para simple. | `@app.post("/process") async def trigger(): asyncio.create_task(long_task()); return {"accepted": True}` |
| **API Security** | Validar input (Pydantic), rate limiting, CORS, auth (JWT/OAuth2), HTTPS. | `from fastapi.security import HTTPBearer` `security = HTTPBearer()` |

---

## 15. SEGURIDAD
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **OWASP Python Top 10** | Injection (SQL, OS, LDAP), Broken Auth, Sensitive Data, XXE, Deserialization (pickle), Misconfig, XSS, Logging, Supply Chain. | Validar input, usar parametrized queries, evitar `eval`/`pickle` con datos externos. |
| **SQL Injection** | Usar ORM (SQLAlchemy, Django) o parámetros posicionales/nombrados. Nunca concatenar. | `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))` |
| **Command Injection** | Nunca pasar input a `os.system`, `subprocess` sin sanitizar. Usar `shlex.quote` o listas. | `subprocess.run(["ls", user_path])` (lista) vs `f"ls {user_path}"` (peligroso). |
| **Secrets Management** | Nunca hardcodear. Usar variables de entorno, `python-dotenv`, Vault, AWS SM. | `import os; API_KEY = os.environ["API_KEY"]` `from dotenv import load_dotenv; load_dotenv()` |
| **Cryptography** | `cryptography` library (recomendada). `hashlib` para hashing. `secrets` para tokens. | `import secrets; token = secrets.token_urlsafe(32)` `hashlib.sha256(data.encode()).hexdigest()` |
| **Pickle Security** | **Nunca** deserializar datos no confiables. Alternativas: `json`, `msgpack`, `protobuf`. | Si es obligatorio: restringir clases permitidas con `pickle.Unpickler` + `find_class` override. |
| **Dependency Scanning** | `pip-audit`, `safety`, `dependabot`, `renovate`. SBOM con `cyclonedx-bom`. | `pip-audit -r requirements.txt` en CI. Rechazar CVEs críticos. |
| **Logging Seguro** | No loggear secrets, PII, stack traces en prod. Usar structured logging (`structlog`). | `logger.info("User action", extra={"user_id": user_id, "action": "login"})` |

---

## 16. PYTHON MODERNO (3.10-3.13+)
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Structural Pattern Matching (3.10+)** | `match`/`case` con patrones avanzados: valores, tipos, guards, desestructuración. | `match event: case {"type": "error", "code": int(code)} if code > 500: alert(code) case _: pass` |
| **Type Hints Avanzados** | `TypeGuard` (3.10), `Self` (3.11), `Unpack` (3.11), `Never`, `LiteralString`. | `def is_user(obj) -> TypeGuard[User]: return isinstance(obj, User)` |
| **`ExceptionGroup` & `except*` (3.11+)** | Manejo de múltiples excepciones concurrentes (asyncio, threads). | `try: ... except* ValueError as eg: handle(eg.exceptions)` |
| **`tomllib` (3.11+)** | Lectura nativa de TOML (stdlib). Reemplaza `toml`/`tomli` externos. | `import tomllib; with open("pyproject.toml", "rb") as f: config = tomllib.load(f)` |
| **`typing.Self` (3.11+)** | Referencia al tipo de la clase actual. Útil para métodos fluidos/herencia. | `class Builder: def set_name(self, name: str) -> Self: ...; return self` |
| **F-Strings Mejorados (3.12+)** | Soporte para expresiones complejas, debugging avanzado, formato más flexible. | `f"{user.name=!r:20} {user.age=}"` → `user.name='Ana'      user.age=30` |
| **Performance Improvements (3.11-3.13)** | Interpreter más rápido (10-60%), mejor error messages, `with` múltiple, `asyncio` optimizado. | Actualizar a 3.11+ para ganancias gratuitas. Perfil antes de optimizar manualmente. |
| **JEPs & Futuro** | Seguir [peps.python.org](https://peps.python.org). Features en desarrollo: JIT experimental, mejor async, typing. | Probar features nuevas en staging con `--enable-feature` si aplica. |

---

## 17. COMUNICACIÓN
| Concepto | Definición Directa | Nota |
|----------|-------------------|----------------------|
| **Trade-off Framework** | Siempre: Pros, Contras, Cuándo usar, Cuándo evitar. Contexto > regla absoluta. | "`list` para acceso aleatorio, `deque` para colas. En microservicios con alta concurrencia I/O, `asyncio` > `threading`." |
| **Preguntas Trampa Comunes** | GIL, mutabilidad de defaults, `is` vs `==`, iteradores vs generadores, EAFP vs LBYL, `*args` order, MRO, `__slots__`, pickling risks. | Preparar explicación concisa + ejemplo de bug real + cómo lo detectaste/arreglaste. |
| **System Design Básico** | Escalabilidad horizontal, caching (Redis), colas (RabbitMQ/Kafka), idempotencia, circuit breaker, observability. | Dibujar flujo: Client → LB → API (FastAPI) → Cache → DB → Worker (Celery) → Monitor (Prometheus). |
| **Debugging Workflow** | Reproducir → Logs → `pdb`/`breakpoint()` → Profiler (`cProfile`, `py-spy`) → Fix → Test → Deploy → Monitor. | No adivinar. Datos > intuición. Usar `logging` estructurado desde el inicio. |
| **Behavioral (STAR)** | Situación, Tarea, Acción, Resultado. Enfocar ownership, aprendizaje, impacto medible (métricas). | "Migré API sincrónica a `asyncio` + `httpx`, reduciendo latencia p95 de 800ms a 120ms. Documenté patrón y traineé equipo." |
| **Code Review Focus** | Legibilidad, testabilidad, seguridad, rendimiento, mantenibilidad. Preguntar, no imponer. | "¿Maneja edge cases? ¿Tiene tests? ¿Es seguro con input externo? ¿Se puede entender en 6 meses?" |
| **Comunicación Técnica** | Estructura lógica: problema → opciones → decisión → trade-offs. Humildad técnica: "no sé, pero lo investigo". | Adaptar nivel al interlocutor (junior vs staff vs PM). Evitar jerga innecesaria. |

---

## 18. CHECKLIST
### Preparación Técnica
1. **Repaso Rápido:** Sintaxis, colecciones, OOP, excepciones, iterators/generators, typing, asyncio basics.
2. **Práctica Código:** Resolver problemas con comprensiones, generadores, `async`/`await`, decorators, pattern matching.
3. **Entrevista Técnica:** Explicar trade-offs con contexto, dibujar arquitectura, escribir código limpio (sin IDE si es necesario).
4. **Debugging Demo:** Usar `pdb`, leer traceback, analizar con `py-spy`/`tracemalloc`, proponer fix medible.
5. **Modern Python:** Dominar 3.10+ features: pattern matching, type hints avanzados, `ExceptionGroup`, performance improvements.
6. **Frameworks:** FastAPI/Flask basics, SQLAlchemy pitfalls (N+1, sessions), testing strategy (pytest + mocking).
7. **Seguridad:** Validar input (Pydantic), manejo secrets, OWASP Top 10, evitar `pickle`/`eval` con datos externos.
8. **Deploy:** Docker multi-stage, virtualenv en contenedor, CI/CD con `ruff`/`mypy`/`pytest`, observability (logs/metrics/traces).

### Despliegue
1. **Entorno:** `python -m venv .venv` → `source .venv/bin/activate` → `pip install -r requirements.txt` / `poetry install`.
2. **Linting/Formatting:** `ruff check . && ruff format .` / `black . && isort .` en pre-commit/CI.
3. **Testing:** `pytest --cov=src --cov-report=xml` → subir cobertura a Codecov/Sonar.
4. **Type Checking:** `mypy --config-file pyproject.toml src/` → fallo en CI si errores.
5. **Build:** `python -m build` → genera `dist/*.whl` y `dist/*.tar.gz`.
6. **Docker:** Imagen slim (`python:3.12-slim`), usuario non-root, instalar deps en capa cacheable. | `FROM python:3.12-slim` `WORKDIR /app` `COPY pyproject.toml .` `RUN pip install --no-cache-dir .` `COPY src/ ./src/` `USER nobody` `CMD ["python", "-m", "src.main"]` |
7. **Tuning Runtime:** Variables de entorno para config, `PYTHONUNBUFFERED=1` en Docker, `asyncio` event loop policies si aplica.
8. **Observability:** Logging estructurado (`structlog`), métricas con `prometheus_client`, tracing con OpenTelemetry.
9. **Hardening:** No ejecutar como root, escanear dependencias (`pip-audit`), deshabilitar endpoints debug en prod, rotar secrets.
10. **Post-Mortem:** Documentar incidentes, root cause, acciones correctivas, lecciones aprendidas. Compartir conocimiento.

---
