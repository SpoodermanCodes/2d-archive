from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from shared.constants import *


def make_back_button(callback):
    btn = Button(
        text='< MENU',
        size_hint=(None, None),
        size=(100, 40),
        pos=(10, Window.height - 50),
        background_color=(0.2, 0.2, 0.2, 1),
        color=(1, 1, 1, 1),
        font_size=14,
    )
    btn.bind(on_press=callback)
    return btn


def draw_header(canvas, title_label, score_label=None, high_label=None):
    with canvas:
        Color(*DARK_GRAY)
        Rectangle(pos=(0, Window.height - HEADER), size=(Window.width, HEADER))
