# RETO SEMANA 01 - CALCULADORA

## -Pasos para ejecutar el programa:
### Desde un Archivo

### Windows (PowerShell)
Get-Content entrada.txt | python main.py

### Windows (CMD)
type entrada.txt | python main.py

### Linux/Mac
python main.py < entrada.txt

### ó también
cat entrada.txt | python main.py

## -Ejemplo para probar el programa:
-Entrada (archivo entrada.txt):
1,2,3
10

1.9,2.1,3.7
1a2,3b,4
-5,10,3
5 , 10 , 15  

-Salida esperada:
6
10
0
6
19
8
30

Autor: González Baldomero Leonardo