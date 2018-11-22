import soundFX

SAMPLE_RATE = 44100

adsr_envelope = soundFX.ADSR_envelope(SAMPLE_RATE, 0.1, 0, 1, .1, 0.75, 0.2, 0.25, .2, 0)
adsr_saw_envelope = soundFX.ADSR_envelope(SAMPLE_RATE, 0.3, 0, 1, .1, .7, 0.2, 0.1, 0.1, 0)
adsr_sine_envelope = soundFX.ADSR_envelope(SAMPLE_RATE, 0.3, 0, 1, .1, 1, 0.2, 0.25, 0.2, 0)
adsr_bass_envelope = soundFX.ADSR_envelope(SAMPLE_RATE, 0.1, 0, 1, 0.25, 0.75, 1, 0.5, 0.1, 0)

timeline = []
timeline.append({"start_sample": 0, "length": SAMPLE_RATE * 1, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": .7, "echo": (0, SAMPLE_RATE * .5, SAMPLE_RATE * 0.05, 0.99999)})
#timeline.append({"start_sample": 0, "length": SAMPLE_RATE * 1, "base_freq": "E", "key": 2, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_envelope, "velocity": .5, "echo": (0, SAMPLE_RATE * .1, SAMPLE_RATE * 0.15, 0.99)})

timeline.append({"start_sample": SAMPLE_RATE * 1.25, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 3, "harmonic_steps": 2, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": 0.5})
timeline.append({"start_sample": SAMPLE_RATE * 2.5, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 3, "harmonic_steps": 2, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": 0.5})
timeline.append({"start_sample": SAMPLE_RATE * 2.95, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 2, "harmonic_steps": 2, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": 0.6})
timeline.append({"start_sample": SAMPLE_RATE * 3.75, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 3, "harmonic_steps": 2, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": 0.5})

timeline.append({"start_sample": SAMPLE_RATE * 1.25, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": .8})
timeline.append({"start_sample": SAMPLE_RATE * 1.5, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": .8})
timeline.append({"start_sample": SAMPLE_RATE * 1.75, "length": SAMPLE_RATE * 0.015, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "triangle", "envelope": adsr_envelope, "velocity": .8})

timeline.append({"start_sample": 0, "length": SAMPLE_RATE * 1, "base_freq": "E", "key": 1, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_bass_envelope, "velocity": 1})
timeline.append({"start_sample": SAMPLE_RATE * 1.25, "length": SAMPLE_RATE * 1, "base_freq": "G", "key": 1, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_bass_envelope, "velocity": 1})
timeline.append({"start_sample": SAMPLE_RATE * 2.5, "length": SAMPLE_RATE * 1, "base_freq": "F", "key": 1, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_bass_envelope, "velocity": 1})
timeline.append({"start_sample": SAMPLE_RATE * 3.75, "length": SAMPLE_RATE * 1, "base_freq": "D", "key": 1, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_bass_envelope, "velocity": 1})

timeline.append({"start_sample": SAMPLE_RATE * 4.5, "length": SAMPLE_RATE * 1, "base_freq": "F", "key": 1, "harmonic_steps": 2, "wave_shape": "sine", "envelope": adsr_bass_envelope, "velocity": 1})

timeline.append({"start_sample": SAMPLE_RATE * 0.75, "length": SAMPLE_RATE * 0.1, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_saw_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 2, "length": SAMPLE_RATE * 0.1, "base_freq": "D", "key": 2, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_saw_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 3.25, "length": SAMPLE_RATE * 0.1, "base_freq": "F", "key": 2, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_saw_envelope, "velocity": .7})

timeline.append({"start_sample": SAMPLE_RATE * 4, "length": SAMPLE_RATE * 0.75, "base_freq": "D", "key": 1, "harmonic_steps": 1, "wave_shape": "saw", "envelope": adsr_saw_envelope, "velocity": .3})

timeline.append({"start_sample": SAMPLE_RATE * 0, "length": SAMPLE_RATE * 0.1, "base_freq": "D", "key": 1, "harmonic_steps": 1, "wave_shape": "saw", "envelope": adsr_saw_envelope, "velocity": .6})
timeline.append({"start_sample": SAMPLE_RATE * 1.25, "length": SAMPLE_RATE * 0.0125, "base_freq": "D", "key": 3, "harmonic_steps": 1, "wave_shape": "saw", "envelope": adsr_saw_envelope, "velocity": .5})
timeline.append({"start_sample": SAMPLE_RATE * 2.5, "length": SAMPLE_RATE * 0.0125, "base_freq": "D", "key": 3, "harmonic_steps": 1, "wave_shape": "saw", "envelope": adsr_saw_envelope, "velocity": .5})
timeline.append({"start_sample": SAMPLE_RATE * 3.75, "length": SAMPLE_RATE * 0.0125, "base_freq": "D", "key": 3, "harmonic_steps": 1, "wave_shape": "saw", "envelope": adsr_saw_envelope, "velocity": .5})
timeline.append({"start_sample": SAMPLE_RATE * 4.85, "length": SAMPLE_RATE * 0.1, "base_freq": "D", "key": 2, "harmonic_steps": 2, "wave_shape": "saw", "envelope": adsr_saw_envelope, "velocity": .4})

timeline.append({"start_sample": SAMPLE_RATE * 1, "length": SAMPLE_RATE * 0.1, "base_freq": "F", "key": 4, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_sine_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 2.25, "length": SAMPLE_RATE * 0.1, "base_freq": "F", "key": 4, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_sine_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 2.6, "length": SAMPLE_RATE * 0.1, "base_freq": "F", "key": 3, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_sine_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 3.25, "length": SAMPLE_RATE * 0.1, "base_freq": "F", "key": 3, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_sine_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 3.45, "length": SAMPLE_RATE * 0.025, "base_freq": "F", "key": 3, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_saw_envelope, "velocity": .7})
timeline.append({"start_sample": SAMPLE_RATE * 3.65, "length": SAMPLE_RATE * 0.025, "base_freq": "F", "key": 3, "harmonic_steps": 1, "wave_shape": "sine", "envelope": adsr_saw_envelope, "velocity": .7})
