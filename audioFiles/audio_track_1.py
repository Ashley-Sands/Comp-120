import soundFX
import wave_ext

"""
Audio Track 1
Author:         Ashley Sands
Track Name:     Critical Creepy 1
"""

TRACK_NAME = "critical_creepy_1"

COMBINE_ADD = wave_ext.ReadWriteWav.COMBINE_ADD
COMBINE_SUB = wave_ext.ReadWriteWav.COMBINE_SUB

SAMPLE_RATE = 44100

adsr_envelope = soundFX.ADSR_Envelope(SAMPLE_RATE, 0.1, 0, 1, .1, 0.75, 0.2, 0.25, .2, 0)
adsr_saw_envelope = soundFX.ADSR_Envelope(SAMPLE_RATE, 0.3, 0, 1, .1, .7, 0.2, 0.1, 0.1, 0)
adsr_sine_envelope = soundFX.ADSR_Envelope(SAMPLE_RATE, 0.3, 0, 1, .1, 1, 0.2, 0.25, 0.2, 0)
adsr_bass_envelope = soundFX.ADSR_Envelope(SAMPLE_RATE, 0.1, 0, 1, 0.25, 0.75, 1, 0.5, 0.1, 0)

timeline = []
timeline.append({"start_sample": 0, "length": SAMPLE_RATE * 1, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": .7, "combine": COMBINE_ADD, "echo": (0, SAMPLE_RATE * .5, SAMPLE_RATE * 0.15, 0.99999)})
timeline.append({"start_sample": 0, "length": SAMPLE_RATE * 1, "base_freq": "D", "key": 1, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_envelope, "velocity": .7, "combine": COMBINE_SUB, "echo": (0, SAMPLE_RATE * .5, SAMPLE_RATE * 0.25, 0.99999)})
timeline.append({"start_sample": 0, "length": SAMPLE_RATE * 1, "base_freq": "F", "key": 2, "harmonic_steps": 3, "wave_shape": "sine", "envelope": adsr_envelope, "velocity": .5, "combine": COMBINE_SUB, "echo": (0, SAMPLE_RATE * .15, SAMPLE_RATE * 0.25, 0.9999)})
