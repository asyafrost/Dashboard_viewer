from libraries import pd

'''MERGING DATASETS'''

def load_and_preprocess_csv(file_paths):
    
    
    dataframes = []
    for file_path in file_paths:
        df = pd.read_csv(file_path, sep=";")
        dataframes.append(df)
    
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    combined_df.drop_duplicates(inplace=True)
    combined_df.dropna(inplace=True)

    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], unit='s')
    combined_df['createdAt'] = pd.to_datetime(combined_df['createdAt'])
    combined_df['updatedAt'] = pd.to_datetime(combined_df['updatedAt'])
    

    client_data = combined_df['cycleId'].apply(lambda x: f"{x.split('-')[0]}")
    client_cycle_data = combined_df['cycleId'].apply(lambda x: f"{x.split('-')[0]}-{x.split('-')[2]}")
    combined_df.insert(0, 'client', client_data)
    combined_df.insert(1, 'cycle', client_cycle_data)
    

    return combined_df
