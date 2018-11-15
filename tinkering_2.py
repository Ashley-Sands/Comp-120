import pygame
from pygame.locals import *
import sys
import math
import wave_ext

pygame.init()
screen = pygame.display.set_mode((150, 150))

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


def dual_tone(freq_1_name, freq_1_key, freq_2_name, freq_2_key, sample_rate, length):

    sound = wave_ext.ReadWriteWav()

    for i in range(sample_rate * length):
        sound.add_sample(get_sin_wave_tone(i, sample_rate, get_tone_by_key(freq_1_key, freq_1_name)))
        sound.combine_samples(i, get_sin_wave_tone(i, sample_rate, get_tone_by_key(freq_2_key, freq_2_name)))

    sound.normalize((MAX_DEPTH * 0.9))
    sound.write_sample_data("audio/two_tones__", 1, sample_rate)


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

    pass


def get_tone_by_key(key, tone_key):

    base_tone = BASE_FREQUENCIES[tone_key]

    for i in range(key):
        base_tone *= 2

    return base_tone


while True:

    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # change the key pressed state
        elif event.type == KEYDOWN:
            if event.key == K_i:
                #sound_to_mono()
                #echo()
                dual_tone("C", 2, "E", 4, 44100, 2)
                print("Done!")
