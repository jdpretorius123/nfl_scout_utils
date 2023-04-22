"""
Basic machine learning on multiclass prediction.

The module provides functionalities to predict a player's
position in a team given specified informations about this
player. This module allows users to read, specify features
of interest, and make predictions on any new data. This 
module is compatible with both .txt files and .csv files.

Dependencies
------------
matplotlib
pandas
numpy
sklearn

rf.get_feature_label(
    parsed_data: pd.DataFrame,
    feature_cols: list[str],
    label_col: str
) -> tuple(pd.DataFrame, pd.DataFrame)
    Returns tuple of feature matrix and label vector

rf.fit(
    X: pd.DataFrame,
    y: pd.DataFrame,
    n_trees: int,
    loss_fun: "MSE",
    random_seed = None:
) -> RandomForestClassifier
    Trains model

rf.visualize(
    y_pred: list[int],
    y_true: list[int],
    style = "confusion": str
) -> None:
    Visualizes classification performance
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from typing import Any


def read_data(fpath: str) -> pd.DataFrame:
    """
    Reads in the data.

    Arguments
    ---------
    fpath: str of data directory.

    Return
    ------
    pd.DataFrame.
    """
    df = pd.read_csv(fpath, sep="\t")
    factor = pd.factorize(df["Pos"])
    df.Pos = factor[0]
    return df


def get_feature_label(
    df: pd.DataFrame, feature_cols: list[int], label_col: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Get feature and label matrix.

    Arguments
    ---------
    df: output of read_data(fpath).
    feature_cols: column indicies that contains features
    desired to be used for prediction.
    label_cols: column index that specify the label in
    the data.


    Return
    ------
    tuple[np.ndarray, np.ndarray]: tuple of feature matrix
    and label vector.
    """
    df_clean = df.dropna()
    X = df_clean.iloc[:, feature_cols].values
    y = df_clean.iloc[:, label_col].values
    print("feature shape: " + str(X.shape))
    print("label shape: " + str(y.shape))
    return (X, y)


def fit(X_train, y_train, n_trees, loss_fn="entropy") -> Any:
    """
    Fit the model.

    Arguments
    ---------
    X_train, y_train: first 2 elements from train_test_split()
    funciton.
    n_trees: number of trees to optimize.
    loss_fn: loss function to be implemented.

    Return
    ------
    A random forest classifier.
    """
    classifier = RandomForestClassifier(
        n_estimators=n_trees,
        criterion=loss_fn,  # loss function
        random_state=7,  # set seed
    )
    classifier.fit(X_train, y_train)
    return classifier


def predict(newdata, classifier) -> int:
    """
    Predict a new person.

    Arguments
    ---------
    new_data: 2d array of informations for new players.
    classifier: classifier to be used for prediction.

    Return
    ------
    int: predicted label.
    """
    return classifier.predict(newdata)


def visualize(y_pred, y_test) -> None:
    """
    Visualize output.

    Arguments
    ---------
    y_pred: list of predicted labels.
    y_test: list of true labels.

    Return
    ------
    None.
    """
    conf_mtx = confusion_matrix(y_test, y_pred, normalize="all")
    show = plt.imshow(conf_mtx)
    bar = plt.colorbar(show)
    plt.show()


def main():
    """Do things."""
    fpath = "~/Duke/821/final_proj/CombinePlayer_data.txt"
    df = read_data(fpath)
    input = get_feature_label(df, [3, 4, 7, 8], 2)
    splited_data = train_test_split(
        input[0], input[1], test_size=0.25, random_state=7
    )

    # model fit
    classifier = fit(splited_data[0], splited_data[2], 10)

    # test new data (one sample)
    new_data = np.array([[70, 200, 1, 13]])
    pred = predict(new_data, classifier)
    print(
        f"A new player with Ht = {new_data[0][0]}, Wt = {new_data[0][1]}, Round = {new_data[0][2]} and Pick = {new_data[0][3]} is predicted to be in position {pred}"
    )
    print(df.head())

    # visualize performance
    y_pred = predict(splited_data[1], classifier)
    visualize(y_pred, y_test=splited_data[3])


if __name__ == "__main__":
    main()
