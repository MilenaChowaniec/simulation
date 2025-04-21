import shapes
import sys
import pygame
import math
import message as mess

# only printing, composition, only drawable

class Window:

    # konstruktor tworzy okno
    def __init__(self, length: int, width: int):
        """
        Inicjalizuje główne elementy aplikacji:
        - Ustawia okno gry.
        - Tworzy zmienne stanu i dane startowe.
        - Inicjalizuje kolory, kształty, teksty, siatkę i obrazy.
        """
        self._init_window(length, width)
        self._init_var()
        self._init_colors()
        self._init_shapes()
        self._init_text()
        self._init_grid()
        self._init_images()
        self._init_error_messages()
    

    def _init_error_messages(self):
        self._error_messages = {
            "sensor_close": mess.Message("Sensors are too close to each other.", self._ERROR),
            "target_close": mess.Message("Targets are too close to each other.", self._ERROR),
            "target_lines": mess.Message("The target must be inside the grid lines.", self._ERROR)
        }


    def _init_window(self, length: int, width: int):
        # Tworzy okno gry o zadanych wymiarach i ustawia tytuł
        self._win = pygame.display.set_mode((length, width))
        pygame.display.set_caption("simulation")
        self._length = length
        self._width = width
        self._interface_length = length // 4 # szerokość części interfejsowej (panel boczny)


    def _init_var(self):
        # Inicjalizacja zmiennych stanu symulacji i interfejsu
        self._IS_ON = False # czy symulacja jest wlaczona
        self._SENSOR_BUTTON_HOVERED = False
        self._TARGET_BUTTON_HOVERED = False
        self._SENSOR_BUTTON_CLICKED = False
        self._TARGET_BUTTON_CLICKED = False

        self._grid_size = int(self._length / 10) # rozmiar komórki siatki (pionowy)
        self._target_coords = list() # lista pozycji celów
        self._sensor_coords = list() # lista pozycji sensorów
        self._pic_size = 50 # rozmiar obrazków (px)
        self._circle_radius = 300


    def _init_colors(self):
        # Definicja kolorów używanych w interfejsie
        self._BACKGROUND = (200,200,200)
        self._FIGURE = (140,140,140)
        self._ON_RECT = (0, 130, 0)
        self._ON_TEXT = (0, 100, 0)
        self._OFF_RECT = (153,0,0)
        self._OFF_TEXT = (100, 0, 0)
        self._BORDER = (190,190,190)
        self._BUTTON = (100,100,100)
        self._GRID = (220,220,220)
        self._ERROR = (164, 33, 33)
        self._CIRCLE = (160,160,160)
        self._HINT = (79, 125, 72)


    def _init_shapes(self):
        # Tworzy kształty: panel boczny, przyciski oraz ich obramowania
        self._left_rect = shapes.Rect(self._FIGURE, (0, 0, self._length / 4, self._width), self._win)
        self._x, self._y = (self._length / 4) - 100, 10

        border_thick = 5
        length, width = 90, 50
        radius = 20

        # Przycisk ON/OFF z obramowaniem
        self._onoff_button_border = shapes.Rect(self._BORDER, (self._x, self._y, length, width), self._win, border_thick, radius)
        self._onoff_button = shapes.Rect(self._OFF_RECT, (self._x + border_thick, self._y + border_thick, length - 2*border_thick, width - 2*border_thick), self._win, 0, radius-6)

        # Przyciski dodawania sensorów i targetow
        self._add_sensor_button = shapes.Rect(self._BUTTON, (self._y, self._y, length*2.5, width), self._win, 0, 15)
        self._add_target_button = shapes.Rect(self._BUTTON, (self._y, self._y + 10 + width, length*2.5, width), self._win, 0, 15)
    

    def _init_text(self):
        # Inicjalizacja czcionek i tekstów przycisków
        self._onoff_text = pygame.font.SysFont('Courier', 40, bold=True).render('OFF', True, self._OFF_TEXT)

        self._add_sensor_text = pygame.font.SysFont('Courier', 30, bold=True).render('ADD SENSOR', True, self._BORDER)
        self._add_target_text = pygame.font.SysFont('Courier', 30, bold=True).render('ADD TARGET', True, self._BORDER)

        self._remove_target_text = pygame.font.SysFont('Arial', 18, bold=True).render('Right-click to remove the target from grid.', True, self._HINT)
        self._remove_sensor_text = pygame.font.SysFont('Arial', 18, bold=True).render('Right-click to remove the sensor from grid.', True, self._HINT)
        

    def _init_images(self):
        # Wczytuje i skaluje obrazki sensorów i targetow
        self._sensor_def_img = pygame.image.load('pics/sensor_def.png')
        self._sensor_def_img = pygame.transform.scale(self._sensor_def_img, (self._pic_size, self._pic_size))

        self._target_blue_img = pygame.image.load('pics/target_blue.png')
        self._target_blue_img = pygame.transform.scale(self._target_blue_img, (self._pic_size, self._pic_size))


    def _init_grid(self):
        """
        Tworzy linie siatki w części symulacyjnej okna:
        - 4 poziome linie
        - 6 pionowych linii
        """
        self._grid_pionlines = []
        self._grid_pozlines = []

        for i in range(4):
            self._grid_pozlines.append(shapes.Line(self._GRID, (self._interface_length, (i+1) * self._grid_size), (self._length, (i+1) * self._grid_size), 4, self._win))
        for i in range(6):
            self._grid_pionlines.append(shapes.Line(self._GRID, (self._interface_length + (i+1) * (self._grid_size+12), 0), (self._interface_length + (i+1) * (self._grid_size+12), self._width), 4, self._win))


    def _onoff_clicked(self):
        """
        Przełącza stan symulacji między ON a OFF:
        - Zmienia kolor przycisku i tekst.
        - Ustawia flagę `self._IS_ON`.
        """

        # Jeśli symulacja jest włączona – wyłącz ją
        if self._onoff_button.get_color() == self._ON_RECT:
            self._onoff_button.set_color(self._OFF_RECT)
            self._onoff_text = pygame.font.SysFont('Courier', 40, bold=True).render('OFF', True, self._OFF_TEXT)
            self._IS_ON = False
        # Jeśli symulacja jest wyłączona – włącz ją
        else:
            self._onoff_button.set_color(self._ON_RECT)
            self._onoff_text = pygame.font.SysFont('Courier', 40, bold=True).render('ON', True, self._ON_TEXT)
            self._IS_ON = True


    def _set_sensor(self):
        """
        Ustawia sensor na najbliższej linii siatki w zależności od pozycji myszy:
        - Sprawdza, czy kliknięcie jest poza interfejsem.
        - Sprawdza, czy w danym miejscu nie ma już sensora.
        - Znajduje najbliższą linię (poziomą lub pionową).
        - Ustawia sensor wzdłuż bliższej z nich.
        """
        # Jesli kliknieto w interfejsie bocznym — nic nie rob
        if self._mouse_x <= self._interface_length:
            return

        # Sprawdz, czy w tym miejscu nie ma juz sensora
        for coords in self._sensor_coords:
            dist = pygame.math.Vector2(coords[0] + 25, coords[1] + 25).distance_to(pygame.math.Vector2(self._mouse_x, self._mouse_y))
            if dist <= self._pic_size-1:
                self._error_messages["sensor_close"]._start_time()
                return
                 
        # Znajdz najblizsza pozioma linie siatki
        min_hor = 1000
        min_hor_line = None
        for line in self._grid_pozlines:
            if abs(self._mouse_y - line.get_y()) < min_hor:
                min_hor = abs(self._mouse_y - line.get_y())
                min_hor_line = line

        # Znajdz najblizsza pionowa linie siatki
        min_ver = 1000
        min_ver_line = None
        for line in self._grid_pionlines:
            if abs(self._mouse_x - line.get_x()) < min_ver:
                min_ver = abs(self._mouse_x - line.get_x())
                min_ver_line = line

        # Umiesc sensor wzdluz blizszej linii (poziomej lub pionowej)
        if min_hor <= min_ver:
            self._sensor_coords.append((self._mouse_x - 25, min_hor_line.get_y() - 25, shapes.Circle(self._win, self._CIRCLE, (self._mouse_x, min_hor_line.get_y()), self._circle_radius, 1)))
        else:
            self._sensor_coords.append((min_ver_line.get_x() - 25, self._mouse_y - 25, shapes.Circle(self._win, self._CIRCLE, (min_ver_line.get_x(), self._mouse_y), self._circle_radius, 1)))


    def _set_target(self):
        # Jesli kliknieto w interfejsie bocznym — nic nie rob
        if self._mouse_x <= self._interface_length:
            return
        
        can_place = True

        # Sprawdz, czy w tym miejscu nie ma juz targetu
        for coords in self._target_coords:
            dist = pygame.math.Vector2(coords[0] + 25, coords[1] + 25).distance_to(pygame.math.Vector2(self._mouse_x, self._mouse_y))
            if dist <= self._pic_size - 8:
                self._error_messages["target_close"]._start_time()
                can_place = False
                return
            
        for line in self._grid_pionlines:
            if pygame.Rect(self._mouse_x - 25, self._mouse_y - 25, self._pic_size, self._pic_size).colliderect(line.get_x(), line.get_y(), 4, self._length):
                self._error_messages["target_lines"]._start_time()
                can_place = False
                return
            
        for line in self._grid_pozlines:
            if pygame.Rect(self._mouse_x - 25, self._mouse_y - 25, self._pic_size, self._pic_size).colliderect(line.get_x(), line.get_y(), self._width, 4):
                self._error_messages["target_lines"]._start_time()
                can_place = False
                return

        if can_place:
            self._target_coords.append((self._mouse_x - 25, self._mouse_y - 25))
            print(len(self._target_coords))
        

    def _delete_sensor(self):
        """
        Usuwa sensor, jesli kliknieto na jego pozycje.
        - Sprawdza, czy pozycja myszy znajduje sie w obszarze ktoregos sensora.
        - Jeśli tak — usuwa go z listy sensorów.
        """
        for coords in self._sensor_coords:
            if pygame.Rect(coords[0], coords[1], self._pic_size, self._pic_size).collidepoint(self._mouse_x, self._mouse_y):
                self._sensor_coords.remove(coords)
                return


    def _delete_target(self):
        """
        Usuwa target, jesli kliknieto na jego pozycje.
        - Sprawdza, czy pozycja myszy znajduje sie w obszarze ktoregos targetu.
        - Jeśli tak — usuwa go z listy targetow.
        """
        for coords in self._target_coords:
            if pygame.Rect(coords[0], coords[1], self._pic_size, self._pic_size).collidepoint(self._mouse_x, self._mouse_y):
                self._target_coords.remove(coords)
                return


    def _handle_mouse_click(self, event):
        """
        Obsługuje kliknięcia myszy:
        - Przełącza stan przycisku ON/OFF.
        - Dodaje lub usuwa sensory i cele.
        - Wykonuje odpowiednie akcje na klikniętych obiektach.
        """
        if event.button == 1: # Sprawdza, czy naciśnięty został lewy przycisk myszy
            # Jeśli kliknięto przycisk ON/OFF
            if self._onoff_button.get_rect().collidepoint(event.pos): 
                self._onoff_clicked()

            # Jeśli kliknięto przycisk "Add Sensor"
            elif self._add_sensor_button.get_rect().collidepoint(event.pos): 
                # Jeśli sensor nie został jeszcze wybrany
                if self._SENSOR_BUTTON_CLICKED == False:
                    self._SENSOR_BUTTON_CLICKED = True # Wybierz sensor
                    self._TARGET_BUTTON_CLICKED = False # Anuluj wybór targetu
                else: 
                    self._SENSOR_BUTTON_CLICKED = False # Jeśli już wybrano sensor, odznacz go

            # Jeśli kliknięto przycisk "Add Target"
            elif self._add_target_button.get_rect().collidepoint(event.pos):
                # Jeśli cel nie został jeszcze wybrany
                if self._TARGET_BUTTON_CLICKED == False:
                    self._TARGET_BUTTON_CLICKED = True
                    self._SENSOR_BUTTON_CLICKED = False
                else: 
                    self._TARGET_BUTTON_CLICKED = False

            # Jeśli wybrano tryb dodawania targetu, wywołaj funkcję ustawiania celu
            elif self._TARGET_BUTTON_CLICKED == True:
                self._set_target()

            # Jeśli wybrano tryb dodawania sensora, wywołaj funkcję ustawiania sensora
            elif self._SENSOR_BUTTON_CLICKED == True:
                self._set_sensor()
        else: # Jeśli naciśnięto prawy przycisk myszy
            # Jeśli aktywny jest tryb usuwania sensora
            if self._SENSOR_BUTTON_CLICKED == True:
                self._delete_sensor() # Usuń sensor
            elif self._TARGET_BUTTON_CLICKED == True:
                self._delete_target() # Usun target


    def _handle_mouse_motion(self, event):
        """
        Obsługuje ruch myszy:
        - Ustala, czy kursor znajduje się nad przyciskami "Add Sensor" i "Add Target".
        - Jeśli kursor znajduje się nad jednym z przycisków i symulacja jest włączona, ustawia komunikat informujący użytkownika.
        """
        # Sprawdza, czy kursor znajduje się nad przyciskiem 'Add Sensor'
        if self._add_sensor_button.get_rect().collidepoint(event.pos):
            self._SENSOR_BUTTON_HOVERED = True 
        
        # Sprawdza, czy kursor znajduje się nad przyciskiem 'Add Target'
        elif self._add_target_button.get_rect().collidepoint(event.pos):
            self._TARGET_BUTTON_HOVERED = True

        # Jeśli kursor nie znajduje się nad żadnym z przycisków, ustawiamy obie zmienne na False
        else:
            self._SENSOR_BUTTON_HOVERED = False
            self._TARGET_BUTTON_HOVERED = False


    def _handle_event(self, event):
        """
        Obsługuje różne zdarzenia w aplikacji, takie jak:
        - Zamykanie aplikacji.
        - Kliknięcia myszy.
        - Ruchy myszy.
        """
        self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:           
            self._handle_mouse_click(event)               
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)


    def _draw_hovered_buttons(self):
        """
        Obsługuje interakcję kursora z interfejsem:
        - Rysuje odpowiedni przycisk, jeśli jest kliknięty lub najechany.
        - Zmienia kursor na 'rękę' lub przywraca strzałkę w zależności od kontekstu.
        """
        if (self._TARGET_BUTTON_HOVERED == True or self._TARGET_BUTTON_CLICKED == True) and self._SENSOR_BUTTON_CLICKED == False:
            self._add_target_button.draw()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self._SENSOR_BUTTON_HOVERED == True or self._SENSOR_BUTTON_CLICKED == True:
            self._add_sensor_button.draw()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self._onoff_button.get_rect().collidepoint(self._mouse_x, self._mouse_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif not self._TARGET_BUTTON_CLICKED and not self._SENSOR_BUTTON_CLICKED:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    def _print_background(self):
        """
        Rysuje elementy tła interfejsu:
        - Panel boczny
        - Przycisk ON/OFF wraz z ramką
        """
        self._left_rect.draw() # rysuj panel po lewej stronie
        self._onoff_button_border.draw() # rysuj ramkę przycisku ON/OFF
        self._onoff_button.draw() # rysuj sam przycisk ON/OFF


    def _render_tool_preview(self):
        """
        Wyświetla podgląd aktualnie wybranego narzędzia (sensor/target):
        - Wyświetla obrazek narzędzia pod kursorem
        - Ustawia kursor myszy na "rękę"
        """
        # Jeśli aktywny jest tryb dodawania sensora
        if self._SENSOR_BUTTON_CLICKED == True:
            self._win.blit(self._sensor_def_img, (self._mouse_x - 25, self._mouse_y - 25))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Jeśli aktywny jest tryb dodawania targetu
        elif self._TARGET_BUTTON_CLICKED == True:
            self._win.blit(self._target_blue_img, (self._mouse_x - 25, self._mouse_y - 25))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


    def _print_text(self):
        """
        Rysuje teksty dla przycisków 'ADD SENSOR' i 'ADD TARGET' oraz stan przycisku ON/OFF na ekranie:
        - 'ADD SENSOR' i 'ADD TARGET' są wyświetlane na górze interfejsu.
        - Tekst stanu ON/OFF wyświetlany obok przycisku ON/OFF w zależności od stanu.
        """
        self._win.blit(self._add_sensor_text, (self._y + 20, self._y + 8))
        self._win.blit(self._add_target_text, (self._y + 20, self._y + 68))
        if self._IS_ON == True:
            self._win.blit(self._onoff_text, (self._x+20, self._y+2))
        else:
            self._win.blit(self._onoff_text, (self._x+10, self._y+2))
        
        if self._SENSOR_BUTTON_CLICKED == True:
            self._win.blit(self._remove_sensor_text, (self._y + 6, self._y + 120))
        if self._TARGET_BUTTON_CLICKED == True:
            self._win.blit(self._remove_target_text, (self._y + 6, self._y + 120))


    def _print_target_sensor_on_grid(self):
        """
        Funkcja odpowiedzialna za rysowanie obrazków (sensorów i celów) na ekranie.
        
        - Pierwsza pętla przechodzi przez wszystkie współrzędne sensorów i rysuje je na ekranie.
        - Druga pętla przechodzi przez wszystkie współrzędne celów i rysuje je na ekranie.
        """
        # target i sensors to musi byc obiekt z ustalona grafika i coords
        for i in range(len(self._sensor_coords)):
            self._win.blit(self._sensor_def_img, (self._sensor_coords[i][0], self._sensor_coords[i][1]))  
            self._sensor_coords[i][2].draw()

        for i in range(len(self._target_coords)):
            self._win.blit(self._target_blue_img, (self._target_coords[i][0], self._target_coords[i][1]))  


    def _print_error_messages(self):
        if self._error_messages["sensor_close"]._get_start_time() is not None and pygame.time.get_ticks() - self._error_messages["sensor_close"]._get_start_time() <= 4000:
            self._error_messages["sensor_close"]._print_text((10, self._width - 40 - (pygame.time.get_ticks() - self._error_messages["sensor_close"]._get_start_time())/20), self._win)
            self._error_messages["sensor_close"]._update_set_alpha()

        if self._error_messages["target_close"]._get_start_time() is not None and pygame.time.get_ticks() - self._error_messages["target_close"]._get_start_time() <= 4000:
            self._error_messages["target_close"]._print_text((10, self._width - 40 - (pygame.time.get_ticks() - self._error_messages["target_close"]._get_start_time())/20), self._win)
            self._error_messages["target_close"]._update_set_alpha()

        if self._error_messages["target_lines"]._get_start_time() is not None and pygame.time.get_ticks() - self._error_messages["target_lines"]._get_start_time() <= 4000:
            self._error_messages["target_lines"]._print_text((10, self._width - 40 - (pygame.time.get_ticks() - self._error_messages["target_lines"]._get_start_time())/20), self._win)
            self._error_messages["target_lines"]._update_set_alpha()


    def _print_grid(self):
        for i in range(4):
            self._grid_pozlines[i].draw()
        for i in range(6):
            self._grid_pionlines[i].draw()       


    def _layout(self):

        self._print_grid()
        self._print_target_sensor_on_grid()
        self._print_background()
        self._draw_hovered_buttons()
        self._print_text()
        self._render_tool_preview()
        self._print_error_messages()

           
    def _render(self):
        """
        Wypełnia ekran tłem i rysuje wszystkie elementy na ekranie.
        """
        self._win.fill(self._BACKGROUND)
        self._layout()

  
    def _update(self):
        """
        Aktualizuje wyświetlanie na ekranie.
        """
        pygame.display.flip()