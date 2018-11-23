import wave_ext

class SoundFxLibrary:

    combine_audio_funct = None

    def __init__(self):

        self.combine_audio_funct = None

    def echo(self, audio_stream, echo_start_sample, echo_length, delay_length, volume_multiplier):

        print("Echoing")

        echo_samples = audio_stream.get_sample_range(int(echo_start_sample), int(echo_start_sample+echo_length))
        current_sample_index = echo_start_sample + delay_length

        # keep applying the echo until the volume < 0.01
        # it needs to be above 0 as the volume_multiplier will never reach exactly 0
        while volume_multiplier > 0.01:
            audio_stream = self.combine_audio_funct(audio_stream, echo_samples, current_sample_index, volume_multiplier)
            volume_multiplier *= volume_multiplier
            current_sample_index += delay_length

        return audio_stream


class EnvelopeValue:
    """Store envelope values for an individual sections of the envelope"""
    start_time = 0      # Samples
    end_time = 0        # Samples
    start_value = 0     # value 0 to 1
    end_value = 0       # value 0 to 1

    def __init__(self, start_time, end_time, start_value, end_value):
        self.start_time = start_time
        self.end_time = end_time
        self.start_value = start_value
        self.end_value = end_value


class ADSR_Envelope:
    """ADSR Envelope"""
    envelope_data = {}
    release_envelope = None

    def __init__(
            self, sample_rate,
            attack_length, attack_start_value, attack_end_value,
            decay_length, decay_end_value,
            sustain_length, sustain_end_value,
            release_length, release_end_value
    ):
        """
        Todo.
        :param sample_rate:
        :param attack_length:
        :param attack_start_value:
        :param attack_end_value:
        :param decay_length:
        :param decay_end_value:
        :param sustain_length:
        :param sustain_end_value:
        :param release_length:
        :param release_end_value:
        """

        # Set up the envelope
        self.envelope_data = {}
        # set the prv end time to 0 as its the start of the envelope
        prv_end_time, prv_end_value = self.set_envelop_value("attack", 0, attack_length, attack_start_value, attack_end_value, sample_rate)
        prv_end_time, prv_end_value = self.set_envelop_value("decay", prv_end_time, decay_length, prv_end_value, decay_end_value, sample_rate)
        prv_end_time, prv_end_value = self.set_envelop_value("sustain", prv_end_time, sustain_length, prv_end_value, sustain_end_value, sample_rate)

        self.release_envelope = EnvelopeValue(0, release_length*sample_rate, prv_end_value, release_end_value)

    def set_envelop_value(self, value_name, prv_end_time, length, start_value, end_value, sample_rate):
        """

        :param sample_rate:         sample rate of the audio file
        :param value_name:          envelope stage name
        :param prv_end_time:        end time of the last stage in samples
        :param length:              length of stage in seconds
        :param start_value:         end value of lsat stage
        :param end_value:           end value of stage
        :return:                    (end time, end value)
        """
        start_time = prv_end_time
        end_time = prv_end_time + int(length * sample_rate)

        self.envelope_data[value_name] = EnvelopeValue(start_time, end_time, start_value, end_value)

        return end_time, end_value

    def apply_adsr_envelop(self, wave_funct, sample_rate, frequency, length, velocity=1):

        current_stage_index = 0
        stages = list(self.envelope_data)

        sound = wave_ext.ReadWriteWav()
        length = length
        # store the envelope value so we can continue from the last value when the key is released
        envelope_value = 0

        # main stages of the envelop
        for sample_index in range(int(length)):
            if sample_index >= self.envelope_data[stages[current_stage_index]].end_time and current_stage_index < len(stages)-1:
                current_stage_index += 1

            envelope_stage_position = (sample_index - self.envelope_data[stages[current_stage_index]].start_time) / (self.envelope_data[stages[current_stage_index]].end_time - self.envelope_data[stages[current_stage_index]].start_time)

            envelope_value = ADSR_envelope.lerp(self.envelope_data[stages[current_stage_index]].start_value, self.envelope_data[stages[current_stage_index]].end_value, envelope_stage_position)
            envelope_value = ADSR_envelope.clamp01(envelope_value)

            sound.add_sample(wave_funct(sample_index, sample_rate, frequency, velocity * envelope_value))

        # release stage of the envelop
        for release_index in range(int(self.release_envelope.end_time)):

            release_position = release_index / self.release_envelope.end_time

            release_value = ADSR_envelope.lerp(envelope_value, self.release_envelope.end_value, release_position)

            sound.add_sample(wave_funct(sample_index + release_index, sample_rate, frequency, velocity * release_value))

        return sound

    @staticmethod
    def lerp(start_value, end_value, time):

        value_dif = end_value - start_value

        return start_value + (value_dif * time)

    @staticmethod
    def clamp01(value):

        if value < 0:
            return 0
        elif value > 1:
            return 1

        return value
