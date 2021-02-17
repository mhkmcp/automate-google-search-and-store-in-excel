import pandas as pd

df1 = pd.read_csv('BD_lookup_table.csv', error_bad_lines=False)

# df_dhk = df1.loc[:, 'division'] ==

rows = int(str(df1.shape)[1:-1].split(', ')[0])
df_dhaka = pd.DataFrame()
print(df1.shape)
print(rows, type(rows))
count = 0
data = {
    'geohash': [],
    'country': [],
    'division': [],
    'district': [],
    'thana': [],
    'union': []
}


df_dhk = df1[df1['division'] == 'Dhaka']
df_dhk.to_csv('BD_dhaka_lookup_table.csv')
print(df_dhk.shape)

# df1_dhk = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)


# for row in range(1, rows):
#     if df1.loc[row, 'division'].lower() == 'dhaka':
#         count += 1
#         print(df1.loc[row, 'division'])

# print(df1.shape, val)

print(count)
