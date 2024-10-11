import os
import json

from pydub import AudioSegment

from config import PATH_AUDIOS, PATH_PARTICIONADO, OUTPUT_EXT

with open('politicos_audios.json', 'r') as data:
  politicos_audios = json.load(data)

os.makedirs(PATH_PARTICIONADO, exist_ok=True)
audios_folder = os.listdir(PATH_AUDIOS)
for audio in audios_folder:
  audio_path = os.path.join(PATH_AUDIOS, audio)
  audio_name = os.path.splitext(audio)[0]
  audio_ext = os.path.splitext(audio)[1]

  if audio_ext == OUTPUT_EXT:
    print(f'Particionando {audio_name}')

    # Cargar el audio en formato .wav
    audio_wav = AudioSegment.from_wav(audio_path)
    # Duración del segmento en milisegundos (1 segundo)
    segment_duration = 1000  
    # Duración total del archivo en milisegundos
    total_duration = len(audio_wav)
    # Número de segmentos
    num_segments = total_duration // segment_duration  

    # Iterar a través de los segmentos y guardarlos con el nombre especificado
    for i in range(num_segments):
      start_time = i * segment_duration
      end_time = (i + 1) * segment_duration
      segment = audio_wav[start_time:end_time]

      # Definir el nombre del archivo de salida
      output_filename = f'{audio_name}_{i+1:04d}_{politicos_audios[audio_name]}.wav'
      output_path = os.path.join(PATH_PARTICIONADO, output_filename)

      # Guardar el segmento como .wav
      segment.export(output_path, format='wav')

      print(f'  Segmento {i+1} guardado como {output_filename}')

print('Conversión y segmentación completadas.')