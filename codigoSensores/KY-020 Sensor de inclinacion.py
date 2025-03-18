import network
import time
import machine
from umqtt.simple import MQTTClient

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensorInclinacionClient"
MQTT_SENSOR_TOPIC = "utng/sensorInclinacion"
MQTT_PORT = 1883

# Configuración del sensor SW-520D
SENSOR_PIN = 4
sensor = machine.Pin(SENSOR_PIN, machine.Pin.IN, machine.Pin.PULL_UP)  # Activa la resistencia interna

def conectar_wifi():
    """Conecta a la red WiFi y maneja reconexiones."""
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Agregar contraseña si es necesario
    intentos = 0
    while not sta_if.isconnected() and intentos < 10:
        print(".", end="")
        time.sleep(1)
        intentos += 1
    if sta_if.isconnected():
        print(" ¡Conectado!")
    else:
        print(" No se pudo conectar a WiFi.")

def conectar_mqtt():
    """Conecta al broker MQTT y maneja reconexiones."""
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                            user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
        client.connect()
        print(f"Conectado a {MQTT_BROKER}")
        print(f"Publicando en el tópico {MQTT_SENSOR_TOPIC}")
        return client
    except Exception as e:
        print(f"Error al conectar a MQTT: {e}")
        return None

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

while True:
    estado = sensor.value()  # Leer el estado del sensor (0 = inclinado, 1 = sin inclinación)
    
    if estado == 0:
        mensaje = "¡Inclinación detectada!"
    else:
        mensaje = "Sin inclinación"

    print(mensaje)

    if client:  # Verifica que MQTT esté conectado
        try:
            client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar mensaje en bytes
        except Exception as e:
            print(f"Error al publicar en MQTT: {e}")
            client = conectar_mqtt()  # Reintenta la conexión
    
    time.sleep(2)  # Esperar 2 segundos antes de la siguiente lectura
