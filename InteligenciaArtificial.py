import threading
import openai
import requests
import pyttsx3
import json
from yarl import URL
from get_env import print_env
import PySimpleGUI as sg
import speech_recognition as sr
from textwrap import wrap
from googleapiclient.discovery import build
# import webbrowser
from tkinter import *
from collections import Counter
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
# pip install https://github.com/pyinstaller/pyinstaller/archive/refs/heads/develop.zip
# recurso tecnico

image = './imagem/micro.png'
env = print_env(['app_key'])
# configura ambiente
openai.api_key = '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'
# mofel_engine
model_engine = 'text-davinci-003'

imagemPrincipal = './imagem/othon.png'
sg.theme('DarkTeal8')
# layout = [[sg.Text('Othon de carvalho')],
#           [sg.ReadFormButton('O', button_color=sg.TRANSPARENT_BUTTON,
#                        image_filename=imagemPrincipal, image_size=(None, None), image_subsample=2, border_width=0 )],
#           ]
layout = [[sg.Button(key='O', button_color=(sg.theme_background_color()), border_width=10, mouseover_colors=('white', 'blue'),
                     use_ttk_buttons=False, pad=(0, 0), image_filename=imagemPrincipal, image_size=(None, None), size=(None, None),
                     expand_x=True, expand_y=True)]]


window1 = sg.Window('Othon de carvalho', layout=layout, location=(0, 0),
                    element_justification='c', resizable=True, use_default_focus=False,
                    size=(sg.Window.get_screen_size()), finalize=True)
window1.set_min_size((800, 600))

