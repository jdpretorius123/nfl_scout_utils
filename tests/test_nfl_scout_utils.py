"""
Unit tests for nfl_scout_utils.py.

This module allows the user to perform units tests on the
functions and class properties and methods in `nfl_scout_utils`.

Dependencies
------------
nfl_scout_utils
os

Functions
---------
test_parse_data() -> None:
    Test the processing of NFL combine data for players.

test_get_score() -> None:
    Test the accessing of player's performance test results.
"""


from nfl_scout_utils import *
import os


PLAYER_FILE: str = "Pfr_ID\tPlayer\tPos\tHt\tWt\tYear\tTeam\tRound\tPick\n\
John Abraham_2000\tJohn Abraham\tOLB\t76\t252\t2000\tNew York Jets\t1\t13\n\
Shaun Alexander_2000\tShaun Alexander\tRB\t72\t218\t2000\tSeattle Seahawks\t1\t19\n\
Corey Atkins_2000\tCorey Atkins\tOLB\t72\t237\t2000\t\t\t\n"			


TEST_FILE: str = "Pfr_ID\tPos\tYear\tTest\tValue\n\
John Abraham_2000\tOLB\t2000\tForty\t4.55\nJohn Abraham_2000\tOLB\t2000\tVertical\t\n\
John Abraham_2000\tOLB\t2000\tBenchReps\t\nJohn Abraham_2000\tOLB\t2000\tBroadJump\t\n\
John Abraham_2000\tOLB\t2000\tCone\t\nJohn Abraham_2000\tOLB\t2000\tShuttle\t\n\
Shaun Alexander_2000\tRB\t2000\tForty\t4.58\nShaun Alexander_2000\tRB\t2000\tVertical\t\n\
Shaun Alexander_2000\tRB\t2000\tBenchReps\t\nShaun Alexander_2000\tRB\t2000\tBroadJump\t\n\
Shaun Alexander_2000\tRB\t2000\tCone\t\nShaun Alexander_2000\tRB\t2000\tShuttle\t\n\
Corey Atkins_2000\tOLB\t2000\tForty\t4.72\nCorey Atkins_2000\tOLB\t2000\tVertical\t31\n\
Corey Atkins_2000\tOLB\t2000\tBenchReps\t21\nCorey Atkins_2000\tOLB\t2000\tBroadJump\t112\n\
Corey Atkins_2000\tOLB\t2000\tCone\t7.96\nCorey Atkins_2000\tOLB\t2000\tShuttle\t4.39\n"

def test_parse_data() -> None:
    """
    Test parse_data().

    Test the processing of NFL combine data for players.

    Arguments
    ---------
    None

    Return
    -------
    None
    """
    # setup
    player_file = "CombinePlayer_data.txt"
    players = open(player_file, mode="w", newline="\n")
    players.write(PLAYER_FILE)
    players.close()

    test_file = "CombineTest_data.txt"
    tests = open(test_file, mode="w", newline="\n")
    tests.write(TEST_FILE)
    tests.close()

    player_id = "John Abraham_2000"
    true_pos = "OLB"
    true_ht = "76"
    true_wt = "252"
    true_year = "2000"

    # run
    records = parse_data(player_file, test_file)

    os.remove(player_file)
    os.remove(test_file)

    player = records[player_id]
    test_pos = player.pos
    test_ht = player.ht
    test_wt = player.wt
    test_year = player.year

    # assert
    assert test_pos == true_pos
    assert test_ht == true_ht
    assert test_wt == true_wt
    assert test_year == true_year


def test_get_score() -> None:
    """
    Test get_score().

    Test the accessing of player's performance test results.

    Arguments
    ---------
    None

    Return
    -------
    None
    """
    # setup
    player_file = "CombinePlayer_data.txt"
    players = open(player_file, mode="w", newline="\n")
    players.write(PLAYER_FILE)
    players.close()

    test_file = "CombineTest_data.txt"
    tests = open(test_file, mode="w", newline="\n")
    tests.write(TEST_FILE)
    tests.close()

    player_id = "John Abraham_2000"
    test = "Forty"
    true_score = "4.55"

    # run
    records = parse_data(player_file, test_file)

    os.remove(player_file)
    os.remove(test_file)

    player = records[player_id]
    test_score = player.get_score(test)

    # assert
    assert test_score == true_score

def test_get_percentile() -> None:
    """
    Test get_percentile().

    Test the calculation of a player's percentile for a performance test
    by their position group or an entire draft class from any year.

    Arguments
    ---------
    None

    Return
    -------
    None
    """
    # setup
    player_file = "CombinePlayer_data.txt"
    players = open(player_file, mode="w", newline="\n")
    players.write(PLAYER_FILE)
    players.close()

    test_file = "CombineTest_data.txt"
    tests = open(test_file, mode="w", newline="\n")
    tests.write(TEST_FILE)
    tests.close()

    player_id = "John Abraham_2000"
    test = "Forty"
    year = "2000"
    group = "draft_class"
    true_percentile = 100.0

    # run
    records = parse_data(player_file, test_file)

    os.remove(player_file)
    os.remove(test_file)

    player = records[player_id]
    test_percentile = player.get_percentile(test, year, group)

    # assert
    assert test_percentile == true_percentile
    