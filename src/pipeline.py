"""_summary_
Here I will generate the pipeline that should be done
"""

import json
import os

from src.aux.utils import DotDict
from src.dbmanager import DbManager
from src.get_local_tickers import get_index, get_local_tickers, get_tickers_from_index
from src.telegram_manager import TelegramManager
from src.yfmanager import Yfmanager


def local_pipeline(telegram=False):

    config_file = "config.json"

    with open(config_file) as f:
        config = DotDict(json.load(f))
        print(config)

    index_list = get_index()
    index_list = ["^AEX"]
    print(index_list)

    for index in index_list:
        companies_list = get_tickers_from_index(index)
        # Then we should download the data from yfinance
        yfmanager = Yfmanager(config=config)
        df = yfmanager.download_companies_yf(companies=companies_list)
        if not os.path.exists(os.path.join("data", index)):
            os.mkdir(os.path.join("data", index))

        df.to_csv(os.path.join("data", index, index + ".csv"))


def pipeline(db=False, telegram=False):

    config_file = "config.json"

    with open(config_file) as f:
        config = DotDict(json.load(f))
        print(config)

    if db:
        db = DbManager()

        # First we should get a list with the companies from de DB
        companies_list = db.get_all_tickers()
    else:
        # companies_list = get_local_tickers()
        companies_list = get_index()
        print(companies_list)
        # companies_list = ["^AEX", "NVDA"]
        # companies_list = config.scratch.companies
        # companies_list = ["^AEX", "TSLA", "NVDA"]

    # Then we should download the data from yfinance
    yfmanager = Yfmanager(config=config)
    df = yfmanager.download_companies_yf(companies=companies_list)

    if telegram:
        tm = TelegramManager()
        if df.empty:
            tm.bot_send_text("no data fetched")
        else:
            tm.bot_send_text("data fetched correctly")
            tm.bot_send_text(str(df["Ticker"].unique()))

    if db:
        # Now we have to upload the df to the database
        db.add_df_to_postgresql(df)
    else:
        #         df.reset_index(inplace=True)
        df.to_csv("test_file.csv")
        print("data saved in csv correctly")
