"""Test rf functions."""
import pandas as pd
import rf
import pytest

PLAYER_FILE: str = "Pfr_ID\tPlayer\tPos\tHt\tWt\tYear\tTeam\tRound\tPick\n\
John Abraham_2000\tJohn Abraham\tOLB\t76\t252\t2000\tNew York Jets\t1\t13\n\
Shaun Alexander_2000\tShaun Alexander\tRB\t72\t218\t2000\tSeattle Seahawks\t1\t19\n\
Corey Atkins_2000\tCorey Atkins\tOLB\t72\t237\t2000\t\t\t\n"

# initialize.
player_file = "CombinePlayer_data.txt"
players = open(player_file, mode="w", newline="\n")
players.write(PLAYER_FILE)
players.close()
df = pd.read_csv(player_file, sep="\t")


def test_get_features() -> None:
    """Test get features."""
    output = rf.get_feature_label(df, [3, 4, 7, 8], 2)
    assert type(output) == tuple, "output not correct."


def test_get_features2() -> None:
    """Test output shape."""
    output = rf.get_feature_label(df, [3, 4, 7, 8], 2)
    assert output[0].shape[0] == output[1].shape[0], "shape not correct."
