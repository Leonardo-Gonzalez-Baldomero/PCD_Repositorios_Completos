import sys #PROGRAMA YA MODIFICADO PARA SU UTILIZACIÓN CON ARCHIVOS.

def limpiar_valor(valor): #FUNCIÓN PARA LIMPIAR UN VALOR INDIVIDUAL.
    caracteres_validos = '0123456789.-' #Variable de caractéres permitidos, si no son esos no los cuenta.
    valor_str = str(valor).strip()  #El valor leído lo pasa a cadena y después elimina los caractéres iniciales y finales de la cadena leída.
    resultado = '' #Variable para almacenar los datos que se vayan leyendo.
    for ch in valor_str: #For desde "0" hasta "ch" de la cadena "valor_str"
        if ch in caracteres_validos: #Si "ch" pertenece a un cv hace un incremento y concatena.
            resultado += ch
    return resultado #Devolder todo el valor individual con los cv permitidos

def procesar_linea(linea): #FUNCIÓN PARA PROCESAR TODA UNA LÍNEA.
    linea = linea.strip() #Eiminar caracteres iniciales y finales de la cadena.
    if not linea: #Si no hay nada devolver 0.
        return 0

    partes = [p for p in linea.split(',')] #Divide la cadena o lista leída con una coma.
    total = 0 #Inicializar el total
    for p in partes: #For usando la función de "limpiar_valor" a cada valor de toda la cadena.
        limpio = limpiar_valor(p)
        if limpio == '' or limpio == '-' or limpio == '.': #Si es positivo, negativo o decimal continuar.
            continue
        try:
            numero = int(float(limpio))  #Pasar la cadena a flotantes y luego truncar decimales con "int()"
            total += numero #Sumar todos los elementos de la cadena.
        except ValueError: #Si no se puede truncar entonces es "0".
            pass
    return total

def main():
    for linea in sys.stdin: #Variable "línea" para leer cada línea del archivo y guardarla.
        resultado = procesar_linea(linea) #Aplica todas las funciones a cada línea.
        print(resultado) #Imprime el resultado de cada línea

if __name__ == "__main__":
    main()