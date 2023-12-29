"""This file is reposible for changing csv files separator"""
import os
from pathlib import Path

import pandas as pd


def change_csv_separator(
        path: str, 
        curr_sep_char: str = ",", 
        new_sep_char: str = ";"
    ) -> None:
    "Change columns separator for CSV file"
    df: pd.DataFrame = pd.read_csv(path, sep=curr_sep_char)
    df.to_csv(path, sep=new_sep_char, index=False)


if __name__ == "__main__":
    for file in Path.iterdir(Path(__file__).resolve().parent):
        f_str: str = str(file)
        if f_str.endswith(".csv"):
            change_csv_separator(f_str)
    print("Finished!")y
