import pandas as pd
import glob

files = [f for f in glob.glob('*.csv') if 'combined' not in f]
df_list = []

for file in files:
    df = pd.read_csv(file)
    name = file.replace('_attention_binding.csv', '')
    parts = name.split('_', 1)
    df['model'] = parts[0]
    df['compound'] = parts[1]
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv('combined_binding_data.csv', index=False)
print(f"Combined {len(files)} files, {len(combined_df)} rows")
print(combined_df.head(10))
