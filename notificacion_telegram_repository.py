import sys
import traceback
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import socket

# Adaptador para forzar salida por IP local específica
class SourceIPAdapter(HTTPAdapter):
    def __init__(self, source_ip, **kwargs):
        self.source_ip = source_ip
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            source_address=(self.source_ip, 0),
            **pool_kwargs
        )

try:
    # Parámetros desde PRTG
    device = sys.argv[1] if len(sys.argv) > 1 else "Dispositivo"
    ip = sys.argv[2] if len(sys.argv) > 2 else "IP desconocida"
    sensor = sys.argv[3] if len(sys.argv) > 3 else "Sensor"
    status = sys.argv[4] if len(sys.argv) > 4 else "Estado desconocido"
    lastmessage = sys.argv[5] if len(sys.argv) > 5 else "Sin detalles"
    since = sys.argv[6] if len(sys.argv) > 6 else "El sistema está abajo desde"

    # Credenciales de Telegram
    bot_token = ''
    chat_id = ''

    # Mensaje a enviar
    body = (
        f'🚨 *Alerta de PRTG* 🚨\n'
        f'*Equipo:* {device}\n'
        f'*IP:* {ip}\n'
        f'*Sensor:* {sensor}\n'
        f'*Estado:* {status}\n'
        f'*Mensaje:* {lastmessage}\n'
        f'*Sin comunicaciones desde:* {since}'
    )

    # Sesión con salida forzada por IP local 192.xxx.xx.xx
    session = requests.Session()
    session.mount("https://", SourceIPAdapter("192.000.0.00"))

    # Enviar mensaje
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': body,
        'parse_mode': 'Markdown'
    }

    response = session.post(url, data=payload)

    if response.status_code == 200:
        print("Mensaje enviado correctamente a Telegram.")
    else:
        print(f"Error al enviar mensaje a Telegram: {response.status_code} - {response.text}")

except Exception as e:
    with open("telegram_error.log", "w") as f:
        f.write("Error al enviar mensaje a Telegram:\n")
        f.write(traceback.format_exc())
