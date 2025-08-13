import argparse
import json
import os
import random
from typing import Dict

import numpy as np
import tensorflow as tf
import yaml


def set_seed(seed: int) -> None:
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)


def load_config(path: str) -> Dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    set_seed(42)
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    model = tf.keras.Sequential([
        tf.keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(cfg["learning_rate"]),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(
        x_train,
        y_train,
        epochs=cfg["epochs"],
        batch_size=cfg["batch_size"],
        verbose=0,
    )
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    out_dir = "experiments/examples/ML-EXP-001/results"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "metrics.json"), "w") as f:
        json.dump({"accuracy": float(acc)}, f)
    with open(os.path.join(out_dir, "model_path.txt"), "w") as f:
        f.write("models/mnist_cnn.h5")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train simple CNN on MNIST")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
