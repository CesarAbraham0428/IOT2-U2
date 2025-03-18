import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep
import time

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_JOYSTICK_TOPIC = "joystick/posicion"
MQTT_PORT = 1883


# Pines del joystick
JOY_X_PIN = 32
JOY_Y_PIN = 33   

# Inicialización de los pines analógicos para el joystick
joy_x = ADC(Pin(JOY_X_PIN))
joy_y = ADC(Pin(JOY_Y_PIN))
joy_x.atten(ADC.ATTN_11DB)  
joy_y.atten(ADC.ATTN_11DB)

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Ingresa la contraseña si es necesario
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

# Función para conectar al broker MQTT
def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    return client

# Función para leer los valores del joystick
def leer_joystick():
    x_val = joy_x.read()
    y_val = joy_y.read()
    print(f"Joystick X: {x_val}, Y: {y_val}")
    return x_val, y_val

# Conectar a WiFi
conectar_wifi()

# Conectar a MQTT
client = subscribir()

# Ciclo de lectura del sensor de campo magnético y joystick
while True:
    # Leer y enviar la posición del joystick
    x, y = leer_joystick()
    payload = f"x: {x}, y: {y}"  
    print("Enviando joystick:", payload)
    client.publish(MQTT_JOYSTICK_TOPIC, payload)

    sleep(0.5)  # Espera antes de la siguiente lectura

