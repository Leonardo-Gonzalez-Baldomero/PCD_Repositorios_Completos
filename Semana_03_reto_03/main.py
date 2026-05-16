import sys
import math

def es_numero_valido(valor):
    """Verifica que el valor sea un número válido y no INF, NAN, etc."""
    try:
        num = float(valor)
        # Rechazar infinitos, NaN y valores no finitos
        if math.isinf(num) or math.isnan(num):
            return False
        return True
    except ValueError:
        return False

def main():
    # Diccionario para agrupar por producto
    productos = {}
    
    primera_linea = True
    
    # Leer todas las lineas
    for linea in sys.stdin:
        linea = linea.strip()
        
        # Saltar encabezado
        if primera_linea:
            primera_linea = False
            continue
        
        # Saltar lineas vacias
        if not linea:
            continue
        
        # Parsear linea
        partes = linea.split(',')
        if len(partes) != 4:
            continue  # Ignorar lineas invalidas
        
        fecha = partes[0]
        producto = partes[1]
        cantidad_str = partes[2]
        precio_str = partes[3]
        
        # Validar que cantidad y precio sean números válidos (no INF, NAN, palabras)
        if not (es_numero_valido(cantidad_str) and es_numero_valido(precio_str)):
            continue  # Ignorar si contienen INF, NAN, palabras, etc.
        
        # Convertir (ahora seguro de que son números válidos)
        cantidad = int(float(cantidad_str))  # Convertir a float primero por si viene como "5.0"
        precio = float(precio_str)
        
        # Crear entrada si no existe
        if producto not in productos:
            productos[producto] = {
                "unidades": 0,
                "ingreso": 0.0
            }
        
        # Acumular
        productos[producto]["unidades"] += cantidad
        productos[producto]["ingreso"] += cantidad * precio
    
    # Calcular precio promedio
    for prod in productos:
        unidades = productos[prod]["unidades"]
        ingreso = productos[prod]["ingreso"]
        productos[prod]["promedio"] = ingreso / unidades if unidades > 0 else 0
    
    # Ordenar por ingreso descendente, luego alfabéticamente por producto
    productos_ordenados = sorted(
        productos.items(),
        key=lambda x: (-x[1]["ingreso"], x[0])
    )
    
    # Imprimir salida
    print("producto,unidades_vendidas,ingreso_total,precio_promedio")
    for nombre, datos in productos_ordenados:
        print(f"{nombre},{datos['unidades']},{datos['ingreso']:.2f},{datos['promedio']:.2f}")

if __name__ == "__main__":
    main()