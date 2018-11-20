import pygame
from pygame.locals import *
import wave_ext
import soundFX
import wave
import sys

WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
fps_clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont("arial", 15)

# Colors
LIGHT_GRAY = (180, 180, 180)

MIN_NOTE_SIZE = 50                          # pixels
MIN_NOTE_LENGTH = 0.1                       # seconds
note_size = {"width": 50, "height": 25}     # pixels
audio_length = 5                            # seconds

INPUTS = {"LMB": False, "RMB": False}

# audio set up
BASE_FREQUENCIES = {}
BASE_FREQUENCIES["C"] = 16.35
BASE_FREQUENCIES["C#"] = 17.32
BASE_FREQUENCIES["D"] = 18.35
BASE_FREQUENCIES["D#"] = 19.45
BASE_FREQUENCIES["E"] = 20.6
BASE_FREQUENCIES["F"] = 21.83
BASE_FREQUENCIES["F#"] = 23.12
BASE_FREQUENCIES["G"] = 24.5
BASE_FREQUENCIES["G#"] = 25.96
BASE_FREQUENCIES["A"] = 27.5
BASE_FREQUENCIES["A#"] = 29.14
BASE_FREQUENCIES["B"] = 30.87

VOLUME = 1.0
MAX_DEPTH = 32767


def inputs():

    # Reset the mouse inputs as we only want a single click
    INPUTS["LMB"], INPUTS["RMB"] = False, False


    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN :
            if event.button == 1:
                INPUTS["LMB"] = True
            elif event.button == 3:
                INPUTS["RMB"] = True


def exit():
    pygame.quit()
    sys.exit()


def create_piano_role(length):

    surface_height = int(len(BASE_FREQUENCIES) * note_size["height"]) + 2
    print((length / MIN_NOTE_LENGTH))

    surface_width = int((length / MIN_NOTE_LENGTH) * note_size["width"]) + 2

    surface = pygame.Surface((surface_width, surface_height))

    # draw the grid to the surface
    for col in range(0, (surface_width + note_size["width"]), note_size["width"]):
        start_position = col, 0
        end_position = col, surface_height

        pygame.draw.line(surface, LIGHT_GRAY, start_position, end_position)

    for row in range(0, surface_height, note_size["height"]):
        start_position = 0, row
        end_position = surface_width, row

        pygame.draw.line(surface, LIGHT_GRAY, start_position, end_position)

    return surface

def get_piano_role_times(length):

    surface_width = int((length / MIN_NOTE_LENGTH) * note_size["width"])
    surface = pygame.Surface((surface_width, 20))

    for col in range(0, (surface_width + note_size["width"]), note_size["width"]):

        time_text = str({0:.2}).format(length * (col/(surface_width + note_size["width"])))

        text_surface = FONT.render(time_text, True, (255, 255, 255))

        surface.blit(text_surface, (col, 0) )

    return surface

def get_key_lables():

    surface_height = int(len(BASE_FREQUENCIES) * note_size["height"]) + 2
    surface_width = 50
    text_x_offset = 15
    surface = pygame.Surface((surface_width, surface_height))
    keys = list(BASE_FREQUENCIES)

    for key_index in range(len(keys)):

        text = keys[key_index]
        text_surface = FONT.render(text, True, (255, 255, 255))

        surface.blit(text_surface, (text_x_offset, key_index * note_size["height"]) )

    return surface

def get_piano_role_cords(mouse_position, piano_role_position, piano_role_offset):

    if mouse_position[0] < piano_role_position[0] or mouse_position[1] < (piano_role_position[1] + piano_role_offset[1]):
        return

    x_cord = int((mouse_position[0] + piano_role_offset[0] - piano_role_position[0]) / note_size["width"])
    y_cord = int((mouse_position[1] - piano_role_position[1] - piano_role_offset[1]) / note_size["height"])

    print(x_cord, y_cord)



def main():

    piano_role_surface = create_piano_role(audio_length)
    piano_role_times = get_piano_role_times(audio_length)
    piano_role_hold_surface = pygame.Surface((WINDOW_WIDTH-50, piano_role_surface.get_height() + piano_role_times.get_height()))
    piano_role_position = (50, 250)
    piano_role_offset = (0, piano_role_times.get_height())
    key_lable_surface = get_key_lables()

    while True:

        inputs()

        if INPUTS["LMB"]:
            get_piano_role_cords(pygame.mouse.get_pos(), piano_role_position, piano_role_offset)

        #text = "Tone: " + tone_type + " Key: " + frequency_name + str(frequency_key)
        text = "test"
        text_surface = pygame.Surface((1000, 150))
        text_surface.fill((25, 25, 25))
        text_surface = FONT.render(text, True, (255, 255, 255))

        pygame.draw.rect(screen, (25, 25, 25), (0, 150, WINDOW_WIDTH, 100), 0)

        screen.blit(text_surface, (0, 150))
        screen.blit(key_lable_surface, (0, piano_role_position[1] + piano_role_times.get_height() + 2))

        piano_role_hold_surface.blit(piano_role_times, (piano_role_offset[0], 0))
        piano_role_hold_surface.blit(piano_role_surface, piano_role_offset)
        screen.blit(piano_role_hold_surface, piano_role_position)

        pygame.display.flip()
        fps_clock.tick(FPS)

        delta_time = fps_clock.get_time() / 1000

if __name__ == "__main__":
    main()
