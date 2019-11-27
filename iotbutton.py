from gpiozero import Button
import requests
import json
import os
import sys
import subprocess

class IotButton():
    
    def __init__(self, name, pin, toy_address):
        self.name = name
        self.pin = pin
        self.toy_address = toy_address
        self.headers = {'content-type': 'application/json'}
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.sound_path = ''
        self.gpio = Button(pin)
    
    def get_speech(self, url):
        print('Requesting speech from {}'.format(self.name))
        payload = {'mac_address': self.toy_address, 'part': self.name}
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        json_response = json.loads(r.text)
        print('Done')
        return json_response[0]
    
    def create_speech_file(self, play=True):
        speech = self.get_speech('https://iotoy.projetos.in/text_to_speech/api/list')
        url_sound = 'http://iotoy.projetos.in' + speech['sound_url']
        r_sound = requests.get(url_sound)
    
        if r_sound.status_code == requests.codes.ok:
            directory = self.dir_path + '/sounds/{}'.format(self.name)
        
            if not os.path.exists(directory):
                os.makedirs(directory)
        
            self.sound_path = directory + '/' + speech['file_name'] + '.wav'
            open(self.sound_path, 'wb').write(r_sound.content)
            if play:
                self.play_speech()
            
    def play_speech(self):
        print('Playing sound...')
        subprocess.call('omxplayer --adev hdmi {}'.format(self.sound_path), shell=True) 
