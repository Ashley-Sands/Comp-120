import pygame
from pygame.locals import *
import wave_ext
import soundFX
import waves
import sys
import menuUi
from audioFiles import audio_track_0 as timeline_0
from audioFiles import audio_track_1 as timeline_1

WINDOW_HEIGHT = 250
WINDOW_WIDTH = 1334

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
fps_clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont("arial", 15)

# Colors
LIGHT_GRAY = (180, 180, 180)

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

timelines = [timeline_0, timeline_1]
timeline_file_names = [None, None]  # Gets added once generated
timeline = timeline_0.timeline
current_timeline_id = 0

effect = soundFX.SoundFxLibrary()

# build audio
wave_lib = waves.WaveLibrary(SAMPLE_RATE, MAX_DEPTH)

menu = menuUi.UiMenu()

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

        print("generating timeline", i)
        tone = wave_lib.get_sound(timeline[i]["wave_shape"], BASE_FREQUENCIES[timeline[i]["base_freq"]], timeline[i]["key"], timeline[i]["harmonic_steps"], timeline[i]["length"], timeline[i]["envelope"])
        tone.normalize(MAX_DEPTH * (0.9 * timeline[i]["velocity"]))

        # set if the timeline element has any effect to be applied
        if "echo" in timeline[i]:
            tone = effect.echo(tone, timeline[i]["echo"][0], timeline[i]["echo"][1], timeline[i]["echo"][2], timeline[i]["echo"][3])
        audio = combine_audio(audio, tone.sample_data, timeline[i]["start_sample"], combine_mode=timeline[i]["combine"])

    print("normalizing")
    audio.normalize(MAX_DEPTH * 0.9)

    file_path = "audio/"+timelines[current_timeline_id].TRACK_NAME
    audio.write_sample_data(file_path, sample_rate=SAMPLE_RATE)
    timeline_file_names[current_timeline_id] = file_path


    print("generating wave image")
    draw_wave_to_screen(1334, 150, audio.sample_data, MAX_DEPTH)

    print("Render Complete!")


def combine_audio(audio_stream, samples_to_combine, start_position, volume=1, combine_mode=wave_ext.ReadWriteWav.COMBINE_ADD):

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
                audio_stream.add_sample(samples_to_combine[i - start_position] * (volume*combine_mode))
        else:
            audio_stream.combine_samples(i, samples_to_combine[i - start_position] * volume, combine_mode)

    return audio_stream

def draw_wave_to_screen(width, height, audio_wave, max_vol):

    surface = pygame.Surface((width, height))
    total_samples = len(audio_wave)
    samples_to_pixels = total_samples // width

    if samples_to_pixels < 1:
        samples_to_pixels = 1

    pixel_array = pygame.PixelArray(surface)

    x = 0

    for samp_numb in range(0, total_samples, samples_to_pixels):

        samp_value = audio_wave[samp_numb] + max_vol
        precent = samp_value / (max_vol*2)

        y = int( (1 - precent) * height)

        pixel_color = (255 * precent, 0, 255 * (1-precent))

        pixel_array[x, height // 2] = (100, 100, 100)
        pygame.draw.line(surface, pixel_color, (x, height // 2), (x, y))

        x += 1
        if x > width-1:
            break

    del pixel_array

    screen.blit(surface, (0, 0))
    pygame.display.flip()



def change_timeline(timeline_id):

    global timeline, current_timeline_id

    current_timeline_id = timeline_id
    timeline = timelines[timeline_id].timeline
    render()


def set_timeline_0():
    change_timeline(0)

def set_timeline_1():
    change_timeline(1)

def play_audio():
    if timeline_file_names[current_timeline_id] is None:
        return
    pygame.mixer.Sound(timeline_file_names[current_timeline_id]+".wav").play()

def setup_menu():
    menu.add_button_type("normal", None, None, None, (150, 50))
    menu.add_menu("Audio")
    menu.current_menu = "Audio"
    menu.add_button("Audio", "normal", "Audio 1", (435, 200), set_timeline_0)
    menu.add_button("Audio", "normal", "Audio 2", (590, 200), set_timeline_1)
    menu.add_button("Audio", "normal", "Audio 3", (745, 200), set_timeline_1)
    menu.add_button("Audio", "normal", "Play", (1000, 170), play_audio)

def main():

    setup_menu()


    while True:

        inputs()

        text = "test"
        text_surface = pygame.Surface((1000, 150))
        text_surface.fill((25, 25, 25))
        text_surface = FONT.render(text, True, (255, 255, 255))

        pygame.draw.rect(screen, (25, 25, 25), (0, 150, WINDOW_WIDTH, 100), 0)

        screen.blit(text_surface, (0, 150))

        menu.draw_buttons(screen, pygame.mouse.get_pos(), INPUTS["LMB"])
        menu.is_button_pressed(pygame.mouse.get_pos(), INPUTS["LMB"])

        pygame.display.flip()
        fps_clock.tick(FPS)

        delta_time = fps_clock.get_time() / 1000

if __name__ == "__main__":
    effect.combine_audio_funct = combine_audio
    main()
