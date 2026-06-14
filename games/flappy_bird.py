import random
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse, Triangle
from kivy.clock import Clock
from kivy.core.window import Window
from shared.constants import *
from shared.scores import save_score, load_scores

BIRD_SIZE = 24
GRAVITY   = -0.5
FLAP      = 8
PIPE_W    = 60
GAP       = 160
PIPE_SPEED = 3


class FlappyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_label = Label(pos=(Window.width*0.35, Window.height-42), font_size=20, color=(1,1,1,1))
        self.hi_label    = Label(pos=(Window.width*0.6,  Window.height-42), font_size=18, color=(1,1,1,1))
        self.msg_label   = Label(text='Tap to flap!', pos=(Window.width*0.3, Window.height//2+40), font_size=24, color=(1,1,0,1))
        self.add_widget(self.score_label)
        self.add_widget(self.hi_label)
        self.add_widget(self.msg_label)
        self._clock = None

    def on_enter(self):
        self.reset()
        self._clock = Clock.schedule_interval(self.update, 1/60)

    def on_leave(self):
        if self._clock: self._clock.cancel()

    def reset(self):
        w, h = Window.width, Window.height
        self.bird_x  = w * 0.25
        self.bird_y  = h * 0.5
        self.bird_vy = 0
        self.pipes   = []
        self.score   = 0
        self.started  = False
        self.game_over = False
        self.pipe_timer = 0
        self.msg_label.text = 'Tap to flap!'
        self.msg_label.opacity = 1

    def _add_pipe(self):
        h = Window.height
        gap_y = random.randint(HEADER + GAP + 40, h - 80)
        self.pipes.append({'x': Window.width, 'gap_y': gap_y, 'passed': False})

    def on_touch_down(self, touch):
        if not self.started:
            self.started = True
            self.msg_label.opacity = 0
        elif self.game_over:
            save_score('flappy_bird', self.score)
            self.reset()
            self.started = True
            self.msg_label.opacity = 0
        else:
            self.bird_vy = FLAP

    def update(self, dt):
        if not self.started or self.game_over:
            self._draw(); return

        h = Window.height

        # gravity
        self.bird_vy += GRAVITY
        self.bird_y  += self.bird_vy

        # floor / ceiling
        if self.bird_y <= HEADER + BIRD_SIZE//2:
            self.game_over = True
            self._end()
            self._draw(); return
        if self.bird_y >= h - BIRD_SIZE//2:
            self.game_over = True
            self._end()
            self._draw(); return

        # pipes
        self.pipe_timer += 1
        if self.pipe_timer >= 90:
            self._add_pipe()
            self.pipe_timer = 0

        for p in self.pipes:
            p['x'] -= PIPE_SPEED
            # score
            if not p['passed'] and p['x'] + PIPE_W < self.bird_x:
                p['passed'] = True
                self.score += 1
            # collision
            bx, by = self.bird_x, self.bird_y
            r = BIRD_SIZE // 2
            if p['x'] < bx+r and p['x']+PIPE_W > bx-r:
                if by+r > p['gap_y'] or by-r < p['gap_y'] - GAP:
                    self.game_over = True
                    self._end()
                    self._draw(); return

        self.pipes = [p for p in self.pipes if p['x'] > -PIPE_W]
        self.score_label.text = f'Score: {self.score}'
        self.hi_label.text    = f'Best: {load_scores()["flappy_bird"]}'
        self._draw()

    def _end(self):
        save_score('flappy_bird', self.score)
        self.msg_label.text = f'Game Over!\nScore: {self.score}\nTap to retry'
        self.msg_label.opacity = 1

    def _draw(self):
        w, h = Window.width, Window.height
        self.canvas.before.clear()
        with self.canvas.before:
            # sky
            Color(0.3, 0.6, 1, 1)
            Rectangle(pos=(0, HEADER), size=(w, h-HEADER))
            # header
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=(0, h-HEADER), size=(w, HEADER))
            # ground
            Color(0.4, 0.8, 0.2, 1)
            Rectangle(pos=(0, HEADER), size=(w, 20))
            # pipes
            Color(0.1, 0.7, 0.1, 1)
            for p in self.pipes:
                top_h = h - p['gap_y']
                bot_h = p['gap_y'] - GAP - HEADER
                # top pipe
                Rectangle(pos=(p['x'], p['gap_y']), size=(PIPE_W, top_h))
                Rectangle(pos=(p['x']-4, p['gap_y']-14), size=(PIPE_W+8, 14))
                # bottom pipe
                if bot_h > 0:
                    Rectangle(pos=(p['x'], HEADER+20), size=(PIPE_W, bot_h))
                    Rectangle(pos=(p['x']-4, HEADER+20+bot_h), size=(PIPE_W+8, 14))
            # bird body
            Color(1, 0.85, 0, 1)
            Ellipse(pos=(self.bird_x-BIRD_SIZE//2, self.bird_y-BIRD_SIZE//2), size=(BIRD_SIZE, BIRD_SIZE))
            # wing
            Color(1, 0.6, 0, 1)
            Ellipse(pos=(self.bird_x-BIRD_SIZE//2-6, self.bird_y-4), size=(14, 10))
            # eye
            Color(1, 1, 1, 1)
            Ellipse(pos=(self.bird_x+4, self.bird_y+2), size=(8, 8))
            Color(0, 0, 0, 1)
            Ellipse(pos=(self.bird_x+6, self.bird_y+4), size=(4, 4))
            # beak
            Color(1, 0.4, 0, 1)
            Triangle(points=[
                self.bird_x+BIRD_SIZE//2, self.bird_y+2,
                self.bird_x+BIRD_SIZE//2+8, self.bird_y,
                self.bird_x+BIRD_SIZE//2, self.bird_y-3
            ])
