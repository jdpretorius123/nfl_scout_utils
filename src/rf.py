"""Basic machine learning.

Dependencies
------------
matplotlib
pandas
numpy
sklearn

Functions
---------
rf.read_data(fpath: str) -> pd.DataFrame:
    Reads in data.

rf.get_feature_label(
    parsed_data: pd.DataFrame,
    feature_cols: list[int],
    label_col: int
) -> tuple(pd.DataFrame, pd.DataFrame)
    Returns tuple of feature matrix and label vector.

rf.fit(
    X: pd.DataFrame,
    y: pd.DataFrame,
    n_trees: int,
    loss_fun: "MSE",
    random_seed = None:
) -> RandomForestClassifier
    Trains model.

rf.visualize(
    y_pred: list[int],
    y_true: list[int],
    style = "confusion": str
) -> None:
    Visualizes classification performance.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


def read_data(fpath: str) -> pd.DataFrame:
    """Read in the data."""
    df = pd.read_csv(fpath, sep="\t")
    factor = pd.factorize(df["Pos"])
    df.Pos = factor[0]
    return df


def get_feature_label(
    df: pd.DataFrame, feature_cols: list[int], label_col: int
) -> tuple[np.ndarray, np.ndarray]:
    """Get feature and label matrix."""
    df_clean = df.dropna()
    X = df_clean.iloc[:, feature_cols].values
    y = df_clean.iloc[:, label_col].values
    print("feature shape: " + str(X.shape))
    print("label shape: " + str(y.shape))
    return (X, y)


def fit(X_train, y_train, n_trees, loss_fn="entropy"):
    """Fit the model."""
    classifier = RandomForestClassifier(
        n_estimators=n_trees,
        criterion=loss_fn,  # loss function
        random_state=7,  # set seed
    )
    classifier.fit(X_train, y_train)
    return classifier


def predict(newdata, classifier):
    """Predict a new person."""
    return classifier.predict(newdata)


def main():
    """Do things."""
    fpath = "./CombinePlayer_data.txt"
    df = read_data(fpath)

    input = get_feature_label(df, [3, 4, 7, 8], 1)
    classifier = fit(input[0], input[1], 10)
    new_data = input[0]
    output = predict(new_data, classifier)


if __name__ == "__main__":
    main()
