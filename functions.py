from libraries import stats, np

"""FUNCTIONS FOR CALCULATING METRICS"""

#Памагити, оно работает, но не работает
def calculate_kde(data):
    try:
        kde = stats.gaussian_kde(data)  
        kde_factor = np.mean(kde(data))  
        #print(kde_factor)
        return kde_factor  
    except Exception as e:
        print("Error in calculate_kde:", e) 
        return np.nan

def calculate_mae(data):
    mean_value = np.mean(data) 
    mae = np.mean(np.abs(data - mean_value))
    mae = float(mae)
    #print(mae)  
    return mae  

def aggregate_mean(data):
    return data.groupby(['cycleId', 'age']).mean().reset_index()