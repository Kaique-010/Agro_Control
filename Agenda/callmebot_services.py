import requests
import os
from dotenv import load_dotenv
load_dotenv()

'''
cria-se a clase de chamar a api craida no callme bot e chama o metodo em send_message que é a mensagem que ser aenviada pelo bot 
'''


class CallMeBot:
    
    def __init__(self):
        self.__base_url = 'https://api.callmebot.com/whatsapp.php'  #a base da api do callme
        self.__api_key = os.getenv('API_KEY')                       #meu .env com a chave da api
    
    def send_message(self, message):                                #o metodo que vai ser o envio da mensagem pelo objeto estanciado
        response = requests.get(                                    #PAssa o get da api concatenado com os dados da minha api criada 
            url=f'{self.__base_url}?phone=554188398453&text={message}&apikey={self.__api_key}' #Chama o objeto para ser passado ao chamar no main
        )   
        return response.text