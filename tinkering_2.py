import pygame
from pygame.locals import *
import sys
import math
import wave_ext

# Base Laser
#((8 * get_sin_wave_tone(current_sample, sample_rate, frequency)) / math.pi) * math.asin(math.sin((8*math.pi*sample_rate)/current_sample))

pygame.init()
screen = pygame.display.set_mode((1000, 250))
fps_clock = pygame.time.Clock()
FPS = 60

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


def average_samples(samples):
    """
    averages a list of samples
    :param samples:      list or tuple of samples
    :return:            mono tone
    """

    sum_of_samples = 0

    for samp in samples:
        sum_of_samples += samp

    return sum_of_samples / len(samples)


def add_samples(samples):
    """
    averages a list of samples
    :param samples:      list or tuple of samples
    :return:            mono tone
    """

    sum_of_samples = 0

    for samp in samples:
        sum_of_samples += samp

    return sum_of_samples


def sound_to_mono():

    edit_file = wave_ext.ReadWriteWav(read_filename="audio/a")
    save_file = wave_ext.ReadWriteWav()

    for samp in range(0, len(edit_file.sample_data), 2):

        channel_samples = []
        for chan in range(2):
            channel_samples.append(edit_file.get_sample_at_position(samp+chan))

        # make mono
        save_file.add_sample(average_samples(channel_samples))

    save_file.write_sample_data("audio/a_mono_2")

    sound = pygame.mixer.Sound("audio/a_mono_2.wav")
    sound.play()


def get_sin_wave_tone(current_sample, sample_rate, frequency):

    return math.sin(2.0 * math.pi * frequency * (current_sample / float(sample_rate))) * (MAX_DEPTH * VOLUME)


def get_triangle_wave_tone(current_sample, sample_rate, frequency):

    current_sample += 1
    return (2.0*MAX_DEPTH/math.pi) * math.asin((math.sin(2.0*math.pi*current_sample/(sample_rate/frequency)))) * (MAX_DEPTH)


def get_saw_wave_tone(current_sample, sample_rate, frequency):

    current_sample += 1
    tan = math.tan(current_sample*math.pi/(sample_rate/frequency))
    return -(2.0*MAX_DEPTH/math.pi) * math.atan(1.0/tan) * (MAX_DEPTH)


def triangle_tone(freq_1_name, freq_1_key, sample_rate, length):

    sound = wave_ext.ReadWriteWav()

    for i in range(int(sample_rate * length)):
        sound.add_sample(get_triangle_wave_tone(i, sample_rate, get_tone_by_key(freq_1_key, freq_1_name)))

    sound.normalize((MAX_DEPTH * 0.9))
    # sound.write_sample_data("audio/two_tones__", channels=1, sample_rate=sample_rate)

    return sound


def saw_tone(freq_1_name, freq_1_key, sample_rate, length):

    sound = wave_ext.ReadWriteWav()

    for i in range(int(sample_rate * length)):
        sound.add_sample(get_saw_wave_tone(i, sample_rate, get_tone_by_key(freq_1_key, freq_1_name)))

    sound.normalize((MAX_DEPTH * 0.9))
    # sound.write_sample_data("audio/two_tones__", channels=1, sample_rate=sample_rate)

    return sound


def dual_tone(freq_1_name, freq_1_key, freq_2_name, freq_2_key, sample_rate, length):

    sound = wave_ext.ReadWriteWav()

    for i in range(int(sample_rate * length)):
        sound.add_sample(get_triangle_wave_tone(i, sample_rate, get_tone_by_key(freq_1_key, freq_1_name)))
        sound.combine_samples(i, get_saw_wave_tone(i, sample_rate, get_tone_by_key(freq_2_key, freq_2_name)))

    sound.normalize((MAX_DEPTH * 0.9))
    #sound.write_sample_data("audio/two_tones__", channels=1, sample_rate=sample_rate)

    return sound


def echo():

    edit_file = wave_ext.ReadWriteWav(read_filename="audio/a")
    echo_samp = edit_file.get_sample_range(0, 5000)
    echo_index = 0

    for i in range(0, len(edit_file.sample_data)):
        echo_samp[echo_index] = echo_samp[echo_index] * 0.5
        edit_file.set_sample(i, add_samples([edit_file.sample_data[i], echo_samp[echo_index]]))
        echo_index += 1
        if echo_index == len(echo_samp):
            echo_index = 0

    edit_file.write_sample_data("audio/a_echo", 2)



def get_tone_by_key(key, tone_key):

    base_tone = BASE_FREQUENCIES[tone_key]

    for i in range(key):
        base_tone *= 2

    return base_tone

