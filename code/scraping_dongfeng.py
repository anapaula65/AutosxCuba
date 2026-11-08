#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraping del catalogo de vehiculos de https://dongfengqba.com/

Extrae las secciones "Autos recomendados" y "Vehiculos comerciales"
y guarda el resultado en dongfeng_cuba_catalogo.csv.

El CSV nunca se sobrescribe: si ya existe, se agregan solo las filas nuevas
(sin duplicar por URL_Anuncio). Requiere:  pip install requests beautifulsoup4 curl_cffi
"""

# ==============================================================================
# IMPORTACIÓN DE LIBRERÍAS (Módulos externos e internos de Python)
# ==============================================================================

# 'csv': Módulo nativo para leer y escribir archivos con formato de valores separados por comas.
import csv

# 'os': Permite consultar el sistema de archivos (verificar si un archivo existe, tamaño, rutas).
import os

# 're': Módulo de Expresiones Regulares para buscar y limpiar patrones de texto complejos.
import re

# 'time': Para pausar la ejecución del código (evitar sobrecargar el servidor web).
import time

# 'urljoin': Une una dirección web base con un enlace relativo (ejemplo: 'https://sitio.com' + '/auto' -> 'https://sitio.com/auto').
from urllib.parse import urljoin

# 'requests': Librería estándar de la industria para enviar peticiones HTTP y descargar páginas.
import requests

# 'BeautifulSoup': Librería para analizar el árbol HTML de una página web y extraer etiquetas fácilmente.
from bs4 import BeautifulSoup


# ==============================================================================
# CONFIGURACIÓN Y CONSTANTES DEL PROGRAMA
# ==============================================================================

# URL completa del sitio web oficial de Dongfeng en Cuba.
URL_PAGINA = "https://dongfengqba.com/"

# Dominio base que usaremos para convertir enlaces relativos en absolutos.
URL_BASE = "https://dongfengqba.com"

# Nombre del archivo donde almacenaremos la información recolectada.
ARCHIVO_CSV = "dongfeng_cuba_catalogo.csv"

# Bandera booleana (True/False):
# True  -> Guarda también los autos que no muestren precio en la página web.
# False -> Descarta cualquier vehículo que no tenga precio visible.
INCLUIR_SIN_PRECIO = True

# Lista con los nombres de las 11 columnas que tendrá el archivo CSV final.
COLUMNAS = [
    "Marca",
    "Modelo",
    "Anio",
    "Precio",
    "Moneda",
    "Papeles",
    "Provincias",
    "Uso y desgaste",
    "Mecánicas y dimensiones",
    "URL_Anuncio",
    "Descripcion_Cruda",
]

# Cabeceras (Headers) HTTP: Simulan una petición proveniente de un navegador Google Chrome real en Linux,
# lo que previene bloqueos automáticos por parte del servidor web.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}


# ==============================================================================
# FUNCIONES DE DESCARGA Y EXTRACCIÓN DE DATOS
# ==============================================================================

def obtener_html(url):
    """
    Descarga el contenido HTML de la página web.
    Usa 'requests' por defecto, pero si recibe un error 403 (Prohibido/Cloudflare),
    activa automáticamente 'curl_cffi' que imita la huella TLS de Chrome.
    """
    try:
        # Hacemos la petición GET con límite de espera de 20 segundos
        respuesta = requests.get(url, headers=HEADERS, timeout=20)
        # Si el servidor responde con 403 Forbidden, forzamos el uso del respaldo
        if respuesta.status_code == 403:
            print("Respuesta 403 con requests; usando curl_cffi como respaldo...")
            raise requests.HTTPError("403 Forbidden")
        # Si hubo otro código de error HTTP (como 404 o 500), genera una excepción
        respuesta.raise_for_status()
        # Si todo fue exitoso, devuelve el texto HTML
        return respuesta.text
    except Exception as error:
        # En caso de cualquier falla con requests, intentamos el plan B con curl_cffi
        print(f"requests fallo ({error}); usando curl_cffi como respaldo...")
        try:
            # Importamos curl_cffi solo cuando es necesario
            from curl_cffi import requests as solicitudes_curl

            # Hacemos la petición fingiendo ser Chrome
            respuesta = solicitudes_curl.get(url, impersonate="chrome", timeout=20)
            respuesta.raise_for_status()
            return respuesta.text
        except Exception as error_curl:
            # Si ambos métodos fallan, informamos el error y devolvemos None
            print(f"No se pudo descargar la pagina: {error_curl}")
            return None
    finally:
        # 'finally' se ejecuta SIEMPRE: aseguramos una pausa de cortesía de 2 segundos
        time.sleep(2)


def limpiar_precio(texto):
    """
    Extrae únicamente los dígitos de un texto de precio con euros.
    Ejemplo: recibe 'Desde € 22.900' y devuelve '22900'.
    """
    if not texto:
        return ""
    # Busca el símbolo de euro seguido de números y puntos (ej: € 22.900)
    encontrado = re.search(r"€\s*([\d.]+)", texto)
    if not encontrado:
        return ""
    # Elimina los puntos de miles y espacios para dejar un número limpio
    return encontrado.group(1).replace(".", "").replace(" ", "")


def detectar_marca(alt_imagen, modelo, id_articulo):
    """
    Determina la submarca o marca del vehículo analizando el texto del modelo,
    el texto alternativo de la imagen (alt) y el atributo id de la etiqueta.
    """
    # Unificamos todos los textos en minúsculas para facilitar la búsqueda
    texto = f"{alt_imagen} {modelo} {id_articulo}".lower()
    # Verificamos si pertenece a las líneas especiales 'Voyah' o 'MHERO'
    if "voyah" in texto:
        return "Voyah"
    if "mhero" in texto:
        return "MHERO"
    # Por defecto, la marca principal del catálogo es Dongfeng
    return "Dongfeng"


def armar_mecanicas(badge_tipo, badge_gauge, caracteristicas):
    """
    Une las etiquetas técnicas (tipo de motor, autonomía/batería, prestaciones)
    en una sola cadena de texto separada por punto y coma ('; ').
    """
    partes = []
    # Recorremos todas las etiquetas recibidas
    for texto in [badge_tipo, badge_gauge] + list(caracteristicas):
        if not texto:
            continue
        # Limpiamos espacios en blanco redundantes
        limpio = re.sub(r"\s+", " ", texto).strip()
        # Filtramos textos no deseados (precios o menciones a garantías)
        if not limpio or "€" in limpio:
            continue
        if limpio.lower().startswith("garantía"):
            continue
        # Evitamos repetir la misma característica dos veces
        if limpio not in partes:
            partes.append(limpio)
    # Retornamos todas las características unidas por '; '
    return "; ".join(partes)


def extraer_vehiculos(html):
    """
    Analiza el HTML descargado, localiza todas las tarjetas de vehículos (<article>)
    y extrae los campos requeridos para el catálogo.
    """
    # Inicializamos el analizador HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    vehiculos = []

    # Buscamos cada tarjeta de producto identificada con la etiqueta <article>
    for articulo in soup.select("article"):
        # Extraemos el título del modelo dentro de la etiqueta <h3>
        h3 = articulo.select_one("h3")
        # Si un artículo no tiene <h3>, probablemente no sea un auto válido y lo saltamos
        if h3 is None:
            continue
        modelo = h3.get_text(" ", strip=True)

        # Buscamos la imagen del auto y su texto alternativo (alt)
        imagen = articulo.select_one("img")
        alt_imagen = imagen.get("alt", "") if imagen else ""

        # Buscamos el enlace a la ficha del vehículo y lo convertimos en URL completa
        enlace = articulo.select_one("a[href]")
        url = urljoin(URL_BASE, enlace["href"]) if enlace else ""

        # Buscamos la etiqueta flotante (badge) con el tipo de vehículo (ej: 'Eléctrico', 'SUV')
        badge = articulo.select_one("div.absolute.left-5.top-5 span")
        badge_tipo = badge.get_text(" ", strip=True) if badge else ""

        # Buscamos el ícono del medidor (gauge) que indica autonomía o potencia
        badge_gauge = ""
        icono = articulo.select_one('svg[data-icon="lucide:gauge"]')
        if icono is not None and icono.parent is not None:
            badge_gauge = icono.parent.get_text(" ", strip=True)

        # Buscamos el párrafo siguiente al título que contiene la descripción del vehículo
        descripcion = ""
        parrafo = h3.find_next("p")
        if parrafo is not None:
            descripcion = re.sub(r"\s+", " ", parrafo.get_text(" ", strip=True))

        # Procesamos la sección de precios y características secundarias
        precio = ""
        caracteristicas = []
        fila_precio = articulo.select_one("div.mt-4.flex.flex-wrap")
        if fila_precio is not None:
            for span in fila_precio.select("span"):
                texto = re.sub(r"\s+", " ", span.get_text(" ", strip=True))
                if not texto:
                    continue
                # Si contiene el símbolo del euro, es el precio del auto
                if "€" in texto and not precio:
                    precio = limpiar_precio(texto)
                else:
                    # En caso contrario, es una especificación técnica adicional
                    caracteristicas.append(texto)

        # Unificamos todas las especificaciones mecánicas
        mecanicas = armar_mecanicas(badge_tipo, badge_gauge, caracteristicas)

        # Si el usuario configuró no incluir autos sin precio, los omitimos aquí
        if not precio and not INCLUIR_SIN_PRECIO:
            continue

        # Agregamos el diccionario con los datos del vehículo a nuestra lista
        vehiculos.append(
            {
                "Marca": detectar_marca(alt_imagen, modelo, articulo.get("id", "")),
                "Modelo": modelo,
                "Anio": "Nuevo",            # Los vehículos de concesionario oficial son 0 km
                "Precio": precio,
                "Moneda": "EUR",            # Los precios en la web oficial están en Euros
                "Papeles": "Nuevo",
                "Provincias": "Cuba",       # Importación y venta directa a nivel nacional
                "Uso y desgaste": "",
                "Mecánicas y dimensiones": mecanicas,
                "URL_Anuncio": url,
                "Descripcion_Cruda": descripcion,
            }
        )

    return vehiculos


# ==============================================================================
# GESTIÓN Y PERSISTENCIA DE DATOS (CSV)
# ==============================================================================

def leer_filas(ruta):
    """
    Lee un archivo CSV existente y devuelve una lista de diccionarios con sus filas.
    Si el archivo no existe o está vacío, devuelve una lista vacía.
    """
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []
    try:
        # Abrimos el archivo en modo lectura ('r' implícito) con codificación utf-8-sig
        with open(ruta, newline="", encoding="utf-8-sig") as archivo:
            # csv.DictReader lee cada línea como un diccionario usando los encabezados como claves
            return list(csv.DictReader(archivo))
    except Exception as error:
        print(f"No se pudo leer {ruta}: {error}")
        return []


def ruta_segura(ruta):
    """
    Mecanismo de seguridad para no corromper datos:
    Si el archivo ya existe pero tiene columnas diferentes a las esperadas,
    crea un nombre nuevo (ej: catalogo_1.csv) para no romper el archivo original.
    """
    filas = leer_filas(ruta)
    # Si el archivo está vacío o sus columnas coinciden exactamente, usamos la ruta original
    if not filas or list(filas[0].keys()) == COLUMNAS:
        return ruta
    
    # Si las columnas no coinciden, buscamos un sufijo libre (_1, _2, etc.)
    contador = 1
    while True:
        alternativa = f"{os.path.splitext(ruta)[0]}_{contador}.csv"
        filas_alt = leer_filas(alternativa)
        if not os.path.exists(alternativa):
            print(f"Columnas distintas en {ruta}; se usara {alternativa}")
            return alternativa
        if list(filas_alt[0].keys()) == COLUMNAS:
            return alternativa
        contador += 1


def guardar_csv(vehiculos, ruta):
    """
    Guarda los vehículos en el archivo CSV sin borrar lo que ya existía (modo append).
    Deduplica por URL_Anuncio para no repetir ningún vehículo que ya estuviera guardado.
    Devuelve una tupla: (cantidad_nuevas, total_acumulado, ruta_usada).
    """
    # Obtenemos la ruta validada
    ruta = ruta_segura(ruta)
    # Leemos las filas que ya estaban guardadas previamente
    existentes = leer_filas(ruta)
    # Creamos un conjunto (set) con las URLs ya conocidas para búsqueda ultra-rápida O(1)
    urls_vistas = {f.get("URL_Anuncio", "") for f in existentes if f.get("URL_Anuncio")}

    # Filtramos solo aquellos vehículos que no hayan sido guardados antes
    nuevas = []
    for fila in vehiculos:
        url = fila.get("URL_Anuncio", "")
        # Si la URL ya existe en el archivo, la omitimos
        if url and url in urls_vistas:
            continue
        if url:
            urls_vistas.add(url)
        nuevas.append(fila)

    # Verificamos si el archivo está vacío o si no existe aún
    archivo_vacio = not os.path.exists(ruta) or os.path.getsize(ruta) == 0
    # Si hay filas nuevas o si el archivo debe crearse desde cero
    if nuevas or archivo_vacio:
        # Modo 'a' (append) para añadir al final, o 'w' (write) para crear de cero
        modo = "a" if not archivo_vacio else "w"
        encoding = "utf-8" if not archivo_vacio else "utf-8-sig"
        with open(ruta, modo, newline="", encoding=encoding) as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
            # Solo escribimos los encabezados si el archivo era nuevo o estaba vacío
            if archivo_vacio:
                escritor.writeheader()
            # Escribimos las filas nuevas
            escritor.writerows(nuevas)

    return len(nuevas), len(existentes) + len(nuevas), ruta


# ==============================================================================
# FUNCIÓN PRINCIPAL (MAIN)
# ==============================================================================

def main():
    """Función orquestadora que ejecuta los pasos del scraping en orden."""
    print(f"Descargando {URL_PAGINA} ...")
    # 1. Descargamos el HTML del sitio web
    html = obtener_html(URL_PAGINA)
    if not html:
        print("No se pudo obtener la pagina.")
        return

    # 2. Analizamos y extraemos los vehículos
    try:
        vehiculos = extraer_vehiculos(html)
    except Exception as error:
        print(f"Error al analizar la pagina: {error}")
        return

    # Si no se encontraron datos, finalizamos con aviso
    if not vehiculos:
        print("No se encontraron vehiculos.")
        return

    # 3. Guardamos los datos en el archivo CSV de forma segura
    try:
        guardadas, total, ruta = guardar_csv(vehiculos, ARCHIVO_CSV)
    except Exception as error:
        print(f"Error al escribir el CSV: {error}")
        return

    # 4. Mostramos estadísticas y métricas del proceso
    sin_precio = sum(1 for v in vehiculos if not v["Precio"])
    print(f"Vehículos extraídos: {len(vehiculos)} ({sin_precio} sin precio visible)")
    print(f"Vehículos guardados exitosamente: {guardadas}")
    print(f"Total de filas en {ruta}: {total}")


# Punto de entrada estándar en Python: asegura que el script corra solo al ejecutarse directamente
if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error inesperado: {error}")
