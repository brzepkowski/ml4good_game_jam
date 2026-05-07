import array
import math
import pygame


class SoundManager:
    def __init__(self):
        self._enabled = False
        self._sounds  = {}
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self._enabled = True
            self._sounds  = self._build_sounds()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Sample generators (return plain lists of 16-bit signed integers)
    # ------------------------------------------------------------------

    def _sine(self, freq, duration_ms, volume=0.5):
        rate = 44100
        n    = int(rate * duration_ms / 1000)
        return [int(32767 * volume * math.sin(2 * math.pi * freq * i / rate))
                for i in range(n)]

    def _sweep(self, f_start, f_end, duration_ms, volume=0.5):
        rate = 44100
        n    = int(rate * duration_ms / 1000)
        return [int(32767 * volume *
                    math.sin(2 * math.pi * (f_start + (f_end - f_start) * i / n) * i / rate))
                for i in range(n)]

    def _arpeggio(self, freqs, total_ms, volume=0.5):
        rate     = 44100
        note_n   = int(rate * total_ms / 1000 / len(freqs))
        samples  = []
        for freq in freqs:
            samples.extend(
                int(32767 * volume * math.sin(2 * math.pi * freq * i / rate))
                for i in range(note_n)
            )
        return samples

    def _fade_out(self, samples, fade_ms=25):
        rate   = 44100
        fade_n = int(rate * fade_ms / 1000)
        result = list(samples)
        for i in range(min(fade_n, len(result))):
            frac = i / fade_n
            result[-(i + 1)] = int(result[-(i + 1)] * frac)
        return result

    def _make_sound(self, samples):
        buf = array.array('h', samples)
        return pygame.mixer.Sound(buffer=buf)

    # ------------------------------------------------------------------
    # Build all sounds
    # ------------------------------------------------------------------

    def _build_sounds(self):
        s = {}
        try:
            s['paddle_hit']  = self._make_sound(self._fade_out(self._sine(440,  80, 0.4)))
            s['wall_hit']    = self._make_sound(self._fade_out(self._sine(330,  60, 0.3)))
            s['brick_hit']   = self._make_sound(self._fade_out(self._sine(520,  70, 0.4)))
            s['brick_break'] = self._make_sound(self._fade_out(
                                   self._arpeggio([640, 400], 130, 0.5)))
            s['life_lost']   = self._make_sound(self._fade_out(
                                   self._sweep(400, 120, 500, 0.6)))
            s['level_win']   = self._make_sound(self._fade_out(
                                   self._arpeggio([262, 330, 392, 523], 600, 0.5)))
            s['game_over']   = self._make_sound(self._fade_out(self._sine(140, 800, 0.5)))
            s['launch']      = self._make_sound(self._fade_out(self._sine(480,  55, 0.3)))
        except Exception:
            pass
        return s

    def play(self, name):
        if self._enabled and name in self._sounds:
            try:
                self._sounds[name].play()
            except Exception:
                pass
