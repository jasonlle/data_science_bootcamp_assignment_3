import pandas as pd
import matplotlib.pyplot as plt

#1
url = "https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=DOWNLOAD"
df = pd.read_csv(url)

weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
df['hour_beginning'] = pd.to_datetime(df['hour_beginning'])
df['Pedestrians'] = pd.to_numeric(df['Pedestrians'])
weekdays = df[df['hour_beginning'].dt.dayofweek < 5]

weekdays['Weekdays'] = weekdays['hour_beginning'].dt.day_name()
pedestrian_per_day = weekdays.groupby('Weekdays')['Pedestrians'].sum()
pedestrian_per_day = pedestrian_per_day.reindex(weekdays_order)

#plt.figure(figsize=(10, 6))
#plt.plot(pedestrian_per_day.index, pedestrian_per_day.values, marker='o', linestyle='-')
#plt.title('Weekday Count of Pedestrian Crossing of Bk Bridge')
#plt.xlabel('Days of the Week (M-F)')
#plt.ylabel('Pedestrian Count (X * 10^6)')
#plt.show()

#2
import seaborn as sns
data_2019 = df[df['hour_beginning'].dt.year == 2019]
data_2019['weather_summary'] = data_2019['weather_summary'].fillna(method='ffill')
encoded_weather = pd.get_dummies(data_2019['weather_summary'], prefix= 'Weather')
data_2019_encoded = pd.concat([data_2019, encoded_weather], axis=1)

correlation_matrix = data_2019_encoded[['Pedestrians'] + list(encoded_weather.columns)].corr()

#plt.figure(figsize=(10, 6))
#sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
#plt.title('HeatMap Between Weather Conditions and Pedestrian Counts for the Year 2019')
#plt.tight_layout()
#plt.show()

#3
time_list = ['Morning', 'Afternoon', 'Evening', 'Night']
def categorize_time(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'
    
df['Time'] = df['hour_beginning'].dt.hour.apply(categorize_time)
pedestrian_by_time = df.groupby('Time')['Pedestrians'].sum()
pedestrian_by_time = pedestrian_by_time.reindex(time_list)

plt.figure(figsize=(10,6))
pedestrian_by_time.plot(kind='bar', color='orange')
plt.title('Pedestrian Count by Time of Day')
plt.xlabel('Time')
plt.ylabel('Pedestrian Count (X * 10^6)')
plt.tight_layout()
plt.show()


