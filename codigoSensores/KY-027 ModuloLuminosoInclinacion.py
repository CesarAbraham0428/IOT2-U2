# Import para acceso a red
import network
# Para usar protocolo MQTT
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/ky027"
MQTT_PORT = 1883

# Configuración del sensor KY-027
sensor_ky027 = Pin(14, Pin.IN, Pin.PULL_UP)  # Señal del sensor de mercurio
led_ky027 = Pin(19, Pin.OUT)  # LED externo controlado por ESP32

# Apago el LED inicialmente
led_ky027.value(0)

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('raberry3', 'linux123')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi Conectada!")

# Función para suscribir al broker MQTT
def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID,
                        MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER,
                        password=MQTT_PASSWORD,
                        keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, en el tópico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Función encargada de manejar los mensajes MQTT recibidos
def llegada_mensaje(topic, msg):
    print(f"Mensaje recibido en {topic}: {msg}")

# Conectar a WiFi
conectar_wifi()

# Subscripción a un broker MQTT
client = subscribir()

# Variable para almacenar el estado anterior del sensor
estado_anterior_ky027 = 1  # Inicialmente el sensor está en reposo

# Ciclo infinito
while True:
    client.check_msg()  # Verifica si hay mensajes MQTT

    # Leer el sensor KY-027
    estado_ky027 = sensor_ky027.value()

    if estado_ky027 != estado_anterior_ky027:
        if estado_ky027 == 0:
            print("Movimiento detectado en el KY-027")
            led_ky027.value(1)  # Enciende LED externo
            client.publish(MQTT_TOPIC, "Movimiento detectado")
        else:
            print("Sin movimiento en el KY-027")
            led_ky027.value(0)  # Apaga LED externo
            client.publish(MQTT_TOPIC, "Sin movimiento")

    estado_anterior_ky027 = estado_ky027

    sleep(2)