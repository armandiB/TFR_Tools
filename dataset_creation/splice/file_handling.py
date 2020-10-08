import librosa
import os
import json
import numpy as np
import datetime
import soundfile

import splice.note as nt
import splice.tables as tb


def get_instrument_paths(input_folder, sr, only_today=False):
    instrument_paths = {}
    for r, d, f in os.walk(input_folder):
        for name in f:
            if '.asd' not in name and name[0] != '.':
                if '-T.wav' in name:
                    sound, _ = librosa.load(os.path.join(r, name), sr=sr)
                    soundfile.write(os.path.join(r, name.replace("-T.wav", "-I.wav")), sound, sr, subtype='PCM_24')

    for r, d, f in os.walk(input_folder):
        for name in f:
            if '.asd' not in name and name[0] != '.':
                if '-I.wav' in name:
                    instrument_name = '_'.join(name.split('_')[:-1])
                    if (not only_today) or (datetime.datetime.today().strftime('%Y%m%d') in instrument_name):
                        if instrument_name in instrument_paths.keys():
                            instrument_paths[instrument_name].append(os.path.join(r, name))
                        else:
                            instrument_paths[instrument_name] = [os.path.join(r, name)]

    return instrument_paths, instrument_paths.keys()  # ToDo clean


def load_sound(instrument_path_list, sr):
    sound_list = []
    for instrument_path in sorted(instrument_path_list):
        sound, _ = librosa.load(instrument_path, sr=sr)
        sound_list += [sound]

    final_sound = np.concatenate(sound_list)
    return final_sound


def load_instr_params(instr_path, instr_name, parameters_config_instr=None):
    instr_params_path = '_'.join(instr_path[0].split('_')[:-1])
    instr_params_path += "_P.csv"
    instr_params = nt.Instrument()
    instr_params.instrument_name = instr_name

    param_file = open(instr_params_path, "r")
    for line in param_file:
        instr_params.read_line_update_params(line.rstrip('\n'), parameters_config_instr)

    param_file.close()

    instr_params.instrument_source_str = tb.source_to_str[instr_params.instrument_source]
    instr_params.instrument_family_str = tb.family_to_str[instr_params.instrument_family]

    instr_params.qualities_str = []
    for i, b in enumerate(instr_params.qualities):
        if b == 1:
            instr_params.qualities_str.append(tb.qualities_idx_to_str[i])

    return instr_params


def make_instr_path_mkdir(instr_name, output_folder):
    instrument_path = os.path.join(output_folder, instr_name)
    if not os.path.exists(instrument_path):
        os.mkdir(instrument_path)

    return instrument_path


def write_json_instrument(notes, instr_output_path):
    file_name = notes[0].instrument_name + ".json"
    writer = open(os.path.join(instr_output_path, file_name), 'w')

    instr_json_dict = {}
    for note in notes:
        instr_json_dict[note.note_str] = note.make_json_dict()

    json.dump(instr_json_dict, writer, indent=2)
    writer.close()
    return

def copy_tracks_make_P():
  return
