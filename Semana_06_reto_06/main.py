import re
from typing import Dict, List
from datetime import datetime

# --- CONFIGURACIÓN ---
DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']

# --- PARTE 1: Funciones de validación individual ---

def validar_producto(codigo: str) -> Dict:
    resultado = {"valido": False, "categoria": None, "numero": None, "pais": None}
    # Formato: 3 letras mayúsculas - 4 dígitos - 2 letras país mayúsculas
    patron = r'^([A-Z]{3})-(\d{4})-([A-Z]{2})$'
    match = re.match(patron, codigo)
    
    if match:
        resultado.update({
            "valido": True,
            "categoria": match.group(1),
            "numero": match.group(2),
            "pais": match.group(3)
        })
    return resultado

def validar_envio(codigo: str) -> Dict:
    resultado = {"valido": False, "fecha": None, "secuencial": None}
    # Formato: ENV-YYYY-MM-DD-NNNNNN
    patron = r'^ENV-(\d{4})-(\d{2})-(\d{2})-(\d{6})$'
    match = re.match(patron, codigo)
    
    if match:
        anio, mes, dia, secuencial = match.groups()
        # Validar rangos básicos y lógica de fecha real
        if 2020 <= int(anio) <= 2030 and 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31:
            try:
                datetime(int(anio), int(mes), int(dia))
                resultado.update({
                    "valido": True,
                    "fecha": f"{anio}-{mes}-{dia}",
                    "secuencial": secuencial
                })
            except ValueError:
                pass # Fecha inexistente (ej. 31 de febrero)
    return resultado

def validar_empleado(codigo: str) -> Dict:
    resultado = {"valido": False, "departamento": None, "numero": None}
    # Formato: EMP-XXX-NNNN
    patron = r'^EMP-([A-Z]{3})-([1-9]\d{3})$'
    match = re.match(patron, codigo)
    
    if match:
        depto = match.group(1)
        if depto in DEPARTAMENTOS_VALIDOS:
            resultado.update({
                "valido": True,
                "departamento": depto,
                "numero": match.group(2)
            })
    return resultado

def validar_factura(codigo: str) -> Dict:
    resultado = {"valido": False, "serie": None, "numero": None}
    # Formato: FAC-S-NNNNNN
    patron = r'^FAC-([A-Z])-(\d{6})$'
    match = re.match(patron, codigo)
    
    if match:
        serie = match.group(1)
        if serie in SERIES_VALIDAS:
            resultado.update({
                "valido": True,
                "serie": serie,
                "numero": match.group(2)
            })
    return resultado

# --- PARTE 2: Validador universal ---

def validar_codigo(codigo: str) -> Dict:
    resultado = {"codigo": codigo, "tipo": "desconocido", "valido": False, "detalles": {}}
    
    if codigo.startswith("ENV-"):
        resultado["tipo"] = "envio"
        resultado["detalles"] = validar_envio(codigo)
    elif codigo.startswith("EMP-"):
        resultado["tipo"] = "empleado"
        resultado["detalles"] = validar_empleado(codigo)
    elif codigo.startswith("FAC-"):
        resultado["tipo"] = "factura"
        resultado["detalles"] = validar_factura(codigo)
    elif re.match(r'^[A-Za-z]{3,4}-', codigo): # Intento de matchear producto
        resultado["tipo"] = "producto"
        resultado["detalles"] = validar_producto(codigo)
    
    if resultado["detalles"] and resultado["detalles"].get("valido"):
        resultado["valido"] = True
        
    return resultado

# --- PARTE 3: Procesamiento por lotes ---

def procesar_lote(codigos: List[str]) -> Dict:
    resultado = {
        "total": 0, "validos": 0, "invalidos": 0,
        "por_tipo": {
            "producto": {"total": 0, "validos": 0},
            "envio": {"total": 0, "validos": 0},
            "empleado": {"total": 0, "validos": 0},
            "factura": {"total": 0, "validos": 0},
            "desconocido": {"total": 0, "validos": 0}
        },
        "detalle": []
    }

    for cod in codigos:
        res = validar_codigo(cod)
        tipo = res["tipo"]
        
        resultado["total"] += 1
        resultado["por_tipo"][tipo]["total"] += 1
        
        if res["valido"]:
            resultado["validos"] += 1
            resultado["por_tipo"][tipo]["validos"] += 1
        else:
            resultado["invalidos"] += 1
        
        resultado["detalle"].append(res)
        
    return resultado

# --- UTILIDADES DE SALIDA ---

def mostrar_resultado(resultado: Dict) -> None:
    estado = "✓" if resultado["valido"] else "✗"
    print(f"{estado} {resultado['codigo']:<30} | Tipo: {resultado['tipo']:<12}")
    if resultado["valido"] and resultado["detalles"]:
        detalles = ", ".join(f"{k}: {v}" for k, v in resultado["detalles"].items() if k != "valido" and v)
        print(f"   └── {detalles}")

def mostrar_reporte(reporte: Dict) -> None:
    if reporte['total'] == 0:
        print("No hay datos para procesar.")
        return
        
    print("=" * 60)
    print("                 REPORTE DE VALIDACIÓN")
    print("=" * 60)
    print(f"\nTotal procesados: {reporte['total']}")
    print(f"Válidos: {reporte['validos']} ({reporte['validos']/reporte['total']*100:.1f}%)")
    print(f"Inválidos: {reporte['invalidos']} ({reporte['invalidos']/reporte['total']*100:.1f}%)")

    print("\nDesglose por tipo:")
    print("-" * 40)
    for tipo, stats in reporte["por_tipo"].items():
        if stats["total"] > 0:
            tasa = (stats["validos"] / stats["total"] * 100)
            print(f"  {tipo.capitalize():<12}: {stats['validos']:>3}/{stats['total']:<3} ({tasa:.0f}% válidos)")
    print("\n" + "=" * 60)

# --- DATOS DE PRUEBA ---

CODIGOS_PRUEBA = [
    "TEC-0001-MX", "ALI-9999-US", "ROB-1234-CA", "tec-0001-MX", "TEC-001-MX", "TECH-0001-MX",
    "ENV-2024-03-15-001234", "ENV-2025-12-01-999999", "ENV-2019-03-15-001234", "ENV-2024-13-15-001234", "ENV-2024-03-32-001234",
    "EMP-VEN-1234", "EMP-TEC-9999", "EMP-ADM-1000", "EMP-VEN-0123", "EMP-XXX-1234", "EMP-VEN-123",
    "FAC-A-123456", "FAC-E-000001", "FAC-B-999999", "FAC-F-123456", "FAC-A-12345", "FAC-a-123456",
    "XXX-1234", "RANDOM-CODE"
]

# --- EJECUCIÓN ---

if __name__ == "__main__":
    print("PRUEBA DE VALIDADOR UNIVERSAL")
    print("=" * 50)
    for codigo in CODIGOS_PRUEBA[:15]:
        resultado = validar_codigo(codigo)
        mostrar_resultado(resultado)

    print("\nPRUEBA DE PROCESAMIENTO POR LOTES")
    reporte = procesar_lote(CODIGOS_PRUEBA)
    mostrar_reporte(reporte)