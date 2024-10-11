import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew

# Cargar el CSV en un DataFrame
df = pd.read_csv('valores_caracteristicas.csv')

# Crear un nuevo DataFrame para almacenar las características extraídas
caracteristicas_estadisticas = []

# Calcular los estadísticos para cada columna de características
for column in df.columns[1:-1]:  # Excluir 'Id' y 'clase'
  data = df[column].dropna()  # Eliminar valores nulos si existen
  stats = {
    'Característica': column,
    'Media': np.mean(data),
    'Media Absoluta': np.mean(np.abs(data)),
    'Mediana': np.median(data),
    'Mediana Absoluta': np.median(np.abs(data)),
    'Desviación Estándar (STD)': np.std(data),
    'Varianza (Var)': np.std(data) / np.mean(data) if np.mean(data) != 0 else np.nan,
    'Kurtosis': kurtosis(data),
    'Skewness': skew(data),
    'Cruce por Cero': np.sum(np.where(np.diff(np.sign(data)))[0]),
    'Percentil(0.0)': np.percentile(data, 0.0),
    'Percentil(0.1)': np.percentile(data, 10.0),
    'Percentil(0.2)': np.percentile(data, 20.0),
    'Percentil(0.3)': np.percentile(data, 30.0),
    'Percentil(0.4)': np.percentile(data, 40.0),
    'Percentil(0.5)': np.percentile(data, 50.0),
    'Percentil(0.6)': np.percentile(data, 60.0),
    'Percentil(0.7)': np.percentile(data, 70.0),
    'Percentil(0.8)': np.percentile(data, 80.0),
    'Percentil(0.9)': np.percentile(data, 90.0),
    'Percentil(1.0)': np.percentile(data, 100.0),
    'Raíz Cuadrada del Promedio de la Suma de los Valores al Cuadrado': np.sqrt(np.mean(data**2))
  }
  caracteristicas_estadisticas.append(stats)

# Convertir la lista de características en un DataFrame
df_estadisticas = pd.DataFrame(caracteristicas_estadisticas)

# Guardar el DataFrame con las características estadisticas en un nuevo CSV
output_estadisticas_csv = 'caracteristicas_estadisticas.csv'
df_estadisticas.to_csv(output_estadisticas_csv, index=False)

print(f'Características estadísticas guardadas en: {output_estadisticas_csv}')
