import webbrowser
import flet
from flet import *
import flet as ft
from time import sleep
import pyperclip
import pyttsx3
import random
import time 
import json
from webbrowser import open_new_tab
import os
import pyautogui
import difflib
from datetime import datetime
import sqlite3
from unidecode import unidecode
import re


dateNow = datetime.now()
day = dateNow.strftime("%d/%m/%Y")

weekend = dateNow.strftime("%A")

if weekend == "Saturday":
    weekend = " num sábado"

if weekend == "Sunday":
    weekend = "num domingo"

if weekend == "Monday":
    weekend = "numa segunda-feira"

if weekend == "Tuesday":
    weekend = "numa terça-feira"

if  weekend == "Wednesday":
    weekend = "numa quarta-feira"

if weekend == "Tursday":
    weekend = "numa quinta-feira"

if weekend == "Friday":
    weekend = "numa sexta-feira"

# Função para carregar as perguntas e respostas do arquivo JSON
def carregar_perguntas_respostas(arquivo_json):
    with open(arquivo_json, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados["perguntas_respostas"]

perguntas_respostas = carregar_perguntas_respostas("faq_fatGonga.json")

def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()


class inicialPage(View):
    def __init__(self, page):
        super(inicialPage, self).__init__(
            route="/inicial",
            padding=50,
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#16242f"
            # bgcolor="#ffffff"
        )

        self.page = page
        self.process = ProgressBar(color="#00ffb4", height=3, bgcolor="#39444d", visible=True, width=200)


        self.controls = [
            Column([
                Column([
                    Container(
                        width=100,
                        height=100,
                        border_radius=100,
                        bgcolor="#ffffff",
                        image_src="image/Bot Icon.gif",
                        border=border.all(6, "#01d194")
                    ),
                    Text("Kawaii".upper(), size=14, text_align="center"),
                ], horizontal_alignment="center")
                ,
                Text("Olá, bom ter você aqui!".upper(), size=40, text_align="center"),
                Column([
                    self.process,
                    Text("aguarde um minuto...!", size=10),
                ], horizontal_alignment="center", spacing=10)
            ], horizontal_alignment="center", spacing=150)
        ]

class choosePage(View):
    def __init__(self, page):
        super(choosePage, self).__init__(
            route="/choose-page",
            padding=50,
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#16242f"
            # bgcolor="#ffffff"
        )

        self.page = page

        self.controls = [
            Row(
                alignment="center",
                controls=[
                Container(
                    Column([

                        Column([
                            Text("Chat".upper(), size=30),
                            Divider(height=10, color="transparent"),
                            Text("Entre em contacto com a kawaii, e desfruta,de uma iteração com o nosso chatbot kawaii."),
                        ]),
                        Row([
                            IconButton(icon=icons.ARROW_RIGHT_ALT, on_click=self.enter_to_chatBot)
                        ], alignment="end")

                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor="#08151e",
                    width=300,
                    height=400,
                    #col={"xl": 6, "xxl": 6, "lg": 6},
                    padding=20,
                    border_radius=4,
                    border=border.all(.5, color="#046649")
                ),
                Container(
                    Column([
                        Column([
                            Text("Site".upper(), size=30),
                            Divider(height=10, color="transparent"),
                            Text("Site institucional não disponível.",)
                        ]),
                        Row([
                            IconButton(icon=icons.ARROW_RIGHT_ALT, disabled=True)
                        ], alignment="end")
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor="#08151e",
                    width=300,
                    height=400,
                    #col={"xl": 6, "xxl": 6, "lg": 6},
                    padding=20,
                    border_radius=4,
                    border=border.all(.5, color="#046649")
                ),
            ])
        ]

    def enter_to_chatBot(self, e):
        self.page.go("/chat-here")
        #self.page.update()

# Pagina de conversação entre o usuario e o chat        

class mainPage(View):
    def __init__(self, page):
        super(mainPage, self).__init__(
            route="/chat-here",
            padding=padding.symmetric(0, 0),
            horizontal_alignment="center",
            vertical_alignment="center",
            bgcolor="#16242f",
            scroll=ScrollMode.ALWAYS,
            auto_scroll=ScrollMode.ALWAYS
        )

        self.page = page

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.EXIT_TO_APP, bgcolor="#01d194", on_click=lambda _:self.page.go("/choose-page"),
        )

        self.alert = SnackBar(
            content=Text("Texto copiado com sucesso", color="white"),
            duration=2000,
            bgcolor="#01d194",
            behavior=SnackBarBehavior.FIXED,
            # width=200,
        )

        self.process = ProgressBar(col={"xl": 6, "xxl": 6, "lg": 6}, color="#00ffb4", height=2, bgcolor="#16242f", visible=False)

        self.text = "Olá, eu sou a kawaii, no que posso te ajudar"
        self.text_answer = Text(value="Olá, eu sou a kawaii, no que posso te ajudar?", selectable=True)
        self.text_ask = Text(f"{os.getlogin()}:")
        self.icon_copy = IconButton(icon=icons.COPY, icon_size=16, icon_color="whitesmoke", on_click=self.copy, tooltip="Cópia")


        # Campo de fazer as perguntas ----------------------------------------
        # ---------------------------------------------------------------------
        self.space_ask = TextField(
            # hint_text="Mensagem",
            label="Mensagem", 
            border_width=.7, 
            border_color="whitesmoke", 
            bgcolor="#08151e", 
            col={"xl": 6, "xxl": 6, "lg": 6},
            border_radius=4,
            suffix_icon=icons.SEARCH,
            on_focus=self.hover,
            on_submit=self.chatting,
            autocorrect=True,
            max_length=50,
        )

        self.op_1 = Text("Como posso entrar com contacto com a secretária?")
        self.op_2 = Text("Que é você, kawaii?")

        self.controls = [
            Column([
                Column([
                    Container(
                        width=100,
                        height=100,
                        border_radius=100,
                        bgcolor="#ffffff",
                        image_src="image/Bot Icon.gif",
                        border=border.all(6, "#01d194")
                    ),
                ], horizontal_alignment="center"),

                Text("O que desejas saber ?".upper(), size=40, text_align="center"),
                Text("Seja bem vindo a sua instituição, noque posso ajuder?...!", size=10, text_align="center"),
                

                ResponsiveRow([
                    Text("Perguntas frequêntes?".upper(), size=13, text_align="center", weight="w400"),
                ], alignment="center"),


                # Campo as perguntas frequentes

                ResponsiveRow([

                    Container(
                        Column([
                            Row([
                                Row([
                                    self.op_1,
                                ], width=250, wrap=True),
                                IconButton(icon=icons.ARROW_DROP_DOWN_SHARP, on_click=self.op1)
                            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor="#08151e",
                        width=300,
                        col={"xl": 3, "xxl": 3, "lg": 3, "sm": 5},
                        padding=20,
                        border_radius=4,
                        border=border.all(.5, color="#046649"),
                    ),

                    Container(
                        Column([
                            Row([
                                Row([
                                    self.op_2,
                                ], width=250, wrap=True),
                                IconButton(icon=icons.ARROW_DROP_DOWN_SHARP, on_click=self.op2)
                            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor="#08151e",
                        width=300,
                        col={"xl": 3, "xxl": 3, "lg": 3, "sm": 5},
                        padding=20,
                        border_radius=4,
                        border=border.all(.5, color="#046649")
                    ),

                ], alignment="center"),

                Divider(thickness=40, color=colors.TRANSPARENT),


                # Campo de conversação do usuário e o kawaii

                ResponsiveRow([
                    Container(
                        Column([
                            Row([
                                Container(
                                    Row([
                                        Text("M", weight="w900")
                                    ], alignment="center"),
                                    width=30,
                                    height=30,
                                    border_radius=100,
                                    bgcolor="#414b53",
                                    #image_src="image/Bot Icon.gif",
                                    border=border.all(.1, "#01d194")
                                ),
                                self.text_ask
                            ], wrap=True),
                            Divider(color="#414b53"),
                            Row([
                                Container(
                                    width=30,
                                    height=30,
                                    border_radius=100,
                                    bgcolor="#ffffff",
                                    image_src="image/Bot Icon.gif",
                                    border=border.all(.1, "#01d194")
                                ),
                                self.text_answer
                            ], wrap=True),
                        ]),
                        bgcolor="#08151e",
                        col={"xl": 6, "xxl": 6, "lg": 6},
                        padding=20,
                        border_radius=4,
                        border=border.all(1, color="#046649")
                    ),
                    #Divider(height=4, color="transparent"),
                    #Row([ Text("MENU DE OPÇÕES".upper()) ], alignment="center"),
                    #Divider(height=4, color="transparent"),

                    # Botões que estão por baixo da caixa de resposta

                    ResponsiveRow([
                        Container(
                            Row([
                                ElevatedButton(icon=icons.SCREENSHOT_MONITOR, text="Screenshot", bgcolor="#046649", color="white", on_click=self.screenshot, style=ButtonStyle(shape={"": RoundedRectangleBorder(radius=3)})),
                                self.icon_copy,
                                IconButton(icon=icons.MIC, icon_size=16, icon_color="whitesmoke", on_click=self.voice, tooltip="Áudio"),
                                # ElevatedButton(icon=icons.EXIT_TO_APP, text="Sair", bgcolor="#08151e", color="white", on_click=self.goout, style=ButtonStyle(shape={"": RoundedRectangleBorder(radius=3)})),
                                ElevatedButton(icon=icons.EMOJI_EMOTIONS, text="Emojis", bgcolor="#046649", color="white", on_click=self.show_emoji, style=ButtonStyle(shape={"": RoundedRectangleBorder(radius=3)})),
                            ], wrap=True, alignment=MainAxisAlignment.START),
                            #bgcolor="#046649",
                            col={"xl": 6, "xxl": 6, "lg": 6},
                            padding=0,
                            border_radius=4,
                            #border=border.all(1, color="#046649")
                        ),
                    ], alignment="center")
                ], alignment="center"),


                Column([], height=30),

                # Caixa de pergunta e resposta
                
                ResponsiveRow([
                    self.space_ask,
                    ResponsiveRow([
                        self.process
                    ], alignment="center"),

                ], alignment="center"),

            ], horizontal_alignment="center", spacing=10)
        ]

    def hover(self, e):
        self.icon_copy.icon = icons.COPY
        self.icon_copy.icon_color = "whitesmoke"
        self.page.update()

    def goout(self, e):
        self.page.go("/choose-page")
        #self.page.update()

    def copy(self, e):
        pyperclip.copy(self.text_answer.value)
        self.icon_copy.icon = icons.CHECK
        self.icon_copy.icon_color = "#046649"
        self.page.dialog = self.alert
        self.alert.open = True
        self.page.update()


    # Função para ler o texto
    def voice(self, e):
        self.process.visible = True
        if self.process.visible == True:
            text_to_speech(self.text)
            self.process.visible = False
        self.page.update()

    # Função para fazer o screenshot
    def screenshot(self, e):
        time.sleep(1)
        pyautogui.hotkey('win', 'prtSc')

    # Função para apresentar o emoji
    def show_emoji(self, e):
        # Espera um segundo antes de simular o pressionamento das teclas
        time.sleep(1)
        self.space_ask.autofocus = True
        self.space_ask.focus()
        # Simula o pressionamento das teclas Win + .
        pyautogui.hotkey('win', '.')
        self.page.update()

    def letra(self, letrin):
        print("Chatbot: ", end="")
        for letra in letrin:
            print(f"{letra}", end="", flush=True)
            time.sleep(0.05)  # Ajuste o intervalo de tempo conforme desejado
        print()  # Nova linha após a resposta completa

    def op1(self, e):
        self.space_ask.value = self.op_1.value
        self.chatting(e)
        pass

    def op2(self, e):
        self.space_ask.value = self.op_2.value
        self.chatting(e)
        pass

    # Função para pré-processar o texto
    def preprocessar_texto(self, texto):
        texto = texto.lower()
        texto = unidecode(texto)
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto

    def encontrar_resposta(self, pergunta_usuario, perguntas_respostas):
        pergunta_usuario = self.preprocessar_texto(pergunta_usuario)
        todas_perguntas = []
        mapa_perguntas = {}

        for item in perguntas_respostas:
            perguntas = [item["pergunta"]] + item.get("sinonimos", [])
            perguntas = [self.preprocessar_texto(pergunta) for pergunta in perguntas]
            todas_perguntas.extend(perguntas)
            for pergunta in perguntas:
                mapa_perguntas[pergunta] = item["resposta"]

        correspondencia = difflib.get_close_matches(pergunta_usuario, todas_perguntas, n=1, cutoff=0.6)

        if correspondencia:
            pergunta_correspondente = correspondencia[0]
            return mapa_perguntas[pergunta_correspondente]

        return "Desculpe, não tenho uma resposta para essa pergunta."

    def chatting(self, e):
        entrada = self.space_ask.value
        self.text_ask.value = f"{self.space_ask.value}"
        resposta = self.encontrar_resposta(entrada, perguntas_respostas)
        print(f"Chatbot: {resposta}")

        self.space_ask.value = ""
        self.text = f"{resposta}"
        self.text_answer.value = f"{resposta}"

        self.space_ask.focus()
        self.page.update()

        if self.process.value == True:
            self.process.visible = False

        self.page.update()



def mainApp(page: Page):


    inicial = inicialPage(page)
    mainpage = mainPage(page)
    choosepage = choosePage(page)

    def router(route):
        page.views.clear()

        if page.route == "/inicial":
            page.views.append(inicial)
            page.update()

        if page.route == "/choose-page":
            page.views.append(choosepage)
            page.update()

        if page.route == "/chat-here":
            page.views.append(mainpage)
            page.update()

    page.on_route_change = router
    page.go("/inicial")

   # text = "Bem vindo ao chat kawai"

    for c in range(0, 101):
        value = c*10/100
        sleep(.3)
        if value == 1.0:
            page.go("/chat-here")
            #text_to_speech(text)
            break
            page.update()
    #page.window_center()
    page.update()


if __name__ == '__main__':
    #app(target=mainApp)
    app(target=mainApp, view=WEB_BROWSER, web_renderer=WebRenderer.HTML)