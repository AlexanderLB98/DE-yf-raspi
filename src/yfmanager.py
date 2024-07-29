import pandas as pd
from datetime import date, timedelta
import yfinance as yf

class Yfmanager:
    
    def __init__(self):
        pass
    
    def download_companies_yf(self, companies: list, dt_days: int = 1, verbose: int= 1) -> pd.DataFrame():
        df = pd.DataFrame()

        for company in companies:
            data = yf.download(company, start=date.today() - timedelta(days=dt_days), end=date.today())
            data = data.reset_index()
            data["company_code"] = company
            df = pd.concat([df, data])
            
        if verbose > 0:
            print(df.head())
        
        return df    
            
    