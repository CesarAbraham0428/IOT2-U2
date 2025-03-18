import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/magnetico"
MQTT_PORT = 1883

# Configuración del sensor magnético KY-003 (conectado a un pin digital, por ejemplo, D15)
sensor_magnetico = Pin(15, Pin.IN, Pin.PULL_UP)  # Se usa pull-up para lecturas estables

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

# Ciclo de lectura del sensor magnético
while True:
    valor_sensor = sensor_magnetico.value()  # Lectura digital (0 o 1)

    if valor_sensor == 0:
        mensaje = "Magnetismo detectado"
    else:
        mensaje = "No hay magnetismo"

    print(mensaje)
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar mensaje como bytes
    sleep(1)  # Espera antes de la siguiente lectura
