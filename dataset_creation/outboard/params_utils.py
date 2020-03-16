ZERO_NOTE = 69

def midi_pitch_to_voltage(pitch):
    # 440Hz at 0V
    return (pitch - ZERO_NOTE) / 12

def pitch2_class_to_freq(int_class):
    return