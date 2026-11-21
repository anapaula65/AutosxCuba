# 🚗 Análisis del Mercado Automotriz en Cuba
### Proyecto de Introducción a la Ciencia de Datos
**Estudiante:** Ana Paula González Gómez  
**Fecha:** Noviembre 2026  

---

## 🎯 1. Pregunta de Investigación
¿Qué relación existe entre las características técnicas y comerciales de los vehículos (como potencia, antigüedad, kilometraje, combustible) y su precio de venta en el mercado cubano, y cómo pueden estas variables utilizarse para predecir el precio de un automóvil?

## 📊 2. Metodología y Fuentes de Datos
Para responder a esta interrogante, se extrajeron más de **170 registros** de 5 fuentes distintas, garantizando un enfoque multi-actor:
1. **Revolico (80 anuncios):** Mercado informal (compra-venta particular).
2. **Dongfeng Cuba (~40 vehículos):** Catálogo oficial estatal (vehículos nuevos).
3. **AutoCubana (24 anuncios):** Portal especializado de clasificados.
4. **Telegram (19 anuncios):** Grupos de compra-venta en redes sociales.
5. **Entrevistas:** A vendedores (particulares/mypimes) y a un **mecánico técnico**.

*(Nota: Las evidencias de las entrevistas, fotos de los vehículos y grabaciones de audio se encuentran adjuntas en la carpeta `data/evidencias/` del proyecto).*

---

## 📈 3. Análisis Exploratorio de Datos (EDA) y Conclusiones

### 3.1 Distribución y Relación de Precios
- **Análisis:** Existe una alta dispersión en los precios. El promedio general es de ~$14,000 USD, pero el mercado está sesgado: la mayoría de los cubanos compran autos económicos (menos de $10,000), mientras que los autos de lujo inflan la media hacia arriba.
- **Conclusión:** El **Año de fabricación** es un factor determinante (correlación positiva), pero los precios atípicos indican que factores como los "papeles" o el estado real del vehículo pesan más que la simple matemática.

![Histograma de Precios](data/graficos/01_histograma_precios.png)
![Relación Año vs Precio](data/graficos/03_anio_vs_precio.png)

### 3.2 Preferencias del Mercado (Marcas y Modelos)
- **Análisis:** En el mercado de anuncios, **Hyundai** (con un 33.9% de peso) y **Kia** (9.2%) dominan los precios más altos. Sin embargo, el análisis cualitativo revela la verdadera preferencia: **Toyota** es la marca más confiable según los mecánicos.
- **Conclusión:** El mercado valora la **disponibilidad de repuestos**. Marcas como MG son evitadas por falta de piezas, mientras que Kia y Hyundai son las más fáciles de reparar.

![Top Marcas](data/graficos/02_top_marcas.png)
![Top Modelos](data/graficos/06_top_modelos.png)

### 3.3 El Factor Cubano: Combustible y Geografía
- **Análisis:** Casi el **68% de los datos recopilados son de vehículos eléctricos** (debido al sesgo de la fuente Dongfeng). Sin embargo, las entrevistas revelan que la crisis eléctrica del país frena la demanda real de estos vehículos. Geográficamente, **La Habana** concentra la gran mayoría de la oferta.
- **Conclusión:** Existe una brecha entre la oferta estatal (eléctricos) y la demanda real (combustión).

![Tipos de Combustible](data/graficos/05_tipos_combustible.png)
![Provincias](data/graficos/04_provincias.png)

---

## 🤖 4. Modelado Predictivo (Machine Learning)
Se entrenó un modelo de **Random Forest Regressor** para predecir el precio en función del Año y la Marca.

- **Resultados:** El modelo presentó un Error Absoluto Medio (MAE) de $15,062 USD, lo que indica que el mercado es altamente volátil.
- **Hallazgo principal (Feature Importance):** El modelo logró identificar que el **Año** explica el **55.5%** del precio, seguido de la marca **Hyundai (33.9%)** y **Kia (9.2%)**.

---

## 🗣️ 5. Conclusiones Cualitativas (Entrevistas)
Las entrevistas (incluyendo al mecánico) revelaron que el precio de un auto en Cuba no es solo una fórmula:
- **Los baches dañan la dirección:** El mecánico indicó que lo que más se repara es la cremallera.
- **Umbral de fallas:** Los carros comienzan a dar problemas graves después de los 200,000 km.
- **Repuestos:** Las reparaciones se encarecen porque las piezas son importadas.

---
