import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mendefiniskan dataframe baru
def total_monthly(df):
    return df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

def total_hourly(df):
    return df.groupby('hr')['cnt'].sum().reset_index()

def average_seasonly(df):
    return df.groupby(['season'])['cnt'].mean().reset_index().reset_index().sort_values('cnt', ascending=False, ignore_index=True)

# Membaca file CSV
df = pd.read_csv('cleaned_data.csv')

#Mengubah tipe date
date_in_day = ["dteday"]

for column in date_in_day:
  df[column]=pd.to_datetime(df[column])

# Fitur Filtering
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Ex-companyLogo.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Select time range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['dteday'] >= str(start_date)) & (df['dteday'] <= str(end_date))]

# Header
st.header('Bike Sharing Dashboard')

st.subheader('Total Bike Rental')
sum_cnt = main_df['cnt'].sum()
formatted_sum_cnt = "{:,.0f}".format(sum_cnt).replace(',', '.')
st.metric('Total Rental Bike in {start_date} to {end_date}'.format(start_date=start_date, end_date=end_date), formatted_sum_cnt)

# Rata-rata banyaknya bike rental each day
st.subheader('Average Bike Rental Daily')

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Membuat kolom untuk menampilkan metrik
cols = st.columns(7)

for i, day in enumerate(days_of_week):
    col = cols[i % 7]
    with col:
        try:
            avg_rental = int(round(main_df[main_df['weekday'] == day]['cnt'].mean(), 0))
        except ValueError:
            avg_rental = 0
        st.metric(day, avg_rental)

# Total Rental Bike Monthly
col8, col9 = st.columns([1, 1])

with col8:
    st.subheader('Sum Bike Rental by Month')

# Pemilihan Month
with col9:
    if start_date.year == end_date.year:
        year = start_date.year
    else:
        year = st.selectbox('Year', ('2011 & 2012', '2011', '2012'))

# Plot line chart
fig, ax = plt.subplots(figsize=(16, 8))
plt.style.use("dark_background")

if year == '2011 & 2012':
    total_monthly = total_monthly(main_df)
    sns.lineplot(data=total_monthly, x="mnth", y="cnt", hue="yr", errorbar=None, marker="o", palette=['blue','yellow'])
else:
    total_monthly = total_monthly(main_df)
    sns.lineplot(data=total_monthly[total_monthly['yr'] == int(year)], x="mnth", y="cnt", hue="yr", errorbar=None, marker="o", palette=['blue' if year == '2011' else 'yellow'])

# Memberi ticks pada sumbu x sesuai urutan bulan
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Memberi label pada sumbu x dan y
plt.xlabel('Month')
plt.ylabel('Total Rental')
plt.grid()
st.pyplot(fig)

#Total Bike Rental Hourly
col10, col11 =st.columns([1,1])

with col10:
    st.subheader('Sum Bike Rental by Hour')

with col11:
    values = st.slider('Range hour',0, 23, (0,23))
    start_hour, end_hour = values

total_hourly=total_hourly(main_df)
fig, ax = plt.subplots(figsize=(16, 8))
plt.style.use("dark_background")
sns.lineplot(data=total_hourly[(df['hr'] >= start_hour)&(df['hr'] <= end_hour)], x="hr", y="cnt", errorbar=None, marker="o", palette='blue')

# Memberi label pada sumbu x dan y
plt.xlabel("Hour")
plt.ylabel("Total Rental Bike")

plt.xticks([i for i in range(start_hour, end_hour+1)])
plt.grid()
st.pyplot(fig)

#Rata-rata bike rental each season
st.subheader('Average Rental Bike by Season')
    
# Plot line chart
fig, ax = plt.subplots(figsize=(16, 8))
plt.style.use("dark_background")
average_seasonly = average_seasonly(main_df)
sns.barplot(data=average_seasonly, x="season", y="cnt", errorbar=None, color='blue')

# Memberi label pada sumbu x dan y
plt.xlabel('Season')
plt.ylabel('Average Rental')

st.pyplot(fig)
