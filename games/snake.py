import random
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from shared.constants import *
from shared.scores import save_score, load_scores

BLOCK = 18


class SnakeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.score_label = Label(size_hint=(None, None), pos_hint={'center_x': 0.55, 'top': 0.99}, font_size=18, color=(1,1,1,1))
        self.hi_label    = Label(size_hint=(None, None), pos_hint={'center_x': 0.8,  'top': 0.99}, font_size=18, color=(1,1,1,1))
        self.msg_label   = Label(text='Swipe to start', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=22, color=(1,1,0,1))
        layout.add_widget(self.score_label)
        layout.add_widget(self.hi_label)
        layout.add_widget(self.msg_label)
        self.add_widget(layout)
        self._clock = None
        self.touch_start = None

    def on_enter(self):
        self.reset()
        self._clock = Clock.schedule_interval(self.update, 1 / FPS)

    def on_leave(self):
        if self._clock:
            self._clock.cancel()

    def reset(self):
        cx = (int(Window.width) // 2 // BLOCK) * BLOCK
        cy = (int(Window.height) // 2 // BLOCK) * BLOCK
        self.snake = [[cx, cy], [cx - BLOCK, cy], [cx - 2*BLOCK, cy]]
        self.direction = 'RIGHT'
        self.change_to  = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.started   = False
        self.food = self._spawn_food()
        self.msg_label.text = 'Swipe to start'
        self.msg_label.opacity = 1

    def _spawn_food(self):
        cols = int(Window.width) // BLOCK
        rows = (int(Window.height) - HEADER) // BLOCK
        while True:
            x = random.randint(0, cols - 1) * BLOCK
            y = random.randint(0, rows - 1) * BLOCK + HEADER
            if [x, y] not in self.snake:
                return [x, y]

    def on_touch_down(self, touch):
        self.touch_start = (touch.x, touch.y)
        if not self.started:
            self.started = True
            self.msg_label.opacity = 0
        elif self.game_over:
            save_score('snake', self.score)
            self.reset()
            self.started = True
            self.msg_label.opacity = 0
        return True

    def on_touch_up(self, touch):
        if not self.touch_start:
            return
        dx = touch.x - self.touch_start[0]
        dy = touch.y - self.touch_start[1]
        if abs(dx) > abs(dy) and abs(dx) > 20:
            if dx > 0 and self.direction != 'LEFT':  self.change_to = 'RIGHT'
            if dx < 0 and self.direction != 'RIGHT': self.change_to = 'LEFT'
        elif abs(dy) > abs(dx) and abs(dy) > 20:
            if dy > 0 and self.direction != 'DOWN':  self.change_to = 'UP'
            if dy < 0 and self.direction != 'UP':    self.change_to = 'DOWN'

    def update(self, dt):
        if self.started and not self.game_over:
            self.direction = self.change_to
            head = self.snake[0].copy()
            if self.direction == 'UP':    head[1] += BLOCK
            elif self.direction == 'DOWN':  head[1] -= BLOCK
            elif self.direction == 'LEFT':  head[0] -= BLOCK
            elif self.direction == 'RIGHT': head[0] += BLOCK

            if (head[0] < 0 or head[0] >= Window.width or
                    head[1] < HEADER or head[1] >= Window.height or
                    head in self.snake):
                self.game_over = True
                self.msg_label.text = 'Game Over! Swipe to retry'
                self.msg_label.opacity = 1
            else:
                self.snake.insert(0, head)
                if head == self.food:
                    self.food = self._spawn_food()
                    self.score += 10
                    if self._clock:
                        self._clock.cancel()
                        self._clock = Clock.schedule_interval(self.update, 1 / (FPS + self.score // 50))
                else:
                    self.snake.pop()

        self.score_label.text = f'Score: {self.score}'
        self.hi_label.text    = f'Best: {load_scores()["snake"]}'
        self._draw()

    def _draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=(0, Window.height - HEADER), size=(Window.width, HEADER))
            Color(1, 0, 0, 1)
            Rectangle(pos=(self.food[0], self.food[1]), size=(BLOCK, BLOCK))
            Color(0.5, 0.2, 0, 1)
            Rectangle(pos=(self.food[0] + BLOCK//2 - 2, self.food[1] + BLOCK - 4), size=(3, 5))
            for i, seg in enumerate(self.snake):
                Color(*DARK_GREEN) if i == 0 else Color(*GREEN)
                Rectangle(pos=(seg[0]+1, seg[1]+1), size=(BLOCK-2, BLOCK-2))
                if i == 0:
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(seg[0]+3, seg[1]+BLOCK-8), size=(4, 4))
                    Ellipse(pos=(seg[0]+BLOCK-7, seg[1]+BLOCK-8), size=(4, 4))
                    Color(0, 0, 0, 1)
                    Ellipse(pos=(seg[0]+4, seg[1]+BLOCK-7), size=(2, 2))
                    Ellipse(pos=(seg[0]+BLOCK-6, seg[1]+BLOCK-7), size=(2, 2))
