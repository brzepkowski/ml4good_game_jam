import sys
import random
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, COLOR_BG, LIVES_START
from entities import Paddle, Ball, ParticleSystem
from levels import LEVELS, build_bricks
from hud import HUD
from sounds import SoundManager
from states import MenuState, CountdownState


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.sounds = SoundManager()
        self.hud    = HUD()

        self.score      = 0
        self.lives      = LIVES_START
        self.level_idx  = 0
        self.high_score = 0

        self.paddle    = Paddle()
        self.ball      = Ball()
        self.bricks    = []
        self.particles = ParticleSystem()

        self.shake_frames = 0
        self.shake_mag    = 0

        self.state = MenuState(self)

    def change_state(self, new_state):
        self.state = new_state

    def start_game(self):
        self.score     = 0
        self.lives     = LIVES_START
        self.level_idx = 0
        self.paddle    = Paddle()
        self.ball      = Ball()
        self.particles = ParticleSystem()
        self.bricks    = build_bricks(LEVELS[0]())
        self.change_state(CountdownState(self))

    def run(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.state.handle_event(event)

            self.state.update()

            self.canvas.fill(COLOR_BG)
            self.state.draw(self.canvas)

            if self.shake_frames > 0:
                dx = random.randint(-self.shake_mag, self.shake_mag)
                dy = random.randint(-self.shake_mag, self.shake_mag)
                self.screen.fill((0, 0, 0))
            else:
                dx, dy = 0, 0

            self.screen.blit(self.canvas, (dx, dy))
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
