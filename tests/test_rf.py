"""Test rf functions."""
import pandas as pd
import rf
import pytest

df = pd.read_csv("~/Duke/821/final_proj/CombinePlayer_data.txt", sep="\t")


def test_get_features() -> None:
    """Test get features."""
    output = rf.get_feature_label(df, [3, 4, 7, 8], 2)
    assert type(output) == tuple, "output not correct."


def test_get_features2() -> None:
    """Test output shape."""
    output = rf.get_feature_label(df, [3, 4, 7, 8], 2)
    assert output[0].shape[0] == output[1].shape[0], "shape not correct."
