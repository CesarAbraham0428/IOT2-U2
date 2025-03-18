import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_SENSOR_TOPIC = "utng/sensorPIR"
MQTT_PORT = 1883

# Configuración del sensor PIR MH-SR602 (conectado a un pin digital, por ejemplo GPIO34)
sensor_pir = Pin(34, Pin.IN)  # Configurar como entrada digital

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Agregar contraseña si es necesario
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Publicando en el tópico {MQTT_SENSOR_TOPIC}")
    return client

# Conectar a WiFi y MQTT
conectar_wifi()
client = subscribir()

# Bucle para leer el sensor PIR y enviar datos
while True:
    valor = sensor_pir.value()  # Leer el estado digital (0 = sin movimiento, 1 = movimiento detectado)
    
    if valor == 1:
        mensaje = "Movimiento detectado"
    else:
        mensaje = "Sin movimiento"
    
    print(mensaje)
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar valor
    
    sleep(2)  # Esperar 2 segundos antes de la siguiente lectura
