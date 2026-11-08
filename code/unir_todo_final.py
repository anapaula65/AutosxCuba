import pandas as pd

print("Iniciando unificación de todas las fuentes...")

# 1. Cargar los archivos individuales
try:
    df_revolico = pd.read_csv('data/revolico_80_anuncios.csv')
    print("✅ Revolico cargado")
except: print("❌ Error cargando Revolico")

try:
    df_dongfeng = pd.read_csv('data/dongfeng_cuba_catalogo.csv')
    print("✅ Dongfeng cargado")
except: print("❌ Error cargando Dongfeng")

try:
    df_telegram = pd.read_csv('data/telegram_autos.csv')
    print("✅ Telegram cargado")
except: print("❌ Error cargando Telegram")

try:
    df_entrevistas = pd.read_csv('data/entrevistas_estructuradas.csv')
    print("✅ Entrevistas cargadas")
except: print("❌ Error cargando Entrevistas")

try:
    df_autocubana = pd.read_csv('data/autocubana_autos_limpio.csv')
    print("✅ AutoCubana cargado")
except: print("❌ Error cargando AutoCubana")

# 2. Unir todos los DataFrames
df_final = pd.concat([df_revolico, df_dongfeng, df_telegram, df_entrevistas, df_autocubana], ignore_index=True)

# 3. Eliminar duplicados exactos
df_final = df_final.drop_duplicates(subset=['Descripcion_Cruda', 'Precio'], keep='first')

# 4. Guardar el archivo definitivo
df_final.to_csv('data/PROYECTO_AUTOS_DATASET_OFICIAL.csv', index=False)

print(f"\n🎉 ¡ÉXITO! El dataset final tiene {len(df_final)} registros.")
print("Archivo guardado como: data/PROYECTO_AUTOS_DATASET_OFICIAL.csv")
