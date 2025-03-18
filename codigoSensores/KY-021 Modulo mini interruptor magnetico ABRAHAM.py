import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/miniInterruptorMagnetico"
MQTT_PORT = 1883

# Configuración del interruptor magnético (conectado a GPIO34)
reed_switch = Pin(34, Pin.IN, Pin.PULL_UP)  # Entrada digital con pull-up interno

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

# Ciclo de detección del campo magnético
while True:
    estado = reed_switch.value()  
    
    if estado == 0:
        mensaje = "Detecta campo magnético"
    else:
        mensaje = "No se detecta campo magnético"

    print(mensaje)  # Mostrar en consola
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar en MQTT

    sleep(0.5)  # Espera antes de la siguiente lectura
