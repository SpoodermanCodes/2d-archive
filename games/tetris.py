import random, copy
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from shared.constants import *
from shared.scores import save_score, load_scores

COLS = 10
BLOCK = 28


def _rows():
    return (int(Window.height) - HEADER) // BLOCK


class TetrisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_label = Label(pos=(Window.width*0.35, Window.height-42), font_size=18, color=(1,1,1,1))
        self.hi_label    = Label(pos=(Window.width*0.6,  Window.height-42), font_size=18, color=(1,1,1,1))
        self.msg_label   = Label(text='Tap to start', pos=(Window.width*0.3, Window.height//2-20), font_size=22, color=(1,1,0,1))
        self.add_widget(self.score_label)
        self.add_widget(self.hi_label)
        self.add_widget(self.msg_label)
        self._clock = None
        self.touch_start = None

    def on_enter(self):
        self.reset()
        self._clock = Clock.schedule_interval(self.update, 0.5)

    def on_leave(self):
        if self._clock: self._clock.cancel()

    def reset(self):
        rows = _rows()
        self.board = [[None]*COLS for _ in range(rows)]
        self.score = 0
        self.game_over = False
        self.started = False
        self.piece = None
        self.msg_label.text = 'Tap to start'
        self.msg_label.opacity = 1
        self._new_piece()

    def _new_piece(self):
        kind = random.choice(list(TETROMINO_SHAPES.keys()))
        self.piece = {
            'kind': kind,
            'shape': [row[:] for row in TETROMINO_SHAPES[kind]],
            'color': TETROMINO_COLORS[kind],
            'x': COLS//2 - len(TETROMINO_SHAPES[kind][0])//2,
            'y': _rows() - 2,
        }
        if self._collides(self.piece, 0, 0):
            self.game_over = True
            save_score('tetris', self.score)
            self.msg_label.text = 'Game Over! Tap to retry'
            self.msg_label.opacity = 1

    def _collides(self, piece, dx, dy):
        rows = _rows()
        for r, row in enumerate(piece['shape']):
            for c, cell in enumerate(row):
                if not cell: continue
                nx, ny = piece['x']+c+dx, piece['y']-r+dy
                if nx < 0 or nx >= COLS or ny < 0: return True
                if ny < rows and self.board[ny][nx]: return True
        return False

    def _lock(self):
        rows = _rows()
        for r, row in enumerate(self.piece['shape']):
            for c, cell in enumerate(row):
                if cell:
                    ny = self.piece['y'] - r
                    if 0 <= ny < rows:
                        self.board[ny][self.piece['x']+c] = self.piece['color']
        self._clear_lines()
        self._new_piece()

    def _clear_lines(self):
        rows = _rows()
        new_board = [row for row in self.board if not all(row)]
        cleared = rows - len(new_board)
        if cleared:
            self.score += [0,100,300,500,800][min(cleared,4)]
            if self._clock:
                self._clock.cancel()
                speed = max(0.1, 0.5 - self.score // 1000 * 0.05)
                self._clock = Clock.schedule_interval(self.update, speed)
        self.board = [[None]*COLS]*cleared + new_board

    def _rotate(self):
        s = self.piece['shape']
        rotated = [list(row) for row in zip(*s[::-1])]
        old = self.piece['shape']
        self.piece['shape'] = rotated
        if self._collides(self.piece, 0, 0):
            self.piece['shape'] = old

    def on_touch_down(self, touch):
        self.touch_start = (touch.x, touch.y)
        if not self.started:
            self.started = True
            self.msg_label.opacity = 0
        elif self.game_over:
            self.reset()
            self.started = True
            self.msg_label.opacity = 0

    def on_touch_up(self, touch):
        if not self.touch_start or not self.started or self.game_over: return
        dx = touch.x - self.touch_start[0]
        dy = touch.y - self.touch_start[1]
        if abs(dx) < 15 and abs(dy) < 15:
            self._rotate()
        elif abs(dx) > abs(dy):
            steps = max(1, int(abs(dx) / BLOCK))
            move = 1 if dx > 0 else -1
            for _ in range(steps):
                if not self._collides(self.piece, move, 0):
                    self.piece['x'] += move
        else:
            if dy < -30:
                while not self._collides(self.piece, 0, -1):
                    self.piece['y'] -= 1
                self._lock()

    def update(self, dt):
        if self.started and not self.game_over:
            if not self._collides(self.piece, 0, -1):
                self.piece['y'] -= 1
            else:
                self._lock()
        self.score_label.text = f'Score: {self.score}'
        self.hi_label.text    = f'Best: {load_scores()["tetris"]}'
        self._draw()

    def _draw(self):
        rows = _rows()
        ox = (Window.width - COLS * BLOCK) // 2
        oy = HEADER
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0,0), size=(Window.width, Window.height))
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=(0, Window.height-HEADER), size=(Window.width, HEADER))
            # board bg
            Color(0.05, 0.05, 0.05, 1)
            Rectangle(pos=(ox, oy), size=(COLS*BLOCK, rows*BLOCK))
            # locked cells
            for r in range(rows):
                for c in range(COLS):
                    if self.board[r][c]:
                        Color(*self.board[r][c])
                        Rectangle(pos=(ox+c*BLOCK+1, oy+r*BLOCK+1), size=(BLOCK-2, BLOCK-2))
            # active piece
            if self.piece:
                Color(*self.piece['color'])
                for r, row in enumerate(self.piece['shape']):
                    for c, cell in enumerate(row):
                        if cell:
                            px = ox + (self.piece['x']+c)*BLOCK
                            py = oy + (self.piece['y']-r)*BLOCK
                            Rectangle(pos=(px+1, py+1), size=(BLOCK-2, BLOCK-2))
            # grid lines
            Color(0.15, 0.15, 0.15, 1)
            for c in range(COLS+1):
                Rectangle(pos=(ox+c*BLOCK, oy), size=(1, rows*BLOCK))
            for r in range(rows+1):
                Rectangle(pos=(ox, oy+r*BLOCK), size=(COLS*BLOCK, 1))
