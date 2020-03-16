class InstrumentConfig:
    instrument_source = None
    instrument_family = None
    qualities = [0] * 24

    def write_P(self, P_path, parameters_matrix, config_outboard_name, parameters_config_name):
        P_file = open(P_path, "x")
        P_file.write("#Type,Value\n")
        P_file.write("instrument_source," + str(self.instrument_source) + "\n")
        P_file.write("instrument_family," + str(self.instrument_family) + "\n")

        P_file.write("qualities," + ''.join([str(b) for b in self.qualities]) + "\n")

        P_file.write("config_outboard_name," + config_outboard_name + "\n")
        P_file.write("parameters_config_name," + parameters_config_name + "\n")
        for idx, params in enumerate(parameters_matrix):
            P_file.write("parameters_matrix," + str(idx) + "," + ':'.join([str(p) for p in params]) + "\n")

        P_file.close()
        return

    def copy(self):
        res = type(self)()
        res.instrument_source = self.instrument_source
        res.instrument_family = self.instrument_family
        res.qualities = self.qualities.copy()
        return res

class InstrumentConfig_ModularTest(InstrumentConfig):
    instrument_source = 1
    instrument_family = 9
