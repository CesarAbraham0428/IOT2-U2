import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_PHOTO_TOPIC = "utng/photo_sensor"
MQTT_PORT = 1883

# Configuración del sensor de fotointerruptor
photo_sensor = Pin(18, Pin.IN)  # Pin de salida digital del fotointerruptor

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
    return client

# Conectar a WiFi
conectar_wifi()
# Subscripción a MQTT
client = subscribir()

# Ciclo de lectura del fotointerruptor
while True:
    sensor_status = photo_sensor.value()
    estado = "No interrumpido" if sensor_status == 0 else "Interrumpido"
    print(f"Estado del sensor: {estado}")
    client.publish(MQTT_PHOTO_TOPIC, estado)
    sleep(3)
