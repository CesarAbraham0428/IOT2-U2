import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_SENSOR_TOPIC = "utng/sensorTM"
MQTT_PORT = 1883

# Configuración del sensor táctil KY-036 (conectado al pin ADC0, por ejemplo)
sensor_tactil = ADC(Pin(34))  # Pin analógico del ESP32
sensor_tactil.atten(ADC.ATTN_11DB)  # Configura la atenuación para medir voltajes de 0-3.3V
sensor_tactil.width(ADC.WIDTH_12BIT)  # Configura la resolución de la lectura (12 bits)

# Umbral para detectar contacto táctil
umbral = 2000  # Ajusta según la sensibilidad de tu sensor

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

# Bucle para leer el sensor táctil y enviar datos
while True:
    valor = sensor_tactil.read()  # Leer el valor analógico del sensor (0-4095 para 12 bits)
    
    # Invertimos la lógica de detección
    if valor < umbral:
        mensaje = f"Toque detectado, valor: {valor}"
    else:
        mensaje = f"Sin contacto, valor: {valor}"
    
    print(mensaje)
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar valor
    
    sleep(2)  # Esperar 2 segundos antes de la siguiente lectura
