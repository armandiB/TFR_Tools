import os


class Instrument:
    instrument_name = ""

    instrument = None
    instrument_str = ""

    instrument_family = None
    instrument_family_str = ""
    instrument_source = None
    instrument_source_str = ""

    # For now static per instrument
    qualities = []
    qualities_str = []
    sample_rate = None

    def read_line_update_params(self, line, parameters_config_instr=None):
        if (not line) or line.startswith('#'):
            return

        tokens = line.split(',')
        if tokens[0] == 'instrument_source':
            self.instrument_source = int(tokens[1])
        if tokens[0] == 'instrument_family':
            self.instrument_family = int(tokens[1])
        if tokens[0] == 'qualities':
            self.qualities = []
            for b in tokens[1]:
                self.qualities += [int(b)]
        if tokens[0] == 'parameters_matrix' and parameters_config_instr is not None:
            parameters_config_instr.parameters_matrix += [list(map(int, tokens[-1].split(':')))] #Assuming indexes in order
        return

    def fill_instr_keys(self, key_dictionary, out_sample_rate):
        instr_key = self.instrument_family_str + "_" + self.instrument_source_str
        if instr_key in key_dictionary.max_instrument_str_nbs.keys():
            instrument_str_nb = 1 + key_dictionary.max_instrument_str_nbs[
                instr_key]
        else:
            instrument_str_nb = 1000
            key_dictionary.instrument_str_nbs[instr_key] = []
        self.instrument_str = instr_key + "_" + format(instrument_str_nb, '04d')

        self.instrument = 1 + key_dictionary.max_instruments
        self.sample_rate = out_sample_rate

        if instr_key in key_dictionary.instrument_str_nbs.keys():
            key_dictionary.instrument_str_nbs[instr_key].append(
                instrument_str_nb)
        else:
            key_dictionary.instrument_str_nbs[instr_key] = [instrument_str_nb]
        key_dictionary.max_instrument_str_nbs[instr_key] = instrument_str_nb
        key_dictionary.instruments.append(self.instrument)
        key_dictionary.max_instruments = self.instrument
        return


class Note(Instrument):

    note = None
    note_str = ""

    pitch = None
    velocity = None
    brightness = None
    density = None
    pitch2 = None
    lfo_period = None
    tremolo_depth = None
    vibrato_depth = None
    noise_amount = None
    inharmonic_amount = None
    wet_reverb = None
    wet_clocked_delay = None
    distorsion_amount = None

    audio = None

    def set_instrument_params(self, instrument):
        self.instrument_name = instrument.instrument_name
        self.instrument = instrument.instrument
        self.instrument_str = instrument.instrument_str
        self.instrument_family = instrument.instrument_family
        self.instrument_family_str = instrument.instrument_family_str
        self.instrument_source = instrument.instrument_source
        self.instrument_source_str = instrument.instrument_source_str
        # For now static per instrument
        self.qualities = instrument.qualities.copy()
        self.qualities_str = instrument.qualities_str.copy()
        self.sample_rate = instrument.sample_rate

        self.note_str = instrument.instrument_str + "-" + str(
            self.pitch) + "-" + str(self.velocity) + "-" + str(self.brightness) + "-" + str(self.density)
        + "-" + str(self.pitch2) + "-" + str(self.lfo_period) + "-" + str(self.tremolo_depth) + "-" + str(self.vibrato_depth)
        + "-" + str(self.noise_amount) + "-" + str(self.inharmonic_amount) + "-" + str(self.wet_reverb) + "-" + str(self.wet_clocked_delay)
        "-" + str(self.distorsion_amount) + "-" + str(self.note)
        return

    def fill_note_keys(self, key_dictionary):
        self.note = 1 + key_dictionary.max_notes

        key_dictionary.notes.append(self.note)
        key_dictionary.max_notes = self.note
        return

    def make_note_path(self, instrument_path):
        return os.path.join(instrument_path, self.note_str + ".wav")

    def make_json_dict(self):
        json_dict = {}
        json_dict["note"] = self.note
        json_dict["sample_rate"] = self.sample_rate
        json_dict["instrument_family"] = self.instrument_family
        json_dict["qualities"] = self.qualities.copy()
        json_dict["instrument_source_str"] = self.instrument_source_str
        json_dict["note_str"] = self.note_str
        json_dict["instrument_family_str"] = self.instrument_family_str
        json_dict["instrument_str"] = self.instrument_str
        json_dict["instrument"] = self.instrument
        json_dict["pitch"] = self.pitch
        json_dict["velocity"] = self.velocity
        json_dict["brightness"] = self.brightness
        json_dict["density"] = self.density
        json_dict["pitch2"] = self.pitch2
        json_dict["lfo_period"] = self.lfo_period
        json_dict["tremolo_depth"] = self.tremolo_depth
        json_dict["vibrato_depth"] = self.vibrato_depth
        json_dict["noise_amount"] = self.noise_amount
        json_dict["inharmonic_amount"] = self.inharmonic_amount
        json_dict["wet_reverb"] = self.wet_reverb
        json_dict["wet_clocked_delay"] = self.wet_clocked_delay
        json_dict["distorsion_amount"] = self.distorsion_amount
        json_dict["instrument_source"] = self.instrument_source
        json_dict["qualities_str"] = self.qualities_str.copy()

        return json_dict


def make_notes(parameters_matrix):
    notes = []

    for params in parameters_matrix:
        note = Note()
        note.pitch = params[0]
        note.velocity = params[1]
        note.brightness = params[2]
        note.density = params[3]
        note.pitch2 = params[4]
        note.lfo_period = params[5]
        note.tremolo_depth = params[6]
        note.vibrato_depth = params[7]
        note.noise_amount = params[8]
        note.inharmonic_amount = params[9]
        note.wet_reverb = params[10]
        note.wet_clocked_delay = params[11]
        note.distorsion_amount = params[12]
        notes += [note]

    return notes
