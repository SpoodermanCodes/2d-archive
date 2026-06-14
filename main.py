from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp

from games.snake         import SnakeScreen
from games.tetris        import TetrisScreen
from games.pong          import PongScreen
from games.space_invaders import SpaceInvadersScreen
from games.flappy_bird   import FlappyScreen
from shared.scores       import load_scores

GAMES = [
    ('snake',          '🐍 Snake',          SnakeScreen,          (0.1, 0.6, 0.1, 1)),
    ('tetris',         '🟦 Tetris',          TetrisScreen,         (0.1, 0.3, 0.8, 1)),
    ('pong',           '🏓 Pong',            PongScreen,           (0.6, 0.1, 0.6, 1)),
    ('space_invaders', '👾 Space Invaders',  SpaceInvadersScreen,  (0.7, 0.1, 0.1, 1)),
    ('flappy_bird',    '🐦 Flappy Bird',     FlappyScreen,         (0.1, 0.5, 0.7, 1)),
]


class MenuScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(name='menu', **kwargs)
        self.sm = sm
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))

        title = Label(
            text='🕹  ARCADE HUB',
            font_size=dp(32),
            bold=True,
            color=(1, 1, 0.2, 1),
            size_hint_y=None,
            height=dp(70),
        )
        root.add_widget(title)

        self.grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self._populate_grid()

        sv = ScrollView(size_hint=(1, 1))
        sv.add_widget(self.grid)
        root.add_widget(sv)

        self.add_widget(root)

    def _populate_grid(self):
        scores = load_scores()
        self.grid.clear_widgets()
        for key, label, _, color in GAMES:
            card = Button(
                text=f'{label}\n[size=14][color=cccccc]Best: {scores.get(key, 0)}[/color][/size]',
                markup=True,
                font_size=dp(22),
                size_hint_y=None,
                height=dp(90),
                background_color=color,
                background_normal='',
            )
            card.bind(on_press=lambda btn, k=key: self._launch(k))
            self.grid.add_widget(card)

    def on_enter(self):
        self._populate_grid()

    def _launch(self, key):
        self.sm.transition = SlideTransition(direction='left')
        self.sm.current = key

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1)
            Rectangle(pos=self.pos, size=self.size)


class ArcadeApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.sm = ScreenManager()
        Clock.schedule_once(self._init_screens)
        return self.sm

    def _init_screens(self, dt):
        from shared.ui import make_back_button
        sm = self.sm

        menu = MenuScreen(sm)
        sm.add_widget(menu)

        for key, _, ScreenClass, _ in GAMES:
            screen = ScreenClass(name=key)
            back = make_back_button(lambda btn, s=sm: self._back(s))
            back.pos = (10, Window.height - 50)
            screen.add_widget(back)
            sm.add_widget(screen)

    def _back(self, sm):
        sm.transition = SlideTransition(direction='right')
        sm.current = 'menu'


if __name__ == '__main__':
    ArcadeApp().run()
