import pygame

class Line:
    def __init__(self, color: tuple, start_pos: tuple, end_pos: tuple, size: int, win):
        self._color = color
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._win = win
        self._size = size

    def draw(self):
        pygame.draw.line(self._win, self._color, self._start_pos, self._end_pos, self._size)
        

class Rect:
    def __init__(self, color: tuple, coords: tuple, win, size: int = 0, border_radius: int = 0):
        self._color = color
        self._coords = coords
        self._win = win
        self._border_radius = border_radius
        self._size = size
        self._rect = pygame.Rect(coords)
    
    def set_color(self, color: tuple):
        self._color = color

    def get_color(self) -> tuple:
        return self._color

    def get_rect(self):
        return self._rect

    def draw(self):
        pygame.draw.rect(self._win, self._color, self._coords, self._size, border_radius= self._border_radius)
