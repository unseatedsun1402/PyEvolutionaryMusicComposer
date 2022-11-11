import pyaudio
from synthesizer import Player,Synthesizer,Waveform

def main():
    player = Player()
    player.open_stream()
    synth  = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.sine, osc2_volume=0.8, osc2_freq_transpose=2)
    # Play A4
    #player.play_wave(synth.generate_constant_wave(440.0, 1.0))
    chord = ["C3", "E3", "G3"]
    player.play_wave(synth.generate_chord(chord,1))

if __name__ == '__main__':
    main()