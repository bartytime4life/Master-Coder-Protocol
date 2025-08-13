# Model Card: ML-MODEL-001

## Overview
CNN trained on MNIST to 99.1% accuracy.

## Intended Use / Limitations
Digit classification; not for handwriting outside MNIST distribution.

## Training and Evaluation Data
MNIST v1.

## Metrics
Accuracy: 0.991

## Ethical Considerations & Risks
Minimal; dataset is sanitized.

## Training Details
Framework: TensorFlow 2.x
Hardware: CPU
Seed: 42

## Artifacts / URIs
Model: `models/mnist_cnn.h5`

## Changelog
- v1.0 initial release.
