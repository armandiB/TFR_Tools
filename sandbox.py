import tensorflow as tf

json_path = r"/GLYPHAB/Datasets/Textures_From_Tracks/Test/Chihei_Hatakeyama_Void_XII/wav_json/examples_promisedland_synthetic_1000.json"
json_path = r"/Users/armandbernardi/Downloads/test.txt"

json_string = tf.io.read_file(json_path)
json_tensor = tf.io.decode_json_example(json_string)

param_file = open(json_path, "r")
for line in param_file.readlines():
    print(line)

param_file.close()

i=0