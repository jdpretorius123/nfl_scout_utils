# A library for NFL scouts on the move!

## Modules
`nfl_scout_utils.py`
An NFL combine data drocessor and analyzer.

This module places power in the hands that need it most...
NFL scouts! These hardworking folks travel incessantly, are
underpaid, and hardly receive credit when processes go well.
This module allows the scout to store, summarize, and
analyze NFL combine data to speed up their processes and
earn them that well-deserved raise! This tool has components
that are compatible with tab-delimited text (.txt) files.

`rf.py`
A basic machine learning tool for prediction.

This module uses a random forest algorithm to predict player
importance. This tool is compatible with comma-separated-value
(.csv) files.

## Usage: `nfl_scout_utils.py`

### Dependencies
`datetime`
`sqlite3`
`matplotlib`
`seaborn`
`pandas`
`numpy`
`sklearn`
`scipy`

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
```

## Example Usage
```
records = parse_data("player_file.txt", "test_file.txt")
player_id = "John Abraham_2000"
test = "Forty"
year = "2000"
group = "draft_class"

player = records[player_id]
position = player.position
player_score = player.get_score(test)
player_percentile = player.get_percentile(test, year, group)
draft_status = player.was_drafted()
```

Do you have a background in statistics? Do you find exploratory
data analysis to be an essential part of your job? We got you 
covered!

```
var = "Height"
year = "2000"
records = parse_data("player_file.txt", "test_file.txt")
pos = "RB"

barplot(var, year, records, pos)
histogram(var, year, records, pos)
boxplot(var, year, records, pos)

var_two = "Forty"

scatterplot(var, var_two, year, records, pos)

k = 4

kmeans(var, var_two, year, records, k, pos)
```

## Usage: `rf.py`

### Dependencies
`matplotlib`
`pandas`
`numpy`
`sklearn`

## Functions
```
read_data(
    fpath: str
) -> pd.DataFrame:
    Reads in the data.

get_feature_label(
    df: pd.DataFrame,
    feature_cols: list[int],
    label_col: int
) -> tuple[np.darray, np.darray]
    Get feature label matrix.

fit(
    X_train: np.ndarray,
    y_train: np.ndarray,
    n_trees: int,
    loss_fn: str = "entropy"
) -> Any
    Fit the model.

predict(
    newdata: np.ndarray,
    classifier: Any
) -> int
    Predict new person.

visualize(
    y_pred: list[int],
    y_test: list[int]
) -> None
    Visualize output.
```

## Example Usage
```
data = read_data(file_path)

cols = [2,3]
label = 4
matrix = get_feature_label(data, cols, label)

x = matrix[0]
y = matrix[1]
num_trees = 6
classifier = fit(x, y, num_trees)

height = 72
weight = 220
new_player_data = np.array([height, weight])
predicted_label = predict(new_player_data, classifier)
```

## Development
We welcome contributions! Before opening a pull request, 
please confirm that existing tests pass with **at least 
80%coverage**:

```
python -m pytest tests/
```
