import numpy as np
import soundfile
import os
import math
import sounddevice as sd


def get_interface(cfo):
    sd.default.device = cfo.IN_CARD_NAME, cfo.OUT_CARD_NAME
    sd.default.samplerate = cfo.OUT_SAMPLE_RATE
    return


def record_instrument(cfo, parameters_config):
    nb_samples_on = int(cfo.NOTE_ON_SECONDS * cfo.OUT_SAMPLE_RATE)
    nb_samples_off = int(cfo.NOTE_OFF_SECONDS * cfo.OUT_SAMPLE_RATE)
    nb_samples_gap = int(cfo.GAP_SECONDS * cfo.OUT_SAMPLE_RATE)

    note_on = [1] * nb_samples_on
    note_off = [0] * (nb_samples_off + nb_samples_gap)
    note_gate = note_on + note_off
    unit_param = [1] * (nb_samples_on + nb_samples_off + nb_samples_gap)

    _ = sd.rec(frames=10000, channels=len(cfo.IN_CHANS))

    instr_sounds_list = []
    for params in cfo.convert_parameters(parameters_config):
        output_list = [note_gate]
        for param in params:
            output_list += [[param * n for n in unit_param]]
        output = np.array(output_list).T

        print(params)
        sd.wait()
        in_note = sd.playrec(output, input_mapping=cfo.IN_CHANS, output_mapping= cfo.OUT_CHANS)
        instr_sounds_list += [in_note]

    instr_sounds = np.concatenate(instr_sounds_list).T
    return instr_sounds


def write_split_wav(instr_dir_path, instr_name, instr_sound, sample_rate, max_nb_samples=442368000):
    nb_splits = math.ceil(instr_sound.size / max_nb_samples)
    array_list = np.array_split(instr_sound, nb_splits)
    for idx, split in enumerate(array_list):
        soundfile.write(os.path.join(instr_dir_path, instr_name + "_" + str(idx) + "-I.wav"), split, sample_rate,
                    subtype='PCM_24')  # Important to be sorted
    return


def check_tuning(cfo, nb_notes):
    note_on = [1] * int(cfo.OUT_SAMPLE_RATE * (cfo.NOTE_ON_SECONDS + cfo.NOTE_OFF_SECONDS + cfo.GAP_SECONDS))
    output_list = [note_on]
    for param in cfo.default_parameters():
        output_list += [[param * n for n in note_on]]
    output = np.array(output_list).T

    # https://python-sounddevice.readthedocs.io/en/0.3.14/examples.html#play-a-sine-signal

    for _ in range(nb_notes):
        sd.play(output, blocking=True)

    print("Tuning done.")
    return
