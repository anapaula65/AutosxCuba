
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('data/graficos', exist_ok=True)
sns.set_theme(style="whitegrid")

print("Cargando dataset...")
df = pd.read_csv('data/DATASET_PARA_GRAFICOS.csv')
df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
df['Anio'] = pd.to_numeric(df['Anio'], errors='coerce')

# ==========================================
# FILTRO MAESTRO: Solo autos con precios lógicos (1000 a 60,000 USD)
# ==========================================
df_real = df[(df['Precio'] >= 1000) & (df['Precio'] <= 60000)].copy()

# ==========================================
# GRÁFICO 1: Histograma de Precios (Realista)
# ==========================================
print("Generando Gráfico 1...")
plt.figure(figsize=(12, 6))
sns.histplot(data=df_real, x='Precio', bins=20, kde=True, color='skyblue')
plt.axvline(df_real['Precio'].median(), color='red', linestyle='--', label=f'Mediana: ${df_real["Precio"].median():,.0f}')
plt.title('Distribución de Precios Reales en el Mercado (Sin autos de lujo)', fontsize=15)
plt.xlabel('Precio (USD)')
plt.ylabel('Cantidad de Anuncios')
plt.legend()
plt.tight_layout()
plt.savefig('data/graficos/01_histograma_precios.png')
plt.close()

# ==========================================
# GRÁFICO 2: Top 10 Marcas (Precio Promedio Realista)
# ==========================================
print("Generando Gráfico 2...")
df_marcas = df_real[(df_real['Marca'] != 'Desconocida') & (df_real['Marca'] != 'Desconocido')]
plt.figure(figsize=(12, 6))
precio_por_marca = df_marcas.groupby('Marca')['Precio'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=precio_por_marca.values, y=precio_por_marca.index, palette='viridis')
plt.title('Top 10 Marcas por Precio Promedio (Rango Normal de Mercado)', fontsize=15)
plt.xlabel('Precio Promedio (USD)')
plt.ylabel('Marca')
plt.tight_layout()
plt.savefig('data/graficos/02_top_marcas.png')
plt.close()

# ==========================================
# GRÁFICO 3: Año vs Precio (Solo autos lógicos)
# ==========================================
print("Generando Gráfico 3...")
df_anio = df_real[(df_real['Anio'] > 1990)]
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df_anio, x='Anio', y='Precio', hue='Fuente', s=100, alpha=0.7)
plt.title('Relación entre Año del Auto y su Precio (Mercado Real)', fontsize=15)
plt.xlabel('Año')
plt.ylabel('Precio (USD)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('data/graficos/03_anio_vs_precio.png')
plt.close()

# ==========================================
# GRÁFICO 4: Provincias
# ==========================================
print("Generando Gráfico 4...")
df_prov = df[(df['Provincias'] != 'Desconocida') & (df['Provincias'] != 'Desconocido')]
plt.figure(figsize=(12, 6))
provincias = df_prov['Provincias'].value_counts().head(10)
sns.barplot(x=provincias.values, y=provincias.index, palette='magma')
plt.title('Top 10 Provincias con Más Anuncios', fontsize=15)
plt.xlabel('Cantidad de Anuncios')
plt.ylabel('Provincia')
plt.tight_layout()
plt.savefig('data/graficos/04_provincias.png')
plt.close()

# ==========================================
# GRÁFICO 5: Combustible (FILTRADO SIN DONGEFENG PARA VER LA REALIDAD)
# ==========================================
print("Generando Gráfico 5...")
plt.title('Oferta de Vehículos por Tipo de Combustible en el Mercado', fontsize=15)
df_comb = df[(df['Combustible'] != 'Desconocido') & (df['Fuente'] != 'Dongfeng')]
if not df_comb.empty:
    plt.figure(figsize=(8, 8))
    colores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    df_comb['Combustible'].value_counts().plot.pie(autopct='%1.1f%%', colors=colores, startangle=90)
    plt.title('Combustible Preferido en el Mercado de Usados (Sin Dongfeng)', fontsize=15)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('data/graficos/05_tipos_combustible.png')
    plt.close()

print("✅ ¡Los 5 gráficos se han regenerado con filtros realistas!")
