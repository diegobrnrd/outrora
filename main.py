# Importação de módulos (KivyMD e Kivy)
from random import choice
from pathlib import Path

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager

from data.story import STORY_STATES, TRANSITIONS


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


def asset_path(*parts: str) -> str:
    """Build an absolute path to a file inside ./assets."""
    return str(ASSETS_DIR.joinpath(*parts))


# Classe principal do jogo
class OutroraApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Gerenciador de telas
        self.screen_manager = ScreenManager()
        self.tela_inicial = TelaInicial(name="tela_inicial")
        self.tela_historia = TelaHistoria(name="tela_historia")
        self.tela_creditos = TelaCreditos(name="tela_creditos")

        # Lista de músicas (paths completos dentro de assets/)
        self.lista_de_musicas = [
            asset_path("audio", "musica.mp3"),
            asset_path("audio", "musica_2.mp3"),
            asset_path("audio", "musica_3.mp3"),
            asset_path("audio", "musica_4.mp3"),
        ]

        # Escolha da música aleatoriamente
        self.musica_aleatoria = choice(self.lista_de_musicas)

        # Carrega a música (pode retornar None dependendo do ambiente/provider)
        self.sound = SoundLoader.load(self.musica_aleatoria)

    def build(self):
        # Adiciona as telas ao gerenciador
        self.screen_manager.add_widget(self.tela_inicial)
        self.screen_manager.add_widget(self.tela_historia)
        self.screen_manager.add_widget(self.tela_creditos)

        # Reproduz a música (se carregou)
        if self.sound:
            self.sound.loop = True
            self.sound.play()

        # Configura o jogo para iniciar em tela cheia
        Config.set("graphics", "fullscreen", "auto")
        Config.write()

        return self.screen_manager

    # Para a música ao fechar o jogo
    def para_musica(self):
        if self.sound and self.sound.state == "play":
            self.sound.stop()
            self.sound.unload()


# Define a tela inicial do jogo
class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Imagem da tela inicial
        imagem = Image(
            source=asset_path("images", "tela_inicial.jpg"),
            allow_stretch=True,
            keep_ratio=True,
        )

        # Botão da tela inicial
        botao_inicial = MDRaisedButton(
            text="Iniciar Jogo",
            on_release=self.troca_tela,
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.5, 0, 0.1, 1),
        )

        # Adiciona a imagem e o botão ao FloatLayout
        layout = FloatLayout()
        layout.add_widget(imagem)
        layout.add_widget(botao_inicial)
        self.add_widget(layout)

    # Troca da tela inicial para a tela história
    def troca_tela(self, instance):
        self.manager.current = "tela_historia"


# Define a tela história do jogo
class TelaHistoria(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Imagem de fundo da tela história
        imagem = Image(
            source=asset_path("images", "historia.jpg"),
            allow_stretch=True,
            keep_ratio=True,
        )

        layout = FloatLayout()
        layout.add_widget(imagem)
        self.add_widget(layout)

        # História do jogo vem de data/story.py
        self.estados_da_historia = STORY_STATES

        # Variável para controlar o estado atual
        self.indice_do_estado_atual = 0

        # Container vertical de texto + botões
        self.container = MDBoxLayout(orientation="vertical", spacing="10")
        self.estado_de_exibicao()
        self.add_widget(self.container)

    # Exibe o texto e os botões na tela
    def estado_de_exibicao(self):
        # Limpa os widgets a cada rodada
        self.container.clear_widgets()

        estado = self.estados_da_historia[self.indice_do_estado_atual]

        texto_pergunta = MDLabel(
            text=estado["pergunta"],
            halign="left",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0.969, 0.902, 0.651, 1),
        )
        texto_pergunta.padding = [50, 0, 50, 0]
        self.container.add_widget(texto_pergunta)

        for escolha in estado["escolhas"]:
            botao = MDRaisedButton(
                text=escolha,
                on_release=self.quando_escolher,
                pos_hint={"center_x": 0.5},
                md_bg_color=(0.902, 0.627, 0.435, 1),
                text_color=(0.012, 0, 0.11, 1),
                opacity=0,
            )
            self.container.add_widget(botao)
            Animation(opacity=1, duration=0.5).start(botao)

    # Controle da história (simplificado)
    def quando_escolher(self, atual):
        escolha_atual = atual.text

        next_step = TRANSITIONS.get((self.indice_do_estado_atual, escolha_atual))
        if next_step is None:
            # Sem transição definida: não quebra o jogo; re-renderiza estado atual
            self.estado_de_exibicao()
            return

        if next_step == "EXIT":
            app = MDApp.get_running_app()
            app.stop()
            return

        if next_step == "CREDITS":
            self.troca_tela_2()
            return

        # Próximo estado numérico
        self.indice_do_estado_atual = next_step
        self.estado_de_exibicao()

    # Para a música e troca para a tela créditos
    def troca_tela_2(self, instance=None):
        app = MDApp.get_running_app()
        if app.sound and app.sound.state == "play":
            app.sound.stop()
            app.sound.unload()
        self.manager.current = "tela_creditos"


