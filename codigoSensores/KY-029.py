import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_SENSOR_TOPIC = "utng/led23mm"
MQTT_PORT = 1883

# Pines del módulo KY-029 (Anodo común)
led_rojo = Pin(32, Pin.OUT)   # GPIO para el color rojo
led_verde = Pin(33, Pin.OUT)  # GPIO para el color verde

# Al ser ánodo común, se encienden con 0 y se apagan con 1
def set_color(rojo, verde):
    led_rojo.value(rojo)   # 0 = ENCENDER rojo, 1 = Apagar
    led_verde.value(verde) # 0 = ENCENDER verde, 1 = Apagar

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

# Bucle principal para cambiar colores
colores = [
    ("Rojo", 1, 0),      # Enciende Rojo (0), Apaga Verde (1)
    ("Verde", 0, 1),     # Enciende Verde (0), Apaga Rojo (1)
    ("Amarillo", 1,1),  # Enciende ambos (Rojo y Verde)
    ("Apagado", 0, 0)    # Apaga ambos (Rojo y Verde)
]

while True:
    for color, rojo, verde in colores:
        set_color(rojo, verde)

        mensaje = f"LED Color: {color}"
        print(mensaje)
        client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar el estado del LED
        
        sleep(3)  # Esperar 3 segundos antes de cambiar el color
