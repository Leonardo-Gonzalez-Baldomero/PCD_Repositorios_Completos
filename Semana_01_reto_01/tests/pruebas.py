import sys #PROGRAMA SIN MODIFICAR PARA ARCHIVOS, SOLO SIRVE PARA UN VALOR QUE YO AGREGUÉ MANUALMENTE

def limpiar_valor(valor):
    """
    Limpia un valor individual:
    - Quita espacios
    - Elimina caracteres no validos
    - Retorna el numero limpio como string
    """
    # Tu codigo aqui
    #QUITAR ESPACIOS DEL PRINCIPIO, FINAL Y DE CADA ELEMENTO
valores = ['  5C', ' 2s', '-3    ',  'B   ', '  -2.3', '2.1    ']
valores_limpios = [v.strip() for v in valores]  # ['1C', '2s', '-3', 'B', '-2.3', '2.1']
print(valores_limpios)

#FUNCIÓN PARA LIMPIAR LOS DATOS Y QUITAR LAS LETRAS Y SIGNOS RAROS
def limpiar(texto):
    caracteres_validos = '0123456789.-'
    resultado = ''
    for char in str(texto):
        if char in caracteres_validos:
            resultado += char
    return resultado
           
#LIMPIAR LOS VALORES LIMPIOS Y DEJAR SOLO LOS NUMEROS
datoslimpios = [limpiar(v) for v in valores_limpios]
print(datoslimpios) #['1', '2', '-3', '', '-23', '2.1']
pass

def procesar_linea(linea):
    """
    Procesa una linea completa:
    - Separa por comas
    - Limpia cada valor
    - Trunca a entero
    - Suma todos
    - Retorna el resultado
    """
    # Tu codigo aqui
    #CONVERTIR DE STRING A ENTERO Y LUEGO TRUNCARLOS
def convertir_a_entero(lista):
    """Convierte texto a entero, truncando decimales."""
    if not lista:  # Si esta vacio
        return 0
    try:
        numeros = str(lista)
        numero = float(numeros)  # Primero a float
        return int(numero)     # Luego truncar a int
    except ValueError:
        return 0  # Si no se puede convertir, es 0

# APLICAR A TODOS LOS ELEMENTOS
resultados = [convertir_a_entero(t) for t in datoslimpios]
print(resultados)

#SUMAR LOS VALORES
def sumar_valores(valores):
    total = sum(resultados)
    return total

print("Suma:", sumar_valores(resultados))
pass

def main():
    """
    Lee de stdin linea por linea
    Procesa cada linea
    Imprime el resultado
    """
    for linea in sys.stdin:
        resultado = procesar_linea(linea)
        print(resultado)

if __name__ == "__main__":
    main()