while True:
    event, values = window1.read()
    if event == sg.WIN_CLOSED:
        break
    else:
        if event == 'O':
            def border(elem):
                return sg.Frame('', [[elem]], background_color='red')

            # Fecha a janela atual
            window1.close()
            sg.theme('LightBlue')

            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            largura = root.winfo_screenwidth()
            altura = root.winfo_screenheight()
            larguras = int(largura)
            alturas = int(altura)
            alturasoma = alturas-300
            if alturasoma < 250:
                alturasoma = 250
            lagurasoma = larguras-300
            if lagurasoma < 250:
                lagurasoma = 250
            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
            img = Image.new(
                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
            cloud_img = Image.open(
                './imagem/04.png').resize((lagurasoma, alturasoma))
            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
            img.paste(
                cloud_img, (0, 0), mask=cloud_img)
            # Cria um objeto de desenho para a imagem
            draw = ImageDraw.Draw(
                img)
            # Define as configurações de fonte e cor para o texto
            font = ImageFont.truetype(
                'arial.ttf', 20)
            # RGBA: preto opaco
            text_color = (
                0, 0, 0, 255)
            # Define o texto a ser exibido e a posição

            text = ""
            limite = 100
            atual = 1
            novaString = ''
            for x in text:
                atual += 1
                if atual >= 70 and x == ' ':
                    novaString = novaString + '\n'
                    atual = 1
                else:
                    novaString = novaString + x
            text_position = (40, 1)
            # Desenha o texto na imagem com fundo transparente
            draw.text(
                text_position, novaString, font=font, fill=text_color)
            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
            img_file = 'cloud_temp.png'
            img.save(img_file)

            font = ("Arial", 13)
            layout = [
                [sg.Input(key='senha', size=(100, 5), font=font,
                          expand_x=True, pad=(0, 0))],

                [
                    sg.Image(filename=img_file, key='textoteste', expand_x=True,
                             expand_y=True, size=(None, None))],

                [sg.Text(' Clique sobre o icone do microfone, faça sua pergunta e aguarde a resposta da IA', size=(
                    70, 1), key='-text-', font=font)],
                [sg.Image("./imagem/4.png"), sg.Image("./imagem/4.png"),
                 sg.Button(key='Falar', metadata={'disabled': False}, button_color=('blue', sg.theme_background_color()),
                               border_width=10, mouseover_colors=(
                     'white', 'blue'), use_ttk_buttons=False, pad=(0, 0), image_filename=image, image_size=(100, 100),
                    size=(None, None), expand_x=True, expand_y=True),
                 sg.Image("./imagem/4.png"), sg.Image("./imagem/4.png")],
                [sg.Text(' ')]
            ]
            window = sg.Window('Inteligencia Artificial', layout=layout, location=(0, 0),
                               element_justification='c', resizable=True, use_default_focus=False, size=(sg.Window.get_screen_size()), finalize=True)
            window.set_min_size((1200, 800))
            while True:
                event, value = window.read()
                if event == sg.WIN_CLOSED:
                    break
                else:
                    if event == 'Falar':
                        window.Disable()
                        # cria um objeto Recognizer
                        r = sr.Recognizer()
                        # abre o microfone e grava o áudio
                        with sr.Microphone() as source:

                            audio = r.listen(source)

                        try:
                            # usa o Google Speech Recognition para converter o áudio em texto
                            text = ""
                            text = r.recognize_google(audio, language='pt-BR')
                            window['senha'].update(text.capitalize() + "?")
                        except sr.UnknownValueError:
                            # exibe uma mensagem de erro se não foi possível entender o áudio
                            # inicializar o motor de sintetização de fala
                            engine = pyttsx3.init()
                            # ajustar as características da voz
                            # velocidade da voz (padrão = 200)
                            engine.setProperty('rate', 200)
                            # tom da voz (padrão = 50)
                            engine.setProperty('pitch', 100)
                            engine.setProperty('volume', 0.9)
                            voices = engine.getProperty('voices')
                            engine.setProperty('voice', voices[0].id)
                            #   falar um texto com a voz de criança
                            texto = "Não foi possível entender o áudio"
                            engine.say(texto)
                            engine.runAndWait()

                        except sr.RequestError as e:
                            # exibe uma mensagem de erro se não foi possível entender o áudio
                            # inicializar o motor de sintetização de fala
                            engine = pyttsx3.init()
                            # ajustar as características da voz
                            # velocidade da voz (padrão = 200)
                            engine.setProperty('rate', 200)
                            # tom da voz (padrão = 50)
                            engine.setProperty('pitch', 100)
                            engine.setProperty('volume', 0.9)
                            voices = engine.getProperty('voices')
                            engine.setProperty('voice', voices[0].id)
                            #   falar um texto com a voz de criança
                            texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                e)
                            engine.say(texto)
                            engine.runAndWait()

                        if len(text) < 2:
                            # exibe uma mensagem de erro se não foi possível entender o áudio
                            # inicializar o motor de sintetização de fala
                            engine = pyttsx3.init()
                            # ajustar as características da voz
                            # velocidade da voz (padrão = 200)
                            engine.setProperty('rate', 200)
                            # tom da voz (padrão = 50)
                            engine.setProperty('pitch', 100)
                            engine.setProperty('volume', 0.9)
                            voices = engine.getProperty('voices')
                            engine.setProperty('voice', voices[0].id)
                            #   falar um texto com a voz de criança
                            texto = "Desculpe eu devo ter entendido errado!"
                            engine.say(texto)
                            engine.runAndWait()
                        else:
                            # exibe uma mensagem de erro se não foi possível entender o áudio
                            # inicializar o motor de sintetização de fala
                            engine = pyttsx3.init()
                            # ajustar as características da voz
                            # velocidade da voz (padrão = 200)
                            engine.setProperty('rate', 200)
                            # tom da voz (padrão = 50)
                            engine.setProperty('pitch', 100)
                            engine.setProperty('volume', 0.9)
                            voices = engine.getProperty('voices')
                            engine.setProperty('voice', voices[0].id)
                            #   falar um texto com a voz de criança
                            texto = "Você falou {0}, está correto?".format(
                                text)
                            engine.say(texto)
                            engine.runAndWait()
                            # cria um objeto Recognizer
                            r = sr.Recognizer()
                            # abre o microfone e grava o áudio
                            with sr.Microphone() as source:
                                audio = r.listen(source)
                            try:
                                certo = ""
                                # usa o Google Speech Recognition para converter o áudio em texto
                                certo = r.recognize_google(
                                    audio, language='pt-BR')
                            except sr.UnknownValueError:
                                # exibe uma mensagem de erro se não foi possível entender o áudio
                                # inicializar o motor de sintetização de fala
                                engine = pyttsx3.init()
                                # ajustar as características da voz
                                # velocidade da voz (padrão = 200)
                                engine.setProperty('rate', 200)
                                # tom da voz (padrão = 50)
                                engine.setProperty('pitch', 100)
                                engine.setProperty('volume', 0.9)
                                voices = engine.getProperty('voices')
                                engine.setProperty('voice', voices[0].id)
                                #   falar um texto com a voz de criança
                                texto = "Não foi possível entender o áudio"
                                engine.say(texto)
                                engine.runAndWait()
                            except sr.RequestError as e:
                                # exibe uma mensagem de erro se não foi possível entender o áudio
                                # inicializar o motor de sintetização de fala
                                engine = pyttsx3.init()
                                # ajustar as características da voz
                                # velocidade da voz (padrão = 200)
                                engine.setProperty('rate', 200)
                                # tom da voz (padrão = 50)
                                engine.setProperty('pitch', 100)
                                engine.setProperty('volume', 0.9)
                                voices = engine.getProperty('voices')
                                engine.setProperty('voice', voices[0].id)
                                #   falar um texto com a voz de criança
                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                    e)
                                engine.say(texto)
                                engine.runAndWait()
                            txto = certo
                            palavra = len(txto.split())
                            palavras = txto.split()
                            simNao = 0
                            while simNao < palavra:
                                if palavras[simNao] == "não" or palavras[simNao] == "incorreto" or palavras[simNao] == "errado":
                                    simNao = 100
                                    # exibe uma mensagem de erro se não foi possível entender o áudio
                                    # inicializar o motor de sintetização de fala
                                    engine = pyttsx3.init()
                                    # ajustar as características da voz
                                    # velocidade da voz (padrão = 200)
                                    engine.setProperty('rate', 200)
                                    # tom da voz (padrão = 50)
                                    engine.setProperty('pitch', 100)
                                    engine.setProperty('volume', 0.9)
                                    voices = engine.getProperty('voices')
                                    engine.setProperty('voice', voices[0].id)
                                    texto = "Desculpe eu devo ter entendido errado!"
                                    engine.say(texto)
                                    engine.runAndWait()

                                elif len(text) > 1 and palavras[simNao] == "sim" or len(text) > 1 and palavras[simNao] == "correto" or len(text) > 1 and palavras[simNao] == "certo" or len(text) > 1 and palavras[simNao] == "está":
                                    simNao = 100
                                    txto = text
                                    palavra = len(txto.split())
                                    palavras = txto.split()
                                    loop = 0
                                    while loop < palavra:
                                        if palavra == 1 and palavras[0] != "Oi" and palavras[0] != "Olá" and palavras[0] != "e-mail" and palavras[0] != "reclamação":
                                            loop = 100
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Por favor seje mais especifico na sua pergunta! oque você quer saber sobre {}".format(
                                                palavras)
                                            engine.say(texto)
                                            engine.runAndWait()
                                            break

                                        elif "ajude" in text and "você" in text or "ajuda" in text and "você" in text or "como" in text and "você" in text or "usar" in text and "te" in text:
                                            loop = 100
                                            window.Disable()
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            textoa = " Para facilitar o seu entendimento vamos fazer um passo a passo juntos. Por favor escolha um tema, entre perguntas relacionada a Othon de Carvalho e perguntas aleatorias sobre coisas diversas"
                                            engine.say(textoa)
                                            engine.runAndWait()
                                            import tkinter as tk
                                            root = tk.Tk()
                                            root.withdraw()
                                            largura = root.winfo_screenwidth()
                                            altura = root.winfo_screenheight()
                                            larguras = int(largura)
                                            alturas = int(altura)
                                            alturasoma = alturas-300
                                            if alturasoma < 250:
                                                alturasoma = 250
                                            lagurasoma = larguras-300
                                            if lagurasoma < 250:
                                                lagurasoma = 250
                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                            img = Image.new(
                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                            cloud_img = Image.open(
                                                './imagem/04.png').resize((lagurasoma, alturasoma))
                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                            img.paste(
                                                cloud_img, (0, 0), mask=cloud_img)
                                            # Cria um objeto de desenho para a imagem
                                            draw = ImageDraw.Draw(
                                                img)
                                            # Define as configurações de fonte e cor para o texto
                                            font = ImageFont.truetype(
                                                'arial.ttf', 18)
                                            # RGBA: preto opaco
                                            text_color = (
                                                0, 0, 0, 255)
                                            # Define o texto a ser exibido e a posição
                                            window.Refresh()
                                            text = textoa
                                            limite = 95
                                            atual = 1
                                            novaString = ''
                                            numerolinha = 1
                                            for x in text:
                                                atual += 1
                                                if atual >= 95 and x == ' ':
                                                    novaString = novaString + '\n'
                                                    atual = 1
                                                    numerolinha += 1
                                                else:
                                                    novaString = novaString + x
                                            print(alturas)
                                            text_position = (
                                                275, 1)
                                            monitor = 0
                                            if alturas == 900 and larguras == 1600:
                                                monitor = 8
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 50)
                                            elif alturas == 900 and larguras == 1440:
                                                monitor = 8
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 40)
                                            elif alturas == 800 and larguras == 1280:
                                                monitor = 6
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    200, 50)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 18)
                                            elif alturas == 864 and larguras == 1152:
                                                monitor = 7
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    180, 50)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 15)
                                            elif alturas == 600 and larguras == 800:
                                                monitor = 0
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    100, 1)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 13)
                                            elif alturas == 1080:
                                                monitor = 12
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 1440:
                                                monitor = 18
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 1200:
                                                monitor = 14
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 1600:
                                                monitor = 20
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas > 1600:
                                                monitor = 100
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 768 and larguras == 1024:
                                                monitor = 5
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    155, 35)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 13)
                                            elif alturas == 768 and larguras == 1366:
                                                monitor = 5
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    250, 35)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 18)
                                            elif alturas == 768 and larguras == 1360:
                                                monitor = 5
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    250, 35)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 18)
                                            elif alturas < 600:
                                                monitor = 0
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    100, 1)
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 13)
                                            # if numerolinha > monitor:
                                            #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                            # text_position = (
                                            #     275, 1)
                                            # Desenha o texto na imagem com fundo transparente
                                            draw.text(
                                                text_position, novaString, font=font, fill=text_color)
                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                            img_file = 'cloud_temp.png'
                                            img.save(img_file)
                                            window['textoteste'].update(
                                                img_file)
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                            try:
                                                escolha = ""
                                                escolha = r.recognize_google(
                                                    audio, language='pt-BR')
                                                window['senha'].update(
                                                    escolha.capitalize())
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()
                                            if len(escolha) > 5:
                                                txto = escolha
                                                palavra = len(txto.split())
                                                palavras1 = txto.split()
                                                loops = 0
                                                while loops < palavra:
                                                    if palavras1[loops] == "relacionada" or palavras1[loops] == "Othon de Carvalho" or palavras1[loops] == "othon" or palavras1[loops] == "carvalho" or palavras1[loops] == "Carvalho" or palavras1[loops] == "Othon":
                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = "Agora Basta Fazer sua Pergunta!"
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        r = sr.Recognizer()
                                                        with sr.Microphone() as source:
                                                            audio = r.listen(
                                                                source)
                                                        try:
                                                            perguntaburro = "Não perguntou"
                                                            perguntaburro = r.recognize_google(
                                                                audio, language='pt-BR')
                                                        except sr.UnknownValueError:
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Não foi possível entender o áudio"
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                        except sr.RequestError as e:
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                                e)
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                        valoroutro = perguntaburro.lower()
                                                        bs = valoroutro
                                                        # [:-1]
                                                        cs = len(bs.split())
                                                        ds = bs.split()
                                                        ioutro = 0
                                                        nums = []
                                                        js = 0
                                                        try:
                                                            if "Tem" in perguntaburro and "loja" in perguntaburro or "se a" in perguntaburro and "loja" in perguntaburro or "Tem" in text and "othon" in perguntaburro or "tem" in perguntaburro and "loja" in perguntaburro or "tem" in perguntaburro and "othon" in perguntaburro or "vende" in perguntaburro and "othon" in perguntaburro or "vende" in perguntaburro and "loja" in perguntaburro:

                                                                materialloja = requests.get(
                                                                    'http://192.168.3.1:8135/nome?nome='+ds[1]+" "+ds[2])
                                                        except:
                                                            materialloja = requests.get(
                                                                'http://192.168.3.1:8135/nome?nome=')
                                                        while ioutro < cs:
                                                            outro = requests.get(
                                                                'http://192.168.3.1:8135/Outrasperguntas?username='+ds[ioutro]).text
                                                            es = json.loads(
                                                                outro)
                                                            gs = 0
                                                            if len(outro) > 5:
                                                                f = es[gs]
                                                                gs += 1
                                                                nums.append(
                                                                    f['id'])

                                                                counter = Counter(
                                                                    nums).most_common()
                                                                agora = counter[0][0]
                                                                agoraSim = str(
                                                                    agora)
                                                                yss = requests.get(
                                                                    'http://192.168.3.1:8135/Outroid/'+agoraSim)
                                                            ioutro += 1
                                                        uy = cs - 1
                                                        try:
                                                            wy = requests.get(
                                                                'http://192.168.3.1:8135/Outrasperguntas?username='+ds[uy])
                                                        except:
                                                            wy = requests.get(
                                                                'http://192.168.3.1:8135/Outrasperguntas?username=')
                                                        x = requests.get(
                                                            'http://192.168.3.1:8135/responder-pergunta?pergunta='+perguntaburro).text

                                                        if "código" in perguntaburro and len(perguntaburro.split()) == 2 or "Código" in perguntaburro and len(perguntaburro.split()) == 2:
                                                            codigo = 0
                                                            codig = perguntaburro.split()
                                                            numecod = len(
                                                                codig)
                                                            while codigo < numecod:
                                                                z = requests.get(
                                                                    'http://192.168.3.1:8135/codigo/'+ds[codigo])
                                                                produto = requests.get(
                                                                    "http://192.168.3.1:8134/java/produto/"+ds[codigo])
                                                                codigo += 1
                                                        else:
                                                            z = requests.get(
                                                                'http://192.168.3.1:8135/codigo/')
                                                            produto = requests.get(
                                                                "http://192.168.3.1:8134/java/produto/")
                                                        print(z.text)
                                                        try:
                                                            if len(wy.text) > 5 and len(ds[uy]) > 3:
                                                                objetoss = json.loads(
                                                                    wy.text)
                                                                objetosss = json.loads(
                                                                    yss.text)
                                                                asdd = objetoss[0]

                                                                respostaa = asdd['outrasrespostas']
                                                                respostaaa = objetosss['outrasrespostas']
                                                            else:
                                                                respostaa = '1'
                                                                respostaaa = '2'
                                                        except:
                                                            respostaa = '1'
                                                            respostaaa = '2'

                                                        a = perguntaburro.lower()
                                                        b = a[:-1]
                                                        c = len(b.split())
                                                        d = b.split()
                                                        e = a.capitalize()
                                                        u = c - 1
                                                        horadata = 0
                                                        hora = 0
                                                        w = requests.get(
                                                            'http://192.168.3.1:8135/perguntas?username='+d[u]).text
                                                        if len(w) > 2 and d[0] == 'onde' or d[0] == "aonde":

                                                            objeto = json.loads(
                                                                w)
                                                            asd = objeto[0]
                                                            resposta = asd['resposta']
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            import tkinter as tk
                                                            root = tk.Tk()
                                                            root.withdraw()
                                                            largura = root.winfo_screenwidth()
                                                            altura = root.winfo_screenheight()
                                                            larguras = int(
                                                                largura)
                                                            alturas = int(
                                                                altura)
                                                            alturasoma = alturas-300
                                                            if alturasoma < 250:
                                                                alturasoma = 250
                                                            lagurasoma = larguras-300
                                                            if lagurasoma < 250:
                                                                lagurasoma = 250
                                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                            img = Image.new(
                                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                            cloud_img = Image.open(
                                                                './imagem/04.png').resize((lagurasoma, alturasoma))
                                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                            img.paste(
                                                                cloud_img, (0, 0), mask=cloud_img)
                                                            # Cria um objeto de desenho para a imagem
                                                            draw = ImageDraw.Draw(
                                                                img)
                                                            # Define as configurações de fonte e cor para o texto
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                            # RGBA: preto opaco
                                                            text_color = (
                                                                0, 0, 0, 255)
                                                            # Define o texto a ser exibido e a posição
                                                            window.Refresh()
                                                            text = resposta
                                                            limite = 95
                                                            atual = 1
                                                            novaString = ''
                                                            numerolinha = 1
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 95 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                            print(alturas)
                                                            text_position = (
                                                                275, 1)
                                                            monitor = 0
                                                            if alturas == 900 and larguras == 1600:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 50)
                                                            elif alturas == 900 and larguras == 1440:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 40)
                                                            elif alturas == 800 and larguras == 1280:
                                                                monitor = 6
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    200, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 864 and larguras == 1152:
                                                                monitor = 7
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    180, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 15)
                                                            elif alturas == 600 and larguras == 800:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 1080:
                                                                monitor = 12
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1440:
                                                                monitor = 18
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1200:
                                                                monitor = 14
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1600:
                                                                monitor = 20
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas > 1600:
                                                                monitor = 100
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 768 and larguras == 1024:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    155, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 768 and larguras == 1366:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 768 and larguras == 1360:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas < 600:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            # if numerolinha > monitor:
                                                            #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                            # text_position = (
                                                            #     275, 1)
                                                            # Desenha o texto na imagem com fundo transparente
                                                            draw.text(
                                                                text_position, novaString, font=font, fill=text_color)
                                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                            img_file = 'cloud_temp.png'
                                                            img.save(img_file)
                                                            window['textoteste'].update(
                                                                img_file)

                                                            texto = resposta
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            break
                                                        elif "Tem" in perguntaburro and "loja" in perguntaburro or "se a" in perguntaburro and "loja" in perguntaburro or "Tem" in perguntaburro and "othon" in perguntaburro or "tem" in perguntaburro and "loja" in perguntaburro or "tem" in perguntaburro and "othon" in perguntaburro or "vende" in perguntaburro and "othon" in perguntaburro or "vende" in perguntaburro and "loja" in perguntaburro:
                                                            loop = 100
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Irei listar os produtos com seus devidos preços, somente para a região 1 :"
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            i = 0
                                                            primeiro = json.loads(
                                                                materialloja.text)
                                                            primeiros = len(
                                                                primeiro)
                                                            textoExemplo = []
                                                            # window['mensagem'].update(
                                                            #     "")
                                                            novaString = ''
                                                            textoc = ''
                                                            while i < primeiros:
                                                                ma = primeiro[i]
                                                                nomeecommerce = ma["nomeecommerce"]
                                                                precos = ma["pvenda1"]
                                                                asd = str(
                                                                    nomeecommerce) + "    " + str(precos)+"R$"
                                                                textoExemplo.append(
                                                                    asd)

                                                                import tkinter as tk
                                                                root = tk.Tk()
                                                                root.withdraw()
                                                                largura = root.winfo_screenwidth()
                                                                altura = root.winfo_screenheight()
                                                                larguras = int(
                                                                    largura)
                                                                alturas = int(
                                                                    altura)
                                                                alturasoma = alturas-300
                                                                if alturasoma < 250:
                                                                    alturasoma = 250
                                                                lagurasoma = larguras-300
                                                                if lagurasoma < 250:
                                                                    lagurasoma = 250
                                                                # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                                img = Image.new(
                                                                    'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                                cloud_img = Image.open(
                                                                    './imagem/04.png').resize((lagurasoma, alturasoma))
                                                                # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                                img.paste(
                                                                    cloud_img, (0, 0), mask=cloud_img)
                                                                # Cria um objeto de desenho para a imagem
                                                                draw = ImageDraw.Draw(
                                                                    img)
                                                                # Define as configurações de fonte e cor para o texto
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                                # RGBA: preto opaco
                                                                text_color = (
                                                                    0, 0, 0, 255)
                                                                # Define o texto a ser exibido e a posição
                                                                window.Refresh()
                                                                textoc = textoc + \
                                                                    '\n' + \
                                                                    str(asd)
                                                                texto = "Feche a lista para fazer uma nova pergunta"
                                                                limite = 95
                                                                atual = 1
                                                                novaString = ''
                                                                numerolinha = 1
                                                                for x in text:
                                                                    atual += 1
                                                                    if atual >= 95 and x == ' ':
                                                                        novaString = novaString + '\n'
                                                                        atual = 1
                                                                        numerolinha += 1
                                                                    else:
                                                                        novaString = novaString + x
                                                                print(alturas)
                                                                text_position = (
                                                                    275, 1)
                                                                monitor = 0
                                                                if alturas == 900 and larguras == 1600:
                                                                    monitor = 8
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 50)
                                                                elif alturas == 900 and larguras == 1440:
                                                                    monitor = 8
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 40)
                                                                elif alturas == 800 and larguras == 1280:
                                                                    monitor = 6
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        200, 50)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 18)
                                                                elif alturas == 864 and larguras == 1152:
                                                                    monitor = 7
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        180, 50)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 15)
                                                                elif alturas == 600 and larguras == 800:
                                                                    monitor = 0
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        100, 1)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 13)
                                                                elif alturas == 1080:
                                                                    monitor = 12
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 1)
                                                                elif alturas == 1440:
                                                                    monitor = 18
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 1)
                                                                elif alturas == 1200:
                                                                    monitor = 14
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 1)
                                                                elif alturas == 1600:
                                                                    monitor = 20
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 1)
                                                                elif alturas > 1600:
                                                                    monitor = 100
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        275, 1)
                                                                elif alturas == 768 and larguras == 1024:
                                                                    monitor = 5
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        155, 35)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 13)
                                                                elif alturas == 768 and larguras == 1366:
                                                                    monitor = 5
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        250, 35)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 18)
                                                                elif alturas == 768 and larguras == 1360:
                                                                    monitor = 5
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        250, 35)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 18)
                                                                elif alturas < 600:
                                                                    monitor = 0
                                                                    if numerolinha > monitor:
                                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                    text_position = (
                                                                        100, 1)
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 13)
                                                                # if numerolinha > monitor:
                                                                #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                                # text_position = (
                                                                #     275, 1)
                                                                # Desenha o texto na imagem com fundo transparente
                                                                draw.text(
                                                                    text_position, texto, font=font, fill=text_color)
                                                                # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                                img_file = 'cloud_temp.png'
                                                                img.save(
                                                                    img_file)
                                                                window['textoteste'].update(
                                                                    img_file)

                                                                i += 1
                                                            sg.popup(
                                                                textoc, location=(50, 50))

                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Para validar estoque, consulte um vendedor!"
                                                            engine.say(texto)
                                                            engine.runAndWait()

                                                        elif respostaa == respostaaa and d[0] != "onde" and d[0] != "aonde":
                                                            resposta = respostaaa
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)

                                                            import tkinter as tk
                                                            root = tk.Tk()
                                                            root.withdraw()
                                                            largura = root.winfo_screenwidth()
                                                            altura = root.winfo_screenheight()
                                                            larguras = int(
                                                                largura)
                                                            alturas = int(
                                                                altura)

                                                            alturasoma = alturas-800
                                                            if alturasoma < 250:
                                                                alturasoma = 250
                                                            lagurasoma = larguras-800
                                                            if lagurasoma < 250:
                                                                lagurasoma = 250
                                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")

                                                            img = Image.new(
                                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                            cloud_img = Image.open(
                                                                './vecteezy_gray-speech-bubbles-on-transparent-background-chat-box-or_11654900_957.png').resize((lagurasoma, alturasoma))

                                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                            img.paste(
                                                                cloud_img, (0, 0), mask=cloud_img)

                                                            # Cria um objeto de desenho para a imagem
                                                            draw = ImageDraw.Draw(
                                                                img)

                                                            # Define as configurações de fonte e cor para o texto
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 20)
                                                            # RGBA: preto opaco
                                                            text_color = (
                                                                0, 0, 0, 255)

                                                            # Define o texto a ser exibido e a posição

                                                            window.Refresh()
                                                            text = resposta
                                                            limite = 100
                                                            atual = 1
                                                            novaString = ''

                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 70 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                else:
                                                                    novaString = novaString + x
                                                            text_position = (
                                                                40, 1)
                                                            monitor = 0
                                                            if alturas == 900 and larguras == 1600:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 50)
                                                            elif alturas == 900 and larguras == 1440:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 40)
                                                            elif alturas == 800 and larguras == 1280:
                                                                monitor = 6
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    200, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 864 and larguras == 1152:
                                                                monitor = 7
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    180, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 15)
                                                            elif alturas == 600 and larguras == 800:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 1080:
                                                                monitor = 12
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1440:
                                                                monitor = 18
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1200:
                                                                monitor = 14
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1600:
                                                                monitor = 20
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas > 1600:
                                                                monitor = 100
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 768 and larguras == 1024:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    155, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 768 and larguras == 1366:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 768 and larguras == 1360:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas < 600:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)

                                                            # Desenha o texto na imagem com fundo transparente
                                                            draw.text(
                                                                text_position, novaString, font=font, fill=text_color)

                                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                            img_file = 'cloud_temp.png'
                                                            img.save(img_file)
                                                            window['textoteste'].update(
                                                                img_file)

                                                            texto = resposta
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            break
                                                        elif len(x) > 40:
                                                            import tkinter as tk
                                                            root = tk.Tk()
                                                            root.withdraw()
                                                            largura = root.winfo_screenwidth()
                                                            altura = root.winfo_screenheight()
                                                            larguras = int(
                                                                largura)
                                                            alturas = int(
                                                                altura)
                                                            alturasoma = alturas-300
                                                            if alturasoma < 250:
                                                                alturasoma = 250
                                                            lagurasoma = larguras-300
                                                            if lagurasoma < 250:
                                                                lagurasoma = 250
                                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                            img = Image.new(
                                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                            cloud_img = Image.open(
                                                                './imagem/04.png').resize((lagurasoma, alturasoma))
                                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                            img.paste(
                                                                cloud_img, (0, 0), mask=cloud_img)
                                                            # Cria um objeto de desenho para a imagem
                                                            draw = ImageDraw.Draw(
                                                                img)
                                                            # Define as configurações de fonte e cor para o texto
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                            # RGBA: preto opaco
                                                            text_color = (
                                                                0, 0, 0, 255)
                                                            # Define o texto a ser exibido e a posição
                                                            window.Refresh()
                                                            text = x
                                                            limite = 95
                                                            atual = 1
                                                            novaString = ''
                                                            numerolinha = 1
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 95 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                            print(alturas)
                                                            text_position = (
                                                                275, 1)
                                                            monitor = 0
                                                            if alturas == 900 and larguras == 1600:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 50)
                                                            elif alturas == 900 and larguras == 1440:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 40)
                                                            elif alturas == 800 and larguras == 1280:
                                                                monitor = 6
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    200, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 864 and larguras == 1152:
                                                                monitor = 7
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    180, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 15)
                                                            elif alturas == 600 and larguras == 800:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 1080:
                                                                monitor = 12
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1440:
                                                                monitor = 18
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1200:
                                                                monitor = 14
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1600:
                                                                monitor = 20
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas > 1600:
                                                                monitor = 100
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 768 and larguras == 1024:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    155, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 768 and larguras == 1366:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 768 and larguras == 1360:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas < 600:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            # if numerolinha > monitor:
                                                            #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                            # text_position = (
                                                            #     275, 1)
                                                            # Desenha o texto na imagem com fundo transparente
                                                            draw.text(
                                                                text_position, novaString, font=font, fill=text_color)
                                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                            img_file = 'cloud_temp.png'
                                                            img.save(img_file)
                                                            window['textoteste'].update(
                                                                img_file)

                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = x
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            break
                                                        elif z.status_code == 200:
                                                            print("Entrou")
                                                            codprod = json.loads(
                                                                produto.content)
                                                            ob = codprod[0]
                                                            dicCovid = json.loads(
                                                                z.content)
                                                            estoqueCD = "0"
                                                            estoqueOthon = "0"
                                                            estoqueCD = ob['estoquecd']
                                                            estoqueOthon = ob['estoqueothon']
                                                            estoquedisponivel = ob['estoquedispothon']
                                                            descricao = dicCovid['nomeecommerce']
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            falar = descricao.split()
                                                            my_string = falar[0]
                                                            last_letter = my_string[-1]
                                                            if last_letter == "A":
                                                                texto = " de acordo com meus dados é uma ", falar[0], " ", falar[
                                                                    1], '\n', " a quantidade disponivel no CD é de ", estoqueCD, '\n', " o estoque Total da Othon incluindo estoque bloqueado, reservado entre outros é de ", estoqueOthon, '\n', " o estoque disponivel na Othon para vendas é de ", estoquedisponivel
                                                            else:
                                                                texto = " de acordo com meus dados é um ", falar[0], falar[
                                                                    1], '\n', " a quantidade disponivel no CD é de ", estoqueCD, '\n', " o estoque Total da Othon incluindo estoque bloqueado, reservado entre outros é de ", estoqueOthon, '\n', " o estoque disponivel na Othon para vendas é de ", estoquedisponivel
                                                            import tkinter as tk
                                                            root = tk.Tk()
                                                            root.withdraw()
                                                            largura = root.winfo_screenwidth()
                                                            altura = root.winfo_screenheight()
                                                            larguras = int(
                                                                largura)
                                                            alturas = int(
                                                                altura)
                                                            alturasoma = alturas-300
                                                            if alturasoma < 250:
                                                                alturasoma = 250
                                                            lagurasoma = larguras-300
                                                            if lagurasoma < 250:
                                                                lagurasoma = 250
                                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                            img = Image.new(
                                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                            cloud_img = Image.open(
                                                                './imagem/04.png').resize((lagurasoma, alturasoma))
                                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                            img.paste(
                                                                cloud_img, (0, 0), mask=cloud_img)
                                                            # Cria um objeto de desenho para a imagem
                                                            draw = ImageDraw.Draw(
                                                                img)
                                                            # Define as configurações de fonte e cor para o texto
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                            # RGBA: preto opaco
                                                            text_color = (
                                                                0, 0, 0, 255)
                                                            # Define o texto a ser exibido e a posição
                                                            window.Refresh()
                                                            text = texto
                                                            limite = 95
                                                            atual = 1
                                                            novaString = ''
                                                            numerolinha = 1
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 95 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + \
                                                                        str(x)
                                                            print(alturas)
                                                            print(larguras)
                                                            text_position = (
                                                                275, 20)
                                                            monitor = 0
                                                            if alturas == 900 and larguras == 1600:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 50)
                                                            elif alturas == 900 and larguras == 1440:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 40)
                                                            elif alturas == 800 and larguras == 1280:
                                                                monitor = 6
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    200, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 864 and larguras == 1152:
                                                                monitor = 7
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    180, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 15)
                                                            elif alturas == 600 and larguras == 800:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 1080:
                                                                monitor = 12
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1440:
                                                                monitor = 18
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1200:
                                                                monitor = 14
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1600:
                                                                monitor = 20
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas > 1600:
                                                                monitor = 100
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 768 and larguras == 1024:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    155, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 768 and larguras == 1366:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 768 and larguras == 1360:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas < 600:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            draw.text(
                                                                text_position, novaString, font=font, fill=text_color)
                                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                            img_file = 'cloud_temp.png'
                                                            img.save(img_file)
                                                            window['textoteste'].update(
                                                                img_file)

                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            break
                                                        else:
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Desculpe, Não entendi oque você falou, Ou a resposta não foi cadastrada neste tema!"
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            window.Enable()
                                                        break
                                                    elif palavras1[loops] == "aleatorias" or palavras1[loops] == "diversas" or palavras1[loops] == "diversa" or palavras1[loops] == "aleatorio" or palavras1[loops] == "aleatoria":
                                                        loops = 10
                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = "Você pode escolher se a resposta da sua pergunta será em vídeo ou em áudio?"
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        r = sr.Recognizer()
                                                        with sr.Microphone() as source:
                                                            audio = r.listen(
                                                                source)
                                                        try:
                                                            text = ""
                                                            text = r.recognize_google(
                                                                audio, language='pt-BR')

                                                        except sr.UnknownValueError:
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Não foi possível entender o áudio"
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            break
                                                        except sr.RequestError as e:
                                                            engine = pyttsx3.init()
                                                            engine.setProperty(
                                                                'rate', 200)
                                                            engine.setProperty(
                                                                'pitch', 100)
                                                            engine.setProperty(
                                                                'volume', 0.9)
                                                            voices = engine.getProperty(
                                                                'voices')
                                                            engine.setProperty(
                                                                'voice', voices[0].id)
                                                            texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                                e)
                                                            engine.say(texto)
                                                            engine.runAndWait()
                                                            break

                                                        audio = text.split()
                                                        tamanhoAudio = len(
                                                            audio)
                                                        tratamentoErros = 0
                                                        while tratamentoErros < tamanhoAudio:
                                                            if audio[tratamentoErros] == 'áudio':
                                                                tratamentoErros = 10
                                                                engine = pyttsx3.init()
                                                                engine.setProperty(
                                                                    'rate', 200)
                                                                engine.setProperty(
                                                                    'pitch', 100)
                                                                engine.setProperty(
                                                                    'volume', 0.9)
                                                                voices = engine.getProperty(
                                                                    'voices')
                                                                engine.setProperty(
                                                                    'voice', voices[0].id)
                                                                texto = "Agora Basta Fazer sua Pergunta!"
                                                                engine.say(
                                                                    texto)
                                                                engine.runAndWait()
                                                                r = sr.Recognizer()
                                                                with sr.Microphone() as source:
                                                                    audio = r.listen(
                                                                        source)
                                                                try:
                                                                    perguntaburro = ""
                                                                    perguntaburro = r.recognize_google(
                                                                        audio, language='pt-BR')
                                                                    window['senha'].update(
                                                                        perguntaburro.capitalize() + "?")
                                                                    a = perguntaburro.lower()
                                                                    b = a[:-1]
                                                                    c = len(
                                                                        b.split())
                                                                    d = b.split()
                                                                    e = a.capitalize()
                                                                    u = c - 1
                                                                    horadata = 0
                                                                    hora = 0
                                                                except sr.UnknownValueError:
                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = "Não foi possível entender o áudio "
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()
                                                                    break
                                                                except sr.RequestError as e:
                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                                        e)
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()
                                                                    break
                                                                while horadata < c:
                                                                    if d[horadata] == "horas":
                                                                        hora = requests.get(
                                                                            'http://192.168.3.1:8135/times').content
                                                                        horas = json.loads(
                                                                            hora)
                                                                    horadata += 1
                                                                datas = 0
                                                                data = 0
                                                                while datas < c:
                                                                    if d[datas] == "dia" or d[datas] == "data":
                                                                        data = requests.get(
                                                                            'http://192.168.3.1:8135/datess').content
                                                                        dataCerta = json.loads(
                                                                            data)
                                                                    datas += 1
                                                                if data != 0:

                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = "Hoje é dia ", dataCerta["dia"], " do ", dataCerta[
                                                                        "mes"], " de ", dataCerta["ano"]
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()
                                                                    import tkinter as tk
                                                                    root = tk.Tk()
                                                                    root.withdraw()
                                                                    largura = root.winfo_screenwidth()
                                                                    altura = root.winfo_screenheight()
                                                                    larguras = int(
                                                                        largura)
                                                                    alturas = int(
                                                                        altura)
                                                                    alturasoma = alturas-300
                                                                    if alturasoma < 250:
                                                                        alturasoma = 250
                                                                    lagurasoma = larguras-300
                                                                    if lagurasoma < 250:
                                                                        lagurasoma = 250
                                                                    # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                                    img = Image.new(
                                                                        'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                                    cloud_img = Image.open(
                                                                        './imagem/04.png').resize((lagurasoma, alturasoma))
                                                                    # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                                    img.paste(
                                                                        cloud_img, (0, 0), mask=cloud_img)
                                                                    # Cria um objeto de desenho para a imagem
                                                                    draw = ImageDraw.Draw(
                                                                        img)
                                                                    # Define as configurações de fonte e cor para o texto
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 18)
                                                                    # RGBA: preto opaco
                                                                    text_color = (
                                                                        0, 0, 0, 255)
                                                                    # Define o texto a ser exibido e a posição
                                                                    window.Refresh()
                                                                    text = texto
                                                                    limite = 95
                                                                    atual = 1
                                                                    novaString = ''
                                                                    numerolinha = 1
                                                                    for x in text:
                                                                        atual += 1
                                                                        if atual >= 95 and x == ' ':
                                                                            novaString = novaString + '\n'
                                                                            atual = 1
                                                                            numerolinha += 1
                                                                        else:
                                                                            novaString = novaString + \
                                                                                str(x)
                                                                    print(
                                                                        alturas)
                                                                    text_position = (
                                                                        275, 1)
                                                                    monitor = 0
                                                                    if alturas == 900 and larguras == 1600:
                                                                        monitor = 8
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 50)
                                                                    elif alturas == 900 and larguras == 1440:
                                                                        monitor = 8
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 40)
                                                                    elif alturas == 800 and larguras == 1280:
                                                                        monitor = 6
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            200, 50)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas == 864 and larguras == 1152:
                                                                        monitor = 7
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            180, 50)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 15)
                                                                    elif alturas == 600 and larguras == 800:
                                                                        monitor = 0
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            100, 1)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    elif alturas == 1080:
                                                                        monitor = 12
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 1440:
                                                                        monitor = 18
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 1200:
                                                                        monitor = 14
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 1600:
                                                                        monitor = 20
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas > 1600:
                                                                        monitor = 100
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 768 and larguras == 1024:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            155, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    elif alturas == 768 and larguras == 1366:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            250, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas == 768 and larguras == 1360:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            250, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas < 600:
                                                                        monitor = 0
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            100, 1)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    # if numerolinha > monitor:
                                                                    #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                                    # text_position = (
                                                                    #     275, 1)
                                                                    # Desenha o texto na imagem com fundo transparente
                                                                    draw.text(
                                                                        text_position, novaString, font=font, fill=text_color)
                                                                    # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                                    img_file = 'cloud_temp.png'
                                                                    img.save(
                                                                        img_file)
                                                                    window['textoteste'].update(
                                                                        img_file)
                                                                    break

                                                                elif hora != 0:

                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = "São ", horas["hour"], " Horas ", horas["minute"], " Minutos"
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()
                                                                    import tkinter as tk
                                                                    root = tk.Tk()
                                                                    root.withdraw()
                                                                    largura = root.winfo_screenwidth()
                                                                    altura = root.winfo_screenheight()
                                                                    larguras = int(
                                                                        largura)
                                                                    alturas = int(
                                                                        altura)
                                                                    alturasoma = alturas-300
                                                                    if alturasoma < 250:
                                                                        alturasoma = 250
                                                                    lagurasoma = larguras-300
                                                                    if lagurasoma < 250:
                                                                        lagurasoma = 250
                                                                    # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                                    img = Image.new(
                                                                        'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                                    cloud_img = Image.open(
                                                                        './imagem/04.png').resize((lagurasoma, alturasoma))
                                                                    # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                                    img.paste(
                                                                        cloud_img, (0, 0), mask=cloud_img)
                                                                    # Cria um objeto de desenho para a imagem
                                                                    draw = ImageDraw.Draw(
                                                                        img)
                                                                    # Define as configurações de fonte e cor para o texto
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 18)
                                                                    # RGBA: preto opaco
                                                                    text_color = (
                                                                        0, 0, 0, 255)
                                                                    # Define o texto a ser exibido e a posição
                                                                    window.Refresh()
                                                                    text = texto
                                                                    limite = 95
                                                                    atual = 1
                                                                    novaString = ''
                                                                    numerolinha = 1
                                                                    for x in text:
                                                                        atual += 1
                                                                        if atual >= 95 and x == ' ':
                                                                            novaString = novaString + '\n'
                                                                            atual = 1
                                                                            numerolinha += 1
                                                                        else:
                                                                            novaString = novaString + \
                                                                                str(x)
                                                                    print(
                                                                        alturas)
                                                                    text_position = (
                                                                        275, 1)
                                                                    monitor = 0
                                                                    if alturas == 900 and larguras == 1600:
                                                                        monitor = 8
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 50)
                                                                    elif alturas == 900 and larguras == 1440:
                                                                        monitor = 8
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 40)
                                                                    elif alturas == 800 and larguras == 1280:
                                                                        monitor = 6
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            200, 50)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas == 864 and larguras == 1152:
                                                                        monitor = 7
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            180, 50)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 15)
                                                                    elif alturas == 600 and larguras == 800:
                                                                        monitor = 0
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            100, 1)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    elif alturas == 1080:
                                                                        monitor = 12
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 1440:
                                                                        monitor = 18
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 1200:
                                                                        monitor = 14
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 1600:
                                                                        monitor = 20
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas > 1600:
                                                                        monitor = 100
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 768 and larguras == 1024:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            155, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    elif alturas == 768 and larguras == 1366:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            250, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas == 768 and larguras == 1360:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            250, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas < 600:
                                                                        monitor = 0
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            100, 1)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    # if numerolinha > monitor:
                                                                    #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                                    # text_position = (
                                                                    #     275, 1)
                                                                    # Desenha o texto na imagem com fundo transparente
                                                                    draw.text(
                                                                        text_position, novaString, font=font, fill=text_color)
                                                                    # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                                    img_file = 'cloud_temp.png'
                                                                    img.save(
                                                                        img_file)
                                                                    window['textoteste'].update(
                                                                        img_file)
                                                                    break
                                                                elif len(perguntaburro) > 3:
                                                                    prompt = perguntaburro
                                                                    completion = openai.Completion.create(
                                                                        engine=model_engine,
                                                                        prompt=prompt,
                                                                        max_tokens=500,
                                                                        temperature=0.5,
                                                                    )
                                                                    response = completion.choices[0].text
                                                                    # window['mensagem'].update(
                                                                    #     response)

                                                                    import tkinter as tk
                                                                    root = tk.Tk()
                                                                    root.withdraw()
                                                                    largura = root.winfo_screenwidth()
                                                                    altura = root.winfo_screenheight()
                                                                    larguras = int(
                                                                        largura)
                                                                    alturas = int(
                                                                        altura)
                                                                    alturasoma = alturas-300
                                                                    if alturasoma < 250:
                                                                        alturasoma = 250
                                                                    lagurasoma = larguras-300
                                                                    if lagurasoma < 250:
                                                                        lagurasoma = 250
                                                                    # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                                    img = Image.new(
                                                                        'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                                    cloud_img = Image.open(
                                                                        './imagem/04.png').resize((lagurasoma, alturasoma))
                                                                    # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                                    img.paste(
                                                                        cloud_img, (0, 0), mask=cloud_img)
                                                                    # Cria um objeto de desenho para a imagem
                                                                    draw = ImageDraw.Draw(
                                                                        img)
                                                                    # Define as configurações de fonte e cor para o texto
                                                                    font = ImageFont.truetype(
                                                                        'arial.ttf', 18)
                                                                    # RGBA: preto opaco
                                                                    text_color = (
                                                                        0, 0, 0, 255)
                                                                    # Define o texto a ser exibido e a posição
                                                                    window.Refresh()
                                                                    text = response
                                                                    limite = 100
                                                                    atual = 1
                                                                    novaString = ''
                                                                    numerolinha = 1
                                                                    if alturas == 768 and larguras == 1024:
                                                                        for x in text:
                                                                            atual += 1
                                                                            if atual >= 80 and x == ' ':
                                                                                novaString = novaString + '\n'
                                                                                atual = 1
                                                                                numerolinha += 1
                                                                            else:
                                                                                novaString = novaString + x
                                                                    elif alturas == 768 and larguras == 1366:
                                                                        for x in text:
                                                                            atual += 1
                                                                            if atual >= 85 and x == ' ':
                                                                                novaString = novaString + '\n'
                                                                                atual = 1
                                                                                numerolinha += 1
                                                                            else:
                                                                                novaString = novaString + x
                                                                    elif alturas == 800 and larguras == 1280:
                                                                        for x in text:
                                                                            atual += 1
                                                                            if atual >= 89 and x == ' ':
                                                                                novaString = novaString + '\n'
                                                                                atual = 1
                                                                                numerolinha += 1
                                                                            else:
                                                                                novaString = novaString + x
                                                                    elif alturas == 864 and larguras == 1152:
                                                                        for x in text:
                                                                            atual += 1
                                                                            if atual >= 89 and x == ' ':
                                                                                novaString = novaString + '\n'
                                                                                atual = 1
                                                                                numerolinha += 1
                                                                            else:
                                                                                novaString = novaString + x
                                                                    else:
                                                                        for x in text:
                                                                            atual += 1
                                                                            if atual >= 100 and x == ' ':
                                                                                novaString = novaString + '\n'
                                                                                atual = 1
                                                                                numerolinha += 1
                                                                            else:
                                                                                novaString = novaString + x
                                                                    print(
                                                                        alturas)
                                                                    text_position = (
                                                                        275, 1)
                                                                    monitor = 0
                                                                    if alturas == 900 and larguras == 1600:
                                                                        monitor = 8
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 20)
                                                                    elif alturas == 900 and larguras == 1440:
                                                                        monitor = 8
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            250, 10)
                                                                    elif alturas == 800 and larguras == 1280:

                                                                        monitor = 6
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            210, 10)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 16)
                                                                    elif alturas == 720 and larguras == 1280:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            200, 10)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 15)
                                                                    elif alturas == 768 and larguras == 1280:
                                                                        monitor = 6
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            200, 10)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 15)
                                                                    elif alturas == 864 and larguras == 1152:
                                                                        monitor = 7
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            180, 30)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 15)
                                                                    elif alturas == 600 and larguras == 800:
                                                                        monitor = 0
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            95, 35)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 12)

                                                                    elif alturas > 1600:
                                                                        monitor = 100
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            275, 1)
                                                                    elif alturas == 768 and larguras == 1024:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            150, 15)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 15)
                                                                    elif alturas == 768 and larguras == 1366:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            230, 10)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 18)
                                                                    elif alturas == 768 and larguras == 1360:
                                                                        monitor = 5
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            210, 20)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 16)
                                                                    elif alturas < 600:
                                                                        monitor = 0
                                                                        if numerolinha > monitor:
                                                                            novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                        text_position = (
                                                                            100, 1)
                                                                        font = ImageFont.truetype(
                                                                            'arial.ttf', 13)
                                                                    # if numerolinha > monitor:
                                                                    #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                                    # text_position = (
                                                                    #     275, 1)
                                                                    # Desenha o texto na imagem com fundo transparente
                                                                    draw.text(
                                                                        text_position, novaString, font=font, fill=text_color)
                                                                    # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                                    img_file = 'cloud_temp.png'
                                                                    img.save(
                                                                        img_file)
                                                                    window['textoteste'].update(
                                                                        img_file)

                                                                    # Cria a interface gráfica do usuário com o campo de entrada editável na imagem

                                                                    #   [sg.InputText(key='-INPUT-', size=(50, 1))],
                                                                    #   [sg.Button('Enviar')]]

                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = response
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()
                                                                    window.Enable()

                                                                    break
                                                                    # if videoTexto =="vídeo" or videoTexto== "em vídeo":
                                                                break
                                                            elif audio[tratamentoErros] == 'vídeo':
                                                                tratamentoErros = 10
                                                                engine = pyttsx3.init()
                                                                engine.setProperty(
                                                                    'rate', 200)
                                                                engine.setProperty(
                                                                    'pitch', 100)
                                                                engine.setProperty(
                                                                    'volume', 0.9)
                                                                voices = engine.getProperty(
                                                                    'voices')
                                                                engine.setProperty(
                                                                    'voice', voices[0].id)
                                                                texto = "Agora Basta Fazer sua Pergunta!"
                                                                engine.say(
                                                                    texto)
                                                                engine.runAndWait()
                                                                r = sr.Recognizer()
                                                                with sr.Microphone() as source:
                                                                    audio = r.listen(
                                                                        source)
                                                                try:
                                                                    perguntaburrovideo = ""
                                                                    perguntaburrovideo = r.recognize_google(
                                                                        audio, language='pt-BR')
                                                                except sr.UnknownValueError:
                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = "Não foi possível entender o áudio"
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()
                                                                except sr.RequestError as e:
                                                                    engine = pyttsx3.init()
                                                                    engine.setProperty(
                                                                        'rate', 200)
                                                                    engine.setProperty(
                                                                        'pitch', 100)
                                                                    engine.setProperty(
                                                                        'volume', 0.9)
                                                                    voices = engine.getProperty(
                                                                        'voices')
                                                                    engine.setProperty(
                                                                        'voice', voices[0].id)
                                                                    texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                                        e)
                                                                    engine.say(
                                                                        texto)
                                                                    engine.runAndWait()

                                                                import os
                                                                api_key = "AIzaSyAQnaak3RBQqHUX7Rml5nE9LV6TB1KLcJM"
                                                                youtube = build('youtube', 'v3', developerKey=api_key,
                                                                                static_discovery=False)
                                                                request = youtube.search().list(
                                                                    part="id",
                                                                    q=perguntaburrovideo,
                                                                    type="video",
                                                                    maxResults=1
                                                                )
                                                                response = request.execute()
                                                                video_id = response['items'][0]['id']['videoId']
                                                                url = "https://www.youtube.com/watch?v=" + video_id
                                                                os.system(
                                                                    "vlc "+url)

                                                                def PlayYT():
                                                                    url = "https://www.youtube.com/watch?v=" + video_id
                                                                    os.system(
                                                                        "vlc "+url + " --preferred-resolution=240")
                                                                break
                                                            tratamentoErros += 1

                                                    loops += 1
                                        elif text == "O que você pode fazer":
                                            loop = 100
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            textoa = "\n \n Eu posso responder qualquer tipo de pergunta , enviar e-mail, posso ser usada para realizar tarefas complexas, como interpretar dados, tomar decisões, aprender e adquirir conhecimentos. posso ser usada para criar sistemas que possam responder a comandos e realizar tarefas com autonomia"
                                            engine.say(textoa)
                                            engine.runAndWait()

                                            import tkinter as tk
                                            root = tk.Tk()
                                            root.withdraw()
                                            largura = root.winfo_screenwidth()
                                            altura = root.winfo_screenheight()
                                            larguras = int(largura)
                                            alturas = int(altura)
                                            alturasoma = alturas-300
                                            if alturasoma < 250:
                                                alturasoma = 250
                                            lagurasoma = larguras-300
                                            if lagurasoma < 250:
                                                lagurasoma = 250
                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                            img = Image.new(
                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                            cloud_img = Image.open(
                                                './imagem/04.png').resize((lagurasoma, alturasoma))
                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                            img.paste(
                                                cloud_img, (0, 0), mask=cloud_img)
                                            # Cria um objeto de desenho para a imagem
                                            draw = ImageDraw.Draw(
                                                img)
                                            # Define as configurações de fonte e cor para o texto
                                            font = ImageFont.truetype(
                                                'arial.ttf', 18)
                                            # RGBA: preto opaco
                                            text_color = (
                                                0, 0, 0, 255)
                                            # Define o texto a ser exibido e a posição
                                            window.Refresh()
                                            text = textoa.capitalize()
                                            limite = 95
                                            atual = 1
                                            novaString = ''
                                            numerolinha = 1
                                            for x in text:
                                                atual += 1
                                                if atual >= 95 and x == ' ':
                                                    novaString = novaString + '\n'
                                                    atual = 1
                                                    numerolinha += 1
                                                else:
                                                    novaString = novaString + x
                                            print(alturas)
                                            text_position = (
                                                275, 40)
                                            monitor = 0
                                            if alturas == 900:
                                                monitor = 8
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 40)
                                            elif alturas == 800:
                                                monitor = 6
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 600:
                                                monitor = 0
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    100, 1)
                                            elif alturas == 1080:
                                                monitor = 12
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 1440:
                                                monitor = 18
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 1200:
                                                monitor = 14
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas == 1600:
                                                monitor = 20
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas > 1600:
                                                monitor = 100
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    275, 1)
                                            elif alturas < 600:
                                                monitor = 0
                                                if numerolinha > monitor:
                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                text_position = (
                                                    100, 1)
                                            # if numerolinha > monitor:
                                            #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                            # text_position = (
                                            #     275, 1)
                                            # Desenha o texto na imagem com fundo transparente
                                            draw.text(
                                                text_position, novaString, font=font, fill=text_color)
                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                            img_file = 'cloud_temp.png'
                                            img.save(img_file)
                                            window['textoteste'].update(
                                                img_file)

                                            # window['mensagem'].update(
                                            #     textoa.capitalize())
                                            break
                                        elif palavras[0] == "Oi" or palavras[0] == "Olá":
                                            loop = 100
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Oi Tudo Bem?"
                                            engine.say(texto)
                                            engine.runAndWait()
                                            break
                                        elif palavras[loop] == "e-mail" and palavras[0] != "qual" and palavras[0] != "o":
                                            loop = 100

                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Oi Tudo Bem ? Qual é o e-mail do destinatario?"
                                            engine.say(texto)
                                            engine.runAndWait()
                                            window.Disable()
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                            try:
                                                destinatario = ""
                                                destinatario = r.recognize_google(
                                                    audio, language='pt-BR')
                                                window['senha'].update(
                                                    destinatario.capitalize())
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Qual é o assunto do E-mail?"
                                            engine.say(texto)
                                            engine.runAndWait()
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                            try:
                                                assuntos = ""
                                                assuntos = r.recognize_google(
                                                    audio, language='pt-BR')
                                                window['senha'].update(
                                                    assuntos.capitalize())
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Qual é o Corpo do e-mail?"
                                            engine.say(texto)
                                            engine.runAndWait()
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                            try:
                                                corpo = ""
                                                corpo = r.recognize_google(
                                                    audio, language='pt-BR')
                                                window['senha'].update(
                                                    corpo.capitalize())
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()

                                            try:
                                                def remove(string):
                                                    return string.replace(" ", "")
                                                email = remove(destinatario)
                                                if "@" in email:
                                                    email = email
                                                else:
                                                    email = email+"@othondecarvalho.com.br"
                                                myobj = {
                                                    "destinatario": email,
                                                    "assunto": assuntos,
                                                    "corpo": corpo,
                                                }
                                                url = 'http://192.168.3.1:8135/email'
                                                response = requests.post(
                                                    url, data=myobj)
                                                window['senha'].update(
                                                    email.capitalize())

                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "E-MAIL ENVIADO COM SUCESSO!"
                                                engine.say(texto)
                                                engine.runAndWait()

                                                import tkinter as tk
                                                root = tk.Tk()
                                                root.withdraw()
                                                largura = root.winfo_screenwidth()
                                                altura = root.winfo_screenheight()
                                                larguras = int(largura)
                                                alturas = int(altura)
                                                alturasoma = alturas-300
                                                if alturasoma < 250:
                                                    alturasoma = 250
                                                lagurasoma = larguras-300
                                                if lagurasoma < 250:
                                                    lagurasoma = 250
                                                # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                img = Image.new(
                                                    'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                cloud_img = Image.open(
                                                    './imagem/04.png').resize((lagurasoma, alturasoma))
                                                # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                img.paste(
                                                    cloud_img, (0, 0), mask=cloud_img)
                                                # Cria um objeto de desenho para a imagem
                                                draw = ImageDraw.Draw(
                                                    img)
                                                # Define as configurações de fonte e cor para o texto
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 18)
                                                # RGBA: preto opaco
                                                text_color = (
                                                    0, 0, 0, 255)
                                                # Define o texto a ser exibido e a posição
                                                window.Refresh()
                                                text = texto
                                                limite = 95
                                                atual = 1
                                                novaString = ''
                                                numerolinha = 1
                                                for x in text:
                                                    atual += 1
                                                    if atual >= 95 and x == ' ':
                                                        novaString = novaString + '\n'
                                                        atual = 1
                                                        numerolinha += 1
                                                    else:
                                                        novaString = novaString + x
                                                print(alturas)
                                                text_position = (
                                                    275, 40)
                                                monitor = 0
                                                if alturas == 900:
                                                    monitor = 8
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 50)
                                                elif alturas == 800:
                                                    monitor = 6
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 600:
                                                    monitor = 0
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        100, 1)
                                                elif alturas == 1080:
                                                    monitor = 12
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 1440:
                                                    monitor = 18
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 1200:
                                                    monitor = 14
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 1600:
                                                    monitor = 20
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas > 1600:
                                                    monitor = 100
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas < 600:
                                                    monitor = 0
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        100, 1)
                                                # if numerolinha > monitor:
                                                #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                # text_position = (
                                                #     275, 1)
                                                # Desenha o texto na imagem com fundo transparente
                                                draw.text(
                                                    text_position, novaString, font=font, fill=text_color)
                                                # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                img_file = 'cloud_temp.png'
                                                img.save(img_file)
                                                window['textoteste'].update(
                                                    img_file)

                                            except:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível enviar o e-mail"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            break
                                        elif palavras[loop] == "reclamação":
                                            loop = 100
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Oi Tudo Bem ? Qual é o tema da reclamação?"
                                            engine.say(texto)
                                            engine.runAndWait()
                                            window.Disable()
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                            try:
                                                reclamacao = ""
                                                reclamacao = r.recognize_google(
                                                    audio, language='pt-BR')
                                                # window['mensagem'].update(
                                                #     reclamacao.capitalize())
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            engine.say(texto)
                                            engine.runAndWait()
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:
                                                audio = r.listen(source)
                                            try:
                                                textoReclamacao = ""
                                                textoReclamacao = r.recognize_google(
                                                    audio, language='pt-BR')
                                                window['senha'].update(
                                                    textoReclamacao.capitalize())
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()
                                            try:
                                                myobj = {
                                                    "destinatario": "atendimento@othondecarvalho.com.br",
                                                    "assunto": reclamacao,
                                                    "corpo": textoReclamacao,
                                                }
                                                url = 'http://192.168.3.1:8135/email'
                                                response = requests.post(
                                                    url, data=myobj)

                                                import tkinter as tk
                                                root = tk.Tk()
                                                root.withdraw()
                                                largura = root.winfo_screenwidth()
                                                altura = root.winfo_screenheight()
                                                larguras = int(largura)
                                                alturas = int(altura)
                                                alturasoma = alturas-300
                                                if alturasoma < 250:
                                                    alturasoma = 250
                                                lagurasoma = larguras-300
                                                if lagurasoma < 250:
                                                    lagurasoma = 250
                                                # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                img = Image.new(
                                                    'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                cloud_img = Image.open(
                                                    './imagem/04.png').resize((lagurasoma, alturasoma))
                                                # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                img.paste(
                                                    cloud_img, (0, 0), mask=cloud_img)
                                                # Cria um objeto de desenho para a imagem
                                                draw = ImageDraw.Draw(
                                                    img)
                                                # Define as configurações de fonte e cor para o texto
                                                font = ImageFont.truetype(
                                                    'arial.ttf', 18)
                                                # RGBA: preto opaco
                                                text_color = (
                                                    0, 0, 0, 255)
                                                # Define o texto a ser exibido e a posição
                                                window.Refresh()
                                                text = "Desculpe-nos o transtorno!"
                                                limite = 95
                                                atual = 1
                                                novaString = ''
                                                numerolinha = 1
                                                for x in text:
                                                    atual += 1
                                                    if atual >= 95 and x == ' ':
                                                        novaString = novaString + '\n'
                                                        atual = 1
                                                        numerolinha += 1
                                                    else:
                                                        novaString = novaString + x
                                                print(alturas)
                                                text_position = (
                                                    275, 1)
                                                monitor = 0
                                                if alturas == 900:
                                                    monitor = 8
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 800:
                                                    monitor = 6
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 600:
                                                    monitor = 0
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        100, 1)
                                                elif alturas == 1080:
                                                    monitor = 12
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 1440:
                                                    monitor = 18
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 1200:
                                                    monitor = 14
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas == 1600:
                                                    monitor = 20
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas > 1600:
                                                    monitor = 100
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        275, 1)
                                                elif alturas < 600:
                                                    monitor = 0
                                                    if numerolinha > monitor:
                                                        novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                    text_position = (
                                                        100, 1)
                                                # if numerolinha > monitor:
                                                #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                # text_position = (
                                                #     275, 1)
                                                # Desenha o texto na imagem com fundo transparente
                                                draw.text(
                                                    text_position, novaString, font=font, fill=text_color)
                                                # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                img_file = 'cloud_temp.png'
                                                img.save(img_file)
                                                window['textoteste'].update(
                                                    img_file)

                                                # window['senha'].update(
                                                #     "Desculpe-nos o transtorno!")
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "RECLAMAÇÃO ENVIADA COM SUCESSO!"
                                                engine.say(texto)
                                                engine.runAndWait()
                                            except:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível enviar a reclamação!"
                                                engine.say(texto)
                                                engine.runAndWait()
                                                break
                                        elif palavras[0] == "assistir":
                                            loop = 100
                                            import os
                                            api_key = "AIzaSyAQnaak3RBQqHUX7Rml5nE9LV6TB1KLcJM"
                                            youtube = build('youtube', 'v3', developerKey=api_key,
                                                            static_discovery=False)
                                            request = youtube.search().list(
                                                part="id",
                                                q=text,
                                                type="video",
                                                maxResults=1
                                            )
                                            response = request.execute()
                                            video_id = response['items'][0]['id']['videoId']
                                            url = "https://www.youtube.com/watch?v=" + video_id
                                            os.system("vlc "+url)

                                            def PlayYT():
                                                url = "https://www.youtube.com/watch?v=" + video_id
                                                os.system(
                                                    "vlc "+url + " --preferred-resolution=240")
                                            break
                                        elif palavra > 1 and palavras[loop] != "Oi" and palavras[loop] != "Olá" and palavras[loop] != "e-mail" and palavras[loop] != "reclamação":
                                            loop = 100
                                            engine = pyttsx3.init()
                                            engine.setProperty('rate', 200)
                                            engine.setProperty('pitch', 100)
                                            engine.setProperty('volume', 0.9)
                                            voices = engine.getProperty(
                                                'voices')
                                            engine.setProperty(
                                                'voice', voices[0].id)
                                            texto = "Você gostaria da sua resposta em vídeo ou em áudio?"
                                            engine.say(texto)
                                            engine.runAndWait()
                                            r = sr.Recognizer()
                                            with sr.Microphone() as source:

                                                audio = r.listen(source)
                                            try:
                                                videoTexto = ""
                                                videoTexto = r.recognize_google(
                                                    audio, language='pt-BR')
                                            except sr.UnknownValueError:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível entender o áudio"
                                                engine.say(texto)
                                                engine.runAndWait()
                                                break
                                            except sr.RequestError as e:
                                                engine = pyttsx3.init()
                                                engine.setProperty('rate', 200)
                                                engine.setProperty(
                                                    'pitch', 100)
                                                engine.setProperty(
                                                    'volume', 0.9)
                                                voices = engine.getProperty(
                                                    'voices')
                                                engine.setProperty(
                                                    'voice', voices[0].id)
                                                texto = "Não foi possível completar a requisição ao Google Speech Recognition; {0}".format(
                                                    e)
                                                engine.say(texto)
                                                engine.runAndWait()
                                                break

                                            audio = videoTexto.split()
                                            tamanhoAudio = len(audio)
                                            tratamentoErro = 0
                                            while tratamentoErro < tamanhoAudio:
                                                if audio[tratamentoErro] == 'áudio':
                                                    valoroutro = text.lower()
                                                    bs = valoroutro
                                                    # [:-1]
                                                    cs = len(bs.split())
                                                    ds = bs.split()
                                                    ioutro = 0
                                                    nums = []
                                                    js = 0
                                                    try:
                                                        if "Tem" in text and "loja" in text or "se a" in text and "loja" in text or "Tem" in text and "othon" in text or "tem" in text and "loja" in text or "tem" in text and "othon" in text or "vende" in text and "othon" in text or "vende" in text and "loja" in text:

                                                            materialloja = requests.get(
                                                                'http://192.168.3.1:8135/nome?nome='+ds[1]+" "+ds[2])
                                                            print(
                                                                materialloja.status_code)
                                                    except:
                                                        materialloja = requests.get(
                                                            'http://192.168.3.1:8135/nome?nome=56')
                                                        print(
                                                            "catch", materialloja.status_code)

                                                    while ioutro < cs:
                                                        outro = requests.get(
                                                            'http://192.168.3.1:8135/Outrasperguntas?username='+ds[ioutro]).text
                                                        es = json.loads(outro)
                                                        gs = 0
                                                        if len(outro) > 5:
                                                            f = es[gs]
                                                            gs += 1
                                                            nums.append(
                                                                f['id'])

                                                            counter = Counter(
                                                                nums).most_common()
                                                            agora = counter[0][0]
                                                            agoraSim = str(
                                                                agora)
                                                            yss = requests.get(
                                                                'http://192.168.3.1:8135/Outroid/'+agoraSim)
                                                        ioutro += 1
                                                    uy = cs - 1
                                                    try:
                                                        wy = requests.get(
                                                            'http://192.168.3.1:8135/Outrasperguntas?username='+ds[uy])
                                                    except:
                                                        wy = requests.get(
                                                            'http://192.168.3.1:8135/Outrasperguntas?username=')
                                                    x = requests.get(
                                                        'http://192.168.3.1:8135/responder-pergunta?pergunta='+text+"?").text

                                                    if "código" in text and len(text.split()) == 2 or "Código" in text and len(text.split()) == 2:

                                                        codigo = 0
                                                        codig = text.split()
                                                        numecod = len(codig)
                                                        while codigo < numecod:
                                                            z = requests.get(
                                                                'http://192.168.3.1:8135/codigo/'+ds[codigo])
                                                            produto = requests.get(
                                                                "http://192.168.3.1:8134/java/produto/"+ds[codigo])
                                                            codigo += 1
                                                    else:
                                                        z = requests.get(
                                                            'http://192.168.3.1:8135/codigo/')
                                                        produto = requests.get(
                                                            "http://192.168.3.1:8134/java/produto/")
                                                    if len(wy.text) > 5 and len(ds[uy]) > 3:
                                                        objetoss = json.loads(
                                                            wy.text)
                                                        objetosss = json.loads(
                                                            yss.text)
                                                        asdd = objetoss[0]

                                                        respostaa = asdd['outrasrespostas']
                                                        respostaaa = objetosss['outrasrespostas']
                                                    else:
                                                        respostaa = '1'
                                                        respostaaa = '2'
                                                    a = text.lower()
                                                    b = a[:-1]
                                                    c = len(b.split())
                                                    d = b.split()
                                                    e = a.capitalize()
                                                    u = c - 1
                                                    horadata = 0
                                                    hora = 0
                                                    w = requests.get(
                                                        'http://192.168.3.1:8135/perguntas?username='+d[u]).text

                                                    # Covid = json.loads(z.content)
                                                    while horadata < c:
                                                        if d[horadata] == "horas":
                                                            hora = requests.get(
                                                                'http://192.168.3.1:8135/times').content
                                                            horas = json.loads(
                                                                hora)
                                                        horadata += 1
                                                    datas = 0
                                                    data = 0
                                                    while datas < c:
                                                        if d[datas] == "dia" or d[datas] == "data":
                                                            data = requests.get(
                                                                'http://192.168.3.1:8135/datess').content
                                                            dataCerta = json.loads(
                                                                data)
                                                        datas += 1

                                                    if data != 0:

                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = "Hoje é dia ", dataCerta["dia"], " do ", dataCerta[
                                                            "mes"], " de ", dataCerta["ano"]
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = texto
                                                        limite = 95
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 95 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                                numerolinha += 1
                                                            else:
                                                                novaString = novaString + \
                                                                    str(x)
                                                        print(alturas)
                                                        text_position = (
                                                            275, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        # if numerolinha > monitor:
                                                        #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                        # text_position = (
                                                        #     275, 1)
                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)
                                                        break

                                                    elif "Tem" in text and "loja" in text or "se a" in text and "loja" in text or "Tem" in text and "othon" in text or "tem" in text and "loja" in text or "tem" in text and "othon" in text or "vende" in text and "othon" in text or "vende" in text and "loja" in text:
                                                        loop = 100
                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = "Irei listar os produtos com seus devidos preços, somente para a região 1 :"
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        i = 0
                                                        primeiro = json.loads(
                                                            materialloja.text)
                                                        primeiros = len(
                                                            primeiro)
                                                        textoExemplo = []
                                                        # window['mensagem'].update( O que é você?
                                                        #     "")
                                                        novaString = ''
                                                        textoc = ''
                                                        while i < primeiros:
                                                            ma = primeiro[i]
                                                            nomeecommerce = ma["nomeecommerce"]
                                                            precos = ma["pvenda1"]
                                                            asd = str(
                                                                nomeecommerce) + "    " + str(precos)+"R$"
                                                            textoExemplo.append(
                                                                asd)

                                                            import tkinter as tk
                                                            root = tk.Tk()
                                                            root.withdraw()
                                                            largura = root.winfo_screenwidth()
                                                            altura = root.winfo_screenheight()
                                                            larguras = int(
                                                                largura)
                                                            alturas = int(
                                                                altura)
                                                            alturasoma = alturas-300
                                                            if alturasoma < 250:
                                                                alturasoma = 250
                                                            lagurasoma = larguras-300
                                                            if lagurasoma < 250:
                                                                lagurasoma = 250
                                                            # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                            img = Image.new(
                                                                'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                            cloud_img = Image.open(
                                                                './imagem/04.png').resize((lagurasoma, alturasoma))
                                                            # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                            img.paste(
                                                                cloud_img, (0, 0), mask=cloud_img)
                                                            # Cria um objeto de desenho para a imagem
                                                            draw = ImageDraw.Draw(
                                                                img)
                                                            # Define as configurações de fonte e cor para o texto
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                            # RGBA: preto opaco
                                                            text_color = (
                                                                0, 0, 0, 255)
                                                            # Define o texto a ser exibido e a posição
                                                            window.Refresh()
                                                            textoc = textoc + \
                                                                '\n' + str(asd)
                                                            texto = "Feche a lista para fazer uma nova pergunta"
                                                            limite = 95
                                                            atual = 1
                                                            novaString = ''
                                                            numerolinha = 1
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 95 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                            print(alturas)
                                                            text_position = (
                                                                275, 1)
                                                            monitor = 0
                                                            if alturas == 900 and larguras == 1600:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 50)
                                                            elif alturas == 900 and larguras == 1440:
                                                                monitor = 8
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 40)
                                                            elif alturas == 800 and larguras == 1280:
                                                                monitor = 6
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    200, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 864 and larguras == 1152:
                                                                monitor = 7
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    180, 50)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 15)
                                                            elif alturas == 600 and larguras == 800:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 1080:
                                                                monitor = 12
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1440:
                                                                monitor = 18
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1200:
                                                                monitor = 14
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 1600:
                                                                monitor = 20
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas > 1600:
                                                                monitor = 100
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    275, 1)
                                                            elif alturas == 768 and larguras == 1024:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    155, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            elif alturas == 768 and larguras == 1366:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas == 768 and larguras == 1360:
                                                                monitor = 5
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    250, 35)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 18)
                                                            elif alturas < 600:
                                                                monitor = 0
                                                                if numerolinha > monitor:
                                                                    novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                                text_position = (
                                                                    100, 1)
                                                                font = ImageFont.truetype(
                                                                    'arial.ttf', 13)
                                                            # if numerolinha > monitor:
                                                            #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                            # text_position = (
                                                            #     275, 1)
                                                            # Desenha o texto na imagem com fundo transparente
                                                            draw.text(
                                                                text_position, texto, font=font, fill=text_color)
                                                            # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                            img_file = 'cloud_temp.png'
                                                            img.save(img_file)
                                                            window['textoteste'].update(
                                                                img_file)

                                                            i += 1
                                                        sg.popup(
                                                            textoc, location=(50, 50))

                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = "Para validar estoque, consulte um vendedor!"
                                                        engine.say(texto)
                                                        engine.runAndWait()

                                                    elif len(w) > 2 and d[0] == 'onde' or d[0] == "aonde":

                                                        objeto = json.loads(w)
                                                        asd = objeto[0]
                                                        resposta = asd['resposta']
                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)

                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = resposta
                                                        limite = 95
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 95 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                                numerolinha += 1
                                                            else:
                                                                novaString = novaString + x
                                                        print(alturas)
                                                        text_position = (
                                                            275, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        # if numerolinha > monitor:
                                                        #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                        # text_position = (
                                                        #     275, 1)
                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)

                                                        texto = resposta
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = texto
                                                        limite = 95
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 95 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                                numerolinha += 1
                                                            else:
                                                                novaString = novaString + \
                                                                    str(x)
                                                        print(alturas)
                                                        text_position = (
                                                            275, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        # if numerolinha > monitor:
                                                        #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                        # text_position = (
                                                        #     275, 1)
                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)
                                                        break
                                                    elif hora != 0:

                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = "São ", horas["hour"], " Horas ", horas["minute"], " Minutos"
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = texto
                                                        limite = 95
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 95 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                                numerolinha += 1
                                                            else:
                                                                novaString = novaString + \
                                                                    str(x)
                                                        print(alturas)
                                                        text_position = (
                                                            275, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        # if numerolinha > monitor:
                                                        #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                        # text_position = (
                                                        #     275, 1)
                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)
                                                        break

                                                    elif respostaa == respostaaa and d[0] != "onde" and d[0] != "aonde":
                                                        resposta = respostaaa
                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)

                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)

                                                        alturasoma = alturas-800
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-800
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")

                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './vecteezy_gray-speech-bubbles-on-transparent-background-chat-box-or_11654900_957.png').resize((lagurasoma, alturasoma))

                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)

                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)

                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 20)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)

                                                        # Define o texto a ser exibido e a posição

                                                        window.Refresh()
                                                        text = resposta
                                                        limite = 100
                                                        atual = 1
                                                        novaString = ''

                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 70 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                            else:
                                                                novaString = novaString + x
                                                        text_position = (40, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)

                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)

                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)

                                                        texto = resposta
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        break
                                                    elif len(x) > 40:

                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = x
                                                        limite = 95
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 95 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                                numerolinha += 1
                                                            else:
                                                                novaString = novaString + x
                                                        print(alturas)
                                                        text_position = (
                                                            275, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        # if numerolinha > monitor:
                                                        #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                        # text_position = (
                                                        #     275, 1)
                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)

                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = text
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        break
                                                    elif z.status_code == 200:
                                                        codprod = json.loads(
                                                            produto.content)
                                                        ob = codprod[0]
                                                        dicCovid = json.loads(
                                                            z.content)
                                                        estoqueCD = "0"
                                                        estoqueOthon = "0"
                                                        descricao = "0"
                                                        estoqueCD = ob['estoquecd']
                                                        estoqueOthon = ob['estoqueothon']
                                                        estoquedisponivel = ob['estoquedispothon']
                                                        descricao = dicCovid['nomeecommerce']
                                                        descricoes = dicCovid['descricao']
                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 190)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        try:
                                                            falar = descricao.split()
                                                        except:
                                                            falar = descricoes.split()
                                                        my_string = falar[0]
                                                        last_letter = my_string[-1]
                                                        if last_letter == "A":
                                                            texto = " de acordo com meus dados é uma ", falar[0], falar[
                                                                1], "\n a quantidade disponivel no CD é de ", estoqueCD, "\n o estoque Total da Othon incluindo estoque bloqueado, reservado entre outros é de ", estoqueOthon, "\n o estoque disponivel na Othon para vendas é de ", estoquedisponivel
                                                        else:
                                                            texto = " de acordo com meus dados é um ", falar[0], falar[
                                                                1], "\n a quantidade disponivel no CD é de ", estoqueCD, "\n o estoque Total da Othon incluindo estoque bloqueado, reservado entre outros é de ", estoqueOthon, "\n o estoque disponivel na Othon para vendas é de ", estoquedisponivel

                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = texto
                                                        limite = 95
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        for x in text:
                                                            atual += 1
                                                            if atual >= 95 and x == ' ':
                                                                novaString = novaString + '\n'
                                                                atual = 1
                                                                numerolinha += 1
                                                            else:
                                                                novaString = novaString + \
                                                                    str(x)
                                                        print(alturas)
                                                        print(larguras)
                                                        text_position = (
                                                            275, 20)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 50)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 40)
                                                        elif alturas == 800 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 50)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 1080:
                                                            monitor = 12
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1440:
                                                            monitor = 18
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1200:
                                                            monitor = 14
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 1600:
                                                            monitor = 20
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                155, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        break
                                                    else:
                                                        prompt = text+"?"
                                                        completion = openai.Completion.create(
                                                            engine=model_engine,
                                                            prompt=prompt,
                                                            max_tokens=500,
                                                            temperature=0.5,
                                                        )
                                                        response = completion.choices[0].text
                                                        # window['mensagem'].update(
                                                        #     response)

                                                        import tkinter as tk
                                                        root = tk.Tk()
                                                        root.withdraw()
                                                        largura = root.winfo_screenwidth()
                                                        altura = root.winfo_screenheight()
                                                        larguras = int(largura)
                                                        alturas = int(altura)
                                                        alturasoma = alturas-300
                                                        if alturasoma < 250:
                                                            alturasoma = 250
                                                        lagurasoma = larguras-300
                                                        if lagurasoma < 250:
                                                            lagurasoma = 250
                                                        # sg.popup(f"Largura do monitor: {largura}\nAltura do monitor: {altura}")
                                                        img = Image.new(
                                                            'RGBA', (lagurasoma, alturasoma), (0, 0, 0, 0))
                                                        cloud_img = Image.open(
                                                            './imagem/04.png').resize((lagurasoma, alturasoma))
                                                        # Copia a imagem da nuvem de conversa para a imagem com fundo transparente
                                                        img.paste(
                                                            cloud_img, (0, 0), mask=cloud_img)
                                                        # Cria um objeto de desenho para a imagem
                                                        draw = ImageDraw.Draw(
                                                            img)
                                                        # Define as configurações de fonte e cor para o texto
                                                        font = ImageFont.truetype(
                                                            'arial.ttf', 18)
                                                        # RGBA: preto opaco
                                                        text_color = (
                                                            0, 0, 0, 255)
                                                        # Define o texto a ser exibido e a posição
                                                        window.Refresh()
                                                        text = response
                                                        limite = 100
                                                        atual = 1
                                                        novaString = ''
                                                        numerolinha = 1
                                                        if alturas == 768 and larguras == 1024:
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 80 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                        elif alturas == 768 and larguras == 1366:
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 85 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                        elif alturas == 800 and larguras == 1280:
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 89 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                        elif alturas == 864 and larguras == 1152:
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 89 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                        else:
                                                            for x in text:
                                                                atual += 1
                                                                if atual >= 100 and x == ' ':
                                                                    novaString = novaString + '\n'
                                                                    atual = 1
                                                                    numerolinha += 1
                                                                else:
                                                                    novaString = novaString + x
                                                        print(alturas)
                                                        text_position = (
                                                            275, 1)
                                                        monitor = 0
                                                        if alturas == 900 and larguras == 1600:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 20)
                                                        elif alturas == 900 and larguras == 1440:
                                                            monitor = 8
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                250, 10)
                                                        elif alturas == 800 and larguras == 1280:

                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                210, 10)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 16)
                                                        elif alturas == 720 and larguras == 1280:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 10)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 768 and larguras == 1280:
                                                            monitor = 6
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                200, 10)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 864 and larguras == 1152:
                                                            monitor = 7
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                180, 30)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 600 and larguras == 800:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                95, 35)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 12)
                                                        elif alturas > 1600:
                                                            monitor = 100
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                275, 1)
                                                        elif alturas == 768 and larguras == 1024:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                150, 15)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 15)
                                                        elif alturas == 768 and larguras == 1366:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                230, 10)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 18)
                                                        elif alturas == 768 and larguras == 1360:
                                                            monitor = 5
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                210, 20)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 16)
                                                        elif alturas < 600:
                                                            monitor = 0
                                                            if numerolinha > monitor:
                                                                novaString = "\n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição \n nesta resolução"
                                                            text_position = (
                                                                100, 1)
                                                            font = ImageFont.truetype(
                                                                'arial.ttf', 13)
                                                        # if numerolinha > monitor:
                                                        #      novaString = "\n \n Não é possivel exibir a resposta desta pergunta!\n a resposta ultrapassa a quantidade de linhas permitidas para a exibição"
                                                        # text_position = (
                                                        #     275, 1)
                                                        # Desenha o texto na imagem com fundo transparente
                                                        draw.text(
                                                            text_position, novaString, font=font, fill=text_color)
                                                        # Salva a imagem com a nuvem de conversa e o texto como um arquivo temporário
                                                        img_file = 'cloud_temp.png'
                                                        img.save(img_file)
                                                        window['textoteste'].update(
                                                            img_file)

                                                        # Cria a interface gráfica do usuário com o campo de entrada editável na imagem

                                                        #   [sg.InputText(key='-INPUT-', size=(50, 1))],
                                                        #   [sg.Button('Enviar')]]

                                                        engine = pyttsx3.init()
                                                        engine.setProperty(
                                                            'rate', 200)
                                                        engine.setProperty(
                                                            'pitch', 100)
                                                        engine.setProperty(
                                                            'volume', 0.9)
                                                        voices = engine.getProperty(
                                                            'voices')
                                                        engine.setProperty(
                                                            'voice', voices[0].id)
                                                        texto = response
                                                        engine.say(texto)
                                                        engine.runAndWait()
                                                        window.Enable()
                                                        break
                                                        # if videoTexto =="vídeo" or videoTexto== "em vídeo":
                                                elif audio[tratamentoErro] == "vídeo":
                                                    # if event == "Assistir Video":
                                                    import os
                                                    # path_json = './imagem/rest.json'
                                                    # with open(path_json) as f:
                                                    #     service = json.load(f)
                                                    # substitua a chave da API com sua própria chave
                                                    api_key = "AIzaSyAQnaak3RBQqHUX7Rml5nE9LV6TB1KLcJM"
                                                    youtube = build('youtube', 'v3', developerKey=api_key,
                                                                    static_discovery=False)
                                                    # pesquisa por vídeos com a palavra-chave "python tutorial"
                                                    request = youtube.search().list(
                                                        part="id",
                                                        q=text,
                                                        type="video",
                                                        maxResults=1
                                                    )
                                                    response = request.execute()
                                                    # obtém o ID do vídeo
                                                    video_id = response['items'][0]['id']['videoId']
                                                    # reproduz o vídeo no navegador
                                                    # webbrowser.open("https://www.youtube.com/watch?v=" + video_id)
                                                    url = "https://www.youtube.com/watch?v=" + video_id
                                                    # url = video.get()
                                                    os.system("vlc "+url)
                                                    # Defina a URL do vídeo que você deseja reproduzir
                                                    # Defina a URL do vídeo que você deseja reproduzir

                                                    def PlayYT():
                                                        url = "https://www.youtube.com/watch?v=" + video_id
                                                        # url = video.get()
                                                        os.system(
                                                            "vlc "+url + " --preferred-resolution=240")
                                                        # def Sair():
                                                        #   gui.destroy()
                                                        # btn_play = Button(gui, text="Play", command=PlayYT)
                                                        # btn_play.pack()
                                                        # btn_sair = Button(gui, text="Sair", command=Sair)
                                                    break
                                                tratamentoErro += 1
                                            break
                                        loop += 1
                                else:
                                    engine = pyttsx3.init()
                                    engine.setProperty('rate', 200)
                                    engine.setProperty('pitch', 100)
                                    engine.setProperty('volume', 0.9)
                                    voices = engine.getProperty('voices')
                                    engine.setProperty('voice', voices[0].id)
                                    texto = ""
                                    engine.say(texto)
                                    engine.runAndWait()
                                    window.Enable()
                                simNao += 1
                    else:
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 200)
                        engine.setProperty('pitch', 100)
                        engine.setProperty('volume', 0.9)
                        voices = engine.getProperty('voices')
                        engine.setProperty('voice', voices[0].id)
                        texto = "Não entendi oque você falou !"
                        engine.say(texto)
                        engine.runAndWait()
                    window.Enable()
