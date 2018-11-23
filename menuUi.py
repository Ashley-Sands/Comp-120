import pygame
import UI


class UiMenu:
    """ Creat a set of menus controlled by a state
    Drive: Ashley.
    """

    active = False      # needed??
    current_menu = None
    # default fontfaces. use set_font_face to change.
    header_fontface = None
    button_fontface = None
    menus = {}
    buttons = {}

    HEADER_Y_POSITION = 150
    HEADER_SIZE = (200, 50)

    def __init__(self):
        self.header_fontface = pygame.font.SysFont("arial", 50)
        self.button_fontface = pygame.font.SysFont("arial", 30)
        self.menus = {}
        self.buttons = {}

    def set_font_face(self, header_fontface, button_fontface):
        """ set the fontface, params are ignored if None """

        if header_fontface is not None:
            self.header_fontface = header_fontface

        if button_fontface is not None:
            self.button_fontface = button_fontface

    def add_button_type(self, type_name,  normal, hover, pressed, size):
        """Add a new button type.

        :param type_name:       the button type/group name
        :param normal:          src to normal button image  (can be none)
        :param hover:           src to hover button image   (can be none)
        :param pressed:         src to pressed button image (can be none)
        :param size:            button size (width, height)
        :return:                None
        """
        self.buttons[type_name] = UI.UIButtons(hover, normal, pressed, size)

    def add_menu(self, menu_title):
        """ Add a new menu to list of menus """
        self.menus[menu_title] = []

    def add_button(self, menu_title, button_type,
                   button_label, position_rect, action_funct):
        """
        Add a button to a menu group
        :param menu_title:      name of the group to add a button to
        :param button_type:     name of the button type to use
        :param button_label:    the label to display on the button.
        :param position_rect:   position and size rect -> (x, y)
        :param action_funct:    the function with the button action
        :return:                None
        """
        self.menus[menu_title].append(
            [button_type, button_label, position_rect, action_funct]
        )

    def set_current_menu(self, menu_name):
        """set the menu to be displayed"""
        self.current_menu = menu_name

    def center_surface(self, hold_surface_size, inner_surface_size):
        """get the position to center the inner surface inside the hold surface.

        :param hold_surface_size: Size of the surface holding the inner surface
        :param inner_surface_size: size of the inner surface
        :return: x, y offset to center center inner surface
        """

        offset_x = (hold_surface_size[0] - inner_surface_size[0]) // 2
        offset_y = (hold_surface_size[1] - inner_surface_size[1]) // 2

        return offset_x, offset_y

    def get_button(self, button, label, fontface, font_color=(0, 0, 0)):
        """get the button to be displayed with a label prefixed """

        temp_surface = button.copy()
        text_surface = fontface.render(label, True, font_color)

        # draw the text to the center of the button.
        offset_x, offset_y = self.center_surface(
            temp_surface.get_size(), text_surface.get_size()
        )
        temp_surface.blit(text_surface, (offset_x, offset_y))

        return temp_surface

    def get_header(self, label, fontface, label_size,
                   font_color=(0, 0, 0, 255),
                   background_color=(255, 255, 255, 255)
                   ):
        """gets the menu header"""

        temp_surface = pygame.Surface(label_size)
        temp_surface.fill(background_color)
        text_surface = fontface.render(label, True, font_color)

        # draw the text to the center of the header label.
        offset_x, offset_y = self.center_surface(temp_surface.get_size(),
                                                 text_surface.get_size())
        temp_surface.blit(text_surface, (offset_x, offset_y))

        return temp_surface

    def draw_buttons(self, surface, mouse_pos, key_pressed):
        """Draws all the buttons and menu header to the surface"""
        # note to self: button_type, button_label, position_rect, action_funct

        # display the header in the hoz center of the screen
        header_surface = self.get_header(self.current_menu,
                                         self.header_fontface,
                                         self.HEADER_SIZE)
        offset_x, offset_y = self.center_surface(surface.get_size(),
                                                 header_surface.get_size())

        surface.blit(header_surface, (offset_x, self.HEADER_Y_POSITION))

        # display all the buttons for the current menu.
        for button in self.menus[self.current_menu]:
            surface.blit(
                self.get_button(
                    self.buttons[button[0]].draw_button(
                        mouse_pos, key_pressed, button[2]),
                    button[1], self.button_fontface),
                button[2]
            )

    def is_button_pressed(self, mouse_position, mouse_is_pressed):
        """find if any of the buttons on the current menu are being pressed"""

        # See if any of the buttons are being pressed on the current menu.
        for button in self.menus[self.current_menu]:
            if self.buttons[button[0]].is_pressed(mouse_position,
                                                  button[2], mouse_is_pressed
                                                  ):
                button[3]()
