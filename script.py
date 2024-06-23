import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the path to the directory containing the CSV files
data_dir = "ERC20-stablecoins/price_data"

# List of CSV files
csv_files = ["dai_price_data.csv", "pax_price_data.csv", "usdc_price_data.csv", "usdt_price_data.csv", "ustc_price_data.csv"]

# Dictionary to hold dataframes
dfs = {}

# Read each CSV file into a dataframe
for csv_file in csv_files:
    path = os.path.join(data_dir, csv_file)
    df = pd.read_csv(path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    dfs[csv_file.split('_')[0]] = df

# Read event data with specified encoding
event_data_path = "ERC20-stablecoins/event_data.csv"
events_df = pd.read_csv(event_data_path, encoding='latin1')  # Change encoding if needed
events_df['timestamp'] = pd.to_datetime(events_df['timestamp'], unit = 's')
events_df = events_df[(events_df['timestamp'] >= '2022-04-01') & (events_df['timestamp'] <= '2022-06-30')]

# Plot closing prices
plt.figure(figsize=(14, 8))

for key, df in dfs.items():
    plt.plot(df.index, df['close'], label=key)

for _, event in events_df.iterrows():
    plt.axvline(event['timestamp'], color='r', linestyle='--')
    plt.text(event['timestamp'], plt.ylim()[1] - (plt.ylim()[1] * 0.05), 
             f"{event['event']} ({event['type']})", rotation=90, verticalalignment='top',
             fontsize=8, backgroundcolor='white', bbox=dict(facecolor='yellow', alpha=0.5))

plt.title('Closing Prices of Stablecoins and Wrapped Luna with Events')
plt.xlabel('Timestamp')
plt.ylabel('Closing Price')
plt.legend()
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.show()
