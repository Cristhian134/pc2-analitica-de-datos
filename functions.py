import librosa
import numpy as np
import parselmouth 

def extraer_formantes(audio_file):
  snd = parselmouth.Sound(audio_file)
  formants = snd.to_formant_burg().get_value_at_time(1, 0.5)  # Valor de formante en tiempo 0.5
  return formants

def extraer_f0(audio, sr):
  f0, _, _ = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
  return np.nanmean(f0)  # Promedio de la frecuencia fundamental

def extraer_velocidad_habla(audio, sr):
  duracion = librosa.get_duration(y=audio, sr=sr)
  palabras_aprox = len(librosa.effects.split(y=audio))  # Aproximación por número de segmentos
  return palabras_aprox / duracion  # Velocidad aproximada (palabras por segundo)

def extraer_prosodia(audio, sr):
  # Variación de la entonación usando la desviación estándar de F0
  f0, _, _ = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
  return np.nanstd(f0)  # Desviación estándar de la frecuencia fundamental

def extraer_energia(audio):
  energy = librosa.feature.rms(y=audio)
  return np.mean(energy)  # Promedio de la energía de la señal

def extraer_pausas_silencios(audio, sr):
  intervals = librosa.effects.split(y=audio)
  return len(intervals)  # Cantidad de pausas detectadas

def extraer_hnr(audio_file):
  # snd = parselmouth.Sound(audio_file)
  # harmonicity = snd.to_harmonicity()
  # hnr_values = harmonicity.values()  # Obtiene los valores de HNR
  # hnr_mean = np.mean(hnr_values)  # Calcula el promedio
  return None

def extraer_mfcc(audio, sr):
  mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
  return np.mean(mfccs, axis=1)  # Promedio de los MFCCs