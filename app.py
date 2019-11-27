from gpiozero import Button
from time import sleep
from iotbutton import IotButton

address = '1A-C2-1E-56-CA-47'
botao_a = IotButton('botao_a', 2, address)
botao_b = IotButton('botao_b', 17, address)

while True:
    botao_a.gpio.wait_for_press()
    botao_a.create_speech_file()
    botao_a.gpio.wait_for_release()
    
    botao_b.gpio.wait_for_press()
    botao_b.create_speech_file()
    botao_b.gpio.wait_for_release()