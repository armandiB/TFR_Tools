import tensorflow as tf
import os

import splice.note as nt


def _bytes_feature(value):
    return tf.train.Feature(
        bytes_list=tf.train.BytesList(value=[value.encode()]))


def _bytes_list_feature(value):
    return tf.train.Feature(
        bytes_list=tf.train.BytesList(value=[v.encode() for v in value]))


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def serialize_note(note):
    note_features = {
        'sample_rate': _int64_feature(note.sample_rate),
        'qualities_str': _bytes_list_feature(note.qualities_str),
        'note_str': _bytes_feature(note.note_str),
        'qualities': _int64_list_feature(note.qualities),
        'audio': _float_list_feature(note.audio),
        'instrument_family': _int64_feature(note.instrument_family),
        'pitch': _int64_feature(note.pitch),
        'instrument_source': _int64_feature(note.instrument_source),
        'instrument_str': _bytes_feature(note.instrument_str),
        'instrument_source_str': _bytes_feature(note.instrument_source_str),
        'note': _int64_feature(note.note),
        'instrument': _int64_feature(note.instrument),
        'instrument_family_str': _bytes_feature(note.instrument_family_str),
        'velocity': _int64_feature(note.velocity)
    }

    example_proto = tf.train.Example(
        features=tf.train.Features(feature=note_features))
    return example_proto.SerializeToString()


def write_tfrecord_instrument(notes, instr_output_path):
    file_name = notes[0].instrument_name + ".tfrecord"
    file_path = os.path.join(instr_output_path, file_name)
    writer = tf.io.TFRecordWriter(file_path)

    for note in notes:
        example = serialize_note(note)
        writer.write(example)

    writer.close()
    return file_path


def append_tfrecords(list_paths, output_path):
    output_instr_list_path = output_path.replace('.tfrecord', '_I.csv')
    instr_list = []
    if os.path.isfile(output_instr_list_path):
        with open(output_instr_list_path, 'r') as instr_list_reader:
            for line in instr_list_reader:
                instr_list += [line.rstrip('\n')]

    instr_list_writer = open(output_instr_list_path, 'a')

    writer = open(output_path, 'ab')
    for instr_path in list_paths:
        instr_names = []
        potential_I_path = instr_path.replace('.tfrecord', '_I.csv')
        if os.path.exists(potential_I_path):
            with open(potential_I_path, 'r') as potential_I_reader:
                for line in potential_I_reader:
                    instr_names += [line.rstrip('\n')]

            with open(instr_path, 'rb') as infile:
                writer.write(infile.read())

            for instr_name in instr_names:
                if instr_name in instr_list:
                    print('Wrote duplicate instrument ' + instr_name + ' from ' + instr_path)

                instr_list_writer.write(instr_name + "\n")
                instr_list += [instr_name]
        else:
            instr_name = os.path.split(instr_path)[1].replace('.tfrecord', '')
            if instr_name in instr_list:
                print('Passed duplicate instrument '+instr_name+' for '+instr_path)
                continue

            with open(instr_path, 'rb') as infile:
                writer.write(infile.read())

            instr_list_writer.write(instr_name + "\n")
            instr_list += [instr_name]

    writer.close()
    instr_list_writer.close()
    return


def read_tfrecord(path):
    notes_list = []
    record_iterator = tf.python_io.tf_record_iterator(path=path)

    for string_record in record_iterator:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        feat = example.features.feature

        note = nt.Note()

        note.sample_rate = int(feat['sample_rate'].int64_list.value[0])
        note.audio = list(feat['audio'].float_list.value)
        notes_list += [note]

    return notes_list
