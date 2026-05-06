# RETO SEMANA 02 - TEMPERATURAS
Repositorio para la segunda tarea de la semana 2 en Programación para la Ciencia de Datos.

## Descripción
Este programa lee un archivo de datos desde la entrada estándar convirtiendo las temperaturas Farenheit a Celsius si es necesario e imprime la ciudad en la que está, la temperatura en Celsius y una clasificación dependiendo de la temperatura que se haya calculado.

¿Cómo Ejecutar el Programa?
Desde un Archivo
## Windows (PowerShell)
Get-Content entrada.txt | python main.py

## Windows (CMD)
type entrada.txt | python main.py

## Linux/Mac
python main.py < entrada.txt (ESTA EJECUCIÓN NO ME FUNCIONA PERO PUEDE SERVIR PARA OTROS DISPOSITIVOS)

## ó también
cat entrada.txt | python main.py (PERSONALMENTE UTILIZO ESTE PARA EJECUTARLO EN MI COMPUTADORA)

## Guardar la Salida
## Guardar resultado en archivo
python main.py < entrada.txt > salida.txt

## Ver y guardar al mismo tiempo
python main.py < entrada.txt | tee salida.txt

## Entrada Manual (para pruebas)
python main.py

## Escribe lineas manualmente
## Presiona Ctrl+D (Linux/Mac) o Ctrl+Z (Windows) para terminar

# Autor
Por: González Baldomero Leonardo