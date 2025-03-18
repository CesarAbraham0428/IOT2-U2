import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_MERCURY_TOPIC = "utng/interuptormercurio"
MQTT_PORT = 1883

# Configuración del interruptor de mercurio (entrada digital)
interruptor_mercurio = Pin(4, Pin.IN, Pin.PULL_UP)  # Ajusta el pin si es necesario

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Ingresa la contraseña si aplica
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Suscrito al tópico {MQTT_MERCURY_TOPIC}")
    return client

# Conectar a WiFi
conectar_wifi()

# Conectar a MQTT
client = subscribir()

# Ciclo de lectura del interruptor de mercurio
while True:
    estado_interruptor = interruptor_mercurio.value()
    estado = "Inclinación detectada" if estado_interruptor == 0 else "Sin inclinación"  # Mensajes actualizados
    print(f"Estado del interruptor de mercurio: {estado}")
    client.publish(MQTT_MERCURY_TOPIC, estado.encode())  # Publicar estado
    sleep(3)  # Tiempo entre lecturas
