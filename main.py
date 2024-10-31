import dht
import machine
import urequests
import time
import network

def conecta_wifi():
    ssid = 'CDATOS'
    password = 'SALA-104'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        print("Conectando al Wi-Fi...")
        time.sleep(1)

    print("¡Conectado al Wi-Fi con éxito!")

conecta_wifi()

sensor = dht.DHT11(machine.Pin(4))

def thingspeak(temperatura, umidade, hidrogeno):
    try:
        
        url = "https://api.thingspeak.com/update?api_key=R30GJOUKAHCNAVUI&field1={}&field2={}".format(temperatura, umidade)
        response = urequests.get(url)
        response.close()
        print("Datos enviados a ThingSpeak: Temp={}°C, Humedad={}%".format(temperatura, umidade))
    except Exception as e:
        print("Error al enviar datos a ThingSpeak:", e)

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        umidade = sensor.humidity()
        
        print("Temperatura: {}°C, Humedad: {}%".format(temperatura, umidade))
        
        thingspeak(temperatura, umidade)
        
    except OSError as e:
        print("Error al leer el sensor:", e)
    
    time.sleep(120)
