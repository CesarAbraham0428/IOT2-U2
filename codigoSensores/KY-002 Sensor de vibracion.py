import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_VIBRATION_TOPIC = "utng/vibracion"
MQTT_PORT = 1883

# Configuración del sensor de vibración
vibration_sensor = Pin(18, Pin.IN)  # Salida digital del sensor de vibración

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')

    # Esperar hasta que se conecte
    intentos = 0
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.5)
        intentos += 1
        if intentos > 20:  # 10 segundos de intentos
            print("No se pudo conectar a WiFi. Reiniciando...")
            sleep(2)
            machine.reset()
    print("Conectado!")

def conectar_mqtt():
    global client
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                            user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
        client.connect()
        print(f"Conectado a {MQTT_BROKER}")
    except Exception as e:
        print(f"Error conectando MQTT: {e}")
        sleep(5)
        machine.reset()  # Reinicia si no se puede conectar

# Conectar a WiFi y MQTT
conectar_wifi()
conectar_mqtt()

# Ciclo de lectura con reconexión automática
while True:
    try:
        sensor_status = vibration_sensor.value()
        estado = "Vibración" if sensor_status == 1 else "Sin Vibración"
        print(f"Estado del sensor: {estado}")

        # Publicar mensaje MQTT correctamente
        client.publish(MQTT_VIBRATION_TOPIC, estado.encode())

    except Exception as e:
        print(f"Error en loop: {e}")
        conectar_wifi()  # Intentar reconectar WiFi
        conectar_mqtt()  # Intentar reconectar MQTT

    sleep(3)

