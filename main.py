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

FONT = pygame.font.SysFont("arial", 35)

# Colors
LIGHT_GRAY = (180, 180, 180)

MIN_NOTE_SIZE = 50                          # pixels
MIN_NOTE_LENGTH = 0.1                       # seconds
note_size = {"width": 50, "height": 25}     # pixels
audio_length = 1                            # seconds

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
    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def exit():
    pygame.quit()
    sys.exit()


def create_piano_role(length):

    surface_height = int(len(BASE_FREQUENCIES) * note_size["height"])
    note_width_muti = note_size["width"] / MIN_NOTE_SIZE
    print(note_width_muti)
    surface_width = int((length / (MIN_NOTE_LENGTH * note_width_muti)) * note_size["width"])

    surface = pygame.Surface((surface_width, surface_height))

    # draw the grid to the surface
    for col in range(0, surface_width, note_size["width"]):
        start_position = col, 0
        end_position = col, surface_height

        pygame.draw.line(surface, LIGHT_GRAY, start_position, end_position)

    for row in range(0, surface_width, note_size["height"]):
        start_position = 0, row
        end_position = surface_width, row

        pygame.draw.line(surface, LIGHT_GRAY, start_position, end_position)

    return surface


def main():

    piano_role_surface = create_piano_role(audio_length)

    while True:

        inputs()

        #text = "Tone: " + tone_type + " Key: " + frequency_name + str(frequency_key)
        text = "test"
        text_surface = pygame.Surface((1000, 150))
        text_surface.fill((25, 25, 25))
        text_surface = FONT.render(text, True, (255, 255, 255))

        pygame.draw.rect(screen, (25, 25, 25), (0, 150, 1000, 100), 0)
        screen.blit(text_surface, (0, 150))
        screen.blit(piano_role_surface, (150, 250))
        pygame.display.flip()
        fps_clock.tick(FPS)

        delta_time = fps_clock.get_time() / 1000

if __name__ == "__main__":
    main()
