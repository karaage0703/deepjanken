#!/bin/bash

sudo ~/deepjanken/deepjanken_ommf2018_miku.py --model_path ~/retrained_graph.binaryproto --label_path ~/retrained_labels.txt --input_height 160 --input_width 160 --input_layer input --output_layer final_result
