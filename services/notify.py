import requests

class Notify:
    
    def __init__(self):
        self.__base_url = 'https://webhook.site/'  # Adiciona a barra no final da URL base
        
    def send_event(self, data):
        # Corrigindo a formação da URL
        url = f'{self.__base_url}dc2174d6-c0d4-4a41-82df-082d52e27284'
        requests.post(
            url=url,
            json=data,
        )
