from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from shared.constants import *
from shared.scores import save_score, load_scores

PAD_W, PAD_H = 12, 80
BALL = 14
SPEED = 5
WIN_SCORE = 7


class PongScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_label = Label(pos=(Window.width*0.35, Window.height-42), font_size=20, color=(1,1,1,1))
        self.msg_label   = Label(text='Tap to start', pos=(Window.width*0.3, Window.height//2-20), font_size=22, color=(1,1,0,1))
        self.add_widget(self.score_label)
        self.add_widget(self.msg_label)
        self._clock = None

    def on_enter(self):
        self.reset()
        self._clock = Clock.schedule_interval(self.update, 1/60)

    def on_leave(self):
        if self._clock: self._clock.cancel()

    def reset(self):
        w, h = Window.width, Window.height
        self.player_y = h // 2 - PAD_H // 2
        self.ai_y     = h // 2 - PAD_H // 2
        self.ball_x   = w // 2
        self.ball_y   = h // 2
        self.ball_vx  = SPEED
        self.ball_vy  = SPEED * 0.7
        self.p_score  = 0
        self.ai_score = 0
        self.started  = False
        self.game_over = False
        self.msg_label.text = 'Drag right paddle\nto play'
        self.msg_label.opacity = 1

    def on_touch_move(self, touch):
        if touch.x > Window.width // 2:
            self.player_y = touch.y - PAD_H // 2
            self.player_y = max(HEADER, min(Window.height - PAD_H, self.player_y))

    def on_touch_down(self, touch):
        if not self.started:
            self.started = True
            self.msg_label.opacity = 0
        elif self.game_over:
            self.reset()
            self.started = True
            self.msg_label.opacity = 0

    def update(self, dt):
        if not self.started or self.game_over:
            self._draw(); return

        w, h = Window.width, Window.height

        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # top/bottom bounce
        if self.ball_y <= HEADER + BALL//2:
            self.ball_vy = abs(self.ball_vy)
        if self.ball_y >= h - BALL//2:
            self.ball_vy = -abs(self.ball_vy)

        # AI tracks ball
        ai_center = self.ai_y + PAD_H // 2
        if ai_center < self.ball_y - 5:  self.ai_y += 3
        elif ai_center > self.ball_y + 5: self.ai_y -= 3
        self.ai_y = max(HEADER, min(h - PAD_H, self.ai_y))

        # player paddle (left=AI, right=player) — left side is AI
        ai_x = 20
        pl_x = w - 20 - PAD_W

        # ball vs AI paddle
        if (self.ball_x - BALL//2 <= ai_x + PAD_W and
                self.ai_y <= self.ball_y <= self.ai_y + PAD_H):
            self.ball_vx = abs(self.ball_vx)

        # ball vs player paddle
        if (self.ball_x + BALL//2 >= pl_x and
                self.player_y <= self.ball_y <= self.player_y + PAD_H):
            self.ball_vx = -abs(self.ball_vx)

        # scoring
        if self.ball_x < 0:
            self.ai_score += 1
            self._reset_ball()
        if self.ball_x > w:
            self.p_score += 1
            self._reset_ball()

        if self.p_score >= WIN_SCORE or self.ai_score >= WIN_SCORE:
            self.game_over = True
            winner = 'You win!' if self.p_score >= WIN_SCORE else 'AI wins!'
            save_score('pong', self.p_score)
            self.msg_label.text = f'{winner}\nTap to retry'
            self.msg_label.opacity = 1

        self.score_label.text = f'AI {self.ai_score}  :  {self.p_score} You'
        self._draw()

    def _reset_ball(self):
        import random
        self.ball_x = Window.width // 2
        self.ball_y = Window.height // 2
        self.ball_vx = SPEED * random.choice([-1, 1])
        self.ball_vy = SPEED * 0.7 * random.choice([-1, 1])

    def _draw(self):
        w, h = Window.width, Window.height
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0,0), size=(w, h))
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=(0, h-HEADER), size=(w, HEADER))
            # center line
            Color(0.3, 0.3, 0.3, 1)
            for y in range(HEADER, h, 20):
                Rectangle(pos=(w//2-1, y), size=(2, 10))
            # paddles
            Color(1, 1, 1, 1)
            Rectangle(pos=(20, self.ai_y), size=(PAD_W, PAD_H))
            Rectangle(pos=(w-20-PAD_W, self.player_y), size=(PAD_W, PAD_H))
            # ball
            Color(1, 1, 0, 1)
            Ellipse(pos=(self.ball_x - BALL//2, self.ball_y - BALL//2), size=(BALL, BALL))
