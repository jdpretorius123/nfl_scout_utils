"""
NFL Combine Data Processor and Analyzer.

This module places power in the hands that need it most...
NFL scouts! These hardworking folks travel incessantly, are
underpaid, and hardly receive credit when processes go well.
This module allows the scout to store, summarize, and
analyze NFL combine data to speed up their processes and
earn them that well-deserved raise! This tool is compatible 
with tab-delimited text (.txt) files.

Dependencies
------------
datetime
sqlite3
matplotlib
seaborn
pandas
numpy
sklearn
scipy

Classes
-------
Player
Test

Functions
---------
parse_data(
    player_filename: str,
    test_filename: str
) -> dict[str, Player]:
    Parse and return performance test history for players

barplot(
    var: str,
    year: str,
    records: dict[str, Player],
    pos: str | None = None
) -> pd.DataFrame:
    Return bar plot of variable average (of position) by draft status.

histogram(
    var: str,
    year: str,
    records: dict[str, Player],
    pos: str | None = None
) -> pd.DataFrame:
    Return histogram of `var` (of position) by draft status.

boxplot(
    var: str,
    year: str,
    records: dict[str, Player],
    pos: str | None = None
) -> pd.DataFrame:
    Return boxplot of `var` (of position) by draft status.

scatterplot(
    var_one: str,
    var_two: str,
    year: str,
    records: dict[str, Player],
    pos: str | None = None
) -> pd.DataFrame:
    Return scatter plot of `var_one` by `var_two` (of position) by draft status.

kmeans(
    var_one: str,
    var_two: str,
    year: str,
    records: dict[str, Player],
    k: int,
    pos: str | None = None
) -> pd.DataFrame:
    Return KMeans plot of `var_one` by `var_two` (of position).
"""

from datetime import *  # type: ignore
from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull
from scipy import interpolate
from matplotlib.lines import Line2D  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import pandas as pd  # type: ignore
import numpy as np
import sqlite3


class Test:
    """
    A class to represent a performance test.

    Attributes
    ----------
    test_id -- a string denoting the test's id

    Methods
    -------
    __init__(self, test_id)
        Construct all attributes for Test class.

        Arguments
        ---------
        test_id -- a string denoting the test's id

        Return
        -------
        None

    test_id
        The Test ID property.

    player_id
        The Test player ID property.

    name
        The Test name property.

    value
        The Test value property.

    year
        The Test year property.
    """

    def __init__(self, test_id: str) -> None:
        """
        Construct all attributes for Test class.

        Arguments
        ---------
        test_id -- a string denoting the test's id

        Return
        -------
        None
        """
        self.test_id = test_id

    @property
    def test_id(self) -> str:
        """The Test ID property."""
        return self._test_id

    @test_id.setter
    def test_id(self, id: str) -> None:
        if isinstance(id, str):
            self._test_id = id
        else:
            raise ValueError('"id" must be a string')

    @property
    def player_id(self) -> str:
        """The Test player ID poperty."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT PlayerID FROM Tests WHERE TestID=?
            """,
            (self.test_id,),
        )
        self._player_id = str(result.fetchall()[0][0])
        connection.close()
        return self._player_id

    @property
    def name(self) -> str:
        """The Test name property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Name FROM Tests WHERE TestID=?
            """,
            (self.test_id,),
        )
        self._name = str(result.fetchall()[0][0])
        connection.close()
        return self._name

    @property
    def value(self) -> str:
        """The Test value property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Value FROM Tests WHERE TestID=?
            """,
            (self.test_id,),
        )
        temp = str(result.fetchall()[0][0])
        connection.close()
        if temp == "":
            self._value = "DNP"
        else:
            self._value = temp
        return self._value

    @property
    def year(self) -> str:
        """The Test year property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Year FROM Tests WHERE TestID=?
            """,
            (self.test_id,),
        )
        self._year = str(result.fetchall()[0][0])
        connection.close()
        return self._year


