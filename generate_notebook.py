import json

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }

cells = []

# 1. Introducción y Arquitectura
cells.append(create_markdown_cell("""# Proyecto: Análisis Predictivo y Modelamiento de Sistema de Control de Acceso RFID
**Ingeniería de Machine Learning, Ciencia de Datos e Ingeniería Informática**

Este proyecto analiza el flujo de personas basado en datos históricos de un sistema RFID, empleando **Machine Learning** y **Modelamiento Matemático**.

## 1. Arquitectura del Sistema
El flujo de la información se estructura de la siguiente manera:
1. **Hardware (Arduino + RFID):** Captura de eventos físicos (Usuario, UID, Fecha, Hora).
2. **Almacenamiento (Base de Datos / Excel):** Registro estructurado de eventos temporales.
3. **Procesamiento (Python):** Preprocesamiento y limpieza de datos (Pandas/NumPy).
4. **Inteligencia Artificial (Machine Learning):** Detección de patrones y modelado predictivo (Scikit-Learn/XGBoost).
5. **Predicción y Acción:** Estimación de congestiones y comportamiento en un entorno de *Smart Campus*."""))

# 2. Instalación de dependencias
cells.append(create_markdown_cell("""## 2. Preparación del Entorno
Ejecuta la siguiente celda para asegurarte de tener instaladas todas las librerías necesarias para el análisis de datos, visualización y machine learning."""))

cells.append(create_code_cell("""# Instalar librerías requeridas (si no están instaladas)
!pip install pandas numpy matplotlib seaborn scikit-learn plotly openpyxl"""))

# 3. Importar librerías
cells.append(create_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import os
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")"""))

# 4. Modelamiento Matemático
cells.append(create_markdown_cell("""## 3. Modelamiento Matemático

En sistemas dinámicos de control de acceso, podemos analizar el flujo de personas mediante ecuaciones diferenciales.

### Flujo de Personas en el Sistema
Sea $N(t)$ el número de personas dentro del recinto en el tiempo $t$.
La variación de personas respecto al tiempo está dada por la ecuación diferencial:
$$ \\frac{dN}{dt} = \lambda - \mu $$

Donde:
* $\lambda$: Tasa de entrada (personas que ingresan por unidad de tiempo).
* $\mu$: Tasa de salida (personas que abandonan el recinto por unidad de tiempo).

Si $\lambda > \mu$, el recinto experimenta acumulación (congestión). Si $\lambda < \mu$, el recinto se está vaciando.

### Crecimiento del Almacenamiento de Datos
El volumen de registros generados por los lectores RFID ($C$) tiende a crecer proporcionalmente al número de transacciones o al tamaño actual si cada transacción genera metadatos encadenados:
$$ \\frac{dC}{dt} = k C $$
La solución a esta ecuación es $C(t) = C_0 e^{kt}$, lo que indica un crecimiento exponencial de los datos. Esto subraya la importancia de la **limpieza de datos (Data Preprocessing)** y estrategias de **Big Data** para evitar la saturación del sistema."""))

# 5. Preprocesamiento y Generación de Datos
cells.append(create_markdown_cell("""## 4. Preprocesamiento de Datos (Data Preprocessing)

En esta sección leeremos el archivo `registros_rfid.xlsx` generado por el sistema RFID.
* **Nota:** Si el archivo no tiene suficientes registros históricos para entrenar un modelo robusto (por ejemplo, si el sistema es nuevo), generaremos automáticamente **datos sintéticos** basados en patrones reales de un *Smart Campus* para garantizar el correcto funcionamiento del análisis predictivo."""))

