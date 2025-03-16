from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración del sensor de sonido (usando salida analógica A0)
sensor_pin = ADC(Pin(35))  # Pin GPIO35 del ESP32
sensor_pin.atten(ADC.ATTN_11DB)  # Ajuste para rango de 0 a 3.3V

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "ESP32_Sonido"  
MQTT_TOPIC = "utng/sonidoBajo"  
MQTT_PORT = 1883

ultimo_valor = None
umbral_cambio = 10  # Sensibilidad para detectar cambios en el sonido

def conectar_wifi():
    print("Conectando WiFi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        sta_if.connect('UTNG_Alumnos', '')  # Asegúrate de poner la contraseña si es necesaria
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(0.3)
    print("\nWiFi conectado!")

def conectar_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                            user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
        client.connect()
        print(f"Conectado al broker MQTT: {MQTT_BROKER}")
        return client
    except Exception as e:
        print("Error conectando a MQTT:", e)
        return None

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

while True:
    try:
        valor_sonido = sensor_pin.read()  # Leer el ADC (0-1023)
        print(f"Valor de sonido leído: {valor_sonido}")  # Depuración adicional

        # Publicamos si el cambio en el valor supera el umbral
        if ultimo_valor is None or abs(valor_sonido - ultimo_valor) > umbral_cambio:
            mensaje = f"Nivel de sonido: {valor_sonido}"
            print(f"Publicando: {mensaje}")
            if client:
                client.publish(MQTT_TOPIC, mensaje)  
            ultimo_valor = valor_sonido

    except Exception as e:
        print("Error:", e)
        client = conectar_mqtt()  # Intentar reconectar a MQTT si hay un error

    time.sleep(1)