import datetime
import os

import outboard.io as io
import splice.file_handling as fh
import outboard.instrument_config as i_conf


def check_tuning(cfo, seconds): 
    io.get_interface(cfo)
    io.check_tuning(cfo, seconds)
    return


def calibrate_pitch_offset(cfo):
    return


def do_outboard(cfo, parameters_config, instrument_species, instrument_genus, iconf_list, mode='w'):
    io.get_interface(cfo)
    print("CHECK INTERFACES SAMPLE RATE.")

    instr_sounds = io.record_instrument(cfo, parameters_config)
    instr_sounds_list = list(instr_sounds)

    if isinstance(iconf_list, type(i_conf.InstrumentConfig)):
        iconf_list = [iconf_list.copy() for _ in range(len(instr_sounds_list))]

    for num, instr_sound in enumerate(instr_sounds_list):
        instr_dir_path = fh.make_instr_path_mkdir(
            datetime.datetime.today().strftime('%Y%m%d') + "_" +
            instrument_species + str(num) + "_" + instrument_genus,
            cfo.OUTPUT_FOLDER)
        instr_name = datetime.datetime.today().strftime('%Y%m%d') + "_" + str(cfo.OUT_SAMPLE_RATE) + "_" + instrument_species \
                     + str(num) + "_" + instrument_genus

        if mode == 'w':
            io.write_split_wav(instr_dir_path, instr_name, instr_sound, cfo.OUT_SAMPLE_RATE)
            iconf_list[num].write_P(os.path.join(instr_dir_path, instr_name + "_P.csv"), parameters_config.parameters_matrix, cfo.__class__.__name__, parameters_config.__class__.__name__)
    return