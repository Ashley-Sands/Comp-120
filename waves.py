import wave_ext
import math

class WaveLibrary:

    sample_rate = 44100
    max_depth = 0

    def __init__(self, sample_rate, max_depth):

        self.sample_rate = sample_rate
        self.max_depth = max_depth

    def get_sound(self, wave_shape, base_freq, key, harmonic_steps, length, envelope=False):


        audio = self.sine_tone(self.get_tone_by_key(base_freq, key), length)

        for harmonic_step in range(0, harmonic_steps+1):
            harm_audio = self.sine_tone(self.get_tone_by_key(base_freq, (key+harmonic_step)), length)
            for samp in range(length):
                audio.combine_samples(samp, harm_audio.sample_data[samp])

        return audio

    @staticmethod
    def get_tone_by_key(key, freq):

        base_tone = freq

        for i in range(int(key)):
            base_tone *= 2

        return base_tone

    def gen_sine_wave_tone(self, current_sample, sample_rate, frequency, volume):
        return math.sin(2.0 * math.pi * frequency * (current_sample / float(sample_rate))) * (self.max_depth * volume)

    def sine_tone(self, frequency, length, volume=1):

        sound = wave_ext.ReadWriteWav()
        # this prevents clicks
        length = length

        for i in range(int(length)):
            sound.add_sample(self.gen_sine_wave_tone(i, self.sample_rate, frequency, volume))

        #sound.normalize((self.max_depth * (0.9 * volume)))

        return sound