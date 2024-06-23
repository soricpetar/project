import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the path to the directory containing the CSV files
data_dir = "ERC20-stablecoins"

# List of CSV files
csv_files = ["token_transfers.csv"]

# Dictionary to hold dataframes
dfs = {}

# Read each CSV file into a dataframe
for csv_file in csv_files:
    path = os.path.join(data_dir, csv_file)
    df = pd.read_csv(path)
    print(df.columns)

df['time_stamp'] = pd.to_datetime(df['time_stamp'], unit='s')

# Define a mapping for contract addresses to stablecoin labels
contract_address_mapping = {
    '0xdac17f958d2ee523a2206206994597c13d831ec7': 'USDT',
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': 'USDC',
    '0x6b175474e89094c44da98b954eedeac495271d0f': 'DAI',
    '0xa47c8bf37f92abed4a126bda807a7b7498661acd' : 'UST',
    '0x8e870d67f660d95d5be530380d0ec0bd388289e1': 'PAX',
    '0xd2877702675e6ceb975b4a1dff9fb7baf4c91ea9': 'WLUNA',

}
unique_contract_addresses = df['contract_address'].unique()
print("Unique Contract Addresses:")
for address in unique_contract_addresses:
    print(address)

# Map the contract addresses to labels
df['stablecoin'] = df['contract_address'].map(contract_address_mapping)

# Find the 100 biggest transactions
biggest_transactions = df.nlargest(100, 'value')

# Plot the biggest transactions
plt.figure(figsize=(14, 8))

for label, group in biggest_transactions.groupby('stablecoin'):
    plt.scatter(group['time_stamp'], group['value'], label=label)

plt.title('100 Biggest Transactions of Stablecoins')
plt.xlabel('Timestamp')
plt.ylabel('Transaction Value')
plt.legend()
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.show()