class Player:
    """
    A class to represent a player.

    Attributes
    ----------
    id -- a string denoting the player's id

    Methods
    -------
    __init__(self, id)
        Construct all attributes for Player class.

        Arguments
        ---------
        id -- a string denoting the player's id

        Return
        ------
        None

    id
        The Player ID property.

    name
        The Player name property.

    pos
        The Player position property.

    ht
        The Player height property.

    wt
        The Player weight property.

    team
        The Player team property.

    round
        The Player draft round property.

    pick
        The Player draft pick property.

    year
        The Player draft year property.

    get_tests(self)
        Return the player's performance test history.

        Time Complexity
        ---------------
        O(N)
        N -- the number of performance tests taken by the player

        Arguments
        ---------
        None

        Return
        ------
        list[Test]
            instances of the Test class, where each instance
            is a recorded performance test for the player

    add_test(self, test)
        Add test to player's performance test history.

        Arguments
        ---------
        test -- an instance of the Test class denoting one
            performance test taken by the player

        Return
        ------
        None

    was_drafted(self)
        Return the player's draft status.

        Time Complexity
        ---------------
        O(1) total

        Arguments
        ---------
        None

        Return
        ------
        bool
            the player's draft status:
                True if player was drafted
                False if otherwise

    get_score(self, test_name: str)
        Return player's score for one performance test.

        Time Complexity
        ---------------
        O(N) total
        N -- number of performance tests taken by player

        Arguments
        ---------
        test_name -- a string denoting the name of a performance test

        Return
        -------
        str
            player's score for the performance test

    get_percentile(self, test_name: str, year: str, group: str)
        Return the player's percentile for a performance test.

        Time Complexity
        ---------------
        O(N) total
        N -- number of players in player's draft class

        Arguments
        ---------
        test_name -- a string denoting the name of a performance test
        year -- a string denoting the year
        group -- a string denoting the level of analysis:
            1. draft_class, or
            2. pos_group

        Return
        -------
        str
            the player's percentile for a performance test relative to
            an entire draft class or their position group from any year
    """

    def __init__(self, id: str) -> None:
        """
        Construct all attributes for Player class.

        Arguments
        ---------
        id -- a string denoting the player's id

        Return
        ------
        None
        """
        self.id = id
        self.tests: list[Test] = []

    @property
    def id(self) -> str:
        """The Player ID property."""
        return self._id

    @id.setter
    def id(self, id: str) -> None:
        if isinstance(id, str):
            self._id = id
        else:
            raise ValueError('"id" must be a string')

    @property
    def name(self) -> str:
        """The Player name property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Name FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        self._name = str(result.fetchall()[0][0])
        connection.close()
        return self._name

    @property
    def pos(self) -> str:
        """The Player position property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Pos FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        self._pos = str(result.fetchall()[0][0])
        connection.close()
        return self._pos

    @property
    def ht(self) -> str:
        """The Player height property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Ht FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        self._ht = str(result.fetchall()[0][0])
        connection.close()
        return self._ht

    @property
    def wt(self) -> str:
        """The Player weight property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Wt FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        self._wt = str(result.fetchall()[0][0])
        connection.close()
        return self._wt

    @property
    def team(self) -> str:
        """The Player team property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Team FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        temp = str(result.fetchall()[0][0])
        connection.close()
        if temp == "":
            self._team = "Undrafted"
        else:
            self._team = temp
        return self._team

    @property
    def round(self) -> str:
        """The Player draft round property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Round FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        temp = str(result.fetchall()[0][0])
        connection.close()
        if temp == "":
            self._round = "Undrafted"
        else:
            self._round = temp
        return self._round

    @property
    def pick(self) -> str:
        """The Player draft pick property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Pick FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        temp = str(result.fetchall()[0][0])
        connection.close()
        if temp == "":
            self._pick = "Undrafted"
        else:
            self._pick = temp
        return self._pick

    @property
    def year(self) -> str:
        """The Player draft year property."""
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            """
            SELECT Year FROM Players WHERE ID=?
            """,
            (self.id,),
        )
        self._year = str(result.fetchall()[0][0])
        connection.close()
        return self._year

    def get_tests(self) -> list[Test]:
        """
        Return the player's performance test history.

        Time Complexity
        ---------------
        O(N)
        N -- the number of performance tests taken by the player

        Arguments
        ---------
        None

        Return
        ------
        list[Test]
            instances of the Test class, where each instance
            is a recorded performance test for the player
        """
        return self.tests  # O(n)

    def add_test(self, test: Test) -> None:
        """
        Add test to player's performance test history.

        Arguments
        ---------
        test -- an instance of the Test class denoting one
            performance test taken by the player

        Return
        ------
        None
        """
        self.get_tests().append(test)

    def was_drafted(self) -> bool:
        """
        Return the player's draft status.

        Time Complexity
        ---------------
        O(1) total

        Arguments
        ---------
        None

        Return
        -------
        bool
            the player's draft status:
                True if player was drafted
                False if otherwise
        """
        draft_status = self.team
        if draft_status != "Undrafted":
            return True
        return False

    def get_score(self, test_name: str) -> str:
        """
        Return player's score for one performance test.

        Time Complexity
        ---------------
        O(N) total
        N -- number of performance tests taken by player

        Arguments
        ---------
        test_name -- a string denoting the name of a performance test

        Return
        -------
        str
            player's score for the performance test
        """
        score = ""
        tests = self.get_tests()[:]  # O(n)
        for test in tests:  # O(n)
            if test.name == test_name:
                score = test.value
        return score

    def get_percentile(
        self, test_name: str, year: str, group: str
    ) -> float | str:
        """
        Return the player's percentile for a performance test.

        Time Complexity
        ---------------
        O(M+N+O) total
        M -- number of performance tests taken by player
        N -- number of players in player's draft class or position group
        O -- number of players in player's draft class with
            recorded score for peformance test

        Assumptions
        -----------
        1. N will be greater than or equal to O

        Arguments
        ---------
        test_name -- a string denoting the name of a performance test
        year -- a string denoting the year
        group -- a string denoting the level of analysis:
            1. draft_class, or
            2. pos_group

        Return
        -------
        str
            the player's percentile for a performance test relative to
            an entire draft class or their position group from any year
        """
        score_str = self.get_score(test_name)  # O(m)
        if score_str == "DNP":
            return self.name + " did not take this performance test!"

        score_float = float(score_str)
        connection = sqlite3.connect("Combine_database.db")
        cursor = connection.cursor()

        if group != "draft_class":
            result = cursor.execute(
                """
                SELECT Value FROM Tests WHERE Name=? AND Year=?
                AND Pos=?
                """,
                (
                    test_name,
                    year,
                    self.pos,
                ),
            )  # O(n)
        else:
            result = cursor.execute(
                """
                SELECT Value FROM Tests WHERE Name=? AND Year=?
                """,
                (
                    test_name,
                    year,
                ),
            )  # O(n)
        values: list[str] = list(result.fetchall())  # O(n)
        connection.close()
        good_values: list[float] = [
            float(value[0]) for value in values if value[0] != ""
        ]  # O(o)
        count = 0
        for value in good_values:  # O(o)
            if value >= score_float:
                count += 1
        percentile = round((count / len(good_values)) * 100, 2)
        return percentile


def parse_data(player_filename: str, test_filename: str) -> dict[str, Player]:
    """
    Parse and return performance test history for players.

    Time Complexity
    ---------------
    O(QR+ST) total
    Q - number of lines in player_filename
    R - number of columns per line in player_filename
    S - number of lines in test_filename
    T - number of columns per line in test_filename

    Assumptions
    -----------
    1.  Only input is tab-delimited .txt files.
    2.  There is adherence to order of positional arguments when calling
        function.

    Arguments
    ---------
    player_filename --  a string denoting the .txt file with scouting
        information for players
    test_filename -- a string denoting the .txt file with scouting
        information for players' performance tests

    Return
    -------
    dict[str, PLAYER]
        keys -- unique Player IDs
        values -- instances of Player class with all performance test history
                  readily accessible
    """
    player_infile = open(player_filename, "r")
    player_vars = player_infile.readline()
    player_var_list = player_vars.split("\t")  # O(r)
    player_var_list[-1] = player_var_list[-1].strip()
    players = player_infile.readlines()  # O(qr)
    player_infile.close()

    player_dict: dict[str, Player] = {}

    connection = sqlite3.connect("Combine_database.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Players")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Players(ID TEXT, Name TEXT, Pos TEXT,
        Ht TEXT, Wt TEXT, Year TEXT, Team TEXT, Round TEXT, Pick TEXT)
        """
    )

    for aline in players:  # O(q)
        player = aline.split("\t")  # O(r)
        player[-1] = player[-1].strip()

        temp: dict[str, str] = dict(zip(player_var_list, player))  # O(r)
        pfr_id = temp["Pfr_ID"]
        player_dict[pfr_id] = Player(pfr_id)

        cursor.execute(
            """
            INSERT INTO Players(ID, Name, Pos, Ht, Wt, Year,
            Team, Round, Pick) VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                pfr_id,
                temp["Player"],
                temp["Pos"],
                temp["Ht"],
                temp["Wt"],
                temp["Year"],
                temp["Team"],
                temp["Round"],
                temp["Pick"],
            ),
        )

    test_infile = open(test_filename, "r")
    test_vars = test_infile.readline()
    test_var_list = test_vars.split("\t")  # O(t)
    test_var_list[-1] = test_var_list[-1].strip()
    tests = test_infile.readlines()  # O(st)
    test_infile.close()

    cursor.execute("DROP TABLE IF EXISTS Tests")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Tests(TestID TEXT,
        PlayerID TEXT, Pos TEST, Name TEXT, Value TEXT,
        Year TEXT)
        """
    )

    for aline in tests:  # O(s)
        test = aline.split("\t")  # O(t)
        test[-1] = test[-1].strip()

        temp_t: dict[str, str] = dict(zip(test_var_list, test))  # O(t)
        test_id = temp_t["Pfr_ID"] + "_" + temp_t["Test"]

        cursor.execute(
            """
            INSERT INTO Tests(TestID, PlayerID, Pos,
            Year, Name, Value) VALUES(?,?,?,?,?,?)
            """,
            (
                test_id,
                temp_t["Pfr_ID"],
                temp_t["Pos"],
                temp_t["Year"],
                temp_t["Test"],
                temp_t["Value"],
            ),
        )

        player_test = Test(test_id)
        player_dict[temp_t["Pfr_ID"]].add_test(player_test)

    connection.commit()
    connection.close()
    records = player_dict
    return records


