import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

print("Cargando datos para el modelo...")
# Cargamos el dataset unificado
df = pd.read_csv('data/PROYECTO_AUTOS_DATASET_OFICIAL.csv')

# 1. Limpieza y filtrado para el modelo
df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
df['Anio'] = pd.to_numeric(df['Anio'], errors='coerce')

# Filtramos: quitamos precios en 0, menores a 1000 y mayores a 100k para que el modelo aprenda mejor
df_modelo = df[(df['Precio'] > 1000) & (df['Precio'] < 100000) & (df['Anio'] > 1990)].copy()

# 2. Definir variables predictoras (X) y la variable objetivo (y)
X = df_modelo[['Anio', 'Marca']]
y = df_modelo['Precio']

# 3. Dividir los datos en Entrenamiento (80%) y Prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Crear el Pipeline (Preprocesar texto y entrenar el modelo)
# Usamos OneHotEncoder para convertir la Marca (texto) en números
preprocesador = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), ['Marca'])],
    remainder='passthrough'
)

# Utilizamos Random Forest Regressor (Bosque Aleatorio)
modelo = Pipeline(steps=[
    ('preprocesador', preprocesador),
    ('regresor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 5. Entrenar el modelo
print("Entrenando el modelo Random Forest...")
modelo.fit(X_train, y_train)

# 6. Evaluar el modelo
y_pred = modelo.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n=== RESULTADOS DEL MODELO PREDICTIVO ===")
print(f"Error Absoluto Medio (MAE): ${mae:,.2f} USD")
print(f"Precisión del modelo (R2): {r2:.2f} (Máximo 1.0)")
print("=======================================")

# 7. Mostrar la importancia de las variables (Feature Importance)
importancias = modelo.named_steps['regresor'].feature_importances_
nombres = modelo.named_steps['preprocesador'].get_feature_names_out()

print("\nImportancia de las variables (¿Qué define el precio?):")
for nombre, imp in sorted(zip(nombres, importancias), key=lambda x: x[1], reverse=True)[:5]:
    print(f"- {nombre.replace('cat__Marca_', 'Marca: ')}: {imp*100:.1f}%")
