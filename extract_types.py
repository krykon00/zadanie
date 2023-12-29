"""Extracting genres from steam.csv file"""
import pandas as pd


def get_uniques(unseparated: list[str], sep: str =";") -> list[str]:
    """Function loops over elements in `unseparated` list 
    and returns list with only uniqe values from every item from list

    Args:
    - unseparated: list with string from where to extract uniques
    - sep: character used to separated values from items in `unseparated` list

    Returns:
    list of unique strings 
    """
    uniques: set[str] = set()
    for item in unseparated:
        for element in item.split(sep=sep):
            uniques.add(element)

    return list(uniques)

if __name__ == "__main__":
    # In below code I extract uniq types of geners and categories to use those two later as filters in dashboard
    df: pd.DataFrame = pd.read_csv("steam.csv", sep=";")
    future_filters: list[str] = ["genres", "categories"]

    games_ids: list[str] = df["appid"].unique()
    # If code is run then for each future_filter a new csv file will be made
    for ff in future_filters:
        ff_df: pd.DataFrame = pd.DataFrame(
            data = {ff: get_uniques(list(df[ff].unique()))}
        )
        ff_df.to_csv(f"{ff}.csv", index=False)
        # Here I extract future_filters for each of individual game for later filtering purposes
        games_unique_types: list[pd.DataFrame] = []
        for g_id in games_ids:
            g_df: pd.DataFrame = df[df["appid"] == g_id]
            uniques_types_for_game: list[str] =  get_uniques(list(g_df[ff].unique()))
            sub_df: pd.DataFrame = pd.DataFrame(
                    data = {
                        "appid": [g_id] * len(uniques_types_for_game),
                        ff: uniques_types_for_game,
                        }
            )
            games_unique_types.append(sub_df)
        
        pd.concat(games_unique_types).to_csv(f"games_{ff}.csv", index=False)

    print("Finished.")
