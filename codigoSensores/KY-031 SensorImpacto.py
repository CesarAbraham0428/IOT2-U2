import network
from umqtt.simple import MQTTClient
from machine import Pin
import time

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/sensorImpacto"
MQTT_PORT = 1883

# Definir el pin con pull-up interno
impact_sensor = Pin(18, Pin.IN, Pin.PULL_UP)

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Ingresa la contraseña si es necesario
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Suscrito al tópico {MQTT_SENSOR_TOPIC}")
    return client

# Conectar a WiFi
conectar_wifi()

# Conectar a MQTT
client = subscribir()

while True:
    if impact_sensor.value() == 0:  # Detecta impacto cuando la señal es baja
        print("¡Impacto detectado!")
        client.publish(MQTT_SENSOR_TOPIC, ("Impacto Detectado").encode())  # Publicar valor como bytes
        time.sleep(2)  # Pequeño retraso para evitar lecturas repetitivas