def barplot(
    var: str, year: str, records: dict[str, Player], pos: str | None = None
) -> pd.DataFrame:
    """
    Return bar plot of `var` average (of position) by draft status.

    Time Complexity
    ---------------

    Arguments
    ---------
    var -- a string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    year -- a string denoting the year
    records -- a dictionary:
        keys -- player IDs
        values -- instances of Player class
    pos -- an optional string denoting position group

    Return
    -------
    pd.DataFrame
        column names:
            "Draft Status"
                datatype: string/categorical
            Name of variable passed to `var` argument
                datatype: float64/numeric
    """
    traits: dict[str, str] = {"Height": "ht", "Weight": "wt"}
    tests: list[str] = [
        "Forty",
        "Vertical",
        "BenchReps",
        "BroadJump",
        "Cone",
        "Shuttle",
    ]
    dataframe: pd.DataFrame = pd.DataFrame(columns=["Draft Status", var])
    group = list(records.values())

    if pos is not None:
        players: list[Player] = [
            player
            for player in group
            if player.year == year and player.pos == pos
        ]
    else:
        players = [player for player in group if player.year == year]

    for player in players:
        if var not in tests:
            value = getattr(player, traits[var])
        else:
            value = getattr(player, "get_score")(var)
        if value != "DNP":
            if player.was_drafted():
                dataframe.loc[len(dataframe.index)] = [  # type: ignore
                    "Drafted",
                    float(value),
                ]
            else:
                dataframe.loc[len(dataframe.index)] = [  # type: ignore
                    "Undrafted",
                    float(value),
                ]

    barplot = dataframe.groupby(["Draft Status"], as_index=False).mean()

    plt.figure(figsize=(8, 4), tight_layout=True)  # type: ignore
    colors = sns.color_palette("pastel")
    plt.bar(barplot["Draft Status"], barplot[var], color=colors[:2])

    if pos is not None:
        title_str = f"Average {var} by Draft Status for {pos}"
    else:
        title_str = f"Average {var} by Draft Status"

    plt.title(title_str)
    plt.xlabel("Draft Status")
    plt.ylabel = f"Average {var}"
    plt.show()

    return barplot


