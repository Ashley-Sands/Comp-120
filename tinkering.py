import pygame
from pygame.locals import *
import sys
import math
import wave
import struct

pygame.init()
screen = pygame.display.set_mode((150, 150))

LENGTH = 15 # time in seconds
CHANNELS = 1
SAMPLE_RATE = 44100
# FREQUENCY = 1500
VOLUME = 0.75
BIT_DEPTH = 32767

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


def open_read_wav_file(filename):
    """does not require the .wav extension"""
    wav = wave.open("audio/"+filename+".wav", "rb")
    return wav


def open_write_wav_file(filename):
    """does not require the .wav extension"""
    wav = wave.open("audio/"+filename+".wav", "w")
    return wav


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


def gen_tone(wav, FREQUENCY):

    wav.setparams((CHANNELS, 2, SAMPLE_RATE, (SAMPLE_RATE * LENGTH), "NONE", "not compressed"))

    values = []

    for i in range(SAMPLE_RATE * LENGTH):
        value = math.sin( 2.0 * math.pi * FREQUENCY * (i / float(SAMPLE_RATE * LENGTH)) ) * ( VOLUME * BIT_DEPTH )
        packed_value = struct.pack('h', int(value))

        #for chan in range(0, CHANNELS):
        values.append(packed_value)

        if (i % 44100) == 44099:
            FREQUENCY *= 2

        print(FREQUENCY)

    print((SAMPLE_RATE * LENGTH))

    value_str = b''.join(values)
    print("Bop")
    wav.writeframesraw(value_str)
    wav.close()


def get_sample_tone(current_sample, frequency, lfo_amount):
    return math.sin(2.0 * math.pi * frequency * (current_sample / float(SAMPLE_RATE)))



def gen_all_tones(wav):

    wav.setparams((CHANNELS, 2, SAMPLE_RATE, (SAMPLE_RATE * LENGTH), "NONE", "not compressed"))

    values = []

    freq_keys = list(BASE_FREQUENCIES)
    max_key = 8

    for k in range(1, (max_key+1)):
        packed_value = struct.pack('h', 0)
        for f in freq_keys:

            frequency = get_tone_by_key(k, f)

            for i in range((SAMPLE_RATE)):
                value = get_sample_tone(i, frequency, 8) * (VOLUME * BIT_DEPTH)
                packed_value = struct.pack('h', int(value))

                for chan in range(0, CHANNELS):
                    values.append(packed_value)

            print(f, k, frequency)

    print((SAMPLE_RATE * LENGTH))

    value_str = b''.join(values)
    print("Bop")
    wav.writeframesraw(value_str)
    wav.close()

def get_tone_by_key(key, tone_key):

    base_tone = BASE_FREQUENCIES[tone_key]

    for i in range(key):
        base_tone *= 2

    return base_tone

def get_sample_value(sample):

    if sample != b'':
        return struct.unpack_from('h', sample)[0]
    else:
        return 0


def print_samples():

    wav = open_read_wav_file("a")
    channels = wav.getnchannels()
    total_samples = wav.getnframes()

    print("Channels", channels)
    print("frequency", wav.getframerate())

    for samp in range(0, total_samples, channels):

        out_str = ''
        for chan in range(channels):
            out_str += " :: chan "+str(chan+1)+": " + str(get_sample_value(wav.readframes(samp+chan)))

        print(samp, out_str)

    wav.close()


def sound_to_mono():

    read_wav = open_read_wav_file("a")

    chan_prams = read_wav.getparams()

    channels =  read_wav.getnchannels()
    sample_rate = read_wav.getframerate()
    total_samples = read_wav.getnframes()

    print("chan: ", channels, "samp rate:", sample_rate, "total samps:", total_samples, "length:", int((total_samples / channels)))

    write_wav = open_write_wav_file("a_mono")
    write_wav.setparams((1, 2, sample_rate, int((total_samples / channels)), "NONE", "not compressed"))

    out_wav = []

    for samp in range(0, total_samples, channels):

        channel_samples = []
        for chan in range(channels):
            #print(read_wav.readframes(samp+chan))
            channel_samples.append(get_sample_value(read_wav.readframes(1)))

        # make mono
        mono = int(average_samples(channel_samples))
        print(mono)
        packed_wav = struct.pack('i', mono)
        print(packed_wav)
        out_wav.append(packed_wav)

    #return
    value_str = b''.join(out_wav)
    write_wav.writeframesraw(value_str)

    read_wav.close()
    write_wav.close()

    sound = pygame.mixer.Sound(value_str)
    sound.play()


save_count = 0

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
                #write_wav_file(read_wav_file("a"))
                #gen_tone(open_write_wav_file("assasa_C"), 16.35)
                gen_all_tones(open_write_wav_file("assasa_ALL"))
                #save_count += 1
                #print(save_count)


