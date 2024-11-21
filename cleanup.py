import pandas as pd

def format_date(save_path):
    try:
        df = pd.read_csv(save_path)
        # Rename the 'Unnamed: 0' column to 'Date'
        df = df.rename(columns={'Unnamed: 0': 'DateTime'})
        # Convert the 'DateTime' column to datetime format
        df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')

        # Extract only the date part
        df['Date'] = df['DateTime'].dt.date

        # df = df.rename(columns={'DateTime': 'Date'})
        df = df.drop(columns=['DateTime'])
        # print(df)
        # Drop the 'Date' column if no longer needed
        # Ensure 'Date' column is the first one
        columns = ['Date'] + [col for col in df.columns if col != 'Date']

        # Reindex the DataFrame to rearrange columns
        df = df[columns]

        print(df.head())
        df.to_csv(save_path, index=False)
    except Exception as e:
        print("Error while formatting the date: ", e)