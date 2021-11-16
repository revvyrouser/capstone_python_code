import pandas as pd
import asyncio
import firebase_admin

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from bleak import BleakScanner

df = pd.read_csv (r"C:\Users\magda\Documents\Processing\capstone_data_to_csv_synth\acc_gyro_mag_updated")
df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour", "minute", "second"]],unit="s")
df["del_t"] = df["t_mil"].shift(-1)- df['t_mil']
df = df.dropna()
first_obs_per_second = df.groupby("datetime").first()
#print(first_obs_per_second)
first_obs_per_second.to_csv("./data/first_obs_per_second.csv")
print(df)   

treated_df = pd.DataFrame(columns=['Datetime', 'Time_diff', 'Pos_x', 'Pos_y', 'Pos_z', 'Ang_x', 'Ang_y', 'Ang_z'])
treated_df['Datetime'] = df["datetime"]
treated_df['Time_diff'] = df['del_t']
treated_df['Ang_x'] = df['gyro_x']*df['del_t'] % 360
treated_df['Ang_y'] = df['gyro_y']*df['del_t'] % 360
treated_df['Ang_z'] = df['gyro_z']*df['del_t'] % 360

treated_df['Pos_x'] = df['acc_x']*df['del_t']*df['del_t']/2
treated_df['Pos_y'] = df['acc_y']*df['del_t']*df['del_t']/2
treated_df['Pos_z'] = df['acc_z']*df['del_t']*df['del_t']/2

print(treated_df)
treated_df[["Pos_x", "Pos_y", "Pos_z"]].plot()
plt.title('Roughly Treated Position (Separated)')
fig1 = plt.figure(1)


treated_df[["Ang_x", "Ang_y", "Ang_z"]].plot()
plt.title('Roughly Treated Angle (Separated)')
plt.figure(2)

posplot = plt.figure().gca(projection='3d')
posplot.plot(treated_df['Pos_x'], treated_df['Pos_y'], treated_df['Pos_z'])
posplot.set_xlabel('x')
posplot.set_ylabel('y')
posplot.set_zlabel('z')
plt.title('Roughly Treated Position')
plt.figure(3)

angplot = plt.figure().gca(projection="3d")
angplot.plot(treated_df['Ang_x'], treated_df['Ang_y'], treated_df['Ang_z'])
angplot.set_xlabel('x')
angplot.set_ylabel('y')
angplot.set_zlabel('z')
plt.title('Roughly Treated Angle')

plt.figure(4)
plt.show()

# async def run():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)
#         print('\n')

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())