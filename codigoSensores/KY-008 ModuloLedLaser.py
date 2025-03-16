import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_LASER_TOPIC = "utng/laser"  # Tópico para el láser
MQTT_PORT = 1883

# Configuración del láser
laser = Pin(15, Pin.OUT)  # Pin del láser

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
    print(f"Conectado a topico {MQTT_LASER_TOPIC}")  # Tópico del láser
    return client

# Conectar a WiFi
conectar_wifi()
# Subscripción a MQTT
client = subscribir()

# Ciclo de control del láser
while True:
    # Encender el láser
    laser.value(1)  # Encender
    print("Láser encendido")
    client.publish(MQTT_LASER_TOPIC, "Láser Encendido".encode())  # Publicar estado
    sleep(2)  # Esperar 2 segundos

    # Apagar el láser
    laser.value(0)  # Apagar
    print("Láser apagado")
    client.publish(MQTT_LASER_TOPIC, "Láser Apagado".encode())  # Publicar estado
    sleep(2)  # Esperar 2 segundos