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
RELE_PIN = machine.Pin(17, machine.Pin.OUT)
RELE_PIN.value(0)

def thingspeak(temperatura, umidade, rele_estado):
    try:
        
        url = "https://api.thingspeak.com/update?api_key=VEH8ZPQZ5D0750KZ&field1={}&field2={}&field3={}".format(temperatura, umidade, rele_estado)
        response = urequests.get(url)
        response.close()
        print("Dados enviados para o ThingSpeak: Temp={}°C, Umidade={}%, Relé={}".format(temperatura, umidade, rele_estado))
    except Exception as e:
        print("Erro ao enviar dados ao ThingSpeak:", e)

def verificar_condicoes(temperatura, umidade):
    if temperatura > 31 or umidade > 70:
        RELE_PIN.value(1)
        print("Relé ligado!")
        return 1
    else:
        RELE_PIN.value(0)
        print("Relé desligado.")
        return 0

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        umidade = sensor.humidity()
        
        print("Temperatura: {}°C, Umidade: {}%".format(temperatura, umidade))
        
        rele_estado = verificar_condicoes(temperatura, umidade)
        thingspeak(temperatura, umidade, rele_estado)
        
    except OSError as e:
        print("Erro ao ler o sensor:", e)
    
    time.sleep(2)