import math
import random
from collections import deque
import pygame

from settings import (
    COLOR_BG, COLOR_PADDLE,
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, PADDLE_Y_OFFSET,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BALL_RADIUS, BALL_SPEED_INIT, BALL_SPEED_MAX, BALL_SPEED_STEP, BALL_TRAIL_LEN,
    BRICK_COLORS, BRICK_WIDTH, BRICK_HEIGHT, BRICK_MARGIN_X, BRICK_MARGIN_TOP, BRICK_GAP,
    HUD_HEIGHT, PARTICLE_COUNT, PARTICLE_LIFETIME, PARTICLE_SPEED,
)


class Paddle:
    def __init__(self):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT - PADDLE_Y_OFFSET
        self.rect = pygame.Rect(cx - PADDLE_WIDTH // 2, cy, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.vel_x = 0.0
        self.flash_timer = 0

    def handle_input(self, keys):
        target = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            target = -PADDLE_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            target = PADDLE_SPEED
        self.vel_x = self.vel_x * 0.7 + target * 0.3

    def update(self):
        self.rect.x += int(self.vel_x)
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        if self.flash_timer > 0:
            self.flash_timer -= 1

    def set_flash(self):
        self.flash_timer = 10

    def get_bounce_factor(self, ball_x):
        half = self.rect.width / 2
        factor = (ball_x - self.rect.centerx) / half
        return max(-0.9, min(0.9, factor))

    def draw(self, surface):
        color = (255, 255, 255) if self.flash_timer > 0 else COLOR_PADDLE
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        top_strip = pygame.Rect(self.rect.x + 3, self.rect.y + 2, self.rect.width - 6, 3)
        pygame.draw.rect(surface, (255, 255, 255), top_strip, border_radius=2)
        border_col = (180, 180, 255) if self.flash_timer > 0 else (80, 80, 150)
        pygame.draw.rect(surface, border_col, self.rect, 2, border_radius=4)


class Ball:
    def __init__(self):
        self.x = float(SCREEN_WIDTH // 2)
        self.y = float(SCREEN_HEIGHT // 2)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.radius = BALL_RADIUS
        self.speed  = BALL_SPEED_INIT
        self.trail  = deque(maxlen=BALL_TRAIL_LEN)
        self.stuck  = True
        self.stuck_offset = 0.0

    def attach_to(self, paddle):
        self.x = paddle.rect.centerx + self.stuck_offset
        self.y = paddle.rect.top - self.radius - 1

    def launch(self):
        angle = -math.pi / 2 + random.uniform(-0.3, 0.3)
        self.vel_x = self.speed * math.cos(angle)
        self.vel_y = self.speed * math.sin(angle)
        self.stuck = False

    def reset(self, paddle):
        self.speed = BALL_SPEED_INIT
        self.stuck = True
        self.stuck_offset = 0.0
        self.trail.clear()
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.attach_to(paddle)

    def update(self):
        self.trail.append((self.x, self.y))
        self.x += self.vel_x
        self.y += self.vel_y

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )

    def increase_speed(self):
        self.speed = min(self.speed + BALL_SPEED_STEP, BALL_SPEED_MAX)
        spd = math.hypot(self.vel_x, self.vel_y)
        if spd > 0:
            scale = self.speed / spd
            self.vel_x *= scale
            self.vel_y *= scale

    def clamp_angle(self):
        min_vy = 1.5
        if abs(self.vel_y) < min_vy:
            sign = 1 if self.vel_y >= 0 else -1
            self.vel_y = sign * min_vy
            spd = math.hypot(self.vel_x, self.vel_y)
            if spd > 0:
                scale = self.speed / spd
                self.vel_x *= scale
                self.vel_y *= scale

    def draw(self, surface):
        trail_list = list(self.trail)
        n = len(trail_list)
        for i, (tx, ty) in enumerate(trail_list):
            frac = (i + 1) / max(n, 1)
            r = max(1, int(self.radius * frac * 0.75))
            col = (int(80 * frac), int(110 * frac), 220)
            pygame.draw.circle(surface, col, (int(tx), int(ty)), r)
        pygame.draw.circle(surface, (80, 100, 200), (int(self.x), int(self.y)), self.radius + 3)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)


class Brick:
    def __init__(self, col, row, hits_required):
        ox = BRICK_MARGIN_X
        oy = HUD_HEIGHT + BRICK_MARGIN_TOP
        x  = ox + col * (BRICK_WIDTH + BRICK_GAP)
        y  = oy + row * (BRICK_HEIGHT + BRICK_GAP)
        self.rect          = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hits_required = hits_required
        self.hits_taken    = 0
        self.base_color    = BRICK_COLORS[row % len(BRICK_COLORS)]
        self.alive         = True
        self.crack_alpha   = 0

    @property
    def color(self):
        factor = 1.0 - 0.35 * (self.hits_taken / max(self.hits_required, 1))
        return tuple(int(c * factor) for c in self.base_color)

    def hit(self):
        self.hits_taken += 1
        self.crack_alpha = 255
        if self.hits_taken >= self.hits_required:
            self.alive = False
            return True
        return False

    def update(self):
        if self.crack_alpha > 80:
            self.crack_alpha = max(80, self.crack_alpha - 8)

    def draw(self, surface):
        col = self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=3)

        hl = tuple(min(255, c + 70) for c in col)
        pygame.draw.line(surface, hl, self.rect.topleft,
                         (self.rect.right - 1, self.rect.top), 2)
        pygame.draw.line(surface, hl, self.rect.topleft,
                         (self.rect.left, self.rect.bottom - 1), 1)

        sh = tuple(max(0, c - 70) for c in col)
        pygame.draw.line(surface, sh,
                         (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right - 1, self.rect.bottom - 1), 2)
        pygame.draw.line(surface, sh,
                         (self.rect.right - 1, self.rect.top),
                         (self.rect.right - 1, self.rect.bottom - 1), 1)

        if self.crack_alpha > 0 and self.hits_taken > 0:
            cw, ch = self.rect.width, self.rect.height
            crack_surf = pygame.Surface((cw, ch), pygame.SRCALPHA)
            a = self.crack_alpha
            pygame.draw.line(crack_surf, (0, 0, 0, a), (4, 4), (cw - 4, ch - 4), 2)
            pygame.draw.line(crack_surf, (0, 0, 0, a), (cw - 4, 4), (4, ch - 4), 2)
            if self.hits_taken >= 2:
                pygame.draw.line(crack_surf, (0, 0, 0, a), (cw // 2, 2), (cw // 2, ch - 2), 1)
            surface.blit(crack_surf, self.rect.topleft)


class Particle:
    def __init__(self, x, y, color):
        self.x    = float(x)
        self.y    = float(y)
        self.vel_x = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.vel_y = random.uniform(-PARTICLE_SPEED, 0)
        self.lifetime = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME
        self.color    = color
        self.size     = random.randint(2, 5)

    def update(self):
        self.x     += self.vel_x
        self.y     += self.vel_y
        self.vel_y += 0.15
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        frac = self.lifetime / self.max_life
        col = (
            int(self.color[0] * frac + COLOR_BG[0] * (1 - frac)),
            int(self.color[1] * frac + COLOR_BG[1] * (1 - frac)),
            int(self.color[2] * frac + COLOR_BG[2] * (1 - frac)),
        )
        radius = max(1, int(self.size * frac))
        pygame.draw.circle(surface, col, (int(self.x), int(self.y)), radius)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=PARTICLE_COUNT):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    def clear(self):
        self.particles.clear()
