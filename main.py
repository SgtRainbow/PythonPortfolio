import os
import sys
from pathlib import Path
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize

class Asset:

    def __init__(self, name, ticker=None):
        self.name = name
        self.ticker = ticker
        self._data = None

    @classmethod
    def __get_txt(self, filepath, *args, **kwargs):
        try:
            path = Path(filepath)
        except Exception as e:
            print(f'{filepath} is not a valid file path!\nError receivied {str(e)}')
            return None

        dep = 'pandas'

        if dep in sys.modules:
            if os.path.exists(path):
                try:
                    if path.suffix[1:4] == 'xls':
                        df = pd.read_excel(path, *args, **kwargs)
                    else:
                        df = pd.read_csv(path, *args, **kwargs)
                
                except:
                    print(f'Unsuccessful read of {path.name}')
                    return None

            else:
                print(f'{path} does not exist!')
                return None
        else:
            raise ImportError(f'{dep} not found - please install and/or import {dep} module')

        return df


    @classmethod
    def __get_call(self, ticker, *args, **kwargs):
        dep = 'yfinance'

        if dep not in sys.modules:
            print(f'Please import {dep} dependency to use Yahoo Finance')
            return None
        
        try:
            print(f'Loading started for {ticker}')
            df = yf.download(ticker, *args, **kwargs)
        
        except Exception as e:
            print(f'Error occured during data download from Yahoo\nError message: {str(e)}')
            return None

        return df

    @property
    def data(self):
        if self._data is not None:
            return self._data
        else:
            print(f'No data loaded for {self.name} - please use get_data method first or pass DataFrame to data')

    @data.setter
    def data(self, df):
        if not isinstance(df, pd.DataFrame):
            print('Please pass pandas DataFrame for data attribute of an Asset')
        else:
            self._data = df
    
    def get_data(self, method, filepath=None, start=None, end=None, *args, **kwargs):
        """
        Retrieves asset's data based on selected method (API call, txt file)

        Params
        ------

        method : string
            Selected method to retrieve asset's data - API (default) or File
        
        filepath : string / Path
            if File method is selected, uses filepath to read the file using Pandas

        start : string
            for API method, starting date from which data will be retrieved in YYYY-MM-DD format
        
        end : string 
            for API method, end date until which data will be retrieved in YYYY-MM-DD format

        *args, **kwargs : to be passed for pandas reader / yfinance API GET

        Returns
        -------

        pandas DataFrame
        """

        if method == 'API':
            if self.ticker is not None:
                df = self.__get_call(self.ticker, start, end)
            else:
                print(f'Ticker is not passed for {self.name} asset - pass ticker to use API method')
                return None

        elif method == 'File' and filepath:
            df = self.__get_txt(filepath, *args, **kwargs)

        else:
            print(f'Incorrect method passed ({method}) - please select API (for Yahoo) or File with filepath')
            return None

        # Setter call
        self.data = df
        
        return df
        

if __name__ == '__main__':
    print(f'Python version: {sys.version}')

    # Creating instance for Microsoft stock
    msft = Asset('Microsoft', ticker='MSFT')

    # TODO: debug call of data attribute
    print(msft.data)

    # Loading data from a txt file
    msft.get_data(method='File',\
        filepath='/Users/shuyaxu/Desktop/Python Project/data/msft.txt',\
        sep='\t')

    # TODO: debug call of data
    print(msft.data)

    # Apple stock
    appl = Asset('Apple', ticker='aapl')

    # calling Yahoo Finance API for stock data
    appl.get_data('API', start='2020-09-01', end='2020-09-20')

    # data attribute check
    print(appl.data)


    