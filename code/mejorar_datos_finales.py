import pandas as pd

print("Mejorando la calidad del dataset...")
df = pd.read_csv('data/PROYECTO_AUTOS_DATASET_OFICIAL.csv')

# 1. Limpiar precios y años
df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
df['Anio'] = pd.to_numeric(df['Anio'], errors='coerce')

# 2. Rellenar "Papeles" si dice "particular" en la descripción
def buscar_papeles(texto):
    if pd.isna(texto): return 'Desconocido'
    texto = str(texto).lower()
    if 'particular' in texto: return 'Particular'
    if 'estatal' in texto or 'estado' in texto: return 'Estatal'
    return 'Desconocido'

df['Papeles'] = df.apply(lambda row: buscar_papeles(row['Descripcion_Cruda']) if row['Papeles'] == 'Desconocido' else row['Papeles'], axis=1)

# 3. Rellenar "Combustible" si lo menciona en el texto
def buscar_combustible(texto):
    if pd.isna(texto): return 'Desconocido'
    texto = str(texto).lower()
    if 'eléctrico' in texto or 'electrico' in texto: return 'Eléctrico'
    if 'híbrido' in texto or 'hibrido' in texto: return 'Híbrido'
    if 'diésel' in texto or 'diesel' in texto: return 'Diésel'
    if 'gasolina' in texto: return 'Gasolina'
    return 'Desconocido'

df['Combustible'] = df['Descripcion_Cruda'].apply(buscar_combustible)

# 4. GUARDAMOS TODO (Sin borrar filas)
df.to_csv('data/DATASET_PARA_GRAFICOS.csv', index=False)

print(f"✅ Datos mejorados.")
print(f"Total de registros listos para graficar: {len(df)} registros.")
