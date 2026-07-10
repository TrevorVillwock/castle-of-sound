from pyo import Server, Mixer, Record, MoogLP, Selector

from music import Music
from ambient_sounds import AmbientSounds
from effects import Effects

import sys
import time
import json

try:
    debug_time_delay = int(sys.argv[1])
except:
    debug_time_delay = 1

s = Server(duplex=0, ichnls=0).boot()
#s = Server(duplex=0).boot()
s.start()

class Main:  
    def __init__(self):
        self.input_is_valid = 1
        self.first_sound_started = 0
        
        self.music = Music("ionian", debug_time_delay) # default mode
        self.music_effects = Effects(self.music.guitar_mixer[0])

        self.ambient_sounds = AmbientSounds()
        self.ambient_sounds_effects = Effects(self.ambient_sounds.mixer[0])

        self.mixer = Mixer(outs=2, chnls=2, mul=0)
       
        self.config = {}
        
        with open("config.json") as settings:
            try:
                self.config = json.load(settings)
            except:
                print("error loading json")
                
        # print(f"config: {self.config}")
        
        # print(self.config)
        # print(self.config["recording_number"])
        
        # the file number is taken from config.yaml and incremented each time the program runs
        self.recorder = Record(self.mixer[0], filename=f"recording-{self.config['recording_number']}.wav")
        
        self.config['recording_number'] += 1
        
        with open("config.json", "w") as settings:
            try:
                json.dump(self.config, settings)
            except Exception as e:
                print(e)
                print("error dumping json")
        
        self.mixer.addInput(0, self.music_effects.delay_selector)
        self.mixer.addInput(1, self.ambient_sounds_effects.delay_selector)
        self.mixer.setAmp(0, 0, 0.5)
        self.mixer.setAmp(1, 0, 0.1)
        self.mixer.setTime(0.01)
        self.mixer.setMul(1)
        
        print("\n\nWelcome to CASTLE OF SOUND\n\n")
        print("""
What do you want to do?

1 - Eat breakfast (Ionian)
2 - Sit by the river (Dorian)
3 - Go to the top of the castle (Phrygian)
4 - Go to the garden (Lydian)
5 - Go for a hike (Mixolydian)
6 - Swim in the river (Aeolian)
7 - Go to the dungeon (Locrian)
w - visit the wizard (octatonic)

e - Drink Essence of Bat (echo/delay)
rt - Drink Elixir of Time (reverse samples)
s - Drink Elixir of Space (reverb)
dis [float] - Drink Elixir of Overdrive (distortion)
v freq [frequency in Hertz] - set vibrato frequency
v mult [float] - set vibrato amount
time [seconds] - Change echo length
rtime [seconds] - Change reverb length
as - Toggle ambient sounds
f [frequency] - Change filter cutoff frequency

ge - Toggle guitar echo
tf - Toggle filter
td - Toggle detune
tr - Toggle reverb
d [float] - Change detune amount
q - Quit \n"""
)
        self.action_selection = input("Input a number or letter to choose: ")
        self.action_selection_array = self.action_selection.split(' ')
        
        while True:
            # print("\n", self.action_selection_array, "\n", len(self.action_selection_array), "\n")
            match self.action_selection_array[0]:
                case "1": 
                    self.input_is_valid = 1
                    self.music.change_mode("ionian")
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("dining_hall")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("dining_hall")
                        self.music.current_triad = 0    
                case "2":
                    self.input_is_valid = 1 
                    self.music.change_mode("dorian")
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("river")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("river")
                        self.music.current_triad = 0
                case "3": 
                    self.input_is_valid = 1
                    self.music.change_mode("phrygian")
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("top_of_castle")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("top_of_castle")
                        self.music.current_triad = 0
                case "4":
                    self.input_is_valid = 1
                    self.music.change_mode("lydian")
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("birds")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("birds")
                        self.music.current_triad = 0
                case "5":
                    self.input_is_valid = 1 
                    self.music.change_mode("mixolydian")
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("hike")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("hike")
                        self.music.current_triad = 0
                case "6":
                    self.input_is_valid = 1 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("underwater")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("underwater")
                        self.music.change_mode("aeolian")
                        self.music.current_triad = 0
                case "7":
                    self.input_is_valid = 1 
                    if not self.first_sound_started:
                        self.ambient_sounds.start_first_sound("dungeon")
                        self.first_sound_started = 1
                    else:
                        self.ambient_sounds.change_sound("dungeon")
                        self.music.change_mode("locrian")
                        self.music.current_triad = 0
                case "w":
                    # print("octatonic")
                    self.input_is_valid = 1
                    self.music.change_mode("octatonic")
                    self.music.current_triad = 0
                case "rt":
                    self.input_is_valid = 1
                    self.music.reverse_samples()
                    self.ambient_sounds.reverse_sounds()
                case "s":
                    self.input_is_valid = 1
                    self.music_effects.toggle_reverb()
                    self.ambient_sounds_effects.toggle_reverb()
                case "rtime":
                    self.input_is_valid = 1
                    rev_time = float(self.action_selection_array[1])
                    self.music_effects.set_reverb_length(rev_time)
                    self.ambient_sounds_effects.set_reverb_length(rev_time)
                case "e":
                    self.input_is_valid = 1
                    self.music_effects.toggle_delay()
                    self.ambient_sounds_effects.toggle_delay()
                case "ge":
                    self.input_is_valid = 1
                    self.music_effects.toggle_delay()
                case "as":
                    self.input_is_valid = 1
                    self.ambient_sounds_effects.volume_toggle()
                case "time":
                    self.input_is_valid = 1
                    delay = float(self.action_selection_array[1])
                    self.ambient_sounds_effects.change_delay(delay)
                    self.music_effects.change_delay(delay)
                case "v":
                    self.input_is_valid = 1
                    
                    if len(self.action_selection_array) == 3:
                        if (self.action_selection_array[1] != "freq" and self.action_selection_array[1] != "mult"):
                            print("Usage: v [freq or mult] [value]\nExample: v freq 0.1")
                        if self.action_selection_array[1] == "freq":
                            # print("set freq")
                            self.music.pitch_lfo.setFreq(float(self.action_selection_array[2]))
                        elif self.action_selection_array[1] == "mult":
                            # print("set mult")
                            self.music.pitch_lfo.setMul(float(self.action_selection_array[2]))
                    else:
                        print("Usage: v [freq or mult] [value]\nExample: v freq 0.1")

                case "f":
                    self.input_is_valid = 1
                    self.music_effects.filter.setFreq(int(self.action_selection_array[1]))
                    self.ambient_sounds_effects.filter.setFreq(int(self.action_selection_array[1]))
                    
                    if self.music_effects.filter_selector.voice == 0:
                        print("Filter is disabled, run tf to enable it.")

                case "tf":
                    self.input_is_valid = 1

                    if self.music_effects.filter_selector.voice == 0:
                        self.music_effects.filter_selector.setVoice(1)
                    else:
                        self.music_effects.filter_selector.setVoice(0)
                        
                case "tr":
                    self.input_is_valid = 1
                    self.music_effects.toggle_reverb()
                
                case "d":
                    self.input_is_valid = 1

                    if len(self.action_selection_array) != 2:
                        print('Usage: d [detune factor (float) ]\nExample: d 0.1')
                    else:
                        self.music.detune_factor = float(self.action_selection_array[1])
                        self.music.detune = True

                case 'tde':
                    self.input_is_valid = 1

                    self.music.detune = not self.music.detune
                    # print('is detuning?', self.music.detune)
                
                case 'dis':
                    self.input_is_valid = 1
                    self.music_effects.distortion.setDrive(float(self.action_selection_array[1]))
                        
                case "q":
                    self.input_is_valid = 1
                    self.mixer.setMul(0.0)
                    self.music.stop()
                    self.ambient_sounds.stop()
                    print("\nFarewell!\n")
                    time.sleep(1)
                    s.shutdown()
                    sys.exit()
                case _:
                    self.input_is_valid = 0
                    self.action_selection = input("Please enter a valid command: ")
            
            if self.input_is_valid:        
                self.action_selection = input("Enter next command: ")
            self.action_selection_array = self.action_selection.split(' ')
      
main = Main()
s.gui(locals)