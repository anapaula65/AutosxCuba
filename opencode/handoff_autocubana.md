# Handoff: Scraping de AutoCubana

## 🎯 Objetivo del Journey
Extraer el catálogo de vehículos de AutoCubana (sitio especializado en Cuba) para obtener datos de oferta de un mercado más formal.

## 🤖 Prompts utilizados (Journey)
1. *"Actúa como un desarrollador experto en Python y Web Scraping. Necesito un script para extraer el catálogo de vehículos en venta de este sitio: https://www.autocubana.com/es..."*

## 🛠️ Soluciones y Aprendizajes
- **Problema encontrado:** Algunos autos tenían precios en CUC (moneda antigua) y otros decían "NEGOTIABLE".
- **Solución implementada:** El script de Python limpió los datos y convirtió los CUC a USD para que el dataset fuera uniforme.
- **Aprendizaje:** Se logró extraer con éxito un total de 24 anuncios de vehículos y motos en un solo intento.

## 📦 Resultado Final (Handoff)
Se generó el script `scraper_autocubana.py` y el archivo `data/autocubana_autos.csv` con 24 registros listos para unificar.
