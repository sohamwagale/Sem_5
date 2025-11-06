#!/usr/bin/env python3
"""
dino_terminal.py - simple Chrome Dino-like game in the terminal using curses.

Controls:
  Space / w -> Jump
  s / Down  -> Duck (hold)
  q         -> Quit
  r         -> Restart after Game Over

Requires:
  - Linux / macOS: Python with curses (builtin)
  - Windows: pip install windows-curses
"""

import curses
import time
import random
import math
import os

HIGHSCORE_FILE = "dino_highscore.txt"

# ---------- Dino constants (tweak to taste) ----------
GRAVITY = 60.0          # pixels per second^2 (virtual pixels are terminal rows)
JUMP_VELOCITY = -24.0     # initial jump velocity (negative = up)
BASE_SPEED = 30.0        # virtual columns per second
SPEED_INCREMENT = 0.5    # speed increase per 100 points
FPS = 25.0

# ---------- Helper functions ----------
def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(int(score)))
    except Exception:
        pass

def clamp(v, a, b):
    return max(a, min(b, v))

# ---------- Entities ----------
class Dino:
    def __init__(self, x, ground_row):
        self.x = float(x)
        self.ground_row = ground_row  # row index of the ground (0 top)
        self.y = float(ground_row)    # current bottom row of the dino (float)
        self.vy = 0.0
        self.state = "running"        # running, jumping, ducking
        self.width = 4                # columns
        self.height = 3               # rows when standing
        self.duck_height = 1          # rows when ducking
        self.run_anim = 0.0

    def start_jump(self):
        if self.state != "jumping":
            self.vy = JUMP_VELOCITY
            self.state = "jumping"

    def start_duck(self):
        if self.state == "running":
            self.state = "ducking"

    def stop_duck(self):
        if self.state == "ducking":
            self.state = "running"

    def update(self, dt):
        if self.state == "jumping":
            self.vy += GRAVITY * dt
            self.y += self.vy * dt 
            if self.y >= self.ground_row:
                self.y = float(self.ground_row)
                self.vy = 0.0
                self.state = "running"
        # running animation (for visual variation)
        self.run_anim += dt * 6.0
        if self.run_anim > 2.0:
            self.run_anim -= 2.0

    def get_bbox(self):
        """
        Return bounding box in terminal coords as (left, top, right, bottom)
        Terminal: row (y) increases downward. We'll treat y as the bottom row of dino.
        """
        left = int(self.x)
        bottom = int(round(self.y))
        if self.state == "ducking":
            h = self.duck_height
        else:
            h = self.height
        top = bottom - h + 1
        right = left + self.width - 1
        return left, top, right, bottom

    def draw(self, stdscr):
        x = int(self.x)
        bottom = int(round(self.y))
        if self.state == "ducking":
            sprite = ["\\_0_/"]  # duck sprite (one row)
            for i, line in enumerate(reversed(sprite)):
                row = bottom - i
                try:
                    stdscr.addstr(row, x, line)
                except Exception:
                    pass
        else:
            # simple 3-row standing sprite, run_anim toggles foot
            foot = "\\" if self.run_anim < 1.0 else "/"
            sprite = [
                "  ᴖ ",      # head row (keep narrow)
                " /|\\",     # arms
                f" /{foot} "  # legs (animated)
            ]
            for i, line in enumerate(reversed(sprite)):
                row = bottom - i
                try:
                    stdscr.addstr(row, x, line)
                except Exception:
                    pass