def histogram(
    var: str, year: str, records: dict[str, Player], pos: str | None = None
) -> pd.DataFrame:
    """
    Return histogram of `var` (of position) by draft status.

    Time Complexity
    ---------------

    Arguments
    ---------
    var -- a string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    year -- a string denoting the year
    records -- a dictionary:
        keys -- player IDs
        values -- instances of Player class
    pos -- an optional string denoting position group

    Return
    -------
    pd.DataFrame
        column names:
            "Draft Status"
                datatype: string/categorical
            Name of variable passed to `var` argument
                datatype: float64/numeric
    """
    traits: dict[str, str] = {"Height": "ht", "Weight": "wt"}
    tests: list[str] = [
        "Forty",
        "Vertical",
        "BenchReps",
        "BroadJump",
        "Cone",
        "Shuttle",
    ]
    data_frame: pd.DataFrame = pd.DataFrame(columns=["Draft Status", var])
    group = list(records.values())

    if pos is not None:
        players: list[Player] = [
            player
            for player in group
            if player.year == year and player.pos == pos
        ]
    else:
        players = [player for player in group if player.year == year]

    for player in players:
        if var not in tests:
            value = getattr(player, traits[var])
        else:
            value = getattr(player, "get_score")(var)
        if value != "DNP":
            if player.was_drafted():
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Drafted", float(value)]  # type: ignore
            else:
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Undrafted", float(value)]  # type: ignore

    plt.figure(figsize=(10, 6), tight_layout=True)  # type: ignore
    ax = sns.histplot(
        data=data_frame,
        x=var,
        hue="Draft Status",
        palette="Set2",
        linewidth=2,
    )

    if pos is not None:
        title_str = f"{var} by Draft Status for {pos}"
    else:
        title_str = f"{var} by Draft Status"

    ax.set(
        title=title_str,
        xlabel=var,
        ylabel="Frequency",
    )
    plt.show()

    return data_frame



