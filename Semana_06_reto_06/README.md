# Validador de Códigos RegEx

Herramienta que valida y clasifica códigos corporativos (productos, envíos, empleados y facturas) mediante expresiones regulares.

## Requisitos

*   Python 3.8 o superior

## Instalación

1. **Clonar el repositorio:**
```bash
git clone [ https://github.com/tu-usuario/validador_regex ]
cd validador_regex
```

2. **Crear ambiente virtual:**
```bash
python -m venv .venv
```

3. **Activar ambiente virtual:**
*   **Windows:** `.venv\Scripts\activate`
*   **Linux/Mac:** `source .venv/bin/activate`

4. **Instalar dependencias:**
*(Nota: Este programa utiliza únicamente la librería estándar de Python, por lo que este paso es preventivo).*
```bash
pip install -r requirements.txt
```

5. **Uso:**
```bash
python main.py
```
**Ejemplo de ejecución:**
El programa procesará la lista interna de `CODIGOS_PRUEBA` y generará un reporte estadístico en la terminal detallando cuántos códigos fueron válidos por cada categoría.

6. **Formato de Salida:**

El reporte generado en consola contiene la siguiente estructura para cada código procesado:

| Campo | Descripción |
| :--- | :--- |
| **Estado (✓/✗)** | Indica si el código cumple con el patrón RegEx definido. |
| **Código** | El identificador original analizado. |
| **Tipo** | Categoría detectada (producto/envio/empleado/factura/desconocido). |
| **Detalles** | Información extraída (ej: serie, país, fecha o departamento). |

**Resumen Estadístico:**
Al finalizar, se muestra un desglose porcentual de la calidad del lote:
*   Total de registros procesados.
*   Porcentaje de éxito (Válidos vs. Inválidos).
*   Tasa de acierto específica por tipo de documento.

**Autor:** González Baldomero Leonardo - Mayo 2026