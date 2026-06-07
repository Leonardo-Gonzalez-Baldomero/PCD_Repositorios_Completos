import re
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict
import json

# ==========================================
# PARTE 1: Parsers de Logs
# ==========================================

# Patrón para log HTTP - usa re.VERBOSE para legibilidad y grupos nombrados
PATRON_HTTP = re.compile(r'''
    ^(?P<ip>[\d.]+)\s               # IP del cliente
    -\s-\s                          # Identificadores fijos
    \[(?P<timestamp>.*?)\]\s        # Fecha y hora entre corchetes
    "(?P<method>\w+)\s              # Método HTTP (GET, POST, etc.)
    (?P<path>.*?)\s                 # Ruta o recurso solicitado
    (?P<protocolo>HTTP\/[\d.]+)"\s  # Protocolo HTTP
    (?P<status>\d{3})\s             # Código de estado HTTP (200, 404, etc.)
    (?P<bytes>\d+)\s                # Tamaño en bytes
    "(?P<referer>.*?)"\s            # Referente
    "(?P<user_agent>.*?)"$          # Navegador / Cliente
''', re.VERBOSE)

def parse_http_log(linea: str) -> Optional[Dict]:
    """Parsea una línea de log HTTP."""
    match = PATRON_HTTP.match(linea)
    if match:
        datos = match.groupdict()
        datos['status'] = int(datos['status'])
        datos['bytes'] = int(datos['bytes'])
        return datos
    return None


# Patrón para log de errores
PATRON_ERROR = re.compile(r'''
    ^\[(?P<timestamp>.*?)\]\s                       # Fecha y hora entre corchetes
    (?P<level>INFO|WARNING|ERROR|CRITICAL|DEBUG)\s  # Nivel del log
    (?P<module>[\w.]+)\s-\s                         # Módulo que generó el error
    (?P<error_type>\w+):\s                          # Tipo de error lanzado
    (?P<message>.*)$                                # Mensaje detallado
''', re.VERBOSE)

def parse_error_log(linea: str) -> Optional[Dict]:
    """Parsea una línea de log de errores."""
    match = PATRON_ERROR.match(linea)
    return match.groupdict() if match else None


# Patrón para log de autenticación utilizando Lookbehinds para extraer valores tras '='
PATRON_AUTH = re.compile(r'''
    ^\[AUTH\]\s(?P<timestamp>[\d-]+\s[\d:]+)\s\|\s
    (?<=user=)(?P<user>[^\s|]+)\s\|\s
    (?<=action=)(?P<action>[^\s|]+)\s\|\s
    (?<=status=)(?P<status>[^\s|]+)\s\|\s
    (?<=ip=)(?P<ip>[^\s|]+)
    (?:\s\|\s(?P<extra>.*))?$                       # Captura opcional de session o attempts
''', re.VERBOSE)

def parse_auth_log(linea: str) -> Optional[Dict]:
    """Parsea una línea de log de autenticación."""
    match = PATRON_AUTH.match(linea)
    if match:
        datos = match.groupdict()
        extra_dict = {}
        if datos['extra']:
            # Extraemos la información residual en un diccionario estructurado
            llave, valor = datos['extra'].split('=')
            extra_dict[llave.strip()] = valor.strip()
        datos['extra'] = extra_dict
        return datos
    return None


# Patrón para log de base de datos (Soporta QUERY y SLOW_QUERY)
PATRON_DB = re.compile(r'''
    ^\[DB-(?P<timestamp>.*?)\]\s
    (?P<query_type>QUERY|SLOW_QUERY)\s
    (?:\((?P<t_slow>[\d.]+)s\)|executed\sin\s(?P<t_query>[\d.]+)s):\s
    (?P<query>.*)$
''', re.VERBOSE)

def parse_db_log(linea: str) -> Optional[Dict]:
    """Parsea una línea de log de base de datos."""
    match = PATRON_DB.match(linea)
    if match:
        datos = match.groupdict()
        # Consolidamos el tiempo de ejecución de manera limpia
        tiempo_str = datos.pop('t_slow') or datos.pop('t_query')
        datos['execution_time'] = float(tiempo_str) if tiempo_str else 0.0
        return datos
    return None


