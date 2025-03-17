import pygame

class Line:
    def __init__(self, color: tuple, start_pos: tuple, end_pos: tuple, size: int, win):
        self.__color = color
        self.__start_pos = start_pos
        self.__end_pos = end_pos
        self.__win = win
        self.__size = size

    def draw(self):
        pygame.draw.line(self.__win, self.__color, self.__start_pos, self.__end_pos, self.__size)
        

class Rect:
    def __init__(self, color: tuple, coords: tuple, win, size: int = 0, border_radius: int = 0):
        self.__color = color
        self.__coords = coords
        self.__win = win
        self.__border_radius = border_radius
        self.__size = size
        self.__rect = pygame.Rect(coords)
    
    def set_color(self, color: tuple):
        self.__color = color

    def get_color(self) -> tuple:
        return self.__color

    def get_rect(self):
        return self.__rect

    def draw(self):
        pygame.draw.rect(self.__win, self.__color, self.__coords, self.__size, border_radius= self.__border_radius)
