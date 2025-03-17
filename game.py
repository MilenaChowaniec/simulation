import window
import pygame

class Game:
    # konstruktor tworzy obiekt okna
    def __init__(self):
        self.__LENGTH = 1600
        self.__WIDTH = 800
        self.__win = window.Window(self.__LENGTH, self.__WIDTH)
    
    # wykonuje wszystkie eventy 
    def __poll_events(self):
        for event in pygame.event.get():
            self.__win._handle_event(event)

    # glowna petla 
    def play(self):
        while True:
            self.__poll_events()
            self.__win._render()
            self.__win._update()