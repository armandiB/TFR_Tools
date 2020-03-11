class Key_Dictionary:
    instrument_str_nbs = {}
    instruments = []
    notes = []

    max_instrument_str_nbs = {}
    max_instruments = -1
    max_notes = -1

    def read_line_update_dictionary(self, line):
        if (not line) or line.startswith('#'):
            return

        tokens = line.split(',')
        if tokens[0] == "instrument_str_nb":
            if tokens[1] in self.instrument_str_nbs.keys():
                self.instrument_str_nbs[tokens[1]].append(int(tokens[2]))
            else:
                self.instrument_str_nbs[tokens[1]] = [int(tokens[2])]
        if tokens[0] == "instrument":
            self.instruments.append(int(tokens[2]))
        if tokens[0] == "note":
            self.notes.append(int(tokens[2]))
        return

    def load_key_dictionary(self, key_dictionary_path):
        dic_file = open(key_dictionary_path, "r")
        for line in dic_file:
            self.read_line_update_dictionary(line.rstrip('\n'))

        dic_file.close()

        self.max_instrument_str_nbs = {
            k: max(v)
            for k, v in self.instrument_str_nbs.items()
        }
        self.max_instruments = max(self.instruments)
        self.max_notes = max(self.notes)

        # Set to empty to fill with new keys
        self.instrument_str_nbs = {}
        self.instruments = []
        self.notes = []
        return

    def write_key_dictionary(self, key_dictionary_path):
        dic_file = open(key_dictionary_path, "a")

        for k, v in self.instrument_str_nbs.items():
            for nb in v:
                dic_file.write("instrument_str_nb," + str(k) + "," + str(nb) +
                               "\n")

        for nb in self.instruments:
            dic_file.write("instrument,," + str(nb) + "\n")

        for nb in self.notes:
            dic_file.write("note,," + str(nb) + "\n")

        dic_file.close()
        return
