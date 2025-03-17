import shapes
import sys
import pygame

class Window:
    # konstruktor tworzy okno
    def __init__(self, length: int, width: int):
        self.__init_window(length, width)
        self.__init_var()
        self.__init_colors()
        self.__init_shapes()
        self.__init_text()
        self.__init_grid()
    
    def __init_window(self, length: int, width: int):
        self.__win = pygame.display.set_mode((length, width))
        pygame.display.set_caption("simulation")
        self.__length = length
        self.__width = width
        self.__interface_length = length / 4
    
    def __init_var(self):
        self.__IS_ON = False # czy symulacja jest wlaczona
        self.__IS_MESSAGE = False # czy wiadomosc jest wyswietlana
        self.__IS_MOUSE_SENSOR_BUTTON = False
        self.__IS_MOUSE_TARGET_BUTTON = False
        self.__grid_size = int(self.__length / 10) # vertical

    def __init_colors(self):
        self.__BACKGROUND = (200,200,200)
        self.__FIGURE = (140,140,140)
        self.__ON_RECT = (0, 130, 0)
        self.__ON_TEXT = (0, 100, 0)
        self.__OFF_RECT = (153,0,0)
        self.__OFF_TEXT = (100, 0, 0)
        self.__BORDER = (190,190,190)
        self.__BUTTON = (100,100,100)
        self.__GRID = (220,220,220)

    def __init_shapes(self):
        self.__left_rect = shapes.Rect(self.__FIGURE, (0, 0, self.__length / 4, self.__width), self.__win)
        self.__x, self.__y = (self.__length / 4) - 100, 10
        border_thick = 5
        length, width = 90, 50
        radius = 20
        self.__onoff_button_border = shapes.Rect(self.__BORDER, (self.__x, self.__y, length, width), self.__win, border_thick, radius)
        self.__onoff_button = shapes.Rect(self.__OFF_RECT, (self.__x + border_thick, self.__y + border_thick, length - 2*border_thick, width - 2*border_thick), self.__win, 0, radius-6)
        self.__add_sensor_button = shapes.Rect(self.__BUTTON, (self.__y, self.__y, length*2.5, width), self.__win, 0, 15)
        self.__add_target_button = shapes.Rect(self.__BUTTON, (self.__y, self.__y + 10 + width, length*2.5, width), self.__win, 0, 15)
    
    def __init_text(self):
        self.__onoff_font = pygame.font.SysFont('Courier', 40, bold=True)
        self.__onoff_text = self.__onoff_font.render('OFF', True, self.__OFF_TEXT)
        self.__add_sensor_text = pygame.font.SysFont('Courier', 30, bold=True).render('ADD SENSOR', True, self.__BORDER)
        self.__add_target_text = pygame.font.SysFont('Courier', 30, bold=True).render('ADD TARGET', True, self.__BORDER)
        self.__not_available_text = pygame.font.SysFont('Courier', 20).render('Opcja nie jest dostepna w trakcie dzialania symulacji', True, (0,0,0))
        

    def __onoff_clicked(self):
        # jesli symulacja dziala
        if self.__onoff_button.get_color() == self.__ON_RECT:
            self.__onoff_button.set_color(self.__OFF_RECT)
            self.__onoff_text = self.__onoff_font.render('OFF', True, self.__OFF_TEXT)
            self.__IS_ON = False
        # jesli symulacja nie dziala
        else:
            self.__onoff_button.set_color(self.__ON_RECT)
            self.__onoff_text = self.__onoff_font.render('ON', True, self.__ON_TEXT)
            self.__IS_ON = True

    # obsluguje pojedynczy event
    def _handle_event(self, event):
        self.__mouse_x, self.__mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:           
            if event.button == 1 and self.__onoff_button.get_rect().collidepoint(event.pos): self.__onoff_clicked()

        elif event.type == pygame.MOUSEMOTION:

            if self.__add_sensor_button.get_rect().collidepoint(event.pos):
                self.__IS_MOUSE_SENSOR_BUTTON = True
                if self.__IS_ON == True: self.__IS_MESSAGE = True   
            elif self.__add_target_button.get_rect().collidepoint(event.pos):
                self.__IS_MOUSE_TARGET_BUTTON = True
                if self.__IS_ON == True: self.__IS_MESSAGE = True  
            else:
                 self.__IS_MOUSE_SENSOR_BUTTON = False
                 self.__IS_MOUSE_TARGET_BUTTON = False
                 self.__IS_MESSAGE = False

    def __init_grid(self):
        self.__grid_vlines = []
        self.__grid_hlines = []

        for i in range(4):
            self.__grid_vlines.append(shapes.Line(self.__GRID, (self.__interface_length, (i+1) * self.__grid_size), (self.__length, (i+1) * self.__grid_size), 4, self.__win))
        for i in range(6):
            self.__grid_hlines.append(shapes.Line(self.__GRID, (self.__interface_length + (i+1) * (self.__grid_size+12), 0), (self.__interface_length + (i+1) * (self.__grid_size+12), self.__width), 4, self.__win))


    # oprawa graficzna 
    def __layout(self):
        self.__left_rect.draw()
        self.__onoff_button_border.draw()
        self.__onoff_button.draw()

        for i in range(4):
            self.__grid_vlines[i].draw()
        for i in range(6):
            self.__grid_hlines[i].draw()


        if self.__IS_MOUSE_TARGET_BUTTON == True:
            self.__add_target_button.draw()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        elif self.__IS_MOUSE_SENSOR_BUTTON == True:
            self.__add_sensor_button.draw()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.__onoff_button.get_rect().collidepoint(self.__mouse_x, self.__mouse_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        self.__win.blit(self.__add_sensor_text, (self.__y + 20, self.__y + 8))
        self.__win.blit(self.__add_target_text, (self.__y + 20, self.__y + 68))
        # wysw wiadomosc not available
        if self.__IS_MESSAGE == True:
            self.__win.blit(self.__not_available_text, (self.__mouse_x + 10, self.__mouse_y + 10))

        # odpowiedni tekst i kolor onoff
        if self.__IS_ON == True:
            self.__win.blit(self.__onoff_text, (self.__x+20, self.__y+2))
        else:
            self.__win.blit(self.__onoff_text, (self.__x+10, self.__y+2))

    # rysowanie obiektow, kolor tla itp
    def _render(self):
        self.__win.fill(self.__BACKGROUND)
        self.__layout()

    # aktualizacja ekranu
    def _update(self):
        pygame.display.flip()