from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/sensorFlama"
MQTT_PORT = 1883

# Configuración de pines
pin_analogico = ADC(Pin(34))  # GPIO 34 -> A0
pin_analogico.atten(ADC.ATTN_11DB)  # Leer 0-3.3V (0-4095)

pin_digital = Pin(32, Pin.IN)  # GPIO 32 -> D0


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
    valor_analogico = pin_analogico.read()  # 0 - 4095
    valor_digital = pin_digital.value()  # 0 = fuego, 1 = sin fuego

    # Invertimos la lógica basada en tus valores
    if valor_analogico == 0:
        print("🔥 Flama detectada")
        client.publish(MQTT_SENSOR_TOPIC, ("🔥 Flama detectada").encode())  # Publicar valor como bytes
    else:
        print("❌ Sin flama")
        client.publish(MQTT_SENSOR_TOPIC, ("❌ Sin flama").encode())  # Publicar valor como bytes

    time.sleep(4)  # Esperar 3 segundos
