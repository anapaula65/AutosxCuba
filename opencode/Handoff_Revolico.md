# Handoff: Scraping de Revolico

## Objetivo del Journey
Extraer información de anuncios de carros en Cuba desde el sitio web Revolico para construir un dataset inicial.

## Prompts utilizados (Journey)
1. *"Actúa como un desarrollador experto en Python y Web Scraping. Necesito un script para extraer exactamente 30 anuncios de la sección de carros de Revolico..."*
2. *"Ahora necesito ampliarlo para extraer al menos 80 anuncios, detectando la paginación..."*

## Soluciones y Aprendizajes
- **Problema encontrado:** El sitio bloqueaba las peticiones básicas con un error 403 (Cloudflare).
- **Solución de OpenCode:** Se implementó la librería `curl_cffi` para imitar la huella digital de un navegador real (Chrome) y evadir el bloqueo.
- **Problema encontrado:** El HTML de la página era desordenado y no tenía clases claras.
- **Solución de OpenCode:** Se usaron expresiones regulares (regex) para extraer la Marca, Modelo y Año a partir del texto del título. Se extrajo la provincia desde el JSON interno (`__NEXT_DATA__`).

## Resultado Final (Handoff)
Se generó el script `scraper_revolico.py` que extrae exitosamente 80 anuncios únicos y los guarda en `revolico_80_anuncios.csv` con las columnas solicitadas (sin realizar limpieza de texto, solo extracción cruda).
