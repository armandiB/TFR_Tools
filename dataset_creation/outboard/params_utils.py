ZERO_NOTE = 69

def midi_pitch_to_voltage(pitch):
    # 440Hz at 0V
    return (pitch - ZERO_NOTE) / 12
