    import asyncio
import csv
import re
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError

# --- CONFIGURACIÓN (CAMBIA ESTOS DATOS POR LOS TUYOS) ---
API_ID = 1234567  # Pon aquí tu api_id (sin comillas, solo el número)
API_HASH = 'tu_api_hash_aqui'  # Pon aquí tu api_hash entre las comillas
SESSION_NAME = 'telegram_scraper'
CSV_FILE = 'data/telegram_autos.csv'
GRUPOS = [
    'https://t.me/goldenbullbusinessfamilycars',
    'https://t.me/Motos_Autos_Discover'
]

def extraer_datos(texto):
    datos = {
        'Marca': 'Desconocida', 'Modelo': '', 'Anio': '', 'Precio': '', 
        'Moneda': 'USD', 'Papeles': '', 'Provincias': '', 
        'Uso_y_Desgaste': '', 'Mecanicas_y_Dimensiones': '', 
        'URL_Anuncio': '', 'Descripcion_Cruda': texto
    }
    # Buscar año
    match_anio = re.search(r'\b(19|20)\d{2}\b', texto)
    if match_anio: 
        datos['Anio'] = match_anio.group(0)
    # Buscar precio (números seguidos de USD o EUR)
    match_precio = re.search(r'(\d{1,3}(?:[.,]\d{3})*)\s*(USD|EUR|CUC)', texto, re.IGNORECASE)
    if match_precio:
        datos['Precio'] = match_precio.group(1)
        datos['Moneda'] = match_precio.group(2).upper()
    return datos

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    print("¡Conectado a Telegram!")

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Marca', 'Modelo', 'Anio', 'Precio', 'Moneda', 'Papeles', 
            'Provincias', 'Uso_y_Desgaste', 'Mecanicas_y_Dimensiones', 
            'URL_Anuncio', 'Descripcion_Cruda'
        ])
        writer.writeheader()

        total_mensajes = 0
        for grupo_url in GRUPOS:
            print(f"\nLeyendo grupo: {grupo_url}")
            try:
                entidad = await client.get_entity(grupo_url)
                async for mensaje in client.iter_messages(entidad, limit=200):
                    if mensaje.text:
                        texto = mensaje.text
                        # Filtro básico de palabras clave
                        if any(p in texto.lower() for p in ['carro', 'auto', 'vendo', 'usd', 'particular', 'motor']):
                            datos = extraer_datos(texto)
                            if hasattr(entidad, 'username') and entidad.username:
                                datos['URL_Anuncio'] = f"https://t.me/{entidad.username}/{mensaje.id}"
                            writer.writerow(datos)
                            total_mensajes += 1
                print(f"  -> Mensajes extraídos de este grupo.")
            except ChannelPrivateError:
                print(f"  -> Error: El grupo {grupo_url} es privado.")
            except FloodWaitError as e:
                print(f"  -> ¡Alerta! Esperando {e.seconds} segundos por límite de Telegram...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"  -> Error inesperado en {grupo_url}: {e}")
            
            await asyncio.sleep(2)

    print(f"\n¡Listo! Total de mensajes guardados: {total_mensajes} en {CSV_FILE}")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
