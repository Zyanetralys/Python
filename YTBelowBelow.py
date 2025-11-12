import urllib.request
import urllib.parse
import json
import re
import os
import http.cookiejar

def crear_opener():
    # cookies y headers para evitar bloqueos
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-US,en;q=0.9'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Connection', 'keep-alive'),
    ]
    
    return opener

def extraer_id_video(url):
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
    opener = crear_opener()
    urllib.request.install_opener(opener)
    
    url_info = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        response = urllib.request.urlopen(url_info)
        html = response.read()
        
        # intentar decodificar
        try:
            html = html.decode('utf-8')
        except:
            import gzip
            html = gzip.decompress(html).decode('utf-8')
        
        # buscar el player response
        patrones = [
            r'var ytInitialPlayerResponse = ({.+?});',
            r'ytInitialPlayerResponse\s*=\s*({.+?});',
        ]
        
        data = None
        for patron in patrones:
            match = re.search(patron, html)
            if match:
                try:
                    data = json.loads(match.group(1))
                    break
                except:
                    continue
        
        if not data:
            return None
        
        detalles = data.get('videoDetails', {})
        streaming = data.get('streamingData', {})
        
        formatos = streaming.get('formats', [])
        formatos_adaptivos = streaming.get('adaptiveFormats', [])
        
        return {
            'titulo': detalles.get('title', 'sin_titulo'),
            'duracion': int(detalles.get('lengthSeconds', 0)),
            'formatos': formatos + formatos_adaptivos
        }
        
    except Exception as e:
        print(f"Error obteniendo info: {e}")
        return None

def limpiar_nombre_archivo(nombre):
    invalidos = '<>:"/\\|?*'
    for char in invalidos:
        nombre = nombre.replace(char, '')
    return nombre[:200]

def descargar_archivo(url, destino, nombre_archivo):
    opener = crear_opener()
    urllib.request.install_opener(opener)
    
    try:
        response = urllib.request.urlopen(url)
        total = int(response.headers.get('content-length', 0))
        descargado = 0
        bloque = 1024 * 1024
        
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
                    mb_descargado = descargado / (1024 * 1024)
                    mb_total = total / (1024 * 1024)
                    print(f"\rDescargando: {porcentaje:.1f}% ({mb_descargado:.1f}/{mb_total:.1f} MB)", end='')
        
        print()
        return True
        
    except Exception as e:
        print(f"\nError descargando: {e}")
        return False

def descargar_youtube(url, carpeta_destino="descargas"):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    print("\n--- Descargador de YouTube ---\n")
    
    video_id = extraer_id_video(url)
    if not video_id:
        print("URL invalida")
        return
    
    print("Obteniendo informacion del video...")
    info = obtener_info_video(video_id)
    
    if not info:
        print("No se pudo obtener la info del video")
        print("Posibles razones:")
        print("- Video privado o restringido")
        print("- YouTube cambio su estructura")
        print("- Problemas de conexion")
        return
    
    titulo = info['titulo']
    duracion = info['duracion']
    formatos = info['formatos']
    
    print(f"\nTitulo: {titulo}")
    print(f"Duracion: {duracion // 60}:{duracion % 60:02d}")
    
    # separar video y audio
    videos = []
    audios = []
    
    for f in formatos:
        url_descarga = f.get('url')
        if not url_descarga:
            continue
            
        mime = f.get('mimeType', '')
        calidad = f.get('qualityLabel', '')
        
        if 'video' in mime and calidad:
            videos.append({
                'calidad': calidad,
                'url': url_descarga,
                'mime': mime,
                'tamaño': f.get('contentLength', 0)
            })
        elif 'audio' in mime:
            audios.append({
                'bitrate': f.get('bitrate', 0),
                'url': url_descarga,
                'mime': mime,
                'tamaño': f.get('contentLength', 0)
            })
    
    if not videos and not audios:
        print("\nNo se encontraron formatos descargables")
        print("El video puede tener restricciones o estar cifrado")
        return
    
    # ordenar
    videos.sort(key=lambda x: int(re.search(r'\d+', x['calidad']).group()) if re.search(r'\d+', x['calidad']) else 0, reverse=True)
    audios.sort(key=lambda x: x['bitrate'], reverse=True)
    
    print("\nFormatos disponibles:")
    
    opciones = []
    
    if videos:
        print("\nVideo:")
        for i, v in enumerate(videos[:6], 1):
            tamaño_mb = int(v['tamaño']) / (1024 * 1024) if v['tamaño'] else 0
            print(f"{i}. {v['calidad']} ({tamaño_mb:.1f} MB)")
            opciones.append(('video', v))
    
    if audios:
        print(f"\n{len(opciones) + 1}. Solo audio (mejor calidad)")
        opciones.append(('audio', audios[0]))
    
    if not opciones:
        print("No hay formatos disponibles")
        return
    
    opcion = input(f"\nElige formato (1-{len(opciones)}): ")
    
    try:
        opcion = int(opcion)
        
        if opcion < 1 or opcion > len(opciones):
            print("Opcion invalida")
            return
        
        tipo, formato = opciones[opcion - 1]
        
        if tipo == 'video':
            nombre = limpiar_nombre_archivo(titulo) + ".mp4"
            print(f"\nDescargando video en {formato['calidad']}...")
        else:
            ext = '.m4a' if 'm4a' in formato['mime'] else '.webm'
            nombre = limpiar_nombre_archivo(titulo) + ext
            print("\nDescargando audio...")
        
        if descargar_archivo(formato['url'], carpeta_destino, nombre):
            print(f"\nListo! Guardado en: {os.path.join(carpeta_destino, nombre)}")
    
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
