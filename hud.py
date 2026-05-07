import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT, COLOR_TEXT


def _load_font(name, size, bold=False):
    try:
        return pygame.font.SysFont(name, size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size + 4)


class HUD:
    def __init__(self):
        self._font_score = _load_font("consolas", 22, bold=True)
        self._font_level = _load_font("consolas", 20, bold=True)
        self._font_heart = _load_font("segoeuisymbol", 20)

    def draw(self, surface, score, lives, level):
        bar = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT))
        bar.fill((10, 10, 20))
        surface.blit(bar, (0, 0))
        pygame.draw.line(surface, (50, 50, 90),
                         (0, HUD_HEIGHT - 1), (SCREEN_WIDTH, HUD_HEIGHT - 1), 1)

        score_surf = self._font_score.render(f"SCORE  {score:05d}", True, COLOR_TEXT)
        surface.blit(score_surf, (12, (HUD_HEIGHT - score_surf.get_height()) // 2))

        level_surf = self._font_level.render(f"LEVEL {level}", True, (180, 180, 255))
        surface.blit(level_surf,
                     (SCREEN_WIDTH // 2 - level_surf.get_width() // 2,
                      (HUD_HEIGHT - level_surf.get_height()) // 2))

        heart_surf = self._font_heart.render("♥", True, (255, 80, 100))
        hx = SCREEN_WIDTH - 12
        hy = (HUD_HEIGHT - heart_surf.get_height()) // 2
        for _ in range(max(0, lives)):
            hx -= heart_surf.get_width() + 4
            surface.blit(heart_surf, (hx, hy))

    def draw_overlay(self, surface, title, subtitle="", subtitle2=""):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        font_big = _load_font("consolas", 56, bold=True)
        font_sub = _load_font("consolas", 26)

        title_surf = font_big.render(title, True, (255, 255, 255))
        surface.blit(title_surf,
                     (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 210))

        if subtitle:
            sub_surf = font_sub.render(subtitle, True, (200, 200, 200))
            surface.blit(sub_surf,
                         (SCREEN_WIDTH // 2 - sub_surf.get_width() // 2, 295))

        if subtitle2:
            sub2_surf = font_sub.render(subtitle2, True, (130, 130, 190))
            surface.blit(sub2_surf,
                         (SCREEN_WIDTH // 2 - sub2_surf.get_width() // 2, 340))
