import pandas as pd  # type: ignore
from itertools import combinations

def find_opposite_values_offsetting_transactions(group):
    seen = {}
    to_close = set()
    for idx, amount in zip(group.index, group["Transaction Amount"]):
        if -amount in seen:
            to_close.add(idx)
            to_close.add(seen[-amount])
            del seen[-amount]
        else:
            seen[amount] = idx
            group.loc[group.index.isin(to_close), "Status"] = "Closed"

    return group

def find_entire_group_sum_zero(group, tolerance=0.5):
    total_sum = abs(group['Transaction Amount'].sum())
    if total_sum <= tolerance:
        group["Status"] = "Closed"
    return group

def find_valid_subsets(numbers, indices, max_iterations=None, tolerance=0.5): 
    valid_subsets = [] 
    n =-len(numbers) 
    iteration_count = 0 
    used_indices = set() 
    for r in range(2, n + 1): 
        for combo in combinations(range(n), r): 
            iteration_count += 1 
            if max_iterations and iteration_count > max_iterations:
                print(f"Reached max iterations: {max_iterations} for subset size {n}. Moving on")
                return valid_subsets
            
            if any(idx in used_indices for idx in combo):
                continue

            current_sum = round(sum(numbers[i] for i in combo), 6)
            if abs(current_sum) < tolerance:  
                subset_combination = [(numbers[i], indices[i]) for i in combo]  
                valid_subsets.append([indices [i] for i in combo])  
                print(f"Subset found with sum zero: {subset_combination}")  
                used_indices.update(combo)  
    return valid_subsets

def offest(sheet_df, direct_counter, subset_counter):
    fund_df = sheet_df[(sheet_df['Remarks'].isnull())].copy()
    
    num_rows = fund_df.shape[0]
    print(f"Number of rows: {num_rows}")

    fund_df['offset'] = '' # Initialize the offset? Adj? column 
    fund_df['offset_type'] = '' # Initialize the offset? Adj? type column 
    amounts = fund_df['Transaction Amount'].tolist() 

    # Check for direct offset? Adj?s 
    indices = list(fund_df.index) 
    used_indices = set() 
    
    for i, amt in enumerate(amounts): 
        if i in used_indices or amt == 0: 
            continue 
        for j in range(i + 1, len(amounts)): 
            if j in used_indices: 
                continue 
            if abs(amounts[j] + amt) < 0.9: # Check if sum is zero considering tolerance 
                fund_df.at[indices[i], 'offset'] = 'offset'
                fund_df.at[indices[j], 'offset'] = 'offset' 
                fund_df.at[indices[i], 'offset_type'] = f'direct {direct_counter}' 
                fund_df.at[indices[j], 'offset_type'] = f'direct {direct_counter}' 
                direct_counter = direct_counter + 1 
                used_indices.update([i, j]) 
                print(f"Direct match found: ({amt}, {indices[i]}) and ({amounts[j]}, {indices[j]})") 
                break

            # Remaining amounts after direct matches 
    remaining_amounts = [amt for i, amt in enumerate(amounts) if i not in used_indices] 
    remaining_indices = [idx for i, idx in enumerate(indices) if i not in used_indices] 
    print(remaining_amounts) 
    print(remaining_indices)

    subset_size =  len(remaining_amounts)
    if subset_size <= 20: 
        max_iterations = None
    else: 
        max_iterations = 500000
    subsets = find_valid_subsets(remaining_amounts, remaining_indices, max_iterations) 

    for subset in subsets: 
        subset_combination = [(remaining_amounts[remaining_indices.index(i)], i) for i in subset] 
        print(f"Subset (subset_counter) found: {subset_combination}") 
        for i in subset: 
            fund_df.at[i, 'offset'] = 'offset' 
            fund_df.at[i, 'offset_type'] = f'subset {subset_counter}' 
        subset_counter += 1

    for index, row in fund_df.iterrows():
        if row['offset'] == 'offset':
            sheet_df.loc[index, 'Status'] = "Closed"

    return sheet_df


fx_file = ""
fx_file_df = pd.read_excel(fx_file)
fx_file_df["Transaction Currency"] = fx_file_df["Transaction Currency"].replace(["=", '"'], "", regex=True)
fx_file_df["Status"] = "Open"

# Step 1: Making all the Zero values Closed
fx_file_df.loc[fx_file_df["Transaction Amount"] == 0, 'Status'] = "Closed"

# Step 2: For each group when the entire group sum is zero, close all transactions in that group
fx_file_df = fx_file_df.groupby(["Workstation ID", "Transaction Currency"], group_keys=False).apply(find_entire_group_sum_zero)

# Step 3: For each group, find opposite values offsetting transactions and close them
fx_file_df = fx_file_df.groupby(["Workstation ID", "Transaction Currency"], group_keys=False).apply(find_opposite_values_offsetting_transactions)

# We are seperating the closed and open status transactions for further processing
# Since we are seperating we can process quickly with the open status transactions
fx_file_closed_status_df = fx_file_df[fx_file_df["Status"] == "Closed"]
fx_file_open_status_df = fx_file_df[fx_file_df["Status"] == "Open"]


# Now processing with the open status transactions with combination logic
fx_file_open_status_df["Remarks"] = None

processed_groups = []

unique_groups = fx_file_open_status_df[["Workstation ID", "Transaction Currency"]].drop_duplicates()
for index, row in unique_groups.iterrows():
    print(f"Workstation ID: {row['Workstation ID']}, Transaction Currency: {row['Transaction Currency']}")
    ws_id = row["Workstation ID"]
    currency = row["Transaction Currency"]
    
    group_df = fx_file_open_status_df[
        (fx_file_open_status_df["Workstation ID"] == ws_id) & 
        (fx_file_open_status_df["Transaction Currency"] == currency)
    ]
    processed_group_df = offest(group_df,1,1)
    processed_groups.append(processed_group_df)

new_closed_fx_file_df = pd.concat(processed_groups, ignore_index=True)

# Now we got new_fx_file_open_status_df with the offsetting transactions closed
# Merge the closed status transactions with the new open status transactions

new_fx_file_df = pd.concat([fx_file_closed_status_df, new_closed_fx_file_df], ignore_index=True)


output_file = ""
new_fx_file_df.to_excel(output_file, index=False)
print("Process completed successfully!")  
