import math
import random
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT, COLOR_BG, SCORE_TABLE, LIVES_START,
)
from levels import LEVELS, build_bricks


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _draw_bg(surface):
    surface.fill(COLOR_BG)
    dot_col = (30, 30, 45)
    for x in range(0, SCREEN_WIDTH, 40):
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.circle(surface, dot_col, (x, y), 1)


def _font(name, size, bold=False):
    try:
        return pygame.font.SysFont(name, size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size + 4)


def _draw_launch_hint(surface):
    f = _font("consolas", 17)
    surf = f.render("SPACE  to launch", True, (90, 90, 140))
    surface.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, SCREEN_HEIGHT - 28))


# ---------------------------------------------------------------------------
# Base state
# ---------------------------------------------------------------------------

class State:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self._tick = 0
        self._font_title = _font("consolas", 72, bold=True)
        self._font_sub   = _font("consolas", 26)
        self._font_info  = _font("consolas", 18)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.start_game()

    def update(self):
        self._tick += 1

    def draw(self, surface):
        _draw_bg(surface)

        scale = 1.0 + 0.03 * math.sin(self._tick * 0.05)
        raw   = self._font_title.render("BREAKOUT", True, (190, 210, 255))
        w = max(1, int(raw.get_width() * scale))
        h = max(1, int(raw.get_height() * scale))
        scaled = pygame.transform.smoothscale(raw, (w, h))
        surface.blit(scaled, (SCREEN_WIDTH // 2 - w // 2, 150))

        pulse = int(128 + 127 * math.sin(self._tick * 0.08))
        sub   = self._font_sub.render("PRESS  SPACE  TO  START", True,
                                      (pulse, pulse, pulse))
        surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 285))

        if self.game.high_score > 0:
            hs = self._font_info.render(f"BEST  {self.game.high_score:05d}",
                                        True, (130, 130, 200))
            surface.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, 355))

        hint = self._font_info.render(
            "←  →  or  A  D  to move     SPACE to launch", True, (70, 70, 110))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 435))


# ---------------------------------------------------------------------------
# Countdown  (3 … 2 … 1 …)
# ---------------------------------------------------------------------------

class CountdownState(State):
    def __init__(self, game):
        super().__init__(game)
        self._timer = 0
        self._font_num = _font("consolas", 100, bold=True)
        self._font_go  = _font("consolas",  80, bold=True)
        game.ball.reset(game.paddle)

    def update(self):
        keys = pygame.key.get_pressed()
        self.game.paddle.handle_input(keys)
        self.game.paddle.update()
        self.game.ball.attach_to(self.game.paddle)
        self._timer += 1
        if self._timer >= 60 * 4:
            self.game.change_state(PlayingState(self.game))

    def draw(self, surface):
        _draw_bg(surface)
        self.game.hud.draw(surface, self.game.score, self.game.lives,
                           self.game.level_idx + 1)
        for brick in self.game.bricks:
            if brick.alive:
                brick.draw(surface)
        self.game.paddle.draw(surface)
        self.game.ball.draw(surface)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))
        surface.blit(overlay, (0, 0))

        frame = self._timer // 60
        if frame < 3:
            label = str(3 - frame)
            col   = [(255, 100, 100), (255, 200, 60), (100, 220, 100)][frame]
            surf  = self._font_num.render(label, True, col)
        else:
            surf = self._font_go.render("GO!", True, (100, 255, 120))

        surface.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2,
                            SCREEN_HEIGHT // 2 - surf.get_height() // 2))


# ---------------------------------------------------------------------------
# Playing  (main game loop)
# ---------------------------------------------------------------------------

