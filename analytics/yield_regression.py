import argparse
import json

import pandas as pd
from sklearn.linear_model import LinearRegression


def main(input_csv: str, report_path: str) -> None:
    df = pd.read_csv(input_csv)
    X = df[["x"]]
    y = df["y"]
    model = LinearRegression().fit(X, y)
    result = {
        "coef": float(model.coef_[0]),
        "intercept": float(model.intercept_),
    }
    with open(report_path, "w") as f:
        json.dump(result, f)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Yield regression example")
    parser.add_argument("input_csv")
    parser.add_argument("report_path")
    args = parser.parse_args()
    main(args.input_csv, args.report_path)
