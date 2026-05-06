import sys #Recuerda utilizamos "sys" para interactuar con stdin y stdout.

def fahrenheit_a_celsius(f): #FNCIÓN PARA CONVERTIR DE FARENHEIT A CELSIUS.
    return (f - 32) * 5 / 9 #Operación para la conversión.

def clasificar(celsius): #FUNCIÓN PARA CLASIFICAR EL TIPO DE TEMPERATURA.
    if celsius < 0:
        return "Congelante"
    elif celsius <= 15:
        return "Frio"
    elif celsius <= 25:
        return "Templado"
    elif celsius <= 35:
        return "Calido"
    else:
        return "Extremo" #Simples categorías para cada nivel de temperatura.

def main(): #FUNCIÓN PRINCIPAL. 
    primera_linea = True #Leer y descartar encabezado de entrada.
    
    print("ciudad,temperatura_celsius,clasificacion") #Imprimir el encabezado de la salida.
    
    for linea in sys.stdin:
        linea = linea.strip() #Recuerda, borra caracteres iniciales y finales con .strip()".
        
        if primera_linea:
            primera_linea = False #Código para saltarse las líneas del encabezado.
            continue
        
        #Saltar lineas vacías.
        if not linea:
            continue
        
        #Dividir los 3 campos.
        partes = linea.split(',') #Lee la línea completa y la divide con comas.
        if len(partes) != 3: #"len()"" devuelve el número de elementos del "objeto"/"cadena".
            continue  #Ignorar las líneas invalidas.
        
        ciudad = partes[0]
        temp_str = partes[1]
        unidad = partes[2].strip().upper() #Converit las minúsculas en mayúsculas y seguimos eliminanto caracteres iniciales y finales.
        
        #Validar si es un "C" ó un "F".
        if unidad not in ['C', 'F']:
            continue  # Ignorar
        
        #Si pertenece a "C" ó a "F" convertir la temperatura.
        try:
            temp = float(temp_str) #Lo leído lo pasamos a flotante y guardamos en nueva variable para usar.
        except ValueError:
            continue  # Ignorar si no es número.
        
        #Utilizamos la función para convertir a celsius.
        if unidad == 'F':
            celsius = fahrenheit_a_celsius(temp) #Si es F aplicamos la función de conversión.
        else:
            celsius = temp #Si no, guardamos normal la temperatura.
        
        #Clasificamos los datos y los imprimimos.
        clasificacion = clasificar(celsius)
        print(f"{ciudad},{celsius:.1f},{clasificacion}") #Escribe los grados con un decimal.

if __name__ == "__main__":
    main()
