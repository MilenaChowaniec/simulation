import pygame
from enum import Enum

class State(Enum):
    DEFAULT = 1
    VIOLET = 2

# obiekt JEDNEGO targetu; 
# 1. ustawianie coords
# 2. rysowanie na mapie
# 3. zmiana stanu
# 4. powinien byc dict z texturami
class Target:
    def __init__(self, coords: tuple):
        self._coords = None

    def get_coords(self):
        return self._coords
    
    def set_coords(self, coords: tuple):
        self._coords = coords

    def print(self):
        pass



        