cells.append(create_code_cell("""def load_or_generate_data(file_path='registros_rfid.xlsx', num_synthetic_records=5000):
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            if len(df) > 100: # Si hay suficientes datos
                print(f"Datos reales cargados: {len(df)} registros encontrados.")
                return df
            else:
                print("El archivo real tiene muy pocos datos. Generando datos sintéticos para el análisis predictivo...")
        except Exception as e:
            print(f"Error al leer {file_path}: {e}. Generando datos sintéticos...")
    else:
        print(f"Archivo {file_path} no encontrado. Generando datos sintéticos...")

    # Generación de Datos Sintéticos para propósitos académicos
    np.random.seed(42)
    users = [f"User_{i:03d}" for i in range(1, 51)]
    uids = [f"{np.random.randint(1000,9999):04x}".upper() for _ in range(50)]
    user_uid_map = dict(zip(users, uids))

    start_date = datetime.now() - timedelta(days=90)
    data = []
    
    for _ in range(num_synthetic_records):
        user = np.random.choice(users)
        uid = user_uid_map[user]
        # Distribuir aleatoriamente en los últimos 90 días, favoreciendo horas de 7am a 8pm
        days_offset = np.random.randint(0, 90)
        hour = int(np.random.normal(12, 4)) # Media 12pm, Desv 4
        hour = max(0, min(23, hour))
        minute = np.random.randint(0, 60)
        
        event_time = start_date + timedelta(days=days_offset, hours=hour, minutes=minute)
        date_str = event_time.strftime("%Y-%m-%d")
        time_str = event_time.strftime("%H:%M:%S")
        
        tipo_acceso = np.random.choice(["Entrada", "Salida"], p=[0.55, 0.45])
        estado = np.random.choice(["Permitido", "Denegado"], p=[0.95, 0.05])
        
        data.append([user, uid, date_str, time_str, tipo_acceso, estado])

    df = pd.DataFrame(data, columns=["Usuario", "UID", "Fecha", "Hora", "Tipo de acceso", "Estado"])
    
    # Exportar para usar luego
    df.to_csv("rfid_datos_sinteticos.csv", index=False)
    return df

df_raw = load_or_generate_data()

# 1. Limpiar datos nulos
df = df_raw.dropna().copy()

# 2. Convertir fechas y horas a formato datetime
df['Datetime'] = pd.to_datetime(df['Fecha'].astype(str) + ' ' + df['Hora'].astype(str))

# 3. Crear variables temporales
df['hora'] = df['Datetime'].dt.hour
df['dia'] = df['Datetime'].dt.day
df['dia_semana'] = df['Datetime'].dt.dayofweek # 0=Lunes, 6=Domingo
df['mes'] = df['Datetime'].dt.month
df['fecha_corta'] = df['Datetime'].dt.date

print("\\n--- Estadísticas Básicas ---")
print(df.describe(include='all', datetime_is_numeric=True))

df.head()"""))

# 6. EDA
cells.append(create_markdown_cell("""## 5. Análisis Exploratorio de Datos (EDA)

Realizamos visualizaciones profesionales para entender el flujo temporal, las horas pico y el comportamiento de los usuarios en el sistema."""))

cells.append(create_code_cell("""# 1. Flujo de Personas por Hora
plt.figure(figsize=(12, 6))
sns.countplot(data=df[df['Estado'] == 'Permitido'], x='hora', hue='Tipo de acceso', palette='viridis')
plt.title('Flujo de Personas por Hora (Entradas vs Salidas)', fontsize=14)
plt.xlabel('Hora del Día', fontsize=12)
plt.ylabel('Cantidad de Eventos', fontsize=12)
plt.legend(title='Tipo de Acceso')
plt.tight_layout()
plt.show()

# 2. Usuarios más frecuentes
plt.figure(figsize=(14, 6))
top_users = df['Usuario'].value_counts().head(10)
sns.barplot(x=top_users.index, y=top_users.values, palette='magma')
plt.title('Top 10 Usuarios Más Frecuentes', fontsize=14)
plt.xlabel('Usuario', fontsize=12)
plt.ylabel('Total de Accesos', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# 3. Accesos Denegados vs Permitidos (Dona)
estado_counts = df['Estado'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(estado_counts, labels=estado_counts.index, autopct='%1.1f%%', colors=['#2ca02c', '#d62728'], startangle=90)
plt.title('Proporción de Accesos: Permitidos vs Denegados', fontsize=14)
plt.show()

# 4. Comportamiento por Día de la Semana
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
flujo_dias = df.groupby('dia_semana').size().reindex(range(7), fill_value=0)

plt.figure(figsize=(10, 5))
sns.lineplot(x=dias, y=flujo_dias.values, marker='o', linewidth=2.5, color='b')
plt.title('Tráfico Total por Día de la Semana', fontsize=14)
plt.ylabel('Cantidad de Accesos')
plt.show()"""))

# 7. Machine Learning
cells.append(create_markdown_cell("""## 6. Modelamiento con Machine Learning

**Objetivo:** Predecir la cantidad de accesos (tráfico) en una hora específica basándonos en variables temporales.

Utilizaremos un modelo **Random Forest Regressor**, que es excelente para capturar relaciones no lineales en datos temporales (como patrones diarios y semanales)."""))

cells.append(create_code_cell("""# Preparar el Dataset para Machine Learning
# Agrupar datos por fecha y hora para contar la cantidad de accesos totales por hora
df_ml = df[df['Estado'] == 'Permitido'].groupby(['fecha_corta', 'mes', 'dia', 'dia_semana', 'hora']).size().reset_index(name='total_accesos')

# Variables independientes (Features) y dependiente (Target)
X = df_ml[['mes', 'dia', 'dia_semana', 'hora']]
y = df_ml['total_accesos']

# Dividir en conjunto de Entrenamiento (80%) y Prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Tamaño del set de entrenamiento: {X_train.shape[0]}")
print(f"Tamaño del set de prueba: {X_test.shape[0]}")

# Instanciar y Entrenar el Modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predecir sobre el conjunto de prueba
y_pred = model.predict(X_test)

# Guardar el modelo entrenado
with open('rfid_rf_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Modelo guardado exitosamente como 'rfid_rf_model.pkl'")"""))

