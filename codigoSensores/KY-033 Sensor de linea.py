import network
import time
import machine
from umqtt.simple import MQTTClient

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_SENSOR_TOPIC = "utng/sensorDeLinea"
MQTT_PORT = 1883

# Configuración del sensor KY-033
SENSOR_PIN = 4  
sensor = machine.Pin(SENSOR_PIN, machine.Pin.IN)

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Agregar contraseña si es necesario
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Publicando en el tópico {MQTT_SENSOR_TOPIC}")
    return client

# Conectar a WiFi y MQTT
conectar_wifi()
client = subscribir()

while True:
    estado = sensor.value()  
    
    if estado == 0:
        mensaje = "Línea detectada"
        client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar valor
        print(mensaje)
    else:
        mensaje = "Línea no detectada"
        print(mensaje)
        client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar valor
        
    time.sleep(2) 