def boxplot(
    var: str, year: str, records: dict[str, Player], pos: str | None = None
) -> pd.DataFrame:
    """
    Return boxplot of `var` (of position) by draft status.

    Time Complexity
    ---------------
    
    Arguments
    ---------
    var -- a string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    year -- a string denoting the year
    records -- a dictionary:
        keys -- player IDs
        values -- instances of Player class
    pos -- an optional string denoting position group

    Return
    -------
    pd.DataFrame
        column names:
            "Draft Status"
                datatype: string/categorical
            Name of variable passed to `var` argument
                datatype: float64/numeric
    """
    traits: dict[str, str] = {"Height": "ht", "Weight": "wt"}
    tests: list[str] = [
        "Forty",
        "Vertical",
        "BenchReps",
        "BroadJump",
        "Cone",
        "Shuttle",
    ]
    data_frame: pd.DataFrame = pd.DataFrame(columns=["Draft Status", var])
    group = list(records.values())

    if pos is not None:
        players: list[Player] = [
            player
            for player in group
            if player.year == year and player.pos == pos
        ]
    else:
        players = [player for player in group if player.year == year]

    for player in players:
        if var not in tests:
            value = getattr(player, traits[var])
        else:
            value = getattr(player, "get_score")(var)
        if value != "DNP":
            if player.was_drafted():
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Drafted", float(value)]  # type: ignore
            else:
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Undrafted", float(value)]  # type: ignore

    plt.figure(figsize=(10, 6), tight_layout=True)  # type: ignore
    ax = sns.boxplot(
        data=data_frame,
        x="Draft Status",
        y=var,
        palette="Set2",
        linewidth=2.5,
    )

    if pos is not None:
        title_str = f"{var} by Draft Status for {pos}"
    else:
        title_str = f"{var} by Draft Status"

    ax.set(
        title=title_str,
        xlabel="Draft Status",
        ylabel=var,
    )
    plt.show()

    return data_frame


