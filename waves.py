import wave_ext
import math

class WaveLibrary:

    sample_rate = 44100
    max_depth = 0

    def __init__(self, sample_rate, max_depth):

        self.sample_rate = sample_rate
        self.max_depth = max_depth

    def get_sound(self, wave_shape, base_freq, key, harmonic_steps, length, envelope=None):

        tone_generator = self.get_wave_function(wave_shape)
        freq = self.get_tone_by_key(base_freq, key)

        audio = wave_ext.ReadWriteWav()

        if envelope is not None:
            audio = envelope.apply_adsr_envelop(tone_generator, self.sample_rate, freq, length)
        else:
            audio = self.get_wave(tone_generator, freq, length)

        for harmonic_step in range(0, harmonic_steps+1):

            freq = self.get_tone_by_key(base_freq, key+harmonic_step)

            if envelope is not None:
                harm_audio = envelope.apply_adsr_envelop(tone_generator, self.sample_rate, freq, length)
            else:
                harm_audio = self.get_wave(tone_generator, freq, length)

            for samp in range(len(harm_audio.sample_data)):
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

    def get_wave_function(self, wave_name):

        if wave_name == "sine":
            return self.gen_sine_wave_tone
        elif wave_name == "triangle":
            return self.gen_triangle_wave_tone
        elif wave_name == "saw":
            return self.gen_saw_wave_tone

        print("Error: wave function not found: ", wave_name)

    def gen_sine_wave_tone(self, current_sample, sample_rate, frequency, volume):

        return math.sin(2.0 * math.pi * frequency * (current_sample / float(sample_rate))) * (self.max_depth * volume)

    def gen_triangle_wave_tone(self, current_sample, sample_rate, frequency, volume):

        return (2.0 * self.max_depth / math.pi) * math.asin(
            (math.sin(2.0 * math.pi * current_sample / (sample_rate / frequency)))) * (self.max_depth * volume)

    def gen_saw_wave_tone(self, current_sample, sample_rate, frequency, volume):

        # add one to current sample so we do not divide by 0
        current_sample += 1

        tan = math.tan(current_sample * math.pi / (sample_rate / frequency))
        return -(2.0 * self.max_depth / math.pi) * math.atan(1.0 / tan) * (self.max_depth * volume)

    def get_wave(self, wave_funct, frequency, length, velocity=1):

        sound = wave_ext.ReadWriteWav()
        length = length

        for sample_index in range(int(length)):
            sound.add_sample(wave_funct(sample_index, self.sample_rate, frequency, velocity))

        return sound
