class SpliceConfig:
    INPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets"
    OUTPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets"
    KEY_DICTIONARY_PATH = r"/Volumes/GLYPHAB/Datasets/Key_Dictionary.csv"

    IN_SAMPLE_RATE = 48000
    OUT_SAMPLE_RATE = 48000
    EXTRACT_SECONDS = 4
    GAP_SECONDS = 4


class SpliceConfig_NSynth(SpliceConfig):
    INPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/NSynth++/Instruments"
    OUTPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/NSynth++"

class SpliceConfig_Tracks(SpliceConfig):
    INPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/Textures_From_Tracks/Instruments"
    OUTPUT_FOLDER = r"/Volumes/GLYPHAB/Datasets/Textures_From_Tracks/Instruments"
    IN_SAMPLE_RATE = 48000
    GAP_SECONDS = -3
