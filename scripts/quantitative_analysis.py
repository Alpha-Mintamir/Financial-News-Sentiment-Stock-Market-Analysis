

import pandas as pd
import talib
import matplotlib.pyplot as plt


def load_and_merge_data(file_paths):
    """
    Load and merge CSV files into a single DataFrame.
    """
    data_frames = []
    for company, file_path in file_paths.items():
        df = pd.read_csv(file_path)
        df['Company'] = company  # Add a column for the company name
        data_frames.append(df)

    merged_df = pd.concat(data_frames, ignore_index=True)
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date', 'Company']
    if not all(col in merged_df.columns for col in required_columns):
        raise ValueError('Data does not contain the required columns')

    merged_df['Date'] = pd.to_datetime(merged_df['Date'])
    merged_df.set_index('Date', inplace=True)
    merged_df.sort_index(inplace=True)
    
    return merged_df

def calculate_indicators(df):
    """
    Calculate technical indicators and add them to the DataFrame.
    """
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df

def plot_stock_data(df, company):
    """
    Plot stock data and technical indicators for a specific company.
    """
    company_df = df[df['Company'] == company]
    
    plt.figure(figsize=(14, 7))
    plt.plot(company_df['Close'], label='Close Price', color='blue')
    plt.plot(company_df['SMA_20'], label='SMA 20', color='red')
    plt.plot(company_df['SMA_50'], label='SMA 50', color='green')
    plt.title(f'{company} Stock Price and Moving Averages')
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(14, 7))
    plt.plot(company_df['RSI'], label='RSI', color='purple')
    plt.title(f'{company} Relative Strength Index (RSI)')
    plt.legend()
    plt.show()
    
    plt.figure(figsize=(14, 7))
    plt.plot(company_df['MACD'], label='MACD', color='blue')
    plt.plot(company_df['MACD_signal'], label='MACD Signal', color='red')
    plt.bar(company_df.index, company_df['MACD_hist'], label='MACD Histogram', color='grey', alpha=0.5)
    plt.title(f'{company} MACD and MACD Signal')
    plt.legend()
    plt.show()

