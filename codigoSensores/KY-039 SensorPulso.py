from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/sensorPulso"
MQTT_PORT = 1883

# Configuración del sensor en GPIO35
sensor = ADC(Pin(35))
sensor.atten(ADC.ATTN_11DB)  # Configurar el rango a 0-3.3V


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
    valor = sensor.read()  # Leer el valor analógico (0-4095)
    print("Pulso:", valor)
    mensaje = f"Pulso: {valor}"  # Formatear la cadena con el valor
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar valor como bytes
    time.sleep(1)  # Pequeño retraso
    