# 8. Métricas
cells.append(create_markdown_cell("""## 7. Evaluación y Métricas del Modelo

Para validar matemáticamente la precisión de nuestras predicciones, calculamos:"""))

cells.append(create_code_cell("""# Cálculo de Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"✅ Error Absoluto Medio (MAE): {mae:.2f} personas")
print(f"✅ Raíz del Error Cuadrático Medio (RMSE): {rmse:.2f} personas")
print(f"✅ Coeficiente de Determinación (R² Score): {r2:.4f}")

# Visualización: Valores Reales vs Predicciones
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='purple')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2) # Línea de identidad
plt.xlabel('Accesos Reales')
plt.ylabel('Accesos Predichos')
plt.title('Desempeño del Modelo: Real vs Predicción')
plt.show()"""))

# 9. Visualizaciones Avanzadas y Predicciones
cells.append(create_markdown_cell("""## 8. Visualizaciones Avanzadas y Predicciones Futuras

### Heatmap (Mapa de Calor) de Congestión
Detectaremos las zonas de saturación horaria."""))

cells.append(create_code_cell("""# Crear Matriz Pivot para Heatmap
heatmap_data = df.groupby(['dia_semana', 'hora']).size().unstack(fill_value=0)
dias_labels = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

plt.figure(figsize=(14, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", yticklabels=dias_labels)
plt.title('Heatmap de Congestión: Día de la Semana vs Hora', fontsize=14)
plt.xlabel('Hora del Día')
plt.ylabel('Día de la Semana')
plt.show()"""))

cells.append(create_markdown_cell("""### Predicción para el "Día de Mañana"
Usando nuestro modelo entrenado, estimaremos el flujo de personas para las próximas 24 horas y alertaremos sobre posibles saturaciones."""))

cells.append(create_code_cell("""# Simular las variables para "mañana"
tomorrow = datetime.now() + timedelta(days=1)
mes_t = tomorrow.month
dia_t = tomorrow.day
dia_semana_t = tomorrow.weekday()

# Crear un DataFrame con las 24 horas de mañana
horas = list(range(24))
df_tomorrow = pd.DataFrame({
    'mes': [mes_t] * 24,
    'dia': [dia_t] * 24,
    'dia_semana': [dia_semana_t] * 24,
    'hora': horas
})

# Predecir tráfico
predicciones_manana = model.predict(df_tomorrow)

# Visualizar predicción futura
plt.figure(figsize=(12, 5))
plt.plot(horas, predicciones_manana, marker='o', linestyle='-', color='teal', linewidth=2)
plt.fill_between(horas, predicciones_manana, alpha=0.2, color='teal')
plt.title(f'Predicción de Flujo de Personas para Mañana ({tomorrow.strftime("%Y-%m-%d")})', fontsize=14)
plt.xlabel('Hora')
plt.ylabel('Cantidad de Personas Predichas')
plt.xticks(range(0, 24))
plt.grid(True)
plt.show()

# Encontrar hora pico predictiva (Posible saturación)
hora_pico = df_tomorrow.iloc[np.argmax(predicciones_manana)]['hora']
print(f"⚠️ ALERTA PREDICTIVA: La hora de mayor tráfico mañana será a las {hora_pico:02d}:00 horas, con aproximadamente {int(max(predicciones_manana))} personas.")"""))

# 10. Conclusiones
cells.append(create_markdown_cell("""## 9. Conclusiones y Arquitectura del Sistema

### Arquitectura del Flujo de Datos Revisitada
Este proyecto demuestra exitosamente la integración de un sistema embebido (Arduino/RFID) con técnicas de Inteligencia Artificial.
1. **IoT (Internet of Things):** La capa física envía tramas de datos por cada escaneo RFID.
2. **Registro e Ingesta:** Los datos se persisten en estructuras tabulares (CSV/Excel).
3. **Analítica (Python):** Se aplican principios de preprocesamiento, limpieza temporal y modelamiento de la dinámica de sistemas ($dN/dt$).
4. **Predicción Inteligente:** El algoritmo Random Forest logra encontrar patrones complejos en la no-linealidad del tráfico humano.

### Beneficios del Análisis Predictivo en Smart Campus
* **Gestión de Recursos:** Permite asignar personal de seguridad o abrir puertas adicionales en horas pico detectadas por la IA.
* **Mantenimiento Preventivo del Sistema:** Evita cuellos de botella en la autenticación del hardware.
* **Ingeniería Informática Aplicada:** Conecta los fundamentos matemáticos (ecuaciones diferenciales de flujo y crecimiento) con herramientas de vanguardia (Scikit-Learn, Pandas) en un ecosistema integral.

> *Proyecto desarrollado para demostrar competencias integrales en Sistemas Embebidos, Ciencia de Datos e Ingeniería de Machine Learning.*"""))


notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("RFID_Predictive_Analytics.ipynb", "w", encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Jupyter Notebook 'RFID_Predictive_Analytics.ipynb' generado con éxito.")
