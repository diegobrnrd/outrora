"""App principal do jogo Outrora.

Contém telas: inicial, história e créditos, além da lógica de
efeito de digitação e controle de fluxo entre estados.

Este arquivo é intencionalmente minimalista: apenas o necessário
para executar o jogo e manter a leitura do código.
"""

from random import choice
from pathlib import Path
from typing import Callable

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from data.story import STORY_STATES, TRANSITIONS


# Configura tela cheia antes da criação da janela, quando possível.
Config.set("graphics", "fullscreen", "auto")


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


IMAGE_TELA_INICIAL = "tela_inicial.png"
IMAGE_HISTORIA = "background.png"
IMAGE_CREDITOS = "creditos.png"


# Paleta de cores
COLOR_TEXT_PRINCIPAL = (237 / 255, 231 / 255, 209 / 255, 1)      # #EDE7D1
COLOR_BTN_BG = (90 / 255, 35 / 255, 45 / 255, 1)                # vinho escuro
COLOR_BTN_ACTIVE_BG = (138 / 255, 46 / 255, 59 / 255, 1)        # vinho queimado
COLOR_BTN_TEXT = (246 / 255, 241 / 255, 227 / 255, 1)           # marfim
COLOR_PANEL = (8 / 255, 10 / 255, 14 / 255, 0.72)               # quase preto translúcido
COLOR_PANEL_BORDER = (208 / 255, 140 / 255, 96 / 255, 0.28)     # cobre discreto


def asset_path(*parts: str) -> str:
    """Retorna caminho absoluto para um arquivo em `assets/`.

    Exemplo: `asset_path('audio', 'musica.mp3')`.
    """
    return str(ASSETS_DIR.joinpath(*parts))


def image_path(filename: str) -> str:
    """Retorna caminho absoluto para imagem dentro de `assets/images`.

    Usado para alimentar widgets `Image`.
    """
    return str(ASSETS_DIR / "images" / filename)


def start_typing(
    label,
    full_text: str,
    interval: float = 0.02,
    on_complete: Callable | None = None,
    cursor_char: str = "|",
    blink_interval: float = 0.5,
):
    """Aplica efeito de digitação no `label`.

    - `interval`: tempo entre caracteres.
    - `on_complete`: função chamada quando a digitação terminar.
    - `cursor_char`: caractere do cursor piscante.
    """
    try:
        ev = getattr(label, "_typing_ev", None)
        if ev:
            ev.cancel()
    except Exception:
        pass

    try:
        cursor_ev = getattr(label, "_cursor_ev", None)
        if cursor_ev:
            cursor_ev.cancel()
    except Exception:
        pass

    label.full_text = full_text
    label._typing_index = 0
    label._display_text = ""
    label._cursor_visible = True
    label.text = ""

    def _update_display():
        try:
            cursor = cursor_char if getattr(label, "_cursor_visible", False) else ""
            label.text = getattr(label, "_display_text", "") + cursor
        except Exception:
            pass

    def _cursor_tick(dt):
        try:
            label._cursor_visible = not getattr(label, "_cursor_visible", False)
            _update_display()
        except Exception:
            pass

    def _tick(dt):
        label._typing_index += 1
        label._display_text = label.full_text[: label._typing_index]
        _update_display()

        if label._typing_index >= len(label.full_text):
            try:
                label._typing_ev.cancel()
            except Exception:
                pass

            label._typing_ev = None

            try:
                label._cursor_ev = Clock.schedule_interval(_cursor_tick, blink_interval)
            except Exception:
                label._cursor_ev = None

            if callable(on_complete):
                try:
                    on_complete()
                except Exception:
                    pass

            return False

        return True

    try:
        label._cursor_ev = Clock.schedule_interval(_cursor_tick, blink_interval)
    except Exception:
        label._cursor_ev = None

    label._typing_ev = Clock.schedule_interval(_tick, interval)


class TextPanel(MDBoxLayout):
    """Painel com fundo translúcido e bordas decorativas.

    Usado como contêiner do texto da história.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = [24, 20, 24, 20]

        with self.canvas.before:
            self._panel_color = Color(*COLOR_PANEL)
            self._panel_rect = Rectangle(pos=self.pos, size=self.size)

        with self.canvas.after:
            self._border_color = Color(*COLOR_PANEL_BORDER)
            self._border_top = Rectangle(pos=self.pos, size=(self.width, 2))
            self._border_bottom = Rectangle(pos=self.pos, size=(self.width, 2))

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self._panel_rect.pos = self.pos
        self._panel_rect.size = self.size

        self._border_top.pos = (self.x, self.y + self.height - 2)
        self._border_top.size = (self.width, 2)

        self._border_bottom.pos = (self.x, self.y)
        self._border_bottom.size = (self.width, 2)


class OutroraApp(MDApp):
    """Aplicação principal que gerencia telas e áudio."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen_manager = ScreenManager()
        self.tela_inicial = TelaInicial(name="tela_inicial")
        self.tela_historia = TelaHistoria(name="tela_historia")
        self.tela_creditos = TelaCreditos(name="tela_creditos")

        self.lista_de_musicas = [
            asset_path("audio", "musica.mp3"),
            asset_path("audio", "musica_2.mp3"),
            asset_path("audio", "musica_3.mp3"),
            asset_path("audio", "musica_4.mp3"),
        ]

        musicas_existentes = [m for m in self.lista_de_musicas if Path(m).exists()]
        self.musica_aleatoria = choice(musicas_existentes or self.lista_de_musicas)
        self.sound = SoundLoader.load(self.musica_aleatoria)

    def build(self):
        self.title = "Outrora"

        try:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Brown"
        except Exception:
            pass

        self.screen_manager.add_widget(self.tela_inicial)
        self.screen_manager.add_widget(self.tela_historia)
        self.screen_manager.add_widget(self.tela_creditos)

        if self.sound:
            self.sound.loop = True
            self.sound.play()

        return self.screen_manager

    def para_musica(self):
        if self.sound and self.sound.state == "play":
            self.sound.stop()
            self.sound.unload()


