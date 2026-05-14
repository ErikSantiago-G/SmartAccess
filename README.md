# Análisis Predictivo y Modelamiento de Sistema de Control de Acceso RFID

Este proyecto es un sistema integral de control de acceso utilizando hardware embebido (Arduino + Módulo RFID RC522) combinado con una robusta tubería (pipeline) de **Ciencia de Datos** y **Machine Learning**. El objetivo principal es ir más allá del simple registro de entradas y salidas, implementando modelamiento matemático para el análisis de flujo y algoritmos predictivos para anticipar la congestión en un entorno de *Smart Campus* o edificio corporativo.

---

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en tres capas principales:

1. **Capa Física (Hardware IoT):** Un Arduino lee tarjetas RFID (MFRC522) y envía tramas de datos estructuradas a través del puerto serie.
2. **Capa de Ingesta (Script Python):** El script `Registro.py` se mantiene a la escucha del puerto serie, decodifica las lecturas y persiste los registros temporalmente en un archivo Excel (`registros_rfid.xlsx`).
3. **Capa Analítica y Predictiva:** El Jupyter Notebook (`RFID_Predictive_Analytics.ipynb`) toma los datos históricos, realiza limpieza, aplica modelos matemáticos y entrena un modelo de Machine Learning para predecir flujos futuros.

---

## 🧮 Modelamiento Matemático

El sistema analiza el comportamiento físico y digital mediante el uso de ecuaciones diferenciales de primer orden.

### 1. Dinámica del Flujo de Personas
Sea $N(t)$ el número de personas dentro del recinto en un instante de tiempo $t$. La variación poblacional respecto al tiempo se define por la ecuación diferencial:

$$ \frac{dN}{dt} = \lambda - \mu $$

Donde:
* **$\lambda$ (Tasa de llegada):** Cantidad de personas que registran *ENTRY* por unidad de tiempo.
* **$\mu$ (Tasa de salida):** Cantidad de personas que registran *EXIT* por unidad de tiempo.

**Análisis de Estabilidad:**
- Si **$\lambda > \mu$**, el sistema experimenta acumulación y posible congestión futura.
- Si **$\lambda < \mu$**, el recinto se está vaciando.

### 2. Crecimiento del Volumen de Datos
Cada lectura RFID genera metadatos (UID, Usuario, Fecha, Hora). El volumen de almacenamiento de la base de datos ($C$) crece proporcionalmente al número de transacciones, lo cual se modela como:

$$ \frac{dC}{dt} = k \cdot C $$

La solución analítica a esta ecuación es **$C(t) = C_0 e^{kt}$**, lo que evidencia un crecimiento de tipo exponencial en ecosistemas de Big Data, justificando la necesidad de los procesos de limpieza de datos automatizados implementados en el proyecto.

---

## 🤖 Modelo de Machine Learning

Para la analítica predictiva, el sistema utiliza un modelo de aprendizaje automático supervisado, específicamente un **Random Forest Regressor**.

### ¿Por qué Random Forest?
El tráfico humano tiene comportamientos altamente no-lineales y cíclicos (ej. picos de entrada a las 8:00 AM, caídas en fines de semana). Random Forest es un ensamble de múltiples árboles de decisión que captura de manera excelente estas correlaciones complejas sin sufrir de sobreajuste (*overfitting*) en la misma medida que otros algoritmos.

### Arquitectura del Modelo
* **Variable Objetivo (Target - $y$):** Cantidad total de accesos permitidos en una hora específica.
* **Variables Independientes (Features - $X$):**
  - `mes`: Para capturar la estacionalidad anual.
  - `dia`: Para variaciones a lo largo del mes.
  - `dia_semana`: Para distinguir días laborales de fines de semana.
  - `hora`: Para identificar los picos diarios.
* **Entrenamiento y Validación:** El modelo se entrena con el 80% del histórico de datos y se evalúa con el 20% restante utilizando validación cruzada para asegurar su fiabilidad.

### Métricas de Evaluación
El sistema evalúa el desempeño del modelo calculando:
- **MAE (Error Absoluto Medio):** Promedio de desviación de personas en las predicciones.
- **RMSE (Raíz del Error Cuadrático Medio):** Penaliza grandes desviaciones en la predicción.
- **$R^2$ Score:** Proporción de la varianza en la variable dependiente que es predecible a partir de las variables independientes.

El modelo entrenado se exporta como `rfid_rf_model.pkl` para ser consumido posteriormente en predicciones de "tiempo real" sobre cómo será el tráfico al día siguiente.

---

## 🛠️ Requisitos e Instalación

### Hardware Necesario
- 1x Arduino (Uno, Nano o Mega)
- 1x Módulo RFID RC522 (Alimentado estrictamente a **3.3V**)
- LEDs indicadores (Rojo y Verde)

### Software y Dependencias
Requiere **Python 3.8+** instalado. Las librerías necesarias son:

```bash
pip install pyserial pandas numpy matplotlib seaborn scikit-learn plotly openpyxl
```

---

## 🚀 Uso del Proyecto

1. **Configuración del Arduino:** 
   Sube el sketch `ConfiguracionArduino.ino` a tu placa. Asegúrate de configurar los pines correctamente, especialmente SS y RST.
2. **Iniciar el Servidor de Registro:** 
   Ejecuta el script de Python para empezar a escuchar los eventos del hardware:
   ```bash
   python Registro.py
   ```
   *Nota: Asegúrate de cerrar el Monitor Serie del Arduino IDE antes de ejecutar el script para evitar conflictos de puerto.*
3. **Generar y Analizar Datos (Machine Learning):**
   Abre y ejecuta el Notebook `RFID_Predictive_Analytics.ipynb` (o ejecuta `python generate_notebook.py` para regenerarlo). Este script:
   - Cargará los datos (o generará datos sintéticos si el histórico es muy corto).
   - Realizará el **Análisis Exploratorio de Datos (EDA)** con gráficos avanzados (mapas de calor, gráficas de series temporales).
   - Entrenará el modelo predictivo **Random Forest**.
   - Emitirá una **Alerta Predictiva** indicando la hora pico estimada para el día de mañana.

---

## 👨‍💻 Autor
Desarrollado para la integración de sistemas de hardware IoT, modelamiento matemático y Machine Learning aplicado a la ingeniería predictiva.
