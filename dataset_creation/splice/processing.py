import librosa
import math


def splice_extracts_mono(instrument_sound, nb_samples_extract, nb_samples_gap):
    mono_sound = librosa.to_mono(instrument_sound)
    nb_samples = mono_sound.shape[0]
    nb_extracts = math.floor(
        nb_samples / (nb_samples_extract + nb_samples_gap))

    extracts = []
    for i in range(0, nb_extracts):
        begin = i * (nb_samples_extract + nb_samples_gap)
        end = begin + nb_samples_extract
        sound = mono_sound[begin:end]
        norm_sound = librosa.util.normalize(sound)
        extracts.append(norm_sound)

    return extracts, nb_extracts


def resample_extracts(original_extracts, sr_in, sr_out):
    resampled = []
    for extract in original_extracts:
        resampled.append(librosa.resample(extract, sr_in, sr_out))

    return resampled
