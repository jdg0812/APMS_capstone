import sqlite3
import pandas as pd
import yaml

conn = sqlite3.connect('cmapss_dataset.db')
cursor = conn.cursor()

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
col_names = config['col_names']
df = pd.read_csv('CMAPSSData/train_FD001.txt', sep='\s+',
                 header=None, index_col=False, names=col_names)

create_table_query = '''
CREATE TABLE IF NOT EXISTS cmapss_dataset (
    unit_number INTEGER,
    time_cycles INTEGER,
    setting_1 REAL,
    setting_2 REAL,
    setting_3 REAL,
    sensor_1 REAL,
    sensor_2 REAL,
    sensor_3 REAL,
    sensor_4 REAL,
    sensor_5 REAL,
    sensor_6 REAL,
    sensor_7 REAL,
    sensor_8 REAL,
    sensor_9 REAL,
    sensor_10 REAL,
    sensor_11 REAL,
    sensor_12 REAL,
    sensor_13 REAL,
    sensor_14 REAL,
    sensor_15 REAL,
    sensor_16 REAL,
    sensor_17 REAL,
    sensor_18 REAL,
    sensor_19 REAL,
    sensor_20 REAL,
    sensor_21 REAL
)
'''

cursor.execute(create_table_query)

for index, row in df.iterrows():
    insert_query = '''
    INSERT INTO cmapss_dataset VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    data_tuple = tuple(row)
    cursor.execute(insert_query, data_tuple)


# select_query = "SELECT * FROM cmapss_dataset"
# cursor.execute(select_query)
# results = cursor.fetchall()

# for row in results:
#     print(row)

conn.commit()
cursor.close()
conn.close()