# ==========================================
# PARTE 2: Analizador de Seguridad
# ==========================================

def detectar_ataques_fuerza_bruta(logs_auth: List[Dict]) -> List[Dict]:
    """Detecta IPs con más de 3 intentos fallidos (FAILED) de login."""
    conteo_fallas = Counter()
    for log in logs_auth:
        if log['status'] == 'FAILED':
            conteo_fallas[log['ip']] += 1
    return [{'ip': ip, 'intentos': intentos} for ip, intentos in conteo_fallas.items() if intentos > 3]


# Patrones de SQL Injection requeridos por la rúbrica
PATRONES_SQL_INJECTION = [
    r"(?i)\bOR\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+",  # OR 1=1
    r"(?i)\bUNION\b.*\bSELECT\b",                       # UNION SELECT
    r"--",                                               # Comentarios SQL
    r"(?i)\bDROP\b\s+\bTABLE\b",                        # DROP TABLE
    r"(?i)\bDELETE\b\s+\bFROM\b.*\bWHERE\b\s+1\s*=\s*1", # DELETE WHERE 1=1
]

def detectar_sql_injection(logs_db: List[Dict]) -> List[Dict]:
    """Detecta posibles intentos de SQL injection en las queries de la BD."""
    alertas = []
    for log in logs_db:
        for patron in PATRONES_SQL_INJECTION:
            if re.search(patron, log['query']):
                alertas.append(log)
                break
    return alertas


def detectar_path_traversal(logs_http: List[Dict]) -> List[Dict]:
    """Detecta intentos de path traversal en rutas de acceso HTTP."""
    patron = r"\.\.\/|\.\.\\|%2e%2e%2f"
    alertas = []
    for log in logs_http:
        if re.search(patron, log['path']):
            alertas.append(log)
    return alertas


def detectar_errores_criticos(logs_error: List[Dict]) -> List[Dict]:
    """Filtra errores de nivel ERROR o CRITICAL ordenados por timestamp."""
    errores = [log for log in logs_error if log['level'] in ('ERROR', 'CRITICAL')]
    return sorted(errores, key=lambda x: x['timestamp'])


# ==========================================
# PARTE 3: Generador de Reportes
# ==========================================

def clasificar_linea(linea: str) -> str:
    """Clasifica una línea de log por su tipo identificador inicial."""
    if linea.startswith('['):
        if linea.startswith('[AUTH]'):
            return 'auth'
        elif linea.startswith('[DB-'):
            return 'db'
        else:
            return 'error'
    elif re.match(r'^\d', linea):
        return 'http'
    return 'desconocido'


def generar_reporte(logs: str) -> Dict:
    """Genera un reporte completo analizando todos los logs."""
    lineas = logs.strip().split('\n')
    
    listas_por_tipo = {'http': [], 'error': [], 'auth': [], 'db': []}
    conteo_tipos = Counter()
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
            
        tipo = clasificar_linea(linea)
        conteo_tipos[tipo] += 1
        
        if tipo == 'http':
            res = parse_http_log(linea)
            if res: listas_por_tipo['http'].append(res)
        elif tipo == 'error':
            res = parse_error_log(linea)
            if res: listas_por_tipo['error'].append(res)
        elif tipo == 'auth':
            res = parse_auth_log(linea)
            if res: listas_por_tipo['auth'].append(res)
        elif tipo == 'db':
            res = parse_db_log(linea)
            if res: listas_por_tipo['db'].append(res)

    # Estadísticas HTTP
    total_requests = len(listas_por_tipo['http'])
    por_status = Counter()
    rutas = Counter()
    ips = Counter()
    for log in listas_por_tipo['http']:
        familia_status = f"{str(log['status'])[0]}xx"
        por_status[familia_status] += 1
        rutas[log['path'].split('?')[0]] += 1
        ips[log['ip']] += 1
        
    # Estadísticas de Errores
    por_nivel = Counter(log['level'] for log in listas_por_tipo['error'])
    por_modulo = Counter(log['module'] for log in listas_por_tipo['error'])
    
    # Rendimiento
    tiempos = [log['execution_time'] for log in listas_por_tipo['db']]
    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0
    queries_lentos = [log for log in listas_por_tipo['db'] if log['query_type'] == 'SLOW_QUERY']

    return {
        "resumen": {
            "total_lineas": len(lineas),
            "por_tipo": dict(conteo_tipos)
        },
        "http": {
            "total_requests": total_requests,
            "por_status": dict(por_status),
            "top_rutas": rutas.most_common(5),
            "top_ips": ips.most_common(5)
        },
        "errores": {
            "total": len(listas_por_tipo['error']),
            "por_nivel": dict(por_nivel),
            "por_modulo": dict(por_modulo)
        },
        "seguridad": {
            "alertas_fuerza_bruta": detectar_ataques_fuerza_bruta(listas_por_tipo['auth']),
            "alertas_sql_injection": detectar_sql_injection(listas_por_tipo['db']),
            "alertas_path_traversal": detectar_path_traversal(listas_por_tipo['http'])
        },
        "rendimiento": {
            "queries_lentos": queries_lentos,
            "tiempo_promedio_queries": tiempo_promedio
        }
    }


