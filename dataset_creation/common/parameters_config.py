import librosa
from scipy.stats.mstats import gmean
import numpy as np
import copy

import outboard.params_utils as pa_ut

class ParametersConfig:
    parameters_matrix = []
    repeats = 2

    def __init__(self):
        self.parameters_matrix = []

    def copy(self):
        res = type(self)()
        res.parameters_matrix = copy.deepcopy(self.parameters_matrix)
        return res

    def apply_repeats(self):
        temp = copy.deepcopy(self.parameters_matrix)
        parameters_matrix = []
        for x in temp:
            for n in range(self.repeats):
                parameters_matrix += [x]


class ParametersConfig_NSynth(ParametersConfig):
    # PITCHS = [2*i+1 for i in range(18, 25)]#41)]
    # PITCHS = [5*i for i in range(20,30)]
    PITCHS = range(18, 113)
    # VELOCITIES = [60, 105]
    VELOCITIES = [10, 25, 50, 75, 87, 100, 112, 127]

    def fill_parameters_matrix(self, *unused):
        self.parameters_matrix = []
        # Later: randomize per pitch?
        for i in self.PITCHS:
            for j in self.VELOCITIES:
                self.parameters_matrix.append((i, j))

        self.apply_repeats()
        return

class ParametersConfig_NSynth_2Pitches_absolute(ParametersConfig):
    # PITCHS = [2*i+1 for i in range(18, 25)]#41)]
    # PITCHS = [5*i for i in range(20,30)]
    PITCHS = range(18, 113)
    # VELOCITIES = [60, 105]
    VELOCITIES = range(18, 113)

    def fill_parameters_matrix(self, *unused):
        self.parameters_matrix = []
        # Later: randomize per pitch?
        for i in self.PITCHS:
            for j in self.VELOCITIES:
                if j % 7 == i % 7 or j == i-1 or j == i+1:
                    self.parameters_matrix.append((i, j))

        self.apply_repeats()
        return

class ParametersConfig_NSynth_2Pitches_relative(ParametersConfig):
    # PITCHS = range(18, 113)
    PITCHS = [18] + list(range(30, 95)) + [106]
    # PITCHS = [2*i+1 for i in range(18, 41)]
    VELOCITIES = [-24] + list(range(-12, 13)) + [24]
    # VELOCITIES = [-24, 3, 0, 7, 12]

    def fill_parameters_matrix(self, *unused):
        self.parameters_matrix = []
        # Later: randomize per pitch?
        for i in self.PITCHS:
            for j in self.VELOCITIES:
                self.parameters_matrix.append((i, j+pa_ut.ZERO_NOTE))

        self.apply_repeats()
        return

class ParametersConfig_Tracks(ParametersConfig):
    # Could test pitch = velo, velo = round((x - round(x) + 0.5)*127)
    def fill_parameters_matrix(self, resampled_extracts, sample_rate):
        DIVISOR_FFT = 4

        self.parameters_matrix = []
        nb_extracts = len(resampled_extracts)

        check_notes = False
        for j, extract in enumerate(resampled_extracts):
            freq = librosa.feature.spectral_centroid(extract, sr=sample_rate, n_fft=int(1+len(extract)/DIVISOR_FFT), hop_length=int(1+len(extract)/DIVISOR_FFT)) #use better estimation of pitch
            zeros = np.argwhere(freq==0.0)
            freq = np.delete(freq, zeros)
            i = int(round(librosa.core.hz_to_midi(gmean(freq))))
            if j > 0:
                if stored_note != i:
                    check_notes = True
            stored_note = i
            if j < nb_extracts-1 or check_notes:
                self.parameters_matrix.append((i, int(round(127 * j / (nb_extracts - 1)))))
            else:
                self.parameters_matrix.append((i+1, int(round(127 * j / (nb_extracts - 1)))))

        self.apply_repeats()
        return
