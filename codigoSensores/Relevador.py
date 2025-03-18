import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_RELAY_TOPIC = "utng/rele"
MQTT_PORT = 1883

# Configuración del módulo relé (conectado a GPIO 2)
rele = Pin(2, Pin.OUT)  # GPIO 2 configurado como salida para el relé

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
    print(f"Publicando en el tópico {MQTT_RELAY_TOPIC}")
    return client

# Conectar a WiFi
conectar_wifi()

# Conectar a MQTT
client = subscribir()

# Ciclo de control del relé
while True:
    rele.on()  # Activa el relé
    client.publish(MQTT_RELAY_TOPIC, "Encendido")  # Publicar estado "ON"
    print("Relé encendido")
    sleep(5)  # Espera 5 segundos
    
    rele.off()  # Desactiva el relé
    client.publish(MQTT_RELAY_TOPIC, "Apagado")  # Publicar estado "OFF"
    print("Relé apagado")
    sleep(5)  # Espera 5 segundos
