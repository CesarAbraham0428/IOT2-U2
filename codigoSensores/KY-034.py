import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_SENSOR_TOPIC = "utng/led7"
MQTT_PORT = 1883

# Configuración del módulo LED KY-034
led = Pin(32, Pin.OUT)  # Configurar GPIO32 como salida para el LED

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

# Variable de estado del LED
estado_led = False  # False = apagado, True = encendido

# Bucle principal
while True:
    estado_led = not estado_led  # Alternar entre encendido y apagado
    
    if estado_led:
        led.value(1)  # Encender LED
        mensaje = "LED Encendido"
    else:
        led.value(0)  # Apagar LED
        mensaje = "LED Apagado"
    
    print(mensaje)
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar estado del LED
    
    sleep(5)  # Esperar 2 segundos antes de cambiar el estado
