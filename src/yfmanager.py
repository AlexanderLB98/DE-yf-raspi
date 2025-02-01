import pandas as pd
from datetime import date, timedelta
import yfinance as yf

class Yfmanager:
    
    def __init__(self, config):
        self.config = config
    

    def download_companies_yf(self, companies: list, verbose: int = 1) -> pd.DataFrame():
        # Download 2 days of data for each ticker, grouping by 'Ticker' to structure the DataFrame with multi-level columns
        df = yf.download(companies, group_by='Ticker', start=date.today() - timedelta(days=self.config.days_to_fetch), end=date.today())

        # Transform the DataFrame: stack the ticker symbols to create a multi-index (Date, Ticker), then reset the 'Ticker' level to turn it into a column
        df = df.stack(level=0, future_stack=True).rename_axis(['Date', 'Ticker']).reset_index(level=1).reset_index()
        return df


    def download_companies_yf_old(self, companies: list, verbose: int= 1) -> pd.DataFrame():
        df = pd.DataFrame()
        
        for company in companies:
            try:
                data = yf.download(company, start=date.today() - timedelta(days=self.config.days_to_fetch), end=date.today())
                data = data.reset_index()
                data["company_code"] = company
                df = pd.concat([df, data], axis=0)
            except Exception as e:
                print(e)
            
        if verbose > 0:
            print(df.head())
        
        return df    
            
    
