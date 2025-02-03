import os
import sys

import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
print(f"project root: {project_root}")
sys.path.insert(0, project_root)  # This does not work, idk why


def get_local_tickers():
    """
    This function get the tickers gathered in the df_stocks.csv stored
    in data/
    """
    df = pd.read_csv("data/df_stocks.csv")
    tickers = list(df["Ticker"].unique())
    # print(tickers.shape)
    # print(tickers[0])
    # tickers.replace(' ', ',')
    return tickers


def get_index():
    """
    This functions gatheres all the indexes available in df_index.csv
    stored in data/
    """
    df = pd.read_csv(os.path.join(project_root, "data/df_index.csv"))
    index = list(df["Ticker"].unique())
    print(f"number of indexes: {len(index)}")
    return index


def get_tickers_from_index(index):
    """
    This function returns all the tickers belonging to a given index
    """
    df_index = pd.read_csv(os.path.join(project_root, "data/df_index.csv"))
    df_stocks = pd.read_csv(
        os.path.join(project_root, "data/df_stocks.csv"), low_memory=False
    )
    # df_stocks = pd.read_csv("data/df_stocks.csv", low_memory=False)
    exchange = df_index[df_index["Ticker"] == index]["Exchange"].values[0]
    tickers = list(df_stocks[df_stocks["Exchange"] == exchange]["Ticker"])
    return tickers


if __name__ == "__main__":
    # get_local_tickers()
    # get_index()
    tickers = get_tickers_from_index("^AEX")
    print(tickers)