class Obstacle:
    def __init__(self, x, ground_row, kind="cactus"):
        self.x = float(x)
        self.kind = kind  # 'cactus' or 'ptera'
        self.ground_row = ground_row
        if kind == "cactus":
            self.width = 3
            self.height = 3
            self.y = ground_row - (self.height - 1)  # top row of sprite calculation uses bottom coords
        elif kind == "ptera":
            self.width = 5
            self.height = 2
            # flying height randomized
            self.y = ground_row - 5 - random.randint(0, 3)
        self.offscreen = False

    def update(self, dt, speed):
        self.x -= speed * dt
        if self.x + self.width < 0:
            self.offscreen = True

    def get_bbox(self):
        left = int(self.x)
        right = left + self.width - 1
        bottom = int(self.ground_row if self.kind == "cactus" else self.y + self.height - 1)
        top = bottom - (self.height - 1)
        return left, top, right, bottom

    def draw(self, stdscr):
        x = int(self.x)
        if self.kind == "cactus":
            # draw small cactus ~3 rows
            rows = [
                " # ",
                "###",
                " # "
            ]
            bottom = int(self.ground_row)
            for i, line in enumerate(reversed(rows)):
                row = bottom - i
                try:
                    stdscr.addstr(row, x, line)
                except Exception:
                    pass
        elif self.kind == "ptera":
            # drawing a little pterodactyl: 2 rows
            rows = [
                r"\/V\/",
                r" \_/ "
            ]
            top = int(self.y)
            for i, line in enumerate(rows):
                row = top + i
                try:
                    stdscr.addstr(row, x, line)
                except Exception:
                    pass

