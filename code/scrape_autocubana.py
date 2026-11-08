#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Web Scraping para extraer el catálogo de vehículos en venta
de la página web: https://www.autocubana.com/es
Guarda los resultados en un archivo CSV dentro de la carpeta data/.
"""

# ============================================================
# 1. IMPORTACIONES DE LIBRERÍAS
# ============================================================

# requests: librería para hacer peticiones HTTP (descargar páginas web)
import requests

# BeautifulSoup: librería para analizar el HTML y buscar datos dentro de él
from bs4 import BeautifulSoup

# csv: librería nativa de Python para crear y escribir archivos CSV
import csv

# os: librería para trabajar con rutas de archivos y carpetas del sistema
import os

# time: librería para añadir pausas entre peticiones (ser respetuosos con el servidor)
import time

# re: librería para usar expresiones regulares (buscar patrones dentro de texto)
import re

# urljoin: función para construir URLs completas a partir de una base y una ruta relativa
from urllib.parse import urljoin

# Intentamos importar curl_cffi como respaldo para cuando la página devuelva error 403.
# curl_cffi simula un navegador real y puede evadir algunos bloqueos anti-bot.
try:
    from curl_cffi import requests as curl_requests
    CURL_DISPONIBLE = True
except ImportError:
    # Si curl_ccci no está instalado, continuamos solo con requests
    CURL_DISPONIBLE = False
    print("[AVISO] curl_cffi no está instalado. Solo se usará requests como respaldo.")


# ============================================================
# 2. CONFIGURACIÓN Y CONSTANTES DEL SCRIPT
# ============================================================

# URL base del sitio web (sin barra final)
URL_BASE = "https://www.autocubana.com"

# URL de la página principal donde se muestran los anuncios de vehículos
URL_PAGINA_PRINCIPAL = f"{URL_BASE}/es"

# Nombre de la carpeta donde se guardará el archivo CSV
CARPETA_DATA = "data"

# Nombre exacto del archivo CSV de salida
NOMBRE_CSV = "autocubana_autos.csv"

# Ruta completa del archivo CSV (carpeta + nombre)
RUTA_CSV = os.path.join(CARPETA_DATA, NOMBRE_CSV)

# Tiempo de espera entre peticiones HTTP en segundos (requisito: time.sleep(2))
TIEMPO_ESPERA = 2

# Lista con los nombres exactos de las columnas que tendrá el CSV
COLUMNAS_CSV = [
    "Marca",
    "Modelo",
    "Anio",
    "Precio",
    "Moneda",
    "Papeles",
    "Provincias",
    "Uso_y_Desgaste",
    "Mecanicas_y_Dimensiones",
    "URL_Anuncio",
    "Descripcion_Cruda"
]

# Encabezados HTTP que simulan un navegador web real (Chrome).
# Esto ayuda a evitar que el servidor rechace las peticiones por parecer de un bot.
ENCABEZADOS_NAVEGADOR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

# Lista de provincias cubanas conocidas, para ayudar a identificar la provincia
# de cada anuncio desde el texto o los enlaces de la página.
PROVINCIAS_CUBA = [
    "Pinar del Rio", "Artemisa", "Mayabeque", "La Habana", "Habana",
    "Matanzas", "Cienfuegos", "Villa Clara", "Sancti Spiritus",
    "Ciego de Avila", "Camaguey", "Las Tunas", "Holguin", "Granma",
    "Santiago de Cuba", "Guantanamo"
]


# ============================================================
# 3. FUNCIONES AUXILIARES (pequeñas herramientas reutilizables)
# ============================================================

def obtener_html(url):
    """
    Descarga el contenido HTML de una página web.
    Si la página devuelve un error 403, intenta usar curl_cffi como respaldo.
    Devuelve el HTML como texto (str) o None si falla.
    """
    try:
        # --- PRIMER INTENTO: usar requests ---
        respuesta = requests.get(url, headers=ENCABEZADOS_NAVEGADOR, timeout=15)

        # Si todo salió bien (código 200), devolvemos el HTML
        if respuesta.status_code == 200:
            return respuesta.text

        # Si el servidor bloqueó el acceso (código 403), usamos curl_cffi
        elif respuesta.status_code == 403:
            print(f"    [!] Error 403 recibido en {url}. Intentando con curl_cffi...")
            if CURL_DISPONIBLE:
                try:
                    # curl_cffi con impersonate="chrome" simula ser Chrome real
                    respuesta_curl = curl_requests.get(url, impersonate="chrome", timeout=15)
                    if respuesta_curl.status_code == 200:
                        return respuesta_curl.text
                    else:
                        print(f"    [X] curl_cffi devolvió código {respuesta_curl.status_code}")
                except Exception as e_curl:
                    print(f"    [X] Error con curl_cffi: {e_curl}")
            else:
                print("    [X] curl_cffi no está disponible.")
            return None

        # Para cualquier otro código de error HTTP
        else:
            print(f"    [!] Código HTTP {respuesta.status_code} para {url}")
            return None

    except requests.exceptions.RequestException as e:
        # Capturamos cualquier error de red (sin conexión, timeout, DNS, etc.)
        print(f"    [X] Error de red al acceder a {url}: {e}")
        return None


def extraer_urls_anuncios(html_pagina_principal):
    """
    Busca en el HTML de la página principal todos los enlaces que lleven
    a anuncios individuales de vehículos (patrón: /ads/anuncio-...).
    Devuelve una lista ordenada de URLs completas.
    """
    # Creamos el objeto BeautifulSoup para poder buscar dentro del HTML
    sopa = BeautifulSoup(html_pagina_principal, "html.parser")

    # Usamos un set() para guardar URLs únicas (los sets eliminan duplicados automáticamente)
    urls_encontradas = set()

    # Buscamos TODOS los enlaces <a> que tengan un atributo href
    for enlace in sopa.find_all("a", href=True):
        # Obtenemos la dirección del enlace
        href = enlace["href"]

        # Verificamos si el enlace apunta a un anuncio de vehículo
        if "/ads/anuncio-" in href:
            # urljoin construye la URL completa: URL_BASE + href
            # (por ejemplo: https://www.autocubana.com + /es/ads/anuncio-...)
            url_completa = urljoin(URL_BASE, href)
            urls_encontradas.add(url_completa)

    # Convertimos el set a lista, la ordenamos alfabéticamente y la devolvemos
    return sorted(list(urls_encontradas))


def extraer_provincia(sopa, url_anuncio):
    """
    Intenta obtener el nombre de la provincia del anuncio.
    Usa dos métodos:
    1) Busca un encabezado <h2> con el patrón '... en {Provincia}'
    2) Analiza la URL del anuncio para extraer la provincia
    Si falla, devuelve 'No especificada'.
    """
    # --- MÉTODO 1: Buscar en los encabezados <h2> ---
    for h2 in sopa.find_all("h2"):
        texto_h2 = h2.get_text(strip=True)
        # Buscamos el patrón "en {Provincia}" al final del texto
        # Por ejemplo: "Comprar carros Toyota en Holguin" -> "Holguin"
        coincidencia = re.search(r'\ben\s+(.+)$', texto_h2)
        if coincidencia:
            provincia_candidata = coincidencia.group(1).strip()
            # Verificamos que coincida con una provincia cubana conocida
            for prov in PROVINCIAS_CUBA:
                if prov.lower() in provincia_candidata.lower():
                    return prov
            # Si no coincide con la lista, igual devolvemos el texto encontrado
            if len(provincia_candidata) < 30:
                return provincia_candidata

    # --- MÉTODO 2: Analizar la URL del anuncio ---
    # La URL tiene el formato: anuncio-{marca}-{modelo}-{provincia}-{ciudad}-{id}
    # Por ejemplo: anuncio-toyota-rav4-holguin-antilla-3415
    # Buscamos la provincia en las partes de la URL
    partes_url = url_anuncio.rstrip("/").split("/")
    ultima_parte = partes_url[-1]  # ej: "anuncio-toyota-rav4-holguin-antilla-3415"
    # Eliminamos el prefijo "anuncio-" y el sufijo numérico
    limpio = re.sub(r'^anuncio-', '', ultima_parte)
    limpio = re.sub(r'-\d+$', '', limpio)  # quitamos el ID numérico final
    # Buscamos alguna provincia conocida dentro de la cadena
    for prov in PROVINCIAS_CUBA:
        patron_prov = prov.lower().replace(" ", "-")
        if patron_prov in limpio:
            return prov

    # Si ningún método funcionó
    return "No especificada"


def extraer_marca_desde_enlaces(sopa):
    """
    Intenta extraer la marca del vehículo desde los enlaces de la página.
    Busca enlaces como: /anuncios-Carro-Toyota o /anuncios-Moto-BMW
    Devuelve la marca como texto o cadena vacía si no la encuentra.
    """
    # Definimos los prefijos de tipo de vehículo que usa el sitio
    prefijos_tipo = ["/anuncios-Carro-", "/anuncios-Moto-", "/anuncios-Utilitario-"]

    for enlace in sopa.find_all("a", href=True):
        href = enlace["href"]
        # Verificamos si el enlace coincide con algún prefijo de tipo Y no es de provincia
        for prefijo in prefijos_tipo:
            if href.startswith(prefijo) and "-en-" not in href:
                # Extraemos la parte después del prefijo (la marca)
                # Por ejemplo: /anuncios-Carro-Toyota -> "Toyota"
                marca = href[len(prefijo):]
                # Limpiamos caracteres no deseados
                marca = marca.replace("%20", " ").strip()
                if marca and len(marca) < 30:
                    return marca
    return ""


def limpiar_precio(texto_precio):
    """
    Limpia el texto del precio para obtener solo el número.
    Por ejemplo: "16 000" -> "16000", "1 111" -> "1111"
    Si no hay número (como "NEGOTIABLE"), devuelve cadena vacía.
    """
    # Eliminamos espacios y comas del texto
    texto_limpio = texto_precio.replace(" ", "").replace(",", "")
    # Buscamos si hay dígitos en el texto
    coincidencia = re.search(r'\d+', texto_limpio)
    if coincidencia:
        return coincidencia.group(0)
    return ""


# ============================================================
# 4. FUNCIÓN PRINCIPAL PARA PARSEAR CADA ANUNCIO INDIVIDUAL
# ============================================================

def parsear_anuncio(url_anuncio):
    """
    Descarga la página de un anuncio individual y extrae toda la información
    solicitada: Marca, Modelo, Año, Precio, Moneda, Papeles, Provincia, etc.
    Devuelve un diccionario con los datos o None si falla.
    """
    # Descargamos el HTML de la página del anuncio
    html_anuncio = obtener_html(url_anuncio)

    # Si no pudimos descargar la página, devolvemos None
    if html_anuncio is None:
        print(f"    [X] No se pudo descargar: {url_anuncio}")
        return None

    # Creamos el objeto BeautifulSoup para analizar el HTML
    sopa = BeautifulSoup(html_anuncio, "html.parser")

    # Inicializamos un diccionario con todos los campos vacíos
    datos = {
        "Marca": "",
        "Modelo": "",
        "Anio": "",
        "Precio": "",
        "Moneda": "",
        "Papeles": "No especificado",
        "Provincias": "",
        "Uso_y_Desgaste": "No especificado",
        "Mecanicas_y_Dimensiones": "",
        "URL_Anuncio": url_anuncio,
        "Descripcion_Cruda": ""
    }

    # --- EXTRAER MARCA Y MODELO ---
    # El título del anuncio está en un <h2> dentro de div.ad-title
    div_titulo = sopa.find("div", class_="ad-title")
    if div_titulo:
        h2_titulo = div_titulo.find("h2")
        if h2_titulo:
            texto_titulo = h2_titulo.get_text(strip=True)
            # Separamos por el primer espacio para separar marca y modelo
            # Por ejemplo: "Toyota RAV4" -> Marca="Toyota", Modelo="RAV4"
            partes = texto_titulo.split(" ", 1)
            if len(partes) >= 2:
                datos["Marca"] = partes[0]
                datos["Modelo"] = partes[1]
            else:
                # Si solo hay una palabra, la usamos como modelo
                datos["Modelo"] = texto_titulo

    # Intentamos mejorar la marca usando los enlaces de la página
    marca_en_enlace = extraer_marca_desde_enlaces(sopa)
    if marca_en_enlace:
        datos["Marca"] = marca_en_enlace
        # Si la marca cambió, ajustamos el modelo quitando la marca del título
        if datos["Modelo"].startswith(datos["Marca"]):
            datos["Modelo"] = datos["Modelo"][len(datos["Marca"]):].strip()

    # --- EXTRAER PROPIEDADES DEL VEHÍCULO (Año, Motor, etc.) ---
    # Las propiedades están en div.vehicle-properties, cada una en un div.prop
    lista_mecanicas = []
    div_props = sopa.find("div", class_="vehicle-properties")
    if div_props:
        for prop in div_props.find_all("div", class_="prop"):
            # Cada prop tiene dos <span>: el nombre y el valor
            spans = prop.find_all("span")
            if len(spans) >= 2:
                # Obtenemos el nombre y valor usando el atributo "title" del span
                nombre = spans[0].get("title", spans[0].get_text(strip=True))
                valor = spans[1].get("title", spans[1].get_text(strip=True))

                # Si es el Año, lo guardamos en su campo específico
                if nombre == "Año":
                    datos["Anio"] = valor

                # Si es la Condición (Usados/Nuevos), lo guardamos como Uso_y_Desgaste
                elif nombre == "Condición":
                    datos["Uso_y_Desgaste"] = valor

                # Para el resto de propiedades (Motor, Caja, Km, etc.),
                # las acumulamos en la lista de mecánicas y dimensiones
                if nombre not in ("Año", "Color"):
                    lista_mecanicas.append(f"{nombre}: {valor}")

    # Unimos todas las propiedades con " | " para el campo Mecanicas_y_Dimensiones
    datos["Mecanicas_y_Dimensiones"] = " | ".join(lista_mecanicas)

    # --- EXTRAER PRECIO Y MONEDA ---
    div_precio = sopa.find("div", class_="ad-price")
    if div_precio:
        # Buscamos el span con la clase "price" que contiene el número
        span_precio = div_precio.find("span", class_="price")
        if span_precio:
            # Hay un precio numérico (ej: "16 000")
            texto_precio = span_precio.get_text(strip=True)
            datos["Precio"] = limpiar_precio(texto_precio)

            # La moneda está en el texto del div.ad-price que NO está en el span.price
            # Por ejemplo: "CUC" aparece antes del número
            texto_completo = div_precio.get_text(strip=True)
            # Eliminamos el precio del texto completo para quedarnos con la moneda
            moneda = texto_completo.replace(texto_precio, "").strip()
            datos["Moneda"] = moneda if moneda else "No especificada"
        else:
            # No hay span.price, el texto completo es la moneda/estado
            # Por ejemplo: "NEGOTIABLE" (negociable)
            texto_precio = div_precio.get_text(strip=True)
            if "NEGOTIABLE" in texto_precio.upper() or "NEGOCIABLE" in texto_precio.upper():
                datos["Moneda"] = "NEGOTIABLE"
                datos["Precio"] = ""
            else:
                datos["Moneda"] = texto_precio

    # --- EXTRAER PROVINCIA ---
    datos["Provincias"] = extraer_provincia(sopa, url_anuncio)

    # --- EXTRAER DESCRIPCIÓN CRUDA (comentario del vendedor) ---
    div_comentario = sopa.find("div", class_="ad-seller-comment")
    if div_comentario:
        # Buscamos el div interior con clase "comment-wrapper" que tiene el texto real
        div_wrapper = div_comentario.find("div", class_="comment-wrapper")
        if div_wrapper:
            # get_text() obtiene todo el texto visible, con saltos de línea
            datos["Descripcion_Cruda"] = div_wrapper.get_text(separator="\n", strip=True)
        else:
            # Si no hay wrapper, tomamos todo el texto del comentario
            datos["Descripcion_Cruda"] = div_comentario.get_text(separator="\n", strip=True)

    # --- BUSCAR PAPELES EN LA DESCRIPCIÓN ---
    # "Papeles" no es un campo estándar del sitio, así que buscamos
    # palabras clave en la descripción del vendedor
    descripcion_lower = datos["Descripcion_Cruda"].lower()
    keywords_papeles = ["papeles", "documentos", "tarjeta", "factura",
                        "placa", "registro", "original", "duplicado"]
    for keyword in keywords_papeles:
        if keyword in descripcion_lower:
            # Si encontramos la palabra clave, intentamos extraer una frase alrededor
            indice = descripcion_lower.find(keyword)
            inicio = max(0, indice - 30)
            fin = min(len(datos["Descripcion_Cruda"]), indice + 50)
            fragmento = datos["Descripcion_Cruda"][inicio:fin].strip()
            datos["Papeles"] = fragmento
            break

    # --- BUSCAR INFORMACIÓN DE USO Y DESGASTE EN LA DESCRIPCIÓN ---
    keywords_uso = ["excelente estado", "buen estado", "como nuevo",
                    "revisado", "mantenimiento", "desgaste", "golpes",
                    "rayones", "estreno", "recién"]
    for keyword in keywords_uso:
        if keyword in descripcion_lower:
            indice = descripcion_lower.find(keyword)
            inicio = max(0, indice - 20)
            fin = min(len(datos["Descripcion_Cruda"]), indice + 60)
            fragmento = datos["Descripcion_Cruda"][inicio:fin].strip()
            # Solo sobrescribimos si el valor actual es el default
            if datos["Uso_y_Desgaste"] == "No especificado":
                datos["Uso_y_Desgaste"] = fragmento
            break

    return datos


# ============================================================
# 5. FUNCIÓN PRINCIPAL DEL SCRIPT
# ============================================================

def main():
    """
    Función principal que orquesta todo el proceso de scraping:
    1. Descarga la página principal
    2. Extrae las URLs de todos los anuncios
    3. Visita cada anuncio y extrae los datos
    4. Guarda todo en un archivo CSV
    """
    print("=" * 60)
    print("  SCRIPT DE WEB SCRAPING - AutoCubana.com")
    print("=" * 60)

    # --- PASO 1: Crear la carpeta data/ si no existe ---
    os.makedirs(CARPETA_DATA, exist_ok=True)
    print(f"\n[1] Carpeta '{CARPETA_DATA}/' lista para guardar el CSV.")

    # --- PASO 2: Descargar la página principal ---
    print(f"\n[2] Descargando página principal: {URL_PAGINA_PRINCIPAL}")
    html_principal = obtener_html(URL_PAGINA_PRINCIPAL)

    if html_principal is None:
        print("    [X] No se pudo descargar la página principal. Abortando.")
        return

    # Pausa educada entre peticiones
    time.sleep(TIEMPO_ESPERA)
    print("    [OK] Página principal descargada correctamente.")

    # --- PASO 3: Extraer las URLs de todos los anuncios visibles ---
    urls_anuncios = extraer_urls_anuncios(html_principal)
    print(f"\n[3] Se encontraron {len(urls_anuncios)} anuncios en la página principal.")

    if not urls_anuncios:
        print("    [X] No se encontraron anuncios. Abortando.")
        return

    # Mostramos las primeras 3 URLs como ejemplo
    for url_ej in urls_anuncios[:3]:
        print(f"    Ejemplo: {url_ej}")

    # --- PASO 4: Visitar cada anuncio y extraer los datos ---
    print(f"\n[4] Procesando cada anuncio (espera de {TIEMPO_ESPERA}s entre peticiones)...")
    lista_datos = []

    for indice, url_anuncio in enumerate(urls_anuncios, start=1):
        print(f"\n  [{indice}/{len(urls_anuncios)}] Procesando: {url_anuncio}")

        try:
            # Parseamos el anuncio actual
            datos_anuncio = parsear_anuncio(url_anuncio)

            # Si el parseo fue exitoso, agregamos los datos a la lista
            if datos_anuncio is not None:
                lista_datos.append(datos_anuncio)
                print(f"    [OK] Marca: {datos_anuncio['Marca']} | "
                      f"Modelo: {datos_anuncio['Modelo']} | "
                      f"Año: {datos_anuncio['Anio']} | "
                      f"Precio: {datos_anuncio['Precio']} {datos_anuncio['Moneda']}")
            else:
                print(f"    [X] No se pudieron extraer datos de este anuncio.")

        except Exception as e:
            # Capturamos cualquier error inesperado al parsear un anuncio
            print(f"    [X] Error inesperado al procesar {url_anuncio}: {e}")

        # Esperamos 2 segundos entre peticiones (requisito del usuario)
        time.sleep(TIEMPO_ESPERA)

    # --- PASO 5: Guardar los datos en el archivo CSV ---
    print(f"\n[5] Guardando {len(lista_datos)} anuncios en '{RUTA_CSV}'...")

    try:
        # Abrimos el archivo CSV en modo escritura ("w")
        # encoding="utf-8-sig" asegura que los acentos y ñ se vean bien en Excel
        with open(RUTA_CSV, mode="w", newline="", encoding="utf-8-sig") as archivo_csv:
            # Creamos un escritor CSV con los nombres de las columnas
            escritor = csv.DictWriter(archivo_csv, fieldnames=COLUMNAS_CSV)

            # Escribimos la fila de encabezados (nombres de columnas)
            escritor.writeheader()

            # Escribimos cada fila de datos
            for fila in lista_datos:
                escritor.writerow(fila)

        print(f"    [OK] Archivo CSV guardado exitosamente en: {RUTA_CSV}")

    except IOError as e:
        # Capturamos errores al escribir el archivo (permisos, disco lleno, etc.)
        print(f"    [X] Error al escribir el archivo CSV: {e}")

    # --- RESUMEN FINAL ---
    print("\n" + "=" * 60)
    print("  RESUMEN DEL SCRAPING")
    print("=" * 60)
    print(f"  Total de anuncios encontrados: {len(urls_anuncios)}")
    print(f"  Anuncios procesados con éxito: {len(lista_datos)}")
    print(f"  Archivo CSV generado: {RUTA_CSV}")
    print("=" * 60)


# ============================================================
# 6. PUNTO DE ENTRADA DEL SCRIPT
# ============================================================

# Verificamos si el script se ejecuta directamente (no se importa como módulo)
if __name__ == "__main__":
    # Llamamos a la función principal
    main()
