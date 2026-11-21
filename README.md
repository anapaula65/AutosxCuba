# Proyecto: Análisis del Mercado Automotriz en Cuba

**Estudiante:** Ana Paula González Gómez 
**Materia:** Ciencia de Datos - 1er Año

## Pregunta de Investigación
¿Qué relación existe entre las características técnicas y comerciales de los vehículos (como potencia, antigüedad, kilometraje, combustible) y su precio de venta en el mercado cubano?

## Fuentes de Datos (Estado Actual)
| Fuente | Estado | Anuncios |
| :--- | :--- | :--- |
| **Dongfeng (Sitio especializado)** | 40 |
| **Revolico (Sitios de anuncios)** | 80 |
| **Grupos/Canales** | 19 |
| **Entrevistas** | 9 |

## Estructura del Repositorio
- Scripts de scraping (Python)
- Datos crudos y limpios (CSV)
- Cuaderno de análisis (Jupyter Notebook)
- Entrevistas y encuestas 
- Análisis Exploretario 

##  Estructura del Repositorio
- `code/`: Scripts de Python (`.py`) documentados línea por línea y el cuaderno de Jupyter (`.ipynb`).
- `historia/`: Documentación del progreso, incluyendo la historia del proyecto y la lista de commits (`commits.md`).
- `opencode/`: Registros de los *Handoffs* y *Journeys* (prompts y soluciones generadas con IA).

## Tecnologías y Herramientas Utilizadas
- **Python** (Pandas, BeautifulSoup, Requests, curl_cffi)
- **Jupyter Notebook** para el análisis exploratorio (EDA).
- **OpenCode** (IA) para la generación y depuración de código de scraping.
- **Git / GitHub** para el control de versiones.

## 🚀 Próximos Pasos
1. Agregar una entrevistas importante para el proyecto 
3. Actualizar gráficos avanzados y análisis exploratorio de los 123 vehículos.
4. Entrenar un modelo de Machine Learning para predecir precios

## Conclusiones del Análisis Exploratorio (EDA)

A partir de la extracción de más de 150 registros (entre anuncios de Revolico, AutoCubana, Telegram, Dongfeng y entrevistas a vendedores y mecánicos), se llegaron a las siguientes conclusiones:

1.  **Relación Año-Precio:** Existe una correlación positiva clara. A mayor año de fabricación, mayor es el precio. Sin embargo, el mercado presenta "valores atípicos" (autos con sobreprecio) debido a marcas de lujo o modelos específicos que rompen esta tendencia.
2.  **Distribución de Precios:** El mercado está fuertemente sesgado hacia la izquierda. El precio promedio general es de ~$14,000 USD, pero la mayoría de los anuncios se concentran en rangos económicos (menos de $10,000). Los autos de lujo inflan la media artificialmente.
3.  **Distribución Geográfica:** Existe una gran cantidad de datos en la categoría "Desconocida" porque muchas plataformas no solicitan la provincia. Entre las provincias registradas, **La Habana** domina la oferta, seguida de Holguín y Matanzas.
4.  **Precios por Marca:** Según los datos extraídos, **Hyundai** tiene el precio promedio más alto en el mercado (superando los $30,000 USD), seguido de Kia. Esto contrasta con la opinión técnica, que sitúa a **Toyota** como la marca más confiable y duradera, pero con precios promedio más moderados en el mercado de segunda mano.

## Limitaciones y Trabajo Futuro
- **Limpieza de datos:** Se requiere separar los vehículos de las motos (Yamaha, Kawasaki) en los análisis de precio.
- **Geolocalización:** Es necesario mejorar la extracción de provincias desde la descripción cruda en futuras iteraciones.
- **Modelado:** Con la base de datos actual, el siguiente paso es entrenar un modelo predictivo (Regresión Lineal) para estimar el precio de un auto en función de su año, marca y estado.

Se intentó entrenar un modelo de Regresión Lineal para predecir el precio de los autos basándose en su Año y Marca. Sin embargo, el modelo arrojó un Error Absoluto Medio (MAE) de ~$36,843 USD y un R² de `nan`.

**¿Por qué falló el modelo y qué aprendimos?**
1. **Volumen de datos:** Con ~170 registros, la muestra es demasiado pequeña para que un modelo de Machine Learning generalice correctamente.
2. **Outliers (Valores Atípicos):** La presencia de autos de lujo (ej. $99,000 USD) junto a autos muy económicos (ej. $2,000 USD) distorsiona la línea de regresión.
3. **Calidad de datos:** Muchos registros tienen marcas "Desconocidas" o precios no especificados.

**Conclusión técnica:** Para la siguiente fase del proyecto, es necesario ampliar el dataset a más de 1,000 registros, limpiar los outliers y aplicar modelos más complejos como *Random Forest*.

##  Conclusión Final del Proyecto

Tras el análisis exploratorio y el modelado predictivo, respondemos a la pregunta de investigación:

**1. ¿Qué relación existe entre las características y el precio?**
El **Año de fabricación** es la variable más determinante (aporta un 55.5% al modelo predictivo). Le sigue la **Marca**, destacando Hyundai (33.9%) y Kia (9.2%) como las marcas que más empujan el precio hacia arriba en el mercado cubano. 

**2. ¿Cómo pueden estas variables predecir el precio?**
Se entrenó un modelo de *Random Forest* (Bosque Aleatorio). Aunque el modelo presentó un alto margen de error (MAE de $15,000 USD) debido a la alta volatilidad y datos atípicos del mercado informal cubano (carros con sobreprecio, falta de datos de kilometraje, etc.), **el algoritmo logró identificar con éxito la jerarquía de las variables**.

**3. Conclusiones de las fuentes cualitativas:**
Las entrevistas a vendedores y mecánicos revelaron que el precio en Cuba no es solo una fórmula matemática. Influyen factores externos como:
- La facilidad de conseguir repuestos (Toyota y Hyundai son las más buscadas).
- El estado de las vías (daño constante en la dirección).
- La crisis energética (preferencia por combustión vs. eléctricos).
- Los "papeles" legales del vehículo.

**4. Aprendizaje del proyecto:**
El mercado automotriz cubano es un ecosistema único y altamente complejo. Para futuras iteraciones del modelo predictivo, se requeriría un dataset de más de 1,000 registros, la inclusión del estado de conservación y la conversión de "papeles" a variables numéricas.

