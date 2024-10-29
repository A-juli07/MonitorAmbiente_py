import dht
import machine
import urequests
import time
import network

def conecta_wifi():
    ssid = 'CLARO_2G0810A0'
    password = 'LACASITA'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        print("Conectando ao Wi-Fi...")
        time.sleep(1)

    print("Conectado ao Wi-Fi com sucesso!")

conecta_wifi()

sensor = dht.DHT11(machine.Pin(4))

def thingspeak(temperatura, umidade, rele_estado):
    try:
        
        url = "https://api.thingspeak.com/update?api_key=R30GJOUKAHCNAVUI&field1={}&field2={}".format(temperatura, umidade)
        response = urequests.get(url)
        response.close()
        print("Dados enviados para o ThingSpeak: Temp={}°C, Umidade={}%".format(temperatura, umidade))
    except Exception as e:
        print("Erro ao enviar dados ao ThingSpeak:", e)

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        umidade = sensor.humidity()
        
        print("Temperatura: {}°C, Umidade: {}%".format(temperatura, umidade))
        
        thingspeak(temperatura, umidade)
        
    except OSError as e:
        print("Erro ao ler o sensor:", e)
    
    time.sleep(2)
