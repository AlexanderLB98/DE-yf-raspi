"""_summary_
Here I will generate the pipeline that should be done
"""

from src.yfmanager import Yfmanager
from src.dbmanager import DbManager
from src.aux.utils import DotDict

import json

def pipeline():
    
    config_file ="config.json"

    with open(config_file) as f:
        config = DotDict(json.load(f))
        print(config)
        
        
    db = DbManager()
    
    # First we should get a list with the companies from de DB 
    companies_list = db.get_all_tickers()
    # companies_list = ["^AEX", "TSLA", "NVDA"]
    
    # Then we should download the data from yfinance
    yfmanager = Yfmanager(config=config)
    df = yfmanager.download_companies_yf(companies=companies_list)
    
    # Now we have to upload the df to the database
    db.add_df_to_postgresql(df)
    