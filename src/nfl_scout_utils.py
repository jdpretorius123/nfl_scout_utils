"""
NFL Combine Data Processor and Analyzer.

This module places power in the hands that need it most...
NFL scouts! These hardworking folks travel incessantly, are
underpaid, and hardly receive credit when processes go well.
This module allows the scout to store, summarize, and
analyze NFL combine data to speed up their processes and
earn them that well-deserved raise! This tool has components
that are compatible with tab-delimited text (.txt) files and
comma-separated-value (.csv) files.

Dependencies
------------
datetime
sqlite3

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
"""

from datetime import *  # type: ignore
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

        Arguments
        ---------
        None

        Return
        ------
        list[Test]
            instances of the Test class, where each instance
            is a recorded performance test for the player
        """
        return self.tests

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
    player_var_list = player_vars.split("\t")
    player_var_list[-1] = player_var_list[-1].strip()
    players = player_infile.readlines()
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

    for aline in players:
        player = aline.split("\t")
        player[-1] = player[-1].strip()

        temp: dict[str, str] = dict(zip(player_var_list, player))
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
    test_var_list = test_vars.split("\t")
    test_var_list[-1] = test_var_list[-1].strip()
    tests = test_infile.readlines()
    test_infile.close()

    cursor.execute("DROP TABLE IF EXISTS Tests")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Tests(TestID TEXT,
        PlayerID TEXT, Pos TEST, Name TEXT, Value TEXT,
        Year TEXT)
        """
    )

    for aline in tests:
        test = aline.split("\t")
        test[-1] = test[-1].strip()

        temp_t: dict[str, str] = dict(zip(test_var_list, test))
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
