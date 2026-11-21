 Historial de Hitos del Proyecto (Commits Lógicos)

*Nota: Debido a problemas técnicos externos (restricciones de red en Cuba y bloqueos de cuenta automáticos de GitHub), el historial de Git se reconstruyó localmente agrupando los avances más significativos del proyecto.*

- `Hito 1 - Inicialización:` Creación de la estructura del proyecto, carpetas base y repositorio local.
- `Hito 2 - Scraping Revolico:` Extracción automatizada de 80 anuncios de autos con manejo de bloqueos 403 (curl_cffi).
- `Hito 3 - Scraping Dongfeng:` Extracción del catálogo oficial de vehículos nuevos (eléctricos e híbridos) y estandarización de precios en EUR.
- `Hito 4 - Recolección Cualitativa:` Extracción manual de 19 anuncios de canales de Telegram y realización de 15 entrevistas (vendedores, particulares y mecánicos).
- `Hito 5 - Scraping AutoCubana:` Desarrollo de script para extraer 24 anuncios de un sitio especializado, incluyendo la limpieza de precios en CUC a USD.
- `Hito 6 - Limpieza y Unificación:` Unión de las 5 fuentes de datos en el archivo maestro `PROYECTO_AUTOS_DATASET_OFICIAL.csv`, gestionando valores nulos y monedas.
- `Hito 7 - Análisis Exploratorio (EDA):` Generación de los 6 gráficos principales (precios, marcas, año, provincias, combustible) y extracción de conclusiones.
- `Hito 8 - Modelado Predictivo:` Implementación y entrenamiento del modelo Random Forest (Machine Learning) para predecir precios basados en año y marca.
- `Hito 9 - Documentación y Web:` Redacción del reporte técnico, la historia del proyecto y desarrollo del sitio web interactivo (AutosxCuba).
- `Hito 10 - Entrega Final:` Empaquetado del código, datos, evidencias y web en el archivo comprimido final para su evaluación.
