import pandas as pd

df = pd.read_csv('bd_v2_main_final.csv', error_bad_lines=False)
df.drop(df[df['geohash'] == 0].index, inplace=True)
# df.drop(df[df['latitude'] < 21].index, inplace=True)
# df.drop(df[df['latitude'] > 24].index, inplace=True)
#
# df.drop(df[df['longitude'] < 88].index, inplace=True)
# df.drop(df[df['longitude'] > 93].index, inplace=True)
# df.dropna(subset=["latitude", "longitude"], inplace=True)
# & (df['latitude'] < 21) &
#     (df['longitude'] < 88) & (df['longitude'] > 93)
#
# index_names = df[(df['latitude'] < 21)].index
#
# df = df.drop(index_names, inplace=True)
# print(index_names)
# print(df.head())

# 200	fmvq7dx	Mid	Hotel & Resort
# 300	wh0kp5	Low	Hospital
# 300	wh0r39g		School
# 300	9vu0p85	Low	Shopping Mall
# 100	tek6pe2rt	High	Restaurant

# df.drop(df[df['longitude'].isnull()])
to_excel = pd.ExcelWriter('bd_v2_main_final.xls')
# write DataFrame to excel
# df.to_csv('bd_v2_main_final.csv')

# save the excel
to_excel.save()
