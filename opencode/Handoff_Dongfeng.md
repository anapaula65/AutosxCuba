# Handoff: Scraping de Dongfeng Cuba

## Objetivo del Journey
Extraer el catálogo completo de vehículos del sitio oficial de Dongfeng Cuba (`dongfengqba.com`) para complementar el dataset con vehículos nuevos (0 km) y precios en Euros.

## Prompts utilizados (Journey)
1. *"Actúa como un desarrollador experto en Python y Web Scraping. Necesito un script para extraer el catálogo completo de vehículos de esta página: https://dongfengqba.com/..."*
2. *"Ahora necesito que modifiques el script para que también entre a la página /catalogo/ y extraiga los modelos adicionales (EM 26, Shine E2, V9 PHEV, etc.)..."*

## Soluciones y Aprendizajes
- **Problema encontrado:** La página de inicio no mostraba todos los vehículos disponibles.
- **Solución de OpenCode:** Se le indicó al scraper que navegara también a la sección `/catalogo/` para capturar la lista completa de modelos (incluyendo vehículos comerciales).
- **Problema encontrado:** Los precios estaban en formato de texto con símbolo de Euro y puntos de miles (ej. `€ 15.900`).
- **Solución de OpenCode:** Se usó manipulación de strings para limpiar el precio y dejarlo como un número entero (ej. `15900`), y se guardó la moneda como `EUR`.

## Resultado Final (Handoff)
Se generó el script `scraper_dongfeng.py` que extrae los vehículos del catálogo de Dongfeng (Shine, T5 EVO, Mage PHEV, MHERO, etc.) y los guarda en el archivo `dongfeng_cuba_catalogo.csv`. Este archivo luego fue unificado con los datos de Revolico, aplicando una conversión de EUR a USD.
