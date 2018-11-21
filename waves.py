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
    def get_tone_by_key(freq, key):

        base_tone = freq

        for i in range(int(abs(key))):
            if key > 0:
                base_tone *= 2
            else:
                base_tone /= 2

        return base_tone

    def gen_sine_wave_tone(self, current_sample, sample_rate, frequency, volume):
        return math.sin(2.0 * math.pi * frequency * (current_sample / float(sample_rate))) * (self.max_depth * volume)

    def get_triangle_wave_tone(self, current_sample, sample_rate, frequency, volume):

        return (2.0 * self.max_depth / math.pi) * math.asin(
            (math.sin(2.0 * math.pi * current_sample / (sample_rate / frequency)))) * (self.max_depth * volume)

    def get_saw_wave_tone(self, current_sample, sample_rate, frequency, volume):

        tan = math.tan(current_sample * math.pi / (sample_rate / frequency))
        return -(2.0 * self.max_depth / math.pi) * math.atan(1.0 / tan) * (self.max_depth * volume)

    def sine_tone(self, frequency, length, volume=1):

        sound = wave_ext.ReadWriteWav()
        # this prevents clicks
        length = length

        for i in range(int(length)):
            sound.add_sample(self.gen_sine_wave_tone(i, self.sample_rate, frequency, volume))

        #sound.normalize((self.max_depth * (0.9 * volume)))

        return sound