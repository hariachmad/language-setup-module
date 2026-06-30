import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "language.json"
class SioClientWrapper:
    def __init__(self, sio_client):
        self.CONFIG_PATH = CONFIG_PATH
        if not self.CONFIG_PATH:
            raise ValueError("CONFIG_PATH environment variable is not set")
        self.sio_client = sio_client
        self._register_events()
        
    def load_config(self,):
        with open(self.CONFIG_PATH, 'r') as f:
            return json.load(f)

    def save_config(self,config):
        with open(self.CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

    def _register_events(self):
        sio = self.sio_client.get_instance().sio

        @sio.event
        def connect(*args):
            print("Connected with server")

        @sio.event
        def disconnect(*args):
            print("Disconnected from server")

        @sio.event
        def message(data):
            print(f"Event received: {data}")
            
        @sio.event
        def error(data):
            print(f"Error: {data}")
        
        @sio.on('LANGUAGE_GET')
        def on_language_get(*args):
            config = self.load_config()
            sio.emit('LANGUAGE_CURRENT', {'lang' : config['language']})    
            
        @sio.on('LANGUAGE_SET')
        def on_language_set(payload):
            language = payload.get('lang')
            supported = ['id', 'en', 'sv']

            if language not in supported:
                self.emit('ACK_LANGUAGE_SET', {
            'success': False,
            'error': f'Language "{language}" not supported'
            })
                return

            config = self.load_config()
            config['language'] = language
            self.save_config(config)

            sio.emit('ACK_LANGUAGE_SET', {'success': True})
            print(f"[LanguageSetup] Language changed to: {language}")