def scatterplot(
    var_one: str, var_two: str, year: str, records: dict[str, Player], pos: str | None = None
) -> pd.DataFrame:
    """
    Return scatter plot of `var_one` by `var_two` (of position) by draft status.

    Time Complexity
    ---------------
    
    Arguments
    ---------
    var_one -- a string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    var_two -- string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    year -- a string denoting the year
    records -- a dictionary:
        keys -- player IDs
        values -- instances of Player class
    pos -- an optional string denoting position group

    Return
    -------
    pd.DataFrame
        column names:
            "Draft Status"
                datatype: string/categorical
            Name of variable passed to `var` argument
                datatype: float64/numeric
    """
    traits: dict[str, str] = {"Height": "ht", "Weight": "wt"}
    tests: list[str] = [
        "Forty",
        "Vertical",
        "BenchReps",
        "BroadJump",
        "Cone",
        "Shuttle",
    ]
    data_frame: pd.DataFrame = pd.DataFrame(columns=["Draft Status", var_one, var_two])
    group = list(records.values())

    if pos is not None:
        players: list[Player] = [
            player
            for player in group
            if player.year == year and player.pos == pos
        ]
    else:
        players = [player for player in group if player.year == year]

    for player in players:
        if var_one not in tests:
            val_one = getattr(player, traits[var_one])
        else:
            val_one = getattr(player, "get_score")(var_one)
        if var_two not in tests:
            val_two = getattr(player, traits[var_two])
        else:
            val_two = getattr(player, "get_score")(var_two)

        if val_one != "DNP" and val_two != "DNP":
            if player.was_drafted():
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Drafted", float(val_one), float(val_two)]  # type: ignore
            else:
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Undrafted", float(val_one), float(val_two)]  # type: ignore

    plt.figure(figsize=(10, 6), tight_layout=True)  # type: ignore
    ax = sns.scatterplot(
        data=data_frame,
        x=var_one,
        y=var_two,
        hue="Draft Status",
        palette="Set2",
        s=60,
    )

    if pos is not None:
        title_str = f"{pos} Draft Status"
    else:
        title_str = "Draft Status"

    ax.set(
        xlabel=var_one,
        ylabel=var_two,
    )
    ax.legend(
        title=title_str,
        title_fontsize=12
    )
    plt.show()

    return data_frame


