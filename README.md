# TFR_Tools
Tool for tensorflow dataset generation with modular synths

dataset_creation package:
- outboard is for use with an external soundcard, plays a grid of parameters and simultaneously records the sound.
- splice is able to cut one or several long recordings into data points, resample, and compile into json/wav and tfrecord datasets.

soundcard package by bastibe not being used except in deprecated io_old (fails on newer Macs for me). sounddevice is used instead.
