import soundFX
import wave_ext

"""
Audio Track 0
Author:         Ashley Sands
Track Name:     Critical Creepy 0
"""

TRACK_NAME = "critical_creepy_0"

COMBINE_ADD = wave_ext.ReadWriteWav.COMBINE_ADD
COMBINE_SUB = wave_ext.ReadWriteWav.COMBINE_SUB

SAMPLE_RATE = 44100

# Envelope pramas
# Sample rate,
# attack length, attack start value, attack end value
# decay length, decay end value,
# sustain length, sustain end value
# release length, release end value
adsr_envelope = soundFX.ADSR_Envelope(SAMPLE_RATE,
                                      0.1, 0, 1,
                                      0.1, 0.75,
                                      0.2, 0.25,
                                      0.2, 0
                                      )
adsr_long_envelope = soundFX.ADSR_Envelope(SAMPLE_RATE,
                                           0.2, 0, 1,
                                           .5, 0.75,
                                           1, 0.5,
                                           0.2, 0
                                           )

timeline = []
timeline.append(
    {
        "start_sample": 0,
        "length": SAMPLE_RATE * 1,
        "base_freq": "D",
        "key": 2,
        "harmonic_steps": 1,
        "wave_shape": "triangle",
        "envelope": adsr_envelope,
        "velocity": 0.7,
        "combine": COMBINE_ADD,
        "echo": (0, SAMPLE_RATE * 0.5, SAMPLE_RATE * 0.15, 0.99999)
    }
)
timeline.append(
    {
        "start_sample": 0,
        "length": SAMPLE_RATE * 1,
        "base_freq": "D",
        "key": 1,
        "harmonic_steps": 2,
        "wave_shape": "sine",
        "envelope": adsr_envelope,
        "velocity": 0.7,
        "combine": COMBINE_SUB,
        "echo": (0, SAMPLE_RATE * 0.5, SAMPLE_RATE * 0.25, 0.99999)
    }
)
timeline.append(
    {
        "start_sample": 0,
         "length": SAMPLE_RATE * 10,
         "base_freq": "D",
         "key": 2,
         "harmonic_steps": 3,
         "wave_shape": "saw",
         "envelope": adsr_long_envelope,
         "velocity": 0.2,
         "combine": COMBINE_ADD,
         "echo": (0, SAMPLE_RATE * 0.5, SAMPLE_RATE * 0.25, 0.99999)
     }
)

timeline.append(
    {
        "start_sample": 0,
        "length": SAMPLE_RATE * 6,
        "base_freq": "F",
        "key": 1,
        "harmonic_steps": 3,
        "wave_shape": "triangle",
        "envelope": adsr_long_envelope,
        "velocity": 1,
        "combine": COMBINE_ADD,
        "echo": (0, SAMPLE_RATE * .5, SAMPLE_RATE * 0.75, 0.9999)
    }
)

timeline.append(
    {
        "start_sample": 0,
        "length": SAMPLE_RATE * 1,
        "base_freq": "D",
        "key": 2,
        "harmonic_steps": 3,
        "wave_shape": "sine",
        "envelope": adsr_long_envelope,
        "velocity": 0.7,
        "combine": COMBINE_SUB,
        "echo": (0, SAMPLE_RATE * 0.25, SAMPLE_RATE * 0.75, 0.99999)
    }
)
