import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

hub_rec6_file_path = ''
rec6_data = pd.ExcelFile(hub_rec6_file_path)
tracking_dict = {}

for sheet_name in sorted(rec6_data.sheet_names):
    print(f"Processing for {sheet_name}")
    particular_date_sheetdata = pd.read_excel(rec6_data, sheet_name=sheet_name)
    particular_date_sheetdata = particular_date_sheetdata.drop(columns=['Source Balance', 'GL Balance'])
    
    current_rows = set(particular_date_sheetdata.apply(lambda row: " | ".join(row.astype(str)), axis=1))
    
    for row, history in tracking_dict.items():
        if row in current_rows:
            history['present_in'].append(sheet_name)
        else:
            history['removed_on'].append(sheet_name)

    new_rows = current_rows - set(tracking_dict.keys())
    for new_row in new_rows:
        tracking_dict[new_row] = {
            'present_in': [sheet_name],
            'removed_on': [],
        }

changes_df = pd.DataFrame([
    {
        'Row': row,
        'Present In': history['present_in'],
        'Removed On': history['removed_on'],
    }
    for row, history in tracking_dict.items()
])


output_filename = "BreakAnalysis.xlsx"

changes_df_sorted = changes_df.sort_values(by='Row', ascending=True)
changes_df_sorted.to_excel(output_filename, index=False)

print(f"Changes saved to {output_filename}")
print("-"*20)
