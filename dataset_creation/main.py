import splice.do_splice as do_sp
import splice.config_splice as cf_sp
import outboard.do_outboard as do_ob
import outboard.config_outboard as cf_ob
import outboard.instrument_config as ic
import common.parameters_config as param_conf

Instrument_Config = ic.InstrumentConfig_ModularTest()
Outboard_Config = cf_ob.OutboardConfig_NSynth_2Pitches()
Splice_Config = cf_sp.SpliceConfig_NSynth()
Parameters_Config = param_conf.ParametersConfig_NSynth_2Pitches_relative()

# Splice_Config.IN_SAMPLE_RATE = 44100
Splice_Config.INPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/NSynth++/Instruments/tmp"

# Outboard_Config.IN_CHANS = [1, 2]

Instrument_Config.instrument_family = 9
Instrument_Config_List = [Instrument_Config.copy() for _ in range(len(Outboard_Config.IN_CHANS))]
# Instrument_Config_List[0].qualities[5] = 1

Outboard_Config.copy_from_splice(Splice_Config)
Parameters_Config.fill_parameters_matrix()

# Record check_tuning
# Parameters as arguments check_tuning
do_ob.check_tuning(Outboard_Config, 2)

# prepare_instrument (do_outboard read mode different config)
do_ob.do_outboard(Outboard_Config, Parameters_Config, "Experiment1", "Lead", Instrument_Config_List, mode='r')

# Changes qualities num instruments INSIDE
do_ob.do_outboard(Outboard_Config, Parameters_Config, "Experiment1", "Lead", Instrument_Config_List, mode='w')

# Transfer paths to do_splice, or flag onlyToday

Splice_Config.OUT_SAMPLE_RATE = 32000
# Format zeros json
do_sp.do_splice(Splice_Config, Parameters_Config, write_in_place=True, only_today=True, write_key_dictionary=True)
