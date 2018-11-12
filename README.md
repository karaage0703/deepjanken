# deepjanken
Deep Janken is AI Janken game which Japanese traditional game like "Rock-paper-scissors"

# Dependency


# Setup

# Usage
## Learning AI Model
See References

## Test on Vision Kit
Execute following command on Vision Kit:
```sh
$ ~/AIY-projects-python/src/examples/vision/mobilenet_based_classifier.py --model_path ~/retrained_graph.binaryproto --label_path ~/retrained_labels.txt --input_height 160 --input_width 160 --input_layer input --output_layer final_result --preview
```

## Deep Janken on Vision Kit
Execute following command on Vision Kit for download script:
```
$ cd && wget https://raw.githubusercontent.com/karaage0703/deepjanken/master/deepjanken.py
```

Execute following command:
```sh
$ ~/deepjanken.py --model_path ~/retrained_graph.binaryproto --label_path ~/retrained_labels.txt --input_height 160 --input_width 160 --input_layer input --output_layer final_result
```

 "Deep Janken" will starts

# Licence
This software is released under the Apache License 2.0 License, see LICENSE.


# Authors
- karaage0703
- [googlecodelabs](https://github.com/googlecodelabs) (retrain.py)

# References
- https://aiyprojects.withgoogle.com/vision/#makers-guide
- https://github.com/googlecodelabs/tensorflow-for-poets-2
