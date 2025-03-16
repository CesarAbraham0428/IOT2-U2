import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_LASER_TOPIC = "utng/sensorObstaculo"  # Tópico para el láser
MQTT_PORT = 1883

# Configurar el pin del sensor
sensor_pin = Pin(25, Pin.IN)  # OUT del KY-032 a GPIO 25
led = Pin(2, Pin.OUT)  # LED interno de la ESP32

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

    if sensor_pin.value() == 0:  # 0 indica obstáculo detectado
        print("¡Obstáculo detectado!")
        led.value(1)  # Encender LED
        client.publish(MQTT_LASER_TOPIC, "Obstáculo detectado".encode())  # Publicar estado
    else:
        print("No hay movimiento")
        led.value(0)  # Apagar LED
        client.publish(MQTT_LASER_TOPIC, "No hay movimiento".encode())
    sleep(0.2)  # Pequeña pausa para evitar demasiadas impresiones
