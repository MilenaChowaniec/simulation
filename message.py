import pygame

class Message:

    def __init__(self, text: str, color: tuple):
        self._error_text = pygame.font.SysFont('Arial', 25, bold=False).render(text, True, color).convert_alpha()
        self._alpha = 255
        self._start = None

    def _print_text(self, coords: tuple, win):
        win.blit(self._error_text, (coords))
    
    def _update_set_alpha(self):
        if self._alpha > 0:
            self._alpha -= 0.13
            if self._alpha <= 0: 
                self._alpha = 0
                self._start = None
        self._error_text.set_alpha(self._alpha)
    
    def _start_time(self):
        self._start = pygame.time.get_ticks()
        self._alpha = 255
    
    def _get_start_time(self):
        return self._start