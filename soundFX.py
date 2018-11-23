"""
Drive: Ashley Sands
Navigator: None
"""
import wave_ext


class SoundFxLibrary:
    """Sound Effects"""
    combine_audio_funct = None

    def __init__(self):

        self.combine_audio_funct = None

    def echo(self,
             audio_stream,
             echo_start_sample,
             echo_length,
             delay_length,
             volume_multiplier
             ):
        """ Echo range of samples from audio stream

        :param audio_stream:        audio stream to echo
        :param echo_start_sample:   position to start echoing from in samples
        :param echo_length:         amount of samples to echo
        :param delay_length:        delay in samples inbetween echos
        :param volume_multiplier:   audio to decress volume by
        (must be less than 1)
        :return:                    audio stream
        """
        print("Echoing")

        # get the range of samples to echo and start position
        echo_samples = audio_stream.get_sample_range(
            int(echo_start_sample),
            int(echo_start_sample+echo_length)
        )
        current_sample_index = echo_start_sample + delay_length

        # keep applying the echo until the volume < 0.01 it needs to be above
        # 0 as the volume_multiplier will never reach exactly 0
        while volume_multiplier > 0.01:
            audio_stream = self.combine_audio_funct(audio_stream,
                                                    echo_samples,
                                                    current_sample_index,
                                                    volume_multiplier
                                                    )
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
        """ Initialize ADSR Envelope

        :param sample_rate:         Audio sample rate
        :param attack_length:       attack length in seconds
        :param attack_start_value:  attack start value
        :param attack_end_value:    attack end value
        :param decay_length:        decay length in seconds
        :param decay_end_value:     decay end value
        :param sustain_length:      sustain length in seconds
        :param sustain_end_value:   sustain end value
        :param release_length:      release length in seconds
        :param release_end_value:   release end value
        """

        # Set up the envelope
        self.envelope_data = {}
        # set the prv end time to 0 as its the start of the envelope and
        # carry the prv time forwards for the next start times/values
        prv_end_time, prv_end_value = self.set_envelop_value(
            "attack",
            0,
            attack_length,
            attack_start_value,
            attack_end_value,
            sample_rate
        )
        prv_end_time, prv_end_value = self.set_envelop_value(
            "decay",
            prv_end_time,
            decay_length,
            prv_end_value,
            decay_end_value,
            sample_rate
        )
        prv_end_time, prv_end_value = self.set_envelop_value(
            "sustain",
            prv_end_time,
            sustain_length,
            prv_end_value,
            sustain_end_value,
            sample_rate
        )

        # release envelope
        self.release_envelope = EnvelopeValue(0,
                                              release_length*sample_rate,
                                              prv_end_value,
                                              release_end_value
                                              )

    def set_envelop_value(self,
                          value_name,
                          prv_end_time,
                          length,
                          start_value,
                          end_value,
                          sample_rate
                          ):
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

        self.envelope_data[value_name] = EnvelopeValue(start_time,
                                                       end_time,
                                                       start_value,
                                                       end_value
                                                       )

        return end_time, end_value

    def apply_adsr_envelop(self,
                           wave_funct,
                           sample_rate,
                           frequency,
                           length,
                           velocity=1
                           ):
        """ Apply the adsr envelop to a wave function

        :param wave_funct:      wave function to apply the envelope to
        :param sample_rate:     sample rate to generate the wave at
        :param frequency:       frequency of wave
        :param length:          length of eave in samples
        :param velocity:        wave velocity
        :return:                audio stream
        """
        # set current stage index and get the stage names
        current_stage_index = 0
        stages = list(self.envelope_data)

        sound = wave_ext.ReadWriteWav()
        length = length

        # store the envelope value so we can continue
        # from the last value when the key is released
        envelope_value = 0

        # main stages of the envelop
        for sample_index in range(int(length)):

            # move to the next stage
            if sample_index >= self.envelope_data[
                stages[current_stage_index]
            ].end_time and current_stage_index < len(stages)-1:
                current_stage_index += 1

            # find our position in the envelope stage and
            # get the value at position
            start_time = self.envelope_data[
                stages[current_stage_index]
            ].start_time
            end_time = self.envelope_data[
                stages[current_stage_index]
            ].end_time

            start_value = self.envelope_data[
                stages[current_stage_index]
            ].start_value
            end_value = self.envelope_data[
                stages[current_stage_index]
            ].end_value

            envelope_stage_position = (
                    (sample_index - start_time) / (end_time - start_time)
            )
            envelope_value = ADSR_Envelope.lerp(start_value,
                                                end_value,
                                                envelope_stage_position
                                                )
            envelope_value = ADSR_Envelope.clamp01(envelope_value)

            sound.add_sample(
                wave_funct(
                    sample_index,
                    sample_rate,
                    frequency,
                    velocity * envelope_value
                )
            )

        # release stage of the envelop
        for release_index in range(int(self.release_envelope.end_time)):

            release_position = release_index / self.release_envelope.end_time
            release_value = ADSR_Envelope.lerp(envelope_value,
                                               self.release_envelope.end_value,
                                               release_position
                                               )

            sound.add_sample(
                wave_funct(
                    sample_index + release_index,
                    sample_rate,
                    frequency,
                    velocity * release_value
                )
            )

        return sound

    @staticmethod
    def lerp(start_value, end_value, time):
        """ lerp from start to end by time (0 to 1)"""
        value_dif = end_value - start_value

        return start_value + (value_dif * time)

    @staticmethod
    def clamp01(value):
        """Clamp value between 0 and 1"""
        if value < 0:
            return 0
        elif value > 1:
            return 1

        return value