# Classe responsável pela tela de créditos do jogo
class TelaCreditos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fechar_jogo = None
        self.video_creditos = None
        self.fallback_layout = None

        # Widget de vídeo (pode existir mesmo sem provider funcional)
        self.video_creditos = Video(
            source=asset_path("video", "creditos.mp4"),
            state="pause",
            options={"allow_stretch": True, "keep_ratio": True},
        )
        self.add_widget(self.video_creditos)

    def _show_fallback(self):
        if self.fallback_layout is not None:
            return

        # Remove vídeo (se estiver presente)
        if self.video_creditos is not None:
            try:
                self.remove_widget(self.video_creditos)
            except Exception:
                pass
            self.video_creditos = None

        self.fallback_layout = MDBoxLayout(
            orientation="vertical",
            spacing="12",
            padding=[24, 24, 24, 24],
        )

        titulo = MDLabel(
            text="Créditos",
            halign="center",
            font_style="H4",
        )

        texto = MDLabel(
            text=(
                "Obrigado por jogar Outrora.\n\n"
                "O vídeo de créditos não pôde ser carregado neste ambiente.\n"
                "Para habilitar vídeo, instale um provider (ex.: ffpyplayer)."
            ),
            halign="center",
        )

        botao = MDRaisedButton(
            text="Fechar Jogo",
            on_release=self.fecha_jogo,
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 1, 1, 1),
            text_color=(0, 0, 0, 1),
        )

        self.fallback_layout.add_widget(titulo)
        self.fallback_layout.add_widget(texto)
        self.fallback_layout.add_widget(botao)
        self.add_widget(self.fallback_layout)

    def on_enter(self):
        super().on_enter()

        # Se não há vídeo (porque já caiu em fallback), não faz nada.
        if self.video_creditos is None:
            return

        # Tenta tocar o vídeo
        try:
            self.video_creditos.state = "play"
        except Exception:
            self._show_fallback()
            return

        # Agenda um check: se o vídeo não "andar", cai em fallback.
        # (sem provider de vídeo, normalmente o position não evolui)
        self._start_pos = None
        try:
            self._start_pos = float(getattr(self.video_creditos, "position", 0.0) or 0.0)
        except Exception:
            self._start_pos = 0.0

        Clock.schedule_once(self._verificar_video_funcionando, 0.8)

        # Se o vídeo funcionar, a gente coloca o botão no tempo esperado
        Clock.schedule_once(self.adicionar_botao_fechar_jogo, 60.7)

    def _verificar_video_funcionando(self, dt):
        # Se já caiu em fallback, não verifica
        if self.video_creditos is None:
            return

        # Heurísticas de "vídeo funcionando":
        # - state continua play
        # - position aumentou um pouco
        try:
            state = getattr(self.video_creditos, "state", None)
            pos = float(getattr(self.video_creditos, "position", 0.0) or 0.0)
        except Exception:
            self._show_fallback()
            return

        # Se não está em play, ou não avançou nada, assume que não carregou/provider ausente
        if state != "play":
            self._show_fallback()
            return

        # tolerância pequena: se não mexeu nada em ~0.8s, provavelmente não está tocando
        if pos <= (self._start_pos + 0.01):
            self._show_fallback()
            return

        # Se chegou aqui, o vídeo está ok (não faz nada)

    def on_leave(self):
        super().on_leave()
        if self.video_creditos is None:
            return
        try:
            self.video_creditos.state = "pause"
        except Exception:
            pass

    def adicionar_botao_fechar_jogo(self, dt):
        # Se caiu em fallback, o botão já existe no layout de fallback
        if self.video_creditos is None:
            return

        if self.fechar_jogo is not None:
            return

        self.fechar_jogo = MDRaisedButton(
            text="Fechar Jogo",
            on_release=self.fecha_jogo,
            pos_hint={"center_x": 0.5, "center_y": 0.050},
            md_bg_color=(1, 1, 1, 1),
            text_color=(0, 0, 0, 1),
        )
        self.add_widget(self.fechar_jogo)

    @staticmethod
    def fecha_jogo(instance):
        app = MDApp.get_running_app()
        app.stop()
        return


# Executa o jogo
if __name__ == "__main__":
    OutroraApp().run()