import urllib.request
import urllib.parse
import json
import re
import os

def extraer_id_video(url):
    # sacar el ID del video de la URL
    patrones = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    
    for patron in patrones:
        match = re.search(patron, url)
        if match:
            return match.group(1)
    return None

def obtener_info_video(video_id):
    # conseguir info del video
    url_info = f"https://www.youtube.com/watch?v={video_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    req = urllib.request.Request(url_info, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        # buscar datos del video en el html
        match = re.search(r'var ytInitialPlayerResponse = ({.+?});', html)
        if not match:
            return None
            
        data = json.loads(match.group(1))
        
        # info basica
        detalles = data.get('videoDetails', {})
        formatos = data.get('streamingData', {}).get('formats', [])
        formatos_adaptivos = data.get('streamingData', {}).get('adaptiveFormats', [])
        
        return {
            'titulo': detalles.get('title', 'sin_titulo'),
            'duracion': int(detalles.get('lengthSeconds', 0)),
            'formatos': formatos + formatos_adaptivos
        }
        
    except Exception as e:
        print(f"Error al obtener info: {e}")
        return None

def limpiar_nombre_archivo(nombre):
    # quitar caracteres raros del nombre
    invalidos = '<>:"/\\|?*'
    for char in invalidos:
        nombre = nombre.replace(char, '')
    return nombre[:200]  # limitar largo

def descargar_archivo(url, destino, nombre_archivo):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            total = int(response.headers.get('content-length', 0))
            descargado = 0
            bloque = 1024 * 1024  # 1MB
            
            ruta_completa = os.path.join(destino, nombre_archivo)
            
            with open(ruta_completa, 'wb') as f:
                while True:
                    datos = response.read(bloque)
                    if not datos:
                        break
                    
                    f.write(datos)
                    descargado += len(datos)
                    
                    if total > 0:
                        porcentaje = (descargado / total) * 100
                        print(f"\rDescargando: {porcentaje:.1f}%", end='')
        
        print()  # nueva linea
        return True
        
    except Exception as e:
        print(f"\nError descargando: {e}")
        return False

def descargar_youtube(url, carpeta_destino="descargas"):
    # crear carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    print("\n--- Descargador de YouTube ---\n")
    
    # sacar ID del video
    video_id = extraer_id_video(url)
    if not video_id:
        print("URL invalida")
        return
    
    print("Obteniendo informacion del video...")
    info = obtener_info_video(video_id)
    
    if not info:
        print("No se pudo obtener la info del video")
        return
    
    titulo = info['titulo']
    duracion = info['duracion']
    formatos = info['formatos']
    
    print(f"\nTitulo: {titulo}")
    print(f"Duracion: {duracion // 60}:{duracion % 60:02d}")
    
    # separar formatos de video y audio
    videos = []
    audios = []
    
    for f in formatos:
        mime = f.get('mimeType', '')
        calidad = f.get('qualityLabel', '')
        
        if 'video' in mime and calidad:
            videos.append({
                'calidad': calidad,
                'url': f.get('url'),
                'mime': mime
            })
        elif 'audio' in mime:
            audios.append({
                'bitrate': f.get('bitrate', 0),
                'url': f.get('url'),
                'mime': mime
            })
    
    # ordenar por calidad
    videos.sort(key=lambda x: int(re.search(r'\d+', x['calidad']).group()) if re.search(r'\d+', x['calidad']) else 0, reverse=True)
    audios.sort(key=lambda x: x['bitrate'], reverse=True)
    
    print("\nFormatos disponibles:")
    print("\nVideo:")
    for i, v in enumerate(videos[:5], 1):  # mostrar top 5
        print(f"{i}. {v['calidad']}")
    
    print(f"\n{len(videos) + 1}. Solo audio (mejor calidad)")
    
    opcion = input("\nElige formato (1-{}): ".format(len(videos) + 1))
    
    try:
        opcion = int(opcion)
        
        if opcion <= len(videos):
            # descargar video
            video_elegido = videos[opcion - 1]
            nombre = limpiar_nombre_archivo(titulo) + ".mp4"
            
            print(f"\nDescargando video en {video_elegido['calidad']}...")
            if descargar_archivo(video_elegido['url'], carpeta_destino, nombre):
                print(f"\nListo! Guardado en: {os.path.join(carpeta_destino, nombre)}")
        
        elif opcion == len(videos) + 1 and audios:
            # descargar audio
            audio_elegido = audios[0]
            ext = '.m4a' if 'm4a' in audio_elegido['mime'] else '.webm'
            nombre = limpiar_nombre_archivo(titulo) + ext
            
            print("\nDescargando audio...")
            if descargar_archivo(audio_elegido['url'], carpeta_destino, nombre):
                print(f"\nListo! Guardado en: {os.path.join(carpeta_destino, nombre)}")
        else:
            print("Opcion invalida")
    
    except ValueError:
        print("Opcion invalida")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n" + "="*50)
        print("YouTube Downloader")
        print("="*50)
        print("\n1. Descargar video")
        print("2. Salir")
        
        opcion = input("\nQue hago? (1-2): ")
        
        if opcion == "1":
            url = input("\nPega la URL del video: ").strip()
            if url:
                carpeta = input("Carpeta destino (enter para 'descargas'): ").strip() or "descargas"
                descargar_youtube(url, carpeta)
        
        elif opcion == "2":
            print("\nChao!")
            break
        
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()
