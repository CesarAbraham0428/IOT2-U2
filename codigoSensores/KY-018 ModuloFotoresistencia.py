from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/moduloFotorresistencia"
MQTT_PORT = 1883

sensor = ADC(Pin(34))  # Asegúrate de usar un pin ADC válido
sensor.atten(ADC.ATTN_11DB)  # Permite leer hasta 3.3V en ESP32

# Definir umbrales de luz (ajústalos según pruebas)
LIMITE_LUZ = 10  # Valor cuando hay mucha luz
LIMITE_OSCURIDAD = 30  # Valor cuando hay poca luz


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

while True:
    valor = sensor.read()  # Lectura del sensor (0 - 4095 en ESP32)
    
    # Determinar el estado de la luz
    if valor < LIMITE_LUZ:
        estado = "Luz detectada ☀"
    elif valor < LIMITE_OSCURIDAD:
        estado = "Poca luz 🌅"
    else:
        estado = "Oscuridad total 🌑"

    print(f"{estado}")
    client.publish(MQTT_SENSOR_TOPIC, (f"{estado}").encode())  # Publicar valor como bytes
    time.sleep(1)