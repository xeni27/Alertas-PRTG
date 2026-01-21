PRTG to Telegram Notification Bridge
Este proyecto consiste en un script de integración desarrollado en Python que automatiza el envío de alertas críticas desde PRTG Network Monitor hacia canales de Telegram. El sistema transforma las variables de monitoreo en notificaciones enriquecidas en tiempo real.
Características principales
Integración Nativa: Diseñado para ser ejecutado como una "Acción de Notificación" en PRTG.
Source IP Binding: Incluye una clase personalizada (SourceIPAdapter) para forzar la salida de datos a través de una interfaz de red específica, ideal para entornos corporativos con múltiples VLANs o restricciones de Firewall.
Formateo Dinámico: Utiliza Markdown para enviar alertas visualmente claras, facilitando la lectura rápida por parte del equipo técnico.
Manejo de Errores: Sistema de logging local para capturar excepciones y facilitar el troubleshooting.

Stack Tecnológico
Lenguaje: Python 3.x
Librerías: requests (Manejo de API HTTP), urllib3 (Gestión de pools de conexión).
Protocolo de Red: SNMP (para la obtención de datos en PRTG).
API: Telegram Bot API.

Funcionamiento Técnico
El script recibe argumentos de línea de comandos (sys.argv) enviados por PRTG tras detectar un cambio de estado en un sensor.
Lógica de Red (Advanced Networking)
A diferencia de un script de peticiones simple, este desarrollo implementa un Adapter de Red personalizado:
Python
Forzado de salida por IP específica para cumplimiento de políticas de firewall
class SourceIPAdapter(HTTPAdapter):
    def init_poolmanager(self, ...):
        self.poolmanager = PoolManager(..., source_address=(self.source_ip, 0))
Esto garantiza que el tráfico de monitoreo siempre provenga de la IP autorizada (111.111.xx.xx), evitando bloqueos en la infraestructura de red.

Configuración en PRTG
Para implementar este sistema:
Colocar el script en la carpeta de notificaciones de PRTG: C:\Program Files (x86)\PRTG Network Monitor\Notifications\EXE.
En la configuración de la notificación, pasar los siguientes parámetros: "%device" "%ip" "%sensor" "%status" "%lastmessage" "%since"
Ejemplo de Alerta en Telegram
🚨 Alerta de PRTG 🚨 Equipo: Switch_Core_01 IP: 10.0.0.1 Sensor: Ping Estado: Down Mensaje: Request Timed Out Sin comunicaciones desde: 21/01/2026 10:00:00
