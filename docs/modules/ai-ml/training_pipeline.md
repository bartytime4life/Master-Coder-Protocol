# Training Pipeline

Pseudo-code:

1. Load config.
2. Prepare MNIST dataset.
3. Build CNN.
4. Train with given hyperparameters.
5. Save metrics to `experiments/examples/ML-EXP-001/results/metrics.json`.

Run with:
```
python ml/train_cnn.py --config experiments/examples/ML-EXP-001/config/cnn_config.yaml
```

Ensure seeds are fixed for reproducibility.
