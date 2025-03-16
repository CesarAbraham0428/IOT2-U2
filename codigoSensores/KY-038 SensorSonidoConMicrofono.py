import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_Sonido_TOPIC = "utng/sonidoDuro"  
MQTT_PORT = 1883

# Configuración del sensor KY-038 (Analógico)
sensor_pin = ADC(Pin(34))  # Entrada analógica del sensor KY-038 (pin A0)
sensor_pin.width(ADC.WIDTH_10BIT)  # Configura el ancho de bits (10 bits = 0-1023)
sensor_pin.atten(ADC.ATTN_11DB)  # Ajustar la atenuación (0-3.6V)

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
    print(f"Conectado a tópico {MQTT_Sonido_TOPIC}")  
    return client

# Conectar a WiFi
conectar_wifi()
client = subscribir()

while True:
    sonido = sensor_pin.read()  

    # Filtrar valores saturados
    if sonido >= 1020:  # Puede estar saturado
        print("[WARN] Sensor saturado, revisa el potenciómetro")
        sonido = 1020  # Limitar el máximo valor útil

    client.publish(MQTT_Sonido_TOPIC, str(sonido))
    print(f"[INFO] Publicado en {MQTT_Sonido_TOPIC}: {sonido}")

    sleep(2)