def generate_tone(tone, freq_name, freq_key, sample_rate=44100, length=1):

    if tone == "dual":
        return dual_tone(freq_name, freq_key, freq_name, freq_key + 3, sample_rate, length)
    elif tone == "saw":
        return saw_tone(freq_name, freq_key, sample_rate, length)
    elif tone == "triangle":
        return triangle_tone(freq_name, freq_key, sample_rate, length)

        print("tone tone found")

    empty_wav = wave_ext.ReadWriteWav()
    empty_wav.sample_data = [0]

    return empty_wav

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
        # pixel_array[x, y] = pixel_color

        x += 1
        if x > width-1:
            break

    del pixel_array

    screen.blit(surface, (0, 0))
    pygame.display.flip()


preview_start = 0
preview_display = 1000
preview_end = preview_start + preview_display
preview_max = 1
previewSamples = wave_ext.ReadWriteWav()
previewSamples.sample_data = [0]

prv_time = 0
prv_pass = 0;
delta_time = 0

tone_type = "dual"
frequency_name = "C"
frequency_key = 5

audio_stream = b''
sound = pygame.mixer.Sound(audio_stream)
sound.play(loops=100)

update_audio_stream = False
key_down = False

fontface = pygame.font.SysFont("arial", 35)

key_sounds = {}
key_audio_stream = {}


def setup_key_streams():

    keys = list(BASE_FREQUENCIES)

    for key in keys:
        key_audio_stream[key] = b''
        key_sounds[key] = {"audio": pygame.mixer.Sound(key_audio_stream[key]), "isPlaying": False, "freqKey":-999}

def play_key_press(freq_name, freq_key, tone_type):
    pass
    #if key_sounds[frequency_name]["freqKey"] != freq_key:
    #    key_sounds =

while True:

    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # change the key pressed state
        elif event.type == KEYDOWN:

            if event.key == K_1:
                tone_type = "dual"
            elif event.key == K_2:
                tone_type = "saw"
            elif event.key == K_3:
                tone_type = "triangle"

            if event.key == K_EQUALS:
                frequency_key += 1
                if key_down:
                    update_audio_stream = True
            elif event.key == K_MINUS:
                frequency_key -= 1
                if key_down:
                    update_audio_stream = True

            if event.key == K_f:
                frequency_name = "C"
            if event.key == K_r:
                frequency_name = "C#"

            if event.key == K_g:
                frequency_name = "D"
            if event.key == K_t:
                frequency_name = "D#"

            if event.key == K_h:
                frequency_name = "E"

            if event.key == K_j:
                frequency_name = "F"
            if event.key == K_u:
                frequency_name = "F#"

            if event.key == K_k:
                frequency_name = "G"
            if event.key == K_i:
                frequency_name = "G#"

            if event.key == K_l:
                frequency_name = "A"
            if event.key == K_o:
                frequency_name = "A#"

            if event.key == K_SEMICOLON:
                frequency_name = "B"


            #sound_to_mono()
            #echo()

            #previewSamples = triangle_tone("C", 0, 44100, 2.5)
            #previewSamples = saw_tone("C", 4, 44100, 2.5)
            #previewSamples = dual_tone("C", 2, "E", 4, 44100, 2.5)

            if event.key == K_f or event.key == K_r or event.key == K_g or event.key == K_t or event.key == K_h or event.key == K_u or event.key == K_j or event.key == K_i \
                    or event.key == K_k or event.key == K_l  or event.key == K_o or event.key == K_SEMICOLON or update_audio_stream:
                previewSamples = generate_tone(tone_type, frequency_name, frequency_key)
                preview_start = 0
                preview_max = len(previewSamples.sample_data)
                previewSamples.encode_samples()
                audio_stream = b''.join(previewSamples.encoded_data)
                sound.stop()
                sound = pygame.mixer.Sound(audio_stream)
                sound.play(loops=-1)
                update_audio_stream = False
                key_down = True
                print("Done!")

        elif event.type == KEYUP:
            if event.key == K_f or event.key == K_r or event.key == K_g or event.key == K_t or event.key == K_h or event.key == K_u or event.key == K_j or event.key == K_i \
                    or event.key == K_k or event.key == K_l  or event.key == K_o or event.key == K_SEMICOLON:
                sound.stop()
                previewSamples = wave_ext.ReadWriteWav()
                previewSamples.sample_data = [0]
                key_down = False

    prv_pass += 441 * delta_time

    if prv_pass > 1:
        preview_start += math.floor(prv_pass)
        prv_pass -= math.floor(prv_pass)

    preview_end = preview_start + preview_display
    if preview_start > preview_max:
        preview_start -= preview_max

    draw_wave_to_screen(1000, 150, previewSamples.sample_data[preview_start:preview_end], MAX_DEPTH)

    text = "Tone: "+tone_type+" Key: "+frequency_name+str(frequency_key)
    text_surface = pygame.Surface((1000, 150))
    text_surface.fill((25, 25, 25))
    text_surface = fontface.render(text, True, (255, 255, 255))

    pygame.draw.rect(screen, (25, 25, 25), (0, 150, 1000, 100), 0)
    screen.blit(text_surface, (0, 150))

    fps_clock.tick(FPS)
    delta_time = fps_clock.get_time() / 1000