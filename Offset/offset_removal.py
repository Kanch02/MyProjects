import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

final_after_removal_df = pd.DataFrame()
final_removal_values_df = pd.DataFrame()

def remove_zero_sum_subsets(new_list_difference, tolerance=0.8):
    def find_zero_sum_subsets(new_list_difference):
        cumulative_sum = 0
        sum_indices = {0: -1}
        subsets_to_remove = set()
        
        for i, num in enumerate(new_list_difference):
            cumulative_sum += num
            
            for s in list(sum_indices.keys()):
                if abs(cumulative_sum - s) <= tolerance:
                    start_index = sum_indices[s] + 1
                    subsets_to_remove.update(range(start_index, i + 1))
                    break

            sum_indices[cumulative_sum] = i


        return sorted(subsets_to_remove)

    while True:
        indices_to_remove = find_zero_sum_subsets(new_list_difference)
        if not indices_to_remove:
            break
        new_list_difference = [num for i, num in enumerate(new_list_difference) if i not in indices_to_remove]

    return new_list_difference

def run_multiple(new_list_difference):
    for i in range(3):
        new_list_difference = remove_zero_sum_subsets(new_list_difference)

    return new_list_difference


def modify_sourcelist(source, today_file_df):
    with open('currency_list', 'r') as file:
        for line in file:
            currency = line.strip()

            source_df = today_file_df.loc[(today_file_df["Trans Curr"]==currency) & (today_file_df["Source"].str.startswith(source))]
            source_df["Difference"] = source_df["Difference"].astype(float)

            total_list_difference = source_df["Difference"].tolist()
            
            if(source=="9Z5"):
                list_after_removal = run_multiple(total_list_difference)
            else:
                list_after_removal = remove_zero_sum_subsets(total_list_difference)

            after_removal_df = source_df.loc[source_df["Difference"].isin(list_after_removal)]
            removed_values_df = source_df.loc[~source_df["Difference"].isin(list_after_removal)]

            final_after_removal_df = pd.concat([final_after_removal_df, after_removal_df], ignore_index=True)
            final_removal_values_df = pd.concat([final_removal_values_df, removed_values_df], ignore_index=True)

# -----------------------------------------------------------

header_row = 97
today_file = ""
sheetname = "Page1"
today_file_df = pd.read_excel(today_file, header=header_row, sheet_name=sheetname)

print("Starting the OFFSET PROCESS !!!")
print("*" * 30)
print("Before Modification:")
print("Total Value in complete file = ", len(today_file_df["Difference"]))


with open('source_list.txt', 'r') as file:
    for line in file:
        source = line.strip()
        modify_sourcelist(source, today_file_df)