import window
import pygame

# main loop

class Game:
    def __init__(self):
        self._LENGTH = 1600
        self._WIDTH = 800
        self._win = window.Window(self._LENGTH, self._WIDTH)
    
    def _poll_events(self):
        for event in pygame.event.get():
            self._win._handle_event(event)

    def play(self):
        while True:
            self._poll_events()
            self._win._render()
            self._win._update()