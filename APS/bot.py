from chave import chave_api, token
import requests
import time
import json
import os

class TelegramBot: #Inicialização a API do telegram passando o Token que está no arquivo chave.py
    def __init__(self):
        self.url = f'https://api.telegram.org/bot{token}/'
    
    def Iniciar(self): #Função principal na qual vai ficar responsavel por coletar informações das outras e devolver a resposta ao usuário através da função de responder 
        update_id = None 
        while True:
            atualizar = self.novas_mensagens(update_id)
            dados = atualizar["result"]
            if dados:
                for dado in dados:
                    update_id = dado["update_id"]
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    primeira_mensagem = int(dado["message"]["message_id"]) == 1
                    resposta = self.gerar_respostas(mensagem, primeira_mensagem)
                    self.responder(resposta, chat_id)
            else:
                time.sleep(10)
    
    def novas_mensagens(self, update_id): #função que utiliza o link dinamico da Telegrambot para capturar o id da mensagem, e retorna como json para função de iniciar
        link = f'{self.url}getUpdates?timeout=5'
        if update_id:
            link = f'{link}&offset={update_id + 1}'
        result = requests.get(link)
        return json.loads(result.content)

    def gerar_respostas(self, mensagem, primeira_mensagem): #função de gerar a primeira resposta pro cliente, caso seja a primeira mensagem com o bot, o bot irá apresentar as informações de navegação para o mesmo
        print('mensagem do cliente: ' + str(mensagem))
        if primeira_mensagem == True or mensagem.lower() in ('Oi','Olá', 'começar', 'menu', '/start'):
            return f'''Olá sou Cornazieri, irei lhe informar sobre o andamento diário das Ações!{os.linesep}Escolha qual empresa lhe interessa saber o valor das ações:{os.linesep}1 - Renner{os.linesep}2 - Magazine Luiza{os.linesep}3- Petrobras{os.linesep}4 - MRV{os.linesep}5 - Bradesco{os.linesep}6 - localiza{os.linesep}7 - Totvs{os.linesep}8 - Santander{os.linesep}9 - Cielo'''
       

        if mensagem == '1' or mensagem.lower() == 'renner':
            symbol = 'LREN3.SA'
            empresa = 'Lojas Renner'
        elif mensagem == '2' or mensagem.lower() == 'magazine luiza':
            symbol = 'MGLU3.SAO'
            empresa = 'Magazine Luiza'
        elif mensagem == '3' or mensagem.lower() == 'petrobras':
            symbol = 'PETR4.SAO'
            empresa = 'Petrobras'
        elif mensagem == '4' or mensagem.lower() == 'mrv':
            symbol = 'MRVE3.SA'
            empresa = 'MRV Engenharia'
        elif mensagem == '5' or mensagem.lower() == 'bradesco':
            symbol = 'BBDC4.SA'
            empresa = 'Bradesco'
        elif mensagem == '6' or mensagem.lower() == 'localiza':
            symbol = 'RENT3.SA'
            empresa = 'Localiza'
        elif mensagem == '7' or mensagem.lower() == 'totvs':
            symbol = 'TOTS3.SA'
            empresa = 'Totvs'
        elif mensagem == '8' or mensagem.lower() == 'santander':
            symbol = 'SANB11.SA'
            empresa = 'Santander'
        elif mensagem == '9' or mensagem.lower() == 'cielo':
            symbol = 'CIEL3.SA'
            empresa = 'Cielo'
        elif mensagem >= '10':
            return f'''Escolha qual empresa lhe interessa saber o valor das ações:{os.linesep}1 - Renner{os.linesep}2 - Magazine Luiza{os.linesep}3- Petrobras{os.linesep}4 - MRV{os.linesep}5 - Bradesco{os.linesep}6 - localiza{os.linesep}7 - Totvs{os.linesep}8 - Santander{os.linesep}9 - Cielo'''
        else:
            return f'''Escolha qual empresa lhe interessa saber o valor das ações:{os.linesep}1 - Renner{os.linesep}2 - Magazine Luiza{os.linesep}3- Petrobras{os.linesep}4 - MRV{os.linesep}5 - Bradesco{os.linesep}6 - localiza{os.linesep}7 - Totvs{os.linesep}8 - Santander{os.linesep}9 - Cielo'''
        
         # url da alphavantage com 3 paramestros obrigatórios passados depois da '?' e separados por '&' function(diario,semanal)/symbol(simbolo da empresa na finance)/apikey(sua key da api)
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={chave_api}'
        r = requests.get(url)
        data = r.json() #transformando a resposta em json

        #adicionando os valores do json a variaveis
        vlrabertura = data['Global Quote']['02. open'].replace(".", ",")
        maiorvlr = data['Global Quote']['03. high'].replace(".", ",")
        menorvlr = data['Global Quote']['04. low'].replace(".", ",")
        preco = data['Global Quote']['05. price'].replace(".", ",")
        previsao = data['Global Quote']['08. previous close'].replace(".", ",")
        margem = data['Global Quote']['10. change percent'].replace(".", ",")
       


        #formando a resposta para mandar a função principal e ser apresentada ao cliente através da função responder
        return f'''
                Hoje as ações da {empresa}{os.linesep}==============================={os.linesep}Abriram com valor de R${vlrabertura}   ☀️{os.linesep}==============================={os.linesep}Máxima Diária de R${maiorvlr}          📈{os.linesep}==============================={os.linesep}Mínima Diária de R${menorvlr}           📉{os.linesep}==============================={os.linesep}Estabilizou em R${preco}               ⭐{os.linesep}==============================={os.linesep}Previsão para R${previsao}                 🎰{os.linesep}==============================={os.linesep}Percentual de mudança {margem}{os.linesep}==============================='''
    
    def responder(self, resposta, chat_id): #função de resposta
        link = f'{self.url}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link)
        print("respondi: " + str(resposta))
    

bot = TelegramBot()
bot.Iniciar() 
