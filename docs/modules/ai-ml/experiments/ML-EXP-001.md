# Experiment ML-EXP-001: MNIST CNN

**Hypothesis:** A small CNN can reach ≥99% accuracy on MNIST.

**Config:** lr=0.001, epochs=5, batch=128
**Environment:** TensorFlow 2.x, seed=42

| Metric | Value |
|--------|-------|
| Accuracy | 0.991 |

Confusion matrix shows misclassifications mostly between 5 and 3.

Overfit risk is low but monitor for larger datasets.

**Next Steps:** add dropout, attempt CIFAR-10.
