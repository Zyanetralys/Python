import yt_dlp
import os

def descargar_youtube(url, carpeta_destino="descargas"):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    print("\n--- Descargador de YouTube ---\n")
    print("Que quieres descargar?")
    print("1. Mejor calidad (video + audio ya combinado)")
    print("2. 1080p (video + audio ya combinado)")
    print("3. 720p (video + audio ya combinado)")
    print("4. 480p (video + audio ya combinado)")
    print("5. Solo audio MP3 (requiere ffmpeg)")
    print("6. Solo audio M4A (requiere ffmpeg)")
    
    opcion = input("\nElige (1-6): ")
    
    ydl_opts = {
        'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        'progress_hooks': [mostrar_progreso],
        'quiet': False,
        'no_warnings': False,
    }
    
    if opcion == "1":
        ydl_opts['format'] = 'best[ext=mp4]/best'
        print("\nDescargando en la mejor calidad disponible...")
        
    elif opcion == "2":
        ydl_opts['format'] = 'best[height<=1080][ext=mp4]/best[height<=1080]'
        print("\nDescargando en 1080p...")
        
    elif opcion == "3":
        ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[height<=720]'
        print("\nDescargando en 720p...")
        
    elif opcion == "4":
        ydl_opts['format'] = 'best[height<=480][ext=mp4]/best[height<=480]'
        print("\nDescargando en 480p...")
        
    elif opcion == "5":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        print("\nDescargando solo audio en MP3...")
        print("NOTA: Requiere ffmpeg instalado")
        
    elif opcion == "6":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
        print("\nDescargando solo audio en M4A...")
        print("NOTA: Requiere ffmpeg instalado")
        
    else:
        print("Opcion invalida")
        return
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            duracion_min = info['duration'] // 60
            duracion_seg = info['duration'] % 60
            
            print(f"\nTitulo: {info['title']}")
            print(f"Duracion: {duracion_min}:{duracion_seg:02d}")
            
            ydl.download([url])
            
        print("\n\nListo! Descarga completada")
        print(f"Guardado en: {carpeta_destino}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")

def mostrar_progreso(d):
    if d['status'] == 'downloading':
        porcentaje = d.get('_percent_str', 'N/A')
        velocidad = d.get('_speed_str', 'N/A')
        tiempo = d.get('_eta_str', 'N/A')
        print(f"\r{porcentaje} - {velocidad} - quedan {tiempo}", end='')
    elif d['status'] == 'finished':
        print("\nProcesando...")

def descargar_varios():
    print("\n--- Descarga Multiple ---")
    urls = []
    
    print("\nPega las URLs (escribe 'listo' cuando termines):")
    while True:
        url = input("URL: ").strip()
        if url.lower() in ['listo', 'fin', 'ya']:
            break
        if url:
            urls.append(url)
    
    if not urls:
        print("No pusiste ninguna URL")
        return
    
    carpeta = input("\nCarpeta destino (enter para 'descargas'): ").strip() or "descargas"
    
    for i, url in enumerate(urls, 1):
        print(f"\n\n{'='*50}")
        print(f"Video {i} de {len(urls)}")
        print(f"{'='*50}")
        descargar_youtube(url, carpeta)

def main():
    while True:
        print("\n" + "="*50)
        print("YouTube Downloader")
        print("="*50)
        print("\n1. Descargar un video")
        print("2. Descargar varios videos")
        print("3. Salir")
        
        opcion = input("\nQue hago? (1-3): ")
        
        if opcion == "1":
            url = input("\nPega la URL del video: ").strip()
            if url:
                carpeta = input("Carpeta destino (enter para 'descargas'): ").strip() or "descargas"
                descargar_youtube(url, carpeta)
        
        elif opcion == "2":
            descargar_varios()
        
        elif opcion == "3":
            print("\nChao!")
            break
        
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()
