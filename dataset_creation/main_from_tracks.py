import os

import do_splice as do_sp
import config_splice as cf_sp
import Common.parameters_config as param_conf
import tfrecord_utils as tf_ut

Splice_Config = cf_sp.SpliceConfig_Tracks()
Parameters_Config = param_conf.ParametersConfig_Tracks()

Splice_Config.INPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/Textures_From_Tracks/Instruments"

Splice_Config.IN_SAMPLE_RATE = 44100
Splice_Config.OUT_SAMPLE_RATE = 32000
Splice_Config.GAP_SECONDS = 1

do_sp.do_splice(Splice_Config, Parameters_Config, write_in_place=True, only_today=False, write_key_dictionary=False)


'''
tf_ut.append_tfrecords([r'/Volumes/GLYPHAB/Datasets/Textures_From_Tracks/Instruments/20190707_onelargeroseI_niblock/20190707_32000_onelargeroseI_niblock/20190707_32000_onelargeroseI_niblock.tfrecord',
                        r'/Volumes/GLYPHAB/Datasets/Textures_From_Tracks/Instruments/20190707_onelargeroseII_niblock/20190707_32000_onelargeroseII_niblock/20190707_32000_onelargeroseII_niblock.tfrecord']
                       , os.path.join(r'/Volumes/GLYPHAB/Datasets/Textures_From_Tracks',
                        '20190709_32000_Config_Tracks_touchstrings2instr_niblock' + ".tfrecord"))
'''