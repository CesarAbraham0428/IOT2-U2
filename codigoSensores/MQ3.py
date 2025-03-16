from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración del sensor MQ-3 en el pin analógico
sensor = ADC(Pin(35))  # Para ESP32 (usar 'A0' en ESP8266)
sensor.atten(ADC.ATTN_11DB)  # Ajusta la atenuación para el rango completo (0-3.3V en ESP32)

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_MQ3 = "utng/mq3"  # Tópico para el láser
MQTT_PORT = 1883

# Umbral de detección de alcohol (ajustar según pruebas)
UMBRAL_ALCOHOL = 1300 

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" Conectado!")

def subscribir():
    global client
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Conectado a topico {MQTT_SENSOR_MQ3}")  # Tópico del láser
    return client

# Conectar a WiFi
conectar_wifi()
# Subscripción a MQTT
client = subscribir()

while True:
    valor = sensor.read()  # Leer valor analógico (0-4095 en ESP32)
    
    if valor > UMBRAL_ALCOHOL:
        print("¡Alcohol detectado!")
        client.publish(MQTT_SENSOR_MQ3, "Alcohol detectado".encode())  # Publicar estado
    else:
        print("No se detecta alcohol")
        client.publish(MQTT_SENSOR_MQ3, "No se detecta alcohol".encode())

    time.sleep(3)