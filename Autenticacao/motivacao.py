import requests
import time

class APIConselhos:
    def __init__(self):
        self.base_url = "https://api.adviceslip.com/advice"
        self.ultimo_tempo_requisicao = 0
        self.conselho_cacheado = None
        self.google_translate_url = "https://translation.googleapis.com/language/translate/v2"
        self.google_translate_api_key = "AIzaSyCs60MsOlahnhHkeRVfI4hqjzm9D2az9wE"

    def obter_conselho_aleatorio(self):
        tempo_atual = time.time()
        
        # Verifica se houve uma solicitação nos últimos 2 segundos e retorna o conselho em cache se sim
        if tempo_atual - self.ultimo_tempo_requisicao < 2 and self.conselho_cacheado:
            return self.conselho_cacheado
        
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()  # Verifica se houve algum erro na solicitação HTTP

            dados_conselho = response.json()
            conselho = dados_conselho['slip']['advice']

            # Traduzindo o conselho para o português usando a API do Google Translate
            conselho_traduzido = self.traduzir_texto(conselho, 'en', 'pt')

            # Atualiza o tempo da última solicitação e o conselho em cache
            self.ultimo_tempo_requisicao = tempo_atual
            self.conselho_cacheado = conselho_traduzido

            return conselho_traduzido
        except requests.exceptions.RequestException as e:
            print("Erro ao obter conselho:", e)
            return None
    
    def traduzir_texto(self, texto, idioma_origem, idioma_destino):
        try:
            parametros = {
                'q': texto,
                'source': idioma_origem,
                'target': idioma_destino,
                'key': self.google_translate_api_key
            }

            response = requests.post(self.google_translate_url, data=parametros)
            response.raise_for_status()

            dados_traducao = response.json()
            texto_traduzido = dados_traducao['data']['translations'][0]['translatedText']
            return texto_traduzido
        except requests.exceptions.RequestException as e:
            print("Erro ao traduzir texto:", e)
            return None