class TelaInicial(Screen):
    """Tela inicial com imagem de fundo e botões de ação."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        imagem = Image(source=image_path(IMAGE_TELA_INICIAL), fit_mode="cover")
        layout.add_widget(imagem)

        botao_inicial = MDRaisedButton(
            text="Iniciar Jogo",
            on_release=self.troca_tela,
            pos_hint={"center_x": 0.4, "center_y": 0.06},
            md_bg_color=COLOR_BTN_BG,
            text_color=COLOR_BTN_TEXT,
            ripple_color=COLOR_BTN_ACTIVE_BG,
        )
        layout.add_widget(botao_inicial)

        botao_fechar_inicial = MDRaisedButton(
            text="Fechar Jogo",
            on_release=self.fecha_jogo,
            pos_hint={"center_x": 0.6, "center_y": 0.06},
            md_bg_color=COLOR_BTN_BG,
            text_color=COLOR_BTN_TEXT,
            ripple_color=COLOR_BTN_ACTIVE_BG,
        )
        layout.add_widget(botao_fechar_inicial)

        self.add_widget(layout)

    def troca_tela(self, instance):
        historia = self.manager.get_screen("tela_historia")
        historia.reiniciar_historia()
        self.manager.current = "tela_historia"

    def fecha_jogo(self, instance):
        app = MDApp.get_running_app()
        app.para_musica()
        app.stop()


class TelaHistoria(Screen):
    """Tela que exibe o texto da narrativa com efeito de digitação.

    As escolhas aparecem apenas após o texto terminar.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.estados_da_historia = STORY_STATES
        self.indice_do_estado_atual = 0
        self._current_text_label = None
        self._current_choices: list[str] = []
        self._buttons_visible = False
        self._started_once = False

        self.layout = FloatLayout()
        self.background = Image(source=image_path(IMAGE_HISTORIA), fit_mode="cover")
        self.layout.add_widget(self.background)

        self.text_container = TextPanel(
            orientation="vertical",
            spacing=10,
            size_hint=(0.88, None),
            pos_hint={"center_x": 0.5, "center_y": 0.62},
        )
        self.text_container.height = max(Window.height * 0.36, 260)

        self.buttons_container = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(0.88, None),
            pos_hint={"center_x": 0.5, "y": 0.06},
        )
        self.buttons_container.height = 190

        self.layout.add_widget(self.text_container)
        self.layout.add_widget(self.buttons_container)
        self.add_widget(self.layout)

        Window.bind(on_resize=self._on_window_resize)

    def _on_window_resize(self, window, width, height):
        self.text_container.height = max(height * 0.36, 260)
        self.buttons_container.height = 190
        self._ajustar_area_do_texto()

    def _ajustar_area_do_texto(self):
        """Mantém o texto centralizado dentro do painel."""
        label = self._current_text_label
        if label is None:
            return

        largura = max(Window.width * 0.88 - 96, 240)
        altura = max(self.text_container.height - 48, 120)

        label.text_size = (largura, altura)
        label.size_hint_y = 1
        label.height = altura

        try:
            label.texture_update()
        except Exception:
            pass

    def on_enter(self):
        super().on_enter()
        Window.bind(on_key_down=self._on_window_key_down)

        if not self._started_once:
            self._started_once = True
            self.estado_de_exibicao()

    def on_leave(self):
        super().on_leave()
        Window.unbind(on_key_down=self._on_window_key_down)
        self._cancel_typing_effects()

    def reiniciar_historia(self):
        self.indice_do_estado_atual = 0
        self._started_once = True
        self.estado_de_exibicao()

    def on_touch_down(self, touch):
        if not self._buttons_visible and self._current_text_label is not None:
            self._finalizar_texto_atual()
            return True

        return super().on_touch_down(touch)

    def _cancel_typing_effects(self):
        for container in (
            getattr(self, "text_container", None),
            getattr(self, "buttons_container", None),
        ):
            if container is None:
                continue

            for child in list(container.children):
                try:
                    ev = getattr(child, "_typing_ev", None)
                    if ev:
                        ev.cancel()
                except Exception:
                    pass

                try:
                    cursor_ev = getattr(child, "_cursor_ev", None)
                    if cursor_ev:
                        cursor_ev.cancel()
                except Exception:
                    pass

    def _on_window_key_down(self, window, keycode, scancode, text, modifiers):
        key_name = keycode[1] if isinstance(keycode, (tuple, list)) and len(keycode) > 1 else ""
        key_number = keycode[0] if isinstance(keycode, (tuple, list)) and len(keycode) > 0 else None

        if key_name in ("space", "spacebar") or key_number == 32:
            if self._current_text_label is not None and not self._buttons_visible:
                self._finalizar_texto_atual()
                return True

        return False

    def _finalizar_texto_atual(self):
        label = self._current_text_label
        if label is None:
            return

        try:
            typing_ev = getattr(label, "_typing_ev", None)
            if typing_ev:
                typing_ev.cancel()
        except Exception:
            pass

        try:
            cursor_ev = getattr(label, "_cursor_ev", None)
            if cursor_ev:
                cursor_ev.cancel()
        except Exception:
            pass

        label._typing_ev = None
        label._cursor_ev = None
        label._display_text = getattr(label, "full_text", label.text)
        label._cursor_visible = False
        label.text = getattr(label, "full_text", label.text)

        self._ajustar_area_do_texto()
        self._mostrar_botoes(self._current_choices)

    def estado_de_exibicao(self):
        self._cancel_typing_effects()

        self.text_container.clear_widgets()
        self.buttons_container.clear_widgets()
        self._buttons_visible = False

        estado = self.estados_da_historia[self.indice_do_estado_atual]
        self._current_choices = estado["escolhas"]

        texto_base = estado["pergunta"].strip()

        texto_pergunta = MDLabel(
            text="",
            halign="left",
            valign="middle",
            font_style="H6",
            theme_text_color="Custom",
            text_color=COLOR_TEXT_PRINCIPAL,
            size_hint=(1, 1),
        )
        texto_pergunta.padding = [8, 0, 8, 0]

        self.text_container.add_widget(texto_pergunta)
        self._current_text_label = texto_pergunta
        self._ajustar_area_do_texto()

        start_typing(
            texto_pergunta,
            texto_base,
            interval=0.035,
            on_complete=self._mostrar_botoes,
        )

    def _mostrar_botoes(self, escolhas=None):
        if self._buttons_visible:
            return

        if escolhas is None:
            escolhas = self._current_choices

        self.buttons_container.clear_widgets()

        for escolha in escolhas:
            botao = MDRaisedButton(
                text=escolha,
                on_release=self.quando_escolher,
                pos_hint={"center_x": 0.5},
                md_bg_color=COLOR_BTN_BG,
                text_color=COLOR_BTN_TEXT,
                ripple_color=COLOR_BTN_ACTIVE_BG,
                opacity=0,
            )
            self.buttons_container.add_widget(botao)
            Animation(opacity=1, duration=0.35).start(botao)

        self._buttons_visible = True

    def quando_escolher(self, atual):
        escolha_atual = atual.text

        next_step = TRANSITIONS.get((self.indice_do_estado_atual, escolha_atual))

        if next_step is None:
            self.estado_de_exibicao()
            return

        if next_step == "EXIT":
            app = MDApp.get_running_app()
            app.para_musica()
            app.stop()
            return

        if next_step == "CREDITS":
            self.troca_tela_creditos()
            return

        self.indice_do_estado_atual = next_step
        self.estado_de_exibicao()

    def troca_tela_creditos(self, instance=None):
        self.manager.current = "tela_creditos"


