import shapes
import sys
import pygame

class Window:
    # konstruktor tworzy okno
    def __init__(self, length: int, width: int):
        self._init_window(length, width)
        self._init_var()
        self._init_colors()
        self._init_shapes()
        self._init_text()
        self._init_grid()
    
    def _init_window(self, length: int, width: int):
        self._win = pygame.display.set_mode((length, width))
        pygame.display.set_caption("simulation")
        self._length = length
        self._width = width
        self._interface_length = length / 4
    
    def _init_var(self):
        self._IS_ON = False # czy symulacja jest wlaczona
        self._IS_MESSAGE = False # czy wiadomosc jest wyswietlana
        self._IS_MOUSE_SENSOR_BUTTON = False
        self._IS_MOUSE_TARGET_BUTTON = False
        self._grid_size = int(self._length / 10) # vertical

    def _init_colors(self):
        self._BACKGROUND = (200,200,200)
        self._FIGURE = (140,140,140)
        self._ON_RECT = (0, 130, 0)
        self._ON_TEXT = (0, 100, 0)
        self._OFF_RECT = (153,0,0)
        self._OFF_TEXT = (100, 0, 0)
        self._BORDER = (190,190,190)
        self._BUTTON = (100,100,100)
        self._GRID = (220,220,220)

    def _init_shapes(self):
        self._left_rect = shapes.Rect(self._FIGURE, (0, 0, self._length / 4, self._width), self._win)
        self._x, self._y = (self._length / 4) - 100, 10
        border_thick = 5
        length, width = 90, 50
        radius = 20
        self._onoff_button_border = shapes.Rect(self._BORDER, (self._x, self._y, length, width), self._win, border_thick, radius)
        self._onoff_button = shapes.Rect(self._OFF_RECT, (self._x + border_thick, self._y + border_thick, length - 2*border_thick, width - 2*border_thick), self._win, 0, radius-6)
        self._add_sensor_button = shapes.Rect(self._BUTTON, (self._y, self._y, length*2.5, width), self._win, 0, 15)
        self._add_target_button = shapes.Rect(self._BUTTON, (self._y, self._y + 10 + width, length*2.5, width), self._win, 0, 15)
    
    def _init_text(self):
        self._onoff_font = pygame.font.SysFont('Courier', 40, bold=True)
        self._onoff_text = self._onoff_font.render('OFF', True, self._OFF_TEXT)
        self._add_sensor_text = pygame.font.SysFont('Courier', 30, bold=True).render('ADD SENSOR', True, self._BORDER)
        self._add_target_text = pygame.font.SysFont('Courier', 30, bold=True).render('ADD TARGET', True, self._BORDER)
        self._not_available_text = pygame.font.SysFont('Courier', 20).render('Opcja nie jest dostepna w trakcie dzialania symulacji', True, (0,0,0))
        

    def _onoff_clicked(self):
        # jesli symulacja dziala
        if self._onoff_button.get_color() == self._ON_RECT:
            self._onoff_button.set_color(self._OFF_RECT)
            self._onoff_text = self._onoff_font.render('OFF', True, self._OFF_TEXT)
            self._IS_ON = False
        # jesli symulacja nie dziala
        else:
            self._onoff_button.set_color(self._ON_RECT)
            self._onoff_text = self._onoff_font.render('ON', True, self._ON_TEXT)
            self._IS_ON = True

    # obsluguje pojedynczy event
    def _handle_event(self, event):
        self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:           
            if event.button == 1 and self._onoff_button.get_rect().collidepoint(event.pos): self._onoff_clicked()

        elif event.type == pygame.MOUSEMOTION:

            if self._add_sensor_button.get_rect().collidepoint(event.pos):
                self._IS_MOUSE_SENSOR_BUTTON = True
                if self._IS_ON == True: self._IS_MESSAGE = True   
            elif self._add_target_button.get_rect().collidepoint(event.pos):
                self._IS_MOUSE_TARGET_BUTTON = True
                if self._IS_ON == True: self._IS_MESSAGE = True  
            else:
                 self._IS_MOUSE_SENSOR_BUTTON = False
                 self._IS_MOUSE_TARGET_BUTTON = False
                 self._IS_MESSAGE = False

    def _init_grid(self):
        self._grid_vlines = []
        self._grid_hlines = []

        for i in range(4):
            self._grid_vlines.append(shapes.Line(self._GRID, (self._interface_length, (i+1) * self._grid_size), (self._length, (i+1) * self._grid_size), 4, self._win))
        for i in range(6):
            self._grid_hlines.append(shapes.Line(self._GRID, (self._interface_length + (i+1) * (self._grid_size+12), 0), (self._interface_length + (i+1) * (self._grid_size+12), self._width), 4, self._win))


    # oprawa graficzna 
    def _layout(self):
        self._left_rect.draw()
        self._onoff_button_border.draw()
        self._onoff_button.draw()

        for i in range(4):
            self._grid_vlines[i].draw()
        for i in range(6):
            self._grid_hlines[i].draw()


        if self._IS_MOUSE_TARGET_BUTTON == True:
            self._add_target_button.draw()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        elif self._IS_MOUSE_SENSOR_BUTTON == True:
            self._add_sensor_button.draw()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self._onoff_button.get_rect().collidepoint(self._mouse_x, self._mouse_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        self._win.blit(self._add_sensor_text, (self._y + 20, self._y + 8))
        self._win.blit(self._add_target_text, (self._y + 20, self._y + 68))
        # wysw wiadomosc not available
        if self._IS_MESSAGE == True:
            self._win.blit(self._not_available_text, (self._mouse_x + 10, self._mouse_y + 10))

        # odpowiedni tekst i kolor onoff
        if self._IS_ON == True:
            self._win.blit(self._onoff_text, (self._x+20, self._y+2))
        else:
            self._win.blit(self._onoff_text, (self._x+10, self._y+2))

    # rysowanie obiektow, kolor tla itp
    def _render(self):
        self._win.fill(self._BACKGROUND)
        self._layout()

    # aktualizacja ekranu
    def _update(self):
        pygame.display.flip()