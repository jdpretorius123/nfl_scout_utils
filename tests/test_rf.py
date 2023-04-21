"""Test rf functions."""
import pandas as pd
import rf
import pytest

df = pd.read_csv("~/Duke/821/final_proj/CombinePlayer_data.txt", sep="\t")


def test_get_features() -> None:
    """Test get features."""
    output = rf.get_feature_label(df, [3,4,7,8], 1)
    assert type(output) == tuple, "output not correct."
