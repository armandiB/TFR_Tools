import soundfile
import os
import datetime

import file_handling as fh
import processing as pr
import note as nt
import key_dictionary as kd
import tfrecord_utils as tf_ut


def do_splice(cf, parameters_config, write_in_place=True, only_today=False, write_key_dictionary=True):
    instr_paths, instr_names = fh.get_instrument_paths(cf.INPUT_FOLDER, cf.IN_SAMPLE_RATE, only_today=only_today)
    key_dictionary = kd.Key_Dictionary()
    key_dictionary.load_key_dictionary(cf.KEY_DICTIONARY_PATH)

    tfrecord_path_list = []
    for original_instr_name in instr_names:
        # instr_name: Date_SampleRate_Species_Genus
        instr_name_split = original_instr_name.split('_')
        in_sample_rate = int(instr_name_split[1])
        if in_sample_rate != cf.IN_SAMPLE_RATE:
            print('Instrument at ' + original_instr_name + ': file name sample rate does not match conf IN_SAMPLE_RATE '
                  + str(cf.IN_SAMPLE_RATE))

        instr_name = instr_name_split[0] + '_' + str(
            cf.OUT_SAMPLE_RATE) + '_' + '_'.join(instr_name_split[2:])

        parameters_config_instr = parameters_config.copy()

        instr_sound = fh.load_sound(instr_paths[original_instr_name], in_sample_rate)
        instr_params = fh.load_instr_params(instr_paths[original_instr_name], instr_name, parameters_config_instr)
        instr_params.fill_instr_keys(key_dictionary, cf.OUT_SAMPLE_RATE)

        nb_samples_extract = int(cf.EXTRACT_SECONDS * in_sample_rate)
        nb_samples_gap = int(cf.GAP_SECONDS * in_sample_rate)

        original_extracts, nb_extracts = pr.splice_extracts_mono(
            instr_sound, nb_samples_extract, nb_samples_gap)
        resampled_extracts = pr.resample_extracts(
            original_extracts, in_sample_rate, cf.OUT_SAMPLE_RATE)

        if len(parameters_config_instr.parameters_matrix) == 0:
            parameters_config_instr.fill_parameters_matrix(resampled_extracts, cf.OUT_SAMPLE_RATE)

        notes = nt.make_notes(parameters_config_instr.parameters_matrix)

        if write_in_place:
            instr_output_path = fh.make_instr_path_mkdir(instr_name, os.path.dirname(instr_paths[original_instr_name][0]))
        else:
            instr_output_path = fh.make_instr_path_mkdir(instr_name, cf.OUTPUT_FOLDER)

        if len(notes) != len(resampled_extracts):
            print("Mismatch number of extracts for " + instr_name)
            print(str(len(notes)) + ", " + str(len(resampled_extracts)))

        for note, sound in zip(notes, resampled_extracts):
            note.set_instrument_params(instr_params)
            note.fill_note_keys(key_dictionary)

            note_path = note.make_note_path(instr_output_path)
            soundfile.write(note_path, sound, note.sample_rate, subtype='PCM_16')

            note.audio = sound

        fh.write_json_instrument(notes, instr_output_path)
        tfrecord_path = tf_ut.write_tfrecord_instrument(notes, instr_output_path)
        tfrecord_path_list += [tfrecord_path]

    if write_key_dictionary:
        key_dictionary.write_key_dictionary(cf.KEY_DICTIONARY_PATH)

    if len(instr_names) > 1:
        tf_ut.append_tfrecords(
            tfrecord_path_list,
            os.path.join(
                cf.OUTPUT_FOLDER,
                datetime.datetime.today().strftime('%Y%m%d') + "_" + str(cf.OUT_SAMPLE_RATE) + "_" +
                cf.__class__.__name__ + "_combined.tfrecord"))
    return

'''
tf_ut.append_tfrecords([r'/Volumes/GLYPHAB/Datasets/NSynth++/20190617_Debug_Datasets/20190703_32000_Config_NSynth_combined_9instr.tfrecord',
                        r'/Volumes/GLYPHAB/Datasets/NSynth++/20190814_NewExperiments_Datasets/20190814_32000_Config_NSynth_Experiments1and2_8instr.tfrecord']
                       , os.path.join(r'/Volumes/GLYPHAB/Datasets/NSynth++/20190814_NewExperiments_Datasets',
                        '20190814_32000_Config_NSynth_combined_17instr' + ".tfrecord"))
'''