class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.game.change_state(PausedState(self.game))
            elif event.key == pygame.K_SPACE and self.game.ball.stuck:
                self.game.ball.launch()
                self.game.sounds.play('launch')

    def update(self):
        game = self.game
        keys = pygame.key.get_pressed()
        game.paddle.handle_input(keys)
        game.paddle.update()

        if game.ball.stuck:
            game.ball.attach_to(game.paddle)
        else:
            game.ball.update()
            self._resolve_collisions()

        game.particles.update()
        for brick in game.bricks:
            brick.update()

        if game.shake_frames > 0:
            game.shake_frames -= 1
            game.shake_mag = int(8 * game.shake_frames / 20)

    def _resolve_collisions(self):
        game = self.game
        ball = game.ball

        # Left / right walls
        if ball.x - ball.radius <= 0:
            ball.x = float(ball.radius)
            ball.vel_x = abs(ball.vel_x)
            game.sounds.play('wall_hit')
        elif ball.x + ball.radius >= SCREEN_WIDTH:
            ball.x = float(SCREEN_WIDTH - ball.radius)
            ball.vel_x = -abs(ball.vel_x)
            game.sounds.play('wall_hit')

        # Top wall
        if ball.y - ball.radius <= HUD_HEIGHT:
            ball.y = float(HUD_HEIGHT + ball.radius)
            ball.vel_y = abs(ball.vel_y)
            game.sounds.play('wall_hit')

        # Ball exits at bottom
        if ball.y - ball.radius > SCREEN_HEIGHT:
            self._lose_life()
            return

        # Paddle
        ball_rect = ball.get_rect()
        if ball_rect.colliderect(game.paddle.rect) and ball.vel_y > 0:
            factor = game.paddle.get_bounce_factor(ball.x)
            speed  = ball.speed
            angle  = factor * (math.pi / 3)
            ball.vel_x = speed * math.sin(angle)
            ball.vel_y = -speed * math.cos(angle)
            ball.clamp_angle()
            ball.y = float(game.paddle.rect.top - ball.radius - 1)
            game.paddle.set_flash()
            game.sounds.play('paddle_hit')

        # Bricks
        ball_rect = ball.get_rect()
        for brick in game.bricks:
            if not brick.alive or not ball_rect.colliderect(brick.rect):
                continue

            dx_left  = ball_rect.right  - brick.rect.left
            dx_right = brick.rect.right - ball_rect.left
            dy_top   = ball_rect.bottom - brick.rect.top
            dy_bot   = brick.rect.bottom - ball_rect.top

            if min(dx_left, dx_right) < min(dy_top, dy_bot):
                ball.vel_x *= -1
            else:
                ball.vel_y *= -1

            destroyed = brick.hit()
            ball.increase_speed()

            if destroyed:
                game.score += SCORE_TABLE.get(brick.hits_required, 10)
                game.particles.emit(brick.rect.centerx, brick.rect.centery,
                                    brick.base_color)
                game.sounds.play('brick_break')
            else:
                game.sounds.play('brick_hit')

            break  # one brick per frame prevents double-reversal

        # Level clear?
        if all(not b.alive for b in game.bricks):
            self._level_win()

    def _lose_life(self):
        game = self.game
        game.lives -= 1
        game.shake_frames = 20
        game.shake_mag    = 8
        game.sounds.play('life_lost')
        if game.lives <= 0:
            game.high_score = max(game.high_score, game.score)
            game.change_state(GameOverState(game))
        else:
            game.change_state(CountdownState(game))

    def _level_win(self):
        game = self.game
        game.high_score = max(game.high_score, game.score)
        game.sounds.play('level_win')
        game.change_state(LevelWinState(game))

    def draw(self, surface):
        game = self.game
        _draw_bg(surface)
        game.hud.draw(surface, game.score, game.lives, game.level_idx + 1)
        for brick in game.bricks:
            if brick.alive:
                brick.draw(surface)
        game.particles.draw(surface)
        game.paddle.draw(surface)
        game.ball.draw(surface)
        if game.ball.stuck:
            _draw_launch_hint(surface)


# ---------------------------------------------------------------------------
# Paused
# ---------------------------------------------------------------------------

class PausedState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            self.game.change_state(PlayingState(self.game))

    def draw(self, surface):
        game = self.game
        _draw_bg(surface)
        game.hud.draw(surface, game.score, game.lives, game.level_idx + 1)
        for brick in game.bricks:
            if brick.alive:
                brick.draw(surface)
        game.particles.draw(surface)
        game.paddle.draw(surface)
        game.ball.draw(surface)
        game.hud.draw_overlay(surface, "PAUSED",
                              "PRESS  ESC  OR  P  TO  CONTINUE")


# ---------------------------------------------------------------------------
# Level win
# ---------------------------------------------------------------------------

class LevelWinState(State):
    def __init__(self, game):
        super().__init__(game)
        self._timer    = 0
        self._advanced = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._advance()

    def update(self):
        self._timer += 1
        if self._timer >= 150:
            self._advance()

    def _advance(self):
        if self._advanced:
            return
        self._advanced = True
        game = self.game
        game.level_idx += 1
        if game.level_idx >= len(LEVELS):
            game.change_state(VictoryState(game))
        else:
            game.bricks = build_bricks(LEVELS[game.level_idx]())
            game.particles.clear()
            game.change_state(CountdownState(game))

    def draw(self, surface):
        _draw_bg(surface)
        self.game.hud.draw(surface, self.game.score, self.game.lives,
                           self.game.level_idx + 1)
        self.game.hud.draw_overlay(surface, "LEVEL  CLEAR!",
                                   f"SCORE  {self.game.score:05d}",
                                   "SPACE  or  wait...")


# ---------------------------------------------------------------------------
# Game over
# ---------------------------------------------------------------------------

class GameOverState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.change_state(MenuState(self.game))

    def draw(self, surface):
        _draw_bg(surface)
        self.game.hud.draw_overlay(surface, "GAME  OVER",
                                   f"SCORE  {self.game.score:05d}",
                                   "PRESS  SPACE")


# ---------------------------------------------------------------------------
# Victory
# ---------------------------------------------------------------------------

class VictoryState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.change_state(MenuState(self.game))

    def draw(self, surface):
        _draw_bg(surface)
        self.game.hud.draw_overlay(surface, "YOU  WIN!",
                                   f"SCORE  {self.game.score:05d}",
                                   "PRESS  SPACE")
