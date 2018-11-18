
class SoundFxLibrary:
    pass


class EnvelopeValue:
    """Store envelope values for an individual sections of the envelope"""
    start_time = 0      # Samples
    end_time = 0        # Samples
    start_value = 0     # value 0 to 1
    end_value = 0       # value 0 to 1

    def __init__(self, start_time, length, start_value, end_value):
        self.start_time = start_time
        self.end_time = start_time + length
        self.start_value = start_value
        self.end_value = end_value


class ADSR_envelope:

    envelope_data = {}
    release_time = None

    def __init__(
            self, sample_rate,
            attack_length, attack_start_value, attack_end_value,
            decay_length, decay_end_value,
            sustain_length, sustain_end_value,
            release_length, release_end_value
    ):
        """
        Todo.
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
        prv_end_time, prv_end_value = self.set_envelop_value("sustain", prv_end_time, sustain_length, prv_end_value, sustain_end_value, sample_rate)
        prv_end_time, prv_end_value = self.set_envelop_value("decay", prv_end_time, decay_length, prv_end_value, decay_end_value, sample_rate)

        self.release_time = EnvelopeValue(0, release_length*sample_rate, prv_end_value, release_end_value, sample_rate)

    def set_envelop_value(self, value_name, prv_end_time, length, start_value, end_value, samples_rate):
        """

        :param value_name:          envelope stage name
        :param prv_end_time:        end time of the last stage in samples
        :param length:              length of stage in seconds
        :param start_value:         end value of lsat stage
        :param end_value:           end value of stage
        :return:                    (end time, end value)
        """
        start_time = prv_end_time
        end_time = prv_end_time + int(length * samples_rate)

        self.envelope_data[value_name] = EnvelopeValue(start_time, end_time, start_value, end_value)

        return end_time, end_value

    def apply_adsr_envelop(self, audio_data, samples):

        current_stage_index = 0
        stages = list(self.envelope_data)

        # loop the sample indexes because its our measurement of time.
        for sample_index in range( len(audio_data) ):

            if sample_index > stages[current_stage_index].end_time and current_stage_index < len(stages)-1:
                current_stage_index += 1

            current_stage = self.envelope_data[ stages[current_stage_index] ]
