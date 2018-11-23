# Comp-120 tinkering with audio
### Contract 2 - Ashley Sands

Contract 2 consists of creating ambient dungeon audio 
 
The alforithms to load, create, modifiy and save .WAV audio file can be found in 'wave_ext.py' 

Sound effect can be found in 'SoundFX.py', sound waves are in 'waves.py' and audio is rendered in 'main.py'  
Audio scripts are loaded from './audioFiles/' folder and audio .WAV file are outputed to './audio/' folder with the name specified in the TRACK_NAME variable from the audio_track script 

The audio tool requires Python 3.6 with pygame 1.9.4, Lib/wave.py and Lib/struct.py installed

To generate a .WAV file run 'main.py' and press either 'Audio 1', 'Audio 2', 'Audio 3' or 'Audio 4' buttons. 
to render the audio script. You can preview the audio once it has rendered by pressing the 'Play' button.  
Note The 'play' button not will play unless you have rendered an audio script and it will play the last rendered audio  
##### WARNING: it a .WAV file already exist it will be overwritten

#### Algorithm list: 	(simple description -> function name)
###### wave_ext.py
```
Get all audio samples from wav file                 -> get_sample_date()
Open wave file for writeing                         -> open_write_file()
Unpack Wave date                                    -> samples_byte_to_value()
Pack sample date                                    -> sample_value_to_byte()
Combine samples (eiter Additive or subtractive)     -> combine_samples()
Normalize audio                                     -> normalize()
Reverse Audio                                       -> reverse()
Save audio to .Wav file                             -> write_sample_date()
```

###### waves.py
```
Modify frequancy by key                             -> get_tone_by_key()
Generate sine tone                                  -> gen_sine_wave_tone()
Generate saw tone                                   -> gen_saw_wave_tone()
Generate triangle tone                              -> gen_triangle_wave_tone()
```

###### soundFx.py
```
Echo audio                                          -> SoundFxLibrary.echo()
Initilize ADSR envelope                             -> ADSR_Envelope.__init__()
Apply ADSR envelope                                 -> ADSR_Envelope.apply_adsr_envelop()
```

###### main.py
```
Render Audio file                                   -> render()
Combine Audio                                       -> combine_audio()
```

###### Audio files to be rendered:
```
./audioFile/audio_track_0.py
./audioFile/audio_track_1.py
./audioFile/audio_track_2.py
./audioFile/audio_track_3.py
```

Github repo: 		https://github.com/Ashley-Sands/Comp-120-tinkering-with-audio  
Github username:	Ashley-Sands  
Github user ID:		44715031