import pandas as pd

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

if __name__ == "__main__":
    print(get_local_tickers())
