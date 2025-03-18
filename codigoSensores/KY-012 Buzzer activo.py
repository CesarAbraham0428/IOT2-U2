import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_BUZZER_TOPIC = "utng/buzzerA"
MQTT_PORT = 1883

# Configuración del buzzer pasivo (usando PWM)
buzzer = PWM(Pin(2))  # Cambia el pin si es necesario

# Notas musicales (frecuencias en Hz)
NOTAS = {
    'C': 261,
    'D': 294,
    'E': 329,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 493,
    'C_high': 523
}

# Melodía simple (lista de notas y duraciones)
melodia = [
    ('C', 0.5), ('D', 0.5), ('E', 0.5), ('F', 0.5),
    ('G', 0.5), ('A', 0.5), ('B', 0.5), ('C_high', 1)
]

def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_Alumnos', '')  # Ingresa la contraseña si aplica
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Suscrito al tópico {MQTT_BUZZER_TOPIC}")
    return client

def reproducir_melodia(melodia):
    client.publish(MQTT_BUZZER_TOPIC, "Buzzer activado".encode())
    print("Buzzer activado - Reproduciendo melodía...")
    
    for nota, duracion in melodia:
        frecuencia = NOTAS.get(nota, 0)
        if frecuencia > 0:
            buzzer.freq(frecuencia)
            buzzer.duty(512)  # Intensidad media (máximo 1023)
            print(f"Tocando nota: {nota} ({frecuencia} Hz)")
            client.publish(MQTT_BUZZER_TOPIC, f"Nota: {nota}".encode())
        else:
            buzzer.duty(0)  # Silencio
        sleep(duracion)
    
    buzzer.duty(0)  # Apagar buzzer al finalizar la melodía
    client.publish(MQTT_BUZZER_TOPIC, "Buzzer desactivado".encode())
    print("Buzzer desactivado")

# Conectar a WiFi y MQTT
conectar_wifi()
client = subscribir()

# Ejecutar la melodía en un ciclo infinito con pausas
while True:
    reproducir_melodia(melodia)
    sleep(5)  # Espera 5 segundos antes de volver a reproducir
