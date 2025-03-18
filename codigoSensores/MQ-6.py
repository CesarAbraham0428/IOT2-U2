import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/mq6"
MQTT_PORT = 1883

# Configuración del sensor de gas MQ-5 (conectado a GPIO35)
sensor_gas = ADC(Pin(35))
sensor_gas.atten(ADC.ATTN_11DB)  # Permite lecturas de hasta ~3.3V
sensor_gas.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits (0-1023)

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

# Ciclo de lectura del sensor de gas MQ-5
while True:
    valor_sensor = sensor_gas.read()  # Lectura del valor analógico (0-1023)
    print(f"Valor del sensor de gas MQ-5: {valor_sensor}")
    client.publish(MQTT_SENSOR_TOPIC, str(valor_sensor).encode())  # Publicar valor como bytes
    sleep(2)  # Espera antes de la siguiente lectura