def kmeans(
    var_one: str,
    var_two: str,
    year: str,
    records: dict[str, Player],
    k: int,
    pos: str | None = None 
) -> pd.DataFrame:
    """
    Return KMeans plot of `var_one` by `var_two` (of position).

    Time Complexity
    ---------------
    
    Arguments
    ---------
    var_one -- a string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    var_two -- string denoting a physical trait or performance test
        Acceptable Parameters:
        1. Height
        2. Weight
        3. Forty
        4. BenchReps
        5. BroadJump
        6. Vertical
        7. Shuttle
        8. Cone
    year -- a string denoting the year
    records -- a dictionary:
        keys -- player IDs
        values -- instances of Player class
    k -- an integer denoting the number of clusters to be created
    pos -- an optional string denoting position group

    Return
    -------
    pd.DataFrame
        column names:
            "Draft Status"
                datatype: string/categorical
            Name of variable passed to `var` argument
                datatype: float64/numeric
    """
    traits: dict[str, str] = {"Height": "ht", "Weight": "wt"}
    tests: list[str] = [
        "Forty",
        "Vertical",
        "BenchReps",
        "BroadJump",
        "Cone",
        "Shuttle",
    ]
    data_frame: pd.DataFrame = pd.DataFrame(columns=["Draft Status", "Pos", var_one, var_two])
    group = list(records.values())
    if pos is not None:
        players: list[Player] = [
            player
            for player in group
            if player.year == year and player.pos == pos
        ]
    else:
        players = [player for player in group if player.year == year]

    for player in players:
        if var_one not in tests:
            val_one = getattr(player, traits[var_one])
        else:
            val_one = getattr(player, "get_score")(var_one)
        if var_two not in tests:
            val_two = getattr(player, traits[var_two])
        else:
            val_two = getattr(player, "get_score")(var_two)

        if val_one != "DNP" and val_two != "DNP":
            if player.was_drafted():
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Drafted", player.pos, float(val_one), float(val_two)]  # type: ignore
            else:
                data_frame.loc[
                    len(data_frame.index)
                ] = ["Undrafted", player.pos, float(val_one), float(val_two)]  # type: ignore
    
    num_clusters = list(range(k))
    kmeans = KMeans(n_clusters=len(num_clusters), random_state=0)
    data_frame["Cluster"] = kmeans.fit_predict(
        data_frame[[var_one, var_two]]
    )

    centroids = kmeans.cluster_centers_
    centroid_x = [c[0] for c in centroids]
    centroid_y = [c[1] for c in centroids]

    data_frame["Centroid_X"] = data_frame.Cluster.map(
        dict(zip(num_clusters, centroid_x))
    )
    data_frame["Centroid_Y"] = data_frame.Cluster.map(
        dict(zip(num_clusters, centroid_y))
    )
    colors = sns.color_palette("pastel") # + sns.color_palette("Set2")
    colors = colors[:len(num_clusters)]

    data_frame["Color"] = data_frame.Cluster.map(
        dict(zip(num_clusters, colors))
    )

    fig,ax = plt.subplots(1, figsize=(8,8))
    plt.scatter(
        data_frame[var_one],
        data_frame[var_two],
        c = data_frame.Color,
        alpha = 0.6,
        s=10
        )
    plt.scatter(
        centroid_x,
        centroid_y,
        marker="^",  # type: ignore
        c=colors,
        s=70
    )

    for cluster in data_frame.Cluster.unique():
        points = data_frame[data_frame.Cluster == cluster][
            [var_one, var_two]
        ].values
        hull = ConvexHull(points)
        x_hull = np.append(
            points[hull.vertices, 0],
            points[hull.vertices,0][0]
        )
        y_hull = np.append(
            points[hull.vertices,1],
            points[hull.vertices,1][0]
        )
        dist = np.sqrt(
            (x_hull[:-1] - x_hull[1:])**2
            + (y_hull[:-1] - y_hull[1:])**2
        )
        dist_along = np.concatenate(([0], dist.cumsum()))
        spline,u = interpolate.splprep(
            [x_hull, y_hull],
            u=dist_along,
            s=0,
            per=1
        )
        interp_d = np.linspace(
            dist_along[0],
            dist_along[-1],
            50
        )
        interp_x, interp_y = interpolate.splev(
            interp_d, spline
        )
        plt.fill(
            interp_x,
            interp_y,
            "--",
            c=colors[cluster],
            alpha=0.2
        )

    legend_elements=[
        Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label="Cluster {}".format(i+1),
        markerfacecolor=mcolor,
        markersize=10
        ) for i, mcolor in enumerate(colors)
        ]
    plt.legend(
        handles=legend_elements,
        loc="upper left",
        ncol = 1
    )

    if pos is not None:
        title_str = f"KMeans: {var_one} by {var_two} for {pos} in {year} Draft Class"
    else:
        title_str = f"KMeans: {var_one} by {var_two} for {year} Draft Class"

    plt.title(title_str)
    plt.xlabel(var_one)
    plt.ylabel(var_two)
    plt.show()
    return data_frame
