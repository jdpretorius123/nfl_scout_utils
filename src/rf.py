"""basic machine learning."""

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


def visualize(y_pred, y_test) -> None:
    """Visualize output."""
    conf_mtx = confusion_matrix(y_test, y_pred, normalize="all")
    show = plt.imshow(conf_mtx)
    bar = plt.colorbar(show)
    plt.show()


def main():
    """Do things."""
    fpath = "~/Duke/821/final_proj/CombinePlayer_data.txt"
    df = read_data(fpath)

    input = get_feature_label(df, [3, 4, 7, 8], 1)
    splited_data = train_test_split(input[0], input[1], test_size=0.25, random_state=7)

    classifier = fit(splited_data[0], splited_data[2], 10)
    y_pred = predict(splited_data[1], classifier)
    visualize(y_pred, splited_data[3])


if __name__ == "__main__":
    main()
