import pandas as pd
import pygeohash as pgh


def get_hash(lat, long, precision):
    hash = pgh.encode(lat, long, precision)
    return hash


def get_rol_col(df):
    shp = df.shape
    row, col = int(list(shp)[0]), int(list(shp)[1])
    return row, col


print("GEOHASH: ", get_hash(22.4353604, 87.8958015, 7), type(get_hash(22.4353604, 87.8958015, 7)))

df1 = pd.read_csv('master_poi.csv', error_bad_lines=False)
df2 = pd.read_csv('my_poi_final.csv', error_bad_lines=False)

row, col = get_rol_col(df2)
# categories = set(df2.iloc[:]['category'])
# print(categories)
# print(df2.at[0, 'latitude'])
# df2.at[0, 'latitude'] = 78.4567890
# print(df2.at[0, 'latitude'])


# for r in range(0, row):
#     cate = df2.at[r, 'category']
#     # print(cate)
#     lat = df2.at[r, 'latitude']
#     long = df2.at[r, 'longitude']
#     # print("LAT/LNG: ", lat, long, type(lat), type(long))
#
#     precision = 9
#
#     if lat and long:
#         if cate is None:
#             pass
#         elif cate == 'Hotel & Resort':
#             # df2.at[r, 'geohash'] = get_hash(lat, long, precision=7)
#             precision = 7
#             df2.at[r, 'radius'] = 200.0
#
#         elif cate == 'Restaurant':
#             # df2.at[r, 'geohash'] = get_hash(lat, long, precision=9)
#             precision = 9
#             df2.at[r, 'radius'] = 100.0
#
#         elif cate == 'Shopping Mall':
#             # df2.at[r, 'geohash'] = get_hash(lat, long, precision=7)
#             precision = 7
#             df2.at[r, 'radius'] = 300
#
#         elif cate == 'Hospital':
#             # df2.at[r, 'geohash'] = get_hash(lat, long, precision=6)
#             precision = 6
#             df2.at[r, 'radius'] = 300
#
#         elif cate == 'School':
#             # df2.at[r, 'geohash'] = get_hash(lat, long, precision=7)
#             precision = 7
#             df2.at[r, 'radius'] = 300
#
#         hash = get_hash(lat, long, precision)
#         # print(hash, type(hash))
#         df2.loc[r, 'geohash'] = hash


print(df1.shape)
print(df2.shape)
# df2.to_csv('my_poi_final.csv')
condition = df2['name'].isin(df1['name'])
df2.drop(df2[condition].index, inplace=True)
df1_filtered = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
print(df1_filtered.shape)
# df1_filtered.to_excel('main_poi_final.xlsx')

# writing to Excel
datatoexcel = pd.ExcelWriter('main_poi_final.xlsx')

# write DataFrame to excel
df1_filtered.to_excel(datatoexcel)

# save the excel
datatoexcel.save()
