import os
import shutil
import glob
import html

carpeta_web = 'Sitio_Web_Proyecto'
os.makedirs(carpeta_web, exist_ok=True)
os.makedirs(f'{carpeta_web}/img/graficos', exist_ok=True)
os.makedirs(f'{carpeta_web}/img/fotos', exist_ok=True)
os.makedirs(f'{carpeta_web}/audio', exist_ok=True)

print("Copiando archivos multimedia...")
if os.path.exists('data/graficos'):
    for f in glob.glob('data/graficos/*.png'):
        shutil.copy(f, f'{carpeta_web}/img/graficos/')

if os.path.exists('data/evidencias/fotos'):
    for f in glob.glob('data/evidencias/fotos/*.*'):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            shutil.copy(f, f'{carpeta_web}/img/fotos/')

if os.path.exists('data/evidencias/audios'):
    for f in glob.glob('data/evidencias/audios/*.*'):
        if f.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg')):
            shutil.copy(f, f'{carpeta_web}/audio/')

def plantilla_html(titulo, contenido):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo} - AutosxCuba 🇨🇺</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #f4f7f6; color: #333; }}
            header {{ background-color: #1a252f; color: white; padding: 20px; text-align: center; }}
            nav {{ background-color: #2c3e50; display: flex; justify-content: center; flex-wrap: wrap; }}
            nav a {{ color: white; padding: 15px 20px; text-decoration: none; font-weight: bold; }}
            nav a:hover {{ background-color: #1abc9c; }}
            .container {{ max-width: 1100px; margin: 30px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h2 {{ color: #2980b9; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            .grafico {{ text-align: center; margin: 40px 0; padding: 20px; background: #f9f9f9; border-radius: 8px; border-left: 5px solid #3498db; }}
            .grafico img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); margin-bottom: 15px; }}
            .explicacion {{ text-align: left; font-size: 1rem; color: #444; line-height: 1.6; }}
            .foto-galeria {{ display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 20px; }}
            .foto-galeria img {{ width: 300px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
            audio {{ width: 100%; margin-top: 10px; margin-bottom: 20px; }}
            pre {{ background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 14px; line-height: 1.4; }}
            .conclusion-box {{ background: #e8f8f5; padding: 20px; border-radius: 8px; border-left: 5px solid #1abc9c; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <header>
            <h1>🚗 AutosxCuba 🇨🇺</h1>
            <p>Análisis del Mercado Automotriz - Ana Paula González Gómez</p>
        </header>
        <nav>
            <a href="index.html">Inicio</a>
            <a href="graficos.html">Análisis Visual</a>
            <a href="entrevistas.html">Evidencias y Resultados</a>
            <a href="historia.html">Metodología y Conclusiones</a>
            <a href="codigo.html">Código Fuente</a>
        </nav>
        <div class="container">
            <h2>{titulo}</h2>
            {contenido}
        </div>
    </body>
    </html>
    """

# --- PÁGINA DE INICIO ---
inicio = """
<p>Bienvenido al reporte interactivo del proyecto <strong>AutosxCuba</strong>. Usa el menú superior para navegar.</p>

<div class="conclusion-box" style="border-left-color: #e74c3c; background-color: #fdedec;">
    <h3>💡 Hallazgo Principal del Proyecto</h3>
    <p><em>"El análisis reveló una discrepancia entre la oferta y la demanda. Los gráficos de scraping muestran que el 54% de los autos a la venta son eléctricos (una oferta inflada por las importaciones). Sin embargo, el análisis cualitativo de las entrevistas demuestra que la demanda real prefiere la gasolina por los problemas de electricidad. Esta desconexión indica que el mercado de eléctricos en Cuba está sobreofertado o que los dueños los están revendiendo por falta de infraestructura para cargarlos."</em></p>
</div>

<h3>Resumen de Fuentes:</h3>
<table style="width:100%; border-collapse: collapse; text-align:left;">
    <tr style="background:#ecf0f1;"><th style="padding:10px;">Fuente</th><th>Estado</th><th>Cantidad</th></tr>
    <tr><td style="padding:10px;">Revolico</td><td>✅ Completado</td><td>80 anuncios</td></tr>
    <tr><td style="padding:10px;">Dongfeng</td><td>✅ Completado</td><td>~40 modelos</td></tr>
    <tr><td style="padding:10px;">AutoCubana</td><td>✅ Completado</td><td>24 anuncios</td></tr>
    <tr><td style="padding:10px;">Telegram</td><td>✅ Completado</td><td>19 mensajes</td></tr>
    <tr><td style="padding:10px;">Entrevistas</td><td>✅ Completado</td><td>15 entrevistas</td></tr>
</table>
"""

# --- PÁGINA DE GRÁFICOS ---
explicaciones = {
    '01_histograma_precios.png': 'El mercado está fuertemente sesgado. La mayoría de los autos se concentran en rangos económicos (menos de $15,000 USD), pero la presencia de autos de lujo infla el promedio. <strong>Conclusión:</strong> La mediana es una medida más representativa del valor real de los vehículos en Cuba que el promedio.',
    '02_top_marcas.png': 'Hyundai, Kia y Toyota dominan abrumadoramente la oferta del mercado. <strong>Conclusión:</strong> Existe una clara preferencia del consumidor por marcas con alta disponibilidad de repuestos, lo que genera una mayor rotación y oferta de estas marcas en el mercado informal.',
    '03_anio_vs_precio.png': 'Se observa una clara correlación positiva: a mayor año, mayor precio. Sin embargo, se identifican "outliers" (valores atípicos) de autos muy nuevos con precios desproporcionados que rompen la tendencia lineal. <strong>Conclusión:</strong> El año de fabricación explica más del 50% del valor del auto.',
    '04_provincias.png': 'Existe una alta concentración de datos en "Desconocida" porque muchas plataformas no solicitan la provincia. Entre las registradas, La Habana domina la oferta, seguida de Holguín y Matanzas. <strong>Conclusión:</strong> El mercado está centralizado en la capital, aunque hay falta de datos geográficos formales.',
    '05_tipos_combustible.png': 'Aproximadamente el 54% de la oferta son vehículos eléctricos. <strong>Conclusión Crítica:</strong> Existe una gran paradoja entre la oferta y la demanda. Aunque los datos muestran una alta oferta de eléctricos, las entrevistas revelan que la demanda real sigue prefiriendo la combustión por la crisis energética. Esto sugiere que el mercado de eléctricos está sobreofertado o que los dueños los revenden por falta de infraestructura para cargarlos.'
}

graficos_html = ""
for img, texto in explicaciones.items():
    ruta_img = f'img/graficos/{img}'
    if os.path.exists(f'{carpeta_web}/{ruta_img}'):
        graficos_html += f"""
        <div class="grafico">
            <img src="{ruta_img}" alt="{img}">
            <div class="explicacion"><strong>Análisis:</strong> {texto}</div>
        </div>
        """

graficos_html += """
<div class="conclusion-box">
    <h3>Conclusiones Generales del Análisis Visual</h3>
    <ul>
        <li><strong>Relación Año-Precio:</strong> Existe una correlación positiva clara, aunque distorsionada por autos de lujo (outliers).</li>
        <li><strong>Sesgo de las fuentes:</strong> La oferta estatal (Dongfeng) empuja la balanza hacia los eléctricos, mientras que el mercado informal (Revolico/Telegram) se inclina más por la combustión.</li>
        <li><strong>Factores cualitativos:</strong> El precio en Cuba no depende solo del año y la marca, sino de los "papeles", el estado de la dirección (por los baches) y la disponibilidad de repuestos.</li>
    </ul>
</div>
"""

# --- PÁGINA DE EVIDENCIAS Y RESULTADOS ---
evidencias_html = "<p>Evidencias recolectadas que garantizan la veracidad de los datos.</p>"

fotos = glob.glob(f'{carpeta_web}/img/fotos/*.*')
if fotos:
    evidencias_html += "<h3>📸 Fotos y Capturas de los Anuncios:</h3><div class='foto-galeria'>"
    for foto in fotos:
        nombre = os.path.basename(foto)
        evidencias_html += f"<img src='img/fotos/{nombre}' alt='{nombre}'>"
    evidencias_html += "</div>"
else:
    evidencias_html += "<p><em>(No se encontraron fotos en la carpeta).</em></p>"

audios = glob.glob(f'{carpeta_web}/audio/*.*')
evidencias_html += "<h3>🎙️ Audios de Entrevistas:</h3>"
if audios:
    for audio in audios:
        nombre = os.path.basename(audio)
        evidencias_html += f"<p><strong>{nombre}</strong></p><audio controls><source src='audio/{nombre}' type='audio/mpeg'></audio>"
else:
    evidencias_html += "<p><em>(No se encontraron audios en la carpeta).</em></p>"

# --- NUEVO BLOQUE DE RESULTADOS FINALES ---
evidencias_html += """
<div class="conclusion-box" style="background-color: #fcf3cf; border-left-color: #f1c40f; margin-top: 40px;">
    <h3>🏆 La Evidencia y el Análisis Final (Resultados)</h3>
    <p>El proyecto no se detuvo en la recolección. Con más de <strong>170 vehículos extraídos</strong> y documentados, llegó el momento de la verdad. El análisis de datos reveló:</p>
    <ul>
        <li><strong>La hegemonía de Hyundai y Kia:</strong> Son las marcas con mayor presencia y precios promedios más altos, demostrando la preferencia por durabilidad y repuestos.</li>
        <li><strong>La paradoja Oferta-Demanda:</strong> Existe un sesgo hacia los vehículos eléctricos en las ofertas (54%), frente a una preferencia real de los compradores por la combustión debido a la crisis energética.</li>
        <li><strong>La realidad del asfalto:</strong> Los baches cubanos dañan principalmente la dirección de los autos (cremalleras), lo que afecta directamente su valor de reventa.</li>
    </ul>
    <p>Finalmente, el modelo de <strong>Machine Learning (Random Forest)</strong> logró cuantificar que el <strong>Año de fabricación (55.5%)</strong> y la <strong>Marca (Hyundai 33.9%)</strong> son los factores que más pesan al predecir un precio.</p>
</div>
"""

# --- PÁGINA DE HISTORIA Y MODELO ---
historia_html = """
<h3>Metodología del Modelo Predictivo: Random Forest</h3>
<p>Para responder a la pregunta de investigación, implementamos un modelo de <strong>Random Forest Regressor</strong> (Bosque Aleatorio).</p>
<p><strong>¿Por qué se utilizó este modelo?</strong> El mercado automotriz cubano presenta una altísima volatilidad. Los modelos lineales simples se confunden fácilmente ante la presencia de autos de lujo con precios desproporcionados. El Random Forest crea cientos de "árboles de decisión" que votan en conjunto, haciéndolo robusto ante valores atípicos.</p>
<p><strong>Importancia de las variables (Feature Importance):</strong></p>
<ul>
    <li><strong>Año de fabricación (55.5%):</strong> Es el factor número uno que define el precio.</li>
    <li><strong>Marca Hyundai (33.9%):</strong> Empuja significativamente el precio hacia arriba.</li>
    <li><strong>Marca Kia (9.2%):</strong> Influye en menor medida.</li>
</ul>

<div class="conclusion-box">
    <h3>Conclusiones Finales de la Investigación</h3>
    <p>A partir del análisis de más de 170 registros y 15 entrevistas, concluimos que:</p>
    <ol>
        <li><strong>El año y la marca son los pilares del precio:</strong> La antigüedad explica más del 50% del valor de un auto en Cuba.</li>
        <li><strong>La durabilidad manda:</strong> Marcas como Toyota y Hyundai son las más buscadas porque los mecánicos confirman que tienen mayor disponibilidad de repuestos.</li>
        <li><strong>El entorno destruye valor:</strong> El mal estado de las calles (baches) provoca daños constantes en la dirección y suspensión, afectando el valor real del vehículo.</li>
        <li><strong>Transición energética condicionada:</strong> Aunque los sitios oficiales ofrecen mayoritariamente autos eléctricos, la crisis eléctrica hace que los compradores sigan prefiriendo la combustión.</li>
    </ol>
    
    <h4 style="color: #c0392b; margin-top: 20px;">🔍 Paradoja Oferta-Demanda</h4>
    <p><em>"Los gráficos muestran que el 54% de los autos a la venta son eléctricos. Sin embargo, las entrevistas demuestran que la demanda real prefiere la gasolina. Esta desconexión indica que el mercado de eléctricos está sobreofertado o que los dueños los revenden por falta de infraestructura para cargarlos."</em></p>
</div>
"""

# --- PÁGINA DE CÓDIGO FUENTE ---
codigo_html = "<p>Aquí se presentan todos los scripts de Python desarrollados para el proyecto.</p>"
archivos_py = sorted(glob.glob('code/*.py'))
for archivo in archivos_py:
    nombre = os.path.basename(archivo)
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = html.escape(f.read())
        codigo_html += f"<h3>📄 {nombre}</h3><pre><code>{contenido}</code></pre><hr>"
    except Exception as e:
        codigo_html += f"<p>Error al leer {nombre}</p>"

# --- GUARDAR PÁGINAS ---
with open(f'{carpeta_web}/index.html', 'w', encoding='utf-8') as f: f.write(plantilla_html("Inicio", inicio))
with open(f'{carpeta_web}/graficos.html', 'w', encoding='utf-8') as f: f.write(plantilla_html("Análisis Visual", graficos_html))
with open(f'{carpeta_web}/entrevistas.html', 'w', encoding='utf-8') as f: f.write(plantilla_html("Evidencias y Resultados", evidencias_html))
with open(f'{carpeta_web}/historia.html', 'w', encoding='utf-8') as f: f.write(plantilla_html("Metodología y Conclusiones", historia_html))
with open(f'{carpeta_web}/codigo.html', 'w', encoding='utf-8') as f: f.write(plantilla_html("Código Fuente", codigo_html))

print("✅ ¡Sitio web 'AutosxCuba' generado con éxito y actualizado con las conclusiones finales!")
print("👉 Abre 'Sitio_Web_Proyecto/index.html' en tu navegador para revisar los cambios.")
