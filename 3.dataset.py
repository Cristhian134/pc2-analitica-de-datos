import os
import pandas as pd

from config import PATH_PARTICIONADO, OUTPUT_PARTICIONADO_EXT
import librosa

from functions import (
  extraer_formantes,
  extraer_f0,
  extraer_velocidad_habla,
  extraer_prosodia,
  extraer_energia,
  extraer_pausas_silencios,
  extraer_hnr,
  extraer_mfcc
)

funciones_caracteristcias = {
  'Timbre (Formantes)': extraer_formantes,  # Formantes (requeriría la ruta al archivo de audio)
  'Frecuencia fundamental (F0)': extraer_f0,  # F0
  'Duración y velocidad del habla': extraer_velocidad_habla,  # Velocidad del habla
  'Entonación (Prosodia)': extraer_prosodia,  # Prosodia
  'Energía de la señal': extraer_energia,  # Energía
  'Patrones de pausas y silencios': extraer_pausas_silencios,  # Pausas
  # 'Relación armónica-ruido (HNR)': extraer_hnr,  # HNR
  # 'Coeficientes Cepstrales en Frecuencia Mel (MFCCs)': extraer_mfcc  # MFCCs
}

audios_particionados_folder = os.listdir(PATH_PARTICIONADO)

valores_caracteristicas = {}

for i, audio_file in enumerate(audios_particionados_folder):
  audio_particionado_path = os.path.join(PATH_PARTICIONADO, audio_file)
  audio_particionado_name = os.path.splitext(audio_file)[0]
  audio_particionado_ext = os.path.splitext(audio_file)[1]
  if audio_particionado_ext == OUTPUT_PARTICIONADO_EXT and i < 5:

    print(f'Extrayendo características de {audio_particionado_name} en {audio_particionado_path}')
    audio, sr = librosa.load(audio_particionado_path)
    if audio_particionado_name not in valores_caracteristicas:
      valores_caracteristicas[audio_particionado_name] = {}

    for caracteristica, funcion in funciones_caracteristcias.items():
      if caracteristica in ['Timbre (Formantes)', 'Relación armónica-ruido (HNR)']:
        valores_caracteristicas[audio_particionado_name][caracteristica] = funcion(audio_particionado_path)
      elif caracteristica in ['Energía de la señal']:
        valores_caracteristicas[audio_particionado_name][caracteristica] = funcion(audio)
      else:
        valores_caracteristicas[audio_particionado_name][caracteristica] = funcion(audio, sr)
      print(f'  {caracteristica}: {valores_caracteristicas[audio_particionado_name][caracteristica]}')
    valores_caracteristicas[audio_particionado_name]['clase'] = audio_particionado_name.split('_')[2]
print(valores_caracteristicas)

# Crear una lista para almacenar los datos de cada audio
data = []

# Recorrer los valores de características
for audio_name, caracteristicas in valores_caracteristicas.items():
  # Crear un diccionario que contenga el nombre del audio y sus características
  entry = {'Id': audio_name}
  entry.update(caracteristicas)  # Añadir las características al diccionario
  data.append(entry)  # Agregar el diccionario a la lista

# Convertir la lista de diccionarios a un DataFrame de pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
output_csv_path = 'valores_caracteristicas.csv'
df.to_csv(output_csv_path, index=False)

print(f'Archivo CSV guardado en: {output_csv_path}')