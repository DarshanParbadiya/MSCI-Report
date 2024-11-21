import pandas as pd
from cleaning_data_functions import MRC_data_parser,read_inputs
from filtering_data_functions import get_result,get_relevant_data
from save_filtered_data_to_csv import save_the_result_to_excel
from datetime import datetime
import os
from cleanup import format_date

# write function to validate paths
def validate_paths(*args):
    for path in args:
        if not os.path.exists(path):
            print(f"Path {path} does not exist.")
            exit()

#-------------------------Generate Dynamic FileName --------------------------------
today = datetime.today()
last_BD_prior_month = (today.replace(day=1) - pd.offsets.BDay(1)).strftime('%Y%m%d')
just_MMDD = last_BD_prior_month[4:]
ref_date = '0628' #dummy for testing
ref_date2 = '20240628' #dummy for testing
static_file_name = '_15290_'

#-------------------------File Paths --------------------------------
master_file_path = r'C:\Users\dparbadiya\OneDrive - AIC Global Holdings\Desktop\Benchmark file inputs\FRO\MSCI'

dm_file = os.path.join(master_file_path, ref_date + 'd_dm.mrc', ref_date + 'D_DM.MRC') #MSCI Developed markets 
em_file = os.path.join(master_file_path, ref_date + 'd_em.mrc', ref_date + 'D_EM.MRC') #MSCI enhanced markets 
custom_file = os.path.join(master_file_path, ref_date2 + '_' + ref_date2 + f'd{static_file_name}', ref_date2 + '_' + ref_date2 + f'_D{static_file_name}') #MSCI custom markets 
benchmark_file = os.path.join(master_file_path, 'Benchmark Performance.xlsx')
save_path = os.path.join(master_file_path, "Output" ,f'Benchmark Performance updated.csv')

#-------------------------Validate Paths--------------------------------
validate_paths(dm_file, em_file, custom_file, benchmark_file)


# benchmark_dataframe = pd.read_excel(benchmark_file)

# -------------------------Configuration--------------------------------
merged_dataframe = MRC_data_parser(dm_file, em_file)
benchmark_excel_dataframe = pd.read_excel(benchmark_file) 
additional_datapoints_file = custom_file

# This commented code block is performing the following actions:
# get the row index 2 
index_arr = list(benchmark_excel_dataframe.iloc[0])[1:]
index_arr = [int(x) for x in index_arr]

# get the row index 3
currency_arr= list(benchmark_excel_dataframe.iloc[1])[1:]
currency_arr = [str(x).strip() for x in currency_arr if str(x) != 'nan']

print(index_arr)
print(currency_arr)
if len(index_arr) != len(currency_arr):
    print("Length of index array and currency array should be same")
    exit()
else:
    cleaned_data = get_relevant_data(merged_dataframe)
    filtered_data = get_result(index_arr,currency_arr,cleaned_data)
    print(filtered_data)
    try:
        save_the_result_to_excel(benchmark_excel_dataframe,filtered_data,additional_datapoints_file,save_path)
        format_date(save_path)
    except Exception as e:
        print("Error while saving the data to the benchmark file: ",e)
        exit()
