import pandas as pd
from datetime import date, timedelta
import yfinance as yf

class Yfmanager:
    
    def __init__(self, config):
        self.config = config
    
    def download_companies_yf(self, companies: list, verbose: int= 1) -> pd.DataFrame():
        df = pd.DataFrame()

        for company in companies:
            data = yf.download(company, start=date.today() - timedelta(days=self.config.days_to_fetch), end=date.today())
            data = data.reset_index()
            data["company_code"] = company
            df = pd.concat([df, data])
            
        if verbose > 0:
            print(df.head())
        
        return df    
            
    