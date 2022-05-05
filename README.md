# ECG Lead Reversal

![intro](https://i.imgur.com/ey6SYR6.png)

The ECG is a time series that measures the electrical activity of the heart. This is the main tool to diagnose heart diseases. 

Recording an ECG is simple: 3 electrodes are placed at the ends of limbs, and 6 on the anterior chest.This generates **12 time series**, called leads, each corresponding to a difference in potential between a pair of electrodes.
The electrodes' position is very important to correctly interpret the ECG. Making the mistake of inverting electrodes compromises interpretation, either because the leads do not explore the expected area (errors in the measures of hypertrophia indices, in the analysis of the ST segment), or because they generate false abnormalities (fake Q waves, error in the heart's axis...).

Inversion errors are frequent (5% of ECGs), and only experts (cardiologists) manage to detect them. But most ECGs are not interpreted by experts: only 30% are, the rest being interpreted by nurses or general practitioners. An algorithm for automatic detection of electrode inversion is therefore paramount to the correct interpretation of ECGs  and would improve the quality of diagnosis.

This project uses convolutional neural networks to automatically detect electrode inversion in an ECG with an accuracy >96%.
Results were tested on more than 2500 ECG records.

## Usage

Dockerfile is provided for training
```shell
$ docker build -f Dockerfile --rm --tag ecg_reversal .
$ docker run -u $(id -u) --gpus all -it -v /home/imag2/External_Projects/ECG_Lead_Reversal:/tf -p 8888:8888 -p 6006:6006 --rm --name lr ecg_reversal:latest
```

## System Requirements

[TensorFlow](https://www.tensorflow.org) 2.8

[Docker](https://www.docker.com) CE 20.10.3 with [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker) for GPU acceleration

Tested with RTX3090 and Intel i9-10900k

## Contacts

For any inquiries please contact: 
[Alessandro Delmonte](https://aledelmo.github.io) @ [alessandro.delmonte@institutimagine.org](mailto:alessandro.delmonte@institutimagine.org)

## License

This project is licensed under the [Apache License 2.0](LICENSE) - see the [LICENSE](LICENSE) file for
details