# ---------- Game engine ----------
class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.rows, self.cols = stdscr.getmaxyx()
        self.ground_row = self.rows - 3  # leave 2 rows for UI
        self.dino = Dino(10, self.ground_row)
        self.obstacles = []
        self.base_speed = BASE_SPEED
        self.speed = self.base_speed
        self.score = 0.0
        self._last_spawn = 0.0
        self._next_gap = self._calc_gap()
        self.running = True
        self.game_over = False
        self.highscore = load_highscore()
        self.start_time = time.time()
        self.pause_until = 0.0

    def reset(self):
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.ground_row = self.rows - 3
        self.dino = Dino(10, self.ground_row)
        self.obstacles = []
        self.speed = self.base_speed
        self.score = 0.0
        self._last_spawn = 0.0
        self._next_gap = self._calc_gap()
        self.running = True
        self.game_over = False
        self.start_time = time.time()

    def _calc_gap(self):
        # gap between obstacles in virtual seconds; shrink with speed/score
        base = clamp(1.0 + (2.0 - (self.speed / 60.0)), 0.5, 2.5)
        var = random.uniform(0.0, 1.5)
        return base + var

    def spawn_obstacle(self):
        # choose type biased to cactus; as score increases, more ptera
        kinds = ["cactus"] * 6 + ["ptera"] * (1 + int(self.score // 150))
        kind = random.choice(kinds)
        x = self.cols - 2
        obs = Obstacle(x, self.ground_row, kind=kind)
        self.obstacles.append(obs)

    def handle_input(self, key):
        if key == -1:
            return
        if key in (ord("q"), ord("Q")):
            self.running = False
        if self.game_over:
            if key in (ord("r"), ord("R")):
                self.reset()
            return
        if key in (curses.KEY_DOWN, ord("s"), ord("S")):
            self.dino.start_duck()
        elif key in (ord(" "), ord("w"), ord("W"), curses.KEY_UP):
            self.dino.start_jump()
        elif key == -1:
            pass

    def handle_key_release(self, key):
        # We don't have key release detection in curses; we use a simple timeout to stop ducking
        pass

    def update(self, dt):
        if not self.running:
            return
        if self.game_over:
            return

        # Update speed scaling with score
        self.speed = self.base_speed + (self.score // 100) * SPEED_INCREMENT

        # Update dino
        self.dino.update(dt)

        # Update obstacles
        for o in self.obstacles:
            o.update(dt, self.speed)
        self.obstacles = [o for o in self.obstacles if not o.offscreen]

        # Spawning obstacles by time gap
        self._last_spawn += dt
        if self._last_spawn >= self._next_gap:
            self.spawn_obstacle()
            self._last_spawn = 0.0
            self._next_gap = self._calc_gap()

        # Update score (score increments with time and speed)
        self.score += dt * (self.speed / 10.0) * 10.0  # tuned for reasonable growth

        # Check collisions
        for o in self.obstacles:
            if self._collides(self.dino, o):
                self.game_over = True
                # update highscore if needed
                if int(self.score) > self.highscore:
                    self.highscore = int(self.score)
                    save_highscore(self.highscore)
                break

        # simple ducking timeout: if key not pressed, dino stays ducking only while key is held.
        # Because curses doesn't let us see key release easily, we will auto-release duck after short window
        if self.dino.state == "ducking":
            # small artificial timeout to avoid stuck duck
            # (players will press down to duck; if they stop pressing, they'll release next frame)
            # We'll check getch in main loop to clear duck state when no down pressed.
            pass

    def _collides(self, dino, obs):
        dl, dt, dr, db = dino.get_bbox()
        ol, ot, or_, ob = obs.get_bbox()
        # AABB overlap check
        if dr < ol or or_ < dl or db < ot or ob < dt:
            return False
        return True

    def render(self):
        stdscr = self.stdscr
        stdscr.erase()
        rows, cols = self.rows, self.cols

        # Draw sky (empty) and ground line
        ground_y = self.ground_row + 1
        try:
            stdscr.hline(ground_y, 0, "-", cols)
        except Exception:
            pass

        # Draw score and UI top-left
        score_text = f"Score: {int(self.score)}  Speed: {int(self.speed)}  High: {self.highscore}"
        try:
            stdscr.addstr(0, 2, score_text)
        except Exception:
            pass

        # Draw dino and obstacles
        self.dino.draw(stdscr)
        for o in self.obstacles:
            o.draw(stdscr)

        # Draw instructions bottom-left
        try:
            stdscr.addstr(rows - 1, 2, "Space/w:Jump  s/Down:Duck  q:Quit")
        except Exception:
            pass

        # If game over, show overlay
        if self.game_over:
            go_text = " GAME OVER "
            restart_text = "Press 'r' to restart or 'q' to quit"
            try:
                mid_row = rows // 2
                mid_col = cols // 2
                stdscr.addstr(mid_row - 1, max(2, mid_col - len(go_text)//2), go_text)
                stdscr.addstr(mid_row + 1, max(2, mid_col - len(restart_text)//2), restart_text)
            except Exception:
                pass

        # Refresh
        try:
            stdscr.refresh()
        except Exception:
            pass

# ---------- Main loop ----------
def main(stdscr):
    # Setup
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)
    stdscr.keypad(True)

    # Colors if supported
    if curses.has_colors():
        curses.start_color()

    game = Game(stdscr)
    dt_target = 1.0 / FPS
    prev_time = time.time()

    # We'll track whether DOWN is pressed by checking getch each frame and
    # if no down pressed, release duck (common approach in simple curses games).
    down_keys = {curses.KEY_DOWN, ord("s"), ord("S")}

    try:
        while game.running:
            now = time.time()
            dt = now - prev_time
            prev_time = now
            if dt > 0.2:
                # clamp large dt (e.g., when switching windows)
                dt = 0.2

            # handle input (consume all keys in buffer this frame)
            pressed_down = False
            key = stdscr.getch()
            while key != -1:
                # we'll process main interactive keys; for duck, detect if held
                if key in down_keys:
                    pressed_down = True
                # pass key to game
                game.handle_input(key)
                # if user pressed 's' as duck and then later stops sending key, we'll detect no held-down
                key = stdscr.getch()

            # if not holding down, ensure dino stops ducking
            if not pressed_down and game.dino.state == "ducking":
                game.dino.stop_duck()

            game.update(dt)
            game.render()

            # frame cap
            elapsed = time.time() - now
            to_sleep = dt_target - elapsed
            if to_sleep > 0:
                time.sleep(to_sleep)

    except KeyboardInterrupt:
        pass
    finally:
        # on exit restore cursor (curses.wrapper will also do this)
        curses.curs_set(1)

if __name__ == "__main__":
    curses.wrapper(main)
