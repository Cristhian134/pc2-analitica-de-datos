import yt_dlp
from config import PATH_FFMPEG, OUTPUT_FORMAT, POLITICOS
import json

PATH_AUDIOS = "audios/%s"

ydl_opts = {
  'format': 'bestaudio/best',
  'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': OUTPUT_FORMAT, 
    'preferredquality': '192',
  }],
  'ffmpeg_location': PATH_FFMPEG,
}

politicos_audios = {

}

count_politico = 0
for politico, info in POLITICOS.items():
  for i,link in enumerate(info['links']):
    if link.strip():
      idx = count_politico*len(info['links']) + i + 1
      audio_name = f'audio{(idx):03d}'
      audio_out_path = PATH_AUDIOS % audio_name
      ydl_opts = {
        **ydl_opts,
        'outtmpl': audio_out_path,
      }
      try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([link])

        politicos_audios[audio_name] = politico

        print("Descarga completada")
      except Exception as e:
          print(f'Ocurrió un error:\n{politico} {info["nombre"]} {link}\n{e}\n\n')
  count_politico += 1

with open('politicos_audios.json', 'w', encoding='utf-8') as archivo_json:
  json.dump(politicos_audios, archivo_json, indent=2)