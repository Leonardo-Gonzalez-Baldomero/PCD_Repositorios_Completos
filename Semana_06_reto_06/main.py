import re  
from typing import Dict, List  
from datetime import datetime  
import sys  

DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']  
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']  


def validar_producto(codigo: str) -> Dict:  
    resultado = {"valido": False, "categoria": None, "numero": None, "pais": None}  
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
    patron = r'^ENV-(\d{4})-(\d{2})-(\d{2})-(\d{6})$'  
    match = re.match(patron, codigo)  
    if match:  
        anio, mes, dia, secuencial = match.groups()  
        if 2020 <= int(anio) <= 2030 and 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31:  
            try:  
                datetime(int(anio), int(mes), int(dia))  
                resultado.update({  
                    "valido": True,  
                    "fecha": f"{anio}-{mes}-{dia}",  
                    "secuencial": secuencial  
                })  
            except ValueError:  
                pass  
    return resultado  


def validar_empleado(codigo: str) -> Dict:  
    resultado = {"valido": False, "departamento": None, "numero": None}  
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
    elif re.match(r'^[A-Za-z]{3,4}-', codigo):
        resultado["tipo"] = "producto"
        resultado["detalles"] = validar_producto(codigo)

    if resultado["detalles"] and resultado["detalles"].get("valido"):
        resultado["valido"] = True

    return resultado


def procesar_lote(codigos: List[str]) -> None:
    """
    Procesa los códigos y escribe CSV a stdout.
    Formato: código, tipo, válido, campo1, campo2, campo3
    """
    # Escribir encabezados
    sys.stdout.write("codigo,tipo,valido,detalle_1,detalle_2,detalle_3\n")

    for cod in codigos:
        res = validar_codigo(cod)

        codigo = res["codigo"]
        tipo = res["tipo"]
        valido = "SI" if res["valido"] else "NO"

        if res["valido"] and res["detalles"]:
            detalles = res["detalles"]
            # Extraer los campos relevantes según el tipo
            if tipo == "producto":
                d1 = detalles.get("categoria", "")
                d2 = detalles.get("numero", "")
                d3 = detalles.get("pais", "")
            elif tipo == "envio":
                d1 = detalles.get("fecha", "")
                d2 = detalles.get("secuencial", "")
                d3 = ""
            elif tipo == "empleado":
                d1 = detalles.get("departamento", "")
                d2 = detalles.get("numero", "")
                d3 = ""
            elif tipo == "factura":
                d1 = detalles.get("serie", "")
                d2 = detalles.get("numero", "")
                d3 = ""
            else:
                d1 = d2 = d3 = ""
        else:
            d1 = d2 = d3 = ""

        sys.stdout.write(f"{codigo},{tipo},{valido},{d1},{d2},{d3}\n")


# --- DATOS DE PRUEBA ---

CODIGOS_PRUEBA = [
    "TEC-0001-MX", "ALI-9999-US", "ROB-1234-CA", "tec-0001-MX",
    "TEC-001-MX", "TECH-0001-MX",
    "ENV-2024-03-15-001234", "ENV-2025-12-01-999999",
    "ENV-2019-03-15-001234", "ENV-2024-13-15-001234",
    "ENV-2024-03-32-001234",
    "EMP-VEN-1234", "EMP-TEC-9999", "EMP-ADM-1000",
    "EMP-VEN-0123", "EMP-XXX-1234", "EMP-VEN-123",
    "FAC-A-123456", "FAC-E-000001", "FAC-B-999999",
    "FAC-F-123456", "FAC-A-12345", "FAC-a-123456",
    "XXX-1234", "RANDOM-CODE"
]

# --- EJECUCIÓN ---

if __name__ == "__main__":
    procesar_lote(CODIGOS_PRUEBA)