# ==========================================
# BONUS (Funcionalidades Extra Opcionales)
# ==========================================

def exportar_reporte_json(reporte: Dict, archivo: str) -> None:
    """Exporta el reporte generado a un archivo JSON físico."""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)


def analisis_temporal(logs_http: List[Dict]) -> Dict:
    """Analiza distribución de requests HTTP agrupados por hora."""
    horas = Counter()
    for log in logs_http:
        # Extrae la hora del formato '15/Mar/2024:10:23:45' -> '10'
        match = re.search(r':(\d{2}):', log['timestamp'])
        if match:
            horas[match.group(1)] += 1
    return dict(horas)


def detectar_bots(logs_http: List[Dict]) -> List[Dict]:
    """Detecta requests HTTP provenientes de herramientas automáticas o bots."""
    patron_bots = r"(?i)curl|wget|python|scrapy|sqlmap|postman"
    return [log for log in logs_http if re.search(patron_bots, log['user_agent'])]


# ==========================================
# Funciones de Visualización Obligatorias
# ==========================================

def mostrar_reporte(reporte: Dict) -> None:
    """Muestra el reporte de forma legible."""
    print("=" * 70)
    print("                    REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 70)
    
    print("\n📊 RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de líneas procesadas: {reporte['resumen']['total_lineas']}")
    print("Por tipo:")
    for tipo, count in reporte['resumen']['por_tipo'].items():
        print(f"  • {tipo.upper()}: {count}")
    
    if 'http' in reporte:
        print("\n🌐 LOGS HTTP")
        print("-" * 40)
        print(f"Total requests: {reporte['http']['total_requests']}")
        print("Por código de estado:")
        for status, count in sorted(reporte['http']['por_status'].items()):
            print(f"  • {status}: {count}")
        print("Top 5 rutas más solicitadas:")
        for ruta, count in reporte['http'].get('top_rutas', []):
            print(f"  • {ruta}: {count} requests")
    
    if 'errores' in reporte:
        print("\n❌ ERRORES")
        print("-" * 40)
        print(f"Total errores: {reporte['errores']['total']}")
        print("Por nivel:")
        for nivel, count in reporte['errores']['por_nivel'].items():
            print(f"  • {nivel}: {count}")
    
    if 'seguridad' in reporte:
        print("\n🔒 ALERTAS DE SEGURIDAD")
        print("-" * 40)
        
        fb = reporte['seguridad'].get('alertas_fuerza_bruta', [])
        if fb:
            print(f"⚠️  Posibles ataques de fuerza bruta: {len(fb)}")
            for alerta in fb:
                print(f"     IP: {alerta['ip']} - {alerta['intentos']} intentos fallidos")
        
        sql = reporte['seguridad'].get('alertas_sql_injection', [])
        if sql:
            print(f"⚠️  Posibles SQL Injection: {len(sql)}")
            for alerta in sql:
                print(f"     Query: {alerta['query'][:60]}...")
        
        pt = reporte['seguridad'].get('alertas_path_traversal', [])
        if pt:
            print(f"⚠️  Posibles Path Traversal: {len(pt)}")
            for alerta in pt:
                print(f"     Ruta: {alerta['path']}")
    
    if 'rendimiento' in reporte:
        print("\n⏱️  RENDIMIENTO")
        print("-" * 40)
        print(f"Queries lentos detectados: {len(reporte['rendimiento'].get('queries_lentos', []))}")
        if 'tiempo_promedio_queries' in reporte['rendimiento']:
            print(f"Tiempo promedio de queries: {reporte['rendimiento']['tiempo_promedio_queries']:.3f}s")
    
    print("\n" + "=" * 70)


# ==========================================
# Datos de Prueba y Ejecución Principal
# ==========================================

LOGS_PRUEBA = """
192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0 (Windows NT 10.0)"
192.168.1.101 - - [15/Mar/2024:10:23:46 -0600] "POST /api/login HTTP/1.1" 200 89 "-" "curl/7.68.0"
192.168.1.102 - - [15/Mar/2024:10:23:47 -0600] "GET /admin/../../../etc/passwd HTTP/1.1" 403 0 "-" "sqlmap/1.0"
[2024-03-15 10:24:00] INFO app.startup - Application started successfully on port 8080
[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused to host db.server.com:5432
[2024-03-15 10:25:15] WARNING app.cache - CacheWarning: Redis connection timeout, using fallback
[2024-03-15 10:26:00] ERROR app.auth - AuthenticationError: Invalid token for user admin@empresa.com
[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz
[AUTH] 2024-03-15 10:31:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=1
[AUTH] 2024-03-15 10:31:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=2
[AUTH] 2024-03-15 10:32:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=3
[AUTH] 2024-03-15 10:32:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=4
[AUTH] 2024-03-15 10:33:00 | user=otro@empresa.com | action=LOGOUT | status=SUCCESS | ip=10.0.0.10 | session=def456uvw
[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users WHERE email = 'admin@empresa.com'
[DB-2024-03-15 10:35:25] QUERY executed in 0.012s: SELECT id, name FROM products WHERE active = 1
[DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders o JOIN products p ON o.product_id = p.id JOIN users u ON o.user_id = u.id
[DB-2024-03-15 10:37:00] QUERY executed in 0.001s: SELECT * FROM users WHERE username = 'admin' OR 1=1--'
[DB-2024-03-15 10:38:00] QUERY executed in 0.002s: SELECT * FROM users UNION SELECT * FROM passwords
192.168.1.200 - - [15/Mar/2024:10:40:00 -0600] "GET /products?id=1 HTTP/1.1" 200 5678 "https://tienda.com" "Mozilla/5.0"
192.168.1.200 - - [15/Mar/2024:10:40:05 -0600] "GET /products?id=2 HTTP/1.1" 200 4321 "https://tienda.com" "Mozilla/5.0"
192.168.1.201 - - [15/Mar/2024:10:41:00 -0600] "GET /api/users HTTP/1.1" 401 123 "-" "PostmanRuntime/7.26.8"
192.168.1.201 - - [15/Mar/2024:10:41:05 -0600] "GET /api/users HTTP/1.1" 500 0 "-" "PostmanRuntime/7.26.8"
[2024-03-15 10:42:00] ERROR app.api - NullPointerException: Cannot read property 'id' of undefined
[DB-2024-03-15 10:45:00] SLOW_QUERY (5.2s): SELECT COUNT(*) FROM logs WHERE date > '2024-01-01'
""".strip()

if __name__ == "__main__":
    print("PRUEBA DE PARSERS INDIVIDUALES")
    print("=" * 50)
    
    linea_http = '192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0"'
    print(f"\n-- Parser HTTP --\nResultado: {parse_http_log(linea_http)}")
    
    linea_error = "[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused"
    print(f"\n-- Parser Error --\nResultado: {parse_error_log(linea_error)}")
    
    linea_auth = "[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz"
    print(f"\n-- Parser Auth --\nResultado: {parse_auth_log(linea_auth)}")
    
    linea_db = "[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users"
    print(f"\n-- Parser DB --\nResultado: {parse_db_log(linea_db)}")
    
    print("\nGENERANDO REPORTE COMPLETO...\n")
    reporte = generar_reporte(LOGS_PRUEBA)
    mostrar_reporte(reporte)