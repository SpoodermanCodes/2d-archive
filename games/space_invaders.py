import random
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Triangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from shared.constants import *
from shared.scores import save_score, load_scores

PLAYER_W, PLAYER_H = 36, 22
ENEMY_W,  ENEMY_H  = 28, 20
BULLET_W, BULLET_H = 4, 12
ENEMY_BULLET_H = 10
ROWS, COLS_E = 3, 8
ENEMY_GAP_X, ENEMY_GAP_Y = 44, 34


class SpaceInvadersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_label = Label(pos=(Window.width*0.35, Window.height-42), font_size=18, color=(1,1,1,1))
        self.hi_label    = Label(pos=(Window.width*0.6,  Window.height-42), font_size=18, color=(1,1,1,1))
        self.msg_label   = Label(text='Drag to move\nTap to shoot', pos=(Window.width*0.25, Window.height//2-30), font_size=20, color=(1,1,0,1))
        self.add_widget(self.score_label)
        self.add_widget(self.hi_label)
        self.add_widget(self.msg_label)
        self._clock = None

    def on_enter(self):
        self.reset()
        self._clock = Clock.schedule_interval(self.update, 1/30)

    def on_leave(self):
        if self._clock: self._clock.cancel()

    def reset(self):
        w = Window.width
        self.player_x = w // 2 - PLAYER_W // 2
        self.player_y = HEADER + 10
        self.bullets  = []
        self.enemy_bullets = []
        self.score    = 0
        self.game_over = False
        self.started   = False
        self.lives     = 3
        self.enemy_dir = 1
        self.enemy_tick = 0
        self.shoot_cooldown = 0
        self._spawn_enemies()
        self.msg_label.text = 'Drag to move\nTap to shoot'
        self.msg_label.opacity = 1

    def _spawn_enemies(self):
        w = Window.width
        start_x = (w - COLS_E * ENEMY_GAP_X) // 2
        start_y = Window.height - HEADER - 60
        self.enemies = [
            [start_x + c*ENEMY_GAP_X, start_y - r*ENEMY_GAP_Y]
            for r in range(ROWS) for c in range(COLS_E)
        ]

    def on_touch_down(self, touch):
        if not self.started:
            self.started = True
            self.msg_label.opacity = 0
            return
        if self.game_over:
            self.reset()
            self.started = True
            self.msg_label.opacity = 0
            return
        # tap = shoot
        if self.shoot_cooldown <= 0:
            bx = self.player_x + PLAYER_W//2 - BULLET_W//2
            self.bullets.append([bx, self.player_y + PLAYER_H])
            self.shoot_cooldown = 15

    def on_touch_move(self, touch):
        self.player_x = touch.x - PLAYER_W//2
        self.player_x = max(0, min(Window.width - PLAYER_W, self.player_x))

    def update(self, dt):
        if not self.started or self.game_over:
            self._draw(); return

        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)

        # move player bullets
        self.bullets = [[bx, by+10] for bx, by in self.bullets if by < Window.height]

        # move enemy bullets
        self.enemy_bullets = [[bx, by-6] for bx, by in self.enemy_bullets if by > HEADER]

        # enemy movement
        self.enemy_tick += 1
        speed = max(1, 3 - len(self.enemies)//10)
        if self.enemy_tick >= max(5, 20 - self.score//50):
            self.enemy_tick = 0
            move_down = False
            for e in self.enemies:
                if (self.enemy_dir == 1 and e[0] + ENEMY_W >= Window.width - 10) or \
                   (self.enemy_dir == -1 and e[0] <= 10):
                    move_down = True; break
            if move_down:
                self.enemy_dir *= -1
                for e in self.enemies: e[1] -= ENEMY_GAP_Y // 2
            else:
                for e in self.enemies: e[0] += self.enemy_dir * 8

        # enemy shoots
        if self.enemies and random.random() < 0.03:
            shooter = random.choice(self.enemies)
            self.enemy_bullets.append([shooter[0]+ENEMY_W//2, shooter[1]])

        # bullet-enemy collision
        remaining = []
        for e in self.enemies:
            hit = False
            for b in self.bullets[:]:
                if e[0] < b[0]+BULLET_W and b[0] < e[0]+ENEMY_W and \
                   e[1] < b[1]+BULLET_H and b[1] < e[1]+ENEMY_H:
                    self.bullets.remove(b)
                    self.score += 10
                    hit = True; break
            if not hit: remaining.append(e)
        self.enemies = remaining

        # enemy bullets hit player
        for b in self.enemy_bullets[:]:
            if (self.player_x < b[0] < self.player_x+PLAYER_W and
                    self.player_y < b[1] < self.player_y+PLAYER_H):
                self.enemy_bullets.remove(b)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    save_score('space_invaders', self.score)
                    self.msg_label.text = f'Game Over!\nScore: {self.score}\nTap to retry'
                    self.msg_label.opacity = 1

        # enemies reach player
        for e in self.enemies:
            if e[1] <= self.player_y + PLAYER_H:
                self.game_over = True
                save_score('space_invaders', self.score)
                self.msg_label.text = f'Game Over!\nTap to retry'
                self.msg_label.opacity = 1

        # next wave
        if not self.enemies:
            self._spawn_enemies()

        self.score_label.text = f'Score: {self.score}  ♥ {self.lives}'
        self.hi_label.text    = f'Best: {load_scores()["space_invaders"]}'
        self._draw()

    def _draw(self):
        w, h = Window.width, Window.height
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0,0), size=(w, h))
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=(0, h-HEADER), size=(w, HEADER))
            # player (triangle ship)
            Color(0.2, 0.8, 1, 1)
            Triangle(points=[
                self.player_x, self.player_y,
                self.player_x+PLAYER_W, self.player_y,
                self.player_x+PLAYER_W//2, self.player_y+PLAYER_H
            ])
            # player bullets
            Color(0, 1, 1, 1)
            for bx, by in self.bullets:
                Rectangle(pos=(bx, by), size=(BULLET_W, BULLET_H))
            # enemy bullets
            Color(1, 0.3, 0, 1)
            for bx, by in self.enemy_bullets:
                Rectangle(pos=(bx, by), size=(BULLET_W, ENEMY_BULLET_H))
            # enemies
            for i, (ex, ey) in enumerate(self.enemies):
                row = i // COLS_E
                Color(*([(1,0.2,0.2,1),(0.2,1,0.2,1),(0.8,0.4,1,1)][row % 3]))
                # body
                Rectangle(pos=(ex+4, ey+4), size=(ENEMY_W-8, ENEMY_H-6))
                Rectangle(pos=(ex, ey+8), size=(ENEMY_W, ENEMY_H-12))
                # legs
                Rectangle(pos=(ex, ey), size=(6, 6))
                Rectangle(pos=(ex+ENEMY_W-6, ey), size=(6, 6))
                # antennae
                Rectangle(pos=(ex+6, ey+ENEMY_H-2), size=(3, 6))
                Rectangle(pos=(ex+ENEMY_W-9, ey+ENEMY_H-2), size=(3, 6))