class TelaCreditos(Screen):
    """Tela final estática. Os textos finais ficam dentro da imagem de créditos."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._return_to_inicial_ev = None

        layout = FloatLayout()

        imagem = Image(
            source=image_path(IMAGE_CREDITOS),
            fit_mode="cover",
        )
        layout.add_widget(imagem)

        self.add_widget(layout)

    def on_enter(self):
        super().on_enter()

        if self._return_to_inicial_ev is not None:
            try:
                self._return_to_inicial_ev.cancel()
            except Exception:
                pass

        def _volta_para_inicial(dt):
            try:
                app = MDApp.get_running_app()
                app.para_musica()
                app.stop()
            except Exception:
                pass

        self._return_to_inicial_ev = Clock.schedule_once(_volta_para_inicial, 15)

    def on_leave(self):
        super().on_leave()

        if self._return_to_inicial_ev is not None:
            try:
                self._return_to_inicial_ev.cancel()
            except Exception:
                pass
            self._return_to_inicial_ev = None

    def reiniciar(self, instance):
        app = MDApp.get_running_app()

        historia = self.manager.get_screen("tela_historia")
        historia.reiniciar_historia()
        self.manager.current = "tela_historia"

    @staticmethod
    def fecha_jogo(instance):
        app = MDApp.get_running_app()
        app.para_musica()
        app.stop()


if __name__ == "__main__":
    OutroraApp().run()
    