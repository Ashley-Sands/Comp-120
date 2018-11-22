import pygame
from pygame.locals import *
import wave_ext
import soundFX
import waves
import sys
from audio_track_1 import timeline

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

SAMPLE_RATE = 44100

# Synths
# list of dicts
# todo add env
synth = {}
synth["sine"] = { "Key": 3, "harmonic_steps": 1}
synth["saw"] = { "Key": 3, "harmonic_steps": 1}
synth["triangle"] = { "Key": 3, "harmonic_steps": 1}

effect = soundFX.SoundFxLibrary()

# build audio
wave_lib = waves.WaveLibrary(SAMPLE_RATE, MAX_DEPTH)

def inputs():

    # Reset the mouse inputs as we only want a single click
    INPUTS["LMB"], INPUTS["RMB"] = False, False


    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                INPUTS["LMB"] = True
            elif event.button == 3:
                INPUTS["RMB"] = True
        elif event.type == KEYDOWN:
            if event.key == K_r:
                render()


def exit():
    pygame.quit()
    sys.exit()


def render():

    print("Rendering...")

    audio = wave_ext.ReadWriteWav()

    for i in range(len(timeline)):
        tone = wave_lib.get_sound(timeline[i]["wave_shape"], BASE_FREQUENCIES[timeline[i]["base_freq"]], timeline[i]["key"], timeline[i]["harmonic_steps"], timeline[i]["length"], timeline[i]["envelope"])
        tone.normalize(MAX_DEPTH * (0.9 * timeline[i]["velocity"]))

        # set if the timeline element has any effect to be applied
        if "echo" in timeline[i]:
            tone = effect.echo(tone, timeline[i]["echo"][0], timeline[i]["echo"][1], timeline[i]["echo"][2], timeline[i]["echo"][3])

        audio = combine_audio(audio, tone.sample_data, timeline[i]["start_sample"])

    audio.normalize(MAX_DEPTH * 0.9)
    audio.write_sample_data("audio/main_1", sample_rate=SAMPLE_RATE)

    print("Render Complete!")


def combine_audio(audio_stream, samples_to_combine, start_position, volume=1):

    start_position = int(start_position)

    if len(audio_stream.sample_data) < start_position:
        start_index = len(audio_stream.sample_data)
    else:
        start_index = start_position

    for i in range(start_index, start_position + len(samples_to_combine)):
        if i >= len(audio_stream.sample_data)-1:
            if i < start_position:
                audio_stream.add_sample(0)
            else:
                audio_stream.add_sample(samples_to_combine[i - start_position] * volume)
        else:
            audio_stream.combine_samples(i, samples_to_combine[i - start_position] * volume)

    return audio_stream


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

def get_piano_role_cords(mouse_position, piano_role_position, piano_role_offset, piano_role_size):


    piano_x_pos = int(piano_role_offset[0] + piano_role_position[0])
    piano_y_pos = int(piano_role_position[1] + piano_role_offset[1])

    if mouse_position[0] < piano_x_pos or mouse_position[1] < piano_y_pos \
            or mouse_position[0] > (piano_x_pos + piano_role_size[0]) or mouse_position[1] > (piano_y_pos + piano_role_size[1] - piano_role_offset[1]):
        return

    x_cord = int((mouse_position[0] + piano_role_offset[0] - piano_role_position[0]) / note_size["width"])
    y_cord = int((mouse_position[1] - piano_role_position[1] - piano_role_offset[1]) / note_size["height"])

    return x_cord, y_cord



def main():

    #piano role
    piano_role_surface = create_piano_role(audio_length)
    piano_role_times = get_piano_role_times(audio_length)
    piano_role_hold_surface = pygame.Surface((WINDOW_WIDTH-50, piano_role_surface.get_height() + piano_role_times.get_height()))
    piano_role_position = (50, 250)
    piano_role_offset = (0, piano_role_times.get_height())
    key_lable_surface = get_key_lables()

    # synths
    current_synth = "sine"

    while True:

        inputs()

        if INPUTS["LMB"]:
            get_piano_role_cords( pygame.mouse.get_pos(), piano_role_position, piano_role_offset, piano_role_hold_surface.get_size() )

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
    effect.combine_audio_funct = combine_audio
    main()
