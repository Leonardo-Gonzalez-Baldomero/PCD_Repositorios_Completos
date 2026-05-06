# RETO SEMANA 03 - VENTAS
Repositorio para la segunda tarea de la semana 3 en Programación para la Ciencia de Datos.

## Descripción
Este programa lee un archivo de datos desde la entrada estándar de una cantidad de productos diferentes, cuántos hay, el precio de cada uno y otros datos más que no son tan relevantes realizando la sumatoria de todos los productos que se hayan comprado y la cantidad total de estos mostrando cuánto de cada producto y el producto mismo para un comprobante o algo parecido.

## ¿Cómo Ejecutar el Programa desde un Archivo?
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
cat entrada.txt | python main.py > mi_salida.txt (PERSONALMENTE UTILIZO ESTE PARA CARGAR EL ARCHIVO CON MI PROGRAMA Y GUARDARLO EN OTRO ARCHIVO)

## Entrada Manual (para pruebas)
python main.py

Escribe lineas manualmente
Presiona Ctrl+D (Linux/Mac) o Ctrl+Z (Windows) para terminar

# Autor
Por: González Baldomero Leonardo