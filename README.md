# A library for NFL scouts on the move!

## Modules
player_utils -- This module is gives NFL scouts the power to 
perform basic operations with their scouting data, such as probing 
player information and making one-to-one or one-to-many player 
comparisons. This tool accepts tab-delimited text (.txt) files.

## Usage
This script requires `datetime` and `sqlite3` and contains the 
following classes and functions.

## Classes
```
Player
Test
```

## Functions
```
parse_data(
    player_filename: str,
    test_filename: str
) -> dict[str, Player]:
    Parse and return test history for players
```

## Example Usage
```
records = parse_data("player_file.txt", "test_file.txt")

player_id = "John Abraham_2000"
test_name = "40 Yard Dash"

player = records[player_id]
position = player.position
player_score = player.get_score(test_name)
player_percentile = player.get_percentile(test_name)
```

Have you found an exciting new prospect? Do you want to 
compare them to past players? We got you covered!

```
player_id = "Anthony Richardson_2023"
test_name = "Vertical"
test_value = "41"

player = records[player_id]
kmeans_result = kmeans(test_name, test_value)
```

## Development
We welcome contributions! Before opening a pull request, 
please confirm that existing tests pass with **at least 
80%coverage**:

```
python -m pytest tests/
```
