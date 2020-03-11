import params_utils as pa_ut


class OutboardConfig:
    OUT_CARD_NAME = 'Aurora' #'ES-8'
    OUT_SCALE_FACTOR = 10
    OUT_CHANS = [1, 2, 3]
    IN_CARD_NAME =  'Aurora' #'ES-8'
    IN_CHANS = [1, 2, 3, 4]

    OUTPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets"

    OUT_SAMPLE_RATE = 48000
    NOTE_ON_SECONDS = 3
    NOTE_OFF_SECONDS = 1
    GAP_SECONDS = 4

    def copy_from_splice(self, cf_splice):
        self.OUTPUT_FOLDER = cf_splice.INPUT_FOLDER
        self.OUT_SAMPLE_RATE = cf_splice.IN_SAMPLE_RATE
        self.NOTE_ON_SECONDS = cf_splice.EXTRACT_SECONDS * 3 / 4
        self.NOTE_OFF_SECONDS = cf_splice.EXTRACT_SECONDS / 4
        self.GAP_SECONDS = cf_splice.GAP_SECONDS

    def convert_parameters(self, *unused):
        pass

    def default_parameters(self):
        pass


class OutboardConfig_NSynth(OutboardConfig):
    OUTPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/NSynth++/Instruments"

    def convert_parameters(self, parameters_matrix):
        converted_matrix = []
        for params in parameters_matrix:
            converted_matrix += [
                [pa_ut.midi_pitch_to_voltage(params[0]) / self.OUT_SCALE_FACTOR,
                params[1] / 127] + params[2:]
            ]
        return converted_matrix

    def default_parameters(self):
        return [0, 0.5]

class OutboardConfig_NSynth_2Pitches(OutboardConfig):
    OUTPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/NSynth++/Instruments"

    def convert_parameters(self, parameters_matrix):
        converted_matrix = []
        for params in parameters_matrix:
            converted_matrix += [
                [pa_ut.midi_pitch_to_voltage(params[0]) / self.OUT_SCALE_FACTOR,
                pa_ut.midi_pitch_to_voltage(params[1]) / self.OUT_SCALE_FACTOR]
                + params[2:]
            ]
        return converted_matrix

    def default_parameters(self):
        return [0.0, 0.0]